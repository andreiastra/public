"""
Rate andreiastra's Research Grade underwater observations in Ireland by rarity
and write a Markdown report to reports/rarity_underwater_ireland.md.

Which observations count: underwater_ireland.underwater_observations() (clustered
onto a dive site), keeping Research Grade only.

Rarity of a taxon is the number of distinct observers who have a verifiable
observation (Research Grade or Needs ID) of it anywhere in Ireland on iNaturalist
(fewest = rarest). This matches the count on the iNaturalist taxon page; Research
Grade alone undercounts taxa, such as fish, that mostly stay at Needs ID. Ties are
broken by the total number of verifiable observations in Ireland. Both come from
the public API:
  GET /v1/observations/observers?taxon_id={id}&place_id={ireland}&verifiable=true
  GET /v1/observations?taxon_id={id}&place_id={ireland}&verifiable=true&per_page=0

Obscured observations (threatened species, true location hidden, see README
"Obscured locations") can't be confirmed underwater from the API. They are
included and flagged, since rarity depends on the taxon, not the site.

The fetching, ranking and rendering live in generate_report(), which is also used
by rarity_underwater_worldwide.py with a different place and measure.

Throttle: 0.5 s between requests, as in rare_birds_ireland.py.

Cache: the per-taxon counts are stored in scripts/.cache/taxon_counts.json and reused
for 90 days, so a normal run only fetches taxa that are new or stale. Pass --refresh
to fetch everything again.

Usage:
  .venv/bin/python scripts/rarity_underwater_ireland.py [--refresh]
"""
import json
import os
import sys
import time
from datetime import datetime, timedelta

import requests

sys.path.insert(0, os.path.dirname(__file__))
from config import API_BASE, CACHE_DIR, IRELAND_PLACE_ID, OUTPUT_DIR, USER_ID
from generate_location_ratings import photo_md
from site_observations import names
from underwater_ireland import iucn_status, underwater_observations

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "rarity_underwater_ireland.md")
REQUEST_PAUSE_S = 0.5
COUNTS_CACHE = os.path.join(CACHE_DIR, "taxon_counts.json")
COUNTS_MAX_AGE = timedelta(days=90)

# (max value, rating). The first matching row applies; anything above is DEFAULT_RATING.
RATINGS = [
    (1, "Unique"),     # only you
    (5, "Very rare"),
    (20, "Rare"),
    (100, "Uncommon"),
]
DEFAULT_RATING = "Common"

UNITS = {"observers": "observers", "total": "observations"}


def rating(value, ratings=RATINGS):
    return next((label for limit, label in ratings if value <= limit), DEFAULT_RATING)


def fetch_counts(taxon_id, place_id=IRELAND_PLACE_ID):
    """Return (distinct observers, observations) with verifiable records.

    place_id=None counts worldwide.
    """
    params = {"taxon_id": taxon_id, "verifiable": "true", "per_page": 1}
    if place_id:
        params["place_id"] = place_id
    counts = []
    for endpoint, extra in (("observations/observers", {}), ("observations", {"per_page": 0})):
        r = requests.get(f"{API_BASE}/{endpoint}", params={**params, **extra}, timeout=30)
        r.raise_for_status()
        counts.append(r.json().get("total_results", 0))
        time.sleep(REQUEST_PAUSE_S)
    return tuple(counts)


def _cache_key(taxon_id, place_id):
    # "verifiable" is part of the key so counts taken with another definition are never reused.
    return f"{taxon_id}:{place_id or 'world'}:verifiable"


def load_counts_cache():
    try:
        with open(COUNTS_CACHE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_counts_cache(cache):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(COUNTS_CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=1, sort_keys=True)


def cached_counts(cache, taxon_id, place_id, refresh=False):
    """Return ((observers, observations), fetched) using the cache when the entry is fresh."""
    key = _cache_key(taxon_id, place_id)
    entry = cache.get(key)
    if entry and not refresh:
        age = datetime.now() - datetime.fromisoformat(entry["fetched"])
        if age < COUNTS_MAX_AGE:
            return (entry["observers"], entry["total"]), False
    observers, total = fetch_counts(taxon_id, place_id)
    cache[key] = {"observers": observers, "total": total,
                  "fetched": datetime.now().isoformat(timespec="seconds")}
    return (observers, total), True


def collect_taxa(site_obs, obscured):
    """Group Research Grade observations by taxon id."""
    taxa = {}
    entries = [(site, o) for site, v in site_obs.items() for o in v]
    entries += [(None, o) for o in obscured]
    for site, obs in entries:
        taxon = obs.get("taxon")
        if obs.get("quality_grade") != "research" or not taxon:
            continue
        info = taxa.setdefault(taxon["id"], {"obs": [], "sites": set(), "obscured": False})
        info["obs"].append(obs)
        if site:
            info["sites"].add(site)
        else:
            info["obscured"] = True
    return taxa


def legend(ratings, metric):
    lines = [f"| Rating | {UNITS[metric].capitalize()} |", "|---|---|"]
    low = 0
    for limit, label in ratings:
        span = f"{limit:,}" if limit == low + 1 else f"{low + 1:,}–{limit:,}"
        lines.append(f"| {label} | {span} |")
        low = limit
    lines.append(f"| {DEFAULT_RATING} | more than {low:,} |")
    return lines


def render(ranked, notes, *, title, script, intro, ratings, metric, scope):
    lines = [
        f"# {title}\n",
        f"> Generated by `scripts/{script}` "
        f"from live iNaturalist data for `{USER_ID}`. Your observations: Research Grade only. "
        f"Comparison counts: all verifiable observations.\n",
    ]
    lines += [f"> ⚠️ {n}" for n in notes]
    lines += [
        f"\n**{len(ranked)}** taxa · **{sum(len(i['obs']) for _, i in ranked)}** observations\n",
        intro + "\n",
        *legend(ratings, metric),
        f"\n| # | Photo | Species | Rating | {scope} observers | {scope} obs | IUCN | My obs | Sites |",
        "|--:|---|---|---|--:|--:|---|--:|---|",
    ]
    for rank, (tid, info) in enumerate(ranked, 1):
        mine = sorted(info["obs"], key=lambda o: o.get("observed_on") or "")
        common, sci = names(mine[0])
        label = f"[{common}](https://www.inaturalist.org/taxa/{tid})" + \
                (f" (*{sci}*)" if sci and sci != common else "")
        sites = ", ".join(sorted(info["sites"]))
        if info["obscured"]:
            sites += (", " if sites else "") + "⚠️ obscured, not confirmed underwater"
        lines.append(
            f"| {rank} | {photo_md(mine[0])} | {label} | {rating(info[metric], ratings)} "
            f"| {info['observers']:,} | {info['total']:,} | {iucn_status(mine[0])} "
            f"| {len(mine)} | {sites} |"
        )
    return "\n".join(lines) + "\n"


def generate_report(*, place_id, metric, ratings, title, script, intro, scope, output_file):
    """Rate the user's Research Grade underwater taxa and write the Markdown report.

    place_id: iNaturalist place for the comparison counts (None = worldwide).
    metric:   "observers" or "total" (observations). Ranks the taxa, fewest first, and
              sets the rating; the other measure breaks ties.
    """
    notes = []
    site_obs, obscured = underwater_observations(notes)
    taxa = collect_taxa(site_obs, obscured)

    refresh = "--refresh" in sys.argv
    cache = load_counts_cache()
    fetched = 0
    print(f"{len(taxa)} Research Grade taxa. Getting {scope} counts…")
    try:
        for i, (tid, info) in enumerate(taxa.items(), 1):
            (info["observers"], info["total"]), was_fetched = cached_counts(
                cache, tid, place_id, refresh)
            fetched += was_fetched
            if i % 20 == 0:
                print(f"  {i}/{len(taxa)}")
    finally:
        save_counts_cache(cache)  # keep progress even if interrupted
    print(f"  {fetched} fetched, {len(taxa) - fetched} from cache")

    other = "total" if metric == "observers" else "observers"
    ranked = sorted(taxa.items(), key=lambda kv: (kv[1][metric], kv[1][other],
                                                 names(kv[1]["obs"][0])[0].lower()))
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(render(ranked, notes, title=title, script=script, intro=intro,
                       ratings=ratings, metric=metric, scope=scope))
    print(f"Saved {len(ranked)} taxa → {os.path.normpath(output_file)}")
    for note in notes:
        print(f"WARNING: {note}")


def main():
    generate_report(
        place_id=IRELAND_PLACE_ID,
        metric="observers",
        ratings=RATINGS,
        title="Rarity of underwater observations in Ireland",
        script="rarity_underwater_ireland.py",
        intro="Rarity is the number of distinct observers with a verifiable record (Research "
              "Grade or Needs ID) of the taxon anywhere in Ireland (fewest = rarest). Ties go "
              "to the taxon with fewer verifiable observations in Ireland.",
        scope="IE",
        output_file=OUTPUT_FILE,
    )


if __name__ == "__main__":
    main()
