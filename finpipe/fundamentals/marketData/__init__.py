"""``getMarketData(ticker)`` — market-observable data (not company-reported).

Source: yfinance primary, FINRA for short interest.

Distinction from ``getFinancials``: this is what the **market observes**, not what
the company **reports**. Never mix these two sources inside one module.
"""

from __future__ import annotations

from .price import Price
from .risk import Risk
from .shares import Shares


class MarketData:
    """Handle returned by ``getMarketData(ticker)``."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        self.price = Price(ticker)
        self.shares = Shares(ticker)
        self.risk = Risk(ticker)


def getMarketData(ticker: str) -> MarketData:
    """Return a ``MarketData`` handle for ``ticker``."""
    return MarketData(ticker)


__all__ = ["MarketData", "Price", "Risk", "Shares", "getMarketData"]
