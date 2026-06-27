"""Unit tests for domain provider protocols."""

from research_agent.domain.entities import Message, SearchResult
from research_agent.domain.providers import LLMProvider, SearchProvider


class _StubLLM:
    """Minimal conforming LLMProvider implementation."""

    async def complete(
        self,
        messages: list[Message],
        *,
        max_tokens: int = 1024,
    ) -> str:
        return "stub response"


class _StubSearch:
    """Minimal conforming SearchProvider implementation."""

    async def search(
        self,
        query: str,
        *,
        max_results: int = 10,
    ) -> list[SearchResult]:
        return []


class _NonConforming:
    """Class that does not implement any provider interface."""

    pass


class TestLLMProvider:
    def test_conforming_class_is_instance(self) -> None:
        assert isinstance(_StubLLM(), LLMProvider)

    def test_non_conforming_class_is_not_instance(self) -> None:
        assert not isinstance(_NonConforming(), LLMProvider)

    def test_missing_complete_method_fails(self) -> None:
        class _NoComplete:
            pass

        assert not isinstance(_NoComplete(), LLMProvider)


class TestSearchProvider:
    def test_conforming_class_is_instance(self) -> None:
        assert isinstance(_StubSearch(), SearchProvider)

    def test_non_conforming_class_is_not_instance(self) -> None:
        assert not isinstance(_NonConforming(), SearchProvider)

    def test_missing_search_method_fails(self) -> None:
        class _NoSearch:
            pass

        assert not isinstance(_NoSearch(), SearchProvider)


class TestProviderExportsFromDomain:
    """Verify that the domain __init__ re-exports provider types."""

    def test_llm_provider_importable_from_domain(self) -> None:
        from research_agent.domain import LLMProvider as LP

        assert LP is LLMProvider

    def test_search_provider_importable_from_domain(self) -> None:
        from research_agent.domain import SearchProvider as SP

        assert SP is SearchProvider

    def test_entities_importable_from_domain(self) -> None:
        from research_agent.domain import Message as M
        from research_agent.domain import MessageRole as MR
        from research_agent.domain import SearchResult as SR

        msg = M(role=MR.USER, content="hi")
        result = SR(url="https://x.com", title="X", snippet="s")
        assert msg is not None
        assert result is not None
