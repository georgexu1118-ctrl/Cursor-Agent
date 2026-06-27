"""Dependency injection infrastructure."""

from research_agent.infrastructure.di.container import (
    Container,
    ServiceNotRegisteredError,
)

__all__ = ["Container", "ServiceNotRegisteredError"]
