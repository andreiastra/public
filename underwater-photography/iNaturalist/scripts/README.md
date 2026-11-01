# iNaturalist scripts

Python scripts that query the [iNaturalist API](https://api.inaturalist.org/v1/docs/) for user `andreiastra`. This file serves as the technical reference for scripts, shared configuration, and output formats. For the project-wide overview, workflows, and pending action items / TODOs, see the root [`../README.md`](../README.md).

Run every script from the `iNaturalist/` directory (the parent of this one) with the project virtualenv. See [Requirements & Setup](../README.md#requirements--setup) for creating it.

```bash
.venv/bin/python scripts/<script>.py
```

## Overview

| Script | Output |
|---|---|
| [`fetch_observations.py`](#fetch_observationspy) | `OUTPUT/observations.json` |
| [`my_places.py`](#my_placespy) | stdout |
| [`my_locations.py`](#my_locationspy) | stdout |
| [`my_projects.py`](#my_projectspy) | stdout |
| [`generate_location_ratings.py`](#generate_location_ratingspy) | `OUTPUT/Location_ratings.md` |
| [`nudibranch_ireland.py`](#nudibranch_irelandpy) | `OUTPUT/nudibranch_ireland.md` |
| [`site_observations.py`](#site_observationspy) | `OUTPUT/<site>.md` |
| [`species_classification.py`](#species_classificationpy) | `OUTPUT/species_classification.md` |
| [`underwater_ireland.py`](#underwater_irelandpy) | `OUTPUT/underwater_ireland.md` |
| [`rarity_underwater_ireland.py`](#rarity_underwater_irelandpy) | `OUTPUT/rarity_underwater_ireland.md` |
| [`rarity_underwater_worldwide.py`](#rarity_underwater_worldwidepy) | `OUTPUT/rarity_underwater_worldwide.md` |
| [`rare_birds_ireland.py`](#rare_birds_irelandpy) | stdout |

Supporting files:

| File | Purpose |
|---|---|
| [`config.py`](config.py) | Shared constants: user, API URLs, page size, clustering radius, place and taxon IDs, `OUTPUT_DIR`. Every script imports from it. |
| [`site_names.py`](site_names.py) | Keyword → canonical dive site name mapping, plus `IGNORED_KEYWORDS` for non-dive places. Names must match [`../Preferred_dive_site_names_ireland.txt`](../Preferred_dive_site_names_ireland.txt). |
| `OUTPUT/` | All generated files: reports and the observations download. Safe to regenerate. |

## Scripts

### `fetch_observations.py`
- **Purpose**: Downloads all of the user's observations and saves them as JSON.
- **How it works**: Paginates the observations API and writes the full result list to `OUTPUT/observations.json`.
- **Git-ignored and always regenerated**: the file is a snapshot that goes stale as soon as new observations are uploaded, so it is not tracked. Don't read it directly. Run this script, or call `refresh()` from `fetch_observations.py`, which re-fetches from the API, rewrites the file and returns the observations. No script currently reads the file; the others fetch live.

### `my_places.py`
- **Purpose**: Lists every distinct `place_guess` string on the user's observations.
- **How it works**: Paginates through all observations and prints place counts with links to the individual observations.

### `my_locations.py`
- **Purpose**: Groups all observations into geospatial clusters and labels each with a canonical site name. **Also used to verify [`site_names.py`](site_names.py)**: run it and check that every cluster resolves to a canonical name.
- **How it works**:
  - Greedy clustering with a 500 m radius (`CLUSTER_RADIUS_M`), using the Haversine great-circle formula.
  - Assigns site names by matching `place_guess` fragments against the keywords in [`site_names.py`](site_names.py).

### `my_projects.py`
- **Purpose**: Lists the collection and umbrella projects the user has joined.

### `generate_location_ratings.py`
- **Purpose**: Generates [`OUTPUT/Location_ratings.md`](OUTPUT/Location_ratings.md), a per-site index of dive sessions and observations with clickable photo thumbnails. Full spec: [`generate_location_ratings_REQUIREMENTS.md`](generate_location_ratings_REQUIREMENTS.md).
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
- **Output**: `OUTPUT/nudibranch_ireland.md`

### `site_observations.py`
- **Purpose**: Lists all of the user's observations at any specific dive site (or all sites with `--all`), with a species summary and photo thumbnails linked to each observation.
- **How it works**: Fetches all observations, matches `place_guess` against canonical site keywords from [`site_names.py`](site_names.py), and incorporates any observation within `CLUSTER_RADIUS_M` of the centroid.
- **Output**: `OUTPUT/<site_slug>.md` (e.g. `OUTPUT/bank_pier.md`, `OUTPUT/kilcrohane_pier.md`).
- **Usage**:
  ```bash
  .venv/bin/python scripts/site_observations.py "Bank Pier"
  .venv/bin/python scripts/site_observations.py "Kilcrohane Pier"
  .venv/bin/python scripts/site_observations.py --all
  ```

### `species_classification.py`
- **Purpose**: Generates [`OUTPUT/species_classification.md`](OUTPUT/species_classification.md), a comprehensive breakdown of user observations in Ireland categorized into clean organism types (Bird, Fish, Crab, Nudibranch, Anemone, Sponge, Jellyfish, Flatworm, etc.) with a summary table, full species list, and individual sightings with thumbnails.
- **How it works**: Fetches user observations in Ireland (`place_id=6718`), traverses taxonomic hierarchies and ancestry to classify each observation into human-friendly organism types, and produces a structured report.
- **Shared helper**: Also exports `species_type(obs)`, which is imported directly by other scripts (such as `site_observations.py`) to classify live API observation objects. Other scripts do **not** read or depend on the generated `OUTPUT/species_classification.md` file from disk.
- **Output**: `OUTPUT/species_classification.md`

### `underwater_ireland.py`
- **Purpose**: Generates [`OUTPUT/underwater_ireland.md`](OUTPUT/underwater_ireland.md), listing all of the user's underwater observations in Ireland, grouped by dive site (most observations first), with a site summary table and a photo thumbnail linked to each observation.
- **How it works**: Reuses `fetch_all_observations()`, `cluster_and_label()`, `count_dives_per_site()`, `species_per_site()` and `render_site_section()` from `generate_location_ratings.py`, so "underwater" means the observation clusters onto a site in [`../Preferred_dive_site_names_ireland.txt`](../Preferred_dive_site_names_ireland.txt). Birding and other above-water places are excluded. Non-Irish dive sites (`NON_IRELAND_SITES`, currently Scapa Flow) are dropped.
- **Obscured locations**: iNaturalist hides the true location of threatened species (for example IUCN VU) from the public API. It returns a randomised point with a public accuracy of 25 km or more, and a generic place name such as "Cork, IE". The API flags these with `obscured: true`. Such a point can't be clustered onto a dive site, and only the owner, logged in on iNaturalist, sees the real location. The script therefore:
  - Splits out every `obscured` observation before clustering, so none are placed on a site.
  - Lists them in a separate **Obscured locations** section, most threatened first (CR, EN, VU, NT), with their IUCN status.
  - Skips obscured observations at ignored places (`IGNORED_KEYWORDS`, for example the Egypt trip).
  - Doesn't count them in the site totals, only in the "with obscured location" count in the report header.

  Editing the location on iNaturalist doesn't fix this, because the species stays obscured. Check the true location on the observation page while logged in. Making the API return the real coordinates would need authentication, which the scripts avoid (see [Conventions](#conventions)).
- **Output**: `OUTPUT/underwater_ireland.md`. Unresolved clusters appear as a `⚠️` warning at the top of the report (see [Keeping places up to date](#keeping-places-up-to-date)).

### `rarity_underwater_ireland.py`
- **Purpose**: Generates [`OUTPUT/rarity_underwater_ireland.md`](OUTPUT/rarity_underwater_ireland.md), rating the user's **Research Grade** underwater taxa in Ireland by rarity, rarest first, with a thumbnail, rating, IUCN status, the user's observation count and the dive sites.
- **How it works**:
  - Gets the observations from `underwater_observations()` in [`underwater_ireland.py`](#underwater_irelandpy) and keeps `quality_grade == "research"`. Needs ID observations are ignored.
  - Rarity is the number of distinct observers with a Research Grade record of the taxon anywhere in Ireland (`/v1/observations/observers`), the same measure as `rare_birds_ireland.py` but counting Research Grade only. Ties go to the taxon with fewer Research Grade observations in Ireland.
  - Ratings: Unique (1 observer, only you), Very rare (2–5), Rare (6–20), Uncommon (21–100), Common (more than 100). Change the cut-offs in `RATINGS`.
  - Makes 2 API calls per taxon with 0.5 s between them, so a run takes a couple of minutes.
- **Obscured locations**: obscured observations (see [Obscured locations](#obscured-locations)) can't be confirmed as underwater. They are still rated, because rarity depends on the taxon, and flagged "obscured, not confirmed underwater" in the Sites column.
- **Shared code**: the fetching, ranking and rendering live in `generate_report()`, which [`rarity_underwater_worldwide.py`](#rarity_underwater_worldwidepy) reuses with a different place and measure.
- **Output**: `OUTPUT/rarity_underwater_ireland.md`

### `rarity_underwater_worldwide.py`
- **Purpose**: Generates [`OUTPUT/rarity_underwater_worldwide.md`](OUTPUT/rarity_underwater_worldwide.md), the same Research Grade underwater observations as the Ireland report, but ranked against the number of Research Grade observations **worldwide**.
- **How it works**:
  - Calls `generate_report()` from [`rarity_underwater_ireland.py`](#rarity_underwater_irelandpy) with no `place_id` (worldwide) and `metric="total"`. Only the comparison changes, so the same observations and obscured-location handling apply.
  - Rarity is the worldwide count of Research Grade observations of the taxon, fewest first. Ties go to the taxon with fewer distinct observers worldwide.
  - Ratings use a log scale, because worldwide counts are far larger: Unique (1 observation, only yours), Very rare (2–100), Rare (101–1,000), Uncommon (1,001–10,000), Common (more than 10,000). Change the cut-offs in `RATINGS`.
  - Makes 2 API calls per taxon with 0.5 s between them, so a run takes a couple of minutes.
- **Reading it next to the Ireland report**: a taxon can be rare in Ireland and common worldwide (Sand Smelt: 3 observers in Ireland, 177 observations worldwide), or the reverse. The two reports answer different questions.
- **Output**: `OUTPUT/rarity_underwater_worldwide.md`

### `rare_birds_ireland.py`
- **Purpose**: Ranks the user's Irish bird species by rarity, measured as the number of **distinct observers** who have recorded the species anywhere in Ireland on iNaturalist (fewest observers = rarest).
- **How it works**:
  - Paginates through the user's bird (Aves) observations in Ireland.
  - Collects each unique taxon, then queries `/v1/observations/observers` once per taxon for its Ireland-wide observer count (0.5 s between requests).
  - Prints a ranked table: rarest species first, with dates, locations and the user's observation count.

## Shared code

- **Constants**: import them from `config.py`. Don't redefine `USER_ID`, URLs or IDs in a script.
- **Helpers**:
  - `fetch_all_observations()`, `haversine()`, and `photo_md()` come from `generate_location_ratings.py`.
  - `species_type()` comes from `species_classification.py`.
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
- Clustering by distance (`cluster_and_label()`, `at_site()`, `my_locations.py`) leaves these observations unmatched, or can place them at the wrong site.
- Site counts, dive counts and species lists silently miss them.
- Editing the location on iNaturalist doesn't help, because the species stays obscured whatever you enter.

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
- Write every generated file to `OUTPUT_DIR` (`scripts/OUTPUT/`), never next to the sources.

## Keeping places up to date

Places change occasionally, so nothing runs on a schedule. `OUTPUT/Location_ratings.md` is only as current as its last run.

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

Then regenerate and check that the warning is gone.

**Two files are easy to mix up:**

- [`../Preferred_dive_site_names_ireland.txt`](../Preferred_dive_site_names_ireland.txt) is read by `generate_location_ratings.py`. Every entry listed here is treated as a distinct dive site and generates an output section in `Location_ratings.md`. Do not place townland aliases or alternate site names here if they map to another canonical site in `site_names.py` (otherwise they will render as empty 0-observation entries).
- [`../Preferred_other_location_names.txt`](../Preferred_other_location_names.txt) is a reference list for you only. No script reads it. Adding a place there does not silence a warning, so add the keyword to `IGNORED_KEYWORDS` as well.

**Keyword rules** (details in the [`site_names.py`](site_names.py) docstring):
- Put longer, more specific keywords first (`bank pier` before `bank`).
- Keywords are matched as lower-case substrings of `place_guess`.
- Canonical names must match `Preferred_dive_site_names_ireland.txt` exactly.

To check how observations are grouped, run `.venv/bin/python scripts/my_locations.py`. It prints each cluster with its resolved name.

Currently ignored: the Egypt trip (`egypt`, `janub sina`, `saudi arabia`, `sharm el sheikh`), plus Clonakilty, Coolanagh, Courtmacsherry, Derrigra and Rosscarbery.
