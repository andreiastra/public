# Dive Logs

## 1. Overview

Directory: `/Users/astra/github/public/underwater-photography/iNaturalist/dive-logs`

This directory contains raw dive workout data exported from the Suunto Eon Core dive computer.

### Data Structure
- `workouts/`: Raw dive logs containing `.fit` (binary dive telemetry including depth profile, temperature, and duration) and `.gpx` (GPS metadata, entry timestamps, and dive site description/notes in `<desc>`) files.
- `user/`, `comments/`, `reactions/`, `videos/`: Export metadata and account assets from Suunto app.

---

## 2. Scripts & Generated Artifacts

### Scripts
- **[`generate_dives_table.py`](generate_dives_table.py)**: Scans all GPX files in `workouts/`, extracts date, timestamp, user description (`<desc>`), and filename, and outputs a complete markdown table.

### Generated Artifacts
- **[`dives_table.md`](dives_table.md)**: Full chronological index table of all recorded dives.

---

## 3. Matching & Correlation

Scripts that cross-reference these logs against iNaturalist observations and preferred location names live in [`../matching-dives-and-places/`](../matching-dives-and-places/).
