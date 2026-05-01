# finpipe — skills index

Entry point for agents and contributors. Each link below is a focused "how to
work on this part" guide. For architecture and naming rules, jump to the deep
docs at the bottom.

## Modules

| Module | When to read |
|--------|--------------|
| [OVERVIEW](assets/docs/modules/OVERVIEW.md) | Module map, status, conventions. Start here if unfamiliar with the repo. |
| [CORE](assets/docs/modules/CORE.md) | Running / building fallback chains, rate limits, cache, config. |
| [FUNDAMENTALS](assets/docs/modules/FUNDAMENTALS.md) | Using `getFinancials` / `getMarketData` / `getFiling` / `getDerived` / `getCompany`, and turning stub methods into live ones. |
| [PROVIDERS](assets/docs/modules/PROVIDERS.md) | Catalog of which vendor backs each public call + how to write a new adapter. |

## Deep docs

- [assets/docs/ARCHITECTURE.md](assets/docs/ARCHITECTURE.md) — layers, data flow, fallback policy, API-shape rules, build status.
- [assets/docs/RULES.md](assets/docs/RULES.md) — naming + package-layout conventions.

## Quick routing

| Task | Go to |
|------|-------|
| Fetch income / balance / ratios / filings | [FUNDAMENTALS](assets/docs/modules/FUNDAMENTALS.md) |
| Inspect or run a fallback chain | [CORE](assets/docs/modules/CORE.md) |
| Add a new data vendor or look up the catalog | [PROVIDERS](assets/docs/modules/PROVIDERS.md) |
| Understand a layer or dependency rule | [ARCHITECTURE.md](assets/docs/ARCHITECTURE.md) |
| Confirm naming style (`camelCase`, `snake_case`, …) | [RULES.md](assets/docs/RULES.md) |
