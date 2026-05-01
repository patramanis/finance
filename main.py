#==============================================
#FUNDAMENTALS CALLS 
#==============================================
from finpipe.fundamentals import *
from finpipe.displays import display

ticker = "AAPL"



'''
# ── getFinancials ──────────────────────────────────────────────
getFinancials(ticker).incomeStatement()
getFinancials(ticker).balanceSheet()
getFinancials(ticker).cashFlow()
getFinancials(ticker).ratios.roe()
getFinancials(ticker).ratios.roa()
getFinancials(ticker).ratios.margins()
getFinancials(ticker).ratios.all()
getFinancials(ticker).valuation.pe()
getFinancials(ticker).valuation.pb()
getFinancials(ticker).valuation.ps()
getFinancials(ticker).earnings.actual()
getFinancials(ticker).earnings.guidance()
getFinancials(ticker).earnings.nextDate()
getFinancials(ticker).dividends.history()
getFinancials(ticker).dividends.payoutRatio()
getFinancials(ticker).segments.bySegment()
getFinancials(ticker).segments.byGeography()
getFinancials(ticker).ownership.insiderTrades()
getFinancials(ticker).ownership.institutional()
getFinancials(ticker).corporateActions.splits()
getFinancials(ticker).corporateActions.buybacks()
getFinancials(ticker).corporateActions.mergers()

# ── getMarketData ──────────────────────────────────────────────
getMarketData(ticker).price.history(period="1y")
getMarketData(ticker).price.current()
getMarketData(ticker).shares.outstanding()
getMarketData(ticker).shares.shortInterest()
getMarketData(ticker).risk.beta()
getMarketData(ticker).risk.realizedVol()

# ── getFiling ──────────────────────────────────────────────────
getFiling(ticker).metadata()
getFiling(ticker).latest(form="10-K")
getFiling(ticker).search(form="10-K", date_range=("2020", "2024"))
getFiling(ticker).statements(form="10-K")
getFiling(ticker).notes(form="10-K", note="leases")
getFiling(ticker).notes(form="10-K", note="goodwill")
getFiling(ticker).notes(form="10-K", note="taxes")
getFiling(ticker).notes(form="10-K", note="debt")
getFiling(ticker).notes(form="10-K", note="eps")
getFiling(ticker).section(form="10-K", part="mda")
getFiling(ticker).section(form="10-K", part="risk_factors")
getFiling(ticker).section(form="10-K", part="business")
getFiling(ticker).section(form="10-K", part="legal_proceedings")
getFiling(ticker).section(form="10-K", part="cybersecurity")
getFiling(ticker).section(form="10-K", part="exec_comp")
getFiling(ticker).get(form="10-K")
getFiling(ticker).get(form="10-Q")
getFiling(ticker).get(form="8-K")
getFiling(ticker).get(form="form4")
getFiling(ticker).get(form="13F")
getFiling(ticker).download(form="10-K", format="pdf")
getFiling(ticker).download(form="10-K", format="html")

# ── getDerived ─────────────────────────────────────────────────
getDerived(ticker).netDebt()
getDerived(ticker).investedCapital()
getDerived(ticker).enterpriseValue()
getDerived(ticker).evEbitda()
getDerived(ticker).wacc()
getDerived(ticker).roic()
getDerived(ticker).eva()

# ── getCompany ─────────────────────────────────────────────────
getCompany(ticker).profile()
getCompany(ticker).description()
getCompany(ticker).analyst.estimates()
getCompany(ticker).analyst.priceTarget()
getCompany(ticker).credit.ratings()
getCompany(ticker).credit.outlook()

# Generic one-function display usage:
# display(getCompany(ticker).profile())
# display(getCompany(ticker).description())
'''










#==============================================
#TECHNICALS CALLS 
#==============================================

#==============================================
#MACRO CALLS 
#==============================================

#==============================================
#SENTIMENT CALLS 
#==============================================

#==============================================
#DERIVATIVES CALLS 
#==============================================
