"""Unit tests for MockLLMProvider."""

from research_agent.domain.entities import Message, MessageRole
from research_agent.domain.providers import LLMProvider
from research_agent.infrastructure.providers.llm.mock import MockLLMProvider


class TestMockLLMProvider:
    def test_default_response(self) -> None:
        provider = MockLLMProvider()
        assert provider._response == "mock response"

    def test_custom_response(self) -> None:
        provider = MockLLMProvider(response="hello world")
        assert provider._response == "hello world"

    async def test_complete_returns_fixed_response(self) -> None:
        provider = MockLLMProvider(response="fixed")
        messages = [Message(role=MessageRole.USER, content="ping")]
        result = await provider.complete(messages)
        assert result == "fixed"

    async def test_complete_ignores_messages(self) -> None:
        provider = MockLLMProvider(response="always this")
        result = await provider.complete([])
        assert result == "always this"

    async def test_complete_ignores_max_tokens(self) -> None:
        provider = MockLLMProvider(response="x")
        messages = [Message(role=MessageRole.USER, content="hi")]
        result = await provider.complete(messages, max_tokens=5)
        assert result == "x"

    def test_satisfies_llm_provider_protocol(self) -> None:
        assert isinstance(MockLLMProvider(), LLMProvider)
