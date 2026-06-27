# Research Agent

Production-quality Python framework for building AI research agents with interchangeable providers and Clean Architecture.

## Status

**Milestone 3 complete** — domain provider interfaces (`LLMProvider`, `SearchProvider`) and value objects (`Message`, `SearchResult`) are in place. Concrete provider implementations and agent orchestration will be added in later milestones.

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

Bootstrap the application to load settings, configure structured logging, and initialize the dependency injection container:

```python
from research_agent import bootstrap
from research_agent.infrastructure.retry import RetryPolicy

context = bootstrap()
logger = context.logger
settings = context.settings
retry_policy = context.container.resolve(RetryPolicy)

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
  domain/              # Entities, interfaces, domain services
  application/         # Bootstrap and use cases
  infrastructure/
    config/            # Settings and env loading
    logging/           # Structured logging setup
    di/                # Dependency injection container
    retry/             # Retry policy and utilities
  interfaces/          # CLI, API, entry points
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
