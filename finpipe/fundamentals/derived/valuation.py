"""Valuation derived from market cap + balance sheet."""

from __future__ import annotations

import pandas as pd


class ValuationDerived:
    """Enterprise value and EV / EBITDA."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def enterpriseValue(self) -> pd.DataFrame:
        """Market cap + net debt + minority interest - cash."""
        raise NotImplementedError

    def evEbitda(self) -> pd.DataFrame:
        """Enterprise value / trailing EBITDA."""
        raise NotImplementedError


__all__ = ["ValuationDerived"]
