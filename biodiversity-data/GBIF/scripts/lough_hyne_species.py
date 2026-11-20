"""
Write reports/lough_hyne_species.md: the underwater (marine) species that anyone
has recorded at Lough Hyne, Co. Cork, according to GBIF, and the records behind
them.

Unlike the other reports this is not limited to andreiastra's records: it uses
every dataset on GBIF (iNaturalist, surveys, museum specimens, ...). The filters:

  1. inside LOUGH_HYNE_POLYGON, drawn around the lough
  2. occurrenceStatus = PRESENT (absence records are dropped)
  3. mediaType = StillImage (the record has a photo)
  4. identified to species
  5. marine species (below), without the groups in NOT_UNDERWATER
  6. copies removed (see without_copies)

GBIF occurrences have no habitat field, so "underwater" comes from the taxon:
a species counts when a GBIF species profile marks it as marine (WoRMS or the
Catalogue of Life). The profiles are fetched once per species and kept in
scripts/.cache/species_profiles.json, because they rarely change.

Usage:
  ../.venv/bin/python scripts/lough_hyne_species.py
"""
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import requests

sys.path.insert(0, os.path.dirname(__file__))
from config import (CACHE_DIR, INATURALIST_DATASET_KEY, LOUGH_HYNE_POLYGON, OCCURRENCE_SEARCH_URL, OUTPUT_DIR,
                    PAGE_SIZE, RECORDED_BY, SPECIES_URL, THROTTLE_S)

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "lough_hyne_species.md")
PROFILE_CACHE = os.path.join(CACHE_DIR, "species_profiles.json")
OCCURRENCE_PAGE = "https://www.gbif.org/occurrence/{}"
WORKERS = 8
THUMB_HEIGHT = 75  # px
# GBIF's image cache resizes any host's photo; the digest is the MD5 of the original URL.
THUMB_URL = "https://api.gbif.org/v1/image/cache/x75/occurrence/{key}/media/{digest}"
# Table groups, from the GBIF classification (phylum, class, order). The first match wins.
GROUPS = [
    ("Nudibranchs", lambda ph, cl, od: od == "Nudibranchia"),
    ("Sea snails and limpets", lambda ph, cl, od: cl == "Gastropoda"),
    ("Bivalves and chitons", lambda ph, cl, od: cl in {"Bivalvia", "Polyplacophora"}),
    ("Sea squirts", lambda ph, cl, od: cl == "Ascidiacea"),
    ("Fish and sharks", lambda ph, cl, od: ph == "Chordata"),
    ("Crustaceans", lambda ph, cl, od: ph == "Arthropoda"),
    ("Anemones and corals", lambda ph, cl, od: cl == "Anthozoa"),
    ("Jellyfish, hydroids and comb jellies", lambda ph, cl, od: ph in {"Cnidaria", "Ctenophora"}),
    ("Starfish, urchins and sea cucumbers", lambda ph, cl, od: ph == "Echinodermata"),
    ("Sponges", lambda ph, cl, od: ph == "Porifera"),
    ("Worms", lambda ph, cl, od: ph in {"Annelida", "Nemertea", "Platyhelminthes"}),
    ("Sea mats", lambda ph, cl, od: ph == "Bryozoa"),
    ("Seaweeds", lambda ph, cl, od: ph == "Ochrophyta"),
]
OTHER = "Other"


def anchor(group):
    """Link target for a group's heading row, e.g. "fish-and-sharks"."""
    return re.sub(r"[^a-z0-9]+", "-", group.lower()).strip("-")


def group_of(o):
    """Table group of an occurrence, from its GBIF classification."""
    ph, cl, od = o.get("phylum"), o.get("class"), o.get("order")
    return next((name for name, test in GROUPS if test(ph, cl, od)), OTHER)


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


def fetch_occurrences():
    """Present occurrences with a photo inside the polygon, from every dataset."""
    params = {"geometry": LOUGH_HYNE_POLYGON, "occurrenceStatus": "PRESENT",
              "mediaType": "StillImage", "limit": PAGE_SIZE}
    results, offset = [], 0
    while True:
        data = get(OCCURRENCE_SEARCH_URL, **params, offset=offset)
        results.extend(data["results"])
        if data["endOfRecords"]:
            return results
        offset += PAGE_SIZE
        time.sleep(THROTTLE_S)


def fetch_profile(key):
    """Taxon details and whether any source calls the species marine."""
    taxon = get(f"{SPECIES_URL}/{key}")
    profiles = get(f"{SPECIES_URL}/{key}/speciesProfiles", limit=100).get("results", [])
    english = [v["vernacularName"] for v in
               get(f"{SPECIES_URL}/{key}/vernacularNames", limit=200).get("results", [])
               if v.get("language") == "eng" and v.get("vernacularName")]
    return {
        "common": english[0] if english else None,
        "name": taxon.get("species") or taxon.get("canonicalName") or taxon.get("scientificName"),
        "group": taxon.get("class") or taxon.get("order") or taxon.get("phylum") or taxon.get("kingdom") or "—",
        "marine": any(p.get("marine") for p in profiles),
    }


def profiles_for(keys):
    profiles = {}
    if os.path.exists(PROFILE_CACHE):
        with open(PROFILE_CACHE, encoding="utf-8") as f:
            profiles = json.load(f)
    todo = [k for k in keys if "common" not in profiles.get(k, {})]
    if todo:
        print(f"Fetching species profiles for {len(todo)} of {len(keys)} species…")
        with ThreadPoolExecutor(WORKERS) as pool:
            for k, p in zip(todo, pool.map(fetch_profile, todo)):
                profiles[k] = p
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(PROFILE_CACHE, "w", encoding="utf-8") as f:
            json.dump(profiles, f, ensure_ascii=False)
    return {k: profiles[k] for k in keys}


def thumbnail(o):
    """GBIF's small cached thumbnail of the first photo, linked to the occurrence page, or "—"."""
    for m in o.get("media") or []:
        if m.get("type") == "StillImage" and m.get("identifier"):
            digest = hashlib.md5(m["identifier"].encode()).hexdigest()
            thumb = THUMB_URL.format(key=o["key"], digest=digest)
            if plain(o.get("recordedBy")) == plain(RECORDED_BY):  # my record: outlined in blue
                return (f'<a href="{OCCURRENCE_PAGE.format(o["key"])}"><img src="{thumb}" height="{THUMB_HEIGHT}" '
                        f'style="border: 3px solid #0f62fe" alt="my photo"></a>')
            return f'<a href="{OCCURRENCE_PAGE.format(o["key"])}"><img src="{thumb}" height="{THUMB_HEIGHT}" alt="photo"></a>'
    return "—"


def plain(text):
    """Lower case without accents, so "Éabha" and "Eabha" match."""
    text = unicodedata.normalize("NFKD", text or "")
    return "".join(c for c in text if not unicodedata.combining(c)).lower().strip()


def without_copies(records):
    """Drop records that copy an iNaturalist observation into another dataset.

    Explore Your Shore (and similar) republish a recorder's iNaturalist photos as
    records of their own, with a different dataset, catalogue number and
    coordinates, so GBIF shows the same photo twice. The records match on species,
    recorder and day. Within such a group, each iNaturalist record cancels one
    record from another dataset; any extra ones stay, as they may be other photos.
    Records with no recorder or date are never treated as copies.
    """
    groups = defaultdict(list)
    for o in records:
        groups[(o["speciesKey"], plain(o.get("recordedBy")), (o.get("eventDate") or "")[:10])].append(o)
    kept, dropped = [], 0
    for (_, who, day), recs in groups.items():
        inat = [o for o in recs if o.get("datasetKey") == INATURALIST_DATASET_KEY]
        other = [o for o in recs if o.get("datasetKey") != INATURALIST_DATASET_KEY]
        if who and day and inat:
            copies = min(len(inat), len(other))
            dropped += copies
            other = other[copies:]
        kept += inat + other
    return kept, dropped


def render(occurrences, profiles):
    """Markdown for the records that pass every filter. `occurrences` all have a photo."""
    keys = {str(o["speciesKey"]): o for o in occurrences if o.get("speciesKey")}
    marine = {k for k, p in profiles.items() if p["marine"] and p["group"] not in NOT_UNDERWATER}
    records = [o for o in occurrences if str(o.get("speciesKey")) in marine]
    records, copies = without_copies(records)
    records.sort(key=lambda o: o.get("eventDate") or "", reverse=True)  # newest photo first

    mine = sum(plain(o.get("recordedBy")) == plain(RECORDED_BY) for o in records)
    by_species = {}
    for o in records:
        by_species.setdefault(str(o["speciesKey"]), []).append(o)
    my_species = len({k for k, recs in by_species.items()
                      if any(plain(o.get("recordedBy")) == plain(RECORDED_BY) for o in recs)})

    def label(k):
        p = profiles[k]
        return p["common"] or f"*{p['name']}*"

    lines = [
        "# Underwater species at Lough Hyne on GBIF\n",
        "> Generated by `scripts/lough_hyne_species.py` from live GBIF data. Every recorder and dataset, "
        "not only `andreiastra`.\n",
        f"**{len(by_species)}** marine species from **{len(records)}** records. "
        f"{len(occurrences)} present occurrences with a photo lie in the polygon, "
        f"covering {len(keys)} species of any habitat. {copies} copies of iNaturalist records were left out.\n",
        "## Filters applied\n",
        f"1. Inside the polygon around Lough Hyne (51°30'10.5\"N 9°18'10.4\"W): `geometry={LOUGH_HYNE_POLYGON}`",
        "2. Occurrence is present, not an absence record: `occurrenceStatus=PRESENT`",
        "3. The record has a photo: `mediaType=StillImage`",
        "4. Identified to species: has a `speciesKey`",
        f"5. Marine species, leaving out {' and '.join(sorted(NOT_UNDERWATER))} (seabirds and coastal plants): "
        "a GBIF species profile (WoRMS or Catalogue of Life) marks it as marine",
        "6. No copies: a record from another dataset (such as Explore Your Shore) is left out when an iNaturalist "
        "record has the same species, recorder and date, because it republishes the same photo\n",
        "Filters 1 to 3 can be repeated on [gbif.org/occurrence/search](https://www.gbif.org/occurrence/search) "
        "(Location, Geometry; Occurrence status, Present; Media type, Still image). "
        "The website can't filter by marine species, so filters 4 to 6 are applied by the script.\n",
    ]

    grouped = {}
    for k, recs in by_species.items():
        grouped.setdefault(group_of(recs[0]), []).append(k)

    ordered = sorted(grouped.items(), key=lambda kv: (kv[0] == OTHER, -len(kv[1]), kv[0]))

    lines += ["\n## Species by group\n", f"**{len(by_species)}** species in {len(grouped)} groups.\n",
              "| Group | Species |", "|---|--:|"]
    lines += [f"| [{group}](#{anchor(group)}) | {len(keys)} |" for group, keys in ordered]

    lines += ["\n## Species\n", f"**{len(by_species)}** species (rows), **{len(records)}** photos, "
              f"**{mine}** of them yours (outlined in blue), "
              f"in **{my_species}** species whose name is also in blue.\n",
              "| Common name | Photos |", "|---|---|"]
    for group, keys in ordered:
        # <br> above and below gives the heading row room to breathe
        lines.append(f'| <a id="{anchor(group)}"></a><br>**{group}** ({len(keys)})<br>&nbsp; | |')
        for k in sorted(keys, key=lambda k: label(k).strip("*").lower()):
            name = label(k)
            if any(plain(o.get("recordedBy")) == plain(RECORDED_BY) for o in by_species[k]):
                name = f'<span style="color: #0f62fe">**{name}**</span>'  # a species I recorded
            lines.append(f"| {name} | {' '.join(thumbnail(o) for o in by_species[k])} |")

    lines.append(
        "\nThe marine flag comes from taxon profiles, so a marine species seen on the shore or from a boat "
        "counts too, and a freshwater or terrestrial species never appears. A species with no marine value "
        "in its GBIF profile (some seaweeds) is left out. The common name is the first English name GBIF "
        "holds for the species; the scientific name is shown in italics where there is none. Species are grouped by their GBIF "
        "classification, with the number of species in brackets. There is one thumbnail per record, newest first, "
        "and each opens its occurrence on GBIF. Records carry a coordinate uncertainty, so some may "
        "come from the surroundings of the lough.")
    return "\n".join(lines) + "\n", len(records), len(by_species)


def main():
    occurrences = fetch_occurrences()
    profiles = profiles_for(sorted({str(o["speciesKey"]) for o in occurrences if o.get("speciesKey")}))
    text, records, species = render(occurrences, profiles)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved {species} marine species from {records} records → {os.path.normpath(OUTPUT_FILE)}")


if __name__ == "__main__":
    main()
