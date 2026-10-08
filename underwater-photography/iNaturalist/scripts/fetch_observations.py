"""
Fetch all iNaturalist observations for andreiastra and save to OUTPUT/observations.json.

The file is a git-ignored snapshot and goes stale as soon as new observations are
uploaded.  Never read it directly: call refresh() (or run this script), which
always re-fetches from the API, rewrites the file, and returns the observations.

    from fetch_observations import refresh
    observations = refresh()

Usage:
  .venv/bin/python scripts/fetch_observations.py
"""
import json
import os
import time

import requests

from config import OBSERVATIONS_URL as BASE_URL, OUTPUT_DIR, PER_PAGE, USER_ID

OUTPUT   = os.path.join(OUTPUT_DIR, "observations.json")


def fetch_all():
    print(f"Fetching observations for '{USER_ID}'…")
    all_obs, page = [], 1
    while True:
        r = requests.get(BASE_URL, params={
            "user_id":  USER_ID,
            "per_page": PER_PAGE,
            "page":     page,
        }, timeout=30)
        r.raise_for_status()
        data    = r.json()
        results = data.get("results", [])
        all_obs.extend(results)
        print(f"  page {page}: {len(results)} obs  (running total: {len(all_obs)})")
        if len(all_obs) >= data.get("total_results", 0):
            break
        page += 1
        time.sleep(1)
    print(f"Total: {len(all_obs)} observations")
    return all_obs


def refresh():
    """Fetch all observations from the API, rewrite OUTPUT, and return them."""
    observations = fetch_all()
    out = os.path.normpath(OUTPUT)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(observations, f, ensure_ascii=False, indent=2)
    print(f"Saved → {out}")
    return observations


def main():
    refresh()


if __name__ == "__main__":
    main()
