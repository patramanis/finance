"""Fundamentals — five grouping functions, each returning an object with methods.

Public API:

- ``getFinancials(ticker)``  — what the company **reports** (statements, ratios, earnings, …)
- ``getMarketData(ticker)``  — what the market **observes** (price, shares, risk)
- ``getFiling(ticker)``      — raw access over SEC EDGAR (all form types)
- ``getDerived(ticker)``     — computed-only (EV, WACC, ROIC, …); no fetching
- ``getCompany(ticker)``     — static / slowly-changing context (profile, analyst, credit)

All methods return ``pd.DataFrame`` or ``dict``; provider-specific objects never surface.
Provider complexity, fallback, and rate limiting are handled by ``finpipe.core``.
"""

from __future__ import annotations

from .company import getCompany
from .derived import getDerived
from .filings import getFiling
from .financials import getFinancials
from .marketData import getMarketData

__all__ = [
    "getCompany",
    "getDerived",
    "getFiling",
    "getFinancials",
    "getMarketData",
]
