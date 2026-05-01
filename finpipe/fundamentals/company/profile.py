"""Company profile — sector, industry, HQ, website, etc."""

from __future__ import annotations


class Profile:
    """Sector / industry / HQ / headcount / website (yfinance / FMP)."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def profile(self) -> dict:
        """Profile dict: ``ticker``, ``sector``, ``industry``, ``exchange``,
        ``currency``, ``employees``, ``hq``, ``founded_year``, ``website``.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Long-form business description."""
        raise NotImplementedError


__all__ = ["Profile"]
