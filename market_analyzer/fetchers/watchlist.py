"""Fetch Corning (GLW) plus the stocks most likely to move alongside it."""
from __future__ import annotations

from market_analyzer.config import DEMAND_DRIVER_TICKERS, HOLDINGS, PEER_TICKERS
from market_analyzer.fetchers.market_data import fetch_quotes


def fetch_watchlist() -> dict:
    return {
        "holdings": fetch_quotes(HOLDINGS),
        "demand_drivers": fetch_quotes(DEMAND_DRIVER_TICKERS),
        "peers": fetch_quotes(PEER_TICKERS),
    }
