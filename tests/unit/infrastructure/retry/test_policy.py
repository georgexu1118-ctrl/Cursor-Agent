"""Unit tests for retry policy."""

from research_agent.infrastructure.config.settings import Settings
from research_agent.infrastructure.retry.policy import RetryPolicy, compute_retry_delay


def test_retry_policy_from_settings() -> None:
    """RetryPolicy maps values from application settings."""
    settings = Settings(
        retry_max_attempts=4,
        retry_base_delay_seconds=0.5,
        retry_max_delay_seconds=8.0,
        retry_exponential_base=3.0,
        _env_file=None,
    )

    policy = RetryPolicy.from_settings(settings)

    assert policy.max_attempts == 4
    assert policy.base_delay_seconds == 0.5
    assert policy.max_delay_seconds == 8.0
    assert policy.exponential_base == 3.0


def test_compute_retry_delay_uses_exponential_backoff() -> None:
    """Retry delay grows exponentially and respects the configured cap."""
    policy = RetryPolicy(
        base_delay_seconds=1.0,
        max_delay_seconds=5.0,
        exponential_base=2.0,
    )

    assert compute_retry_delay(1, policy) == 1.0
    assert compute_retry_delay(2, policy) == 2.0
    assert compute_retry_delay(3, policy) == 4.0
    assert compute_retry_delay(4, policy) == 5.0
