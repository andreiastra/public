"""
Fetch all iNaturalist observations for andreiastra and save to data/observations.json.

Usage:
  .venv/bin/python scripts/fetch_observations.py
"""
import json
import os
import time

import requests

USER_ID  = "andreiastra"
BASE_URL = "https://api.inaturalist.org/v1/observations"
PER_PAGE = 200
OUTPUT   = os.path.join(os.path.dirname(__file__), "..", "data", "observations.json")


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


def main():
    observations = fetch_all()
    out = os.path.normpath(OUTPUT)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(observations, f, ensure_ascii=False, indent=2)
    print(f"Saved → {out}")


if __name__ == "__main__":
    main()
