"""
Fetch all GBIF occurrences recorded by Andre Astra from the iNaturalist
research-grade dataset and save them to scripts/.cache/occurrences.json.

The file is a git-ignored snapshot. GBIF lags iNaturalist by days, so re-run the
script instead of reading an old file.

Usage:
  ../iNaturalist/.venv/bin/python scripts/fetch_occurrences.py
  ../iNaturalist/.venv/bin/python scripts/fetch_occurrences.py --country IE
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


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--country", help="ISO 3166-1 alpha-2 code, e.g. IE")
    args = parser.parse_args()

    occurrences = fetch_all(args.country)
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(occurrences, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(occurrences)} occurrences → {os.path.normpath(OUTPUT)}")


if __name__ == "__main__":
    main()
