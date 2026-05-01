"""Financial ratios. Fetched from FMP where available, otherwise computed from statements."""

from __future__ import annotations

import pandas as pd


class Ratios:
    """Profitability / efficiency ratios."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def roe(self) -> pd.DataFrame:
        """Return on equity, per reporting period."""
        raise NotImplementedError

    def roa(self) -> pd.DataFrame:
        """Return on assets, per reporting period."""
        raise NotImplementedError

    def margins(self) -> pd.DataFrame:
        """Gross / operating / net margins, per reporting period."""
        raise NotImplementedError

    def all(self) -> pd.DataFrame:
        """Union of every ratio this provider exposes."""
        raise NotImplementedError


__all__ = ["Ratios"]
