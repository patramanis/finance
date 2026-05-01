"""Configuration: API keys, identities, and per-provider availability.

Reads environment variables (including a ``.env`` file at the project root,
parsed by hand so we don't pull in ``python-dotenv``).

The single source of truth for "does this provider need a key, and do we have it?"
— used by ``chains.py`` to skip un-keyed providers when building default chains.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Mapping

_PROVIDER_ENV_KEYS: Mapping[str, tuple[str, ...]] = {
    "yfinance": (),
    "ccxt": (),
    "coingecko": (),
    "sec_edgar": ("SEC_IDENTITY",),
    "sec_downloader": ("SEC_IDENTITY",),
    "finnhub": ("FINNHUB_API_KEY",),
    "polygon": ("POLYGON_API_KEY",),
    "fmpsdk": ("FMP_API_KEY",),
    "simfin": ("SIMFIN_API_KEY",),
    "alpha_vantage": ("ALPHA_VANTAGE_API_KEY",),
    "tardis": ("TARDIS_API_KEY",),
    "ib_insync": (),
    "datareader": (),
}

_disabled: set[str] = set()


def _load_dotenv(path: Path) -> None:
    """Populate ``os.environ`` from ``path`` without overwriting existing values."""
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


_load_dotenv(_project_root() / ".env")


def getKey(provider: str) -> str | None:
    """Return the configured API key for ``provider`` (first matching env var), else ``None``."""
    for var in _PROVIDER_ENV_KEYS.get(provider, ()):
        value = os.environ.get(var)
        if value:
            return value
    return None


def isAvailable(provider: str) -> bool:
    """True if ``provider`` can be used right now (key present when required, not disabled)."""
    if provider in _disabled:
        return False
    required = _PROVIDER_ENV_KEYS.get(provider, ())
    if not required:
        return True
    return getKey(provider) is not None


def disable(provider: str) -> None:
    """Mark ``provider`` unusable for the rest of the session (e.g. after an auth failure)."""
    _disabled.add(provider)


def enable(provider: str) -> None:
    """Re-enable a previously disabled provider."""
    _disabled.discard(provider)


def registeredProviders() -> tuple[str, ...]:
    return tuple(_PROVIDER_ENV_KEYS)


__all__ = [
    "disable",
    "enable",
    "getKey",
    "isAvailable",
    "registeredProviders",
]
