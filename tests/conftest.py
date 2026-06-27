"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from research_agent.config import Settings


@pytest.fixture
def settings() -> Settings:
    """Return default application settings for unit tests."""
    return Settings(environment="test", log_level="DEBUG")
