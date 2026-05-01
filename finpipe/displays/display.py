"""Single display entrypoint for users.

Users call ``display(obj)`` without caring about the concrete type.
Type-specific renderers are used when available; otherwise Rich prints the object.
"""

from __future__ import annotations

from typing import Any

from rich.console import Console

from .edgar import StatementKind, renderStatement

try:
    from edgar.financials import Financials
except Exception:  # pragma: no cover - optional dependency/runtime environment
    Financials = None  # type: ignore[assignment]


def display(
    obj: Any,
    *,
    console: Console | None = None,
    kind: StatementKind = "income",
    headlines: bool = False,
) -> None:
    """Render ``obj`` with one stable API.

    - EdgarTools ``Financials`` objects use ``renderStatement``.
    - Everything else falls back to ``rich.Console.print``.
    """
    c = console or Console()
    if Financials is not None and isinstance(obj, Financials):
        renderStatement(obj, kind=kind, console=c, headlines=headlines)
        return
    c.print(obj)


__all__ = ["display"]

