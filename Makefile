.PHONY: help install lint format typecheck test clean run migrate

# Default target
help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies using Poetry"
	@echo "  lint       - Run linting checks (ruff)"
	@echo "  format     - Format code (black + ruff)"
	@echo "  typecheck  - Run type checking (mypy)"
	@echo "  test       - Run tests (pytest)"
	@echo "  clean      - Clean build artifacts"
	@echo "  run        - Run the CLI (example usage)"
	@echo "  migrate    - Run database migrations"

# Development setup
install:
	poetry install --with dev

# Code quality
lint:
	poetry run ruff check src/ tests/
	poetry run ruff format --check src/ tests/

format:
	poetry run black src/ tests/
	poetry run ruff format src/ tests/
	poetry run ruff check --fix src/ tests/

typecheck:
	poetry run mypy src/

test:
	poetry run pytest

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf dist/
	rm -rf build/

# Application commands
run:
	@echo "Example usage:"
	@echo "  poetry run healthhub-batch --help"
	@echo "  poetry run healthhub-batch fetch --start-date 2024-01-01 --end-date 2024-01-02"

migrate:
	poetry run healthhub-batch migrate

# CI-friendly targets
ci-lint: lint typecheck
ci-test: test