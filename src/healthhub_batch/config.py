# src/healthhub_batch/config.py
# healthHubアプリケーションの設定管理モジュール
# pydantic-settingsを使用して環境変数から設定を読み込み、バリデーションを提供
# RELEVANT FILES: cli.py, .env, ../tests/test_config.py

"""Configuration management using pydantic-settings."""
from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Oura API settings
    oura_pat: str = Field(..., description="Oura Personal Access Token")

    # Database settings
    supabase_db_url: str = Field(..., description="Supabase PostgreSQL connection URL")
    supabase_service_role_key: str = Field(
        default="",
        description="Supabase Service Role Key (optional for REST API calls)",
    )

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")

    # Notification settings
    line_channel_access_token: str = Field(
        default="",
        description="LINE Messaging API Channel Access Token (optional)",
    )
    line_user_id: str = Field(
        default="",
        description="LINE User ID for notifications (optional)",
    )

    # Application settings
    user_id: str = Field(
        default="00000000-0000-0000-0000-000000000000",
        description="User ID for single-user batch processing",
    )
    timezone: str = Field(default="UTC", description="Timezone for data processing")

    def validate_required_secrets(self) -> None:
        """Validate that required secrets are provided."""
        if not self.oura_pat:
            msg = "OURA_PAT environment variable is required"
            raise ValueError(msg)
        if not self.supabase_db_url:
            msg = "SUPABASE_DB_URL environment variable is required"
            raise ValueError(msg)