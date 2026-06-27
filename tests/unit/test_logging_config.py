"""Unit tests for structured logging configuration."""

import logging

from research_agent.infrastructure.config.settings import LogFormat
from research_agent.infrastructure.logging.setup import configure_logging, get_logger


def test_configure_logging_sets_level() -> None:
    """configure_logging sets the root logger to the requested level."""
    configure_logging("DEBUG")
    assert logging.getLogger().level == logging.DEBUG


def test_configure_logging_supports_json_format() -> None:
    """configure_logging accepts JSON log format without error."""
    configure_logging("INFO", log_format=LogFormat.JSON)
    logger = get_logger("test")
    logger.info("event", key="value")


def test_get_logger_returns_bound_logger() -> None:
    """get_logger returns a logger that accepts structured key-value context."""
    configure_logging("INFO")
    logger = get_logger("test")
    logger.info("event", key="value")
