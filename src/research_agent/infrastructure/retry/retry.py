"""Retry execution utilities with exponential backoff."""

from __future__ import annotations

import asyncio
import functools
import time
from collections.abc import Awaitable, Callable
from typing import ParamSpec, TypeVar

from research_agent.infrastructure.retry.policy import RetryPolicy, compute_retry_delay

P = ParamSpec("P")
T = TypeVar("T")


class RetryError(Exception):
    """Raised when all retry attempts are exhausted."""

    def __init__(
        self,
        message: str,
        *,
        attempts: int,
        last_exception: Exception,
    ) -> None:
        super().__init__(message)
        self.attempts = attempts
        self.last_exception = last_exception


def call_with_retry(  # noqa: UP047
    func: Callable[[], T],
    policy: RetryPolicy,
    *,
    retry_on: tuple[type[Exception], ...] = (Exception,),
    sleep: Callable[[float], None] = time.sleep,
) -> T:
    """Call ``func`` with retries using the provided policy.

    Args:
        func: Zero-argument callable to execute.
        policy: Retry policy controlling attempts and backoff.
        retry_on: Exception types that trigger a retry.
        sleep: Sleep function used between attempts (injectable for tests).

    Returns:
        Result of ``func`` when a call succeeds.

    Raises:
        RetryError: When all attempts fail with retryable exceptions.
    """
    last_exception: Exception | None = None

    for attempt in range(1, policy.max_attempts + 1):
        try:
            return func()
        except retry_on as exc:
            last_exception = exc
            if attempt >= policy.max_attempts:
                break
            sleep(compute_retry_delay(attempt, policy))

    assert last_exception is not None
    msg = f"Operation failed after {policy.max_attempts} attempts"
    raise RetryError(msg, attempts=policy.max_attempts, last_exception=last_exception)


async def call_with_retry_async(  # noqa: UP047
    func: Callable[[], Awaitable[T]],
    policy: RetryPolicy,
    *,
    retry_on: tuple[type[Exception], ...] = (Exception,),
    sleep: Callable[[float], Awaitable[None]] | None = None,
) -> T:
    """Call an async ``func`` with retries using the provided policy."""
    sleep_fn = sleep or asyncio.sleep
    last_exception: Exception | None = None

    for attempt in range(1, policy.max_attempts + 1):
        try:
            return await func()
        except retry_on as exc:
            last_exception = exc
            if attempt >= policy.max_attempts:
                break
            await sleep_fn(compute_retry_delay(attempt, policy))

    assert last_exception is not None
    msg = f"Operation failed after {policy.max_attempts} attempts"
    raise RetryError(msg, attempts=policy.max_attempts, last_exception=last_exception)


def retry(
    policy: RetryPolicy,
    *,
    retry_on: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator that retries a sync function using the provided policy."""

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            return call_with_retry(
                lambda: func(*args, **kwargs),
                policy,
                retry_on=retry_on,
            )

        return wrapper

    return decorator


def async_retry(
    policy: RetryPolicy,
    *,
    retry_on: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    """Decorator that retries an async function using the provided policy."""

    def decorator(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            return await call_with_retry_async(
                lambda: func(*args, **kwargs),
                policy,
                retry_on=retry_on,
            )

        return wrapper

    return decorator
