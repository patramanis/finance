"""Earnings actuals, guidance, and calendar."""

from __future__ import annotations

import pandas as pd


class Earnings:
    """EPS actuals, surprises, guidance, and next-report date."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def actual(self) -> pd.DataFrame:
        """Historical actuals + consensus estimates + surprise."""
        raise NotImplementedError

    def guidance(self) -> pd.DataFrame:
        """Company-issued forward guidance (where disclosed)."""
        raise NotImplementedError

    def nextDate(self) -> dict:
        """Next scheduled earnings date and (if known) time-of-day."""
        raise NotImplementedError


__all__ = ["Earnings"]
