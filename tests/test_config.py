"""Tests for configuration module."""
import pytest

from healthhub_batch.config import Settings


def test_settings_validation():
    """Test settings validation with missing required fields."""
    with pytest.raises(ValueError, match="OURA_PAT"):
        settings = Settings(oura_pat="", supabase_db_url="")
        settings.validate_required_secrets()


def test_settings_with_valid_values():
    """Test settings with valid values."""
    settings = Settings(
        oura_pat="test-token",
        supabase_db_url="postgresql://test:test@localhost/test"
    )
    settings.validate_required_secrets()  # Should not raise