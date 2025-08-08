build:
	docker build -t ingestion .

local-docker-run:
	docker run ingestion

run:
	uv sync
	uv run main.py
