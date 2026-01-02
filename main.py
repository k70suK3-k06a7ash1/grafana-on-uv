"""Entry point."""

import sys

from returns.io import IO, IOFailure, IOSuccess, impure_safe

from src.grafana_on_uv.client import create_client
from src.grafana_on_uv.combinators import format_result
from src.grafana_on_uv.data import DASHBOARD_PRESETS
from src.grafana_on_uv.types import GrafanaResult
from src.grafana_on_uv.workflows import full_workflow

PRESETS = list(DASHBOARD_PRESETS.keys())


@impure_safe
def run_workflows(preset: str) -> list[tuple[str, GrafanaResult]]:
    """ワークフローを実行 (副作用をIOでラップ)."""
    client = create_client()
    return full_workflow(client, dashboard_preset=preset)


def print_results(results: list[tuple[str, GrafanaResult]]) -> IO[None]:
    """結果を出力."""
    def _print() -> None:
        print("=== Grafana Client (Monadic) ===\n")
        for label, result in results:
            print(format_result(label)(result))
        print("\n=== Done ===")
    return IO(_print)


def print_usage() -> None:
    """使用方法を出力."""
    print("Usage: main.py [preset]")
    print(f"\nPresets: {', '.join(PRESETS)}")


def main() -> None:
    """エントリーポイント."""
    preset = sys.argv[1] if len(sys.argv) > 1 else "simple"

    if preset not in PRESETS:
        print(f"Error: Unknown preset '{preset}'")
        print_usage()
        sys.exit(1)

    match run_workflows(preset):
        case IOSuccess(results):
            print_results(results)._inner_value()
        case IOFailure(error):
            print(f"Fatal Error: {error}")


if __name__ == "__main__":
    main()
