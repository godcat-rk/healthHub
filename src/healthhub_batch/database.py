# src/healthhub_batch/database.py
# データベース接続とセッション管理
# SQLAlchemy非同期エンジンとセッションファクトリを提供
# RELEVANT FILES: db_models.py, config.py, repository.py

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from healthhub_batch.config import Settings

logger = structlog.get_logger()


class Database:
    """データベース接続管理クラス"""

    def __init__(self, settings: Settings):
        """
        データベースエンジンとセッションファクトリを初期化

        Args:
            settings: アプリケーション設定
        """
        self.settings = settings

        # PostgreSQL接続文字列をasyncpg用に変換
        # postgresql:// → postgresql+asyncpg://
        db_url = settings.supabase_db_url
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

        # 非同期エンジンの作成
        self.engine = create_async_engine(
            db_url,
            echo=False,  # SQLログを出力しない（本番環境）
            pool_pre_ping=True,  # 接続チェック
            pool_size=5,  # コネクションプール数
            max_overflow=10,  # 最大オーバーフロー接続数
            connect_args={
                "timeout": 30,  # 接続タイムアウト（秒）
                "command_timeout": 30,  # コマンドタイムアウト（秒）
                "ssl": "prefer",  # SSL接続を優先（Supabase推奨）
            }
        )

        # セッションファクトリの作成
        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,  # コミット後もオブジェクトを使える
        )

        logger.info("database_initialized", db_host=self._get_db_host(db_url))

    def _get_db_host(self, db_url: str) -> str:
        """接続文字列からホスト名を抽出（ログ用）"""
        try:
            # postgresql+asyncpg://user:pass@host:port/db
            parts = db_url.split("@")
            if len(parts) > 1:
                host_port = parts[1].split("/")[0]
                return host_port.split(":")[0]
        except Exception:
            pass
        return "unknown"

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        データベースセッションを提供するコンテキストマネージャ

        Yields:
            AsyncSession: データベースセッション

        Example:
            async with db.session() as session:
                result = await session.execute(query)
        """
        async with self.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error("database_session_error", error=str(e))
                raise
            finally:
                await session.close()

    async def close(self):
        """データベース接続を閉じる"""
        await self.engine.dispose()
        logger.info("database_closed")


# グローバルなデータベースインスタンス（アプリケーション起動時に初期化）
_db_instance: Database | None = None


def init_database(settings: Settings) -> Database:
    """
    データベースインスタンスを初期化

    Args:
        settings: アプリケーション設定

    Returns:
        Database: データベースインスタンス
    """
    global _db_instance
    _db_instance = Database(settings)
    return _db_instance


def get_database() -> Database:
    """
    データベースインスタンスを取得

    Returns:
        Database: データベースインスタンス

    Raises:
        RuntimeError: データベースが初期化されていない場合
    """
    if _db_instance is None:
        raise RuntimeError(
            "Database not initialized. Call init_database() first."
        )
    return _db_instance
