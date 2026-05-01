"""Technicals — one submodule per category.

Categories map to provider stacks:

- ohlcv_historical — yfinance, finnhub, alpha_vantage, polygon, ccxt, tardis
- orderbook — crypto: ccxt, tardis | stocks/futures: polygon
- tick_trades — crypto: ccxt, tardis | stocks: polygon, ib_insync
- volume — crypto: ccxt (per exchange), coingecko (agg/dominance), tardis (tick);
  stocks: yfinance, polygon, finnhub, ib_insync
- streaming — finnhub, ccxt_pro (subset of venues), ib_insync
"""



__all__ = [

]
