"""EdgarTools adapter — SEC EDGAR financials and filings.

Thin wrapper: no Rich, no fallback logic. Errors are translated into
``finpipe.core.exceptions`` so the fallback engine can reason about them.
"""

from __future__ import annotations

from typing import Any, Optional

from edgar import Company
from edgar.financials import Financials

from finpipe.core import utils
from finpipe.core.exceptions import AuthError, NotFound, TransientError

PROVIDER_NAME = "sec_edgar"


def _company(ticker: str) -> Company:
    utils.ensureSecIdentity()
    try:
        return Company(ticker)
    except (KeyError, ValueError, LookupError) as e:
        raise NotFound(PROVIDER_NAME, f"ticker {ticker!r} not found on SEC EDGAR") from e
    except Exception as e:
        msg = repr(e).lower()
        if "identity" in msg or "user-agent" in msg or "user agent" in msg:
            raise AuthError(
                PROVIDER_NAME,
                "SEC requires an identity; set SEC_IDENTITY env var or call edgar.set_identity()",
            ) from e
        raise TransientError(PROVIDER_NAME, f"company lookup failed: {e!r}") from e


def getCompany(ticker: str) -> Company:
    """Return an EdgarTools ``Company`` for ``ticker`` (CIK also works where supported)."""
    return _company(ticker)


def getFinancials(ticker: str) -> Optional[Financials]:
    """Latest annual financials (10-K / 20-F / 40-F). ``None`` means "no data, try next provider"."""
    company = _company(ticker)
    try:
        financials = company.get_financials()
    except Exception as e:
        raise TransientError(PROVIDER_NAME, f"get_financials failed: {e!r}") from e
    return financials


def getQuarterlyFinancials(ticker: str) -> Optional[Financials]:
    """Latest quarterly financials (10-Q / 6-K). ``None`` means "no data, try next provider"."""
    company = _company(ticker)
    try:
        return company.get_quarterly_financials()
    except Exception as e:
        raise TransientError(PROVIDER_NAME, f"get_quarterly_financials failed: {e!r}") from e


def getFilings(ticker: str, *, form: Optional[str] = None, **kwargs: Any) -> Any:
    """Company filings iterator/list; pass ``form`` to filter (e.g. ``"10-K"``, ``"4"``)."""
    company = _company(ticker)
    try:
        if form is not None:
            return company.get_filings(form=form, **kwargs)
        return company.get_filings(**kwargs)
    except Exception as e:
        raise TransientError(PROVIDER_NAME, f"get_filings failed: {e!r}") from e


__all__ = [
    "PROVIDER_NAME",
    "getCompany",
    "getFilings",
    "getFinancials",
    "getQuarterlyFinancials",
]
