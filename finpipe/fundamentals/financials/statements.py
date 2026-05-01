"""Core XBRL-tagged financial statements. Most reliable layer of the fundamentals stack."""

from __future__ import annotations

import pandas as pd


class Statements:
    """Income statement / balance sheet / cash flow."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def incomeStatement(self) -> pd.DataFrame:
        """Consolidated income statement."""
        raise NotImplementedError

    def balanceSheet(self) -> pd.DataFrame:
        """Consolidated balance sheet."""
        raise NotImplementedError

    def cashFlow(self) -> pd.DataFrame:
        """Consolidated cash-flow statement."""
        raise NotImplementedError


__all__ = ["Statements"]
