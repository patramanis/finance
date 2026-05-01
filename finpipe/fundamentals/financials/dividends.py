"""Dividend history and payout metrics (yfinance primary)."""

from __future__ import annotations

import pandas as pd


class Dividends:
    """Dividend cash flows and payout ratios."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def history(self) -> pd.DataFrame:
        """Per-share dividend payments with ex-date, record date, pay date."""
        raise NotImplementedError

    def payoutRatio(self) -> pd.DataFrame:
        """Dividends paid / net income, per reporting period."""
        raise NotImplementedError


__all__ = ["Dividends"]
