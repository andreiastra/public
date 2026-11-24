"""
The marine ("underwater") check shared by the GBIF reports.

GBIF occurrences have no habitat field, so "underwater" comes from the taxon: a species
counts when a GBIF species profile marks it as marine (WoRMS or the Catalogue of Life).
GBIF calls seabirds and coastal plants "marine" too, but they are not underwater, so the
classes in NOT_UNDERWATER are always left out.

    flags = marine_flags(species_keys)                  # {speciesKey: True/False}
    underwater = is_underwater(flags[key], taxon_class)  # flag and not a bird or flowering plant

The flags are fetched once per species and kept in scripts/.cache/marine_flags.json, because
they rarely change. Flags already in the older caches (species_profiles.json and
west_cork_species.json) are copied across, so they are not fetched again. Delete the file to
refresh.
"""
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests

sys.path.insert(0, os.path.dirname(__file__))
from config import CACHE_DIR, SPECIES_URL

FLAG_CACHE = os.path.join(CACHE_DIR, "marine_flags.json")
# Caches from before this module, read once to fill in flags that are already known.
SEED_CACHES = [os.path.join(CACHE_DIR, "species_profiles.json"), os.path.join(CACHE_DIR, "west_cork_species.json")]
WORKERS = 8
SAVE_EVERY = 200  # write the cache after this many lookups, so a stopped run loses little

# GBIF calls seabirds and coastal plants "marine", but they are not underwater.
NOT_UNDERWATER = {"Aves", "Magnoliopsida"}


def get(url, **params):
    for attempt in range(5):
        try:
            r = requests.get(url, params=params, timeout=60)
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            if attempt == 4:
                raise
            time.sleep(2 ** attempt)


def fetch_flag(key):
    """True when any source (WoRMS, Catalogue of Life) calls the species marine."""
    profiles = get(f"{SPECIES_URL}/{key}/speciesProfiles", limit=100).get("results", [])
    return any(p.get("marine") for p in profiles)


def _load(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save(flags):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(FLAG_CACHE, "w", encoding="utf-8") as f:
        json.dump(flags, f)


def marine_flags(keys):
    """{speciesKey: marine} for the given species keys (strings), fetching only the unknown ones."""
    flags = _load(FLAG_CACHE)
    for path in SEED_CACHES:
        for k, entry in _load(path).items():
            if k not in flags and "marine" in entry:
                flags[k] = entry["marine"]
    todo = [k for k in keys if k not in flags]
    if todo:
        print(f"Checking the marine flag of {len(todo)} of {len(keys)} species…", flush=True)
        with ThreadPoolExecutor(WORKERS) as pool:
            for i, (k, flag) in enumerate(zip(todo, pool.map(fetch_flag, todo)), 1):
                flags[k] = flag
                if i % SAVE_EVERY == 0:
                    _save(flags)
                    print(f"  {i}/{len(todo)}", flush=True)
    _save(flags)
    return {k: flags[k] for k in keys}


def is_underwater(flag, taxon_class):
    """A marine species that is not a bird or a flowering plant."""
    return bool(flag) and taxon_class not in NOT_UNDERWATER
