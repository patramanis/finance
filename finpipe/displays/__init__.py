"""Display helpers — Rich renderers. Pure (no network)."""

from .display import display
from .edgar import StatementKind, renderStatement

__all__ = [
    "display",
    "StatementKind",
    "renderStatement",
]
