"""Fetch US and Japan policy-relevant interest rates (free, no API key required)."""
from __future__ import annotations

import requests

from market_analyzer.config import JGB_YIELD_CSV_URL, NY_FED_RATES_URL, REQUEST_TIMEOUT_SECONDS

_ERA_OFFSETS = {"R": 2018, "H": 1988, "S": 1925}  # Reiwa, Heisei, Showa


def _parse_era_date(value: str) -> str | None:
    era, rest = value[0], value[1:]
    offset = _ERA_OFFSETS.get(era)
    if offset is None:
        return None
    year_str, month_str, day_str = rest.split(".")
    return f"{offset + int(year_str)}-{int(month_str):02d}-{int(day_str):02d}"


def fetch_fed_funds_rate() -> dict:
    """Latest EFFR and FOMC target range from the NY Fed reference rates API."""
    try:
        resp = requests.get(NY_FED_RATES_URL, timeout=REQUEST_TIMEOUT_SECONDS)
        resp.raise_for_status()
        rates = resp.json()["refRates"]
    except (requests.RequestException, ValueError, KeyError) as exc:
        return {"error": str(exc)}

    effr = next((r for r in rates if r.get("type") == "EFFR"), None)
    if not effr:
        return {"error": "EFFR not found in response"}
    return {
        "effr": effr["percentRate"],
        "target_low": effr["targetRateFrom"],
        "target_high": effr["targetRateTo"],
        "as_of": effr["effectiveDate"],
    }


def fetch_jgb_10y_yield() -> dict:
    """Latest 10-year JGB yield from the MOF's current-month CSV."""
    try:
        resp = requests.get(JGB_YIELD_CSV_URL, timeout=REQUEST_TIMEOUT_SECONDS)
        resp.raise_for_status()
        text = resp.content.decode("shift_jis")
    except (requests.RequestException, UnicodeDecodeError) as exc:
        return {"error": str(exc)}

    rows = [line.split(",") for line in text.splitlines() if line.strip()]
    header = next((r for r in rows if r[0] == "基準日"), None)
    if not header:
        return {"error": "header row not found"}
    try:
        col = header.index("10年")
    except ValueError:
        return {"error": "10年 column not found"}

    data_rows = [r for r in rows[rows.index(header) + 1 :] if r[0] and len(r) > col and r[col]]
    if not data_rows:
        return {"error": "no data rows"}

    latest = data_rows[-1]
    as_of = _parse_era_date(latest[0])
    result = {"yield": float(latest[col]), "as_of": as_of}
    if len(data_rows) >= 2:
        result["prev_yield"] = float(data_rows[-2][col])
    return result


def fetch_interest_rates() -> dict:
    return {
        "us": fetch_fed_funds_rate(),
        "japan": fetch_jgb_10y_yield(),
    }
