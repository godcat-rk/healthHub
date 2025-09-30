# src/healthhub_batch/cli.py
# healthHubバッチアプリケーションのCLIエントリーポイント
# Oura Ringデータの取得とデータベース管理のためのコマンドラインインターフェースを提供
# RELEVANT FILES: config.py, __init__.py, ../tests/test_config.py

"""Command Line Interface for healthhub batch processing."""
from __future__ import annotations

import typer
from typing_extensions import Annotated

from healthhub_batch.config import Settings

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
    settings = Settings()

    typer.echo(f"Fetching Oura data from {start_date} to {end_date}")
    typer.echo(f"Dry run: {dry_run}")
    typer.echo(f"Database URL: {settings.supabase_db_url}")

    # TODO: Implement actual data fetching logic
    typer.echo("✅ Data fetching completed (placeholder)")


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