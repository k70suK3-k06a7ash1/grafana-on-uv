# grafana-on-uv

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- Docker

## Setup

```bash
uv sync
```

## Start Grafana

```bash
docker compose up -d
```

Grafana: http://localhost:3000 (admin/admin)

## Usage

```bash
uv run main.py
```

## Make Commands

```bash
make setup  # Install dependencies
make up     # Start Grafana
make down   # Stop Grafana
make logs   # View Grafana logs
make run    # Run main.py
```

## Development

```bash
# Add a package
uv add <package-name>

# Remove a package
uv remove <package-name>
```
