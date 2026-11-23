# iNaturalist Integration — Known Issues & TODOs

This file tracks active bugs, data quality issues, and backlog enhancements for the iNaturalist and dive log integration pipelines.

---

## 1. 🔴 Outdated Static Snapshot Tables in README
* **Problem:** Hardcoded point-in-time counts (e.g. *54 Needs ID*, *17 at Lough Hyne*, *2 observations at Trafrask*) in markdown documentation become stale and inaccurate as new observations or community identifications are made.
* **TODO:**
  - [x] Remove hardcoded counts from `README.md` and replace with dynamic iNaturalist query links.
  - [ ] *(Enhancement)* Build an automated script (e.g. `scripts/generate_action_items.py` or extend `generate_location_ratings.py`) to query the live API and output a dynamic `reports/needs_id_breakdown.md` report on demand.

---

## 2. 🔵 Generator Formatting for Zero-Observation Sites
* **Problem:** [`scripts/generate_location_ratings.py`](scripts/generate_location_ratings.py) unconditionally renders full markdown sections and table rows for every canonical site in `DIVE_SITES.txt`, even when it has 0 observations.
* **TODO:**
  - [ ] Update `generate_location_ratings.py` to optionally filter out 0-observation sites or group them into a compact "Unobserved Sites" section at the end of the report.

---

## 3. 🟡 Keep `site_names.py` in Sync with the Location Lists
* **Problem:** Location names are kept in two places that can drift apart:
  - [`LAND_SITES.txt`](LAND_SITES.txt) used to be read by no script, so every above-water place also had to be added by hand to `IGNORED_KEYWORDS` in [`scripts/site_names.py`](scripts/site_names.py). That is fixed: `site_names.py` now reads the file.
  - [`DIVE_SITES.txt`](DIVE_SITES.txt) and the hand-written `SITE_ALIASES`. Each site's full name is now a keyword automatically, and an alias pointing to a site that is not in the file raises a warning on import. A site with no alias whose `place_guess` lacks its full name is still not flagged.
* **Why not check file timestamps:** modified times change on `git checkout`, `git pull` or a plain re-save, so they don't show whether names changed. They also can't say which names are new or which keyword they need. Compare file contents with `site_names.py` on every run instead.
* **Why dive-site keywords stay hand-written:** they need judgement. A bare `"simon"` matched "Cloghmac**simon**, Bandon", and a bare `"sandmount"` merged Bank Pier with Sandmount Bay Beach. Some sites also need aliases that can't be derived from the name, such as `"derreenacarrin"` for Zetland Pier, or `"bank"` for the plus-code place names.
* **TODO:**
  - [x] Make `site_names.py` read `LAND_SITES.txt` and skip any place name containing one of its entries (lower-cased).
  - [ ] Move `derrigra` from `IGNORED_KEYWORDS` into `LAND_SITES.txt`. Keep only the overseas entries (Egypt, Saudi Arabia) in `IGNORED_KEYWORDS`.
  - [x] Build `SITE_KEYWORDS` from the full names in `DIVE_SITES.txt`, keeping only short fragments and townland aliases in `SITE_ALIASES`.
  - [x] Warn for each `SITE_ALIASES` entry whose site name is not in `DIVE_SITES.txt`.
  - [ ] *(Optional)* Warn at the top of `Location_ratings.md` for a site in the file that has 0 observations and no alias, so a short-form `place_guess` isn't missed.
  - [x] Update the "Two files are easy to mix up" section of [`scripts/README.md`](scripts/README.md), which said no script reads `LAND_SITES.txt`.
* **Workflow once done:** edit a `.txt` file, run `generate_location_ratings.py`, then read the warnings at the top of the report.

---

## 4. 🟡 Handle Obscured Locations in Other Scripts
* **Problem:** iNaturalist hides the true location of threatened species from the public API (`obscured: true`), so GPS-based scripts miss them or place them at the wrong site. Only [`scripts/underwater_ireland.py`](scripts/underwater_ireland.py) handles this. Details: [`scripts/README.md`](scripts/README.md#obscured-locations).
* **Affected, wrong results:** `generate_location_ratings.py` (unmatched-cluster warning, observation missing from the site), `site_observations.py` (distance clustering), `nudibranch_ireland.py` (matches on `place_guess`, which is "Cork, IE" for obscured observations, so the site falls back to that name).
* **Affected, display only:** `species_classification.py` and `rare_birds_ireland.py` show `place_guess`, so obscured observations show a vague place such as "Cork, IE". Nothing is misplaced, but the place shown is not the real one.
* **TODO:**
  - [ ] Move the obscured-observation split from `underwater_ireland.py` into a shared helper in `generate_location_ratings.py`.
  - [ ] Use it in the other scripts, and list obscured observations separately instead of dropping them or raising an unmatched-cluster warning.
  - [ ] *(Optional)* Add a per-observation site override for obscured observations, so they can be counted on their real site.

---

## 5. 🟡 Underwater Life-List Reports: Open Items
Added with `one_and_done_ireland.py`, `rarity_by_site_ireland.py`, `gap_analysis_ireland.py` and `year_in_review.py` (see [`scripts/README.md`](scripts/README.md)).
* **Unmatched places:** "Ardra, Co. Cork" (4 observations) shows the `site_names.py` unmatched-cluster warning, so it is missing from every site-based report. Decide whether it is a dive site (add to `DIVE_SITES.txt`, plus a `SITE_ALIASES` entry if needed) or an ignored place (add to `LAND_SITES.txt`). "Union Hall, Unionhall" and "Trá an Oileáin" are now ignored places.
* **Not built yet** (ideas from the report review, none needs new API calls):
  - [ ] Seasonality: species group by month. Wait for more than one winter of data.
  - [ ] Needs ID action list (extends item 1): group the Needs ID observations by what blocks them (genus only, disagreement, one identifier).
  - [ ] Egypt trip report: the Irish reports ignore the 169 Red Sea observations.
  - [ ] Identifier credits by organism group.
* **Gap analysis is sparse:** few people post in West Cork, so most sites list under 10 nearby species. A bigger radius or a county-level comparison would give more, at the cost of relevance.
* **Dives are dates:** "best dive" and "dive days" count one date at one site, as `count_dives_per_site()` does. Two dives in a day at the same site count as one.
* **Baseline for run reports:** commit the four new reports so the next run report ([`scripts/RUN_REPORT.md`](scripts/RUN_REPORT.md)) has something to compare against.
