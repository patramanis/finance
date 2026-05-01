"""In-memory TTL cache for fallback-chain results.

Keyed by the stable hash from ``utils.makeCacheKey`` (chain name + args).
A disk backend can be layered on later without touching call sites.
"""

from __future__ import annotations

import threading
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class _Entry:
    value: Any
    provider: str
    expires_at: float


_MAX_ENTRIES = 1024
_store: OrderedDict[str, _Entry] = OrderedDict()
_lock = threading.Lock()


def get(key: str) -> _Entry | None:
    """Return a cache entry if present and fresh, else ``None``."""
    now = time.monotonic()
    with _lock:
        entry = _store.get(key)
        if entry is None:
            return None
        if entry.expires_at < now:
            _store.pop(key, None)
            return None
        _store.move_to_end(key)
        return entry


def put(key: str, value: Any, *, provider: str, ttl_seconds: float) -> None:
    """Insert ``value`` with a ``ttl_seconds`` expiry. ``ttl_seconds <= 0`` is a no-op."""
    if ttl_seconds <= 0:
        return
    expires_at = time.monotonic() + ttl_seconds
    with _lock:
        _store[key] = _Entry(value=value, provider=provider, expires_at=expires_at)
        _store.move_to_end(key)
        while len(_store) > _MAX_ENTRIES:
            _store.popitem(last=False)


def clear() -> None:
    with _lock:
        _store.clear()


def size() -> int:
    with _lock:
        return len(_store)


__all__ = ["clear", "get", "put", "size"]
