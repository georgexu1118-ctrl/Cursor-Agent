"""Unit tests for the provider factory."""

import pytest

from research_agent.infrastructure.config.settings import LLMProviderName, Settings
from research_agent.infrastructure.providers.factory import create_llm_provider
from research_agent.infrastructure.providers.llm.mock import MockLLMProvider
from research_agent.infrastructure.providers.llm.openai import OpenAILLMProvider


def _settings(**overrides: object) -> Settings:
    """Build a Settings instance with test-safe defaults."""
    return Settings(
        _env_file=None,
        **overrides,  # type: ignore[arg-type]
    )


class TestCreateLLMProvider:
    def test_mock_provider_is_default(self) -> None:
        settings = _settings()
        assert settings.llm_provider == LLMProviderName.MOCK
        provider = create_llm_provider(settings)
        assert isinstance(provider, MockLLMProvider)

    def test_explicit_mock_returns_mock_provider(self) -> None:
        settings = _settings(LLM_PROVIDER="mock")
        provider = create_llm_provider(settings)
        assert isinstance(provider, MockLLMProvider)

    def test_openai_returns_openai_provider(self) -> None:
        settings = _settings(LLM_PROVIDER="openai", OPENAI_API_KEY="sk-test")
        provider = create_llm_provider(settings)
        assert isinstance(provider, OpenAILLMProvider)

    def test_openai_provider_uses_model_from_settings(self) -> None:
        settings = _settings(
            LLM_PROVIDER="openai",
            OPENAI_API_KEY="sk-test",
            OPENAI_MODEL="gpt-4o",
        )
        provider = create_llm_provider(settings)
        assert isinstance(provider, OpenAILLMProvider)
        assert provider._model == "gpt-4o"

    def test_openai_without_api_key_raises(self) -> None:
        settings = _settings(LLM_PROVIDER="openai", OPENAI_API_KEY="")
        with pytest.raises(ValueError, match="API key"):
            create_llm_provider(settings)

    def test_unknown_provider_raises(self) -> None:
        settings = _settings()
        settings = settings.model_copy(
            update={"llm_provider": "anthropic"}  # type: ignore[arg-type]
        )
        with pytest.raises(ValueError, match="Unknown LLM_PROVIDER"):
            create_llm_provider(settings)
