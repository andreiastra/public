# Generated Reports

This directory contains generated Markdown reports produced by the scripts in [`../scripts/`](../scripts/README.md).

All reports are generated from live [GBIF](https://www.gbif.org) data for records recorded by `Andre Astra` in the [iNaturalist Research-grade Observations](https://www.gbif.org/dataset/50c9509d-22c7-4a22-a47d-8c48425ef4a7) dataset, and can be regenerated at any time. `sync_status.md` and `underwater_ireland.md` also read iNaturalist. The exception is `lough_hyne_species.md`, which covers every recorder and dataset on GBIF.

---

## Report Catalog

| Report | Description | Generator Script |
|---|---|---|
| **[`gbif_summary.md`](gbif_summary.md)** | What the records on GBIF look like: counts by country, organism group and year, the species total, the underwater records and species, and the issues GBIF raised. | [`gbif_summary.py`](../scripts/README.md#gbif_summarypy) |
| **[`sync_status.md`](sync_status.md)** | Research-grade iNaturalist observations that are not on GBIF yet, and records still on GBIF that are no longer research grade. | [`sync_status.py`](../scripts/README.md#sync_statuspy) |
| **[`underwater_ireland.md`](underwater_ireland.md)** | The underwater observations in Ireland (the iNaturalist report's data set) that are on GBIF, by organism group, site and year, and the research-grade ones still missing. | [`underwater_ireland.py`](../scripts/README.md#underwater_irelandpy) |
| **[`lough_hyne_species.md`](lough_hyne_species.md)** | The marine species anyone has recorded inside a polygon around Lough Hyne on GBIF (all datasets, not only mine), only occurrences with a photo, identified to species, with copies of iNaturalist records in other datasets left out. It has the filters applied, a count of species per group (each group name links to its rows) and one row per species, grouped (fish, nudibranchs, crustaceans and so on): its common name and a clickable thumbnail for each record. Your records are outlined in blue, and the name of a species you recorded is blue too. | [`lough_hyne_species.py`](../scripts/README.md#lough_hyne_speciespy) |
| **[`cork_underwater.md`](cork_underwater.md)** | The marine species anyone has recorded in a polygon around West Cork and its coastal waters on GBIF (all datasets, not only mine), only occurrences with a photo, identified to species. It has the filters applied, a table of species per group, the 25 most photographed species and one table per group. Each row shows how many of the photos are mine, and each scientific name links to the same search on gbif.org. It is built from GBIF counts, so it has no thumbnails and no copy removal. | [`cork_underwater.py`](../scripts/README.md#cork_underwaterpy) |
| **[`citations.md`](citations.md)** | Research GBIF links to the iNaturalist dataset (papers, downloads, by year and topic), and the papers that mention species you recorded. | [`citations.py`](../scripts/README.md#citationspy) |
| **[`investigations/<date>-<topic>.md`](investigations/2026-11-23-west-cork-polygon-counts.md)** | One-off write-ups of a question answered from live data, with the method and caveats. Written by hand, not regenerated. | None |

---

For script usage and parameters, see [`../scripts/README.md`](../scripts/README.md).
