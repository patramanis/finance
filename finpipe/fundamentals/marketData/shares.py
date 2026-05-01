"""Share counts and short interest."""

from __future__ import annotations

import pandas as pd


class Shares:
    """Shares outstanding and short interest (FINRA / yfinance)."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def outstanding(self) -> pd.DataFrame:
        """Total shares outstanding over time."""
        raise NotImplementedError

    def shortInterest(self) -> pd.DataFrame:
        """Short interest, days-to-cover, and % of float."""
        raise NotImplementedError


__all__ = ["Shares"]
