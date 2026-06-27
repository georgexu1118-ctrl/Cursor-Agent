"""Environment variable and dotenv file loading utilities."""

from __future__ import annotations

import os
from pathlib import Path

from research_agent.infrastructure.config.settings import Settings


def resolve_env_file(explicit_path: str | Path | None = None) -> Path | None:
    """Resolve the dotenv file path from an explicit value or ``DOTENV_PATH``.

    Args:
        explicit_path: Optional override path to a dotenv file.

    Returns:
        Resolved path when the file exists, otherwise ``None``.
    """
    if explicit_path is not None:
        candidate = Path(explicit_path)
        return candidate if candidate.is_file() else None

    configured_path = os.environ.get("DOTENV_PATH", ".env")
    candidate = Path(configured_path)
    return candidate if candidate.is_file() else None


def load_settings(*, env_file: str | Path | None = None) -> Settings:
    """Load and validate settings from the environment and optional dotenv file.

    Args:
        env_file: Optional dotenv file path override.

    Returns:
        Validated application settings.

    Raises:
        pydantic.ValidationError: If settings are missing or invalid.
    """
    resolved = resolve_env_file(env_file)
    if resolved is None:
        return Settings.model_validate({})
    return Settings(_env_file=resolved)  # type: ignore[call-arg]
