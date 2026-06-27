"""Unit tests for retry execution utilities."""

from __future__ import annotations

import pytest

from research_agent.infrastructure.retry.policy import RetryPolicy
from research_agent.infrastructure.retry.retry import (
    RetryError,
    async_retry,
    call_with_retry,
    call_with_retry_async,
    retry,
)


def test_call_with_retry_recovers_before_max_attempts() -> None:
    """call_with_retry returns when a later attempt succeeds."""
    attempts = {"count": 0}
    delays: list[float] = []

    def flaky() -> str:
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise RuntimeError("temporary")
        return "ok"

    policy = RetryPolicy(max_attempts=3, base_delay_seconds=1.0, max_delay_seconds=10.0)
    result = call_with_retry(flaky, policy, sleep=delays.append)

    assert result == "ok"
    assert attempts["count"] == 3
    assert delays == [1.0, 2.0]


def test_call_with_retry_raises_retry_error_when_exhausted() -> None:
    """call_with_retry raises RetryError after all attempts fail."""
    policy = RetryPolicy(max_attempts=2, base_delay_seconds=0.1, max_delay_seconds=1.0)
    delays: list[float] = []

    def always_fail() -> None:
        raise ValueError("fail")

    with pytest.raises(RetryError) as exc_info:
        call_with_retry(always_fail, policy, sleep=delays.append)

    assert exc_info.value.attempts == 2
    assert isinstance(exc_info.value.last_exception, ValueError)
    assert delays == [0.1]


def test_retry_decorator_retries_sync_function() -> None:
    """The retry decorator applies retry policy to sync callables."""
    attempts = {"count": 0}
    policy = RetryPolicy(max_attempts=2, base_delay_seconds=0.0, max_delay_seconds=0.0)

    @retry(policy, retry_on=(RuntimeError,))
    def flaky() -> str:
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise RuntimeError("temporary")
        return "done"

    assert flaky() == "done"
    assert attempts["count"] == 2


@pytest.mark.asyncio
async def test_call_with_retry_async_recovers_before_max_attempts() -> None:
    """call_with_retry_async returns when a later attempt succeeds."""
    attempts = {"count": 0}
    delays: list[float] = []

    async def sleep(delay: float) -> None:
        delays.append(delay)

    async def flaky() -> str:
        attempts["count"] += 1
        if attempts["count"] < 2:
            raise RuntimeError("temporary")
        return "ok"

    policy = RetryPolicy(max_attempts=3, base_delay_seconds=0.5, max_delay_seconds=5.0)
    result = await call_with_retry_async(flaky, policy, sleep=sleep)

    assert result == "ok"
    assert attempts["count"] == 2
    assert delays == [0.5]


@pytest.mark.asyncio
async def test_async_retry_decorator_retries_async_function() -> None:
    """The async_retry decorator applies retry policy to async callables."""
    attempts = {"count": 0}
    policy = RetryPolicy(max_attempts=2, base_delay_seconds=0.0, max_delay_seconds=0.0)

    @async_retry(policy, retry_on=(RuntimeError,))
    async def flaky() -> str:
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise RuntimeError("temporary")
        return "done"

    assert await flaky() == "done"
    assert attempts["count"] == 2
