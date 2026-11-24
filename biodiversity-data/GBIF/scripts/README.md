# GBIF scripts

Python scripts that query the [GBIF API](https://techdocs.gbif.org/en/openapi/) for records recorded by `Andre Astra` in the iNaturalist research-grade dataset. This file is the technical reference for scripts, shared configuration and output formats. For the overview, see [`../README.md`](../README.md). API notes are in [API notes](#api-notes) below.

Run every script from the `GBIF/` directory (the parent of this one) with the shared virtualenv. See [Shared setup](../../README.md#shared-setup) for creating it.

```bash
../.venv/bin/python scripts/<script>.py
```

## Overview

| Script | Output |
|---|---|
| [`run_all.py`](#run_allpy) | all the reports below |
| [`fetch_occurrences.py`](#fetch_occurrencespy) | `scripts/.cache/occurrences.json` |
| [`gbif_summary.py`](#gbif_summarypy) | `reports/gbif_summary.md` |
| [`sync_status.py`](#sync_statuspy) | `reports/sync_status.md` |
| [`underwater_ireland.py`](#underwater_irelandpy) | `reports/underwater_ireland.md` |
| [`lough_hyne_species.py`](#lough_hyne_speciespy) | `reports/lough_hyne_species.md` |
| [`cork_underwater.py`](#cork_underwaterpy) | `reports/cork_underwater.md` |
| [`citations.py`](#citationspy) | `reports/citations.md` |

Supporting files:

| File | Purpose |
|---|---|
| [`config.py`](config.py) | Shared constants: API URLs, page sizes, `RECORDED_BY`, the iNaturalist dataset key, `OUTPUT_DIR`, `INATURALIST_SCRIPTS_DIR` (where `underwater_ireland.py` finds the iNaturalist scripts). Every script imports from it. |
| [`../reports/`](../reports) | Generated reports, for the reader. Safe to regenerate. |
| `.cache/` | Working data for the scripts, git-ignored: `occurrences.json` (the download), `species_profiles.json` (marine flags used by `lough_hyne_species.py`) and `west_cork_species.json` (marine flags and names used by `cork_underwater.py`). |

## API notes

Base URL `https://api.gbif.org/v1`. Reads need no authentication.

| Endpoint | Purpose |
|---|---|
| `/occurrence/{key}` | One occurrence record |
| `/occurrence/search` | Search occurrences (taxon, country, date, dataset, coordinates, `recordedBy`, …) |
| `/occurrence/download/request` | Large asynchronous downloads (needs a GBIF account) |
| `/species/match?name=` | Match a name to the GBIF backbone taxonomy |
| `/species/{key}` | Taxon details |
| `/dataset/{key}` | Dataset metadata |

Search results return at most 300 records per page. Deep paging stops at an offset of about 100,000. Use `limit=0` for a count only, and `facet=<field>` for counts grouped by a field.

### How GBIF differs from iNaturalist

- **Research grade only.** Needs ID observations and observations without an open licence are absent, so GBIF counts are lower than the iNaturalist ones.
- **Lag.** GBIF re-reads iNaturalist periodically. Check `lastInterpreted` on a record to see when it last synced.
- **No user id.** Records are matched by the text field `recordedBy` (`Andre Astra`), not by the iNaturalist login or ID. Linking an [ORCID iD](../../README.md#orcid) adds a real identifier once it is synced.
- **Own keys.** `taxonKey` and `speciesKey` come from the GBIF backbone and differ from iNaturalist taxon IDs. A record can carry the issue `TAXON_ID_NOT_FOUND` when the iNaturalist ID has no match; the name still resolves.
- **Rounded coordinates.** Expect the issue `COORDINATE_ROUNDED` (6 decimal places).
- **Obscured locations.** Threatened species are generalised, as on iNaturalist.

### Counts from the API (2026-11-19)

Research-grade records `recordedBy=Andre Astra` in the [iNaturalist Research-grade Observations](https://www.gbif.org/dataset/50c9509d-22c7-4a22-a47d-8c48425ef4a7) dataset:

| Country | Records |
|---|---|
| Ireland (IE) | 205 |
| Egypt (EG) | 90 |
| United Kingdom (GB) | 1 |
| Saudi Arabia (SA) | 1 |
| **Total** | **297** |

These are snapshot figures and go stale. Re-run the [handy queries](#handy-queries) for current ones.

### Handy queries

```bash
B=https://api.gbif.org/v1

# One record
curl -s "$B/occurrence/6520575999"

# Count of my records, grouped by country
curl -s "$B/occurrence/search?recordedBy=Andre%20Astra&limit=0&facet=country"

# Same species recorded by anyone in Ireland
curl -s "$B/occurrence/search?scientificName=Tubulanus%20annulatus&country=IE&limit=20"

# Match a name to the backbone
curl -s "$B/species/match?name=Tubulanus%20annulatus"

# Verify the dataset key
curl -s "$B/dataset/50c9509d-22c7-4a22-a47d-8c48425ef4a7"
```

## Scripts

### `run_all.py`
- **Purpose**: Runs every script that writes a report, with a single download of the occurrences.
- **How it works**: Calls `fetch_occurrences.refresh()` first, which keeps the occurrences in memory. The report scripts read them through `cached()` instead of calling GBIF again. A failing script doesn't stop the run; failures are listed at the end and the exit code is 1.
- **Usage**: `../.venv/bin/python scripts/run_all.py`
- **Standalone runs**: each script still works on its own. With nothing in memory it fetches from the API.

### `fetch_occurrences.py`
- **Purpose**: Downloads all of the user's occurrences from the dataset and saves them as JSON.
- **How it works**: Pages through `/occurrence/search` (300 per page) and writes the full list to `scripts/.cache/occurrences.json`, and keeps it in memory for the rest of the process.
- **Git-ignored and always regenerated**: the file goes stale as GBIF re-reads iNaturalist, so it is not tracked. Don't read it directly. Run this script, or call `refresh()`, which re-fetches from the API, rewrites the file and returns the occurrences.
- **Usage**: `../.venv/bin/python scripts/fetch_occurrences.py [--country IE]`. A `--country` fetch is saved but not kept in memory for other scripts.

### `gbif_summary.py`
- **Purpose**: Generates [`reports/gbif_summary.md`](../reports/gbif_summary.md).
- **How it works**: Counts the occurrences by country, organism group and year, counts distinct species, and lists the issues GBIF raised with a plain-language meaning. The organism group is the GBIF class, or the order or phylum where the backbone has no class (ray-finned fish, flatworms). Makes no iNaturalist calls.
- **Usage**: `../.venv/bin/python scripts/gbif_summary.py`

### `sync_status.py`
- **Purpose**: Generates [`reports/sync_status.md`](../reports/sync_status.md).
- **How it works**: Downloads the research-grade observations from the iNaturalist API (2 calls for about 340 observations) and matches them to the GBIF occurrences on the iNaturalist observation id, which GBIF keeps in `occurrenceID`. Lists the observations that are not on GBIF yet, and any GBIF record that is no longer research grade.
- **Reading it**: a missing observation is normally waiting for GBIF's next sync, which lags by days. GBIF has no date for when an observation became research grade, so the report shows iNaturalist's `updated_at`, which is an upper bound.
- **Usage**: `../.venv/bin/python scripts/sync_status.py`

### `underwater_ireland.py`
- **Purpose**: Generates [`reports/underwater_ireland.md`](../reports/underwater_ireland.md), the user's underwater observations in Ireland and which of them are on GBIF.
- **How it works**: GBIF has no habitat field, so "underwater" comes from iNaturalist. The script runs `underwater_observations()` from [`../../iNaturalist/scripts/underwater_ireland.py`](../../iNaturalist/scripts/underwater_ireland.py) in a subprocess (both folders have a `config.py`, so it can't be imported; the path is `INATURALIST_SCRIPTS_DIR` in `config.py`). That is the data set of the iNaturalist report: observations on a dive site, plus the obscured ones, at any grade. Each is matched to its GBIF occurrence on the iNaturalist observation id in `occurrenceID`.
- **Output**: totals (on GBIF, not research grade, research grade but not yet synced, other Irish records), counts by organism group, site and year, and the research-grade observations still missing from GBIF. The iNaturalist observations are downloaded live, so this script needs network access to both APIs.
- **Dependency**: if `underwater_observations()` is renamed or changes what it returns, this script breaks. Keep it in step with the iNaturalist script.
- **Usage**: `../.venv/bin/python scripts/underwater_ireland.py`

### `lough_hyne_species.py`
- **Purpose**: Generates [`reports/lough_hyne_species.md`](../reports/lough_hyne_species.md), the underwater species recorded at Lough Hyne by anyone, from every GBIF dataset.
- **How it works**: Calls `/occurrence/search` with `geometry` (`LOUGH_HYNE_POLYGON` in `config.py`, the same polygon as the website's Location filter), `occurrenceStatus=PRESENT`, `mediaType=StillImage` (only occurrences with a photo; videos and sounds do not count) and downloads the matching occurrences page by page. GBIF occurrences have no habitat field, so "underwater" comes from the taxon: a species counts when any source in `/species/{key}/speciesProfiles` (WoRMS, Catalogue of Life) marks it as marine. Birds (`Aves`) and flowering plants (`Magnoliopsida`) are left out, since GBIF marks seabirds and coastal plants as marine too (`NOT_UNDERWATER`). Seals, otters and turtles stay in the list.
- **Copies**: Explore Your Shore republishes a recorder's iNaturalist photos as records of their own (another dataset, catalogue number and coordinates), so the same photo shows twice. A record from another dataset is dropped when an iNaturalist record has the same species, recorder (ignoring accents) and date; each iNaturalist record cancels one such copy, and any extra ones stay because they may be other photos. Records without a recorder or date are never dropped. The report states how many were left out. The photos themselves are not compared.
- **Output**: the filters applied as a numbered list (with their GBIF search parameters), then a small table counting the species in each group (each group name links to its heading row in the main table), then the main table (Common name, Photos) with a row per marine species, grouped by a bold heading row with a blank line above and below it, made with `<br>` (the anchor for the group link sits in that row). The groups (fish, nudibranchs, sea snails, crustaceans and so on, from the `GROUPS` rules in the script, which use the GBIF phylum, class and order; the biggest group first, and an "Other" group if a species matches none): its common name (the first English name GBIF holds, or the scientific name where there is none) and a thumbnail (150 px high) for each record, newest first. A thumbnail comes from GBIF's image cache and opens the full-size photo when clicked. Your own records (`RECORDED_BY` in `config.py`, compared ignoring accents and case) are outlined in blue, and a species row with one of them has its common name in bold blue. The report counts both.
- **Cache**: the profiles take 2 calls per species (about 400 for the 191 species with a photo) on the first run, so they are kept in `scripts/.cache/species_profiles.json` and only new species are fetched afterwards. Delete the file to refresh them. It does not use `occurrences.json`, so `run_all.py` does not share a download with it.
- **Reading it**: the polygon takes in the shore and some land around the lough, so land records are in the totals (the marine filter drops them from the species list). To repeat the search in the GBIF website, paste the polygon into Location, Geometry; with Occurrence status set to Present and Media type set to Still image, the website's count matches the report's.
- **Usage**: `../.venv/bin/python scripts/lough_hyne_species.py`

### `cork_underwater.py`
- **Purpose**: Generates [`reports/cork_underwater.md`](../reports/cork_underwater.md), the underwater species recorded by anyone in West Cork and its coastal waters, from every GBIF dataset.
- **How it works**: It does not download the records. One `/occurrence/search` call with `geometry` (`WEST_CORK_POLYGON` in `config.py`), `occurrenceStatus=PRESENT`, `mediaType=StillImage`, `limit=0` and `facet=speciesKey` returns the photo count per species in under a second. A second call adds `recordedBy` (`RECORDED_BY`) for my own counts. The marine check and the marine filter are the same as in `lough_hyne_species.py` (a species counts when a GBIF species profile marks it as marine; `Aves` and `Magnoliopsida` are left out). Mammals and reptiles get their own group, "Seals, whales and turtles", because the shared groups would file them under fish. The polygon was drawn in the GBIF occurrence search. It replaced the GADM boundary `IRL.4.9_1`, which covers land only and so missed the coast and the sea.
- **Cache**: one `speciesProfiles` call per species for the marine flag, then the name and common names for the marine ones only. The results are kept in `scripts/.cache/west_cork_species.json` and saved every 200 species, so a stopped run loses little. Flags already in `species_profiles.json` are reused. The first run took about 3 minutes (2,215 species in the polygon). Delete the file to refresh.
- **Not in `run_all.py`**: it does not use `occurrences.json`, and the first run is slow, so it is run on its own.
- **Limits**: counts cannot remove copies of iNaturalist records that other datasets republish (that needs the recorder and date of each record), so photo counts can be a little high. There are no thumbnails and no year or dataset tables.
- **Usage**: `../.venv/bin/python scripts/cork_underwater.py`

### `citations.py`
- **Purpose**: Generates [`reports/citations.md`](../reports/citations.md), the research GBIF links to the iNaturalist dataset and to the species you recorded.
- **How it works**: Calls `/literature/search` filtered by `gbifDatasetKey` for the dataset-wide totals and facets (year, topic, researcher country, peer review, open access), and `/occurrence/download/dataset/{key}` for the download count. It then searches the same literature for the GBIF taxon keys on your records (repeated `gbifTaxonKey` parameters are an OR, 100 keys per request) and ranks the papers by how many of your species they mention. About 7 API calls (one per second) and no iNaturalist calls.
- **Direct citations**: GBIF's literature index also stores occurrence keys that papers cite explicitly, but that is rare for iNaturalist records. `/literature/search?gbifOccurrenceKey=` fails on the API (`Unknown SearchParameter data type java.lang.Long`), so the script reads the `gbifOccurrenceKey` facet over the whole index (about 1,300 cited keys) and intersects it with your occurrence keys. The script stops if the facet is truncated.
- **Reading it**: apart from direct citations, GBIF links papers to the dataset and to taxa, not to a contributor. The dataset figures cover every iNaturalist contributor. A paper that mentions a species you recorded may have used only other people's records of it.
- **Usage**: `../.venv/bin/python scripts/citations.py`
