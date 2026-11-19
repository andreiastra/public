# GBIF

Notes and scripts for exploring the [GBIF API](https://techdocs.gbif.org/en/openapi/) with my own records. This is the counterpart of [`../iNaturalist`](../iNaturalist).

[GBIF](https://www.gbif.org) (Global Biodiversity Information Facility) is an open biodiversity data aggregator. Research-grade iNaturalist observations with an open licence are published to it automatically, in the dataset [iNaturalist Research-grade Observations](https://www.gbif.org/dataset/50c9509d-22c7-4a22-a47d-8c48425ef4a7).

Example: iNaturalist observation [395263077](https://www.inaturalist.org/observations/395263077) is GBIF occurrence [6520575999](https://www.gbif.org/occurrence/6520575999). The iNaturalist API response lists it under `outlinks`.

---

## GBIF API

Base URL `https://api.gbif.org/v1`. Reads need no authentication.

| Endpoint | Purpose |
|---|---|
| `/occurrence/{key}` | One occurrence record |
| `/occurrence/search` | Search occurrences (taxon, country, date, dataset, coordinates, `recordedBy`, …) |
| `/occurrence/download/request` | Large asynchronous downloads (needs a GBIF account) |
| `/species/match?name=` | Match a name to the GBIF backbone taxonomy |
| `/species/{key}` | Taxon details |
| `/dataset/{key}` | Dataset metadata |

Search results return at most 300 records per page. Deep paging stops at an offset of about 100,000. Use `limit=0` for a count only, and `facet=<field>` for counts grouped by a field.

### How GBIF differs from iNaturalist

- **Research grade only.** Needs ID observations and observations without an open licence are absent, so GBIF counts are lower than the iNaturalist ones.
- **Lag.** GBIF re-reads iNaturalist periodically. Check `lastInterpreted` on a record to see when it last synced.
- **No user id.** Records are matched by the text field `recordedBy` (`Andre Astra`), not by the iNaturalist login or ID. Linking an [ORCID iD](#orcid) adds a real identifier once it is synced.
- **Own keys.** `taxonKey` and `speciesKey` come from the GBIF backbone and differ from iNaturalist taxon IDs. A record can carry the issue `TAXON_ID_NOT_FOUND` when the iNaturalist ID has no match; the name still resolves.
- **Rounded coordinates.** Expect the issue `COORDINATE_ROUNDED` (6 decimal places).
- **Obscured locations.** Threatened species are generalised, as on iNaturalist.

### Counts from the API (2026-11-19)

Research-grade records `recordedBy=Andre Astra`, dataset above:

| Country | Records |
|---|---|
| Ireland (IE) | 205 |
| Egypt (EG) | 90 |
| United Kingdom (GB) | 1 |
| Saudi Arabia (SA) | 1 |
| **Total** | **297** |

These are snapshot figures and go stale. Re-run the queries below for current ones.

---

## ORCID

[ORCID](https://orcid.org) gives a person a permanent identifier that stays the same if the name changes or is spelled differently. Mine is [0009-0008-8643-0031](https://orcid.org/0009-0008-8643-0031) (created 2026-11-19, email verified, name `Andrei Astrakharchik`).

**Why it matters here.** The records are matched by the name string `Andre Astra`, which differs from the ORCID name and could clash with another person of the same name. GBIF has a field for a proper identifier, `recordedByIDs`. iNaturalist fills it from the ORCID on the user's profile and also fills `identifiedByIDs` for identifications ([community explanation](https://forum.inaturalist.org/t/question-on-orcid-ids-and-exports-to-gbif/32061)).

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

**What it does not do.** The ORCID attributes records to me. It does not create paper citations: [`reports/citations.md`](reports/citations.md) still works per dataset and per taxon, and the ORCID is useful there only for finding papers by hand. The scripts still select records with `RECORDED_BY` in [`scripts/config.py`](scripts/config.py); switching to the ORCID is a possible change after the link has synced.

---

## Handy queries

```bash
B=https://api.gbif.org/v1

# One record
curl -s "$B/occurrence/6520575999"

# Count of my records, grouped by country
curl -s "$B/occurrence/search?recordedBy=Andre%20Astra&limit=0&facet=country"

# Same species recorded by anyone in Ireland
curl -s "$B/occurrence/search?scientificName=Tubulanus%20annulatus&country=IE&limit=20"

# Match a name to the backbone
curl -s "$B/species/match?name=Tubulanus%20annulatus"

# Verify the dataset key
curl -s "$B/dataset/50c9509d-22c7-4a22-a47d-8c48425ef4a7"
```

---

## Downstream citations

Once records are on GBIF, research that uses them can be tracked. GBIF does this mainly per **dataset** and per **taxon**, so the figures cover all iNaturalist users. Papers can also cite a single occurrence by its GBIF key, but that is rare for iNaturalist records (they are usually used through bulk downloads or cited by their inaturalist.org URL). The `gbifOccurrenceKey` search filter fails on the API, so the report checks the key facet instead. The *Citations* tab on the [dataset page](https://www.gbif.org/dataset/50c9509d-22c7-4a22-a47d-8c48425ef4a7) lists the linked papers, and [`reports/citations.md`](reports/citations.md) summarises them and picks out the papers that mention species I recorded.

```bash
B=https://api.gbif.org/v1
K=50c9509d-22c7-4a22-a47d-8c48425ef4a7

# Papers linked to the dataset (count only), then by year
curl -s "$B/literature/search?gbifDatasetKey=$K&limit=0"
curl -s "$B/literature/search?gbifDatasetKey=$K&limit=0&facet=year"

# Papers linked to the dataset that mention one species (GBIF taxon key)
curl -s "$B/literature/search?gbifDatasetKey=$K&gbifTaxonKey=2265793&limit=5"

# Downloads that used the dataset (count only)
curl -s "$B/occurrence/download/dataset/$K?limit=0"
```

---

## Directory Overview

- **[`scripts/`](scripts)** — API data pipelines and report generators (see [`scripts/README.md`](scripts/README.md)).
- **[`reports/`](reports)** — Generated markdown reports (see [`reports/README.md`](reports/README.md)): [`gbif_summary.md`](reports/gbif_summary.md), [`sync_status.md`](reports/sync_status.md), [`underwater_ireland.md`](reports/underwater_ireland.md) and [`citations.md`](reports/citations.md).

Run from this directory, using the virtualenv shared with [`../iNaturalist`](../iNaturalist). To create it, see [Shared setup](../README.md#shared-setup).

```bash
../.venv/bin/python scripts/run_all.py
```

---

## Ideas to explore

- Species recorded in Ireland on GBIF that are missing from the iNaturalist life list, from sources other than iNaturalist (museums, surveys, Seasearch).
- Download a full species list for a dive-site area with `geometry` or a bounding box (`decimalLatitude`, `decimalLongitude` ranges).
