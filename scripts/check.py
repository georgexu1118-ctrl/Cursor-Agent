#!/usr/bin/env python3
"""Run local quality checks matching the CI pipeline."""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Sequence


def run_command(command: Sequence[str]) -> int:
    """Run a shell command and return its exit code."""
    print(f"\n>>> {' '.join(command)}")
    result = subprocess.run(list(command), check=False)
    return result.returncode


def main() -> int:
    """Execute lint, format, type, and test checks in CI order."""
    checks: list[list[str]] = [
        [sys.executable, "-m", "ruff", "check", "."],
        [sys.executable, "-m", "ruff", "format", "--check", "."],
        [sys.executable, "-m", "black", "--check", "."],
        [sys.executable, "-m", "mypy", "src/"],
        [sys.executable, "-m", "pytest"],
    ]

    for command in checks:
        exit_code = run_command(command)
        if exit_code != 0:
            return exit_code

    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
