"""``getCompany(ticker)`` — static / slowly-changing context (not financial data).

Best candidate for aggressive caching (long TTL) since this rarely changes.
Profile lives flat on the handle; analyst and credit are nested.
"""

from __future__ import annotations

from .analyst import Analyst
from .credit import Credit
from .profile import Profile


class Company:
    """Handle returned by ``getCompany(ticker)``."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        self._profile = Profile(ticker)
        self.analyst = Analyst(ticker)
        self.credit = Credit(ticker)

    def profile(self) -> dict:
        """Company profile dict: ``ticker``, ``sector``, ``industry``, ``exchange``,
        ``currency``, ``employees``, ``hq``, ``founded_year``, ``website``.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Long-form business description (yfinance / FMP)."""
        raise NotImplementedError


def getCompany(ticker: str) -> Company:
    """Return a ``Company`` handle for ``ticker``."""
    return Company(ticker)


__all__ = ["Analyst", "Company", "Credit", "Profile", "getCompany"]
