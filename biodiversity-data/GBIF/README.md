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
- **No user id.** Records are matched by the text field `recordedBy` (`Andre Astra`), not by the iNaturalist login or ID.
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

## Scripts

Run from this directory, using the virtualenv shared with [`../iNaturalist`](../iNaturalist). To create it, see [Shared setup](../README.md#shared-setup).

```bash
../.venv/bin/python scripts/fetch_occurrences.py
../.venv/bin/python scripts/fetch_occurrences.py --country IE
```

| File | Purpose |
|---|---|
| [`scripts/config.py`](scripts/config.py) | Shared constants: API URLs, page size, `RECORDED_BY`, iNaturalist dataset key, country codes. |
| [`scripts/fetch_occurrences.py`](scripts/fetch_occurrences.py) | Downloads all my occurrences from the iNaturalist dataset to `scripts/.cache/occurrences.json` (a snapshot, regenerate rather than read). Optional `--country`. |

---

## Ideas to explore

- Compare the GBIF set against the iNaturalist set, to list research-grade observations that have not reached GBIF yet and to spot ones that never will (licence, location).
- Species recorded in Ireland on GBIF that are missing from the iNaturalist life list, from sources other than iNaturalist (museums, surveys, Seasearch).
- Download a full species list for a dive-site area with `geometry` or a bounding box (`decimalLatitude`, `decimalLongitude` ranges).
