"""
Generates Location_ratings.md — a structured dive-site reference with:
  - Number of dive sessions per site (distinct observation dates at that site)
  - iNaturalist observations per site (fetched live from the API)
  - Each observation as a clickable photo thumbnail linking to the observation page

Authoritative sources:
  - Canonical site names : Preferred_dive_site_names.txt
  - Keyword → name mapping: scripts/site_names.py

── Site keyword mapping ──────────────────────────────────────────────────────

Observations are assigned to sites by matching each observation's place_guess
string against the keyword list in scripts/site_names.py.  That list must be
kept in sync with Preferred_dive_site_names.txt and verified against live
iNaturalist data before running this script.  See scripts/site_names.py for
the full refresh procedure.

Usage:
  .venv/bin/python scripts/generate_location_ratings.py
"""
import math
import os
import re
import sys
import time

import requests

# ── Paths ─────────────────────────────────────────────────────────────────────
_ROOT      = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SITES_FILE = os.path.join(_ROOT, "Preferred_dive_site_names.txt")
OUTPUT     = os.path.join(_ROOT, "Location_ratings.md")

sys.path.insert(0, os.path.dirname(__file__))
from site_names import SITE_KEYWORDS, IGNORED_KEYWORDS  # noqa: E402

# ── API config ────────────────────────────────────────────────────────────────
USER_ID  = "andreiastra"
BASE_URL = "https://api.inaturalist.org/v1/observations"
PER_PAGE = 200
RADIUS_M = 500   # geospatial clustering radius in metres


# ── Load dive sites from file ─────────────────────────────────────────────────

def load_dive_sites(path):
    """Return a set of canonical site names from Preferred_dive_site_names.txt."""
    sites = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            name = line.strip()
            if name:
                sites.add(name)
    return sites


# ── Helpers ───────────────────────────────────────────────────────────────────

def haversine(lat1, lon1, lat2, lon2):
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi    = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def resolve_site(place_guesses, dive_sites):
    """Return the canonical site name for a list of place_guess strings, or None."""
    combined = " ".join(place_guesses).lower()
    for kw, name in SITE_KEYWORDS:
        if kw in combined and name in dive_sites:
            return name
    return None


# ── API fetch ─────────────────────────────────────────────────────────────────

def fetch_all_observations(notes):
    """
    Fetch all observations from the iNaturalist API.
    On a page-level HTTP error, appends a warning to notes and stops early
    (returning whatever was collected so far rather than aborting entirely).
    """
    print(f"Fetching observations for '{USER_ID}' from iNaturalist…")
    all_obs, page = [], 1
    while True:
        try:
            r = requests.get(BASE_URL, params={
                "user_id":  USER_ID,
                "per_page": PER_PAGE,
                "page":     page,
            }, timeout=30)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            notes.append(f"API timeout on page {page} — output may be incomplete.")
            print(f"  WARNING: timeout on page {page}, stopping early.")
            break
        except requests.exceptions.HTTPError as exc:
            notes.append(f"API HTTP error on page {page}: {exc} — output may be incomplete.")
            print(f"  WARNING: HTTP error on page {page}: {exc}, stopping early.")
            break
        except requests.exceptions.RequestException as exc:
            notes.append(f"API network error on page {page}: {exc} — output may be incomplete.")
            print(f"  WARNING: network error on page {page}: {exc}, stopping early.")
            break

        data    = r.json()
        results = data.get("results", [])
        all_obs.extend(results)
        print(f"  page {page}: {len(results)} obs  (running total: {len(all_obs)})")
        if len(all_obs) >= data.get("total_results", 0):
            break
        page += 1
        time.sleep(1)

    print(f"Total: {len(all_obs)} observations\n")
    return all_obs


# ── Clustering ────────────────────────────────────────────────────────────────

def cluster_and_label(observations, dive_sites, notes):
    """
    Greedy 500 m radius clustering (same algorithm as my_locations.py).
    Returns dict: canonical_site_name → list of observation dicts.
    Only clusters that resolve to a name present in dive_sites are kept.
    Appends a warning to notes for each cluster that could not be resolved.
    """
    clusters      = []
    no_coords     = 0

    for obs in observations:
        coords = (obs.get("geojson") or {}).get("coordinates")
        lat = coords[1] if coords else None
        lon = coords[0] if coords else None
        if lat is None or lon is None:
            no_coords += 1
            continue

        nearest, nearest_dist = None, float("inf")
        for c in clusters:
            d = haversine(lat, lon, c["centroid"][0], c["centroid"][1])
            if d < nearest_dist:
                nearest_dist, nearest = d, c

        if nearest and nearest_dist <= RADIUS_M:
            nearest["obs"].append(obs)
            lats = [o["geojson"]["coordinates"][1] for o in nearest["obs"] if o.get("geojson")]
            lons = [o["geojson"]["coordinates"][0] for o in nearest["obs"] if o.get("geojson")]
            nearest["centroid"] = (sum(lats) / len(lats), sum(lons) / len(lons))
        else:
            clusters.append({"centroid": (lat, lon), "obs": [obs]})

    if no_coords:
        notes.append(
            f"{no_coords} observation(s) had no GPS coordinates and were excluded."
        )

    site_obs   = {}
    unresolved = []
    for c in clusters:
        guesses  = [o.get("place_guess") or "" for o in c["obs"]]
        combined = " ".join(guesses).lower()
        name     = resolve_site(guesses, dive_sites)
        if name:
            site_obs.setdefault(name, []).extend(c["obs"])
        elif any(kw in combined for kw in IGNORED_KEYWORDS):
            pass  # known non-dive location — silently skip
        else:
            sample = next((g for g in guesses if g), "unknown location")
            unresolved.append(f'{len(c["obs"])} obs near \u201c{sample}\u201d')

    if unresolved:
        notes.append(
            "The following clusters could not be matched to a known dive site — "
            "consider updating scripts/site_names.py: "
            + "; ".join(unresolved)
        )

    return site_obs


# ── Dive-session counting ─────────────────────────────────────────────────────

def count_dives_per_site(site_obs):
    """
    Return dict: site_name → number of distinct observation dates.
    Each unique date is treated as one dive session.
    """
    counts = {}
    for site, obs_list in site_obs.items():
        dates = {o.get("observed_on") for o in obs_list if o.get("observed_on")}
        counts[site] = len(dates)
    return counts


# ── Markdown rendering ────────────────────────────────────────────────────────

def photo_md(obs):
    """
    Return a Markdown image-link for the first photo, or a plain link if none.
    Upgrades iNaturalist /square. thumbnail to /small. (240 px wide).
    """
    url  = obs.get("uri") or f"https://www.inaturalist.org/observations/{obs['id']}"
    name = ((obs.get("taxon") or {}).get("preferred_common_name")
            or (obs.get("taxon") or {}).get("name")
            or "Unknown species")
    photos = obs.get("photos") or []
    if photos:
        thumb = photos[0].get("url") or ""
        thumb = re.sub(r"/square\.(jpe?g|png|gif)$", r"/small.\1", thumb, flags=re.I)
        return f'[![{name}]({thumb})]({url} "{name}")'
    return f"[{name}]({url})"


def render_site_section(site, obs_list, dive_count):
    anchor = site.lower().replace(" ", "-").replace("'", "").replace("(", "").replace(")", "")
    lines  = [
        f'\n<a id="{anchor}"></a>',
        f"## {site}\n",
        f"**Dives:** {dive_count}  |  **Observations:** {len(obs_list)}\n",
    ]

    if not obs_list:
        lines.append("_No iNaturalist observations recorded for this site._\n")
        return "\n".join(lines)

    obs_list.sort(key=lambda o: o.get("observed_on") or "", reverse=True)

    lines += [
        "| Photo | Species | Date | Status |",
        "|-------|---------|------|--------|",
    ]
    for obs in obs_list:
        photo   = photo_md(obs)
        taxon   = obs.get("taxon") or {}
        common  = taxon.get("preferred_common_name") or taxon.get("name") or "Unknown"
        sci     = taxon.get("name") or ""
        sp_cell = f"**{common}**" + (f"<br>*{sci}*" if sci and sci != common else "")
        date    = obs.get("observed_on") or "—"
        quality = obs.get("quality_grade") or "unknown"
        badge   = "✅ Research Grade" if quality == "research" else "🔍 Needs ID"
        obs_url = obs.get("uri") or f"https://www.inaturalist.org/observations/{obs['id']}"
        lines.append(f"| {photo} | [{sp_cell}]({obs_url}) | {date} | {badge} |")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    notes = []   # warnings accumulated during the run; written to the doc header

    try:
        dive_sites = load_dive_sites(SITES_FILE)
    except OSError as exc:
        # Fatal — cannot continue without the site list
        print(f"ERROR: cannot read {SITES_FILE}: {exc}")
        sys.exit(1)

    observations = fetch_all_observations(notes)
    site_obs     = cluster_and_label(observations, dive_sites, notes)
    dive_counts  = count_dives_per_site(site_obs)

    # Build records for every site in Preferred_dive_site_names.txt
    records = [
        (site, site_obs.get(site, []), dive_counts.get(site, 0))
        for site in sorted(dive_sites)
    ]
    # Sort: most observations first, then most dives, then alphabetical
    records.sort(key=lambda r: (-len(r[1]), -r[2], r[0]))

    notes_block = ""
    if notes:
        note_lines = "\n".join(f"> ⚠️ {n}" for n in notes)
        notes_block = f"\n{note_lines}\n"

    lines = [
        "# Dive Site Observations\n",
        "> Generated by `scripts/generate_location_ratings.py` from live iNaturalist data.",
        f"> **{len(observations)}** total observations across **{len(records)}** sites.",
        notes_block,
        "---\n",
        "## Site Summary\n",
        "| # | Site | Dives | Observations |",
        "|---|------|------:|-------------:|",
    ]
    for i, (site, obs_list, dc) in enumerate(records, 1):
        anchor = site.lower().replace(" ", "-").replace("'", "").replace("(", "").replace(")", "")
        lines.append(f"| {i} | [{site}](#{anchor}) | {dc} | {len(obs_list)} |")

    lines.append("\n---\n")

    for site, obs_list, dc in records:
        lines.append(render_site_section(site, obs_list, dc))
        lines.append("\n---\n")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\nWrote {OUTPUT}")
    for site, obs_list, dc in records:
        print(f"  {site:30s}  dives={dc:3d}  obs={len(obs_list):3d}")


if __name__ == "__main__":
    main()
