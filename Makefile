.PHONY: install test lint format typecheck check

install:
	uv sync --all-extras

test:
	uv run pytest --cov=path_seeker

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy src

check: lint typecheck test
