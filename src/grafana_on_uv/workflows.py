"""Workflow definitions."""

from typing import Callable

from grafana_client import GrafanaApi
from returns.pipeline import flow

from .combinators import handle_datasource_exists
from .data import DASHBOARD_PRESETS, DATASOURCE_PRESETS
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


def datasource_workflow(
    client: GrafanaApi,
    datasource_fn: Callable[[], dict] = DATASOURCE_PRESETS["testdata"],
) -> GrafanaResult[dict]:
    """データソースワークフロー: 作成."""
    return flow(
        create_datasource(client, datasource_fn()),
        handle_datasource_exists,
    )


def dashboard_workflow(
    client: GrafanaApi,
    dashboard_fn: Callable[[], dict] = DASHBOARD_PRESETS["simple"],
) -> GrafanaResult[dict]:
    """ダッシュボードワークフロー: 作成."""
    return create_dashboard(client, dashboard_fn())


def full_workflow(
    client: GrafanaApi,
    dashboard_preset: str = "simple",
) -> list[tuple[str, GrafanaResult]]:
    """全ワークフローを実行."""
    dashboard_fn = DASHBOARD_PRESETS.get(dashboard_preset, DASHBOARD_PRESETS["simple"])

    return [
        ("Health Check", health_check_workflow(client)),
        ("DataSources", list_datasources(client)),
        ("Create DataSource", datasource_workflow(client)),
        ("Dashboards", list_dashboards(client)),
        (f"Create Dashboard ({dashboard_preset})", dashboard_workflow(client, dashboard_fn)),
    ]
