"""Application settings model and validation."""

from enum import StrEnum

from pydantic import Field, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMProviderName(StrEnum):
    """Supported LLM provider identifiers."""

    MOCK = "mock"
    OPENAI = "openai"


class LogFormat(StrEnum):
    """Supported structured log output formats."""

    CONSOLE = "console"
    JSON = "json"


class Settings(BaseSettings):
    """Application settings validated at startup.

    Attributes:
        environment: Deployment environment name.
        log_level: Python logging level name.
        log_format: Structured log renderer format.
        llm_provider: LLM backend to use (``mock`` or ``openai``).
        openai_api_key: OpenAI secret key (required when ``llm_provider=openai``).
        openai_model: OpenAI model name used for completions.
        retry_max_attempts: Maximum retry attempts for external calls.
        retry_base_delay_seconds: Initial delay between retries in seconds.
        retry_max_delay_seconds: Upper bound for retry delay in seconds.
        retry_exponential_base: Exponential backoff multiplier.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    environment: str = Field(default="development", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_format: LogFormat = Field(default=LogFormat.CONSOLE, alias="LOG_FORMAT")

    # LLM provider selection and configuration
    llm_provider: LLMProviderName = Field(
        default=LLMProviderName.MOCK,
        alias="LLM_PROVIDER",
    )
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")

    retry_max_attempts: int = Field(default=3, alias="RETRY_MAX_ATTEMPTS", ge=1)
    retry_base_delay_seconds: float = Field(
        default=1.0,
        alias="RETRY_BASE_DELAY_SECONDS",
        gt=0,
    )
    retry_max_delay_seconds: float = Field(
        default=60.0,
        alias="RETRY_MAX_DELAY_SECONDS",
        gt=0,
    )
    retry_exponential_base: float = Field(
        default=2.0,
        alias="RETRY_EXPONENTIAL_BASE",
        gt=1,
    )

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

    @field_validator("retry_max_delay_seconds")
    @classmethod
    def validate_max_delay_not_less_than_base(
        cls,
        value: float,
        info: ValidationInfo,
    ) -> float:
        """Ensure max retry delay is not less than the base delay."""
        base_delay = info.data.get("retry_base_delay_seconds")
        if base_delay is not None and value < base_delay:
            msg = (
                "RETRY_MAX_DELAY_SECONDS must be greater than or equal to "
                "RETRY_BASE_DELAY_SECONDS"
            )
            raise ValueError(msg)
        return value
