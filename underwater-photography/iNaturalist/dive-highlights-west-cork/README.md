# West Cork Dive Highlights

Generates the interactive, standalone HTML summary report showcasing top dive sites, species highlights, and standout underwater photography in West Cork from live iNaturalist data.

This file serves as the technical reference for the highlights generator. For project-wide workflows and action items, see the root [`../README.md`](../README.md).

---

## 1. Scripts & Output

### `generate_dive_highlights.py`
- **Purpose**: Generates [`dive-highlights-west-cork.html`](dive-highlights-west-cork.html) (also published on GitHub Pages).
- **How It Works**:
  - Fetches observation records and high-resolution photo URLs via the iNaturalist REST API.
  - Groups sightings into curated dive sites (excluding terrestrial and birding spots like Rosscarbery and Coolanagh).
  - Formats species cards, hero image banners, and standout sightings into a self-contained HTML page.
- **Output**: [`dive-highlights-west-cork.html`](dive-highlights-west-cork.html)
- **Execution**:
  ```bash
  .venv/bin/python dive-highlights-west-cork/generate_dive_highlights.py
  ```

---

## 2. Technical Documentation

For an in-depth breakdown of API fields, computed stats, and hardcoded config, see [`generate_dive_highlights_HOW_IT_WORKS.md`](generate_dive_highlights_HOW_IT_WORKS.md).
