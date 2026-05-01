# finpipe — overview

Five domain modules + shared engine + pluggable providers. Free-tier financial
data with automatic fallback between providers.

```
finpipe/
├── core/         orchestration engine (fallback chains, rate limit, cache, config)
├── providers/    one adapter per vendor (yfinance, sec_edgar, finnhub, ...)
├── displays/     pure Rich renderers (no network)
├── fundamentals/ company-reported data, market data, filings, derived, company
├── technicals/   OHLCV, order book, ticks, streaming         (stub)
├── macro/        rates, CPI, GDP, COT, commodities            (stub)
├── derivatives/  options, futures, perps, funding             (stub)
└── sentiment/    news, social, NLP, on-chain                  (stub)
```

## Module status

| Module | Status | Doc |
|--------|--------|-----|
| `core` | implemented | [CORE](CORE.md) |
| `providers` | only `sec_edgar_adapter` wired | [PROVIDERS](PROVIDERS.md) |
| `fundamentals` | API scaffold only, all methods raise `NotImplementedError` | [FUNDAMENTALS](FUNDAMENTALS.md) |
| `technicals`, `macro`, `derivatives`, `sentiment` | empty `__init__.py` only | — |
| `displays` | `display(obj)` router + `edgar.py` specialized renderer | — |

## Naming conventions

- Package / module names: `lowercase` or `snake_case` (PEP 8).
- Class names: `PascalCase`.
- Functions and methods: `camelCase`, `get` prefix for fetchers (project-specific — see [RULES.md](../RULES.md)).
- Module-level constants: `UPPER_SNAKE_CASE`.

Three files currently use `camelCase` filenames (`marketData/`, `corporateActions.py`, `costOfCapital.py`) — known exceptions, open for rename.

## Public surface today

```python
from finpipe.fundamentals import (
    getFinancials, getMarketData, getFiling, getDerived, getCompany,
)

from finpipe.core.chains import FUNDAMENTALS_STATEMENTS   # pre-wired, unconsumed
from finpipe.core.fallback import FallbackChain           # build ad-hoc chains
from finpipe.core.result import Ok, Err                   # result envelopes
from finpipe.core import config, rate_limiter, cache      # engine controls
from finpipe.displays import display                      # one-function display entrypoint
```

## Where to read next

- Architecture (layers, fallback policy, wiring rules): [ARCHITECTURE.md](../ARCHITECTURE.md)
- Naming rules: [RULES.md](../RULES.md)
- Provider inventory + adapter-authoring guide: [PROVIDERS.md](PROVIDERS.md)
- Skills index from project root: [SKILLS.md](../../../SKILLS.md)
