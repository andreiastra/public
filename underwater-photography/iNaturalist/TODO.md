# iNaturalist Integration — Known Issues & TODOs

This file tracks active bugs, data quality issues, and backlog enhancements for the iNaturalist and dive log integration pipelines.

---

## 1. 🔴 Outdated Static Snapshot Tables in README
* **Problem:** Hardcoded point-in-time counts (e.g. *54 Needs ID*, *17 at Lough Hyne*, *2 observations at Trafrask*) in markdown documentation become stale and inaccurate as new observations or community identifications are made.
* **TODO:**
  - [x] Remove hardcoded counts from `README.md` and replace with dynamic iNaturalist query links.
  - [ ] *(Enhancement)* Build an automated script (e.g. `scripts/generate_action_items.py` or extend `generate_location_ratings.py`) to query the live API and output a dynamic `OUTPUT/needs_id_breakdown.md` report on demand.

---

## 2. 🔵 Generator Formatting for Zero-Observation Sites
* **Problem:** [`scripts/generate_location_ratings.py`](scripts/generate_location_ratings.py) unconditionally renders full markdown sections and table rows for every canonical site in `Preferred_dive_site_names_ireland.txt`, even when it has 0 observations.
* **TODO:**
  - [ ] Update `generate_location_ratings.py` to optionally filter out 0-observation sites or group them into a compact "Unobserved Sites" section at the end of the report.

---

## 3. 🟡 Keep `site_names.py` in Sync with the Location Lists
* **Problem:** Location names are kept in two places that can drift apart:
  - [`Preferred_other_location_names.txt`](Preferred_other_location_names.txt) is not read by any script. Every above-water place must also be added by hand to `IGNORED_KEYWORDS` in [`scripts/site_names.py`](scripts/site_names.py). Example: `Bandon` was in the file but its observations still triggered an "unmatched cluster" warning until `"bandon"` was added to `IGNORED_KEYWORDS`.
  - [`Preferred_dive_site_names_ireland.txt`](Preferred_dive_site_names_ireland.txt) and `SITE_KEYWORDS` are not checked against each other. A new dive site with no keyword, or a keyword pointing to a renamed or removed site, goes unnoticed.
* **Why not check file timestamps:** modified times change on `git checkout`, `git pull` or a plain re-save, so they don't show whether names changed. They also can't say which names are new or which keyword they need. Compare file contents with `site_names.py` on every run instead.
* **Why dive-site keywords stay hand-written:** they need judgement. A bare `"simon"` matched "Cloghmac**simon**, Bandon", and a bare `"sandmount"` merged Bank Pier with Sandmount Bay Beach. Some sites also need aliases that can't be derived from the name, such as `"derreenacarrin"` for Zetland Pier, or `"bank"` for the plus-code place names.
* **TODO:**
  - [ ] Make `site_names.py` read `Preferred_other_location_names.txt` and skip any place name containing one of its entries (lower-cased).
  - [ ] Move `derrigra` from `IGNORED_KEYWORDS` into `Preferred_other_location_names.txt`. Keep only the overseas entries (Egypt, Saudi Arabia) in `IGNORED_KEYWORDS`.
  - [ ] In `generate_location_ratings.py`, add a warning at the top of `Location_ratings.md` for each site in `Preferred_dive_site_names_ireland.txt` that has no keyword in `SITE_KEYWORDS`.
  - [ ] Add a warning for each `SITE_KEYWORDS` entry whose site name is not in `Preferred_dive_site_names_ireland.txt`.
  - [ ] Update the "Two files are easy to mix up" section of [`scripts/README.md`](scripts/README.md), which currently says no script reads `Preferred_other_location_names.txt`.
* **Workflow once done:** edit a `.txt` file, run `generate_location_ratings.py`, then read the warnings at the top of the report.

---

## 4. 🟡 Handle Obscured Locations in Other Scripts
* **Problem:** iNaturalist hides the true location of threatened species from the public API (`obscured: true`), so GPS-based scripts miss them or place them at the wrong site. Only [`scripts/underwater_ireland.py`](scripts/underwater_ireland.py) handles this. Details: [`scripts/README.md`](scripts/README.md#obscured-locations).
* **Affected, wrong results:** `generate_location_ratings.py` (unmatched-cluster warning, observation missing from the site), `site_observations.py` and `my_locations.py` (distance clustering), `nudibranch_ireland.py` (matches on `place_guess`, which is "Cork, IE" for obscured observations, so the site falls back to that name).
* **Affected, display only:** `my_places.py`, `species_classification.py` and `rare_birds_ireland.py` print `place_guess`, so obscured observations show a vague place such as "Cork, IE". Nothing is misplaced, but the place shown is not the real one.
* **TODO:**
  - [ ] Move the obscured-observation split from `underwater_ireland.py` into a shared helper in `generate_location_ratings.py`.
  - [ ] Use it in the other scripts, and list obscured observations separately instead of dropping them or raising an unmatched-cluster warning.
  - [ ] *(Optional)* Add a per-observation site override for obscured observations, so they can be counted on their real site.
