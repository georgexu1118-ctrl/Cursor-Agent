"""Unit tests for structured logging configuration."""

import logging

from research_agent.logging_config import configure_logging, get_logger


def test_configure_logging_sets_level() -> None:
    """configure_logging sets the root logger to the requested level."""
    configure_logging("DEBUG")
    assert logging.getLogger().level == logging.DEBUG


def test_get_logger_returns_bound_logger() -> None:
    """get_logger returns a logger that accepts structured key-value context."""
    configure_logging("INFO")
    logger = get_logger("test")
    logger.info("event", key="value")
