# How `generate_dive_highlights.py` Works

Run it with:

```bash
.venv/bin/python dive-highlights-west-cork/generate_dive_highlights.py
```

It fetches your live iNaturalist observations, computes stats, and writes
`dive-highlights-west-cork/dive-highlights-west-cork.html` from scratch. The whole file is overwritten
every time — there is nothing to merge or diff.

---

## Overview

```
iNaturalist API
      │
      ▼
fetch_all_observations()   ← pages through all your observations
      │
      ├──▶ compute_stats()     ← counts totals, sites, sharks, nudibranchs, faves
      │
      └──▶ build_html()        ← assembles the HTML from config + live data
                │
                ├── header + stats bar      (live counts)
                ├── hero card               (hardcoded config)
                ├── sightings grid          (config + live dates)
                ├── best sites table        (config + live obs counts)
                └── worth revisiting table  (hardcoded config)
```

---

## What comes from the live API

These values are recalculated every time the script runs:

| HTML element | Source |
|---|---|
| "Total observations" stat | `total_results` from API |
| "Dive sites visited" stat | count of distinct resolved dive sites |
| "Shark encounters" stat | observations with "catshark" in common name |
| "Nudibranch species" stat | observations matching known nudibranch name list |
| "Community-faved find" stat | observations with `faves_count > 0` |
| Observation count per site (Best Sites table) | grouped observations by resolved site |
| Date on each sighting card (`· Aug 2025`) | `observed_on` field on the observation |

---

## What is hardcoded in the script

These require manual edits when something changes:

| Constant | What it controls | When to update |
|---|---|---|
| `USER_ID` | iNaturalist username | Never (unless account changes) |
| `PREPARED_FOR` | Name in the subtitle | Change for a different recipient |
| `SITE_KEYWORDS` | Keyword → site name mapping | Add a row when a new site appears in `place_guess` |
| `DIVE_SITES` | Which sites count as dive sites | Add when you first dive somewhere new |
| `SITE_RATINGS` | Star ratings (1–3) | Update when a site earns a higher rating |
| `SITE_DESCS` | Sub-line under site name in table | Edit for accuracy |
| `SITE_WHY` | "Why it stands out" column text | Update when notable new species found |
| `REVISIT_SITES` | "Worth Revisiting" table rows | Add/remove sites as data grows |
| `HERO` | The single most impressive find | Swap when a better find comes along |
| `STANDOUT_SIGHTINGS` | The photo grid cards | Add a row for each new featured sighting |

---

## How the sightings grid works

Each row in `STANDOUT_SIGHTINGS` is a tuple:

```python
(name, scientific_name, photo_url, obs_url, site_label, badge_list)
```

| Field | Example | Notes |
|---|---|---|
| `name` | `"Small-spotted Catshark"` | Display name on the card |
| `scientific_name` | `"Scyliorhinus canicula"` | Shown in italics |
| `photo_url` | `"https://inaturalist-open-data.s3...medium.jpg"` | iNaturalist S3 photo |
| `obs_url` | `"https://www.inaturalist.org/observations/395273855"` | Clicking the photo opens this |
| `site_label` | `"Zetland Pier"` | Site name only — **no date** |
| `badge_list` | `[("research", "Research Grade"), ("", "Shark")]` | List of `(css_class, label)` pairs |

**The date is resolved automatically.** The script extracts the observation ID
from `obs_url`, looks it up in the downloaded observations, and appends
`· Mon YYYY` from the `observed_on` field. You never type a date manually.

Badge CSS classes:

| Class | Colour | Use for |
|---|---|---|
| `"research"` | Green | Research Grade observations |
| `"faved"` | Yellow | Community-favourited finds |
| `"threatened"` | Red | IUCN threatened / near-threatened species |
| `""` | Grey | Any other label |

---

## How site grouping works (`resolve_site`)

iNaturalist's `place_guess` field returns inconsistent strings like
`"Gortdubh Pier, Knockaphuca, Co. Cork, Ireland"` or just `"Canty's Cove"`.

`resolve_site()` matches the lowercased `place_guess` against `SITE_KEYWORDS`
(ordered, first match wins) and returns the canonical site name. Observations
that don't match any keyword (e.g. bird observations at Coolanagh) return
`None` and are excluded from all dive stats.

---

## Adding a new featured sighting

1. Find the observation on iNaturalist and copy its URL.
2. Copy the photo URL from the observation (right-click → copy image address,
   then replace `/square.` with `/medium.`).
3. Add a row to `STANDOUT_SIGHTINGS`:
   ```python
   ("Species Name", "Genus species",
    "https://inaturalist-open-data.s3.amazonaws.com/photos/PHOTOID/medium.jpg",
    "https://www.inaturalist.org/observations/OBSID",
    "Site Name",
    [("research", "Research Grade")]),
   ```
4. Run the script — date is filled in automatically.

If the species is IUCN threatened, use `("threatened", "Near Threatened ⚠️")`
as the first badge.

---

## Adding a new dive site

1. Add a keyword entry to `SITE_KEYWORDS`:
   ```python
   ("keyword_in_place_guess", "Preferred Site Name"),
   ```
2. Add the name to `DIVE_SITES`.
3. Optionally add entries to `SITE_DESCS`, `SITE_RATINGS`, `SITE_WHY` when
   enough dives have been done to rate it.
4. Run the script.
