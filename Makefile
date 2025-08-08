test:
	uv sync
	uv run pytest

format:
	black .
