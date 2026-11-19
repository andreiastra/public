"""
Fetch all iNaturalist observations for andreiastra and save to scripts/.cache/observations.json.

The file is a git-ignored snapshot and goes stale as soon as new observations are
uploaded.  Never read it directly: call refresh() (or run this script), which
always re-fetches from the API, rewrites the file, and returns the observations.

    from fetch_observations import refresh
    observations = refresh()

In-process cache: refresh() also stores the observations in memory, and the other
scripts read them through generate_location_ratings.fetch_all_observations(), so
run_all.py downloads them once for the whole run.  Use the helpers below to take
the Ireland, nudibranch and bird subsets from that list instead of calling the API.

Usage:
  ../.venv/bin/python scripts/fetch_observations.py
"""
import json
import os
import sys
import time

import requests

sys.path.insert(0, os.path.dirname(__file__))
from config import (
    AVES_TAXON_ID,
    CACHE_DIR,
    IRELAND_PLACE_ID,
    NUDIBRANCHIA_TAXON_ID,
    OBSERVATIONS_URL as BASE_URL,
    PER_PAGE,
    USER_ID,
)

OUTPUT   = os.path.join(CACHE_DIR, "observations.json")

_cache = None  # observations downloaded earlier in this process, or None


def cached():
    """Return the observations downloaded earlier in this process, or None."""
    return _cache


def set_cache(observations):
    global _cache
    _cache = observations


def in_ireland(observations):
    """Observations in Ireland (same result as the API's place_id filter)."""
    return [o for o in observations if IRELAND_PLACE_ID in (o.get("place_ids") or [])]


def of_taxon(observations, taxon_id):
    """Observations of taxon_id or any descendant (same as the API's taxon_id filter)."""
    return [o for o in observations
            if taxon_id in ((o.get("taxon") or {}).get("ancestor_ids") or [])]


def nudibranchs_in_ireland(observations):
    return of_taxon(in_ireland(observations), NUDIBRANCHIA_TAXON_ID)


def birds_in_ireland(observations):
    return of_taxon(in_ireland(observations), AVES_TAXON_ID)


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
    """Fetch all observations from the API, rewrite OUTPUT, cache and return them."""
    observations = fetch_all()
    set_cache(observations)
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
