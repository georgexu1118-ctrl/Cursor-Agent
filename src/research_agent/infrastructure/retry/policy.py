"""Retry policy configuration."""

from dataclasses import dataclass
from typing import Self

from research_agent.infrastructure.config.settings import Settings


@dataclass(frozen=True)
class RetryPolicy:
    """Configurable retry behavior for external calls.

    Attributes:
        max_attempts: Total number of attempts including the first call.
        base_delay_seconds: Initial delay before the first retry.
        max_delay_seconds: Maximum delay between retries.
        exponential_base: Multiplier applied per failed attempt.
    """

    max_attempts: int = 3
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 60.0
    exponential_base: float = 2.0

    @classmethod
    def from_settings(cls, settings: Settings) -> Self:
        """Build a retry policy from application settings."""
        return cls(
            max_attempts=settings.retry_max_attempts,
            base_delay_seconds=settings.retry_base_delay_seconds,
            max_delay_seconds=settings.retry_max_delay_seconds,
            exponential_base=settings.retry_exponential_base,
        )


def compute_retry_delay(attempt: int, policy: RetryPolicy) -> float:
    """Compute exponential backoff delay for a retry attempt.

    Args:
        attempt: One-based retry attempt number.
        policy: Retry policy defining backoff parameters.

    Returns:
        Delay in seconds, capped at ``policy.max_delay_seconds``.
    """
    exponent = max(attempt - 1, 0)
    delay = policy.base_delay_seconds * (policy.exponential_base**exponent)
    return min(delay, policy.max_delay_seconds)
