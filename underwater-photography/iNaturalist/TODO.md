# iNaturalist Integration — Known Issues & TODOs

This file tracks active bugs, data quality issues, and backlog enhancements for the iNaturalist and dive log integration pipelines.

---

## 1. 🔴 Outdated Static Snapshot Tables in README
* **Problem:** Hardcoded point-in-time counts (e.g. *54 Needs ID*, *17 at Lough Hyne*, *2 observations at Trafrask*) in markdown documentation become stale and inaccurate as new observations or community identifications are made.
* **TODO:**
  - [x] Remove hardcoded counts from `README.md` and replace with dynamic iNaturalist query links.
  - [ ] *(Enhancement)* Build an automated script (e.g. `scripts/generate_action_items.py` or extend `generate_location_ratings.py`) to query the live API and output a dynamic `OUTPUT/needs_id_breakdown.md` report on demand.

---

## 2. 🟡 Generator Treats Townland Aliases as Separate Dive Sites
* **Problem:** [`Preferred_dive_site_names_ireland.txt`](Preferred_dive_site_names_ireland.txt) lists `Sandmount` and `Sandmount Bay Beach` as separate canonical sites. However, [`scripts/site_names.py`](scripts/site_names.py) maps the place keyword `"sandmount"` to `Bank Pier`. Because observations cluster under `Bank Pier`, `Sandmount` and `Sandmount Bay Beach` appear as empty rows with 0 dives / 0 observations in [`scripts/OUTPUT/Location_ratings.md`](scripts/OUTPUT/Location_ratings.md).
* **TODO:**
  - [ ] Prune `Sandmount` and `Sandmount Bay Beach` from `Preferred_dive_site_names_ireland.txt`.
  - [ ] Ensure any dive logs labeled `Sandmount` in `dive-logs/workouts/` are normalized to `Bank Pier` in [`matching-dives-and-places/export_unmatched_dives.py`](matching-dives-and-places/export_unmatched_dives.py).

---

## 3. 🟡 Sites with GPX Dive Logs but No Uploaded Observations
* **Problem:** `Tragumna` and `Reenabulliga Pier` are genuine dive sites with recorded GPX files in `dive-logs/workouts/`, but currently have zero iNaturalist observations uploaded, causing them to render with 0 counts in `Location_ratings.md`.
* **TODO:**
  - [ ] Upload corresponding underwater photo observations to iNaturalist for Tragumna and Reenabulliga Pier when available.

---

## 4. 🔵 Generator Formatting for Zero-Observation Sites
* **Problem:** [`scripts/generate_location_ratings.py`](scripts/generate_location_ratings.py) unconditionally renders full markdown sections and table rows for every canonical site in `Preferred_dive_site_names_ireland.txt`, even when it has 0 observations.
* **TODO:**
  - [ ] Update `generate_location_ratings.py` to optionally filter out 0-observation sites or group them into a compact "Unobserved Sites" section at the end of the report.
