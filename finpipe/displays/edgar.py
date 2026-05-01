"""Pretty-print EdgarTools ``Financials`` via Rich.

Pure renderer: takes an already-fetched ``Financials`` object. Does not call
the network or choose a provider — that is the fallback chain's job.
"""

from __future__ import annotations

from typing import Literal

from edgar.financials import Financials
from rich.console import Console

StatementKind = Literal["income", "balance", "cashflow", "equity", "comprehensive"]


def renderStatement(
    financials: Financials,
    kind: StatementKind,
    *,
    console: Console | None = None,
    headlines: bool = False,
) -> None:
    """Render one statement. ``headlines`` adds scalar summaries for ``income`` / ``balance``."""
    c = console or Console()
    match kind:
        case "income":
            c.print(financials.income_statement())
            if headlines:
                c.print()
                c.print("Headline (USD)")
                c.print(f"  Revenue:          {financials.get_revenue()}")
                c.print(f"  Net income:       {financials.get_net_income()}")
                c.print(f"  Operating income: {financials.get_operating_income()}")
        case "balance":
            c.print(financials.balance_sheet())
            if headlines:
                c.print()
                c.print("Headline (USD)")
                c.print(f"  Total assets:        {financials.get_total_assets()}")
                c.print(f"  Total liabilities:   {financials.get_total_liabilities()}")
                c.print(f"  Stockholders equity: {financials.get_stockholders_equity()}")
                c.print(f"  Current assets:      {financials.get_current_assets()}")
                c.print(f"  Current liabilities: {financials.get_current_liabilities()}")
        case "cashflow":
            c.print(financials.cashflow_statement())
        case "equity":
            c.print(financials.statement_of_equity())
        case "comprehensive":
            c.print(financials.comprehensive_income())


__all__ = ["StatementKind", "renderStatement"]
