"""Unit tests for application configuration."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from research_agent.infrastructure.config.loader import load_settings, resolve_env_file
from research_agent.infrastructure.config.settings import LogFormat, Settings


def test_settings_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Default settings use development environment and INFO logging."""
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("LOG_FORMAT", raising=False)

    settings = Settings(_env_file=None)

    assert settings.environment == "development"
    assert settings.log_level == "INFO"
    assert settings.log_format is LogFormat.CONSOLE
    assert settings.retry_max_attempts == 3


def test_settings_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Settings load values from environment variables."""
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("LOG_LEVEL", "warning")
    monkeypatch.setenv("LOG_FORMAT", "json")
    monkeypatch.setenv("RETRY_MAX_ATTEMPTS", "5")

    settings = Settings(_env_file=None)

    assert settings.environment == "production"
    assert settings.log_level == "WARNING"
    assert settings.log_format is LogFormat.JSON
    assert settings.retry_max_attempts == 5


def test_invalid_log_level_raises_validation_error() -> None:
    """Invalid log levels are rejected at validation time."""
    with pytest.raises(ValidationError):
        Settings(log_level="VERBOSE", _env_file=None)


def test_invalid_retry_delay_bounds_raise_validation_error() -> None:
    """Max retry delay cannot be less than the base delay."""
    with pytest.raises(ValidationError):
        Settings(
            retry_base_delay_seconds=10.0,
            retry_max_delay_seconds=5.0,
            _env_file=None,
        )


def test_load_settings_returns_validated_settings(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """load_settings returns a validated Settings instance."""
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    settings = load_settings()
    assert isinstance(settings, Settings)


def test_resolve_env_file_returns_none_for_missing_file(tmp_path: Path) -> None:
    """resolve_env_file returns None when the configured file does not exist."""
    missing = tmp_path / "missing.env"
    assert resolve_env_file(missing) is None


def test_resolve_env_file_uses_explicit_path(tmp_path: Path) -> None:
    """resolve_env_file returns an existing explicit dotenv path."""
    env_file = tmp_path / ".env"
    env_file.write_text("ENVIRONMENT=test\n", encoding="utf-8")

    resolved = resolve_env_file(env_file)

    assert resolved == env_file


def test_load_settings_reads_explicit_env_file(tmp_path: Path) -> None:
    """load_settings loads values from an explicit dotenv file."""
    env_file = tmp_path / ".env"
    env_file.write_text("ENVIRONMENT=staging\nLOG_LEVEL=ERROR\n", encoding="utf-8")

    settings = load_settings(env_file=env_file)

    assert settings.environment == "staging"
    assert settings.log_level == "ERROR"
