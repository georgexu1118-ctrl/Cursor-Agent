"""Research Agent — production-quality AI research agent framework."""

from research_agent.application.bootstrap import (
    ApplicationContext,
    bootstrap,
    create_container,
)
from research_agent.application.research_agent import ResearchAgent, ResearchResult

__all__ = [
    "ApplicationContext",
    "ResearchAgent",
    "ResearchResult",
    "__version__",
    "bootstrap",
    "create_container",
]

__version__ = "0.6.0"
