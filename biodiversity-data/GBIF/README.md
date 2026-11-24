# GBIF

Notes, scripts and reports for exploring the [GBIF API](https://techdocs.gbif.org/en/openapi/) with my own wildlife records. This is the counterpart of [`../iNaturalist`](../iNaturalist).

**Links:**

- [my records on GBIF](https://www.gbif.org/occurrence/search?recordedBy=Andre+Astra) (occurrence search, `recordedBy=Andre Astra`)
- [iNaturalist dataset on GBIF](https://www.gbif.org/dataset/50c9509d-22c7-4a22-a47d-8c48425ef4a7)
- [underwater species](#underwater-species-search) (photos of marine species in an area you give; built by a script)

---

## What GBIF is

[GBIF](https://www.gbif.org) (Global Biodiversity Information Facility) is an open biodiversity data aggregator. Research-grade iNaturalist observations with an open licence are published to it automatically, in the dataset [iNaturalist Research-grade Observations](https://www.gbif.org/dataset/50c9509d-22c7-4a22-a47d-8c48425ef4a7). So GBIF is a second view of the same data as [`../iNaturalist`](../iNaturalist), with fewer records and different keys.

Example: iNaturalist observation [395263077](https://www.inaturalist.org/observations/395263077) is GBIF occurrence [6520575999](https://www.gbif.org/occurrence/6520575999). The iNaturalist API response lists it under `outlinks`.

For the endpoints, paging limits, example queries and how GBIF differs from iNaturalist, see the [API notes](scripts/README.md#api-notes). For linking my records to a person identifier, see [ORCID](../README.md#orcid).

---

## What is in this folder

| Folder | Contents |
|---|---|
| [`scripts/`](scripts) | Pipelines and report generators, the shared `config.py`, and the API notes. See [`scripts/README.md`](scripts/README.md). |
| [`reports/`](reports) | Generated reports, and one-off write-ups in [`reports/investigations/`](reports/investigations). See [`reports/README.md`](reports/README.md). |

Reports:

- [`gbif_summary.md`](reports/gbif_summary.md): what my records on GBIF look like.
- [`sync_status.md`](reports/sync_status.md): research-grade observations not on GBIF yet.
- [`underwater_ireland.md`](reports/underwater_ireland.md): the Irish underwater observations that are on GBIF.
- [`lough_hyne_species.md`](reports/lough_hyne_species.md): marine species anyone has recorded around Lough Hyne.
- [`cork_underwater.md`](reports/cork_underwater.md): marine species anyone has recorded in West Cork and its coastal waters.
- [`citations.md`](reports/citations.md): research that uses the dataset.

## Running

Run from this directory, using the virtualenv shared with [`../iNaturalist`](../iNaturalist). To create it, see [Shared setup](../README.md#shared-setup).

```bash
../.venv/bin/python scripts/run_all.py
```

This writes every report except [`cork_underwater.md`](reports/cork_underwater.md), which has its own script because its first run is slow: `../.venv/bin/python scripts/cork_underwater.py`.

---

## Underwater species search

[`scripts/underwater_url.py`](scripts/underwater_url.py) prints a gbif.org search URL for the underwater species recorded in an area you give it, as a WKT polygon (longitude first; draw one in the **Location** filter on gbif.org to get it):

```bash
../.venv/bin/python scripts/underwater_url.py --geometry "POLYGON((-9.18931 51.52073,-9.19342 51.51876,-9.18799 51.5156,-9.18062 51.518,-9.18139 51.51957,-9.18931 51.52073))"
```

The URL has the polygon, `occurrenceStatus=DETECTED`, `mediaType=StillImage` (a photo) and one `taxonKey` per species.

GBIF occurrences have no habitat field (`habitat=MARINE` is ignored by the occurrence search), so "underwater" comes from the species: the script lists the species with a photo in the area, keeps the ones a GBIF species profile marks as marine (the same check as [`cork_underwater.md`](reports/cork_underwater.md); birds and flowering plants are left out), and puts each one in the URL. Checking species rather than whole groups means snails, crabs, worms and wrasse are included and land species are not. The values are Catalogue of Life IDs (`DXNZ`), which gbif.org takes, not the numeric GBIF keys of the API.

Limits: only species that already have a photo in the area are in the URL, so run the script again to pick up new ones. A species with no exact Catalogue of Life match is left out, with a warning. A very large area gives a very long URL (about 20 characters per species). See [`underwater_url.py`](scripts/README.md#underwater_urlpy) for details.

---

## Downstream citations

Once records are on GBIF, research that uses them can be tracked. GBIF does this mainly per **dataset** and per **taxon**, so the figures cover all iNaturalist users. Papers can also cite a single occurrence by its GBIF key, but that is rare for iNaturalist records (they are usually used through bulk downloads or cited by their inaturalist.org URL). The `gbifOccurrenceKey` search filter fails on the API, so the report checks the key facet instead.

The *Citations* tab on the [dataset page](https://www.gbif.org/dataset/50c9509d-22c7-4a22-a47d-8c48425ef4a7) lists the linked papers. [`reports/citations.md`](reports/citations.md) summarises them and picks out the papers that mention species I recorded.

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

## Ideas to explore

- Species recorded in Ireland on GBIF that are missing from the iNaturalist life list, from sources other than iNaturalist (museums, surveys, Seasearch).
- A full species list for another dive-site area, using `geometry` or a bounding box (`decimalLatitude`, `decimalLongitude` ranges). [`lough_hyne_species.md`](reports/lough_hyne_species.md) does this for Lough Hyne with a `geometry` polygon, and adds filters for photos, marine species and duplicate records.
