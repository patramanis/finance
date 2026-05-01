# finpipe.providers

One file per vendor under `finpipe/providers/<name>_adapter.py`. Adapters are
**thin**: plain functions, no classes, no Rich, no caching, no fallback logic.
Vendor-specific work is limited to error translation.

This doc has three halves:

1. **[Current providers in use](#current-providers-in-use-today)** — what is actually wired in code right now.
2. **[Catalog](#catalog--providers-per-public-call-target-order)** — target provider(s) per public call, in fallback order.
3. **[Writing a new adapter](#writing-a-new-adapter)** — the full authoring guide.

-----

## Current providers in use today

This is the real implementation status at the moment:

- Adapter files currently implemented under `finpipe/providers`: `sec_edgar_adapter` only.
- Chain steps currently wired in `finpipe/core/chains.py`: `FUNDAMENTALS_STATEMENTS` uses only `sec_edgar`.
- Domain methods are still scaffolded (`NotImplementedError`), so this wiring is present but mostly not consumed yet.

Provider keys/registration exist for several planned providers in `finpipe/core/config.py`
(`finnhub`, `fmpsdk`, `simfin`, `polygon`, `alpha_vantage`, etc.), but those adapters
are not wired into chains yet.

-----

## Catalog — providers per public call (target order)

Order shown = intended fallback order once corresponding adapters/chains are wired
(leftmost tried first). Blank sections are top-level modules not yet designed.

### fundamentals

#### financials/

| Call | Providers (in fallback order) |
|------|-------------------------------|
| `.incomeStatement()`, `.balanceSheet()`, `.cashFlow()` | sec_edgar (XBRL via edgartools) → simfinapi → fmpsdk → yfinance |
| `.ratios.*` (`roe`, `roa`, `margins`, `all`) | fmpsdk → finnhub → computed from statements |
| `.valuation.*` (`pe`, `pb`, `ps`) | yfinance → fmpsdk |
| `.earnings.*` (`actual`, `guidance`, `nextDate`) | finnhub → fmpsdk → yfinance → alpha_vantage |
| `.dividends.*` (`history`, `payoutRatio`) | yfinance → fmpsdk |
| `.segments.*` (`bySegment`, `byGeography`) | sec_edgar (XBRL) → fmpsdk |
| `.ownership.insiderTrades()` | sec_edgar (Form 4) → finnhub → fmpsdk |
| `.ownership.institutional()` | sec_edgar (13F) → yfinance → fmpsdk |
| `.corporateActions.splits()` | yfinance → fmpsdk |
| `.corporateActions.buybacks()` | fmpsdk → sec_edgar (10-K notes) |
| `.corporateActions.mergers()` | fmpsdk → sec_edgar (8-K events) |

#### marketData/

| Call | Providers |
|------|-----------|
| `.price.history()`, `.price.current()` | yfinance |
| `.shares.outstanding()` | yfinance → fmpsdk |
| `.shares.shortInterest()` | yfinance (FINRA-sourced) → finnhub |
| `.risk.beta()` | yfinance (provider-supplied) |
| `.risk.realizedVol()` | computed locally from `price.history()` |

#### filings/

| Call | Providers |
|------|-----------|
| all (`.metadata`, `.latest`, `.search`, `.statements`, `.notes`, `.section`, `.get`, `.download`) | sec_edgar via edgartools |

#### derived/

No providers. Every method is computed locally from `getFinancials`,
`getMarketData`, and (later) `macro`. See the dependency chain in
[ARCHITECTURE.md](../ARCHITECTURE.md).

#### company/

| Call | Providers |
|------|-----------|
| `.profile()`, `.description()` | yfinance → fmpsdk |
| `.analyst.estimates()`, `.analyst.priceTarget()` | fmpsdk → finnhub → yfinance |
| `.credit.ratings()`, `.credit.outlook()` | fmpsdk (patchy on free tier) |

### technicals

TBD.

### macro

TBD.

### derivatives

TBD.

### sentiment

TBD.

-----

## Writing a new adapter

### Checklist

```
- [ ] Create finpipe/providers/<vendor>_adapter.py
- [ ] Module-level PROVIDER_NAME = "<vendor>"
- [ ] Implement fetchers matching the category's standard signature
- [ ] Translate native errors to finpipe.core.exceptions.*
- [ ] Register env var(s) in finpipe/core/config.py::_PROVIDER_ENV_KEYS (if keyed)
- [ ] Register rate limit in finpipe/core/rate_limiter.py::_DEFAULT_LIMITS (if documented)
- [ ] Append (PROVIDER_NAME, <fn>) to the relevant chain in finpipe/core/chains.py
```

### Category signatures (every adapter in a category must match)

| Category | Standard signature | Return |
|----------|--------------------|--------|
| Financial statements | `getFinancials(ticker: str)` | vendor object → normalized in domain layer |
| Quarterly statements | `getQuarterlyFinancials(ticker: str)` | vendor object |
| OHLCV | `getOHLCV(symbol: str, *, interval: str, start, end)` | `pd.DataFrame` |
| Filings list | `getFilings(ticker: str, *, form: str \| None = None, **kw)` | iterable / list |
| Ratios | `getRatios(ticker: str)` | vendor object or dict |
| Earnings | `getEarnings(ticker: str)` | vendor object |

Same name across vendors = interchangeable behind a `FallbackChain`.

### Typed-exception translation

Import from `finpipe.core.exceptions`:

| Vendor situation | Raise |
|------------------|-------|
| Ticker doesn't exist on this vendor | `NotFound(PROVIDER_NAME, "...")` |
| Missing / invalid API key | `AuthError(PROVIDER_NAME, "...")` |
| 429 / quota exceeded | `RateLimited(PROVIDER_NAME, "...")` |
| Network error / 5xx / timeout | `TransientError(PROVIDER_NAME, "...")` |
| Vendor cannot answer this query (e.g. crypto on SEC) | `UnsupportedQuery(PROVIDER_NAME, "...")` |

Anything else the fallback chain treats as "skip, record as unexpected". That's
fine for truly unforeseen errors, but don't use it as the default — classify.

### Canonical example

```python
# finpipe/providers/sec_edgar_adapter.py

from __future__ import annotations
from typing import Any, Optional

from edgar import Company
from edgar.financials import Financials

from finpipe.core import utils
from finpipe.core.exceptions import AuthError, NotFound, TransientError

PROVIDER_NAME = "sec_edgar"


def _company(ticker: str) -> Company:
    utils.ensureSecIdentity()
    try:
        return Company(ticker)
    except (KeyError, ValueError, LookupError) as e:
        raise NotFound(PROVIDER_NAME, f"ticker {ticker!r} not found") from e
    except Exception as e:
        msg = repr(e).lower()
        if "identity" in msg or "user-agent" in msg:
            raise AuthError(PROVIDER_NAME, "set SEC_IDENTITY") from e
        raise TransientError(PROVIDER_NAME, f"lookup failed: {e!r}") from e


def getFinancials(ticker: str) -> Optional[Financials]:
    company = _company(ticker)
    try:
        return company.get_financials()
    except Exception as e:
        raise TransientError(PROVIDER_NAME, f"get_financials failed: {e!r}") from e
```

Notes:

- `PROVIDER_NAME` is the same key used by `config.isAvailable(...)`, `rate_limiter.allow(...)`, and chain step tuples. Keep it consistent.
- Return `None` (not raise) when the vendor has no data for a valid ticker — the chain treats `None` as "empty, try next".
- `from e` preserves the original traceback; always use it on `raise ... from`.

### Registering keys

If the vendor needs an API key, add it to `finpipe/core/config.py`:

```python
_PROVIDER_ENV_KEYS: Mapping[str, tuple[str, ...]] = {
    ...
    "my_vendor": ("MY_VENDOR_API_KEY",),
}
```

`config.isAvailable("my_vendor")` then returns `True` iff the env var is set
(and the provider isn't session-disabled).

### Registering rate limits

If the vendor publishes a quota, add it to `finpipe/core/rate_limiter.py`:

```python
_DEFAULT_LIMITS: Mapping[str, tuple[float, float]] = {
    ...
    "my_vendor": (100, 100 / 86_400.0),   # 100/day
}
```

`(capacity, refill_per_sec)`. Per-minute: `(cap, cap / 60)`. Per-day:
`(cap, cap / 86_400)`. Per-second: `(cap, cap)`.

Providers without an entry always pass `allow(...)` — use this for public /
untyped sources (e.g. `yfinance`, `ccxt` public endpoints) where the HTTP layer
surfaces rate errors naturally.

### Appending to a chain

Open `finpipe/core/chains.py` and append a step to the relevant constant:

```python
from finpipe.providers import sec_edgar_adapter, my_vendor_adapter

FUNDAMENTALS_STATEMENTS = FallbackChain(
    name="fundamentals.financials",
    steps=(
        ("sec_edgar", sec_edgar_adapter.getFinancials),
        ("my_vendor", my_vendor_adapter.getFinancials),   # new
    ),
    cache_ttl=timedelta(hours=24),
)
```

Order matters: leftmost is tried first. Put the most accurate / highest-quota /
most-covering provider first, cheap free tiers last. The existing fallback order
per call is in the [catalog](#catalog--providers-per-public-call) above.

### Don't

- Don't import anything from `finpipe.fundamentals` / `finpipe.technicals` / `finpipe.displays` inside an adapter — it's a layer violation and creates import cycles.
- Don't normalize data inside the adapter (no DataFrame construction, no column renaming). Normalization is a domain-layer concern.
- Don't print, log, or call `rich.print` in an adapter.
- Don't cache inside an adapter. The chain handles caching.

-----

## Related modules

- Consume the chain you just extended: [CORE](CORE.md)
- Expose the new capability as a domain method: [FUNDAMENTALS](FUNDAMENTALS.md)
