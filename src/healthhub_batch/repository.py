# src/healthhub_batch/repository.py
# データ保存ロジック（Repositoryパターン）
# Pydanticモデルからデータベースへの変換・upsert処理を提供
# RELEVANT FILES: db_models.py, models.py, database.py

from datetime import date
from typing import Any
from uuid import UUID

import structlog
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from healthhub_batch.db_models import (
    DailyActivitySummary,
    DailyReadinessSummary,
    DailyResilienceSummary,
    DailySleepSummary,
    DailyStressSummary,
)
from healthhub_batch.models import (
    DailyActivity,
    DailyReadiness,
    DailyResilience,
    DailySleep,
    DailyStress,
)

logger = structlog.get_logger()


class HealthDataRepository:
    """ヘルスデータのリポジトリクラス"""

    def __init__(self, session: AsyncSession, user_id: UUID):
        """
        Args:
            session: データベースセッション
            user_id: ユーザーID
        """
        self.session = session
        self.user_id = user_id

    async def upsert_sleep_data(self, sleep_data: list[DailySleep]) -> int:
        """
        睡眠データをupsert（存在すれば更新、なければ挿入）

        Args:
            sleep_data: 睡眠データのリスト

        Returns:
            int: 保存したレコード数
        """
        if not sleep_data:
            return 0

        saved_count = 0
        for item in sleep_data:
            values = {
                "user_id": self.user_id,
                "day": item.day,
                "score": item.score,
                "contributors_deep_sleep": item.contributors.deep_sleep,
                "contributors_efficiency": item.contributors.efficiency,
                "contributors_latency": item.contributors.latency,
                "contributors_rem_sleep": item.contributors.rem_sleep,
                "contributors_restfulness": item.contributors.restfulness,
                "contributors_timing": item.contributors.timing,
                "contributors_total_sleep": item.contributors.total_sleep,
                "source_timestamp": item.timestamp,
                "document_id": UUID(item.id),
            }

            stmt = insert(DailySleepSummary).values(**values)
            stmt = stmt.on_conflict_do_update(
                index_elements=["user_id", "day"],
                set_={
                    "score": stmt.excluded.score,
                    "contributors_deep_sleep": stmt.excluded.contributors_deep_sleep,
                    "contributors_efficiency": stmt.excluded.contributors_efficiency,
                    "contributors_latency": stmt.excluded.contributors_latency,
                    "contributors_rem_sleep": stmt.excluded.contributors_rem_sleep,
                    "contributors_restfulness": stmt.excluded.contributors_restfulness,
                    "contributors_timing": stmt.excluded.contributors_timing,
                    "contributors_total_sleep": stmt.excluded.contributors_total_sleep,
                    "source_timestamp": stmt.excluded.source_timestamp,
                    "document_id": stmt.excluded.document_id,
                },
            )

            await self.session.execute(stmt)
            saved_count += 1

        logger.info("sleep_data_upserted", count=saved_count)
        return saved_count

    async def upsert_activity_data(self, activity_data: list[DailyActivity]) -> int:
        """
        活動データをupsert

        Args:
            activity_data: 活動データのリスト

        Returns:
            int: 保存したレコード数
        """
        if not activity_data:
            return 0

        saved_count = 0
        for item in activity_data:
            values = {
                "user_id": self.user_id,
                "day": item.day,
                "score": item.score,
                "steps": item.steps,
                "active_calories": item.active_calories,
                "total_calories": item.total_calories,
                "target_calories": item.target_calories,
                "equivalent_walking_distance": item.equivalent_walking_distance,
                "high_activity_time": item.high_activity_time,
                "medium_activity_time": item.medium_activity_time,
                "low_activity_time": item.low_activity_time,
                "sedentary_time": item.sedentary_time,
                "resting_time": item.resting_time,
                "non_wear_time": item.non_wear_time,
                "inactivity_alerts": item.inactivity_alerts,
                "contributors_meet_daily_targets": item.contributors.meet_daily_targets,
                "contributors_move_every_hour": item.contributors.move_every_hour,
                "contributors_recovery_time": item.contributors.recovery_time,
                "contributors_stay_active": item.contributors.stay_active,
                "contributors_training_frequency": item.contributors.training_frequency,
                "contributors_training_volume": item.contributors.training_volume,
                "source_timestamp": item.timestamp,
                "document_id": UUID(item.id),
            }

            stmt = insert(DailyActivitySummary).values(**values)
            stmt = stmt.on_conflict_do_update(
                index_elements=["user_id", "day"],
                set_={
                    k: getattr(stmt.excluded, k)
                    for k in values.keys()
                    if k not in ["user_id", "day", "created_at"]
                },
            )

            await self.session.execute(stmt)
            saved_count += 1

        logger.info("activity_data_upserted", count=saved_count)
        return saved_count

    async def upsert_readiness_data(
        self, readiness_data: list[DailyReadiness]
    ) -> int:
        """
        レディネスデータをupsert

        Args:
            readiness_data: レディネスデータのリスト

        Returns:
            int: 保存したレコード数
        """
        if not readiness_data:
            return 0

        saved_count = 0
        for item in readiness_data:
            values = {
                "user_id": self.user_id,
                "day": item.day,
                "score": item.score,
                "temperature_deviation": item.temperature_deviation,
                "temperature_trend_deviation": item.temperature_trend_deviation,
                "contributors_activity_balance": item.contributors.activity_balance,
                "contributors_body_temperature": item.contributors.body_temperature,
                "contributors_previous_day_activity": item.contributors.previous_day_activity,
                "contributors_previous_night": item.contributors.previous_night,
                "contributors_recovery_index": item.contributors.recovery_index,
                "contributors_resting_heart_rate": item.contributors.resting_heart_rate,
                "contributors_sleep_balance": item.contributors.sleep_balance,
                "contributors_hrv_balance": item.contributors.hrv_balance,
                "source_timestamp": item.timestamp,
                "document_id": UUID(item.id),
            }

            stmt = insert(DailyReadinessSummary).values(**values)
            stmt = stmt.on_conflict_do_update(
                index_elements=["user_id", "day"],
                set_={
                    k: getattr(stmt.excluded, k)
                    for k in values.keys()
                    if k not in ["user_id", "day", "created_at"]
                },
            )

            await self.session.execute(stmt)
            saved_count += 1

        logger.info("readiness_data_upserted", count=saved_count)
        return saved_count

    async def upsert_stress_data(self, stress_data: list[DailyStress]) -> int:
        """
        ストレスデータをupsert

        Args:
            stress_data: ストレスデータのリスト

        Returns:
            int: 保存したレコード数
        """
        if not stress_data:
            return 0

        saved_count = 0
        for item in stress_data:
            values = {
                "user_id": self.user_id,
                "day": item.day,
                "day_summary": item.day_summary,
                "stress_high": item.stress_high,
                "recovery_high": item.recovery_high,
                "document_id": UUID(item.id),
            }

            stmt = insert(DailyStressSummary).values(**values)
            stmt = stmt.on_conflict_do_update(
                index_elements=["user_id", "day"],
                set_={
                    k: getattr(stmt.excluded, k)
                    for k in values.keys()
                    if k not in ["user_id", "day", "created_at"]
                },
            )

            await self.session.execute(stmt)
            saved_count += 1

        logger.info("stress_data_upserted", count=saved_count)
        return saved_count

    async def upsert_resilience_data(
        self, resilience_data: list[DailyResilience]
    ) -> int:
        """
        レジリエンスデータをupsert

        Args:
            resilience_data: レジリエンスデータのリスト

        Returns:
            int: 保存したレコード数
        """
        if not resilience_data:
            return 0

        saved_count = 0
        for item in resilience_data:
            values = {
                "user_id": self.user_id,
                "day": item.day,
                "level": item.level,
                "contributors_sleep_recovery": item.contributors.sleep_recovery,
                "contributors_daytime_recovery": item.contributors.daytime_recovery,
                "contributors_stress": item.contributors.stress,
                "document_id": UUID(item.id),
            }

            stmt = insert(DailyResilienceSummary).values(**values)
            stmt = stmt.on_conflict_do_update(
                index_elements=["user_id", "day"],
                set_={
                    k: getattr(stmt.excluded, k)
                    for k in values.keys()
                    if k not in ["user_id", "day", "created_at"]
                },
            )

            await self.session.execute(stmt)
            saved_count += 1

        logger.info("resilience_data_upserted", count=saved_count)
        return saved_count
