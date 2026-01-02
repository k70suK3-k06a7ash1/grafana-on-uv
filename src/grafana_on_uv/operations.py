"""Grafana API operations (pure functions with Result monad)."""

from grafana_client import GrafanaApi
from returns.result import safe


@safe
def get_health(client: GrafanaApi) -> dict:
    """Grafanaのヘルスチェック."""
    return client.health.check()


@safe
def list_datasources(client: GrafanaApi) -> list:
    """データソース一覧を取得."""
    return client.datasource.list_datasources()


@safe
def create_datasource(client: GrafanaApi, datasource: dict) -> dict:
    """データソースを作成."""
    return client.datasource.create_datasource(datasource)


@safe
def list_dashboards(client: GrafanaApi) -> list:
    """ダッシュボード一覧を取得."""
    return client.search.search_dashboards()


@safe
def create_dashboard(client: GrafanaApi, dashboard: dict) -> dict:
    """ダッシュボードを作成."""
    return client.dashboard.update_dashboard(dashboard)
