"""Unit tests for application bootstrap."""

import pytest

from research_agent.application.bootstrap import bootstrap, create_container
from research_agent.infrastructure.config.settings import Settings
from research_agent.infrastructure.di.container import Container
from research_agent.infrastructure.retry.policy import RetryPolicy


def test_create_container_registers_core_services() -> None:
    """create_container registers settings, container, and retry policy."""
    settings = Settings(_env_file=None)
    container = create_container(settings)

    assert container.resolve(Settings) is settings
    assert container.resolve(Container) is container

    retry_policy = container.resolve(RetryPolicy)
    assert retry_policy.max_attempts == settings.retry_max_attempts


def test_bootstrap_returns_application_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """bootstrap wires settings, logging, and dependency injection."""
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    context = bootstrap()

    assert context.settings.environment == "development"
    assert context.container.resolve(Settings) is context.settings
    assert context.logger is not None
