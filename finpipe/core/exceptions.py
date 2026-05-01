"""Typed provider errors the fallback engine reasons about.

Adapters translate their native exceptions (``requests.HTTPError``,
``yfinance.exceptions.YFRateLimitError``, ...) into one of these so
``FallbackChain`` can decide whether to retry, skip to the next provider,
or abort the whole chain.
"""

from __future__ import annotations


class ProviderError(Exception):
    """Base class for every error an adapter raises on behalf of a provider."""

    def __init__(self, provider: str, message: str = "") -> None:
        super().__init__(f"[{provider}] {message}" if message else f"[{provider}]")
        self.provider = provider
        self.message = message


class RateLimited(ProviderError):
    """Provider quota exhausted. Chain should skip to the next provider."""


class AuthError(ProviderError):
    """Missing / invalid API key. Chain should disable this provider for the session."""


class NotFound(ProviderError):
    """Symbol, ticker, or resource genuinely does not exist.

    The chain should abort instead of trying other providers — every provider
    will give the same answer.
    """


class TransientError(ProviderError):
    """Temporary failure (network blip, 5xx). Chain should move on to the next provider."""


class UnsupportedQuery(ProviderError):
    """Provider cannot answer this particular request (e.g. crypto on SEC EDGAR).

    Chain should silently skip to the next provider.
    """


__all__ = [
    "AuthError",
    "NotFound",
    "ProviderError",
    "RateLimited",
    "TransientError",
    "UnsupportedQuery",
]
