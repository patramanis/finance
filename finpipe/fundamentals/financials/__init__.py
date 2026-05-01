"""``getFinancials(ticker)`` — company-reported financial data.

Sources: SEC EDGAR, SimFin, FMP (free tier), yfinance.
Granularity: quarterly or annual, driven by the underlying filing (10-K / 10-Q).

The returned ``Financials`` object flattens the three core statement methods
(``incomeStatement``, ``balanceSheet``, ``cashFlow``) onto itself, and exposes the
other areas as attributes so calls read naturally:

    getFinancials("AAPL").incomeStatement()
    getFinancials("AAPL").ratios.roe()
    getFinancials("AAPL").valuation.pe()
    getFinancials("AAPL").ownership.insiderTrades()
"""

from __future__ import annotations

import pandas as pd

from .corporateActions import CorporateActions
from .dividends import Dividends
from .earnings import Earnings
from .ownership import Ownership
from .ratios import Ratios
from .segments import Segments
from .statements import Statements
from .valuation import Valuation


class Financials:
    """Handle returned by ``getFinancials(ticker)``.

    Flattened statement methods + nested submodule handles.
    """

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        self._statements = Statements(ticker)
        self.ratios = Ratios(ticker)
        self.valuation = Valuation(ticker)
        self.earnings = Earnings(ticker)
        self.dividends = Dividends(ticker)
        self.segments = Segments(ticker)
        self.ownership = Ownership(ticker)
        self.corporateActions = CorporateActions(ticker)

    def incomeStatement(self) -> pd.DataFrame:
        """Consolidated income statement."""
        raise NotImplementedError

    def balanceSheet(self) -> pd.DataFrame:
        """Consolidated balance sheet."""
        raise NotImplementedError

    def cashFlow(self) -> pd.DataFrame:
        """Consolidated cash-flow statement."""
        raise NotImplementedError


def getFinancials(ticker: str) -> Financials:
    """Return a ``Financials`` handle for ``ticker``."""
    return Financials(ticker)


__all__ = [
    "CorporateActions",
    "Dividends",
    "Earnings",
    "Financials",
    "Ownership",
    "Ratios",
    "Segments",
    "Statements",
    "Valuation",
    "getFinancials",
]
