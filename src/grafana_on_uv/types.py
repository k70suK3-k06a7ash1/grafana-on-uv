"""Type definitions."""

from returns.io import IOResult
from returns.result import Result

type GrafanaResult[T] = Result[T, Exception]
type GrafanaIO[T] = IOResult[T, Exception]
type WorkflowResult = list[tuple[str, GrafanaResult]]
