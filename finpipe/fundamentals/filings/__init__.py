"""``getFiling(ticker)`` — raw access over SEC EDGAR via ``edgartools``.

Covers every form SEC accepts (10-K, 10-Q, 8-K, Form 4, 13F, DEF 14A, S-1,
13D / 13G, …). Returns structured DataFrames where XBRL-tagged, raw text
elsewhere.

Limitations:

- Pre-1996 filings are scanned images — no parsing possible.
- Exhibits inside filings are reachable but messy.
- Data not disclosed by the company does not exist.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from .download import Download
from .metadata import Metadata
from .raw import Raw
from .structured import Structured
from .text import Text


class Filing:
    """Handle returned by ``getFiling(ticker)``. All methods are flat for ergonomics."""

    def __init__(self, ticker: str, form: str | None = None) -> None:
        self.ticker = ticker
        self.form = form
        self._metadata = Metadata(ticker)
        self._structured = Structured(ticker)
        self._text = Text(ticker)
        self._raw = Raw(ticker)
        self._download = Download(ticker)

    def metadata(self) -> dict:
        """Top-level company metadata (CIK, SIC, name, addresses)."""
        raise NotImplementedError

    def latest(self, form: str) -> dict:
        """Most recent filing of ``form`` for this ticker."""
        raise NotImplementedError

    def search(self, form: str, date_range: tuple[str, str] | None = None) -> list[dict]:
        """List filings of ``form``, optionally restricted to ``date_range = (start, end)``."""
        raise NotImplementedError

    def statements(self, form: str) -> pd.DataFrame:
        """XBRL financial statements extracted from a ``form`` filing."""
        raise NotImplementedError

    def notes(self, form: str, note: str) -> pd.DataFrame:
        """Named footnote table from a ``form`` filing.

        Valid ``note`` values: ``leases``, ``goodwill``, ``taxes``, ``debt``,
        ``stock_based_comp``, ``eps``.
        """
        raise NotImplementedError

    def section(self, form: str, part: str) -> str:
        """Raw text of a named section (unstructured).

        Valid ``part`` values: ``mda``, ``risk_factors``, ``business``,
        ``legal_proceedings``, ``cybersecurity``, ``exec_comp``, ``properties``.
        """
        raise NotImplementedError

    def get(self, form: str) -> Any:
        """Return the underlying ``edgartools`` Filing object for ``form``.

        Escape hatch for operations not covered by the other methods.
        """
        raise NotImplementedError

    def download(self, form: str, format: str = "pdf") -> str:
        """Download the ``form`` filing to disk in ``format`` (``pdf``, ``html``, ``txt``).

        Returns the path written.
        """
        raise NotImplementedError


def getFiling(ticker: str, form: str | None = None) -> Filing:
    """Return a ``Filing`` handle for ``ticker`` (optionally scoped to ``form``)."""
    return Filing(ticker, form=form)


__all__ = [
    "Download",
    "Filing",
    "Metadata",
    "Raw",
    "Structured",
    "Text",
    "getFiling",
]
