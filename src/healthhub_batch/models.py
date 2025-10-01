# src/healthhub_batch/models.py
# Oura API レスポンスデータのPydanticモデル定義
# API取得データのバリデーションと型安全性を提供
# RELEVANT FILES: oura_client.py, fetcher.py, database.py

from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


# ===============================
# Daily Sleep Models
# ===============================


class SleepContributors(BaseModel):
    """睡眠スコアの貢献要素"""

    deep_sleep: int
    efficiency: int
    latency: int
    rem_sleep: int
    restfulness: int
    timing: int
    total_sleep: int


class DailySleep(BaseModel):
    """日次睡眠サマリー"""

    id: str
    contributors: SleepContributors
    day: date
    score: Optional[int] = None
    timestamp: datetime


# ===============================
# Daily Activity Models
# ===============================


class ActivityContributors(BaseModel):
    """活動スコアの貢献要素"""

    meet_daily_targets: int
    move_every_hour: int
    recovery_time: int
    stay_active: int
    training_frequency: int
    training_volume: int


class DailyActivity(BaseModel):
    """日次活動サマリー（時系列データは除外）"""

    id: str
    class_5_min: Optional[str] = None  # 非常に長いため、保存するか要検討
    score: Optional[int] = None
    active_calories: int
    average_met_minutes: float = Field(alias="average_met_minutes")
    contributors: ActivityContributors
    equivalent_walking_distance: int
    high_activity_met_minutes: int
    high_activity_time: int
    inactivity_alerts: int
    low_activity_met_minutes: int
    low_activity_time: int
    medium_activity_met_minutes: int
    medium_activity_time: int
    # met: dict は除外（itemsに2991個の数値配列があるため）
    meters_to_target: int
    non_wear_time: int
    resting_time: int
    sedentary_met_minutes: int
    sedentary_time: int
    steps: int
    target_calories: int
    target_meters: int
    total_calories: int
    day: date
    timestamp: datetime

    class Config:
        populate_by_name = True


# ===============================
# Daily Readiness Models
# ===============================


class ReadinessContributors(BaseModel):
    """レディネススコアの貢献要素"""

    activity_balance: int
    body_temperature: int
    hrv_balance: int
    previous_day_activity: int
    previous_night: int
    recovery_index: int
    resting_heart_rate: int
    sleep_balance: int
    sleep_regularity: int


class DailyReadiness(BaseModel):
    """日次レディネスサマリー"""

    id: str
    contributors: ReadinessContributors
    day: date
    score: Optional[int] = None
    temperature_deviation: Optional[float] = None
    temperature_trend_deviation: Optional[float] = None
    timestamp: datetime


# ===============================
# Daily Stress Models
# ===============================


class DailyStress(BaseModel):
    """日次ストレスサマリー"""

    id: str
    day: date
    stress_high: Optional[int] = None  # 高ストレス時間（秒）
    recovery_high: Optional[int] = None  # 高回復時間（秒）
    day_summary: Optional[str] = None  # "normal", "stressful" など


# ===============================
# Daily Resilience Models
# ===============================


class ResilienceContributors(BaseModel):
    """レジリエンスの貢献要素"""

    sleep_recovery: float
    daytime_recovery: float
    stress: float


class DailyResilience(BaseModel):
    """日次レジリエンスサマリー"""

    id: str
    day: date
    contributors: ResilienceContributors
    level: Optional[str] = None  # "solid", "strong" など


# ===============================
# API Response Wrappers
# ===============================


class OuraApiResponse(BaseModel):
    """Oura API共通レスポンス形式"""

    data: list[dict[str, Any]]
    next_token: Optional[str] = None
