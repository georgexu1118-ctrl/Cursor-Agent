"""In-memory mock LLM provider for tests and local development."""

from __future__ import annotations

from research_agent.domain.entities import Message


class MockLLMProvider:
    """Returns a fixed response without calling any external API.

    Satisfies the ``LLMProvider`` protocol structurally.

    Args:
        response: Text returned from every ``complete`` call.
    """

    def __init__(self, response: str = "mock response") -> None:
        self._response = response

    async def complete(
        self,
        messages: list[Message],
        *,
        max_tokens: int = 1024,
    ) -> str:
        """Return the fixed response regardless of input."""
        return self._response
