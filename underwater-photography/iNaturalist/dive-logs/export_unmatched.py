#!/usr/bin/env python3
"""
export_unmatched.py

Compares iNaturalist observations (fetched live from the API) with Suunto dive dates
from the `workouts/` GPX files.

Outputs `unmatched_observations.json` containing observations that were recorded on days
without a corresponding scuba dive log (e.g. terrestrial birds, insects, or shore observations).
"""

import glob
import json
import os
import re
import requests
import xml.etree.ElementTree as ET
from collections import defaultdict

# Base directory configuration
BASE_DIR = '/Users/astra/github/public/underwater-photography/iNaturalist'
WORKOUTS_DIR = os.path.join(BASE_DIR, 'dive-logs/workouts')
OUTPUT_FILE = os.path.join(BASE_DIR, 'dive-logs/unmatched_observations.json')

USER_ID = "andreiastra"
BASE_URL = "https://api.inaturalist.org/v1/observations"
PER_PAGE = 200


def fetch_all_observations(user_id):
    observations = []
    page = 1
    while True:
        response = requests.get(BASE_URL, params={
            "user_id": user_id,
            "per_page": PER_PAGE,
            "page": page,
        })
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        observations.extend(results)
        print(f"  Fetched page {page} ({len(results)} observations)...")
        if len(observations) >= data.get("total_results", 0):
            break
        page += 1
    return observations

# 1. Collect all unique dive dates (YYYY-MM-DD) from GPX filenames
gpx_files = sorted(glob.glob(os.path.join(WORKOUTS_DIR, '*.gpx')))
dive_dates = set()
for g in gpx_files:
    fname = os.path.basename(g)
    m = re.match(r'(\d{4}-\d{2}-\d{2})_(\d{2}\.\d{2}\.\d{2})', fname)
    if m:
        dive_dates.add(m.group(1))

# 2. Fetch iNaturalist observations live from the API
print(f"Fetching observations for user '{USER_ID}'...")
observations = fetch_all_observations(USER_ID)
print(f"Total observations fetched: {len(observations)}\n")

# 3. Identify observations whose `observed_on` date does not match any dive log date
unmatched_by_date = defaultdict(list)
unmatched_list = []

for obs in observations:
    obs_date = obs.get('observed_on')
    if obs_date not in dive_dates:
        obs_item = {
            'id': obs.get('id'),
            'observed_on': obs_date,
            'time_observed_at': obs.get('time_observed_at'),
            'species_guess': obs.get('species_guess'),
            'taxon_common_name': obs.get('taxon', {}).get('preferred_common_name') if obs.get('taxon') else None,
            'taxon_scientific_name': obs.get('taxon', {}).get('name') if obs.get('taxon') else None,
            'place_guess': obs.get('place_guess'),
            'location': obs.get('location'),
            'uri': obs.get('uri')
        }
        unmatched_list.append(obs_item)
        unmatched_by_date[obs_date].append(obs_item)

# 4. Structure output summary with aggregated counts
summary = {
    'total_observations': len(observations),
    'total_unmatched_observations': len(unmatched_list),
    'unmatched_dates_count': len(unmatched_by_date),
    'unmatched_by_date': {d: unmatched_by_date[d] for d in sorted(unmatched_by_date.keys())},
    'all_unmatched_observations': unmatched_list
}

# Write results to unmatched_observations.json
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(f'Wrote {len(unmatched_list)} unmatched observations across {len(unmatched_by_date)} dates to {OUTPUT_FILE}')
