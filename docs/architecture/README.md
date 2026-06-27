# Architecture

This document describes the high-level architecture of the Research Agent framework.

## Overview

The framework follows **Clean Architecture** with four layers:

| Layer | Responsibility |
|-------|----------------|
| **Domain** | Entities, value objects, interfaces, domain services |
| **Application** | Use cases, orchestration, agent loop |
| **Infrastructure** | Provider implementations (LLM, search, storage, etc.) |
| **Interfaces** | CLI, API, and other entry points |

## Dependency Rule

Dependencies point inward. The orchestration layer depends only on abstractions defined in the domain and application layers. Provider-specific SDKs live exclusively in infrastructure.

## Planned Provider Abstractions

Future milestones will introduce interchangeable interfaces for:

- LLM providers
- Search providers
- Memory providers
- Embedding providers
- Storage providers
- Report generators

## Repository Layout

```
src/research_agent/
  domain/
  application/
  infrastructure/
  interfaces/
  config.py
  logging_config.py
tests/
  unit/
  integration/
docs/
examples/
scripts/
```

See [configuration.md](configuration.md) for environment variables and settings.
