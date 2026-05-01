"""Insider and institutional ownership.

Sources Form 4 (insider) and 13F (institutional) via EDGAR — **not** 10-K.
"""

from __future__ import annotations

import pandas as pd


class Ownership:
    """Insider trades and institutional holdings."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def insiderTrades(self) -> pd.DataFrame:
        """Form 4 insider transactions (buys, sells, grants)."""
        raise NotImplementedError

    def institutional(self) -> pd.DataFrame:
        """13F institutional holdings snapshot."""
        raise NotImplementedError


__all__ = ["Ownership"]
