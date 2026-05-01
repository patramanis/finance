"""The ``FallbackChain`` executor.

A chain is a list of ``(provider_name, callable)`` steps plus a cache TTL.
``run`` walks the list, consulting the rate limiter and cache, and returns the
first ``Ok(value, provider)`` or a terminal ``Err`` with the full attempt trail.

This is the single abstraction every domain call goes through. Providers are
unaware of it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
from typing import Any, Callable

from . import cache, config, rate_limiter, utils
from .exceptions import (
    AuthError,
    NotFound,
    ProviderError,
    RateLimited,
    TransientError,
    UnsupportedQuery,
)
from .result import Err, Ok, Result

ProviderFn = Callable[..., Any]
Step = tuple[str, ProviderFn]


@dataclass(frozen=True, slots=True)
class FallbackChain:
    """An ordered list of providers to try for a single data category."""

    name: str
    steps: tuple[Step, ...]
    cache_ttl: timedelta = field(default_factory=lambda: timedelta(0))

    def run(self, *args: Any, strict: bool = False, **kwargs: Any) -> Result:
        """Try each step in order. Returns ``Ok`` on first success, else a final ``Err``.

        ``strict=True`` raises the underlying exception from the last attempt instead
        of returning ``Err`` (handy for tests and CLI usage).
        """
        ttl_seconds = self.cache_ttl.total_seconds()
        key = utils.makeCacheKey(self.name, args, kwargs) if ttl_seconds > 0 else ""

        if ttl_seconds > 0:
            hit = cache.get(key)
            if hit is not None:
                return Ok(value=hit.value, provider=hit.provider, from_cache=True)

        trail: list[tuple[str, str]] = []
        last_exc: Exception | None = None

        for provider, fn in self.steps:
            if not config.isAvailable(provider):
                trail.append((provider, "unavailable (missing key or disabled)"))
                continue
            if not rate_limiter.allow(provider):
                trail.append((provider, "rate-limited, skipped"))
                continue

            try:
                value = fn(*args, **kwargs)
            except NotFound as e:
                if strict:
                    raise
                trail.append((provider, f"not-found: {e.message or e}"))
                return Err(
                    provider=provider,
                    reason="resource not found",
                    exc=e,
                    attempts=tuple(trail),
                )
            except AuthError as e:
                config.disable(provider)
                trail.append((provider, f"auth: {e.message or e}"))
                last_exc = e
                continue
            except (RateLimited, TransientError, UnsupportedQuery, ProviderError) as e:
                trail.append((provider, f"{type(e).__name__.lower()}: {e.message or e}"))
                last_exc = e
                continue
            except Exception as e:
                trail.append((provider, f"unexpected: {e!r}"))
                last_exc = e
                continue

            if value is None:
                trail.append((provider, "empty result"))
                continue

            if ttl_seconds > 0:
                cache.put(key, value, provider=provider, ttl_seconds=ttl_seconds)
            return Ok(value=value, provider=provider)

        if strict and last_exc is not None:
            raise last_exc
        return Err(
            provider=trail[-1][0] if trail else "none",
            reason="no provider succeeded",
            exc=last_exc,
            attempts=tuple(trail),
        )


__all__ = ["FallbackChain", "Step"]
