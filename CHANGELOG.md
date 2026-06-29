# Changelog

All notable changes to this project will be documented in this file.

## [0.6.0] - 2026-06-28

### Added

- `research-agent` console script registered in `pyproject.toml`.
- `interfaces/cli.py`: argument parsing (`query`, `--max-results`, `--max-tokens`, `--env-file`), formatted output with source list, error handling with stderr + exit code 1.
- 22 unit tests covering parser defaults, output formatting, `_run()` coroutine, and `main()` success/error paths. No real network calls.

## [0.5.0] - 2026-06-28

### Added

- `ResearchAgent` use case in `application/research_agent.py`: accepts a query, retrieves sources via `SearchProvider`, formats them into an LLM prompt, and returns a `ResearchResult`.
- `ResearchResult` frozen dataclass: `query`, `sources`, `summary`.
- `create_search_provider` factory in `infrastructure/providers/factory.py` (returns `MockSearchProvider`; real backends in a later milestone).
- `LLMProvider`, `SearchProvider`, and `ResearchAgent` are now registered in the DI container by `create_container`.
- `ResearchAgent` and `ResearchResult` exported from the top-level `research_agent` package.
- Unit tests: 19 new tests covering `ResearchResult` immutability, `ResearchAgent.run()` behaviour, message construction, and container registration.

## [0.4.0] - 2026-06-27

### Added

- `MockLLMProvider` — deterministic in-memory LLM provider for tests.
- `MockSearchProvider` — deterministic in-memory search provider for tests.
- `OpenAILLMProvider` — chat completion via the OpenAI SDK; key validated at construction.
- `create_llm_provider` factory that selects an implementation from `LLM_PROVIDER` config.
- `LLMProviderName` enum and three new settings: `LLM_PROVIDER`, `OPENAI_API_KEY`, `OPENAI_MODEL`.
- `openai>=1.0` optional dependency (`pip install research-agent[openai]`).
- Unit tests for all new providers and the factory; no real network calls required.

## [0.3.0] - 2026-06-27

### Added

- Domain value objects: `MessageRole`, `Message`, `SearchResult` (frozen dataclasses).
- Domain provider protocols: `LLMProvider`, `SearchProvider` (`@runtime_checkable`).
- `domain/__init__.py` re-exports all public domain types.
- Unit tests for entity construction, immutability, equality, and protocol conformance.

## [0.2.0] - 2026-06-26

### Added

- Core infrastructure: centralized configuration, dotenv loading, structured logging (console/json).
- Dependency injection container with singleton and transient registrations.
- Retry utilities with configurable exponential backoff (sync and async).
- Application bootstrap wiring settings, logging, and core services.
- Unit tests for config, logging, DI, retry, and bootstrap.

## [0.1.0] - 2026-06-26

### Added

- Project foundation: Clean Architecture package layout, configuration, and structured logging.
- Tooling: Ruff, Black, MyPy, pytest, and GitHub Actions CI.
- Documentation: README, architecture overview, and configuration reference.
