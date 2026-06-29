"""OpenAI chat completion provider."""

from __future__ import annotations

from openai import AsyncOpenAI

from research_agent.domain.entities import Message, MessageRole


class OpenAILLMProvider:
    """Calls the OpenAI Chat Completions API to generate replies.

    Satisfies the ``LLMProvider`` protocol structurally.

    Args:
        api_key: OpenAI API key.  Raises ``ValueError`` immediately if empty.
        model: Model name, e.g. ``"gpt-4o-mini"``.

    Raises:
        ValueError: If ``api_key`` is empty or whitespace.
    """

    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        if not api_key or not api_key.strip():
            msg = (
                "OpenAI API key is required.  "
                "Set OPENAI_API_KEY in your environment or .env file."
            )
            raise ValueError(msg)
        self._api_key = api_key
        self._model = model
        self._client: AsyncOpenAI | None = None

    def _get_client(self) -> AsyncOpenAI:
        """Return a lazily constructed OpenAI async client."""
        if self._client is None:
            self._client = AsyncOpenAI(api_key=self._api_key)
        return self._client

    async def complete(
        self,
        messages: list[Message],
        *,
        max_tokens: int = 1024,
    ) -> str:
        """Send messages to the OpenAI Chat Completions API and return the reply.

        Args:
            messages: Ordered conversation history.
            max_tokens: Upper bound on generated tokens.

        Returns:
            Text content of the assistant message.
        """
        client = self._get_client()
        openai_messages = [
            {"role": _role_str(msg.role), "content": msg.content} for msg in messages
        ]
        response = await client.chat.completions.create(
            model=self._model,
            messages=openai_messages,  # type: ignore[arg-type]
            max_tokens=max_tokens,
        )
        content: str = response.choices[0].message.content or ""
        return content


def _role_str(role: MessageRole) -> str:
    """Convert a ``MessageRole`` to the string expected by the OpenAI API."""
    return role.value
