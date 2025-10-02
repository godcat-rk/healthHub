# src/healthhub_batch/db_models.py
# SQLAlchemy ORMモデル定義（Supabase PostgreSQL用）
# Oura APIデータをデータベースに永続化するためのテーブル定義
# RELEVANT FILES: models.py, database.py, design.md

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Date, DateTime, Integer, Numeric, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """SQLAlchemyのベースクラス"""

    pass


# ===============================
# Daily Sleep Summaries
# ===============================


class DailySleepSummary(Base):
    """日次睡眠サマリーテーブル"""

    __tablename__ = "daily_sleep_summaries"
    __table_args__ = {"schema": "healthhub"}

    # Primary Key
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    day: Mapped[date] = mapped_column(Date, primary_key=True)

    # Score and metrics
    score: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)

    # Contributors (展開)
    contributors_deep_sleep: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_efficiency: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_latency: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_rem_sleep: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_restfulness: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_timing: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_total_sleep: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )

    # Metadata
    source_timestamp: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), nullable=False, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


# ===============================
# Daily Activity Summaries
# ===============================


class DailyActivitySummary(Base):
    """日次活動サマリーテーブル"""

    __tablename__ = "daily_activity_summaries"
    __table_args__ = {"schema": "healthhub"}

    # Primary Key
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    day: Mapped[date] = mapped_column(Date, primary_key=True)

    # Score and main metrics
    score: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    steps: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    active_calories: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_calories: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    target_calories: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    equivalent_walking_distance: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )

    # Activity time breakdown (seconds)
    high_activity_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    medium_activity_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    low_activity_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sedentary_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    resting_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    non_wear_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Other metrics
    inactivity_alerts: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)

    # Contributors (展開)
    contributors_meet_daily_targets: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_move_every_hour: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_recovery_time: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_stay_active: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_training_frequency: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_training_volume: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )

    # Metadata
    source_timestamp: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), nullable=False, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


# ===============================
# Daily Readiness Summaries
# ===============================


class DailyReadinessSummary(Base):
    """日次レディネスサマリーテーブル"""

    __tablename__ = "daily_readiness_summaries"
    __table_args__ = {"schema": "healthhub"}

    # Primary Key
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    day: Mapped[date] = mapped_column(Date, primary_key=True)

    # Score and temperature
    score: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    temperature_deviation: Mapped[Optional[float]] = mapped_column(
        Numeric(5, 2), nullable=True
    )
    temperature_trend_deviation: Mapped[Optional[float]] = mapped_column(
        Numeric(5, 2), nullable=True
    )

    # Contributors (展開)
    contributors_activity_balance: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_body_temperature: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_previous_day_activity: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_previous_night: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_recovery_index: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_resting_heart_rate: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_sleep_balance: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )
    contributors_hrv_balance: Mapped[Optional[int]] = mapped_column(
        SmallInteger, nullable=True
    )

    # Metadata
    source_timestamp: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), nullable=False, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


# ===============================
# Daily Stress Summaries
# ===============================


class DailyStressSummary(Base):
    """日次ストレスサマリーテーブル"""

    __tablename__ = "daily_stress_summaries"
    __table_args__ = {"schema": "healthhub"}

    # Primary Key
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    day: Mapped[date] = mapped_column(Date, primary_key=True)

    # Summary
    day_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Stress levels (seconds)
    stress_high: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    stress_medium: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    stress_low: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Recovery levels (seconds)
    recovery_high: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    recovery_medium: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    recovery_low: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Metadata
    source_timestamp: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), nullable=False, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


# ===============================
# Daily Resilience Summaries
# ===============================


class DailyResilienceSummary(Base):
    """日次レジリエンスサマリーテーブル"""

    __tablename__ = "daily_resilience_summaries"
    __table_args__ = {"schema": "healthhub"}

    # Primary Key
    user_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    day: Mapped[date] = mapped_column(Date, primary_key=True)

    # Level
    level: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Contributors (展開)
    contributors_sleep_recovery: Mapped[Optional[float]] = mapped_column(
        Numeric(5, 2), nullable=True
    )
    contributors_daytime_recovery: Mapped[Optional[float]] = mapped_column(
        Numeric(5, 2), nullable=True
    )
    contributors_stress: Mapped[Optional[float]] = mapped_column(
        Numeric(5, 2), nullable=True
    )

    # Metadata
    source_timestamp: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), nullable=False, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
