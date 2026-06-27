# Claude Code Workflow

## Purpose

Claude Code is the main implementation agent for this repository.

Use Claude Code to build the project milestone by milestone. Claude should focus on architecture, feature implementation, clean code, tests, and documentation.

Cursor is used for opening the repo, inspecting files, manually editing, running terminal commands, committing, and pushing.

Codex is used after Claude Code to review, debug, and fix errors.

## Important rule

Always run Claude Code from the repository root, not from inside `.claude`.

Correct:

```powershell
cd C:\Users\georg\Projects\Cursor-Agent
claude
```

Incorrect:

```powershell
cd C:\Users\georg\Projects\Cursor-Agent\.claude
claude
```

The repo root is the folder containing:

```txt
README.md
pyproject.toml
src/
tests/
docs/
.claude/
.codex/
.cursor/
CLAUDE.md
AGENTS.md
```

## Claude Code responsibilities

Claude Code should:

1. Build one milestone at a time.
2. Preserve the existing architecture.
3. Create production-quality code.
4. Add or update tests when changing behavior.
5. Keep commits logically organized.
6. Avoid unnecessary rewrites.
7. Explain what changed after each milestone.
8. Stop after the requested milestone is complete.
9. Avoid implementing future milestones early.
10. Keep the repo clean and easy to review.

## Before starting a milestone

Claude should read these files first:

```txt
README.md
CLAUDE.md
AGENTS.md
.claude/workflow.md
pyproject.toml
```

Then Claude should inspect the relevant source folders:

```txt
src/
tests/
docs/
examples/
scripts/
.github/workflows/
```

Claude should understand the current architecture before editing.

## Milestone workflow

For each milestone, follow this process:

### 1. Understand the goal

Restate the milestone in practical terms.

Example:

```txt
Milestone 1: Create the production-ready project foundation.
Do not implement the AI research agent yet.
```

### 2. Inspect the current repo

Before editing, inspect:

```txt
README.md
pyproject.toml
src/
tests/
docs/
.github/workflows/ci.yml
```

Do not assume files exist. Check first.

### 3. Plan the smallest safe implementation

Make a short implementation plan before changing files.

The plan should include:

```txt
Files to create
Files to edit
Tests to add/update
Commands to run
Expected final state
```

### 4. Implement only the milestone

Do not jump ahead.

If the user asks for Milestone 1, do not build Milestone 2.

If the user asks for config/logging/retry/DI, do not build the full research agent.

### 5. Add tests

Any meaningful logic should have tests.

Prefer simple tests that check behavior clearly.

Do not remove tests to make the suite pass.

### 6. Run checks

Use the project’s configured tools.

Common commands:

```powershell
ruff check .
ruff format --check .
mypy src
pytest
```

If formatting is needed:

```powershell
ruff format .
```

### 7. Summarize results

At the end, summarize:

```txt
What was built
Files changed
Tests added
Commands run
Any remaining issues
Recommended next milestone
```

## Coding standards

Use clean, maintainable Python.

Prefer:

```txt
Small modules
Clear names
Type hints
Dataclasses or Pydantic models where useful
Dependency inversion
Interface-first design
Explicit error handling
Simple tests
Readable docs
```

Avoid:

```txt
Huge files
Hidden global state
Hardcoded secrets
Unnecessary abstractions
Overengineering
Mixing infrastructure with domain logic
Changing unrelated code
```

## Architecture principles

The project should favor:

```txt
dependency inversion
interface-first design
modularity
extensibility
maintainability
scalable repository organization
```

Suggested separation:

```txt
src/research_agent/domain/
src/research_agent/application/
src/research_agent/infrastructure/
src/research_agent/services/
src/research_agent/config/
src/research_agent/utils/
tests/
docs/
examples/
scripts/
```

Domain code should not depend directly on infrastructure.

Infrastructure can depend on domain/application interfaces.

Application orchestration should connect domain logic to infrastructure adapters.

## Git behavior

Claude Code should not push automatically unless the user explicitly asks.

Preferred flow:

```txt
Claude Code edits files
Cursor terminal runs checks
Cursor user reviews diff
Cursor commits
Cursor pushes
Codex reviews/debugs if needed
```

## What Claude should not do

Claude should not:

```txt
Add API keys
Create real .env files with secrets
Delete tests to pass checks
Rewrite the whole project without permission
Change project goals without asking
Build future milestones early
Commit or push without explicit instruction
Ignore failing tests
Hide errors
```

## Good Claude prompt template

Use this when asking Claude Code to build a milestone:

```txt
Read CLAUDE.md, AGENTS.md, .claude/workflow.md, README.md, and pyproject.toml first.

Proceed with Milestone X: [describe milestone].

Build this milestone only. Do not implement future milestones.

Preserve the existing architecture. Keep changes small, typed, tested, and maintainable.

After implementing, run or tell me to run:
- ruff check .
- ruff format --check .
- mypy src
- pytest

Stop after the milestone is complete and summarize:
1. files changed,
2. tests added,
3. commands run,
4. remaining issues,
5. next recommended milestone.
```

## Milestone completion checklist

A milestone is complete only when:

```txt
The requested files/features exist
The implementation matches the requested scope
Tests are added or updated where needed
Ruff passes
Formatting passes
MyPy passes or known issues are documented
Pytest passes
README/docs are updated if needed
No secrets are committed
The diff is reviewable
```

## Relationship with Codex

After Claude Code completes a milestone, Codex should review/debug.

Claude Code builds.

Codex verifies and fixes.

Cursor controls the repo, terminal, commits, and pushes.
