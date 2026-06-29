"""In-memory mock search provider for tests and local development."""

from __future__ import annotations

from research_agent.domain.entities import SearchResult


class MockSearchProvider:
    """Returns fixed search results without calling any external API.

    Satisfies the ``SearchProvider`` protocol structurally.

    Args:
        results: Results returned from every ``search`` call.
    """

    def __init__(self, results: list[SearchResult] | None = None) -> None:
        self._results: list[SearchResult] = results if results is not None else []

    async def search(
        self,
        query: str,
        *,
        max_results: int = 10,
    ) -> list[SearchResult]:
        """Return the fixed result list, trimmed to ``max_results``."""
        return self._results[:max_results]
