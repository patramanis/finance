"""Persist a filing to disk in a chosen format."""

from __future__ import annotations


class Download:
    """Download filings as PDF / HTML / TXT."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def download(self, form: str, format: str = "pdf") -> str:
        """Save a filing. ``format`` ∈ {pdf, html, txt}. Returns the path written."""
        raise NotImplementedError


__all__ = ["Download"]
