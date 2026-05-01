"""Debt-side derived metrics. Depends on the balance sheet."""

from __future__ import annotations

import pandas as pd


class Debt:
    """Net debt and invested capital."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def netDebt(self) -> pd.DataFrame:
        """Total debt - cash and equivalents."""
        raise NotImplementedError

    def investedCapital(self) -> pd.DataFrame:
        """Total debt + equity - cash."""
        raise NotImplementedError


__all__ = ["Debt"]
