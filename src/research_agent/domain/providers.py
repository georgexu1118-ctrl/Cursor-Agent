"""Provider abstractions for the domain layer.

Concrete provider implementations live in the infrastructure layer and must
satisfy these structural protocols — no inheritance required.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from research_agent.domain.entities import Message, SearchResult


@runtime_checkable
class LLMProvider(Protocol):
    """Async interface for large-language-model completions."""

    async def complete(
        self,
        messages: list[Message],
        *,
        max_tokens: int = 1024,
    ) -> str:
        """Return an assistant reply for the given conversation.

        Args:
            messages: Ordered conversation history sent to the model.
            max_tokens: Upper bound on tokens in the generated reply.

        Returns:
            Text of the model's response.
        """
        ...


@runtime_checkable
class SearchProvider(Protocol):
    """Async interface for web or corpus search."""

    async def search(
        self,
        query: str,
        *,
        max_results: int = 10,
    ) -> list[SearchResult]:
        """Return ranked search results for the given query.

        Args:
            query: Natural-language or keyword search query.
            max_results: Maximum number of results to return.

        Returns:
            List of search results ordered by relevance.
        """
        ...
