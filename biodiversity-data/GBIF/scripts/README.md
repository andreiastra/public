# GBIF scripts

Python scripts that query the [GBIF API](https://techdocs.gbif.org/en/openapi/) for records recorded by `Andre Astra` in the iNaturalist research-grade dataset. This file is the technical reference for scripts, shared configuration and output formats. For the overview and API notes, see [`../README.md`](../README.md).

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
| [`citations.py`](#citationspy) | `reports/citations.md` |

Supporting files:

| File | Purpose |
|---|---|
| [`config.py`](config.py) | Shared constants: API URLs, page sizes, `RECORDED_BY`, the iNaturalist dataset key, `OUTPUT_DIR`, `INATURALIST_SCRIPTS_DIR` (where `underwater_ireland.py` finds the iNaturalist scripts). Every script imports from it. |
| [`../reports/`](../reports) | Generated reports, for the reader. Safe to regenerate. |
| `.cache/` | Working data for the scripts, git-ignored: `occurrences.json` (the download). |

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

### `citations.py`
- **Purpose**: Generates [`reports/citations.md`](../reports/citations.md), the research GBIF links to the iNaturalist dataset and to the species you recorded.
- **How it works**: Calls `/literature/search` filtered by `gbifDatasetKey` for the dataset-wide totals and facets (year, topic, researcher country, peer review, open access), and `/occurrence/download/dataset/{key}` for the download count. It then searches the same literature for the GBIF taxon keys on your records (repeated `gbifTaxonKey` parameters are an OR, 100 keys per request) and ranks the papers by how many of your species they mention. About 7 API calls (one per second) and no iNaturalist calls.
- **Direct citations**: GBIF's literature index also stores occurrence keys that papers cite explicitly, but that is rare for iNaturalist records. `/literature/search?gbifOccurrenceKey=` fails on the API (`Unknown SearchParameter data type java.lang.Long`), so the script reads the `gbifOccurrenceKey` facet over the whole index (about 1,300 cited keys) and intersects it with your occurrence keys. The script stops if the facet is truncated.
- **Reading it**: apart from direct citations, GBIF links papers to the dataset and to taxa, not to a contributor. The dataset figures cover every iNaturalist contributor. A paper that mentions a species you recorded may have used only other people's records of it.
- **Usage**: `../.venv/bin/python scripts/citations.py`
