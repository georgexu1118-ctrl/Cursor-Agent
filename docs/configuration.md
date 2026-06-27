# Configuration Reference

Application settings are loaded from environment variables and validated at startup via `research_agent.config.Settings`.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENVIRONMENT` | No | `development` | Deployment environment (`development`, `staging`, `production`, etc.) |
| `LOG_LEVEL` | No | `INFO` | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL` |

## Usage

Copy the example file and adjust values for your environment:

```bash
cp .env.example .env
```

Load settings in application code:

```python
from research_agent.config import load_settings
from research_agent.logging_config import configure_logging

settings = load_settings()
configure_logging(settings.log_level)
```

## Validation

Invalid values (such as an unrecognized `LOG_LEVEL`) raise a validation error at startup so misconfiguration fails fast.

Future milestones will document additional provider credentials and agent-specific settings here.
