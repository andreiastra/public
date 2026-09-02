# Dive Logs & iNaturalist Integration

## 1. Overview

Directory: `/Users/astra/github/public/underwater-photography/iNaturalist/dive-logs`

This directory contains dive workouts exported from the Suunto Eon Core dive computer along with tooling to process, normalize, and match dive logs against iNaturalist observations.

### Data Structure
- `workouts/`: Raw dive logs containing `.fit` (binary dive telemetry including depth profile, temperature, and duration) and `.gpx` (GPS metadata, entry timestamps, and dive site description/notes in `<desc>`) files.
- `user/`, `comments/`, `reactions/`, `videos/`: Export metadata and account assets from Suunto app.

---

## 2. Location Normalization & Preferred Locations

Dive logs frequently record location descriptions in the GPX `<desc>` tag. Location names are normalized and mapped against the canonical list defined in [`Preferred_location_names.txt`](../Preferred_location_names.txt).

The matching logic accommodates:
- Stripping or appending common suffixes (e.g. `Pier`).
- Normalization of typographic quotes and apostrophes.
- Common aliases and local shorthand (e.g. `7 Heads` $\rightarrow$ `Seven Heads Pier`, `Barloque` $\rightarrow$ `Barloge Pier`, `Cantys Cove` $\rightarrow$ `Canty's Cove`).

---

## 3. Scripts & Generated Artifacts

### Scripts
- **[`generate_dives_table.py`](generate_dives_table.py)**: Scans all GPX files in `workouts/`, extracts date, timestamp, user description (`<desc>`), and filename, and outputs a complete markdown table.
- **[`export_unmatched_dives.py`](export_unmatched_dives.py)**: Evaluates all dive descriptions against `Preferred_location_names.txt` using normalization rules and exports matched/unmatched dive summaries.
- **[`export_unmatched.py`](export_unmatched.py)**: Cross-references iNaturalist observations against dive workout dates to identify observations recorded on non-diving days.

### Generated Artifacts
- **[`dives_table.md`](dives_table.md)**: Full chronological index table of all recorded dives.
- **[`unmatched_dives.json`](unmatched_dives.json)**: JSON dataset containing counts and lists of dives whose descriptions do not match the current preferred locations list.
- **[`unmatched_observations.json`](unmatched_observations.json)**: JSON dataset of iNaturalist observations that occurred on dates without a corresponding dive log (e.g. terrestrial birds, shore fauna, or insect sightings).

---

## 4. iNaturalist Matching Workflow

1. **Date-Based Correlation**: Match observation `observed_on` date (`YYYY-MM-DD`) directly with dive workout dates.
2. **Multi-Dive Disambiguation**: For dates containing multiple dive workouts, use observation timestamps and location proximity to associate records with the correct dive session.
3. **Taxa Association**: For each matched dive, link the observed taxa, photo assets, and observation IDs to the verified location name.
4. **Highlights & Reporting**: Feed the enriched dive data into reporting tools (such as `generate_dive_highlights.py`).
