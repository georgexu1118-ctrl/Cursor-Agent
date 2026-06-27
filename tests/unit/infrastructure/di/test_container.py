"""Unit tests for dependency injection container."""

import pytest

from research_agent.infrastructure.di.container import (
    Container,
    ServiceNotRegisteredError,
)


class _Service:
    def __init__(self) -> None:
        self.value = "ready"


def test_register_and_resolve_singleton() -> None:
    """Singleton services return the same instance on repeated resolution."""
    container = Container()
    container.register(_Service, _Service, singleton=True)

    first = container.resolve(_Service)
    second = container.resolve(_Service)

    assert first is second


def test_register_and_resolve_transient() -> None:
    """Transient services create a new instance on each resolution."""
    container = Container()
    container.register(_Service, _Service, singleton=False)

    first = container.resolve(_Service)
    second = container.resolve(_Service)

    assert first is not second


def test_register_instance() -> None:
    """Pre-built instances can be registered directly."""
    container = Container()
    instance = _Service()
    container.register_instance(_Service, instance)

    assert container.resolve(_Service) is instance


def test_resolve_unregistered_service_raises() -> None:
    """Resolving an unregistered service raises ServiceNotRegisteredError."""
    container = Container()

    with pytest.raises(ServiceNotRegisteredError):
        container.resolve(_Service)


def test_is_registered_reports_registration_state() -> None:
    """is_registered reflects whether a service type is available."""
    container = Container()
    assert container.is_registered(_Service) is False

    container.register(_Service, _Service)
    assert container.is_registered(_Service) is True
