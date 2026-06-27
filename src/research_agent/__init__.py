"""Research Agent — production-quality AI research agent framework."""

from research_agent.application.bootstrap import (
    ApplicationContext,
    bootstrap,
    create_container,
)

__all__ = [
    "ApplicationContext",
    "__version__",
    "bootstrap",
    "create_container",
]

__version__ = "0.2.0"
