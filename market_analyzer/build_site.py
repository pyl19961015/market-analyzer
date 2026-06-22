"""Sync generated reports into site/data/ for the static dashboard."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from market_analyzer.report import REPORTS_DIR

SITE_DIR = Path(__file__).resolve().parent.parent / "site"
SITE_DATA_DIR = SITE_DIR / "data"


def sync_site_data() -> None:
    SITE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    dates = []
    for path in sorted(REPORTS_DIR.glob("*.json")):
        shutil.copy(path, SITE_DATA_DIR / path.name)
        dates.append(path.stem)
    dates.sort(reverse=True)
    (SITE_DATA_DIR / "index.json").write_text(json.dumps(dates, ensure_ascii=False))


if __name__ == "__main__":
    sync_site_data()
    print(f"Synced {len(list(REPORTS_DIR.glob('*.json')))} report(s) to {SITE_DATA_DIR}")
