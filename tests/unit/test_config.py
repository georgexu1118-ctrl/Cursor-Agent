"""Unit tests for application configuration."""

import pytest
from pydantic import ValidationError

from research_agent.config import Settings, load_settings


def test_settings_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Default settings use development environment and INFO logging."""
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    settings = Settings(_env_file=None)

    assert settings.environment == "development"
    assert settings.log_level == "INFO"


def test_settings_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Settings load values from environment variables."""
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("LOG_LEVEL", "warning")

    settings = Settings()

    assert settings.environment == "production"
    assert settings.log_level == "WARNING"


def test_invalid_log_level_raises_validation_error() -> None:
    """Invalid log levels are rejected at validation time."""
    with pytest.raises(ValidationError):
        Settings(log_level="VERBOSE")


def test_load_settings_returns_validated_settings(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """load_settings returns a validated Settings instance."""
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    settings = load_settings()
    assert isinstance(settings, Settings)
