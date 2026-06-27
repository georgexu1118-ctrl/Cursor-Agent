.PHONY: install lint format typecheck test check

install:
	pip install -e ".[dev]"

lint:
	ruff check .

format:
	ruff format .
	black .

format-check:
	ruff format --check .
	black --check .

typecheck:
	mypy src/

test:
	pytest

check: lint format-check typecheck test
