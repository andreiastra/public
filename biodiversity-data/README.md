# Biodiversity data

Scripts, reports and notes for working with my wildlife records through public biodiversity APIs. The focus is underwater (marine) observations in **Ireland**.

| Folder | What it is |
|---|---|
| [`iNaturalist/`](iNaturalist) | Pipelines and generated reports built on the [iNaturalist API](https://api.inaturalist.org/v1/docs/) for user [`andreiastra`](https://www.inaturalist.org/people/andreiastra): dive-site ratings, rarity, life-list and gap-analysis reports. Start with [`iNaturalist/README.md`](iNaturalist/README.md). |
| [`GBIF/`](GBIF) | Notes and scripts for exploring the [GBIF API](https://techdocs.gbif.org/en/openapi/). GBIF holds the research-grade subset of the iNaturalist records, so it is a second view of the same data; [how the two differ](GBIF/README.md#how-gbif-differs-from-inaturalist). Start with [`GBIF/README.md`](GBIF/README.md). |

## Shared setup

Both folders use one virtual environment at `biodiversity-data/.venv` (git-ignored). Its dependencies are listed in [`requirements.txt`](requirements.txt).

```bash
cd /Users/astra/github/public/biodiversity-data
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Run each script from its own folder, using `../.venv/bin/python` (or `source ../.venv/bin/activate` for the session):

```bash
cd iNaturalist && ../.venv/bin/python scripts/run_all.py
cd GBIF && ../.venv/bin/python scripts/fetch_occurrences.py --country IE
```

The venv stores absolute paths. If you move this folder, delete `.venv` and create it again with the commands above.

## Conventions

- Reports under `iNaturalist/reports/` and `GBIF/reports/` are generated. Regenerate them rather than editing them by hand.
- Each folder has the same layout: `scripts/` for the generators and `reports/` for their output, each with its own README, and a `run_all.py` that regenerates everything with one download.
- Downloaded API data is cached in each folder's `scripts/.cache/`, which is git-ignored. These files are snapshots and go stale, so re-run the fetch script instead of reading an old copy.
