# Underwater Photography & iNaturalist Integration

This repository contains tools, data pipelines, and reporting scripts for cataloging underwater photography, managing dive logs from the Suunto Eon Core dive computer, and linking records to [iNaturalist](https://www.inaturalist.org) observations.

---

## Directory Overview

```text
iNaturalist/
├── Preferred_location_names.txt       # Canonical preferred names for West Cork dive sites
├── Location_ratings.md                # Dive site ratings, accessibility notes, and descriptions
├── Overview.md                        # Summary overview of dive sites and observed species
├── observations_raw.json              # Cached raw observations fetched from iNaturalist API
├── dive-highlights-west-cork.html     # Generated HTML report highlighting standout marine sightings
├── generate_dive_highlights_HOW_IT_WORKS.md # Technical documentation for HTML report generation
│
├── my_locations.py                    # Clusters observations into dive sites via geospatial radius
├── my_places.py                       # Lists all distinct places from user observations
├── my_projects.py                     # Lists joined iNaturalist projects
├── generate_dive_highlights.py        # Generates the standalone HTML report
│
└── dive-logs/                         # Suunto dive computer logs and correlation tools
    ├── README.md                      # Dive logs architecture and matching documentation
    ├── workouts/                      # Raw .gpx and .fit files exported from Suunto Eon Core
    ├── generate_dives_table.py        # Generates dives_table.md index from workouts
    ├── export_unmatched_dives.py      # Identifies dive workouts with unmapped locations
    ├── export_unmatched.py            # Identifies observations recorded on non-diving days
    ├── dives_table.md                 # Complete index of recorded dive workouts
    ├── unmatched_dives.json           # Review dataset of unmapped dive sites
    └── unmatched_observations.json    # Review dataset of non-dive observations
```

---

## Core Scripts Documentation

### 1. `my_locations.py`
- **Purpose**: Fetches all observations for the user (`andreiastra`) from iNaturalist and groups them into geospatial clusters.
- **How It Works**:
  - Uses a greedy clustering algorithm with a 500-metre radius (calculated via the Haversine great-circle formula).
  - Assigns canonical site names by matching `place_guess` fragments against [`Preferred_location_names.txt`](Preferred_location_names.txt).
- **Execution**:
  ```bash
  .venv/bin/python my_locations.py
  ```

### 2. `generate_dive_highlights.py`
- **Purpose**: Generates the standalone, interactive [`dive-highlights-west-cork.html`](dive-highlights-west-cork.html) summary report.
- **How It Works**:
  - Fetches observation records and high-resolution photo URLs via the iNaturalist REST API.
  - Groups sightings into curated dive sites (excluding terrestrial and birding spots like Rosscarbery and Coolanagh).
  - Formats species cards, hero image banners, and standout sightings into a self-contained HTML page.
- **Execution**:
  ```bash
  .venv/bin/python generate_dive_highlights.py
  ```

### 3. `my_places.py`
- **Purpose**: Fetches and aggregates all distinct `place_guess` strings associated with observations.
- **How It Works**: Paginates through all user observations and outputs place counts with links to individual observations.
- **Execution**:
  ```bash
  .venv/bin/python my_places.py
  ```

### 4. `my_projects.py`
- **Purpose**: Retrieves all iNaturalist collection and umbrella projects joined by the user.
- **Execution**:
  ```bash
  .venv/bin/python my_projects.py
  ```

---

## Dive Logs & Telemetry Scripts (`dive-logs/`)

The [`dive-logs/`](dive-logs) subfolder manages telemetry and workout logs downloaded from the Suunto Eon Core dive computer.

### 1. `dive-logs/generate_dives_table.py`
- **Purpose**: Parses all `.gpx` files in `dive-logs/workouts/` to build a chronological markdown table of all dive sessions.
- **Output**: [`dive-logs/dives_table.md`](dive-logs/dives_table.md)
- **Execution**:
  ```bash
  .venv/bin/python dive-logs/generate_dives_table.py
  ```

### 2. `dive-logs/export_unmatched_dives.py`
- **Purpose**: Normalizes dive `<desc>` tags and maps them against canonical site names in `Preferred_location_names.txt`.
- **How It Works**: Handles character normalization (smart quotes, apostrophes), case-insensitivity, and aliases (`7 Heads` $\rightarrow$ `Seven Heads Pier`, `Barloque` $\rightarrow$ `Barloge Pier`).
- **Output**: [`dive-logs/unmatched_dives.json`](dive-logs/unmatched_dives.json)
- **Execution**:
  ```bash
  .venv/bin/python dive-logs/export_unmatched_dives.py
  ```

### 3. `dive-logs/export_unmatched.py`
- **Purpose**: Cross-references iNaturalist observation dates against Suunto dive dates.
- **How It Works**: Filters out non-diving observations (e.g. terrestrial birds, shore fauna, or moths) for review.
- **Output**: [`dive-logs/unmatched_observations.json`](dive-logs/unmatched_observations.json)
- **Execution**:
  ```bash
  .venv/bin/python dive-logs/export_unmatched.py
  ```

---

## Requirements & Setup

A virtual environment with `requests` installed is required to run the API scripts:

```bash
cd /Users/astra/github/public/underwater-photography/iNaturalist
python3 -m venv .venv
.venv/bin/pip install requests
```
