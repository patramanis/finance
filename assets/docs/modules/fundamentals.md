# finpipe.fundamentals

Five grouping functions. Each returns a handle; call methods on it. Methods
return `pd.DataFrame` or `dict`. Provider-native objects never surface.

**Current state:** every method body raises `NotImplementedError`. The classes
and signatures are fixed; wiring is the open work.

## Public API

```python
from finpipe.fundamentals import (
    getFinancials,   # what the company reports
    getMarketData,   # what the market observes
    getFiling,       # raw SEC EDGAR access
    getDerived,      # computed-only (no fetching)
    getCompany,      # static / slow-changing context
)
```

## Call surface (copy-paste reference)

### `getFinancials(ticker)`

```python
getFinancials("AAPL").incomeStatement()
getFinancials("AAPL").balanceSheet()
getFinancials("AAPL").cashFlow()

getFinancials("AAPL").ratios.roe()
getFinancials("AAPL").ratios.roa()
getFinancials("AAPL").ratios.margins()
getFinancials("AAPL").ratios.all()

getFinancials("AAPL").valuation.pe()
getFinancials("AAPL").valuation.pb()
getFinancials("AAPL").valuation.ps()

getFinancials("AAPL").earnings.actual()
getFinancials("AAPL").earnings.guidance()
getFinancials("AAPL").earnings.nextDate()

getFinancials("AAPL").dividends.history()
getFinancials("AAPL").dividends.payoutRatio()

getFinancials("AAPL").segments.bySegment()
getFinancials("AAPL").segments.byGeography()

getFinancials("AAPL").ownership.insiderTrades()    # Form 4
getFinancials("AAPL").ownership.institutional()    # 13F

getFinancials("AAPL").corporateActions.splits()
getFinancials("AAPL").corporateActions.buybacks()
getFinancials("AAPL").corporateActions.mergers()
```

### `getMarketData(ticker)`

```python
getMarketData("AAPL").price.history(period="1y", interval="1d")
getMarketData("AAPL").price.current()
getMarketData("AAPL").shares.outstanding()
getMarketData("AAPL").shares.shortInterest()
getMarketData("AAPL").risk.beta()
getMarketData("AAPL").risk.realizedVol(window=30)
```

### `getFiling(ticker, form=None)` — flat API

```python
getFiling("AAPL").metadata()
getFiling("AAPL").latest(form="10-K")
getFiling("AAPL").search(form="10-K", date_range=("2020", "2024"))
getFiling("AAPL").statements(form="10-K")
getFiling("AAPL").notes(form="10-K", note="leases")
getFiling("AAPL").section(form="10-K", part="mda")   # returns str, unstructured
getFiling("AAPL").get(form="8-K")                    # raw edgartools Filing
getFiling("AAPL").download(form="10-K", format="pdf")
```

Valid `note` values: `leases`, `goodwill`, `taxes`, `debt`, `stock_based_comp`, `eps`.
Valid `part` values: `mda`, `risk_factors`, `business`, `legal_proceedings`, `cybersecurity`, `exec_comp`, `properties`.

### `getDerived(ticker)` — flat, no fetching

```python
getDerived("AAPL").netDebt()
getDerived("AAPL").investedCapital()
getDerived("AAPL").enterpriseValue()
getDerived("AAPL").evEbitda()
getDerived("AAPL").wacc()
getDerived("AAPL").roic()
getDerived("AAPL").eva()
```

Dependency chain:

```
price + shares          → marketCap
statements              → netDebt → investedCapital
beta + riskFree         → wacc
investedCapital + wacc  → roic → eva
marketCap + netDebt     → enterpriseValue → evEbitda
```

### `getCompany(ticker)`

```python
getCompany("AAPL").profile()             # dict
getCompany("AAPL").description()         # str
getCompany("AAPL").analyst.estimates()
getCompany("AAPL").analyst.priceTarget()
getCompany("AAPL").credit.ratings()
getCompany("AAPL").credit.outlook()
```

`.profile()` dict shape: `ticker`, `sector`, `industry`, `exchange`, `currency`,
`employees`, `hq`, `founded_year`, `website`.

## Exact method contracts (implementation target)

Use this as the source of truth for what each method must do.

### Global rules (apply to every method)

- `ticker` is uppercase symbol input (examples: `AAPL`, `MSFT`).
- Time-series outputs are sorted oldest -> newest unless stated otherwise.
- All numeric values are raw numbers (not formatted strings with commas).
- Currency defaults to issuer reporting currency unless method explicitly market-priced.
- Missing fields are `NaN`/`None`; methods should not silently drop rows to hide gaps.
- On total provider failure: raise a clear runtime error at domain layer (after `Err` from chain).

### `getFinancials(ticker)`

| Method | Return type | Exact behavior |
|---|---|---|
| `incomeStatement()` | `pd.DataFrame` | Consolidated income statement by period. Required columns: `period_end`, `revenue`, `gross_profit`, `operating_income`, `net_income`, `eps_basic`, `eps_diluted`. |
| `balanceSheet()` | `pd.DataFrame` | Consolidated balance sheet by period. Required columns: `period_end`, `total_assets`, `total_liabilities`, `total_equity`, `cash_and_equivalents`, `current_assets`, `current_liabilities`. |
| `cashFlow()` | `pd.DataFrame` | Consolidated cash flow by period. Required columns: `period_end`, `operating_cash_flow`, `investing_cash_flow`, `financing_cash_flow`, `capex`, `free_cash_flow` (if not supplied, compute when possible). |
| `ratios.roe()` | `pd.DataFrame` | Period series with `period_end`, `roe` as decimal (0.15 = 15%). |
| `ratios.roa()` | `pd.DataFrame` | Period series with `period_end`, `roa` as decimal. |
| `ratios.margins()` | `pd.DataFrame` | Period series with `period_end`, `gross_margin`, `operating_margin`, `net_margin` (decimals). |
| `ratios.all()` | `pd.DataFrame` | Wide table combining all ratio outputs keyed by `period_end`. |
| `valuation.pe()` | `pd.DataFrame` | Valuation time series with `date`, `pe`. |
| `valuation.pb()` | `pd.DataFrame` | Valuation time series with `date`, `pb`. |
| `valuation.ps()` | `pd.DataFrame` | Valuation time series with `date`, `ps`. |
| `earnings.actual()` | `pd.DataFrame` | Earnings history with `period_end`, `eps_actual`, optional `revenue_actual`. |
| `earnings.guidance()` | `pd.DataFrame` | Guidance records with `as_of`, `period`, `metric`, `guidance_value`, optional low/high fields. |
| `earnings.nextDate()` | `dict` | Keys: `ticker`, `next_earnings_date`, optional `time_of_day`, `source`. |
| `dividends.history()` | `pd.DataFrame` | Dividend events with `ex_date`, `pay_date` (if available), `dividend_per_share`. |
| `dividends.payoutRatio()` | `pd.DataFrame` | Period series with `period_end`, `payout_ratio` (decimal). |
| `segments.bySegment()` | `pd.DataFrame` | Segment breakdown rows with `period_end`, `segment`, `value`. |
| `segments.byGeography()` | `pd.DataFrame` | Geography breakdown rows with `period_end`, `region`, `value`. |
| `ownership.insiderTrades()` | `pd.DataFrame` | Form 4 style trades with `filed_at`, `insider_name`, `transaction_type`, `shares`, `price` (if available). |
| `ownership.institutional()` | `pd.DataFrame` | Institutional holdings snapshots with `as_of`, `institution`, `shares`, optional `value`. |
| `corporateActions.splits()` | `pd.DataFrame` | Split events with `date`, `from_factor`, `to_factor` (or `ratio`). |
| `corporateActions.buybacks()` | `pd.DataFrame` | Buyback disclosures with `period_end`, `shares_repurchased` (or normalized alias + source raw column), optional spend amount. |
| `corporateActions.mergers()` | `pd.DataFrame` | Merger/acquisition events with `announced_at`, `counterparty`, `status`, optional value fields. |

### `getMarketData(ticker)`

| Method | Return type | Exact behavior |
|---|---|---|
| `price.history(period="1y", interval="1d")` | `pd.DataFrame` | OHLCV history. Required columns: `timestamp`, `open`, `high`, `low`, `close`, `volume`; timezone-aware timestamp when source supports it. |
| `price.current()` | `dict` | Keys: `ticker`, `price`, `as_of`, optional `currency`, `source`. |
| `shares.outstanding()` | `pd.DataFrame` | Shares history with `as_of`, `shares_outstanding`. |
| `shares.shortInterest()` | `pd.DataFrame` | Short-interest history with `as_of`, `short_shares`, optional `days_to_cover`, `short_percent_float`. |
| `risk.beta()` | `dict` | Keys: `ticker`, `beta`, optional `benchmark`, `lookback`. |
| `risk.realizedVol(window=30)` | `pd.DataFrame` | Realized volatility series computed from returns. Columns: `date`, `realized_vol`; annualization documented in method docstring when implemented. |

### `getFiling(ticker, form=None)`

| Method | Return type | Exact behavior |
|---|---|---|
| `metadata()` | `dict` | Filing metadata summary. Keys include `ticker`, `company_name`, `cik`, and available filing forms/count hints when source provides them. |
| `latest(form="10-K")` | `dict` | Latest filing metadata for form. Keys: `form`, `filed_at`, `accession_number`, optional links. |
| `search(form="10-K", date_range=(...))` | `pd.DataFrame` | Filing list filtered by form/date. Columns: `form`, `filed_at`, `accession_number`, `primary_doc`, optional url fields. |
| `statements(form="10-K")` | `pd.DataFrame` | Structured statement rows extracted from filing (normalized statement-like table). |
| `notes(form="10-K", note="leases")` | `pd.DataFrame` | Structured rows for requested note type. Includes `period_end` where available. |
| `section(form="10-K", part="mda")` | `str` | Raw narrative section text (unstructured prose). |
| `get(form="8-K")` | `dict` | Provider-neutral raw filing envelope (must not leak provider object type publicly). |
| `download(form="10-K", format="pdf")` | `dict` | Download result metadata. Keys: `path` or `url`, `format`, `form`, `status`. |

### `getDerived(ticker)` (compute-only)

| Method | Return type | Exact behavior |
|---|---|---|
| `netDebt()` | `pd.DataFrame` | Derived series: `period_end`, `net_debt = total_debt - cash_and_equivalents`. |
| `investedCapital()` | `pd.DataFrame` | Derived series: `period_end`, `invested_capital` using normalized balance-sheet inputs. |
| `enterpriseValue()` | `pd.DataFrame` | Derived series: `date`, `enterprise_value = market_cap + net_debt` (adjustments documented in code if added). |
| `evEbitda()` | `pd.DataFrame` | Derived series: `date`, `ev_ebitda` using EV and EBITDA inputs aligned by period/date rule. |
| `wacc()` | `pd.DataFrame` | Derived series: `date`, `wacc` (decimal). Method docstring must state assumptions (risk-free source, ERP, tax handling). |
| `roic()` | `pd.DataFrame` | Derived series: `period_end`, `roic` (decimal) from NOPAT and invested capital. |
| `eva()` | `pd.DataFrame` | Derived series: `period_end`, `eva = nopat - (invested_capital * wacc)`. |

### `getCompany(ticker)`

| Method | Return type | Exact behavior |
|---|---|---|
| `profile()` | `dict` | Required keys: `ticker`, `sector`, `industry`, `exchange`, `currency`, `employees`, `hq`, `founded_year`, `website`. |
| `description()` | `str` | Long-form company description/business summary text. |
| `analyst.estimates()` | `pd.DataFrame` | Analyst estimate history/consensus rows. Columns include `as_of`, `metric`, `estimate`, optional low/high/num_analysts. |
| `analyst.priceTarget()` | `dict` | Keys: `ticker`, `target_mean`, optional `target_low`, `target_high`, `as_of`, `num_analysts`. |
| `credit.ratings()` | `pd.DataFrame` | Credit ratings rows with `as_of`, `agency`, `rating`, optional watch fields. |
| `credit.outlook()` | `pd.DataFrame` or `dict` | Credit outlook state (`positive/negative/stable` etc.) with `as_of` and `agency` when available. |

## Invariants

1. **Nothing in `derived/` fetches.** It consumes `getFinancials` / `getMarketData` and computes locally.
2. **`getFiling` is raw; `getFinancials` is clean.** They are not duplicates — different layers.
3. **`getMarketData` observes, `getFinancials` reports.** Never mix the two sources in one module.
4. **Return `pd.DataFrame` or `dict` only.** No provider objects, no EdgarTools types, no yfinance `Ticker`.
5. **`getFiling().section()` returns `str`.** Sections are prose, not tables.

## Implementing a stub method

Pattern — never import a provider directly from a domain method; always go
through a `FallbackChain` in `finpipe.core.chains`.

```python
# finpipe/fundamentals/financials/statements.py
from finpipe.core.chains import FUNDAMENTALS_STATEMENTS
from finpipe.core.result import Err


class Statements:
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def incomeStatement(self):
        res = FUNDAMENTALS_STATEMENTS.run(self.ticker)
        if isinstance(res, Err):
            raise RuntimeError(
                f"No provider served financials for {self.ticker}: {res.reason}"
            )
        return _normalizeIncome(res.value)   # return DataFrame
```

Normalization helpers (turning a vendor object into a uniform DataFrame) belong
in the domain layer (e.g. `fundamentals/_normalize/`), **not** in the adapter.

## When to add a new chain vs reuse one

- Same data category, new vendor → append a step to the existing chain in `core/chains.py`.
- New data category (e.g. "dividends" distinct from "statements") → new chain constant in `core/chains.py`, domain method runs that one.

See [CORE](CORE.md) for chain mechanics and [PROVIDERS](PROVIDERS.md) for how to write an adapter.

## Folder layout

Full scaffold layout is in [ARCHITECTURE.md](../ARCHITECTURE.md) under
"fundamentals/ — domain API surface".
