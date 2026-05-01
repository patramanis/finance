"""Credit ratings and outlook (FMP — patchy on the free tier)."""

from __future__ import annotations

import pandas as pd


class Credit:
    """Agency ratings and outlook."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def ratings(self) -> pd.DataFrame:
        """Current and historical credit ratings per agency."""
        raise NotImplementedError

    def outlook(self) -> dict:
        """Most recent outlook per agency (stable / positive / negative / watch)."""
        raise NotImplementedError


__all__ = ["Credit"]
