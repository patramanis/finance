"""Price history and current quote (yfinance)."""

from __future__ import annotations

import pandas as pd


class Price:
    """OHLCV history and latest quote."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def history(self, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """OHLCV over ``period`` at ``interval`` (yfinance conventions)."""
        raise NotImplementedError

    def current(self) -> dict:
        """Latest quote: price, change, bid / ask, day range, timestamp."""
        raise NotImplementedError


__all__ = ["Price"]
