"""Unit tests for ResearchAgent use case."""

from __future__ import annotations

import pytest

from research_agent.application.research_agent import ResearchAgent, ResearchResult
from research_agent.domain.entities import Message, MessageRole, SearchResult
from research_agent.infrastructure.providers.llm.mock import MockLLMProvider
from research_agent.infrastructure.providers.search.mock import MockSearchProvider

_SOURCE = SearchResult(
    url="https://example.com",
    title="Example Article",
    snippet="Very useful information.",
    score=0.9,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _CapturingLLM:
    """Records the messages list passed to each complete() call."""

    def __init__(self, response: str = "captured response") -> None:
        self.calls: list[list[Message]] = []
        self._response = response

    async def complete(
        self,
        messages: list[Message],
        *,
        max_tokens: int = 1024,
    ) -> str:
        self.calls.append(messages)
        return self._response


class _CapturingSearch:
    """Records calls to search() and delegates to an inner provider."""

    def __init__(self, results: list[SearchResult] | None = None) -> None:
        self._inner = MockSearchProvider(results=results)
        self.calls: list[tuple[str, int]] = []

    async def search(
        self,
        query: str,
        *,
        max_results: int = 10,
    ) -> list[SearchResult]:
        self.calls.append((query, max_results))
        return await self._inner.search(query, max_results=max_results)


# ---------------------------------------------------------------------------
# ResearchResult value object
# ---------------------------------------------------------------------------


class TestResearchResult:
    def test_creation(self) -> None:
        result = ResearchResult(query="q", sources=[], summary="s")
        assert result.query == "q"
        assert result.sources == []
        assert result.summary == "s"

    def test_immutable_query(self) -> None:
        result = ResearchResult(query="q", sources=[], summary="s")
        with pytest.raises(AttributeError):
            result.query = "changed"  # type: ignore[misc]

    def test_immutable_summary(self) -> None:
        result = ResearchResult(query="q", sources=[], summary="s")
        with pytest.raises(AttributeError):
            result.summary = "changed"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# ResearchAgent.run() core behaviour
# ---------------------------------------------------------------------------


class TestResearchAgentRun:
    async def test_returns_research_result(self) -> None:
        agent = ResearchAgent(llm=MockLLMProvider(), search=MockSearchProvider())
        result = await agent.run("test query")
        assert isinstance(result, ResearchResult)

    async def test_preserves_query(self) -> None:
        agent = ResearchAgent(llm=MockLLMProvider(), search=MockSearchProvider())
        result = await agent.run("what is Python?")
        assert result.query == "what is Python?"

    async def test_sources_come_from_search_provider(self) -> None:
        agent = ResearchAgent(
            llm=MockLLMProvider(),
            search=MockSearchProvider(results=[_SOURCE]),
        )
        result = await agent.run("test")
        assert result.sources == [_SOURCE]

    async def test_summary_comes_from_llm_provider(self) -> None:
        agent = ResearchAgent(
            llm=MockLLMProvider(response="LLM answer here."),
            search=MockSearchProvider(),
        )
        result = await agent.run("test")
        assert result.summary == "LLM answer here."

    async def test_max_results_forwarded_to_search(self) -> None:
        many = [
            SearchResult(url=f"https://{i}.com", title=str(i), snippet="s")
            for i in range(10)
        ]
        capture = _CapturingSearch(results=many)
        agent = ResearchAgent(llm=MockLLMProvider(), search=capture)
        result = await agent.run("query", max_results=3)
        assert len(result.sources) == 3
        assert capture.calls[0] == ("query", 3)

    async def test_search_called_with_original_query(self) -> None:
        capture = _CapturingSearch()
        agent = ResearchAgent(llm=MockLLMProvider(), search=capture)
        await agent.run("climate change impact")
        assert capture.calls[0][0] == "climate change impact"

    async def test_empty_search_results_still_returns_summary(self) -> None:
        agent = ResearchAgent(
            llm=MockLLMProvider(response="Nothing found."),
            search=MockSearchProvider(),
        )
        result = await agent.run("obscure query")
        assert result.summary == "Nothing found."
        assert result.sources == []


# ---------------------------------------------------------------------------
# Message construction
# ---------------------------------------------------------------------------


class TestMessageBuilding:
    async def test_first_message_is_system_prompt(self) -> None:
        capture = _CapturingLLM()
        agent = ResearchAgent(llm=capture, search=MockSearchProvider())
        await agent.run("my query")
        messages = capture.calls[0]
        assert messages[0].role == MessageRole.SYSTEM

    async def test_last_message_is_user_message(self) -> None:
        capture = _CapturingLLM()
        agent = ResearchAgent(llm=capture, search=MockSearchProvider())
        await agent.run("my query")
        messages = capture.calls[0]
        assert messages[-1].role == MessageRole.USER

    async def test_user_message_contains_query(self) -> None:
        capture = _CapturingLLM()
        agent = ResearchAgent(llm=capture, search=MockSearchProvider())
        await agent.run("what is machine learning?")
        user_content = capture.calls[0][-1].content
        assert "what is machine learning?" in user_content

    async def test_user_message_contains_source_title(self) -> None:
        capture = _CapturingLLM()
        agent = ResearchAgent(
            llm=capture,
            search=MockSearchProvider(results=[_SOURCE]),
        )
        await agent.run("query")
        user_content = capture.calls[0][-1].content
        assert "Example Article" in user_content

    async def test_user_message_contains_source_snippet(self) -> None:
        capture = _CapturingLLM()
        agent = ResearchAgent(
            llm=capture,
            search=MockSearchProvider(results=[_SOURCE]),
        )
        await agent.run("query")
        user_content = capture.calls[0][-1].content
        assert "Very useful information." in user_content

    async def test_user_message_contains_source_url(self) -> None:
        capture = _CapturingLLM()
        agent = ResearchAgent(
            llm=capture,
            search=MockSearchProvider(results=[_SOURCE]),
        )
        await agent.run("query")
        user_content = capture.calls[0][-1].content
        assert "https://example.com" in user_content

    async def test_empty_sources_noted_in_user_message(self) -> None:
        capture = _CapturingLLM()
        agent = ResearchAgent(llm=capture, search=MockSearchProvider())
        await agent.run("query")
        user_content = capture.calls[0][-1].content
        assert "No search results found." in user_content

    async def test_multiple_sources_all_appear(self) -> None:
        sources = [
            SearchResult(url="https://a.com", title="Alpha", snippet="snippet a"),
            SearchResult(url="https://b.com", title="Beta", snippet="snippet b"),
        ]
        capture = _CapturingLLM()
        agent = ResearchAgent(
            llm=capture,
            search=MockSearchProvider(results=sources),
        )
        await agent.run("query")
        user_content = capture.calls[0][-1].content
        assert "Alpha" in user_content
        assert "Beta" in user_content
