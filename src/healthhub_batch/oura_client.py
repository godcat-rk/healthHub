# src/healthhub_batch/oura_client.py
# Oura Ring API v2クライアント
# Personal Access Tokenを使用してOura APIからヘルスデータを取得
# RELEVANT FILES: config.py, cli.py

"""Oura Ring API v2 client for fetching health data."""
from __future__ import annotations

import asyncio
from typing import Any

import httpx
import structlog

logger = structlog.get_logger(__name__)

# リトライ設定
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 2.0  # 指数バックオフの係数
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}  # リトライ対象のステータスコード


class OuraClient:
    """Client for interacting with Oura Ring API v2."""

    BASE_URL = "https://api.ouraring.com/v2/usercollection"

    def __init__(self, personal_access_token: str, timeout: float = 30.0) -> None:
        """Initialize Oura API client.

        Args:
            personal_access_token: Oura Personal Access Token
            timeout: Request timeout in seconds (default: 30.0)
        """
        self.token = personal_access_token
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> OuraClient:
        """Async context manager entry."""
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
            },
            timeout=self.timeout,
        )
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    async def _get(self, endpoint: str, params: dict[str, str]) -> dict[str, Any]:
        """Make GET request to Oura API with retry logic.

        Args:
            endpoint: API endpoint path (e.g., "daily_sleep")
            params: Query parameters (e.g., start_date, end_date)

        Returns:
            JSON response as dictionary

        Raises:
            httpx.HTTPStatusError: If the request fails after all retries
            httpx.RequestError: If network error occurs after all retries
        """
        if not self._client:
            msg = "Client not initialized. Use async context manager."
            raise RuntimeError(msg)

        logger.info("oura_api_request", endpoint=endpoint, params=params)

        last_exception: Exception | None = None

        for attempt in range(MAX_RETRIES):
            try:
                response = await self._client.get(endpoint, params=params)

                # レート制限やサーバーエラーの場合はリトライ
                if response.status_code in RETRY_STATUS_CODES:
                    wait_time = RETRY_BACKOFF_FACTOR**attempt
                    logger.warning(
                        "oura_api_retry",
                        endpoint=endpoint,
                        status_code=response.status_code,
                        attempt=attempt + 1,
                        max_retries=MAX_RETRIES,
                        wait_seconds=wait_time,
                    )

                    if attempt < MAX_RETRIES - 1:
                        await asyncio.sleep(wait_time)
                        continue

                # ステータスコードチェック
                response.raise_for_status()

                # 成功
                data = response.json()
                logger.info(
                    "oura_api_response",
                    endpoint=endpoint,
                    status_code=response.status_code,
                    record_count=len(data.get("data", [])),
                    attempts=attempt + 1,
                )

                return data

            except httpx.RequestError as e:
                # ネットワークエラー
                last_exception = e
                wait_time = RETRY_BACKOFF_FACTOR**attempt

                logger.warning(
                    "oura_api_network_error",
                    endpoint=endpoint,
                    error=str(e),
                    attempt=attempt + 1,
                    max_retries=MAX_RETRIES,
                    wait_seconds=wait_time,
                )

                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(wait_time)
                    continue

            except httpx.HTTPStatusError as e:
                # HTTPエラー（4xx, 5xx）
                last_exception = e

                if e.response.status_code not in RETRY_STATUS_CODES:
                    # リトライ対象外のエラーは即座に失敗
                    logger.error(
                        "oura_api_http_error",
                        endpoint=endpoint,
                        status_code=e.response.status_code,
                        error=str(e),
                    )
                    raise

                wait_time = RETRY_BACKOFF_FACTOR**attempt
                logger.warning(
                    "oura_api_http_retry",
                    endpoint=endpoint,
                    status_code=e.response.status_code,
                    attempt=attempt + 1,
                    max_retries=MAX_RETRIES,
                    wait_seconds=wait_time,
                )

                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(wait_time)
                    continue

        # 全リトライ失敗
        logger.error(
            "oura_api_max_retries_exceeded",
            endpoint=endpoint,
            max_retries=MAX_RETRIES,
            last_error=str(last_exception),
        )

        if last_exception:
            raise last_exception

        msg = f"Failed to fetch {endpoint} after {MAX_RETRIES} retries"
        raise RuntimeError(msg)

    async def get_daily_sleep(
        self, start_date: str, end_date: str
    ) -> dict[str, Any]:
        """Fetch daily sleep summaries.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            API response with sleep data
        """
        return await self._get(
            "daily_sleep",
            {"start_date": start_date, "end_date": end_date},
        )

    async def get_daily_activity(
        self, start_date: str, end_date: str
    ) -> dict[str, Any]:
        """Fetch daily activity summaries.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            API response with activity data
        """
        return await self._get(
            "daily_activity",
            {"start_date": start_date, "end_date": end_date},
        )

    async def get_daily_stress(
        self, start_date: str, end_date: str
    ) -> dict[str, Any]:
        """Fetch daily stress summaries.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            API response with stress data
        """
        return await self._get(
            "daily_stress",
            {"start_date": start_date, "end_date": end_date},
        )

    async def get_daily_resilience(
        self, start_date: str, end_date: str
    ) -> dict[str, Any]:
        """Fetch daily resilience summaries.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            API response with resilience data
        """
        return await self._get(
            "daily_resilience",
            {"start_date": start_date, "end_date": end_date},
        )

    async def get_daily_readiness(
        self, start_date: str, end_date: str
    ) -> dict[str, Any]:
        """Fetch daily readiness summaries.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            API response with readiness data
        """
        return await self._get(
            "daily_readiness",
            {"start_date": start_date, "end_date": end_date},
        )