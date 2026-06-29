"""Research agent use case: search then summarise."""

from __future__ import annotations

from dataclasses import dataclass

from research_agent.domain.entities import Message, MessageRole, SearchResult
from research_agent.domain.providers import LLMProvider, SearchProvider


@dataclass(frozen=True)
class ResearchResult:
    """Outcome of a single research query.

    Attributes:
        query: The original user question.
        sources: Search results used as context for the LLM.
        summary: LLM-generated answer grounded in the sources.
    """

    query: str
    sources: list[SearchResult]
    summary: str


class ResearchAgent:
    """Orchestrates search and LLM summarisation to answer a research query.

    Depends only on the ``LLMProvider`` and ``SearchProvider`` protocols;
    no infrastructure imports appear here.

    Args:
        llm: Provider used to generate the research summary.
        search: Provider used to retrieve relevant sources.
    """

    _SYSTEM_PROMPT = (
        "You are a research assistant. "
        "Read the provided search results and write a concise, accurate summary "
        "that directly answers the user's query. "
        "Cite sources where relevant."
    )

    def __init__(self, llm: LLMProvider, search: SearchProvider) -> None:
        self._llm = llm
        self._search = search

    async def run(
        self,
        query: str,
        *,
        max_results: int = 5,
        max_tokens: int = 1024,
    ) -> ResearchResult:
        """Execute a research query: retrieve sources, then summarise.

        Args:
            query: Natural-language research question.
            max_results: Maximum number of search results to retrieve.
            max_tokens: Upper bound on tokens in the LLM response.

        Returns:
            A ``ResearchResult`` containing the query, sources, and summary.
        """
        sources = await self._search.search(query, max_results=max_results)
        messages = self._build_messages(query, sources)
        summary = await self._llm.complete(messages, max_tokens=max_tokens)
        return ResearchResult(query=query, sources=sources, summary=summary)

    def _build_messages(
        self,
        query: str,
        sources: list[SearchResult],
    ) -> list[Message]:
        """Format the query and search results into an LLM conversation."""
        if sources:
            sources_text = "\n\n".join(
                f"[{i + 1}] {r.title}\n{r.url}\n{r.snippet}"
                for i, r in enumerate(sources)
            )
        else:
            sources_text = "No search results found."

        user_content = f"Query: {query}\n\nSearch results:\n{sources_text}"
        return [
            Message(role=MessageRole.SYSTEM, content=self._SYSTEM_PROMPT),
            Message(role=MessageRole.USER, content=user_content),
        ]
