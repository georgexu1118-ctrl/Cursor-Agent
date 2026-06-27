"""Centralized application configuration loaded from environment variables."""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings validated at startup.

    Attributes:
        environment: Deployment environment name.
        log_level: Python logging level name.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    environment: str = Field(default="development", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        """Normalize and validate the configured log level."""
        normalized = value.upper()
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if normalized not in valid_levels:
            msg = f"Invalid LOG_LEVEL '{value}'. Must be one of: {sorted(valid_levels)}"
            raise ValueError(msg)
        return normalized


def load_settings() -> Settings:
    """Load and validate settings from the environment.

    Returns:
        Validated application settings.

    Raises:
        ValidationError: If required settings are missing or invalid.
    """
    return Settings()
