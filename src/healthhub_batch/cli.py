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
from healthhub_batch.fetcher import fetch_all_data, print_summary

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
        typer.echo(f"❌ Configuration error: {e}", err=True)
        raise typer.Exit(code=1) from e

    typer.echo(f"🔄 Fetching Oura data from {start_date} to {end_date}")
    if dry_run:
        typer.echo("ℹ️  Dry run mode: データベースには保存しません")

    # 非同期処理を実行
    results = asyncio.run(fetch_all_data(start_date, end_date, settings))

    # 結果を表示
    print_summary(results)

    typer.echo("✅ Data fetching completed")


@app.command()
def migrate() -> None:
    """Run database migrations."""
    typer.echo("Running database migrations...")
    # TODO: Implement migration logic
    typer.echo("✅ Database migrations completed (placeholder)")


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