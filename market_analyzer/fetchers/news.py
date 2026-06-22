"""Fetch financial news headlines via RSS (no key required)."""
from __future__ import annotations

import feedparser

from market_analyzer.config import NEWS_FEEDS, NEWS_ITEMS_PER_FEED


def fetch_news(limit_per_feed: int = NEWS_ITEMS_PER_FEED) -> dict[str, list[dict]]:
    results: dict[str, list[dict]] = {}
    for label, url in NEWS_FEEDS.items():
        parsed = feedparser.parse(url)
        if parsed.bozo and not parsed.entries:
            results[label] = [{"error": str(parsed.bozo_exception)}]
            continue
        results[label] = [
            {
                "title": entry.get("title"),
                "link": entry.get("link"),
                "published": entry.get("published", entry.get("updated")),
            }
            for entry in parsed.entries[:limit_per_feed]
        ]
    return results
