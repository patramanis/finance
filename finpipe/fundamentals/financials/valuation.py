"""Valuation multiples that combine live price with filing data."""

from __future__ import annotations

import pandas as pd


class Valuation:
    """Price-driven multiples (P/E, P/B, P/S)."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def pe(self) -> pd.DataFrame:
        """Price to earnings."""
        raise NotImplementedError

    def pb(self) -> pd.DataFrame:
        """Price to book."""
        raise NotImplementedError

    def ps(self) -> pd.DataFrame:
        """Price to sales."""
        raise NotImplementedError


__all__ = ["Valuation"]
