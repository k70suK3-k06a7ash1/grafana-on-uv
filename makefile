.PHONY: setup up down logs run

setup:
	uv sync

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

run:
	uv run main.py
