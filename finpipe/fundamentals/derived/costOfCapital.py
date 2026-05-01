"""Cost of capital. Depends on beta + risk-free rate (macro) + capital structure + tax rate."""

from __future__ import annotations


class CostOfCapital:
    """Weighted average cost of capital."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def wacc(self) -> float:
        """Current WACC as a decimal (e.g. 0.087 = 8.7%)."""
        raise NotImplementedError


__all__ = ["CostOfCapital"]
