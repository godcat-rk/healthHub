# src/healthhub_batch/fetcher.py
# Oura APIからデータを取得するメインロジック
# 複数エンドポイントを並列で取得し、結果をログ出力
# RELEVANT FILES: oura_client.py, cli.py, config.py

"""Data fetching orchestration for Oura Ring API."""
from __future__ import annotations

import asyncio
from typing import Any

import structlog

from healthhub_batch.config import Settings
from healthhub_batch.oura_client import OuraClient

logger = structlog.get_logger(__name__)


async def fetch_all_data(
    start_date: str, end_date: str, settings: Settings
) -> dict[str, Any]:
    """Fetch all daily summaries from Oura API.

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


def print_summary(results: dict[str, Any]) -> None:
    """Print a summary of fetched data.

    Args:
        results: Fetched data dictionary
    """
    print("\n=== Oura API Fetch Summary ===")
    for endpoint, data in results.items():
        if "error" in data:
            print(f"❌ {endpoint}: ERROR - {data['error']}")
        else:
            records = data.get("data", [])
            print(f"✅ {endpoint}: {len(records)} records")

            # サンプルデータを表示
            if records:
                sample = records[0]
                print(f"   Sample fields: {list(sample.keys())[:5]}...")
                if "day" in sample:
                    print(f"   Date: {sample['day']}")
                if "score" in sample:
                    print(f"   Score: {sample.get('score', 'N/A')}")

    print("\n" + "=" * 30 + "\n")