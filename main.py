"""Entry point."""

from returns.io import IO, IOFailure, IOSuccess, impure_safe

from src.grafana_on_uv.client import create_client
from src.grafana_on_uv.combinators import format_result
from src.grafana_on_uv.types import GrafanaResult
from src.grafana_on_uv.workflows import full_workflow


@impure_safe
def run_workflows() -> list[tuple[str, GrafanaResult]]:
    """ワークフローを実行 (副作用をIOでラップ)."""
    client = create_client()
    return full_workflow(client)


def print_results(results: list[tuple[str, GrafanaResult]]) -> IO[None]:
    """結果を出力."""
    def _print() -> None:
        print("=== Grafana Client (Monadic) ===\n")
        for label, result in results:
            print(format_result(label)(result))
        print("\n=== Done ===")
    return IO(_print)


def main() -> None:
    """エントリーポイント."""
    match run_workflows():
        case IOSuccess(results):
            print_results(results)._inner_value()
        case IOFailure(error):
            print(f"Fatal Error: {error}")


if __name__ == "__main__":
    main()
