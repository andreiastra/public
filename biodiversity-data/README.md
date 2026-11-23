# Biodiversity data

Scripts, reports and notes for working with my wildlife records through public biodiversity APIs. The focus is underwater (marine) observations in **Ireland**.

| Folder | What it is |
|---|---|
| [`iNaturalist/`](iNaturalist) | Pipelines and generated reports built on the [iNaturalist API](https://api.inaturalist.org/v1/docs/) for user [`andreiastra`](https://www.inaturalist.org/people/andreiastra): dive-site ratings, rarity, life-list and gap-analysis reports. Start with [`iNaturalist/README.md`](iNaturalist/README.md). |
| [`GBIF/`](GBIF) | Notes and scripts for exploring the [GBIF API](https://techdocs.gbif.org/en/openapi/). GBIF holds the research-grade subset of the iNaturalist records, so it is a second view of the same data; [how the two differ](GBIF/scripts/README.md#how-gbif-differs-from-inaturalist). Start with [`GBIF/README.md`](GBIF/README.md). |

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

## ORCID

[ORCID](https://orcid.org) gives a person a permanent identifier that stays the same if the name changes or is spelled differently. Mine is [0009-0008-8643-0031](https://orcid.org/0009-0008-8643-0031) (created 2026-11-19, email verified, name `Andrei Astrakharchik`).

**Why it matters here.** The GBIF records are matched by the name string `Andre Astra`, which differs from the ORCID name and could clash with another person of the same name. GBIF has a field for a proper identifier, `recordedByIDs`. iNaturalist fills it from the ORCID on the user's profile and also fills `identifiedByIDs` for identifications ([community explanation](https://forum.inaturalist.org/t/question-on-orcid-ids-and-exports-to-gbif/32061)).

**Status on 2026-11-19: connected on iNaturalist, not on GBIF yet.**

| Check | Result |
|---|---|
| ORCID record exists | Yes, `pub.orcid.org` returns 200 |
| ORCID connected on iNaturalist | Yes, listed under Connected Accounts in Settings, Applications (authorized 2026-11-19) |
| ORCID in the iNaturalist API | Not yet (`orcid` is `null` for `andreiastra`; this may lag the settings page) |
| `recordedByIDs` on my GBIF records | Empty on all 297 (latest `lastInterpreted` is 2026-11-12, before the link) |
| `occurrence/search?recordedByID=` with my iD | 0 records |

**To link it.**

1. Connect ORCID on iNaturalist: Settings, Applications, Connected Accounts, ORCID, Connect. It signs in through orcid.org, so no iD is typed in. Done on 2026-11-19.
2. Wait for GBIF to re-read iNaturalist. A developer reply says this takes about a week or more. Records already on GBIF are expected to be updated too.
3. Re-run the checks below. Once `recordedByID` returns records, it is a better key than `recordedBy`.

```bash
B=https://api.gbif.org/v1

# Records GBIF attributes to my ORCID (0 until the link has synced)
curl -s "$B/occurrence/search?recordedByID=https://orcid.org/0009-0008-8643-0031&limit=0"

# ORCID shown on my iNaturalist profile (null until linked)
curl -s "https://api.inaturalist.org/v1/users/andreiastra" | python3 -c "import sys,json; print(json.load(sys.stdin)['results'][0].get('orcid'))"
```

**What it does not do.** The ORCID attributes records to me. It does not create paper citations: [`GBIF/reports/citations.md`](GBIF/reports/citations.md) still works per dataset and per taxon, and the ORCID is useful there only for finding papers by hand. The GBIF scripts still select records with `RECORDED_BY` in [`GBIF/scripts/config.py`](GBIF/scripts/config.py); switching to the ORCID is a possible change after the link has synced.
