"""Per-provider token-bucket rate limiter.

Each provider gets a bucket sized to its documented free-tier quota. When a
``FallbackChain`` is about to call provider X it consults ``allow("x")``; if
the bucket is empty the chain skips to the next provider instead of burning
a token on a request we know will 429.

Buckets are in-memory (per process). That is correct for a single-user CLI /
notebook workflow; multi-process usage would need a shared store later.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Mapping


@dataclass
class _Bucket:
    capacity: float
    refill_per_sec: float
    tokens: float = field(init=False)
    last: float = field(init=False)

    def __post_init__(self) -> None:
        self.tokens = self.capacity
        self.last = time.monotonic()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self.last
        if elapsed > 0:
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_per_sec)
            self.last = now

    def try_take(self, cost: float = 1.0) -> bool:
        self._refill()
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False

    def wait_time(self, cost: float = 1.0) -> float:
        self._refill()
        if self.tokens >= cost:
            return 0.0
        missing = cost - self.tokens
        return missing / self.refill_per_sec if self.refill_per_sec > 0 else float("inf")


_DEFAULT_LIMITS: Mapping[str, tuple[float, float]] = {
    "finnhub": (60, 60 / 60.0),
    "fmpsdk": (250, 250 / 86_400.0),
    "polygon": (5, 5 / 60.0),
    "alpha_vantage": (25, 25 / 86_400.0),
    "marketaux": (100, 100 / 86_400.0),
    "newsapi": (100, 100 / 86_400.0),
    "simfin": (2000, 2000 / 86_400.0),
    "cryptopanic": (1000, 1000 / 86_400.0),
    "coinglass": (300, 300 / 86_400.0),
    "bls": (3000, 3000 / 86_400.0),
    "sec_edgar": (10, 10.0),
}


_buckets: dict[str, _Bucket] = {}
_lock = threading.Lock()


def _bucket_for(provider: str) -> _Bucket | None:
    with _lock:
        if provider in _buckets:
            return _buckets[provider]
        limit = _DEFAULT_LIMITS.get(provider)
        if limit is None:
            return None
        capacity, refill = limit
        bucket = _Bucket(capacity=capacity, refill_per_sec=refill)
        _buckets[provider] = bucket
        return bucket


def register(provider: str, *, capacity: float, refill_per_sec: float) -> None:
    """Install / replace a limiter for ``provider``. Override defaults at runtime."""
    with _lock:
        _buckets[provider] = _Bucket(capacity=capacity, refill_per_sec=refill_per_sec)


def allow(provider: str, *, cost: float = 1.0) -> bool:
    """Try to consume ``cost`` tokens. Returns False if the bucket is empty.

    Providers with no registered limit always return True (e.g. ``yfinance``,
    ``ccxt`` public endpoints — we let the HTTP layer surface rate errors).
    """
    bucket = _bucket_for(provider)
    if bucket is None:
        return True
    with _lock:
        return bucket.try_take(cost)


def waitTime(provider: str, *, cost: float = 1.0) -> float:
    """Seconds until ``cost`` tokens are available for ``provider``. 0 if available now."""
    bucket = _bucket_for(provider)
    if bucket is None:
        return 0.0
    with _lock:
        return bucket.wait_time(cost)


def reset(provider: str | None = None) -> None:
    """Reset one or all buckets. Primarily for tests."""
    with _lock:
        if provider is None:
            _buckets.clear()
        else:
            _buckets.pop(provider, None)


__all__ = ["allow", "register", "reset", "waitTime"]
