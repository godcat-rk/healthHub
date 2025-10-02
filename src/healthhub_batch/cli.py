# src/healthhub_batch/cli.py
# healthHubバッチアプリケーションのCLIエントリーポイント
# Oura Ringデータの取得とデータベース管理のためのコマンドラインインターフェースを提供
# RELEVANT FILES: config.py, fetcher.py, oura_client.py

"""Command Line Interface for healthhub batch processing."""
from __future__ import annotations

import asyncio

import structlog
import typer
from typing_extensions import Annotated

from healthhub_batch.config import Settings
from healthhub_batch.database import init_database
from healthhub_batch.fetcher import fetch_all_data, fetch_and_save_data, print_summary

# structlogの設定
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.dev.ConsoleRenderer(),
    ]
)

app = typer.Typer(
    name="healthhub-batch",
    help="Oura Ring data batch processing system",
    no_args_is_help=True,
)


@app.command()
def fetch(
    start_date: Annotated[str, typer.Option("--start-date", "-s", help="Start date (YYYY-MM-DD)")],
    end_date: Annotated[str, typer.Option("--end-date", "-e", help="End date (YYYY-MM-DD)")],
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Run without saving to database")] = False,
) -> None:
    """Fetch Oura Ring data for the specified date range."""
    try:
        settings = Settings()
        settings.validate_required_secrets()
    except ValueError as e:
        typer.echo(f"[ERROR] Configuration error: {e}", err=True)
        raise typer.Exit(code=1) from e

    typer.echo(f"[INFO] Fetching Oura data from {start_date} to {end_date}")

    if dry_run:
        # Dry runモード：APIからデータ取得のみ（DB保存なし）
        typer.echo("[INFO] Dry run mode: データベースには保存しません")
        results = asyncio.run(fetch_all_data(start_date, end_date, settings))
        print_summary(results)
    else:
        # 通常モード：データ取得 + DB保存
        typer.echo("[INFO] Saving data to database...")
        db = init_database(settings)

        save_counts = asyncio.run(
            fetch_and_save_data(start_date, end_date, settings, db)
        )

        # 保存結果を表示
        typer.echo("\n=== Save Summary ===")
        for data_type, count in save_counts.items():
            typer.echo(f"[OK] {data_type}: {count} records saved")
        typer.echo("=" * 30 + "\n")

    typer.echo("[OK] Data fetching completed")


@app.command()
def migrate() -> None:
    """Run database migrations."""
    typer.echo("Running database migrations...")
    # TODO: Implement migration logic
    typer.echo("[OK] Database migrations completed (placeholder)")


@app.command()
def version() -> None:
    """Show version information."""
    from healthhub_batch import __version__
    typer.echo(f"healthhub-batch version: {__version__}")


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()