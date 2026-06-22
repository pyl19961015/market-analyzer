"""Fetch this week's macro economic events (free, no API key required)."""
from __future__ import annotations

from datetime import date

import requests

from market_analyzer.config import ECONOMIC_CALENDAR_URL, REQUEST_TIMEOUT_SECONDS

# The feed's "impact" field uses these labels.
IMPACT_ORDER = {"High": 0, "Medium": 1, "Low": 2, "Holiday": 3}


def fetch_economic_calendar(country_filter: tuple[str, ...] = ("USD",)) -> list[dict]:
    """Return this week's events for the given country codes, sorted by date then impact."""
    try:
        resp = requests.get(ECONOMIC_CALENDAR_URL, timeout=REQUEST_TIMEOUT_SECONDS)
        resp.raise_for_status()
        events = resp.json()
    except (requests.RequestException, ValueError) as exc:
        return [{"error": str(exc)}]

    filtered = [e for e in events if e.get("country") in country_filter]
    filtered.sort(key=lambda e: (e.get("date", ""), IMPACT_ORDER.get(e.get("impact"), 9)))
    return filtered


def fetch_todays_events(country_filter: tuple[str, ...] = ("USD",)) -> list[dict]:
    today = date.today().isoformat()
    return [e for e in fetch_economic_calendar(country_filter) if e.get("date", "").startswith(today)]
