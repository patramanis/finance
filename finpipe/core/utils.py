"""Small cross-cutting helpers (cache keys, time, identity setup)."""

from __future__ import annotations

import hashlib
import json
import os
from typing import Any


def makeCacheKey(namespace: str, args: tuple[Any, ...], kwargs: dict[str, Any]) -> str:
    """Stable hash of ``(namespace, args, kwargs)`` suitable as a cache key.

    ``namespace`` is typically the chain name (e.g. ``"fundamentals.financials"``).
    Non-JSON-serializable values fall back to ``repr`` so keys remain stable for the
    same inputs within a process.
    """
    payload = {"ns": namespace, "args": list(args), "kwargs": dict(sorted(kwargs.items()))}
    try:
        blob = json.dumps(payload, default=repr, sort_keys=True, separators=(",", ":"))
    except TypeError:
        blob = repr(payload)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()


def ensureSecIdentity() -> str | None:
    """Call ``edgar.set_identity`` from ``SEC_IDENTITY`` (if set) and return the value.

    EdgarTools refuses requests without an identity header. Callers that go through
    the SEC adapter should call this once; it is idempotent.
    """
    identity = os.environ.get("SEC_IDENTITY")
    if not identity:
        return None
    try:
        from edgar import set_identity

        set_identity(identity)
    except Exception:
        pass
    return identity


__all__ = ["ensureSecIdentity", "makeCacheKey"]
