"""Unit tests for MockSearchProvider."""

from research_agent.domain.entities import SearchResult
from research_agent.domain.providers import SearchProvider
from research_agent.infrastructure.providers.search.mock import MockSearchProvider

_RESULT_A = SearchResult(url="https://a.com", title="A", snippet="a snippet", score=0.9)
_RESULT_B = SearchResult(url="https://b.com", title="B", snippet="b snippet", score=0.7)
_RESULT_C = SearchResult(url="https://c.com", title="C", snippet="c snippet", score=0.5)


class TestMockSearchProvider:
    def test_default_returns_empty_list(self) -> None:
        provider = MockSearchProvider()
        assert provider._results == []

    def test_custom_results_stored(self) -> None:
        provider = MockSearchProvider(results=[_RESULT_A])
        assert provider._results == [_RESULT_A]

    async def test_search_returns_all_results_by_default(self) -> None:
        provider = MockSearchProvider(results=[_RESULT_A, _RESULT_B])
        results = await provider.search("anything")
        assert results == [_RESULT_A, _RESULT_B]

    async def test_search_trims_to_max_results(self) -> None:
        provider = MockSearchProvider(results=[_RESULT_A, _RESULT_B, _RESULT_C])
        results = await provider.search("anything", max_results=2)
        assert results == [_RESULT_A, _RESULT_B]

    async def test_search_ignores_query(self) -> None:
        provider = MockSearchProvider(results=[_RESULT_A])
        assert await provider.search("foo") == await provider.search("bar")

    async def test_empty_provider_returns_empty(self) -> None:
        provider = MockSearchProvider()
        results = await provider.search("anything")
        assert results == []

    def test_satisfies_search_provider_protocol(self) -> None:
        assert isinstance(MockSearchProvider(), SearchProvider)
