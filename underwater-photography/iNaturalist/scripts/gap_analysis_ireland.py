"""
Write reports/gap_analysis_ireland.md: for each dive site, the species that other
iNaturalist observers have recorded within SITE_RADIUS_KM of it and that andreiastra
has not recorded underwater in Ireland. Use it to decide what to look for next.

For each site the script takes the centroid of the user's observations there and asks
  GET /v1/observations/species_counts?lat=&lng=&radius=&quality_grade=research
        &without_taxon_id=<LAND_TAXON_IDS>
(one request per site). The comparison is limited to Research Grade records of
non-land groups, and includes everyone's records, yours too.

A species is "seen" when it is on your underwater list at species rank (any grade).
Only "New for you" species are listed: those you haven't recorded at any Irish dive
site. Species you have recorded at another site are skipped.

Caveats:
  * West Cork has few iNaturalist observers, so most sites have only a handful of nearby
    species. Counts are small; a site with nothing listed means nobody has posted there.
  * The radius is a circle, so shore and land-adjacent records (limpets, periwinkles,
    seaweed) appear next to true underwater species. Most intertidal species are
    still worth photographing, so they are not filtered out.
  * Counts are observations, not dives, and depend on where people take photos.
  * Marine mammals and seabirds are excluded (see LAND_TAXON_IDS in config.py).

Cache: scripts/.cache/site_species.json, 30 days per site. --refresh fetches every site again.

Usage:
  .venv/bin/python scripts/gap_analysis_ireland.py [--refresh]
"""
import json
import os
import sys
import time
from collections import defaultdict
from datetime import date, datetime, timedelta

import requests

sys.path.insert(0, os.path.dirname(__file__))
from config import API_BASE, CACHE_DIR, LAND_TAXON_IDS, OUTPUT_DIR, THROTTLE_S, USER_ID
from species_classification import species_type
from underwater_stats import species_table, underwater_entries

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "gap_analysis_ireland.md")
CACHE_FILE = os.path.join(CACHE_DIR, "site_species.json")
CACHE_MAX_AGE = timedelta(days=30)
SITE_RADIUS_KM = 1
MIN_NEARBY_OBS = 1      # West Cork has few observers, so a single Research Grade record still counts
PER_PAGE = 500          # species_counts maximum
OBS_PER_PAGE = 200      # observations maximum


def site_centroids(entries):
    """Return {site: (lat, lng)}, the mean position of the user's observations at each site."""
    points = defaultdict(list)
    for site, obs in entries:
        coords = (obs.get("geojson") or {}).get("coordinates")
        if site and coords:
            points[site].append(coords)
    return {s: (sum(c[1] for c in v) / len(v), sum(c[0] for c in v) / len(v))
            for s, v in points.items()}


def fetch_observation_ids(lat, lng, species_ids):
    """Observation ids within SITE_RADIUS_KM of a point, grouped by species: {taxon_id: [obs_id]}.

    Observations identified below species rank are credited to their species ancestor.
    """
    by_species, page, total, seen = defaultdict(list), 1, None, 0
    while total is None or seen < total:
        r = requests.get(f"{API_BASE}/observations", params={
            "lat": lat, "lng": lng, "radius": SITE_RADIUS_KM,
            "quality_grade": "research", "locale": "en",
            "without_taxon_id": ",".join(map(str, LAND_TAXON_IDS)),
            "order_by": "id", "order": "desc", "per_page": OBS_PER_PAGE, "page": page,
        }, timeout=60)
        r.raise_for_status()
        data = r.json()
        total = data.get("total_results", 0)
        batch = data.get("results", [])
        if not batch:
            break
        seen += len(batch)
        for obs in batch:
            t = obs.get("taxon") or {}
            for tid in [t.get("id")] + list(t.get("ancestor_ids") or []):
                if tid in species_ids:
                    by_species[tid].append(obs["id"])
                    break
        page += 1
        time.sleep(THROTTLE_S)
    return by_species


def fetch_nearby(lat, lng):
    """Species within SITE_RADIUS_KM of a point: [{id, name, common, type, count, photo, obs}]."""
    results, page, total = [], 1, None
    while total is None or len(results) < total:
        r = requests.get(f"{API_BASE}/observations/species_counts", params={
            "lat": lat, "lng": lng, "radius": SITE_RADIUS_KM,
            "quality_grade": "research", "locale": "en",
            "without_taxon_id": ",".join(map(str, LAND_TAXON_IDS)),
            "per_page": PER_PAGE, "page": page,
        }, timeout=30)
        r.raise_for_status()
        data = r.json()
        total = data.get("total_results", 0)
        batch = data.get("results", [])
        if not batch:
            break
        for item in batch:
            t = item["taxon"]
            if t.get("rank") != "species":
                continue
            results.append({
                "id": t["id"], "name": t.get("name"), "common": t.get("preferred_common_name"),
                "type": species_type({"taxon": t}),
                "count": item["count"], "photo": (t.get("default_photo") or {}).get("square_url"),
            })
        page += 1
        time.sleep(THROTTLE_S)
    if results:
        obs_ids = fetch_observation_ids(lat, lng, {s["id"] for s in results})
        for s in results:
            s["obs"] = obs_ids.get(s["id"], [])
    return results


def load_cache():
    try:
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_cache(cache):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=1, sort_keys=True)


def nearby_species(cache, site, lat, lng, refresh):
    key = f"{site}:{SITE_RADIUS_KM}km"
    entry = cache.get(key)
    if entry and not refresh and all("obs" in s and "type" in s for s in entry["species"]):
        if datetime.now() - datetime.fromisoformat(entry["fetched"]) < CACHE_MAX_AGE:
            return entry["species"]
    species = fetch_nearby(lat, lng)
    cache[key] = {"species": species, "fetched": datetime.now().isoformat(timespec="seconds")}
    return species


def label(sp):
    common = sp["common"] or sp["name"]
    text = f"[{common}](https://www.inaturalist.org/taxa/{sp['id']})"
    return text + (f" (*{sp['name']}*)" if sp["name"] and sp["name"] != common else "")


def obs_links(ids):
    return ", ".join(f"[{i}](https://www.inaturalist.org/observations/{i})" for i in ids)


def thumb(sp):
    return f"![{sp['common'] or sp['name']}]({sp['photo']})" if sp.get("photo") else ""


def slug(site):
    return site.lower().replace(" ", "-").replace("'", "")


def render(mine_by_site, mine_all, nearby, notes):
    """mine_by_site: {site: {taxon_id}}; mine_all: {taxon_id}; nearby: {site: [species]}.

    Only "New for you" species are listed: those not on your Irish underwater list at any site.
    """
    rows = {}
    for site, species in nearby.items():
        species = [s for s in species if s["count"] >= MIN_NEARBY_OBS]
        have = [s for s in species if s["id"] in mine_by_site[site]]
        new = [s for s in species if s["id"] not in mine_all]
        rows[site] = (species, have, sorted(new, key=lambda s: (-s["count"], s["name"] or "")))

    # New species near several sites: the best targets overall.
    overall = defaultdict(lambda: {"sp": None, "sites": [], "count": 0, "obs": []})
    for site, (_, _, new) in rows.items():
        for s in new:
            o = overall[s["id"]]
            o["sp"], o["count"] = s, o["count"] + s["count"]
            o["sites"].append(site)
            o["obs"] += s["obs"]

    lines = [
        "# Gap analysis: what else lives at your dive sites\n",
        f"> Generated by `scripts/gap_analysis_ireland.py` on {date.today()} "
        f"from live iNaturalist data for `{USER_ID}`. Compares your underwater species with "
        f"every observer's Research Grade records within {SITE_RADIUS_KM} km of each site "
        f"(land groups excluded).\n",
    ]
    lines += [f"> ⚠️ {n}" for n in notes]
    lines += [
        "\n**Read it as a to-do list, not a score.** Records near a site include shore and "
        "intertidal species, and counts depend on where people take photos.\n",
        "## Sites\n",
        "| Site | Species there (all observers) | You have | New for you |",
        "|---|--:|--:|--:|",
    ]
    for site in sorted(rows, key=lambda s: (-len(rows[s][2]), s)):
        species, have, new = rows[site]
        lines.append(f"| [{site}](#{slug(site)}) | {len(species)} | {len(have)} | {len(new)} |")

    targets = sorted(overall.values(), key=lambda o: (-len(o["sites"]), -o["count"]))
    lines += [
        "\n## Best targets across all sites\n",
        "\"New for you\" species recorded near several of your sites. They are not on your "
        "Irish underwater list at any site; species you have recorded anywhere in Ireland are skipped.\n",
        "| Photo | Species | Organism type | Sites near | Observations |",
        "|---|---|---|--:|---|",
    ]
    for o in targets[:20]:
        sp = o["sp"]
        lines.append(f"| {thumb(sp)} | {label(sp)} | {sp['type']} | {len(o['sites'])} | "
                     f"{obs_links(sorted(set(o['obs']), reverse=True))} |")

    for site in sorted(rows, key=lambda s: (-len(rows[s][2]), s)):
        species, have, new = rows[site]
        lines += [
            f"\n## {site}\n",
            f"{len(species)} species recorded nearby, **{len(have)}** on your list, "
            f"**{len(new)}** new for you, most records first:\n",
            "| Photo | Species | Organism type | Observations |",
            "|---|---|---|---|",
        ]
        for sp in new:
            lines.append(f"| {thumb(sp)} | {label(sp)} | {sp['type']} | {obs_links(sp['obs'])} |")
        if not new:
            lines.append("| | Nothing new for you at this site. | | |")
    return "\n".join(lines) + "\n"


def main():
    notes = []
    entries = underwater_entries(notes)
    table = species_table(entries)
    mine_all = set(table)
    mine_by_site = defaultdict(set)
    for tid, info in table.items():
        for site, _ in info["entries"]:
            if site:
                mine_by_site[site].add(tid)

    centroids = site_centroids(entries)
    refresh = "--refresh" in sys.argv
    cache = load_cache()
    nearby = {}
    print(f"Comparing {len(centroids)} sites ({SITE_RADIUS_KM} km radius)…")
    try:
        for i, (site, (lat, lng)) in enumerate(sorted(centroids.items()), 1):
            nearby[site] = nearby_species(cache, site, lat, lng, refresh)
            print(f"  {i}/{len(centroids)} {site}: {len(nearby[site])} species nearby")
    finally:
        save_cache(cache)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(render(mine_by_site, mine_all, nearby, notes))
    print(f"Saved {len(nearby)} sites → {os.path.normpath(OUTPUT_FILE)}")
    for note in notes:
        print(f"WARNING: {note}")


if __name__ == "__main__":
    main()
