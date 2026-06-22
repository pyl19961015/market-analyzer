"""Fetch broad market indices, sentiment gauges, and sector performance via yfinance."""
from __future__ import annotations

import yfinance as yf

from market_analyzer.config import INDEX_TICKERS, JAPAN_INDEX_TICKERS, SECTOR_ETFS


def _pct_change(history) -> float | None:
    closes = history["Close"].dropna()
    if len(closes) < 2:
        return None
    prev, last = closes.iloc[-2], closes.iloc[-1]
    if prev == 0:
        return None
    return round((last - prev) / prev * 100, 2)


def _last_close(history) -> float | None:
    closes = history["Close"].dropna()
    if closes.empty:
        return None
    return round(float(closes.iloc[-1]), 2)


def fetch_quotes(tickers: dict[str, str]) -> dict[str, dict]:
    """Return {label: {symbol, last, pct_change}} for each ticker, skipping failures."""
    results: dict[str, dict] = {}
    symbols = list(tickers.values())
    data = yf.download(
        symbols, period="5d", interval="1d", group_by="ticker",
        progress=False, auto_adjust=False, threads=True,
    )
    for label, symbol in tickers.items():
        try:
            history = data[symbol]
            results[label] = {
                "symbol": symbol,
                "last": _last_close(history),
                "pct_change": _pct_change(history),
            }
        except (KeyError, IndexError):
            results[label] = {"symbol": symbol, "last": None, "pct_change": None, "error": "no data"}
    return results


def fetch_market_sentiment() -> dict:
    return {
        "indices": fetch_quotes(INDEX_TICKERS),
        "sectors": fetch_quotes(SECTOR_ETFS),
    }


def fetch_japan_market() -> dict:
    return {"indices": fetch_quotes(JAPAN_INDEX_TICKERS)}
