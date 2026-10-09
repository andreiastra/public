# Underwater Photography & iNaturalist Integration

This repository contains tools, data pipelines, and reporting scripts for cataloging underwater photography, managing dive logs from the Suunto Eon Core dive computer, and linking records to [iNaturalist](https://www.inaturalist.org) observations.

---

## Profile & Links

- **iNaturalist Profile:** [andreiastra on iNaturalist](https://www.inaturalist.org/people/andreiastra)
- **West Cork Dive Highlights:** [dive-highlights-west-cork.html](https://andreiastra.github.io/public/underwater-photography/iNaturalist/dive-highlights-west-cork/dive-highlights-west-cork.html)
- **Dive Site Observations:** [Location_ratings.md](https://github.com/andreiastra/public/blob/main/underwater-photography/iNaturalist/scripts/OUTPUT/Location_ratings.md)
- **Species Classification & Organism Types:** [species_classification.md](https://github.com/andreiastra/public/blob/main/underwater-photography/iNaturalist/scripts/OUTPUT/species_classification.md)
- **Least Observed Wildflowers Tool:** [Wildflower Tracker (`andreiastra`)](https://elias.pschernig.com/wildflower/leastobserved.html?user=andreiastra&place=ireland)
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

- **[`scripts/`](scripts)** — API data pipelines and markdown report generators (see [`scripts/README.md`](scripts/README.md)).
- **[`dive-highlights-west-cork/`](dive-highlights-west-cork)** — Interactive HTML highlights showcase (see [`dive-highlights-west-cork/README.md`](dive-highlights-west-cork/README.md)).
- **[`dive-logs/`](dive-logs)** — Raw Suunto dive computer telemetry (`.fit` / `.gpx`) and chronological dive index. Used historically as date and location anchors to resolve place names for old observations (see [`dive-logs/README.md`](dive-logs/README.md)).
- **[`matching-dives-and-places/`](matching-dives-and-places)** — Historical scripts used to resolve place names for old iNaturalist observations by cross-referencing dive log dates against observation dates. No longer needed for new observations (see [`matching-dives-and-places/README.md`](matching-dives-and-places/README.md)).
- **[`Preferred_dive_site_names_ireland.txt`](Preferred_dive_site_names_ireland.txt)** & **[`Preferred_other_location_names.txt`](Preferred_other_location_names.txt)** — Canonical dive site and terrestrial location reference lists.
- **[`TODO.md`](TODO.md)** — Active task tracker, known data/generator issues, and backlog improvements.

---

> **Documentation Convention:** This root README is the single source of truth for high-level workflows and project setup. Subfolder documentation files serve as focused technical references for script parameters, schemas, and data structures. Active issues and backlog tasks are tracked in [`TODO.md`](TODO.md).

---

## Requirements & Setup

A shared virtual environment in the project root with `requests` installed is used by all Python scripts across `scripts/`, `dive-highlights-west-cork/`, and `matching-dives-and-places/`:

```bash
cd /Users/astra/github/public/underwater-photography/iNaturalist
python3 -m venv .venv
.venv/bin/pip install requests
```

Run any script directly without activating the venv:

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

## Recommended Workflows

### 1. 🔍 Review "Needs ID" Observations
To help observations reach **Research Grade** (which requires community consensus / 2+ agreeing identifications to be shared with scientific repositories like GBIF):
- **Live Identification Queue:** [Identify `andreiastra` observations needing ID](https://www.inaturalist.org/observations/identify?user_id=andreiastra&quality_grade=needs_id)
- **Live Needs-ID Map:** [Browse pending observations on the map](https://www.inaturalist.org/observations?user_id=andreiastra&quality_grade=needs_id&subview=map)

### 2. 📊 Monitor Site Coverage & Ratings
Instead of tracking static counts manually in markdown, regenerate the dynamic site reports from live iNaturalist data:
- Run `.venv/bin/python scripts/generate_location_ratings.py` to update [`scripts/OUTPUT/Location_ratings.md`](scripts/OUTPUT/Location_ratings.md) with current dive counts, observation totals, and species lists per site.
- Use the summary table in [`Location_ratings.md`](scripts/OUTPUT/Location_ratings.md) to identify under-explored dive sites.

### 3. 📋 Track Known Issues & Data Tasks
For active bug fixes, canonical site list pruning, and generator enhancements, see [`TODO.md`](TODO.md).
