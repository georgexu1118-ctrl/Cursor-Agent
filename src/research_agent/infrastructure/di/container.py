"""Lightweight dependency injection container."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar, cast

T = TypeVar("T")


class ServiceNotRegisteredError(LookupError):
    """Raised when a requested service type has not been registered."""


@dataclass(frozen=True)
class _Registration(Generic[T]):  # noqa: UP046
    """Internal registration metadata for a service factory."""

    factory: Callable[[], T]
    singleton: bool


class Container:
    """Register and resolve application services by type."""

    def __init__(self) -> None:
        self._registrations: dict[type[object], _Registration[object]] = {}
        self._singletons: dict[type[object], object] = {}

    def register(
        self,
        service_type: type[T],
        factory: Callable[[], T],
        *,
        singleton: bool = True,
    ) -> None:
        """Register a factory for the given service type.

        Args:
            service_type: Type key used for resolution.
            factory: Callable that creates the service instance.
            singleton: When ``True``, reuse the first resolved instance.
        """
        self._registrations[service_type] = _Registration(
            factory=factory,
            singleton=singleton,
        )
        self._singletons.pop(service_type, None)

    def register_instance(self, service_type: type[T], instance: T) -> None:
        """Register a pre-built singleton instance for the given service type."""
        self._registrations[service_type] = _Registration(
            factory=lambda: instance,
            singleton=True,
        )
        self._singletons[service_type] = instance

    def resolve(self, service_type: type[T]) -> T:
        """Resolve a service instance by type.

        Args:
            service_type: Registered service type to resolve.

        Returns:
            Service instance produced by the registered factory.

        Raises:
            ServiceNotRegisteredError: If the service type is not registered.
        """
        registration = self._registrations.get(service_type)
        if registration is None:
            msg = f"Service not registered: {service_type.__name__}"
            raise ServiceNotRegisteredError(msg)

        if registration.singleton:
            cached = self._singletons.get(service_type)
            if cached is not None:
                return cast(T, cached)

            instance = registration.factory()
            self._singletons[service_type] = instance
            return cast(T, instance)

        return cast(T, registration.factory())

    def is_registered(self, service_type: type[object]) -> bool:
        """Return whether the given service type is registered."""
        return service_type in self._registrations
