# Configuration Reference

Application settings are loaded from environment variables and validated at startup via `research_agent.infrastructure.config.Settings`.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENVIRONMENT` | No | `development` | Deployment environment (`development`, `staging`, `production`, etc.) |
| `LOG_LEVEL` | No | `INFO` | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL` |
| `LOG_FORMAT` | No | `console` | Structured log output: `console` or `json` |
| `DOTENV_PATH` | No | `.env` | Path to a dotenv file when present |
| `RETRY_MAX_ATTEMPTS` | No | `3` | Maximum attempts for retryable external calls |
| `RETRY_BASE_DELAY_SECONDS` | No | `1.0` | Initial retry delay in seconds |
| `RETRY_MAX_DELAY_SECONDS` | No | `60.0` | Maximum retry delay in seconds |
| `RETRY_EXPONENTIAL_BASE` | No | `2.0` | Exponential backoff multiplier |

## Usage

Copy the example file and adjust values for your environment:

```bash
cp .env.example .env
```

Bootstrap the application with centralized configuration, logging, and dependency injection:

```python
from research_agent import bootstrap
from research_agent.infrastructure.retry import RetryPolicy

context = bootstrap()
retry_policy = context.container.resolve(RetryPolicy)
logger = context.logger
settings = context.settings
```

Or load settings and configure logging manually:

```python
from research_agent.infrastructure.config import load_settings
from research_agent.infrastructure.logging import configure_logging, get_logger

settings = load_settings()
configure_logging(settings.log_level, log_format=settings.log_format)
logger = get_logger(__name__)
```

## Validation

Invalid values (such as an unrecognized `LOG_LEVEL` or a `RETRY_MAX_DELAY_SECONDS` less than the base delay) raise a validation error at startup so misconfiguration fails fast.

Provider credentials and agent-specific settings will be documented in later milestones.
