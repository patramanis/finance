"""Filing discovery: metadata, latest, search."""

from __future__ import annotations


class Metadata:
    """Company + filing metadata, not the filing content."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def metadata(self) -> dict:
        """Top-level company metadata (CIK, SIC, name, addresses)."""
        raise NotImplementedError

    def latest(self, form: str) -> dict:
        """Most recent filing of ``form`` for this ticker."""
        raise NotImplementedError

    def search(self, form: str, date_range: tuple[str, str] | None = None) -> list[dict]:
        """List filings of ``form``, optionally restricted to ``(start, end)``."""
        raise NotImplementedError


__all__ = ["Metadata"]
