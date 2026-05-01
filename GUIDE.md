# finpipe Beginner Guide

This is the one-file guide for taking over the project.

## 1) What finpipe is

`finpipe` is a Python data framework for finance that is built in layers:

- **Domain modules**: what users ask for (`fundamentals`, `technicals`, `macro`, `derivatives`, `sentiment`)
- **Core engine**: how providers are tried (`fallback`, `chains`, `cache`, `rate_limiter`, `config`)
- **Provider adapters**: one file per vendor (`sec_edgar_adapter`, future `yfinance_adapter`, etc.)
- **Displays**: one user entrypoint `display(obj)` plus type-specific renderers (`edgar.py`)

Design goal: users call domain APIs (`getFinancials`, `getCompany`, etc.) and never care which provider served data.

---

## 2) Folder map (important)

```text
finpipe/
├── core/         fallback engine (provider-agnostic)
├── providers/    vendor adapters (one per provider)
├── displays/     display(obj) router + specialized renderers
├── fundamentals/ primary domain module (scaffolded API surface)
├── technicals/   stub
├── macro/        stub
├── derivatives/  stub
└── sentiment/    stub
assets/docs/      deeper architecture/module docs
```

---

## 3) Current implementation status (today)

- `core/`: implemented
- `providers/`: only `sec_edgar_adapter.py` implemented
- `chains`: only `FUNDAMENTALS_STATEMENTS` is wired, currently with `sec_edgar` step only
- `fundamentals/`: full class/method scaffold exists, most methods still `NotImplementedError`
- `technicals/macro/derivatives/sentiment`: placeholders only
- `displays/`: implemented generic `display(obj)` and specialized `edgar.py` renderer

So the architecture is real, but domain method wiring is still in progress.

---

## 4) How data flows (most important concept)

For any real domain call, intended flow is:

1. User calls domain method (example: `getFinancials("AAPL").incomeStatement()`)
2. Domain method runs a pre-wired chain from `core/chains.py`
3. `FallbackChain` tries providers in order
4. First good result is cached and returned
5. Domain normalizes provider output to project output (`DataFrame`/`dict`)
6. User can call `display(obj)` to render it

The domain layer should not contain hardcoded provider fallback logic; chains own that.

---

## 5) FallbackChain behavior

`FallbackChain.run(...)` handles:

- provider availability checks (`config.isAvailable`)
- rate limit checks (`rate_limiter.allow`)
- cache lookup/write (`cache`)
- step-by-step provider attempts
- typed error policies:
  - `NotFound`: abort chain
  - `AuthError`: disable provider for session and continue
  - `RateLimited`: continue
  - `TransientError`: continue
  - `UnsupportedQuery`: continue
  - unknown exception: continue and record

Return type is `Ok(...)` or `Err(...)` (from `core/result.py`).

---

## 6) Provider contract (how all adapters should look)

Each adapter file in `finpipe/providers` should:

- define `PROVIDER_NAME`
- expose category-standard function names/signatures
- translate native SDK/HTTP errors into `core.exceptions`
- avoid fallback logic, caching, rendering, or domain imports

Same category across providers must use same function signatures so chains can swap them.

---

## 7) Display system (simple rule)

- Public rendering API is one function: `from finpipe.displays import display`
- Call `display(any_object)`
- Router logic:
  - if object is Edgar `Financials`, use specialized renderer (`edgar.renderStatement`)
  - else use generic Rich print

This keeps UI simple for users while preserving rich type-specific formatting.

---

## 8) Naming conventions used here

- module/package names: `snake_case` (or lowercase)
- classes: `PascalCase`
- variables: `snake_case`
- constants: `UPPER_SNAKE_CASE`
- public fetchers/methods in this project: `camelCase` with `get` style

Note: there are a few known camelCase filename exceptions in fundamentals scaffold.

---

## 9) How to add a new provider (step-by-step)

1. Create `finpipe/providers/<vendor>_adapter.py`
2. Implement required function(s) for the target category
3. Map vendor errors to typed core exceptions
4. Register env key in `core/config.py` (if provider needs auth)
5. Register default rate limits in `core/rate_limiter.py` (if known)
6. Add provider step to correct chain in `core/chains.py`
7. In domain method, call chain and normalize result to `DataFrame`/`dict`
8. Optionally test output with `display(obj)`

If this sequence is followed, the project stays consistent.

---

## 10) How to add a new domain method

1. Pick or create chain in `core/chains.py`
2. In domain method, run chain
3. Handle `Err` clearly (raise project-friendly runtime error)
4. Normalize successful provider output
5. Return stable project shape (`DataFrame`/`dict`)
6. Keep rendering out of domain method (render separately via `display`)

---

## 11) Practical first tasks for an intern

Good starter order:

1. Wire one extra provider into `FUNDAMENTALS_STATEMENTS`
2. Implement `incomeStatement()` in fundamentals using that chain
3. Add normalization helper for one statement shape
4. Confirm `display(...)` works on produced object
5. Repeat same pattern for `balanceSheet()` / `cashFlow()`

This gives immediate progress without architecture churn.

---

## 12) What not to break

- Do not import `fundamentals` from provider adapters (layer violation)
- Do not put fallback logic inside domain methods
- Do not return provider-native types from public domain methods
- Do not bypass typed exceptions in adapters
- Do not remove `display(obj)` as the single public display entrypoint

If these rules hold, the system scales cleanly as more providers are added.

---

## 13) Quick reference imports

```python
from finpipe.fundamentals import getFinancials, getMarketData, getFiling, getDerived, getCompany
from finpipe.core.chains import FUNDAMENTALS_STATEMENTS
from finpipe.core.result import Ok, Err
from finpipe.displays import display
```

---

If you only remember one thing: **domain methods call chains; chains call providers; display is separate and uses one `display(obj)` function.**

