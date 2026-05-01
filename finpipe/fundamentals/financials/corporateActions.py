"""Corporate actions: splits, buybacks, M&A (yfinance / FMP)."""

from __future__ import annotations

import pandas as pd


class CorporateActions:
    """Stock splits, share repurchases, and M&A events."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def splits(self) -> pd.DataFrame:
        """Historical stock splits with effective date and ratio."""
        raise NotImplementedError

    def buybacks(self) -> pd.DataFrame:
        """Share repurchase activity by period."""
        raise NotImplementedError

    def mergers(self) -> pd.DataFrame:
        """M&A events (acquirer / target / date / consideration)."""
        raise NotImplementedError


__all__ = ["CorporateActions"]
