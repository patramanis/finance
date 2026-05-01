"""Analyst estimates and price targets (FMP free tier / yfinance)."""

from __future__ import annotations

import pandas as pd


class Analyst:
    """Consensus estimates and price targets."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def estimates(self) -> pd.DataFrame:
        """Consensus EPS / revenue estimates by forward period."""
        raise NotImplementedError

    def priceTarget(self) -> dict:
        """Current consensus price target (mean / median / high / low / n_analysts)."""
        raise NotImplementedError


__all__ = ["Analyst"]
