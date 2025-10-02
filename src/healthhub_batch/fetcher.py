# src/healthhub_batch/fetcher.py
# Oura APIからデータを取得し、データベースに保存するメインロジック
# 複数エンドポイントを並列で取得し、Pydanticモデルでパース、Repositoryで保存
# RELEVANT FILES: oura_client.py, cli.py, repository.py, models.py

"""Data fetching orchestration for Oura Ring API."""
from __future__ import annotations

import asyncio
from typing import Any
from uuid import UUID

import structlog

from healthhub_batch.config import Settings
from healthhub_batch.database import Database
from healthhub_batch.models import (
    DailyActivity,
    DailyReadiness,
    DailyResilience,
    DailySleep,
    DailyStress,
)
from healthhub_batch.oura_client import OuraClient
from healthhub_batch.repository import HealthDataRepository

logger = structlog.get_logger(__name__)


async def fetch_all_data(
    start_date: str, end_date: str, settings: Settings
) -> dict[str, Any]:
    """Fetch all daily summaries from Oura API (raw response).

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        settings: Application settings

    Returns:
        Dictionary with all fetched data by endpoint
    """
    results: dict[str, Any] = {}

    async with OuraClient(settings.oura_pat) as client:
        logger.info("fetch_started", start_date=start_date, end_date=end_date)

        # 各エンドポイントからデータ取得
        tasks = {
            "daily_sleep": client.get_daily_sleep(start_date, end_date),
            "daily_activity": client.get_daily_activity(start_date, end_date),
            "daily_stress": client.get_daily_stress(start_date, end_date),
            "daily_resilience": client.get_daily_resilience(start_date, end_date),
            "daily_readiness": client.get_daily_readiness(start_date, end_date),
        }

        # 並列実行
        completed = await asyncio.gather(*tasks.values(), return_exceptions=True)

        # 結果を整理
        for endpoint, result in zip(tasks.keys(), completed):
            if isinstance(result, Exception):
                logger.error("fetch_failed", endpoint=endpoint, error=str(result))
                results[endpoint] = {"error": str(result)}
            else:
                results[endpoint] = result
                logger.info(
                    "fetch_success",
                    endpoint=endpoint,
                    records=len(result.get("data", [])),
                )

        logger.info("fetch_completed", total_endpoints=len(results))

    return results


async def fetch_and_save_data(
    start_date: str, end_date: str, settings: Settings, db: Database
) -> dict[str, int]:
    """
    Oura APIからデータを取得し、データベースに保存

    Args:
        start_date: 開始日 (YYYY-MM-DD)
        end_date: 終了日 (YYYY-MM-DD)
        settings: アプリケーション設定
        db: データベースインスタンス

    Returns:
        エンドポイントごとの保存件数
    """
    # USER_IDの取得
    user_id = UUID(settings.user_id)
    logger.info("fetch_and_save_started", user_id=str(user_id))

    # APIからデータ取得
    raw_data = await fetch_all_data(start_date, end_date, settings)

    # Pydanticモデルでパース
    parsed_data = {
        "sleep": [],
        "activity": [],
        "readiness": [],
        "stress": [],
        "resilience": [],
    }

    # Sleep
    if "daily_sleep" in raw_data and "data" in raw_data["daily_sleep"]:
        try:
            parsed_data["sleep"] = [
                DailySleep(**item) for item in raw_data["daily_sleep"]["data"]
            ]
            logger.info("sleep_parsed", count=len(parsed_data["sleep"]))
        except Exception as e:
            logger.error("sleep_parse_error", error=str(e))

    # Activity
    if "daily_activity" in raw_data and "data" in raw_data["daily_activity"]:
        try:
            parsed_data["activity"] = [
                DailyActivity(**item) for item in raw_data["daily_activity"]["data"]
            ]
            logger.info("activity_parsed", count=len(parsed_data["activity"]))
        except Exception as e:
            logger.error("activity_parse_error", error=str(e))

    # Readiness
    if "daily_readiness" in raw_data and "data" in raw_data["daily_readiness"]:
        try:
            parsed_data["readiness"] = [
                DailyReadiness(**item) for item in raw_data["daily_readiness"]["data"]
            ]
            logger.info("readiness_parsed", count=len(parsed_data["readiness"]))
        except Exception as e:
            logger.error("readiness_parse_error", error=str(e))

    # Stress
    if "daily_stress" in raw_data and "data" in raw_data["daily_stress"]:
        try:
            parsed_data["stress"] = [
                DailyStress(**item) for item in raw_data["daily_stress"]["data"]
            ]
            logger.info("stress_parsed", count=len(parsed_data["stress"]))
        except Exception as e:
            logger.error("stress_parse_error", error=str(e))

    # Resilience
    if "daily_resilience" in raw_data and "data" in raw_data["daily_resilience"]:
        try:
            parsed_data["resilience"] = [
                DailyResilience(**item) for item in raw_data["daily_resilience"]["data"]
            ]
            logger.info("resilience_parsed", count=len(parsed_data["resilience"]))
        except Exception as e:
            logger.error("resilience_parse_error", error=str(e))

    # データベースに保存
    save_counts = {}
    try:
        async with db.session() as session:
            repo = HealthDataRepository(session, user_id)

            save_counts["sleep"] = await repo.upsert_sleep_data(parsed_data["sleep"])
            save_counts["activity"] = await repo.upsert_activity_data(
                parsed_data["activity"]
            )
            save_counts["readiness"] = await repo.upsert_readiness_data(
                parsed_data["readiness"]
            )
            save_counts["stress"] = await repo.upsert_stress_data(parsed_data["stress"])
            save_counts["resilience"] = await repo.upsert_resilience_data(
                parsed_data["resilience"]
            )

        logger.info("fetch_and_save_completed", save_counts=save_counts)
        return save_counts
    finally:
        await db.close()


def print_summary(results: dict[str, Any]) -> None:
    """Print a summary of fetched data.

    Args:
        results: Fetched data dictionary
    """
    print("\n=== Oura API Fetch Summary ===")
    for endpoint, data in results.items():
        if "error" in data:
            print(f"[ERROR] {endpoint}: ERROR - {data['error']}")
        else:
            records = data.get("data", [])
            print(f"[OK] {endpoint}: {len(records)} records")

            # サンプルデータを表示
            if records:
                sample = records[0]
                print(f"   Sample fields: {list(sample.keys())[:5]}...")
                if "day" in sample:
                    print(f"   Date: {sample['day']}")
                if "score" in sample:
                    print(f"   Score: {sample.get('score', 'N/A')}")

    print("\n" + "=" * 30 + "\n")