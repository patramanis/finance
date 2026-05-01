"""Escape hatch — return the underlying ``edgartools`` Filing object."""

from __future__ import annotations

from typing import Any


class Raw:
    """Passthrough for operations not covered by the structured / text layers."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def get(self, form: str) -> Any:
        """Return the raw ``edgartools`` Filing for ``form``."""
        raise NotImplementedError


__all__ = ["Raw"]
