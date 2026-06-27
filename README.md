# Research Agent

Production-quality Python framework for building AI research agents with interchangeable providers and Clean Architecture.

## Status

**Milestone 1 complete** — project foundation, tooling, and CI are in place. Agent orchestration and provider implementations will be added in later milestones.

## Prerequisites

- Python 3.12 or newer
- pip

## Installation

Create a virtual environment and install the package with development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Alternatively:

```bash
pip install -r requirements.txt
pip install -e .
```

## Configuration

Copy the example environment file and adjust values:

```bash
cp .env.example .env
```

See [docs/configuration.md](docs/configuration.md) for the full environment variable reference.

## Quick Start

Load validated settings and configure structured logging:

```python
from research_agent.config import load_settings
from research_agent.logging_config import configure_logging, get_logger

settings = load_settings()
configure_logging(settings.log_level)

logger = get_logger(__name__)
logger.info("framework_ready", environment=settings.environment)
```

## Development

Run the same checks as CI locally:

```bash
python scripts/check.py
```

Or individually:

```bash
ruff check .
ruff format --check .
black --check .
mypy src/
pytest
```

With Make (Linux/macOS):

```bash
make check
```

## Project Structure

```
src/research_agent/
  domain/           # Entities, interfaces, domain services
  application/      # Use cases and orchestration
  infrastructure/   # Provider implementations
  interfaces/       # CLI, API, entry points
  config.py         # Centralized configuration
  logging_config.py # Structured logging setup
tests/
  unit/
  integration/
docs/
examples/
scripts/
```

Architecture details: [docs/architecture/README.md](docs/architecture/README.md)

## License

MIT — see [LICENSE](LICENSE).
