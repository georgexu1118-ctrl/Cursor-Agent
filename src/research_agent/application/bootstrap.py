"""Application bootstrap and startup orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from structlog.stdlib import BoundLogger

from research_agent.application.research_agent import ResearchAgent
from research_agent.domain.providers import LLMProvider, SearchProvider
from research_agent.infrastructure.config.loader import load_settings
from research_agent.infrastructure.config.settings import Settings
from research_agent.infrastructure.di.container import Container
from research_agent.infrastructure.logging.setup import configure_logging, get_logger
from research_agent.infrastructure.providers.factory import (
    create_llm_provider,
    create_search_provider,
)
from research_agent.infrastructure.retry.policy import RetryPolicy


@dataclass(frozen=True)
class ApplicationContext:
    """Bootstrapped application dependencies."""

    settings: Settings
    container: Container
    logger: BoundLogger


def create_container(settings: Settings) -> Container:
    """Create a dependency injection container with all core services registered."""
    container = Container()
    container.register_instance(Settings, settings)
    container.register_instance(Container, container)
    container.register(
        RetryPolicy,
        lambda: RetryPolicy.from_settings(settings),
        singleton=True,
    )
    container.register(
        LLMProvider,  # type: ignore[type-abstract]
        lambda: create_llm_provider(settings),
        singleton=True,
    )
    container.register(
        SearchProvider,  # type: ignore[type-abstract]
        lambda: create_search_provider(settings),
        singleton=True,
    )
    container.register(
        ResearchAgent,
        lambda: ResearchAgent(
            llm=container.resolve(LLMProvider),  # type: ignore[type-abstract]
            search=container.resolve(SearchProvider),  # type: ignore[type-abstract]
        ),
        singleton=True,
    )
    return container


def bootstrap(*, env_file: str | Path | None = None) -> ApplicationContext:
    """Initialize configuration, logging, and core dependency injection.

    Args:
        env_file: Optional dotenv file path override.

    Returns:
        Application context with settings, container, and logger.
    """
    settings = load_settings(env_file=env_file)
    configure_logging(settings.log_level, log_format=settings.log_format)
    container = create_container(settings)
    logger = get_logger("research_agent")
    logger.info(
        "application_bootstrapped",
        environment=settings.environment,
        log_format=settings.log_format.value,
    )
    return ApplicationContext(
        settings=settings,
        container=container,
        logger=logger,
    )
