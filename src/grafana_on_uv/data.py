"""Sample data definitions."""


def sample_datasource() -> dict:
    """サンプルデータソース定義."""
    return {
        "name": "TestData",
        "type": "testdata",
        "access": "proxy",
        "isDefault": True,
    }


def sample_dashboard() -> dict:
    """サンプルダッシュボード定義."""
    return {
        "dashboard": {
            "title": "Sample Dashboard",
            "tags": ["sample"],
            "timezone": "browser",
            "panels": [
                {
                    "id": 1,
                    "title": "Random Walk",
                    "type": "timeseries",
                    "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8},
                    "datasource": {"type": "testdata", "uid": "testdata"},
                    "targets": [{"refId": "A", "scenarioId": "random_walk"}],
                }
            ],
            "schemaVersion": 38,
        },
        "overwrite": True,
    }
