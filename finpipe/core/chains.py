"""Pre-wired fallback chains (the README's ASCII fallback tables, as code).

Domain modules import chains from here — they never import providers directly.
Each chain is a module-level constant so it is cheap to reuse and easy to inspect.

Add a new provider to a category in one place: append a step here.
"""

from __future__ import annotations
from datetime import timedelta
from finpipe.providers import sec_edgar_adapter
from .fallback import FallbackChain


#==============================================
#FUNDAMENTALS STATEMENTS
#==============================================

#Paradeigma:
# ── financials/statements.py ──────────────────────────────────────────────
FUNDAMENTALS_STATEMENTS = FallbackChain(
    name="fundamentals.financials", 
    steps=(
        ("sec_edgar", sec_edgar_adapter.getFinancials), #Chain Fallback
        #("simfin", simfin_adapter.getFinancials), h opoiodipote allo adapter-provider theleis 
        # pane me thn opoia seira theloume na kanoume chain
    ),  
    cache_ttl=timedelta(hours=24), #Cache for 24 hours(avoiding unnecessary API calls)
)

__all__ = ["FUNDAMENTALS_STATEMENTS"]
