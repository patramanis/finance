"""Return-on-capital derived metrics. Depends on investedCapital + wacc + income."""

from __future__ import annotations

import pandas as pd


class Returns:
    """ROIC and EVA."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def roic(self) -> pd.DataFrame:
        """NOPAT / invested capital."""
        raise NotImplementedError

    def eva(self) -> pd.DataFrame:
        """(ROIC - WACC) * invested capital."""
        raise NotImplementedError


__all__ = ["Returns"]
