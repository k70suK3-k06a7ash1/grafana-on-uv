"""Combinators for Result transformation."""

from typing import Callable

from returns.io import IO
from returns.result import Failure, Success

from .types import GrafanaResult


def handle_datasource_exists[T](result: GrafanaResult[T]) -> GrafanaResult[T | dict]:
    """データソース重複エラーをハンドリング."""
    match result:
        case Failure(e) if "already exists" in str(e):
            return Success({"message": "already exists"})
        case _:
            return result


def format_result[T](label: str) -> Callable[[GrafanaResult[T]], str]:
    """結果をフォーマット."""
    def formatter(result: GrafanaResult[T]) -> str:
        match result:
            case Success(value):
                return f"[{label}] Success: {value}"
            case Failure(error):
                return f"[{label}] Failure: {error}"
    return formatter


def log(message: str) -> IO[None]:
    """ログ出力 (IO monad)."""
    return IO(lambda: print(message))
