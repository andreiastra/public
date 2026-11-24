"""
Write reports/cork_underwater.md: an overview of the underwater (marine) species
that anyone has recorded in West Cork and its coastal waters, according to GBIF.

Like lough_hyne_species.py this uses every dataset on GBIF, not only andreiastra's
records, and the same marine filter (marine.py). Unlike it, this script does not download the
records. GBIF counts them per species with the `facet` parameter, so one request
replaces about 80 pages of 300 records. The area is a polygon around West Cork and
its coastal waters (WEST_CORK_POLYGON in config.py). The filters:

  1. inside the West Cork polygon (geometry = WEST_CORK_POLYGON)
  2. occurrenceStatus = PRESENT (absence records are dropped)
  3. mediaType = StillImage (the record has a photo)
  4. identified to species (the facet is speciesKey)
  5. marine species (see marine.py), without the groups in NOT_UNDERWATER

Counts cannot drop copies of iNaturalist records that other datasets republish
(see lough_hyne_species.without_copies; it needs the recorder and date of each
record), so photo counts here can be a little too high. There are no thumbnails.

The marine flags are kept by marine.py in scripts/.cache/marine_flags.json. The names and
Catalogue of Life IDs are fetched once per species and kept in
scripts/.cache/west_cork_species.json.

Usage:
  ../.venv/bin/python scripts/cork_underwater.py
"""
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote_plus

sys.path.insert(0, os.path.dirname(__file__))
from config import (CACHE_DIR, COL_CHECKLIST_KEY, NUDIBRANCHIA_COL_ID, OCCURRENCE_SEARCH_URL, OUTPUT_DIR,
                    RECORDED_BY, SPECIES_MATCH_V2_URL, SPECIES_URL, WEST_CORK_POLYGON)
import lough_hyne_species as lh
from marine import NOT_UNDERWATER, WORKERS, get, is_underwater, marine_flags

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "cork_underwater.md")
SPECIES_CACHE = os.path.join(CACHE_DIR, "west_cork_species.json")
TOP_SPECIES = 25        # rows in the "most photographed" table
FACET_LIMIT = 100000    # facetLimit: more than the species in any area
SAVE_EVERY = 200        # write the cache after this many lookups, so a stop loses little


def facet_counts(**extra):
    """(records, {speciesKey: photos}) for present occurrences with a photo inside the polygon."""
    data = get(OCCURRENCE_SEARCH_URL, geometry=WEST_CORK_POLYGON, occurrenceStatus="PRESENT",
                  mediaType="StillImage", limit=0, facet="speciesKey", facetLimit=FACET_LIMIT,
                  facetMincount=1, **extra)
    counts = {c["name"]: c["count"] for c in data["facets"][0]["counts"]} if data["facets"] else {}
    return data["count"], counts


def load(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save(cache):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(SPECIES_CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False)


def details(key):
    """Name, common name and classification of a species, for the group table."""
    taxon = get(f"{SPECIES_URL}/{key}")
    english = [v["vernacularName"] for v in
               get(f"{SPECIES_URL}/{key}/vernacularNames", limit=200).get("results", [])
               if v.get("language") == "eng" and v.get("vernacularName")]
    return {"marine": True,
            "name": taxon.get("species") or taxon.get("canonicalName") or taxon.get("scientificName"),
            "common": english[0] if english else None,
            "phylum": taxon.get("phylum"), "class": taxon.get("class"), "order": taxon.get("order")}


def col_id(key, cache):
    """Catalogue of Life ID of a species, which is what gbif.org takes as `taxonKey`.
    None when the name has no exact match, so the report shows the name without a link."""
    match = get(SPECIES_MATCH_V2_URL, scientificName=cache[key]["name"], rank="SPECIES",
                   checklistKey=COL_CHECKLIST_KEY)
    if match.get("diagnostics", {}).get("matchType") != "EXACT":
        return {"col": None}
    usage = match.get("acceptedUsage") or match.get("usage") or {}  # a synonym's records sit under the accepted name
    return {"col": usage.get("key")}


def run_batch(label, keys, work, cache):
    """Run `work(key)` for each key on a few threads, merge the results into the cache, and save as it goes."""
    if not keys:
        return
    print(f"{label}: {len(keys)} species", flush=True)
    with ThreadPoolExecutor(WORKERS) as pool:
        for i, (k, result) in enumerate(zip(keys, pool.map(work, keys)), 1):
            cache.setdefault(k, {}).update(result)
            if i % SAVE_EVERY == 0:
                save(cache)
                print(f"  {i}/{len(keys)}", flush=True)
    save(cache)


def marine_species(keys):
    """{speciesKey: details} for the marine species among `keys`."""
    cache = load(SPECIES_CACHE)
    for k, flag in marine_flags(keys).items():
        cache.setdefault(k, {})["marine"] = flag
    run_batch("Fetching names", [k for k in keys if cache[k]["marine"] and "name" not in cache[k]],
              details, cache)
    run_batch("Fetching Catalogue of Life IDs", [k for k in keys if cache[k]["marine"] and "col" not in cache[k]],
              lambda k: col_id(k, cache), cache)
    return {k: cache[k] for k in keys if is_underwater(cache[k]["marine"], cache[k].get("class"))}


SEA_MAMMALS = "Seals, whales and turtles"


def group_of(s):
    """Table group. Mammals and reptiles get their own group; the shared list would call them fish."""
    if s.get("class") in {"Mammalia", "Reptilia", "Testudines"}:
        return SEA_MAMMALS
    return lh.group_of({"phylum": s.get("phylum"), "class": s.get("class"), "order": s.get("order")})


def search_url(*taxa):
    """gbif.org occurrence search with the report's filters for the given species (repeated `taxonKey`
    values are an OR), or None when none of them has a Catalogue of Life ID."""
    ids = list(dict.fromkeys(s["col"] for s in taxa if s.get("col")))  # a synonym and its accepted name share an ID
    if not ids:
        return None
    return ("https://www.gbif.org/occurrence/search?geometry=" + quote_plus(WEST_CORK_POLYGON) +
            "&mediaType=StillImage&occurrenceStatus=DETECTED" + "".join(f"&taxonKey={i}" for i in ids))


def render(records, counts, mine, species):
    """Markdown overview. `counts` and `mine` map a speciesKey to photos; `species` are the marine ones."""
    photos = sum(counts[k] for k in species)
    my_photos = sum(mine.get(k, 0) for k in species)
    my_species = sum(1 for k in species if mine.get(k))

    def label(k):
        return species[k]["common"] or f"*{species[k]['name']}*"

    def latin(k):
        """Scientific name, linked to its search on gbif.org when it has a Catalogue of Life ID."""
        url = search_url(species[k])
        return f"[*{species[k]['name']}*]({url})" if url else f"*{species[k]['name']}*"

    grouped = {}
    for k, s in species.items():
        grouped.setdefault(group_of(s), []).append(k)
    ordered = sorted(grouped.items(), key=lambda kv: (kv[0] == lh.OTHER, -len(kv[1]), kv[0]))
    top = sorted(species, key=lambda k: (-counts[k], label(k).strip("*").lower()))[:TOP_SPECIES]

    lines = [
        "# Underwater species in West Cork on GBIF\n",
        "> Generated by `scripts/cork_underwater.py` from live GBIF counts. Every recorder and dataset, "
        "not only `andreiastra`.\n",
        f"**{len(species)}** marine species in **{photos}** photos in West Cork and its coastal waters. "
        f"**{my_species}** of the species and **{my_photos}** of the photos are mine. "
        f"The area holds {records} present occurrences with a photo, of every habitat. "
        "The photo counts can include copies of iNaturalist records that other datasets republish "
        "(counts cannot tell them apart), so they may be a little high.\n",
        "## Filters applied\n",
        f"1. Inside the polygon around West Cork and its coastal waters: `geometry={WEST_CORK_POLYGON}`",
        "2. Occurrence is present, not an absence record: `occurrenceStatus=PRESENT`",
        "3. The record has a photo: `mediaType=StillImage`",
        "4. Identified to species: counted per `speciesKey` with `facet=speciesKey`",
        f"5. Marine species, leaving out {' and '.join(sorted(NOT_UNDERWATER))} (seabirds and coastal plants): "
        "a GBIF species profile (WoRMS or Catalogue of Life) marks it as marine\n",
        "The filters can be repeated on [gbif.org/occurrence/search](https://www.gbif.org/occurrence/search) "
        "(Location, the polygon above; Occurrence status, Present; Media type, Still image). "
        "The website can't filter by marine species, so filters 4 and 5 are applied by the script. "
        f"My photos use the same filters plus `recordedBy={RECORDED_BY}`. "
        "Each scientific name below links to the same search for that species on gbif.org, and each group's "
        "photo count links to the search for all its species (the nudibranchs link to the whole order, "
        "so that search also finds photos identified only to genus or order, which the counts here leave out) "
        "(the website's `taxonKey` is a Catalogue of Life ID; a name with no exact match there has no link "
        "and is left out of its group's search).\n",
        "## Species by group\n",
        f"**{len(species)}** species in {len(grouped)} groups.\n",
        "| Group | Species | Photos | Mine |",
        "|---|--:|--:|--:|",
    ]
    def group_photos(g, ks):
        """Photo total of a group, linked to the search for all its species. The nudibranchs link to
        the whole order, which also finds photos identified only to genus or order."""
        total = sum(counts[k] for k in ks)
        taxa = [{"col": NUDIBRANCHIA_COL_ID}] if g == "Nudibranchs" else [species[k] for k in ks]
        url = search_url(*taxa)
        return f"[{total}]({url})" if url else str(total)

    lines += [f"| [{g}](#{lh.anchor(g)}) | {len(ks)} | {group_photos(g, ks)} | "
              f"{sum(mine.get(k, 0) for k in ks)} |" for g, ks in ordered]

    lines += ["\n## Most photographed species\n",
              f"The {TOP_SPECIES} species with the most photos.\n",
              "| Common name | Species | Group | Photos | Mine |", "|---|---|---|--:|--:|"]
    lines += [f"| {label(k)} | {latin(k)} | {group_of(species[k])} | {counts[k]} | {mine.get(k, 0)} |"
              for k in top]

    lines.append("\n## All species by group\n")
    for g, ks in ordered:
        lines += [f"### {g}\n", "| Common name | Species | Photos | Mine |", "|---|---|--:|--:|"]
        lines += [f"| {label(k)} | {latin(k)} | {counts[k]} | {mine.get(k, 0)} |"
                  for k in sorted(ks, key=lambda k: (-counts[k], label(k).strip("*").lower()))]
        lines.append("")

    lines.append(
        "The marine flag comes from taxon profiles, so a marine species seen on the shore or from a boat "
        "counts too, and a freshwater or terrestrial species never appears. A species with no marine value "
        "in its GBIF profile (some seaweeds) is left out. Records carry a coordinate uncertainty, so some may "
        "come from the sea or land just outside the polygon. For the photos themselves, see "
        "[`lough_hyne_species.md`](lough_hyne_species.md) for the Lough Hyne records.")
    return "\n".join(lines) + "\n"


def main():
    records, counts = facet_counts()
    _, mine = facet_counts(recordedBy=RECORDED_BY)
    print(f"{records} records, {len(counts)} species, {len(mine)} of them mine", flush=True)
    species = marine_species(sorted(counts))
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(render(records, counts, mine, species))
    print(f"Saved {len(species)} marine species → {os.path.normpath(OUTPUT_FILE)}", flush=True)


if __name__ == "__main__":
    main()
