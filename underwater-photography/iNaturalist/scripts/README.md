# iNaturalist scripts

Python scripts that query the [iNaturalist API](https://api.inaturalist.org/v1/docs/) for user `andreiastra`. This file serves as the technical reference for scripts, shared configuration, and output formats. For the project-wide overview, workflows, and pending action items / TODOs, see the root [`../README.md`](../README.md).

Run every script from the `iNaturalist/` directory (the parent of this one) with the project virtualenv. See [Requirements & Setup](../README.md#requirements--setup) for creating it.

```bash
.venv/bin/python scripts/<script>.py
```

## Overview

| Script | Output |
|---|---|
| [`run_all.py`](#run_allpy) | all the reports below |
| [`fetch_observations.py`](#fetch_observationspy) | `scripts/.cache/observations.json` |
| [`generate_location_ratings.py`](#generate_location_ratingspy) | `reports/Location_ratings.md` |
| [`nudibranch_ireland.py`](#nudibranch_irelandpy) | `reports/nudibranch_ireland.md` |
| [`site_observations.py`](#site_observationspy) | `reports/sites/<site_name>.md` |
| [`species_classification.py`](#species_classificationpy) | `reports/species_classification.md` |
| [`underwater_ireland.py`](#underwater_irelandpy) | `reports/underwater_ireland.md` |
| [`rarity_underwater_ireland.py`](#rarity_underwater_irelandpy) | `reports/rarity_underwater_ireland.md` |
| [`rarity_underwater_worldwide.py`](#rarity_underwater_worldwidepy) | `reports/rarity_underwater_worldwide.md` |
| [`rare_birds_ireland.py`](#rare_birds_irelandpy) | `reports/rare_birds_ireland.md` |
| [`one_and_done_ireland.py`](#one_and_done_irelandpy) | `reports/one_and_done_ireland.md` |
| [`rarity_by_site_ireland.py`](#rarity_by_site_irelandpy) | `reports/rarity_by_site_ireland.md` |
| [`gap_analysis_ireland.py`](#gap_analysis_irelandpy) | `reports/gap_analysis_ireland.md` |
| [`year_in_review.py`](#year_in_reviewpy) | `reports/year_in_review.html` |

Supporting files:

| File | Purpose |
|---|---|
| [`config.py`](config.py) | Shared constants: user, API URLs, page size, clustering radius, place and taxon IDs, `OUTPUT_DIR`. Every script imports from it. |
| [`site_names.py`](site_names.py) | Keyword → canonical dive site name mapping, plus `IGNORED_KEYWORDS` for non-dive places. Names must match [`../Preferred_dive_site_names_ireland.txt`](../Preferred_dive_site_names_ireland.txt). |
| [`underwater_stats.py`](underwater_stats.py) | Shared data preparation for the four underwater life-list reports (`one_and_done_ireland.py`, `rarity_by_site_ireland.py`, `gap_analysis_ireland.py`, `year_in_review.py`): underwater observations as `(site, obs)` entries, a species table (species rank only), and dives. Defines functions only. |
| [`../reports/`](../reports) | Generated reports, for the reader. Safe to regenerate. |
| `.cache/` | Working data for the scripts, git-ignored: `observations.json` (the download), `taxon_counts.json` (per-taxon rarity counts, 90 days) and `site_species.json` (species recorded near each dive site, 30 days, used by the gap analysis). |

## Scripts

### `run_all.py`
- **Purpose**: Runs every script that writes a report, in one go, with a single download of the observations.
- **How it works**: Calls `fetch_observations.refresh()` first, which keeps the observations in memory. The other scripts read them through `fetch_all_observations()` instead of calling the API again, and the Ireland, nudibranch and bird scripts filter the list locally. The rarity scripts (including the birds and `rarity_by_site_ireland.py`) make 2 API calls per taxon that isn't in the 90-day cache. `gap_analysis_ireland.py` makes at least 2 calls per dive site that isn't in its 30-day cache (more for sites with many nearby observations). `one_and_done_ireland.py` makes no calls. `year_in_review.py` only needs counts for the species in the 90-day cache, so in a full run it makes none; run on its own it fetches any that are missing.
- **Order**: the four underwater life-list scripts (`one_and_done_ireland.py`, `rarity_by_site_ireland.py`, `gap_analysis_ireland.py`, `year_in_review.py`) run after the rarity reports, so they reuse the counts those just cached. `site_observations.py --all` (writes `reports/sites/`) runs last. A failing script doesn't stop the run; failures are listed at the end and the exit code is 1.
- **Usage**: `.venv/bin/python scripts/run_all.py`
- **Standalone runs**: each script still works on its own. With nothing in memory it fetches from the API as before.
- **Run reports**: after a full run, write up what changed in [`../reports/runs/`](../reports/runs). The procedure is in [`RUN_REPORT.md`](RUN_REPORT.md).

### `fetch_observations.py`
- **Purpose**: Downloads all of the user's observations and saves them as JSON.
- **How it works**: Paginates the observations API and writes the full result list to `scripts/.cache/observations.json`, and keeps it in memory for the rest of the process.
- **Git-ignored and always regenerated**: the file is a snapshot that goes stale as soon as new observations are uploaded, so it is not tracked. Don't read it directly. Run this script, or call `refresh()` from `fetch_observations.py`, which re-fetches from the API, rewrites the file and returns the observations.
- **Helpers**: `cached()` returns the observations in memory (or `None`). `in_ireland()`, `nudibranchs_in_ireland()` and `birds_in_ireland()` give the same results as the API's `place_id` and `taxon_id` filters.

### `generate_location_ratings.py`
- **Purpose**: Generates [`reports/Location_ratings.md`](../reports/Location_ratings.md), a per-site index of dive sessions and observations with clickable photo thumbnails. Full spec: [`generate_location_ratings_REQUIREMENTS.md`](generate_location_ratings_REQUIREMENTS.md).
- **How it works**:
  - Fetches all observations and clusters them (500 m radius).
  - Resolves each cluster to a canonical site name via [`site_names.py`](site_names.py).
  - Counts distinct observation dates per site as a proxy for dive sessions.
  - Renders each observation as a linked `/small.jpg` thumbnail pointing to its iNaturalist page.
- **Prerequisite**: Verify [`site_names.py`](site_names.py) is current (see [Keeping places up to date](#keeping-places-up-to-date)).
- **Shared helpers**: also defines `fetch_all_observations()`, `haversine()` and `photo_md()`, which other scripts import. Importing the module only defines functions and doesn't run a report.

### `nudibranch_ireland.py`
- **Purpose**: Lists the user's nudibranch (order Nudibranchia) observations in Ireland, grouped by dive site, with a photo thumbnail and a link to each observation.
- **How it works**: Filters the observations API by the nudibranch `taxon_id` and Ireland `place_id`, resolves each place to a site name via [`site_names.py`](site_names.py), and writes a site summary table and an observation table.
- **Output**: `reports/nudibranch_ireland.md`

### `site_observations.py`
- **Purpose**: Lists all of the user's observations at any specific dive site (or all sites with `--all`), with a species summary and photo thumbnails linked to each observation.
- **How it works**: Fetches all observations, matches `place_guess` against canonical site keywords from [`site_names.py`](site_names.py), and incorporates any observation within `CLUSTER_RADIUS_M` of the centroid.
- **Output**: `reports/sites/<site_name>.md` (e.g. `reports/sites/bank_pier.md`, `reports/sites/kilcrohane_pier.md`).
- **Usage**:
  ```bash
  .venv/bin/python scripts/site_observations.py "Bank Pier"
  .venv/bin/python scripts/site_observations.py "Kilcrohane Pier"
  .venv/bin/python scripts/site_observations.py --all
  ```

### `species_classification.py`
- **Purpose**: Generates [`reports/species_classification.md`](../reports/species_classification.md), a comprehensive breakdown of user observations in Ireland categorized into clean organism types (Bird, Fish, Crab, Nudibranch, Anemone, Sponge, Jellyfish, Flatworm, etc.) with a summary table, full species list, and individual sightings with thumbnails.
- **How it works**: Fetches user observations in Ireland (`place_id=6718`), traverses taxonomic hierarchies and ancestry to classify each observation into human-friendly organism types, and produces a structured report.
- **Shared helper**: Also exports `species_type(obs)`, which is imported directly by other scripts (such as `site_observations.py`) to classify live API observation objects. Other scripts do **not** read or depend on the generated `reports/species_classification.md` file from disk.
- **Output**: `reports/species_classification.md`

### `underwater_ireland.py`
- **Purpose**: Generates [`reports/underwater_ireland.md`](../reports/underwater_ireland.md), listing all of the user's underwater observations in Ireland, grouped by dive site (most observations first), with a site summary table and a photo thumbnail linked to each observation.
- **How it works**: Reuses `fetch_all_observations()`, `cluster_and_label()`, `count_dives_per_site()`, `species_per_site()` and `render_site_section()` from `generate_location_ratings.py`, so "underwater" means the observation clusters onto a site in [`../Preferred_dive_site_names_ireland.txt`](../Preferred_dive_site_names_ireland.txt). Birding and other above-water places are excluded. Non-Irish dive sites (`NON_IRELAND_SITES`, currently Scapa Flow) are dropped.
- **Obscured locations**: the reference implementation of the handling described in [Obscured locations](#obscured-locations). The script:
  - Splits out every `obscured` observation before clustering, so none are placed on a site.
  - Lists them in a separate **Obscured locations** section, most threatened first (CR, EN, VU, NT), with their IUCN status.
  - Skips obscured observations at ignored places (`IGNORED_KEYWORDS`, for example the Egypt trip).
  - Doesn't count them in the site totals, only in the "with obscured location" count in the report header.
- **Output**: `reports/underwater_ireland.md`. Unresolved clusters appear as a `⚠️` warning at the top of the report (see [Keeping places up to date](#keeping-places-up-to-date)).

### `rarity_underwater_ireland.py`
- **Purpose**: Generates [`reports/rarity_underwater_ireland.md`](../reports/rarity_underwater_ireland.md), rating the user's **Research Grade** underwater taxa in Ireland by rarity, rarest first, with a thumbnail, rating, IUCN status, the user's observation count and the dive sites.
- **How it works**:
  - Gets the observations from `underwater_observations()` in [`underwater_ireland.py`](#underwater_irelandpy) and keeps `quality_grade == "research"`. Needs ID observations are ignored.
  - Rarity is the number of distinct observers with a verifiable record (`verifiable=true`: Research Grade or Needs ID) of the taxon anywhere in Ireland (`/v1/observations/observers`). This matches the count on the iNaturalist taxon page. Counting Research Grade only would undercount taxa such as fish that mostly stay at Needs ID. Ties go to the taxon with fewer verifiable observations in Ireland.
  - Ratings: Unique (1 observer, only you), Very rare (2–5), Rare (6–20), Uncommon (21–100), Common (more than 100). Change the cut-offs in `RATINGS`.
  - Makes 2 API calls per taxon with 0.5 s between them, so an uncached run takes a couple of minutes. The counts are cached in `scripts/.cache/taxon_counts.json` for 90 days (change `COUNTS_MAX_AGE`), so a normal run only fetches taxa that are new or stale and takes seconds. Run with `--refresh` to fetch every count again.
- **Obscured locations**: obscured observations (see [Obscured locations](#obscured-locations)) can't be confirmed as underwater. They are still rated, because rarity depends on the taxon, and flagged "obscured, not confirmed underwater" in the Sites column.
- **Shared code**: the fetching, ranking and rendering live in `generate_report()`, which [`rarity_underwater_worldwide.py`](#rarity_underwater_worldwidepy) reuses with a different place and measure.
- **Output**: `reports/rarity_underwater_ireland.md`

### `rarity_underwater_worldwide.py`
- **Purpose**: Generates [`reports/rarity_underwater_worldwide.md`](../reports/rarity_underwater_worldwide.md), the same Research Grade underwater observations as the Ireland report, but ranked against the number of verifiable observations **worldwide**.
- **How it works**:
  - Calls `generate_report()` from [`rarity_underwater_ireland.py`](#rarity_underwater_irelandpy) with no `place_id` (worldwide) and `metric="total"`. Only the comparison changes, so the same observations and obscured-location handling apply.
  - Rarity is the worldwide count of verifiable observations of the taxon, fewest first. Ties go to the taxon with fewer distinct observers worldwide.
  - Ratings use a log scale, because worldwide counts are far larger: Unique (1 observation, only yours), Very rare (2–100), Rare (101–1,000), Uncommon (1,001–10,000), Common (more than 10,000). Change the cut-offs in `RATINGS`.
  - Makes 2 API calls per taxon with 0.5 s between them. Uses the same count cache as the Ireland report (worldwide entries are stored separately) and also accepts `--refresh`.
- **Reading it next to the Ireland report**: a taxon can be rare in Ireland and common worldwide (Sand Smelt: 10 observers in Ireland, 503 observations worldwide), or the reverse. The two reports answer different questions.
- **Output**: `reports/rarity_underwater_worldwide.md`

### `rare_birds_ireland.py`
- **Purpose**: Generates [`reports/rare_birds_ireland.md`](../reports/rare_birds_ireland.md), ranking the user's Irish bird species by rarity, measured as the number of **distinct observers** with a verifiable record of the species anywhere in Ireland on iNaturalist (fewest observers = rarest).
- **How it works**:
  - Takes the user's bird (Aves) observations in Ireland from the shared download (`birds_in_ireland()`), or from the API when run on its own. All grades are included.
  - Collects each unique taxon and gets its Ireland-wide counts with `cached_counts()` from [`rarity_underwater_ireland.py`](#rarity_underwater_irelandpy), so it uses the same measure, the same rating cut-offs (`RATINGS`) and the same `taxon_counts.json` cache. Accepts `--refresh`.
  - Writes a ranked table: rarest species first, with thumbnail, rating, Ireland observers and observations, the user's observation count, and dated links and places.
- **Output**: `reports/rare_birds_ireland.md`

### `one_and_done_ireland.py`
- **Purpose**: Generates [`reports/one_and_done_ireland.md`](../reports/one_and_done_ireland.md), the underwater species in Ireland recorded in exactly one observation.
- **How it works**: Uses [`underwater_stats.py`](underwater_stats.py), so the observations are the same as in `underwater_ireland.py`. A species counts only when an observation is identified to species rank, at any grade. The report shows the share by organism type (`species_type()`), by site, and a photo table per site with the grade.
- **Output**: `reports/one_and_done_ireland.md`. No API calls beyond the shared download.

### `rarity_by_site_ireland.py`
- **Purpose**: Generates [`reports/rarity_by_site_ireland.md`](../reports/rarity_by_site_ireland.md), which sites give the rare finds.
- **How it works**: Takes Research Grade, species-rank observations, rates each species with the same Ireland-wide observer count, `RATINGS` and `taxon_counts.json` cache as [`rarity_underwater_ireland.py`](#rarity_underwater_irelandpy), and counts per site how many species fall in each rating. Also lists the 30 rarest finds. Obscured observations are in the rarest-finds table as "Obscured location" and left out of the site table.
- **Output**: `reports/rarity_by_site_ireland.md`. Accepts `--refresh`. Makes API calls only for species not already in the cache.

### `gap_analysis_ireland.py`
- **Purpose**: Generates [`reports/gap_analysis_ireland.md`](../reports/gap_analysis_ireland.md), the species other observers have recorded near each of your dive sites that are "New for you".
- **How it works**: For each site, takes the centroid of your observations there and calls `/v1/observations/species_counts` with a 1 km radius, `quality_grade=research` and `without_taxon_id=LAND_TAXON_IDS` to get the species. It then pages through `/v1/observations` with the same filters to collect the observation links for each species. Only species that are not on your Irish underwater list at any site ("New for you") are listed; species you have recorded at another site are skipped. The "Organism type" column comes from `species_type()` in [`species_classification.py`](species_classification.py).
- **Land exclusion**: `LAND_TAXON_IDS` in [`config.py`](config.py) is a fixed list of 12 broad taxon IDs: plants, fungi, insects, arachnids, birds, mammals, reptiles, amphibians, land snails and slugs, woodlice, myriapods and earthworms. iNaturalist drops each listed taxon with all its descendants, so the filter works on whole groups, not on habitat. That means marine mammals and seabirds are excluded too, while land species outside these groups stay in. It applies only to other observers' records; your own list is never filtered. To change what is excluded, edit the list and run with `--refresh`.
- **Limits**: West Cork has few observers, so most sites list only a handful of species. The radius includes shore and intertidal records. A site showing nothing new means you have recorded everything nearby, or nobody has posted there. Obscured observations have no site, so they don't move a site's centroid or count towards "you have".
- **Cache**: `scripts/.cache/site_species.json`, 30 days per site (the species request plus one request per 200 nearby observations, so a first run takes a few minutes). Accepts `--refresh`.
- **Output**: `reports/gap_analysis_ireland.md`

### `year_in_review.py`
- **Purpose**: Generates [`reports/year_in_review.html`](../reports/year_in_review.html), a one-page, static HTML summary of the underwater life list in Ireland.
- **How it works**: Same observations as the reports above. Shows totals, the best dive (most species on one date at one site), the rarest find (Ireland-wide observers, from the shared `taxon_counts.json` cache), the most photographed site, the share of dives on Saturdays and of observations before noon, monthly growth of the species list, and the users who identified most of your observations.
- **Output**: `reports/year_in_review.html`. No scripts, no external resources.

## Shared code

- **Constants**: import them from `config.py`. Don't redefine `USER_ID`, URLs or IDs in a script.
- **Helpers**:
  - `fetch_all_observations()`, `haversine()`, and `photo_md()` come from `generate_location_ratings.py`.
  - `species_type()` comes from `species_classification.py`.
  - `underwater_entries()`, `species_table()`, `dives()`, `site_label()`, `taxon_link()`, `weekday()` and `pct()` come from [`underwater_stats.py`](underwater_stats.py). `underwater_entries()` returns `(site, obs)` pairs for every underwater observation in Ireland, with `site` set to `None` for obscured ones. `species_table()` keeps species rank only, so genus-level observations are not counted as species. A "dive" is one date at one site, the same proxy `count_dives_per_site()` uses.
  - `cached_counts()`, `load_counts_cache()`, `save_counts_cache()` and `rating()` come from `rarity_underwater_ireland.py`.
- **Site names**: `site_names.py` is imported directly where needed. It is not re-exported through `config.py`.

## Verify place and taxon IDs

A wrong `place_id` or `taxon_id` raises no error. The API returns data for a different place or taxon. For example, `6788` is Chuquisaca, Bolivia, not Ireland (Ireland is `6718`). Confirm an ID before adding it to `config.py`:

```bash
# Find a place or taxon by name
curl -s "https://api.inaturalist.org/v1/places/autocomplete?q=Ireland"
curl -s "https://api.inaturalist.org/v1/taxa?q=Nudibranchia&rank=order"

# Confirm what an ID is
curl -s "https://api.inaturalist.org/v1/places/6718"
```

Put the source URL in a comment beside the constant, for example `https://www.inaturalist.org/places/6718`.

## Obscured locations

**Any script that uses `geojson.coordinates` or `place_guess` gets wrong locations for threatened species.** iNaturalist hides the true location of these observations from the public API (flagged `obscured: true`, and `taxon_geoprivacy` is `obscured`). It returns a randomised point instead, with a public accuracy of 25 km or more, and a generic place name such as "Cork, IE".

| What the script sees | What is true |
|---|---|
| A point several km from the dive site | The dive was at the site |
| `place_guess` "Cork, IE" | The owner sees "Kilcrohane, Co. Cork, Ireland" |
| `public_positional_accuracy` ≈ 26 000 m | `positional_accuracy` is 15 m |

Example: the Nursehound (IUCN VU), [observation 407269590](https://www.inaturalist.org/observations/407269590), was 10 km from the Kilcrohane Pier cluster.

**Consequences:**
- Clustering by distance (`cluster_and_label()`, `at_site()`) leaves these observations unmatched, or can place them at the wrong site.
- Site counts, dive counts and species lists silently miss them.
- `generate_location_ratings.py` raises an unmatched-cluster `⚠️` warning for each one, such as `1 obs near “Cork, IE”`.

**What doesn't fix it:** editing the location or place name on iNaturalist. The species stays obscured whatever you enter. To see the true location, open the observation page while logged in as the owner.

**How to handle it:**
- Test `obs.get("obscured")` before using coordinates, and report these observations separately instead of dropping them. [`underwater_ireland.py`](#underwater_irelandpy) is the reference implementation.
- Don't treat IUCN status as the test. Some threatened species aren't obscured (the NT European Seabass at Zetland Pier), and some obscured species have no IUCN status.
- Getting real coordinates needs an authenticated request as the owner. The scripts avoid this on purpose (see [Conventions](#conventions)).

Scripts that don't handle this yet are tracked in [`../TODO.md`](../TODO.md).

## Conventions

- Paginate with `per_page=200` until `total_results` is reached.
- Sleep about 1 second between pages (`THROTTLE_S` in `config.py`).
- Use `timeout=30` on requests.
- No authentication is needed for public read access. The catch is that threatened species come back with [obscured locations](#obscured-locations).
- Write every generated file to `OUTPUT_DIR` (`reports/`), never next to the sources.

## Keeping places up to date

Places change occasionally, so nothing runs on a schedule. `reports/Location_ratings.md` is only as current as its last run.

**Regenerate it** after you add or rename a place, or after a batch of new observations:

```bash
.venv/bin/python scripts/generate_location_ratings.py
```

Then read the `⚠️` warning block at the top of the generated file. Each entry is a cluster of observations that matched neither a dive site nor an ignored place. No warning means every observation is accounted for.

**Fix a warning** by choosing one of these:

| The cluster is… | Do this |
|---|---|
| A dive site | Add the name to [`../Preferred_dive_site_names_ireland.txt`](../Preferred_dive_site_names_ireland.txt), then add a keyword for it to `SITE_KEYWORDS` in [`site_names.py`](site_names.py). |
| Not a dive site (birding, a trip abroad, a village) | Add a keyword to `IGNORED_KEYWORDS` in [`site_names.py`](site_names.py). |
| Logged under a generic place name, such as "Cork, Co. Cork, Ireland" | Rename the place on iNaturalist first, then add a keyword for the new name. A keyword can't safely match a generic name. |
| Logged as "Cork, IE" and the species is threatened (for example a VU Nursehound) | Nothing to fix. The location is [obscured](#obscured-locations), so the warning stays until `generate_location_ratings.py` handles these (see [`../TODO.md`](../TODO.md)). |

Then regenerate and check that the warning is gone.

**Two files are easy to mix up:**

- [`../Preferred_dive_site_names_ireland.txt`](../Preferred_dive_site_names_ireland.txt) is read by `generate_location_ratings.py`. Every entry listed here is treated as a distinct dive site and generates an output section in `Location_ratings.md`. Do not place townland aliases or alternate site names here if they map to another canonical site in `site_names.py` (otherwise they will render as empty 0-observation entries).
- [`../Preferred_other_location_names.txt`](../Preferred_other_location_names.txt) is a reference list for you only. No script reads it. Adding a place there does not silence a warning, so add the keyword to `IGNORED_KEYWORDS` as well.

**Keyword rules** (details in the [`site_names.py`](site_names.py) docstring):
- Put longer, more specific keywords first (`bank pier` before `bank`).
- Keywords are matched as lower-case substrings of `place_guess`.
- Canonical names must match `Preferred_dive_site_names_ireland.txt` exactly.

To check how observations are grouped, read the `⚠️` warning block at the top of `reports/Location_ratings.md`. It lists each cluster that didn't resolve, with a sample `place_guess`.

Currently ignored: the Egypt trip (`egypt`, `janub sina`, `saudi arabia`, `sharm el sheikh`), plus Clonakilty, Coolanagh, Courtmacsherry, Derrigra and Rosscarbery.
