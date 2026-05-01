"""Return envelope for fallback-chain calls.

Callers inspect ``isinstance(res, Ok)`` vs ``Err`` rather than catching exceptions
(exceptions are reserved for programmer errors and the ``strict=True`` path).

``Ok`` carries which provider served the value and whether it came from cache,
so users can tell ``yfinance`` from ``finnhub`` after the fact.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Ok(Generic[T]):
    value: T
    provider: str
    from_cache: bool = False


@dataclass(frozen=True, slots=True)
class Err:
    provider: str
    reason: str
    exc: Exception | None = None
    attempts: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    """Per-provider trail of ``(provider, reason)`` for diagnostics."""


Result = Ok[T] | Err


__all__ = ["Err", "Ok", "Result"]
