"""``getDerived(ticker)`` — computed-only metrics. Nothing is fetched from a provider.

Pulls already-fetched data from ``getFinancials`` / ``getMarketData`` / ``macro``
and computes locally. Computation order matters:

    price + shares          → marketCap
    statements              → netDebt → investedCapital
    beta + riskFree         → wacc
    investedCapital + wacc  → roic → eva
    marketCap + netDebt     → enterpriseValue → evEbitda
"""

from __future__ import annotations

import pandas as pd

from .costOfCapital import CostOfCapital
from .debt import Debt
from .returns import Returns
from .valuation import ValuationDerived


class Derived:
    """Handle returned by ``getDerived(ticker)``. Methods flat for ergonomics."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        self._debt = Debt(ticker)
        self._valuation = ValuationDerived(ticker)
        self._returns = Returns(ticker)
        self._costOfCapital = CostOfCapital(ticker)

    def netDebt(self) -> pd.DataFrame:
        """Debt minus cash and equivalents, per reporting period."""
        raise NotImplementedError

    def investedCapital(self) -> pd.DataFrame:
        """Debt + equity - cash, per reporting period."""
        raise NotImplementedError

    def enterpriseValue(self) -> pd.DataFrame:
        """Market cap + net debt + minority interest - cash."""
        raise NotImplementedError

    def evEbitda(self) -> pd.DataFrame:
        """Enterprise value divided by trailing EBITDA."""
        raise NotImplementedError

    def roic(self) -> pd.DataFrame:
        """NOPAT / invested capital, per reporting period."""
        raise NotImplementedError

    def eva(self) -> pd.DataFrame:
        """Economic value added: (ROIC - WACC) * invested capital."""
        raise NotImplementedError

    def wacc(self) -> float:
        """Weighted average cost of capital (current snapshot)."""
        raise NotImplementedError


def getDerived(ticker: str) -> Derived:
    """Return a ``Derived`` handle for ``ticker``."""
    return Derived(ticker)


__all__ = [
    "CostOfCapital",
    "Debt",
    "Derived",
    "Returns",
    "ValuationDerived",
    "getDerived",
]
