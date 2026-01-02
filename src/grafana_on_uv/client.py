"""Grafana API client factory."""

from grafana_client import GrafanaApi


def create_client(
    url: str = "http://localhost:3000",
    username: str = "admin",
    password: str = "admin",
) -> GrafanaApi:
    """Grafana APIクライアントを作成."""
    return GrafanaApi.from_url(url, credential=(username, password))
