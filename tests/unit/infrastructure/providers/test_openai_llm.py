"""Unit tests for OpenAILLMProvider — no real network calls."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from research_agent.domain.entities import Message, MessageRole
from research_agent.domain.providers import LLMProvider
from research_agent.infrastructure.providers.llm.openai import OpenAILLMProvider


class TestOpenAILLMProviderConstruction:
    def test_valid_key_constructs_successfully(self) -> None:
        provider = OpenAILLMProvider(api_key="sk-test", model="gpt-4o-mini")
        assert provider._model == "gpt-4o-mini"

    def test_default_model(self) -> None:
        provider = OpenAILLMProvider(api_key="sk-test")
        assert provider._model == "gpt-4o-mini"

    def test_empty_api_key_raises(self) -> None:
        with pytest.raises(ValueError, match="API key"):
            OpenAILLMProvider(api_key="")

    def test_whitespace_api_key_raises(self) -> None:
        with pytest.raises(ValueError, match="API key"):
            OpenAILLMProvider(api_key="   ")

    def test_client_not_created_at_init(self) -> None:
        provider = OpenAILLMProvider(api_key="sk-test")
        assert provider._client is None

    def test_satisfies_llm_provider_protocol(self) -> None:
        assert isinstance(OpenAILLMProvider(api_key="sk-test"), LLMProvider)


class TestOpenAILLMProviderComplete:
    async def test_complete_calls_openai_and_returns_content(self) -> None:
        provider = OpenAILLMProvider(api_key="sk-test", model="gpt-4o-mini")

        fake_message = MagicMock()
        fake_message.content = "The answer is 42."
        fake_choice = MagicMock()
        fake_choice.message = fake_message
        fake_response = MagicMock()
        fake_response.choices = [fake_choice]

        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(return_value=fake_response)

        provider._client = mock_client

        messages = [Message(role=MessageRole.USER, content="What is the answer?")]
        result = await provider.complete(messages, max_tokens=50)

        assert result == "The answer is 42."
        mock_client.chat.completions.create.assert_awaited_once()

    async def test_complete_passes_model_and_max_tokens(self) -> None:
        provider = OpenAILLMProvider(api_key="sk-test", model="gpt-4o")

        fake_message = MagicMock()
        fake_message.content = "response"
        fake_choice = MagicMock()
        fake_choice.message = fake_message
        fake_response = MagicMock()
        fake_response.choices = [fake_choice]

        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(return_value=fake_response)
        provider._client = mock_client

        messages = [Message(role=MessageRole.USER, content="hi")]
        await provider.complete(messages, max_tokens=256)

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert call_kwargs["model"] == "gpt-4o"
        assert call_kwargs["max_tokens"] == 256

    async def test_complete_maps_message_roles(self) -> None:
        provider = OpenAILLMProvider(api_key="sk-test")

        fake_message = MagicMock()
        fake_message.content = "ok"
        fake_choice = MagicMock()
        fake_choice.message = fake_message
        fake_response = MagicMock()
        fake_response.choices = [fake_choice]

        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(return_value=fake_response)
        provider._client = mock_client

        messages = [
            Message(role=MessageRole.SYSTEM, content="You are helpful."),
            Message(role=MessageRole.USER, content="Hello."),
        ]
        await provider.complete(messages)

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        sent = call_kwargs["messages"]
        assert sent[0] == {"role": "system", "content": "You are helpful."}
        assert sent[1] == {"role": "user", "content": "Hello."}

    async def test_complete_returns_empty_string_for_none_content(self) -> None:
        provider = OpenAILLMProvider(api_key="sk-test")

        fake_message = MagicMock()
        fake_message.content = None
        fake_choice = MagicMock()
        fake_choice.message = fake_message
        fake_response = MagicMock()
        fake_response.choices = [fake_choice]

        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(return_value=fake_response)
        provider._client = mock_client

        result = await provider.complete([Message(role=MessageRole.USER, content="hi")])
        assert result == ""
