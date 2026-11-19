"""
Fetch all GBIF occurrences recorded by Andre Astra from the iNaturalist
research-grade dataset and save them to scripts/.cache/occurrences.json.

The file is a git-ignored snapshot and goes stale: GBIF lags iNaturalist by
days. Never read it directly. Call refresh() (or run this script), which always
re-fetches from the API, rewrites the file, and returns the occurrences.

    from fetch_occurrences import refresh
    occurrences = refresh()

In-process cache: refresh() also stores the occurrences in memory, and the report
scripts read them through cached(), so run_all.py downloads them once.

Usage:
  ../.venv/bin/python scripts/fetch_occurrences.py
  ../.venv/bin/python scripts/fetch_occurrences.py --country IE
"""
import argparse
import json
import os
import sys
import time

import requests

sys.path.insert(0, os.path.dirname(__file__))
from config import (
    CACHE_DIR,
    INATURALIST_DATASET_KEY,
    OCCURRENCE_SEARCH_URL,
    PAGE_SIZE,
    RECORDED_BY,
    THROTTLE_S,
)

OUTPUT = os.path.join(CACHE_DIR, "occurrences.json")

_cache = None  # occurrences downloaded earlier in this process, or None


def cached():
    """Return the occurrences downloaded earlier in this process, or None."""
    return _cache


def fetch_all(country=None):
    params = {
        "recordedBy": RECORDED_BY,
        "datasetKey": INATURALIST_DATASET_KEY,
        "limit":      PAGE_SIZE,
    }
    if country:
        params["country"] = country

    print(f"Fetching GBIF occurrences recorded by '{RECORDED_BY}'" + (f" in {country}" if country else "") + "…")
    results, offset = [], 0
    while True:
        r = requests.get(OCCURRENCE_SEARCH_URL, params={**params, "offset": offset}, timeout=30)
        r.raise_for_status()
        data = r.json()
        results.extend(data.get("results", []))
        print(f"  offset {offset}: {len(data.get('results', []))} records  (running total: {len(results)} of {data.get('count')})")
        if data.get("endOfRecords", True):
            break
        offset += PAGE_SIZE
        time.sleep(THROTTLE_S)
    return results


def refresh(country=None):
    """Fetch the occurrences from the API, rewrite OUTPUT, cache and return them.

    Report scripts call this with no country. A country-filtered fetch is only for
    looking at the data by hand, so it is saved but not kept in the in-process cache.
    """
    global _cache
    occurrences = fetch_all(country)
    if country is None:
        _cache = occurrences
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(occurrences, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(occurrences)} occurrences → {os.path.normpath(OUTPUT)}")
    return occurrences


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--country", help="ISO 3166-1 alpha-2 code, e.g. IE")
    args = parser.parse_args()
    refresh(args.country)


if __name__ == "__main__":
    main()
