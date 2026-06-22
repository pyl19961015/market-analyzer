"""Build and persist the daily market-factor report."""
from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

from market_analyzer.config import ECONOMIC_CALENDAR_COUNTRIES
from market_analyzer.fetchers.economic_calendar import fetch_economic_calendar
from market_analyzer.fetchers.fed_policy import fetch_fed_updates
from market_analyzer.fetchers.market_data import fetch_japan_market, fetch_market_sentiment
from market_analyzer.fetchers.news import fetch_news
from market_analyzer.fetchers.rates import fetch_interest_rates
from market_analyzer.fetchers.watchlist import fetch_watchlist

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"


def _with_spread(rates: dict, us_10y: float | None) -> dict:
    jgb = rates["japan"]
    if us_10y is not None and "yield" in jgb:
        rates["spread_10y"] = round(us_10y - jgb["yield"], 2)
    return rates


def build_report() -> dict:
    market_sentiment = fetch_market_sentiment()
    rates = _with_spread(
        fetch_interest_rates(),
        market_sentiment["indices"].get("10Y Treasury Yield", {}).get("last"),
    )
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "date": date.today().isoformat(),
        "market_sentiment": market_sentiment,
        "japan_market": fetch_japan_market(),
        "rates": rates,
        "watchlist": fetch_watchlist(),
        "economic_calendar": fetch_economic_calendar(ECONOMIC_CALENDAR_COUNTRIES),
        "fed_policy": fetch_fed_updates(),
        "news": fetch_news(),
    }


def save_report(report: dict) -> Path:
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / f"{report['date']}.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    return path


def main() -> None:
    from market_analyzer.build_site import sync_site_data

    report = build_report()
    path = save_report(report)
    sync_site_data()
    print(f"Report saved to {path}")


if __name__ == "__main__":
    main()
