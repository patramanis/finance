"""Unstructured text extraction from named filing sections."""

from __future__ import annotations


class Text:
    """Raw-text sections from filings.

    By design always returns ``str`` — sections are prose, not tables.
    """

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def section(self, form: str, part: str) -> str:
        """Raw text of a named section.

        ``part`` ∈ {mda, risk_factors, business, legal_proceedings,
        cybersecurity, exec_comp, properties}.
        """
        raise NotImplementedError


__all__ = ["Text"]
