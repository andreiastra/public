# Underwater Photography & iNaturalist Integration

This repository contains tools, data pipelines, and reporting scripts for cataloging underwater photography, managing dive logs from the Suunto Eon Core dive computer, and linking records to [iNaturalist](https://www.inaturalist.org) observations.

---

## Profile & Links

- **iNaturalist Profile:** [andreiastra on iNaturalist](https://www.inaturalist.org/people/andreiastra)
- **West Cork Dive Highlights:** [dive-highlights-west-cork.html](https://andreiastra.github.io/public/underwater-photography/iNaturalist/dive-highlights-west-cork/dive-highlights-west-cork.html)
- **Dive Site Observations:** [Location_ratings.md](https://andreiastra.github.io/public/underwater-photography/iNaturalist/Location_ratings.md)
- **Least Observed Wildflowers Tool:** [Wildflower Tracker (`andreiastra`)](https://elias.pschernig.com/wildflower/leastobserved.html?user=andreiastra)
- **Google Colab Notebook:** [iNaturalist Data & Analysis Notebook](https://colab.research.google.com/drive/1kVHbCJRIewDRhXd8-t0d67D-vpwy7aPl#scrollTo=flI4KNDDsCv_)

---

## What is iNaturalist?

**iNaturalist** is a leading global citizen science platform and biodiversity network. It enables naturalists, researchers, and nature enthusiasts to record, map, and share observations of living organisms worldwide.

- **Community Identification:** When community consensus is reached an observation achieves **Research Grade** status and is shared with scientific repositories like **GBIF**.
- **Automated Computer Vision:** Integrated AI suggestions assist in identifying species from uploaded photographs.
- **Conservation & Research:** Serves as a vital open-access ecological dataset used by researchers and conservationists to track species distribution, migration patterns, and phenology.

---

## iNaturalist API

The iNaturalist API provides programmatic access to the platform's biodiversity database.

- **`/v1/observations`** — search, filter, and fetch geo-located observation records
- **`/v1/taxa`** — taxonomic hierarchies, scientific and common names, conservation status
- **`/v1/identifications` & `/v1/users`** — community contributions and user activity
- **`/v1/places`** — geographic boundaries and location-based species lists

Supports filtering by `user_id`, `taxon_id`, `place_id`, bounding boxes, date ranges, quality grade (`research`, `needs_id`), and media presence. Returns JSON with page-based or `id_above` pagination. Public read access requires no authentication; write actions use OAuth2. Recommended throttle: **~1 request/second**.

---

## Directory Overview

```text
iNaturalist/
├── Preferred_dive_site_names.txt      # Canonical preferred names for West Cork dive sites
├── Preferred_other_location_names.txt # Canonical preferred names for non-dive observation locations
├── Location_ratings.md                # Generated dive site index with observations and photo links
│
├── scripts/                           # Standalone helper scripts
│   ├── site_names.py                  # Shared keyword → canonical site name mapping (refresh before use)
│   ├── generate_location_ratings.py   # Generates Location_ratings.md from live iNaturalist data
│   ├── my_locations.py                # Clusters observations into dive sites; use to verify site_names.py
│   ├── my_places.py                   # Lists all distinct places from user observations
│   ├── my_projects.py                 # Lists joined iNaturalist projects
│   └── Locations.sh                   # Captured sample output from my_locations.py
│
├── dive-highlights-west-cork/         # Report generator, documentation, and output
│   ├── generate_dive_highlights.py    # Generates the standalone HTML report
│   ├── generate_dive_highlights_HOW_IT_WORKS.md # Technical documentation
│   └── dive-highlights-west-cork.html # Generated HTML report
│
├── dive-logs/                         # Raw Suunto dive computer export
│   ├── README.md                      # Dive logs documentation
│   ├── workouts/                      # Raw .gpx and .fit files exported from Suunto Eon Core
│   ├── generate_dives_table.py        # Generates dives_table.md index from workouts
│   └── dives_table.md                 # Complete chronological index of recorded dives
│
└── matching-dives-and-places/         # Cross-references dive logs with iNaturalist observations
    ├── export_unmatched_dives.py      # Identifies dive workouts with unmapped locations
    ├── export_unmatched.py            # Identifies observations recorded on non-diving days
    ├── unmatched_dives.json           # Review dataset of unmapped dive sites
    └── unmatched_observations.json    # Review dataset of non-dive observations
```

---

## Core Scripts Documentation

### 1. `scripts/generate_location_ratings.py`
- **Purpose**: Generates [`Location_ratings.md`](Location_ratings.md) — a per-site index of dive sessions and iNaturalist observations with clickable photo thumbnails.
- **How It Works**:
  - Fetches all observations from the iNaturalist API and clusters them geospatially (500 m radius).
  - Resolves each cluster to a canonical site name via [`scripts/site_names.py`](scripts/site_names.py).
  - Counts distinct observation dates per site as a proxy for dive sessions.
  - Renders each observation as a linked thumbnail (`/small.jpg`) pointing to the iNaturalist observation page.
- **Prerequisite**: Verify [`scripts/site_names.py`](scripts/site_names.py) is current before running (see that file for the refresh procedure).
- **Execution**:
  ```bash
  .venv/bin/python scripts/generate_location_ratings.py
  ```

### 2. `scripts/my_locations.py`
- **Purpose**: Fetches all observations for the user (`andreiastra`) from iNaturalist and groups them into geospatial clusters. **Also used to verify [`scripts/site_names.py`](scripts/site_names.py)** — run this and check that every cluster resolves to a canonical name.
- **How It Works**:
  - Uses a greedy clustering algorithm with a 500-metre radius (calculated via the Haversine great-circle formula).
  - Assigns canonical site names by matching `place_guess` fragments against the keyword mapping in [`scripts/site_names.py`](scripts/site_names.py).
- **Execution**:
  ```bash
  .venv/bin/python scripts/my_locations.py
  ```

### 3. `dive-highlights-west-cork/generate_dive_highlights.py`
- **Purpose**: Generates the standalone, interactive [`dive-highlights-west-cork/dive-highlights-west-cork.html`](dive-highlights-west-cork/dive-highlights-west-cork.html) summary report — also published at the GitHub Pages URL above.
- **How It Works**:
  - Fetches observation records and high-resolution photo URLs via the iNaturalist REST API.
  - Groups sightings into curated dive sites (excluding terrestrial and birding spots like Rosscarbery and Coolanagh).
  - Formats species cards, hero image banners, and standout sightings into a self-contained HTML page.
- **Execution**:
  ```bash
  .venv/bin/python dive-highlights-west-cork/generate_dive_highlights.py
  ```

### 4. `scripts/my_places.py`
- **Purpose**: Fetches and aggregates all distinct `place_guess` strings associated with observations.
- **How It Works**: Paginates through all user observations and outputs place counts with links to individual observations.
- **Execution**:
  ```bash
  .venv/bin/python scripts/my_places.py
  ```

### 5. `scripts/my_projects.py`
- **Purpose**: Retrieves all iNaturalist collection and umbrella projects joined by the user.
- **Execution**:
  ```bash
  .venv/bin/python scripts/my_projects.py
  ```

---

## Dive Logs (`dive-logs/`)

The [`dive-logs/`](dive-logs) subfolder holds the raw Suunto Eon Core telemetry export and a table generator.

### 1. `dive-logs/generate_dives_table.py`
- **Purpose**: Parses all `.gpx` files in `dive-logs/workouts/` to build a chronological markdown table of all dive sessions.
- **Output**: [`dive-logs/dives_table.md`](dive-logs/dives_table.md)
- **Execution**:
  ```bash
  .venv/bin/python dive-logs/generate_dives_table.py
  ```

---

## Matching Dives & Places (`matching-dives-and-places/`)

The [`matching-dives-and-places/`](matching-dives-and-places) subfolder contains scripts that cross-reference dive logs against iNaturalist observations and the canonical preferred locations list.

### 1. `matching-dives-and-places/export_unmatched_dives.py`
- **Purpose**: Normalizes dive `<desc>` tags and maps them against canonical site names in `Preferred_dive_site_names.txt`.
- **How It Works**: Handles character normalization (smart quotes, apostrophes), case-insensitivity, and aliases (`7 Heads` $\rightarrow$ `Seven Heads Pier`, `Barloque` $\rightarrow$ `Barloge Pier`).
- **Output**: [`matching-dives-and-places/unmatched_dives.json`](matching-dives-and-places/unmatched_dives.json)
- **Execution**:
  ```bash
  .venv/bin/python matching-dives-and-places/export_unmatched_dives.py
  ```

### 2. `matching-dives-and-places/export_unmatched.py`
- **Purpose**: Cross-references iNaturalist observation dates against Suunto dive dates.
- **How It Works**: Fetches all observations live from the iNaturalist API, then filters out non-diving observations (e.g. terrestrial birds, shore fauna, or moths) for review.
- **Output**: [`matching-dives-and-places/unmatched_observations.json`](matching-dives-and-places/unmatched_observations.json)
- **Execution**:
  ```bash
  .venv/bin/python matching-dives-and-places/export_unmatched.py
  ```

---

## Requirements & Setup

A virtual environment with `requests` installed is required to run the API scripts:

```bash
cd /Users/astra/github/public/underwater-photography/iNaturalist
python3 -m venv .venv
.venv/bin/pip install requests
```

Run a script directly without activating the venv:

```bash
.venv/bin/python scripts/my_projects.py
```

Or activate for the session:

```bash
source .venv/bin/activate
python scripts/my_projects.py
deactivate
```

---

## Recommended Actions

*Last reviewed against live API data — 93 observations across 14 sites.*

### 🟡 High value: Resolve 54 Needs ID observations (58%)

Only 39 of 93 observations (42%) have reached Research Grade. Adding a second ID agreement pushes an observation to Research Grade and contributes to GBIF.

**Quick link:** [View all Needs ID observations for andreiastra](https://www.inaturalist.org/observations/identify?user_id=andreiastra&quality_grade=needs_id)

Highest-priority clusters:

| Site | Needs ID | Notable species awaiting confirmation |
|------|----------|---------------------------------------|
| Lough Hyne | 17 | Cylinder Anemone, Gem Anemone, 6× spider crabs, Aeolidiella alderi/glauca, Thin Bubble-Shell ×2 |
| Gortdubh Pier | 8 | Portuguese Blenny, Tompot Blenny, Sandalled Anemone, Blue-rayed Limpet, Dead Man's Fingers |
| Zetland Pier | 5 | Sea Potato, Toothed Crab, Sea Vase, Connemarra Clingfish, Halichondria bowerbanki |
| Canty's Cove | 5 | Sea Lemon, Pink Coryphella, Aeolid Nudibranch, Atlantic Black Sea Cucumber |
| Seven Heads | 3 | Polycera faeroensis, Blood Stars, Topknot |

The second Football Jersey Worm observation ([395263077](https://www.inaturalist.org/observations/395263077)) is still Needs ID despite the species being Research Grade elsewhere — worth tagging for community attention.

### 🟡 High value: Revisit under-explored sites

| Site | Only find so far | Why go back |
|------|-----------------|-------------|
| Simon's Cove | Strawberry Anemone | 1 dive only — rocky crevices likely hold nudibranchs |
| Barloge Pier | Spiny Squat Lobster | Remote, barely explored — high potential |
| Blind Strand Pier | Tompot Blenny | Pier structure likely holds more fish |
| Trafrask Pier | Seabass + Pouting | 2 obs — fish activity suggests a productive site |
