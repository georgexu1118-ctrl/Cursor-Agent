"""Provider factory functions."""

from __future__ import annotations

from research_agent.domain.providers import LLMProvider, SearchProvider
from research_agent.infrastructure.config.settings import Settings
from research_agent.infrastructure.providers.llm.mock import MockLLMProvider
from research_agent.infrastructure.providers.llm.openai import OpenAILLMProvider
from research_agent.infrastructure.providers.search.mock import MockSearchProvider


def create_llm_provider(settings: Settings) -> LLMProvider:
    """Return an LLMProvider implementation selected by ``settings.llm_provider``.

    Supported values of ``LLM_PROVIDER``:
        - ``"mock"``   — deterministic in-memory mock (default, safe for tests)
        - ``"openai"`` — OpenAI Chat Completions via the ``openai`` SDK

    Args:
        settings: Validated application settings.

    Returns:
        An object satisfying the ``LLMProvider`` protocol.

    Raises:
        ValueError: For unrecognised ``llm_provider`` values.
    """
    provider = settings.llm_provider.lower()

    if provider == "mock":
        return MockLLMProvider()

    if provider == "openai":
        return OpenAILLMProvider(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
        )

    msg = (
        f"Unknown LLM_PROVIDER '{settings.llm_provider}'. "
        "Supported values: mock, openai."
    )
    raise ValueError(msg)


def create_search_provider(settings: Settings) -> SearchProvider:
    """Return a SearchProvider implementation.

    Currently always returns ``MockSearchProvider``.  Future milestones will
    add real search backends (Brave, Tavily, …) selectable via settings.

    Args:
        settings: Validated application settings.

    Returns:
        An object satisfying the ``SearchProvider`` protocol.
    """
    return MockSearchProvider()
