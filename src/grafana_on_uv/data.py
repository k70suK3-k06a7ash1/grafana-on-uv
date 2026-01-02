"""Sample data definitions."""

from dataclasses import asdict, dataclass
from enum import Enum


# =============================================================================
# Enums
# =============================================================================


class ScenarioId(Enum):
    """TestData シナリオ."""

    RANDOM_WALK = "random_walk"
    PREDICTABLE_PULSE = "predictable_pulse"
    CSV_CONTENT = "csv_content"
    LOGS = "logs"
    STREAMING_CLIENT = "streaming_client"


class PanelType(Enum):
    """パネルタイプ."""

    TIMESERIES = "timeseries"
    STAT = "stat"
    GAUGE = "gauge"
    TABLE = "table"
    LOGS = "logs"
    BARCHART = "barchart"
    PIECHART = "piechart"


# =============================================================================
# Panel Builders
# =============================================================================


@dataclass(frozen=True)
class GridPos:
    """パネル位置 (イミュータブル)."""

    x: int
    y: int
    w: int
    h: int


def panel(
    panel_id: int,
    title: str,
    panel_type: PanelType,
    grid_pos: GridPos,
    scenario_id: ScenarioId = ScenarioId.RANDOM_WALK,
) -> dict:
    """パネルを生成."""
    return {
        "id": panel_id,
        "title": title,
        "type": panel_type.value,
        "gridPos": asdict(grid_pos),
        "datasource": {"type": "testdata", "uid": "testdata"},
        "targets": [{"refId": "A", "scenarioId": scenario_id.value}],
    }


# =============================================================================
# DataSources
# =============================================================================


def testdata_datasource() -> dict:
    """TestData データソース."""
    return {
        "name": "TestData",
        "type": "testdata",
        "access": "proxy",
        "isDefault": True,
    }


def prometheus_datasource(url: str = "http://prometheus:9090") -> dict:
    """Prometheus データソース."""
    return {
        "name": "Prometheus",
        "type": "prometheus",
        "access": "proxy",
        "url": url,
        "isDefault": False,
    }


def loki_datasource(url: str = "http://loki:3100") -> dict:
    """Loki データソース."""
    return {
        "name": "Loki",
        "type": "loki",
        "access": "proxy",
        "url": url,
        "isDefault": False,
    }


# =============================================================================
# Dashboards
# =============================================================================


def dashboard(
    title: str,
    panels: list[dict],
    tags: list[str] | None = None,
    overwrite: bool = True,
) -> dict:
    """ダッシュボードを生成."""
    return {
        "dashboard": {
            "title": title,
            "tags": tags or [],
            "timezone": "browser",
            "panels": panels,
            "schemaVersion": 38,
        },
        "overwrite": overwrite,
    }


def simple_dashboard() -> dict:
    """シンプルなダッシュボード (1パネル)."""
    return dashboard(
        title="Simple Dashboard",
        tags=["simple"],
        panels=[
            panel(1, "Random Walk", PanelType.TIMESERIES, GridPos(0, 0, 24, 8)),
        ],
    )


def metrics_dashboard() -> dict:
    """メトリクスダッシュボード (複数パネル)."""
    return dashboard(
        title="Metrics Dashboard",
        tags=["metrics", "monitoring"],
        panels=[
            panel(1, "Time Series", PanelType.TIMESERIES, GridPos(0, 0, 12, 8)),
            panel(2, "Current Value", PanelType.STAT, GridPos(12, 0, 6, 4)),
            panel(3, "Gauge", PanelType.GAUGE, GridPos(18, 0, 6, 4)),
            panel(4, "Bar Chart", PanelType.BARCHART, GridPos(12, 4, 12, 4)),
        ],
    )


def logs_dashboard() -> dict:
    """ログダッシュボード."""
    return dashboard(
        title="Logs Dashboard",
        tags=["logs"],
        panels=[
            panel(
                1, "Log Stream", PanelType.LOGS, GridPos(0, 0, 24, 12),
                scenario_id=ScenarioId.LOGS,
            ),
        ],
    )


def overview_dashboard() -> dict:
    """オーバービューダッシュボード (6パネル)."""
    return dashboard(
        title="Overview Dashboard",
        tags=["overview", "sample"],
        panels=[
            # Row 1
            panel(1, "Requests/sec", PanelType.STAT, GridPos(0, 0, 6, 4)),
            panel(2, "Error Rate", PanelType.GAUGE, GridPos(6, 0, 6, 4)),
            panel(3, "Latency P99", PanelType.STAT, GridPos(12, 0, 6, 4)),
            panel(4, "Uptime", PanelType.STAT, GridPos(18, 0, 6, 4)),
            # Row 2
            panel(5, "Traffic", PanelType.TIMESERIES, GridPos(0, 4, 12, 8)),
            panel(6, "Distribution", PanelType.PIECHART, GridPos(12, 4, 12, 8)),
        ],
    )


# =============================================================================
# Presets
# =============================================================================


DATASOURCE_PRESETS = {
    "testdata": testdata_datasource,
    "prometheus": lambda: prometheus_datasource(),
    "loki": lambda: loki_datasource(),
}

DASHBOARD_PRESETS = {
    "simple": simple_dashboard,
    "metrics": metrics_dashboard,
    "logs": logs_dashboard,
    "overview": overview_dashboard,
}
