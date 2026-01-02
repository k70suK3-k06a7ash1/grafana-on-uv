"""Workflow definitions."""

from grafana_client import GrafanaApi
from returns.pipeline import flow

from .combinators import handle_datasource_exists
from .data import sample_dashboard, sample_datasource
from .operations import (
    create_dashboard,
    create_datasource,
    get_health,
    list_dashboards,
    list_datasources,
)
from .types import GrafanaResult


def health_check_workflow(client: GrafanaApi) -> GrafanaResult[dict]:
    """ヘルスチェックワークフロー."""
    return get_health(client)


def datasource_workflow(client: GrafanaApi) -> GrafanaResult[dict]:
    """データソースワークフロー: 作成."""
    return flow(
        create_datasource(client, sample_datasource()),
        handle_datasource_exists,
    )


def dashboard_workflow(client: GrafanaApi) -> GrafanaResult[dict]:
    """ダッシュボードワークフロー: 作成."""
    return create_dashboard(client, sample_dashboard())


def full_workflow(client: GrafanaApi) -> list[tuple[str, GrafanaResult]]:
    """全ワークフローを実行."""
    return [
        ("Health Check", health_check_workflow(client)),
        ("DataSources", list_datasources(client)),
        ("Create DataSource", datasource_workflow(client)),
        ("Dashboards", list_dashboards(client)),
        ("Create Dashboard", dashboard_workflow(client)),
    ]
