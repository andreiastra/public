# Matching Dives & Places

Scripts that cross-reference Suunto Eon Core dive logs (`dive-logs/workouts/`) against live [iNaturalist](https://www.inaturalist.org) observations and canonical site names in [`../Preferred_dive_site_names_ireland.txt`](../Preferred_dive_site_names_ireland.txt).

This file serves as the technical reference for matching scripts and review datasets. For project-wide workflows and action items, see the root [`../README.md`](../README.md).

---

## Scripts & Output Datasets

### 1. `export_unmatched_dives.py`
- **Purpose**: Normalizes dive `<desc>` tags from Suunto GPX workout files and maps them against canonical site names in `Preferred_dive_site_names_ireland.txt`.
- **How It Works**:
  - Scans all `.gpx` files in `dive-logs/workouts/`.
  - Normalizes text (smart quotes, apostrophes, lowercasing, and stripping 'Pier' suffixes).
  - Handles common aliases (e.g., `7 Heads` $\rightarrow$ `Seven Heads Pier`, `Barloque` $\rightarrow$ `Barloge Pier`, `Cantys` $\rightarrow$ `Canty's Cove`).
  - Identifies unmatched dive logs (empty descriptions, overseas trips, or unlisted local sites).
- **Output**: [`unmatched_dives.json`](unmatched_dives.json)
- **Execution**:
  ```bash
  .venv/bin/python matching-dives-and-places/export_unmatched_dives.py
  ```

### 2. `export_unmatched.py`
- **Purpose**: Cross-references iNaturalist observation dates against Suunto dive dates.
- **How It Works**:
  - Fetches all user observations live from the iNaturalist REST API.
  - Compares observation dates with dive dates extracted from Suunto GPX files.
  - Filters out non-diving observations (e.g. terrestrial birds, shore fauna, or moths) for review.
- **Output**: [`unmatched_observations.json`](unmatched_observations.json)
- **Execution**:
  ```bash
  .venv/bin/python matching-dives-and-places/export_unmatched.py
  ```
