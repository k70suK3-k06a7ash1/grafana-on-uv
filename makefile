.PHONY: help setup up down restart logs ps run clean open
.PHONY: run-simple run-metrics run-logs run-overview run-all

# Default
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Setup:"
	@echo "  setup        Install dependencies"
	@echo ""
	@echo "Docker:"
	@echo "  up           Start Grafana"
	@echo "  down         Stop Grafana"
	@echo "  restart      Restart Grafana"
	@echo "  logs         View Grafana logs"
	@echo "  ps           Show container status"
	@echo ""
	@echo "App:"
	@echo "  run          Run with default preset (simple)"
	@echo "  run-simple   Create simple dashboard"
	@echo "  run-metrics  Create metrics dashboard"
	@echo "  run-logs     Create logs dashboard"
	@echo "  run-overview Create overview dashboard"
	@echo "  run-all      Create all dashboards"
	@echo "  open         Open Grafana in browser"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean        Remove volumes and cache"

# Setup
setup:
	uv sync

# Docker
up:
	docker compose up -d

down:
	docker compose down

restart: down up

logs:
	docker compose logs -f

ps:
	docker compose ps

# App
run:
	uv run main.py

run-simple:
	uv run main.py simple

run-metrics:
	uv run main.py metrics

run-logs:
	uv run main.py logs

run-overview:
	uv run main.py overview

run-all: run-simple run-metrics run-logs run-overview

open:
	open http://localhost:3000

# Cleanup
clean:
	docker compose down -v
	rm -rf .venv __pycache__ src/**/__pycache__ src/**/*.egg-info
