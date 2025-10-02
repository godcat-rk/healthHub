# scripts/test_db_connection.py
# データベース接続テストスクリプト
# Supabase PostgreSQLへの接続を確認

import asyncio
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from healthhub_batch.config import Settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


async def test_connection():
    """データベース接続をテスト"""
    print("=== Database Connection Test ===\n")

    # 設定を読み込み
    try:
        settings = Settings()
        print(f"[OK] Settings loaded")
        print(f"     USER_ID: {settings.user_id}")
        print(f"     DB Host: {settings.supabase_db_url.split('@')[1].split('/')[0]}\n")
    except Exception as e:
        print(f"[ERROR] Failed to load settings: {e}")
        return

    # 接続文字列を変換
    db_url = settings.supabase_db_url
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    print(f"[INFO] Attempting to connect to database...")

    # エンジンを作成
    try:
        engine = create_async_engine(
            db_url,
            echo=False,
            pool_pre_ping=True,
            connect_args={
                "timeout": 10,  # 10秒でタイムアウト
                "command_timeout": 10,
            }
        )
        print(f"[OK] Engine created\n")
    except Exception as e:
        print(f"[ERROR] Failed to create engine: {e}")
        return

    # 接続テスト
    try:
        async with engine.connect() as conn:
            print(f"[OK] Connected to database!")

            # 簡単なクエリを実行
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"[OK] PostgreSQL version: {version[:50]}...\n")

            # スキーマの存在確認
            result = await conn.execute(
                text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'healthhub'")
            )
            schema_exists = result.scalar()

            if schema_exists:
                print(f"[OK] Schema 'healthhub' exists")

                # テーブル一覧を取得
                result = await conn.execute(
                    text("""
                        SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema = 'healthhub'
                        ORDER BY table_name
                    """)
                )
                tables = result.fetchall()

                if tables:
                    print(f"[OK] Found {len(tables)} tables:")
                    for table in tables:
                        print(f"     - {table[0]}")
                else:
                    print(f"[WARNING] No tables found in 'healthhub' schema")
            else:
                print(f"[WARNING] Schema 'healthhub' does not exist")
                print(f"[INFO] You need to create the schema and tables first")

        print(f"\n[OK] Connection test successful!")

    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        print(f"\nDetails:")
        print(f"  Error type: {type(e).__name__}")
        print(f"  Error message: {str(e)}")

    finally:
        await engine.dispose()
        print(f"\n[INFO] Engine disposed")


if __name__ == "__main__":
    asyncio.run(test_connection())
