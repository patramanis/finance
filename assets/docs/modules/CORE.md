# finpipe.core — fallback engine

The engine every domain call goes through. Chains try providers in order, consult
a cache, respect per-provider rate limits, and surface typed `Ok` / `Err` results.

## Quick mental model

```
chain.run(*args)
  → cache.get(key)?                   → Ok(from_cache=True)
  → for each (provider, fn) in steps:
       if not config.isAvailable(provider): skip
       if not rate_limiter.allow(provider): skip
       try:
           value = fn(*args)
       except NotFound:       return Err                      # abort chain
       except AuthError:      config.disable(provider); continue
       except RateLimited / TransientError / UnsupportedQuery: continue
       except Exception:      continue
       if value is None: continue
       cache.put(key, value, ttl)
       return Ok(value, provider)
  → Err(attempts=...)
```

## Inspecting a chain

Chains are plain values in `finpipe.core.chains`:

```python
from finpipe.core.chains import FUNDAMENTALS_STATEMENTS

FUNDAMENTALS_STATEMENTS.name        # "fundamentals.financials"
FUNDAMENTALS_STATEMENTS.steps       # (("sec_edgar", <fn>),)
FUNDAMENTALS_STATEMENTS.cache_ttl   # timedelta(hours=24)
```

## Running a chain

```python
from finpipe.core.chains import FUNDAMENTALS_STATEMENTS
from finpipe.core.result import Ok, Err

res = FUNDAMENTALS_STATEMENTS.run("NVDA")
if isinstance(res, Ok):
    print(res.provider, res.from_cache)
    data = res.value                    # provider-native value; normalize before returning to users
else:
    print(res.reason, res.attempts)     # diagnostic trail
```

`strict=True` re-raises the last underlying exception instead of returning `Err`:

```python
FUNDAMENTALS_STATEMENTS.run("NVDA", strict=True)
```

## Building an ad-hoc chain

```python
from datetime import timedelta
from finpipe.core.fallback import FallbackChain
from finpipe.providers import sec_edgar_adapter

MY_CHAIN = FallbackChain(
    name="my.financials",
    steps=(
        ("sec_edgar", sec_edgar_adapter.getFinancials),
        # ("fmpsdk", fmpsdk_adapter.getFinancials),
        # ("yfinance", yfinance_adapter.getFinancials),
    ),
    cache_ttl=timedelta(hours=1),
)
MY_CHAIN.run("AAPL")
```

Every step callable must accept the same arguments passed to `run`.

## Exceptions the chain understands

Adapters raise these from `finpipe.core.exceptions`; anything else is treated as
"unexpected, skip provider, record in attempts":

| Exception | Meaning | Chain does |
|-----------|---------|------------|
| `NotFound` | Resource does not exist (wrong ticker) | **Abort** — return `Err` |
| `AuthError` | Bad / missing credentials | **Disable** provider for session, continue |
| `RateLimited` | Quota exhausted | Skip to next |
| `TransientError` | Network / 5xx / flaky | Skip to next |
| `UnsupportedQuery` | Vendor cannot answer this request | Skip silently |

## Configuration

`.env` at project root, auto-loaded by `finpipe.core.config`:

```dotenv
SEC_IDENTITY=you@example.com
FINNHUB_API_KEY=...
POLYGON_API_KEY=...
FMP_API_KEY=...
```

Runtime checks:

```python
from finpipe.core import config

config.isAvailable("sec_edgar")   # True iff SEC_IDENTITY is set
config.isAvailable("finnhub")     # True iff FINNHUB_API_KEY is set
config.disable("finnhub")         # session-scoped disable
```

## Rate limits

Defaults registered at import for known providers. Override at runtime:

```python
from finpipe.core import rate_limiter

rate_limiter.register("finnhub", capacity=30, refill_per_sec=0.5)
rate_limiter.waitTime("finnhub")  # seconds until a token is available
rate_limiter.reset("finnhub")     # or reset() to clear all
```

Providers without a registered limit always pass.

## Cache

In-memory, TTL-based (per chain). Clear between tests:

```python
from finpipe.core import cache

cache.clear()
cache.size()
```

Cache key = stable sha1 of `(chain.name, args, kwargs)` via
`finpipe.core.utils.makeCacheKey`.

## Full rate-limit / env var tables

See [ARCHITECTURE.md](../ARCHITECTURE.md) — "Configuration" and "Rate-limit defaults" sections.

## When a chain returns `Err`

Inspect `.attempts` — a tuple of `(provider, reason)` pairs in try order. Common causes:

- Every provider was `unavailable` → no API keys set for any registered vendor.
- Every provider was `rate-limited, skipped` → burned the quotas; wait or widen limits.
- A provider raised `unexpected` → adapter isn't translating its native errors to `core.exceptions.*`. That's a bug in the adapter, not the chain.

## Related modules

- Add a new provider to a chain: [PROVIDERS](PROVIDERS.md)
- Consume a chain from a domain method: [FUNDAMENTALS](FUNDAMENTALS.md)
