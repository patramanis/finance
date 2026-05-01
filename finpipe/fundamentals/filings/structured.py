"""Structured (XBRL-tagged) extraction from filings."""

from __future__ import annotations

import pandas as pd


class Structured:
    """Financial statements + named footnote tables from a filing."""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def statements(self, form: str) -> pd.DataFrame:
        """Income / balance / cash-flow tables extracted from a ``form`` filing."""
        raise NotImplementedError

    def notes(self, form: str, note: str) -> pd.DataFrame:
        """Named footnote table. ``note`` ∈ {leases, goodwill, taxes, debt, stock_based_comp, eps}."""
        raise NotImplementedError


__all__ = ["Structured"]
