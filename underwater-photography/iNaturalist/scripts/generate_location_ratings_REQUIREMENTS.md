# Requirements: `Location_ratings.md` Generator

**Script:** `scripts/generate_location_ratings.py`
**Output:** `Location_ratings.md`

---

## Purpose

Generate a Markdown reference document that lists all West Cork dive sites with
the number of dive sessions recorded at each site and every iNaturalist
observation made there, each shown as a clickable photo thumbnail.

---

## Inputs

| Input | Source | Notes |
|---|---|---|
| iNaturalist observations | Live API (`/v1/observations`) | Fetched at run time for user `andreiastra`; 30 s timeout per page |
| Canonical site names | `Preferred_dive_site_names.txt` | One name per line; every entry appears in output |
| Keyword → name mapping | `scripts/site_names.py` → `SITE_KEYWORDS` | Maps `place_guess` fragments to canonical names |
| Non-dive location skip-list | `scripts/site_names.py` → `IGNORED_KEYWORDS` | Clusters matching these are silently excluded |

---

## Output Format

### File: `Location_ratings.md`

#### Header block
- Title: `# Dive Site Observations`
- Generator note and total observation / site counts.
- If any warnings were raised during the run, each appears as a `> ⚠️ …`
  blockquote line immediately below the totals.

#### Site Summary table
Sorted by observation count descending (ties broken by dive count, then name).

| Column | Content |
|---|---|
| `#` | Rank |
| `Site` | Canonical name, linked to the section anchor below |
| `Dives` | Number of distinct `observed_on` dates at that site |
| `Observations` | Total iNaturalist observation count at that site |

#### Per-site sections
One section per site in `Preferred_dive_site_names.txt`.  Each section contains:

- Anchor `<a id="...">` derived from the lowercase, hyphenated site name
- `## Site Name` heading
- Summary line: `**Dives:** N  |  **Observations:** N`
- Observation table (see below), sorted by `observed_on` descending

#### Observation table columns

| Column | Content |
|---|---|
| `Photo` | Clickable thumbnail: `[![alt](thumb_url)](obs_url "species name")` — thumbnail upgraded from `/square.jpg` to `/small.jpg` (240 px). If no photo, a plain text link. |
| `Species` | Bold common name + italic scientific name on second line (omitted if identical to common name), linked to the iNaturalist observation page |
| `Date` | `observed_on` date (YYYY-MM-DD) |
| `Status` | `✅ Research Grade` or `🔍 Needs ID` |

---

## Dive Session Count

Dive sessions are counted as the number of **distinct `observed_on` dates**
among the observations at that site.  No dependency on dive-log files.

---

## Site Matching

Observations are assigned to sites in two steps:

1. **Geospatial clustering** — greedy 500 m radius (Haversine distance).
   Observations with no GPS coordinates are counted and reported as a warning.

2. **Keyword matching** — each cluster's combined `place_guess` strings are
   checked against `SITE_KEYWORDS` in `scripts/site_names.py`.
   - Matched → assigned to the canonical site name.
   - Matched by `IGNORED_KEYWORDS` → silently skipped (known non-dive locations
     such as Coolanagh, Courtmacsherry, Derrigra).
   - No match → reported as a `⚠️` warning in the document header, prompting
     an update to `scripts/site_names.py`.

---

## Prerequisites

1. `scripts/site_names.py` must be current — run `scripts/my_locations.py` and
   verify every cluster resolves to a canonical name or is listed in
   `IGNORED_KEYWORDS` before generating.
2. `.venv` with `requests` installed (`pip install requests`).

---

## Execution

```bash
.venv/bin/python scripts/generate_location_ratings.py
```

Expected console output: page-by-page fetch progress, then a per-site summary
of dive and observation counts.

---

## Error Handling

| Situation | Behaviour |
|---|---|
| `Preferred_dive_site_names.txt` unreadable | Fatal — script exits immediately |
| API timeout (30 s) | Warning in doc; output uses partial data collected so far |
| API HTTP error (e.g. 429, 500) | Warning in doc with status code; partial data |
| API network error | Warning in doc; partial data |
| Observations with no GPS coordinates | Warning in doc with count |
| Cluster not matching any site or ignore keyword | Warning in doc listing place_guess; update `site_names.py` |

---

## Known Limitations

- **Dive count is approximate.** Multiple dives on the same calendar day at the
  same site count as one session (only the date, not the time, is used).
- **`place_guess` is OSM-derived** and may change as OpenStreetMap data is
  updated. If a cluster stops resolving, re-verify `site_names.py`.
- **Sites with zero observations are included** — every site in
  `Preferred_dive_site_names.txt` appears in the output, showing
  `Dives: 0 | Observations: 0` and a placeholder message in place of the
  observation table.
- **API results may lag.** iNaturalist can take a few minutes to reflect edits
  made to observations; re-run the script after waiting if counts look stale.
