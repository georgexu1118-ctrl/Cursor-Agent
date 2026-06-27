# Codex Debugging Guide

## Purpose

Codex is the repository reviewer, debugger, and error-fixing assistant.

Use Codex after Claude Code has built a milestone or changed important code.

Codex should focus on:

```txt
lint errors
formatting errors
type errors
test failures
import problems
broken CI
small bugs
architecture regressions
missing edge cases
```

Codex should not be the main feature builder unless the user explicitly asks.

## Important rule

Always run Codex from the repository root, not from inside `.codex`.

Correct:

```powershell
cd C:\Users\georg\Projects\Cursor-Agent
codex
```

Incorrect:

```powershell
cd C:\Users\georg\Projects\Cursor-Agent\.codex
codex
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

## Codex responsibilities

Codex should:

1. Read the repo instructions first.
2. Run the project checks.
3. Identify real failures.
4. Fix the smallest safe set of files.
5. Avoid unrelated refactors.
6. Preserve architecture.
7. Rerun checks after fixing.
8. Explain what failed and what changed.

## Files to read first

Before making changes, read:

```txt
AGENTS.md
CLAUDE.md
README.md
pyproject.toml
.codex/debugging.md
.claude/workflow.md
.github/workflows/ci.yml
```

Then inspect relevant source and test files.

## Standard debugging workflow

### 1. Check repo state

Run:

```powershell
git status
```

Understand whether there are existing uncommitted changes.

Do not overwrite user changes.

### 2. Run checks

Run:

```powershell
ruff check .
ruff format --check .
mypy src
pytest
```

If a command is unavailable, report it clearly and inspect the project config.

### 3. Group failures by type

Classify problems into:

```txt
Formatting
Lint
Typing
Tests
Imports
Packaging
CI configuration
Architecture/design issues
```

### 4. Fix smallest safe set

Fix only what is needed.

Avoid broad rewrites.

Prefer targeted edits.

### 5. Rerun checks

After fixing, rerun:

```powershell
ruff check .
ruff format --check .
mypy src
pytest
```

If formatting is needed, run:

```powershell
ruff format .
```

Then rerun:

```powershell
ruff format --check .
```

### 6. Summarize

Final response should include:

```txt
What failed
Root cause
Files changed
Commands run
Commands now passing
Remaining issues
Recommended next step
```

## Rules

Codex must not:

```txt
Add new features unless asked
Rewrite the architecture
Delete tests to make checks pass
Commit secrets
Add real API keys
Create a real .env file
Ignore type errors without explanation
Make large unrelated refactors
Change public interfaces unless required
```

Codex may:

```txt
Fix lint errors
Fix formatting
Fix type annotations
Fix imports
Fix failing tests
Add missing tests for changed behavior
Improve small error handling
Update docs if they are wrong
Suggest follow-up refactors
```

## Error-fixing priority

Fix in this order:

```txt
1. Syntax/import errors
2. Formatting errors
3. Ruff lint errors
4. Type errors
5. Test failures
6. CI issues
7. Documentation mismatches
```

Reason: syntax/import errors can block all other checks.

## Python-specific rules

Prefer modern, readable Python.

Use:

```txt
type hints
Protocol or ABC for interfaces when useful
dataclasses where appropriate
pathlib instead of raw string paths
explicit exceptions
small functions
clear module boundaries
```

Avoid:

```txt
bare except
mutable defaults
hidden global state
large functions
circular imports
side effects at import time
hardcoded secrets
```

## Testing rules

Tests should be:

```txt
small
deterministic
fast
clear
focused on behavior
```

Do not test implementation details unless necessary.

Do not remove failing tests unless the test is clearly wrong, and explain why.

When fixing a bug, add or update a test if reasonable.

## Architecture rules

Preserve separation between:

```txt
domain
application
infrastructure
services
config
utils
```

Domain code should stay clean and not depend directly on infrastructure.

Infrastructure should implement interfaces/adapters.

Application code should orchestrate.

Avoid coupling config, logging, retry logic, and dependency injection too tightly.

## Config/debugging rules

For configuration code:

```txt
Validate required settings clearly
Avoid loading secrets at import time
Use .env.example for example variables
Never commit real .env
Prefer clear error messages
```

For logging code:

```txt
Use structured, useful logs
Avoid printing secrets
Avoid noisy logs in tests
```

For retry code:

```txt
Retry only expected failures
Respect max attempts
Avoid infinite loops
Make sleep injectable for tests
Test success, retry, and failure paths
```

For dependency injection code:

```txt
Keep construction explicit
Avoid hidden side effects
Keep container easy to test
Do not instantiate external clients unnecessarily in tests
```

## Git workflow

Codex should not commit or push unless the user explicitly asks.

Preferred flow:

```txt
Codex edits files
User reviews in Cursor
User runs git status and git diff
User commits
User pushes
```

Suggested user commands after Codex finishes:

```powershell
git status
git diff
git add .
git commit -m "Fix lint, type, and test issues"
git push
```

## Good Codex prompt template

Use this prompt when asking Codex to debug the repo:

```txt
Read AGENTS.md, CLAUDE.md, README.md, pyproject.toml, .claude/workflow.md, and .codex/debugging.md first.

You are debugging this repository. Do not add new features. Do not rewrite the architecture.

Run:
- ruff check .
- ruff format --check .
- mypy src
- pytest

Fix all real lint, formatting, typing, import, and test errors with the smallest safe changes.

Important:
- Preserve the current architecture.
- Do not delete tests to make them pass.
- Do not add secrets or real .env files.
- Do not make unrelated refactors.
- Do not change public interfaces unless required.
- Add or update tests only when needed to verify behavior.

After fixing, rerun the checks and summarize:
1. what failed,
2. root cause,
3. files changed,
4. commands run,
5. commands now passing,
6. any remaining issues.
```

## Emergency debugging prompt

Use this when the repo is broken and confusing:

```txt
The repo may have broken changes. First, inspect git status and the latest modified files.

Do not make changes yet. Tell me:
1. what files are modified,
2. what seems broken,
3. what checks fail,
4. the smallest safe fix plan.

After I approve the plan, apply the fixes.
```

## Completion checklist

Codex is done only when:

```txt
git status was inspected
ruff check . passes or remaining issues are documented
ruff format --check . passes or formatting was applied
mypy src passes or remaining issues are documented
pytest passes or remaining issues are documented
changes are minimal
no secrets were added
summary is clear
```
