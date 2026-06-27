"""Structured logging configuration for the framework."""

import logging
from typing import cast

import structlog
from structlog.stdlib import BoundLogger


def configure_logging(log_level: str = "INFO") -> None:
    """Configure structlog and stdlib logging for the application.

    Args:
        log_level: Logging level name (e.g. ``INFO``, ``DEBUG``).
    """
    level = getattr(logging, log_level.upper(), logging.INFO)

    logging.basicConfig(format="%(message)s", level=level, force=True)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> BoundLogger:
    """Return a structured logger bound to the given name.

    Args:
        name: Logger name, typically ``__name__`` of the calling module.

    Returns:
        Configured structlog bound logger.
    """
    return cast(BoundLogger, structlog.get_logger(name))
