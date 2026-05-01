"""Segment- and geography-level breakdowns (XBRL via EDGAR / FMP).

Not every company reports segment data; expect ``None`` / empty for many tickers.
"""

from __future__ import annotations

import pandas as pd


class Segments:
    """Revenue / profit split by reported segment or geography."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def bySegment(self) -> pd.DataFrame:
        """Revenue and operating income by reportable business segment."""
        raise NotImplementedError

    def byGeography(self) -> pd.DataFrame:
        """Revenue by geographic region, as disclosed."""
        raise NotImplementedError


__all__ = ["Segments"]
