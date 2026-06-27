# Architecture

This document describes the high-level architecture of the Research Agent framework.

## Overview

The framework follows **Clean Architecture** with four layers:

| Layer | Responsibility |
|-------|----------------|
| **Domain** | Entities, value objects, interfaces, domain services |
| **Application** | Use cases, orchestration, bootstrap |
| **Infrastructure** | Configuration, logging, DI, retry, provider implementations |
| **Interfaces** | CLI, API, and other entry points |

## Dependency Rule

Dependencies point inward. The orchestration layer depends only on abstractions defined in the domain and application layers. Provider-specific SDKs live exclusively in infrastructure.

## Core Infrastructure (Milestone 2)

| Module | Responsibility |
|--------|----------------|
| `infrastructure/config` | Settings model, environment variable and dotenv loading |
| `infrastructure/logging` | Structured logging with console or JSON output |
| `infrastructure/di` | Lightweight dependency injection container |
| `infrastructure/retry` | Retry policy and exponential backoff utilities |
| `application/bootstrap` | Application startup and service registration |

## Domain Provider Interfaces (Milestone 3)

| Module | Responsibility |
|--------|----------------|
| `domain/entities.py` | `MessageRole`, `Message`, `SearchResult` value objects |
| `domain/providers.py` | `LLMProvider`, `SearchProvider` runtime-checkable protocols |

All provider protocols use `@runtime_checkable` structural typing. Concrete
implementations in the infrastructure layer need only satisfy the protocol
structurally — no inheritance is required.

## Planned Provider Implementations

Future milestones will add concrete infrastructure adapters for:

- LLM providers (Anthropic, OpenAI, …)
- Search providers (Brave, Tavily, …)
- Memory providers
- Embedding providers
- Storage providers
- Report generators

## Repository Layout

```
src/research_agent/
  domain/
    entities.py        # Message, SearchResult value objects
    providers.py       # LLMProvider, SearchProvider protocols
  application/
    bootstrap.py
  infrastructure/
    config/
    logging/
    di/
    retry/
  interfaces/
tests/
  unit/
    domain/
    infrastructure/
    application/
  integration/
docs/
examples/
scripts/
```

See [configuration.md](../configuration.md) for environment variables and settings.
