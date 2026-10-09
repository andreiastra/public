# Dive Logs

## 1. Overview

Directory: `/Users/astra/github/public/underwater-photography/iNaturalist/dive-logs`

This directory contains raw dive workout data exported from the Suunto Eon Core dive computer. This file serves as the technical reference for log formats and indexing scripts. For the project-wide overview, workflows, and pending action items / TODOs, see [`../README.md`](../README.md).

### Data Structure
- `workouts/`: Raw dive logs containing `.fit` (binary dive telemetry including depth profile, temperature, and duration) and `.gpx` (GPS metadata, entry timestamps, and dive site description/notes in `<desc>`) files.
- `user/`, `comments/`, `reactions/`, `videos/`: Export metadata and account assets from Suunto app.

---

## 2. Scripts & Generated Artifacts

### `generate_dives_table.py`
- **Purpose**: Parses all `.gpx` files in `dive-logs/workouts/` to build a chronological markdown table of all dive sessions.
- **Output**: [`dives_table.md`](dives_table.md)
- **Execution**:
  ```bash
  .venv/bin/python dive-logs/generate_dives_table.py
  ```

### Generated Artifact
- **[`dives_table.md`](dives_table.md)**: Complete chronological index table of all recorded dives.

---

## 3. Matching & Correlation

Scripts that cross-reference these logs against iNaturalist observations and preferred location names live in [`../matching-dives-and-places/`](../matching-dives-and-places/).

> **Historical use:** The dive logs were used as date and location anchors to resolve place names for old iNaturalist observations uploaded before consistent site naming was in place. That work is complete; these logs are not needed for processing new observations.
