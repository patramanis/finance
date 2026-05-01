# finpipe — architecture

Public import style:

```python
import finpipe as fp

fp.fundamentals.getFinancials("AAPL").incomeStatement()
# or:
from finpipe.fundamentals import getFinancials, getMarketData
```

High-level design: **shared engine in `core`**, **pluggable provider adapters**, **pre-wired fallback chains**, **thin domain APIs** (`technicals`, `fundamentals`, …). Naming conventions live in [`RULES.md`](RULES.md).

-----

## Layers

```text
┌─────────────────────────────────────────────────────────────┐
│  Facade       fp.fundamentals.getFinancials, .getMarketData  │
├─────────────────────────────────────────────────────────────┤
│  Domain       fundamentals/  technicals/  macro/  …          │  <- "what data"
├─────────────────────────────────────────────────────────────┤
│  core/  (the engine)                                         │
│    fallback.py   chains.py     result.py   exceptions.py     │  <- provider-agnostic
│    rate_limiter.py  cache.py   config.py   utils.py          │     orchestration
├─────────────────────────────────────────────────────────────┤
│  providers/   yfinance_adapter.py  sec_edgar_adapter.py  …   │  <- "how to fetch"
├─────────────────────────────────────────────────────────────┤
│  displays/    display(obj) router + type-specific renderers   │
└─────────────────────────────────────────────────────────────┘
```

Rule: lower layers never import upper layers. Domain code does **not** embed long "try A then B" lists — it asks `core.chains` for the right `FallbackChain` and runs it.

-----

## `core/` — the engine

| File | Role |
|------|------|
| `exceptions.py` | `ProviderError` + `RateLimited`, `AuthError`, `NotFound`, `TransientError`, `UnsupportedQuery`. Adapters translate their native errors into these. |
| `result.py` | `Ok[T](value, provider, from_cache)` and `Err(provider, reason, exc, attempts)`. Chains return these instead of raising. |
| `config.py` | Loads `.env` at import, declares which env vars each provider needs, exposes `isAvailable(provider)`, `getKey(provider)`, `disable / enable`. Auth failures auto-disable a provider for the session. |
| `rate_limiter.py` | Per-provider token bucket pre-loaded with documented free-tier quotas (finnhub 60/min, fmp 250/day, polygon 5/min, …). Providers without a registered limit always pass. |
| `cache.py` | In-memory TTL LRU (1024 entries, threadsafe), keyed by chain name + args via `utils.makeCacheKey`. Disk backend is future work. |
| `utils.py` | `makeCacheKey` (stable sha1 of args) and `ensureSecIdentity` (idempotently wires `SEC_IDENTITY` into EdgarTools). |
| `fallback.py` | `FallbackChain(name, steps, cache_ttl).run(*args, strict=False, **kw)` — walks steps, consulting cache → availability → rate limiter, applies per-exception policy. Returns `Ok` or `Err` with an attempt trail. |
| `chains.py` | Pre-wired chains as module-level constants. One per data category. |

### Fallback chain semantics

A chain is a value, not a framework:

```python
FUNDAMENTALS_STATEMENTS = FallbackChain(
    name="fundamentals.financials",
    steps=(
        ("sec_edgar", sec_edgar_adapter.getFinancials),
    ),
    cache_ttl=timedelta(hours=24),
)
```

Per-step policy inside `fallback.run`:

| Exception from adapter | Chain behavior |
|------------------------|-----------------|
| `NotFound` | Abort. Every provider will give the same answer; return `Err`. |
| `AuthError` | Disable provider for the session, continue. |
| `RateLimited` | Skip to next provider. |
| `TransientError` | Skip to next provider. |
| `UnsupportedQuery` | Skip to next provider. |
| Any other `Exception` | Skip, record in `attempts`. |
| Returns `None` | Treat as "empty, try next". |
| Returns a value | Cache (if TTL > 0) and return `Ok`. |

`strict=True` re-raises the last underlying exception instead of returning `Err`.

-----

## `providers/` — adapters

Rules:

- One file per vendor.
- Module-level `PROVIDER_NAME` string constant.
- Plain functions (no classes). Same signature across vendors for a category (every OHLCV adapter exposes `getOHLCV(symbol, *, interval, start, end)`; every financials adapter exposes `getFinancials(ticker)`; etc.).
- Translate native errors into `core.exceptions.*`. Nothing else goes up.
- No Rich, no caching, no fallback logic.

Current: only `sec_edgar_adapter.py` is implemented. Everything else is a scaffolded empty file.

-----

## `fundamentals/` — domain API surface

Five grouping functions. Each returns an object; users call methods on that object. No classes are public; the objects are handles.

```python
from finpipe.fundamentals import (
    getFinancials,   # what the company reports (statements, ratios, earnings, …)
    getMarketData,   # what the market observes (price, shares, risk)
    getFiling,       # raw SEC EDGAR access (all form types)
    getDerived,      # computed-only (EV, WACC, ROIC, …); no fetching
    getCompany,      # static context (profile, analyst, credit)
)
```

All methods return `pd.DataFrame` or `dict` — provider-specific objects never surface.

### Folder layout

```text
fundamentals/
├── __init__.py                # re-exports the 5 grouping functions
├── financials/
│   ├── __init__.py            # getFinancials(ticker) -> Financials
│   ├── statements.py          # class Statements: incomeStatement, balanceSheet, cashFlow
│   ├── ratios.py              # class Ratios
│   ├── valuation.py           # class Valuation
│   ├── earnings.py            # class Earnings
│   ├── dividends.py           # class Dividends
│   ├── segments.py            # class Segments
│   ├── ownership.py           # class Ownership  (insider, 13F)
│   └── corporateActions.py    # class CorporateActions
├── marketData/
│   ├── __init__.py            # getMarketData(ticker) -> MarketData
│   ├── price.py               # class Price
│   ├── shares.py              # class Shares
│   └── risk.py                # class Risk
├── filings/
│   ├── __init__.py            # getFiling(ticker, form=None) -> Filing  (flat API)
│   ├── metadata.py            # class Metadata
│   ├── structured.py          # class Structured
│   ├── text.py                # class Text
│   ├── raw.py                 # class Raw
│   └── download.py            # class Download
├── derived/
│   ├── __init__.py            # getDerived(ticker) -> Derived  (flat API)
│   ├── debt.py                # class Debt
│   ├── valuation.py           # class ValuationDerived
│   ├── returns.py             # class Returns
│   └── costOfCapital.py       # class CostOfCapital
└── company/
    ├── __init__.py            # getCompany(ticker) -> Company
    ├── profile.py             # class Profile  (flat on handle)
    ├── analyst.py             # class Analyst  (nested)
    └── credit.py              # class Credit   (nested)
```

### API-shape rules

| Grouping | Handle flat methods | Nested attributes |
|----------|---------------------|-------------------|
| `getFinancials` | `incomeStatement`, `balanceSheet`, `cashFlow` | `ratios`, `valuation`, `earnings`, `dividends`, `segments`, `ownership`, `corporateActions` |
| `getMarketData` | (none) | `price`, `shares`, `risk` |
| `getFiling` | `metadata`, `latest`, `search`, `statements`, `notes`, `section`, `get`, `download` | (none) |
| `getDerived` | `netDebt`, `investedCapital`, `enterpriseValue`, `evEbitda`, `roic`, `eva`, `wacc` | (none) |
| `getCompany` | `profile`, `description` | `analyst`, `credit` |

### Design rules

1. Nothing in `derived/` is fetched — it is a computation layer only.
2. `getFiling` is the raw SEC access layer; `getFinancials` is the clean structured layer. They are not duplicates.
3. `getFinancials` is not a 10-K wrapper — it pulls from whichever provider has the data cleanly. Filing type is metadata, not structure.
4. `getMarketData` = market observes. `getFinancials` = company reports. Never mix the two inside one module.
5. `getFiling().section()` returns `str` by design — sections are prose, not tables.
6. All public methods return `pd.DataFrame` or `dict`.

### Current state

Scaffold only. Every method body is `raise NotImplementedError` with a docstring. No provider wiring yet.

-----

## Configuration

- `.env` at the project root, auto-loaded by `core.config` (no `python-dotenv` dep).

| Provider | Env var |
|----------|---------|
| `sec_edgar`, `sec_downloader` | `SEC_IDENTITY` |
| `finnhub` | `FINNHUB_API_KEY` |
| `polygon` | `POLYGON_API_KEY` |
| `fmpsdk` | `FMP_API_KEY` |
| `simfin` | `SIMFIN_API_KEY` |
| `alpha_vantage` | `ALPHA_VANTAGE_API_KEY` |
| `tardis` | `TARDIS_API_KEY` |
| `yfinance`, `ccxt`, `coingecko`, `datareader`, `ib_insync` | none |

`config.isAvailable("finnhub")` ↔ does the required env var exist (and is the provider not session-disabled)?

-----

## Rate-limit defaults

Registered at import in `rate_limiter.py`:

| Provider | Capacity | Refill |
|----------|----------|--------|
| `finnhub` | 60 | per minute |
| `fmpsdk` | 250 | per day |
| `polygon` | 5 | per minute |
| `alpha_vantage` | 25 | per day |
| `marketaux` | 100 | per day |
| `newsapi` | 100 | per day |
| `simfin` | 2000 | per day |
| `cryptopanic` | 1000 | per day |
| `coinglass` | 300 | per day |
| `bls` | 3000 | per day |
| `sec_edgar` | 10 | per second |

Override via `rate_limiter.register(provider, capacity=..., refill_per_sec=...)`.

-----

## Asset-class detection

Not yet implemented. Chains that depend on asset class (stocks vs crypto OHLCV) will live as separate constants (`STOCKS_OHLCV`, `CRYPTO_OHLCV`) selected by an explicit `asset=` argument or a later symbol heuristic (`/`, `-PERP`, `-USDT` → crypto).

-----

## Build order

Intended dependency direction: `core` → `technicals` → `fundamentals` → `macro` → `derivatives` → `sentiment`.

Current status:

- `core/` — implemented.
- `providers/` — only `sec_edgar_adapter` implemented.
- `fundamentals/` — full API **scaffold** (classes, method signatures, docstrings); no bodies.
- `technicals/`, `macro/`, `derivatives/`, `sentiment/` — empty.
- `displays/` — implemented as a two-layer display system:
  - `display.py` exports one public function `display(obj, ...)` (single user entrypoint).
  - type-specific modules (currently `edgar.py`) implement specialized render logic.
  - router behavior: if object is `edgartools.Financials`, dispatch to `edgar.renderStatement`; otherwise generic Rich print.
- `core/chains.py` defines `FUNDAMENTALS_STATEMENTS`; waiting for `financials/statements.py` to consume it.

-----

## Wiring the first domain method (when ready)

Pattern for turning a `NotImplementedError` stub into a live method:

```python
# fundamentals/financials/statements.py
from finpipe.core.chains import FUNDAMENTALS_STATEMENTS
from finpipe.core.result import Err

class Statements:
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def incomeStatement(self):
        res = FUNDAMENTALS_STATEMENTS.run(self.ticker)
        if isinstance(res, Err):
            raise RuntimeError(f"No provider served financials: {res.reason}")
        return _normalizeToDataFrame(res.value, kind="income")
```

Rules when filling in scaffolds:

- Never import a provider adapter directly from a domain method — go through a chain in `core.chains`.
- Method must return `pd.DataFrame` or `dict`, never a provider-native object.
- If the adapter's native object needs normalization, that logic lives inside the domain method (or a helper under `fundamentals/_normalize/`), not inside the adapter.

-----

## SEC / EdgarTools note

EdgarTools is one adapter among many. It requires an identity header; `core.utils.ensureSecIdentity` handles this from `SEC_IDENTITY`. The SEC fair-access guideline (≤ 10 req/s) is enforced by `rate_limiter` for the `sec_edgar` provider.
