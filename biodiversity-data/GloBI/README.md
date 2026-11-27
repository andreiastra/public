# GloBI

Notes, scripts and reports for exploring [GloBI (Global Biotic Interactions)](https://www.globalbioticinteractions.org/) with my own wildlife records. This is a companion to [`../iNaturalist`](../iNaturalist) and [`../GBIF`](../GBIF).

**Links:**

- [My GloBI-cited observations on iNaturalist](https://www.inaturalist.org/observations?place_id=any&verifiable=any&user_id=10958443&outlink_source=GloBI) (all-time, `outlink_source=GloBI`)
- [GloBI interaction explorer](https://www.globalbioticinteractions.org/browse/)
- [iNaturalist ↔ GloBI harvest review](https://depot.globalbioticinteractions.org/reviews/globalbioticinteractions/inaturalist/)
- [GloBI API](https://api.globalbioticinteractions.org/)

---

## What GloBI is

[GloBI](https://www.globalbioticinteractions.org) (Global Biotic Interactions) is an open-access database that aggregates species interaction records — predation, pollination, parasitism, commensalism, mutualism, and more. It harvests from published literature, natural history collections, and citizen science platforms including iNaturalist.

GloBI indexes iNaturalist observations by scanning **Observation Field Values (OFVs)** where the value is a linked taxon (not free text), extracting a two-species interaction pair. An observation must have a taxon-linked OFV using a recognised field name (`Preying on`, `Eating`, `Associated organism`, `Host`, `Parasite of`, `Visiting flower of`, etc.) to be cited.

Example: iNaturalist observation [395263077](https://www.inaturalist.org/observations/395263077) (*Tubulanus annulatus* preying on *Sabella pavonina*) is indexed by GloBI as a predation record. The GloBI outlink badge appears on the observation after the next harvest cycle (days to weeks).

For how to qualify observations and which OFV fields GloBI reliably parses, see [`reports/investigations/globi-outlink-candidates.md`](reports/investigations/globi-outlink-candidates.md).

---

## What is in this folder

| Folder | Contents |
|--------|----------|
| [`reports/investigations/`](reports/investigations) | One-off write-ups and audit reports. |

Reports:

- [`reports/investigations/globi-outlink-candidates.md`](reports/investigations/globi-outlink-candidates.md): full audit of observations currently cited by GloBI, those awaiting sync, and priority candidates for adding interaction OFVs.

---

## Querying my records via the GloBI API

```bash
# All interactions for a specific iNaturalist observation
curl "https://api.globalbioticinteractions.org/interaction.csv?sourceOccurrenceId=https://www.inaturalist.org/observations/395271306"

# All interactions for a taxon, sourced from iNaturalist
curl "https://api.globalbioticinteractions.org/interaction?sourceTaxon=Tubulanus+annulatus&accordingTo=iNaturalist&type=json"

# Interaction explorer URL for a taxon
# https://www.globalbioticinteractions.org/?sourceTaxon=Marthasterias+glacialis
```

GloBI harvests iNaturalist via a periodic batch export — not the live API — so there is always a lag between adding an OFV and the outlink appearing.

---

## Relationship to iNaturalist and GBIF

```
iNaturalist observation (Research Grade, open licence)
    │
    ├─► GBIF occurrence (automatic, ~weekly sync)
    │
    └─► GloBI interaction record (requires taxon-linked OFV, periodic harvest)
```

All three views derive from the same iNaturalist observation. GBIF indexing is automatic for Research Grade records; GloBI indexing requires deliberate OFV tagging.
