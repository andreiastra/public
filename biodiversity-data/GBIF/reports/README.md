# Generated Reports

This directory contains generated Markdown reports produced by the scripts in [`../scripts/`](../scripts/README.md).

All reports are generated from live [GBIF](https://www.gbif.org) data for records recorded by `Andre Astra` in the [iNaturalist Research-grade Observations](https://www.gbif.org/dataset/50c9509d-22c7-4a22-a47d-8c48425ef4a7) dataset, and can be regenerated at any time. `sync_status.md` and `underwater_ireland.md` also read iNaturalist.

---

## Report Catalog

| Report | Description | Generator Script |
|---|---|---|
| **[`gbif_summary.md`](gbif_summary.md)** | What the records on GBIF look like: counts by country, organism group and year, the species total, and the issues GBIF raised. | [`gbif_summary.py`](../scripts/README.md#gbif_summarypy) |
| **[`sync_status.md`](sync_status.md)** | Research-grade iNaturalist observations that are not on GBIF yet, and records still on GBIF that are no longer research grade. | [`sync_status.py`](../scripts/README.md#sync_statuspy) |
| **[`underwater_ireland.md`](underwater_ireland.md)** | The underwater observations in Ireland (the iNaturalist report's data set) that are on GBIF, by organism group, site and year, and the research-grade ones still missing. | [`underwater_ireland.py`](../scripts/README.md#underwater_irelandpy) |

---

For script usage and parameters, see [`../scripts/README.md`](../scripts/README.md).
