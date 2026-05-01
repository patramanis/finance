"""Market risk observables: beta, realized volatility."""

from __future__ import annotations


class Risk:
    """Beta (provider-supplied) and locally-computed realized vol."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def beta(self) -> float:
        """Equity beta as published by yfinance."""
        raise NotImplementedError

    def realizedVol(self, window: int = 30) -> float:
        """Annualized realized volatility over the last ``window`` trading days."""
        raise NotImplementedError


__all__ = ["Risk"]
