# GloBI Outlink Candidates — andreiastra

**Investigation date:** 2026-11-26  
**iNaturalist user:** [andreiastra](https://www.inaturalist.org/people/andreiastra)  
**Filter URL (all-time):** https://www.inaturalist.org/observations?place_id=any&verifiable=any&user_id=10958443&outlink_source=GloBI

---

## Background

[GloBI (Global Biotic Interactions)](https://www.globalbioticinteractions.org/) is an open-access database that aggregates species interaction records (predation, pollination, parasitism, commensalism, mutualism, etc.). It harvests iNaturalist observations by scanning **Observation Field Values (OFVs)** that map to biological interaction terms.

### How an iNaturalist observation qualifies

Two criteria must both be met:

1. **A taxon-linked interaction OFV is present.**  
   GloBI reads fields where the *value* is a linked iNaturalist taxon (not free text), so it can extract a two-species pair. Reliable field names:
   - `Preying on` / `Eating`
   - `Associated organism` / `Host`
   - `Parasite of` / `Parasitized by`
   - `Visiting flower of` / `Pollinating`
   - `Epibionts / Epiphytes / Parasites`

   > ⚠️ Text-only fields like `Interactions: predation` are not sufficient alone — always pair with a taxon-linked field.

2. **Baseline data quality.**  
   - Verifiable (not casual/captive), valid date + location + media  
   - Open license (CC0, CC BY, or CC BY-NC — default for this account)  
   - Research Grade preferred for full GBIF/GloBI downstream ingestion

3. **Sync lag.**  
   GloBI runs periodic batch harvests from iNaturalist. After adding a valid OFV, the outlink badge typically appears within **days to a few weeks**.

---

## Current GloBI-cited observations (4)

| Photo | Species | Common name | Observed | Location | OFV |
|-------|---------|-------------|----------|----------|-----|
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/728954778/thumb.jpg)](https://www.inaturalist.org/observations/397443343) | *Marthasterias glacialis* | Spiny Starfish | 5 Sep 2026 | Sandmount Bay Beach, Co. Cork | Preying on → *Phallusia mammillata* |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/726468376/thumb.jpg)](https://www.inaturalist.org/observations/395263077) | *Tubulanus annulatus* | Football Jersey Worm | 4 Apr 2026 | Lough Hyne, Co. Cork | Preying on + Eating → *Sabella pavonina* |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/724746232/thumb.jpg)](https://www.inaturalist.org/observations/395271306) | *Tubulanus annulatus* | Football Jersey Worm | 14 Mar 2026 | Lough Hyne, Co. Cork | Preying on + Eating → *Sabella pavonina* |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/726513540/thumb.jpg)](https://www.inaturalist.org/observations/396175259) | *Marthasterias glacialis* | Spiny Starfish | 12 Jul 2025 | Aghabeg Pier, Co. Cork | Preying on → Brachyura |

---

## OFV added — awaiting GloBI sync (5)

These observations already have taxon-linked OFVs but have not yet appeared in GloBI (likely within the sync window).

| Photo | Species | OFV |
|-------|---------|-----|
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/766685566/thumb.jpg)](https://www.inaturalist.org/observations/416315379) | *Anemonia viridis* (Snakelocks Anemone) | Associated organism → Copepoda |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/766767998/thumb.jpg)](https://www.inaturalist.org/observations/416355705) | *Carcinus maenas* (European Green Crab) | Epibionts / Epiphytes / Parasites → *Spirobranchus* |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/737006875/thumb.jpg)](https://www.inaturalist.org/observations/401538064) | *Urocaridella antonbruunii* (Red Sea Cleaner Shrimp) | Associated organism + Host → *Gymnothorax javanicus* |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/737006875/thumb.jpg)](https://www.inaturalist.org/observations/417088244) | *Gymnothorax javanicus* (Giant Moray) | Associated organism → *Urocaridella antonbruunii* |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/724706714/thumb.jpg)](https://www.inaturalist.org/observations/395250582) | *Aplysia punctata* (Spotted Seahare) | Associated organism + Eating → *Desmarestia* |

---

## Priority candidates — OFV not yet added

Observations where a biotic interaction is visible or strongly implied in the photo. Check each observation and add the appropriate taxon-linked OFV if the interacting organism is identifiable.

### Ireland — marine (Lough Hyne, West Cork coast)

| Photo | Species | Common name | Observed | Suggested OFV |
|-------|---------|-------------|----------|---------------|
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/740558473/thumb.jpg)](https://www.inaturalist.org/observations/403325901) | *Thor amboinensis* | Squat Anemone Shrimp | 25 Sep 2026 | `Associated organism` / `Found on` → host anemone taxon (e.g. *Entacmaea quadricolor*) |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/724700275/thumb.jpg)](https://www.inaturalist.org/observations/395246903) | *Prostheceraeus vittatus* | Candy Stripe Flatworm | 18 Jul 2026 | `Eating` → tunicate/bryozoan taxon if visible |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/724704135/thumb.jpg)](https://www.inaturalist.org/observations/395249124) | *Aplysia punctata* | Spotted Seahare | 27 Jun 2026 | `Eating` → algae taxon if visible |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/724693602/thumb.jpg)](https://www.inaturalist.org/observations/395243552) | *Homarus gammarus* | European Lobster | 18 Jul 2026 | `Eating` / `Preying on` → prey if visible |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/728001576/thumb.jpg)](https://www.inaturalist.org/observations/396955919) | *Prostheceraeus vittatus* | Candy Stripe Flatworm | 27 Jun 2026 | `Eating` → tunicate/bryozoan taxon if visible |

### Red Sea — Sharm El Sheikh (Sep 2026)

| Photo | Species | Common name | Observed | Suggested OFV |
|-------|---------|-------------|----------|---------------|
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/740558473/thumb.jpg)](https://www.inaturalist.org/observations/403325901) | *Thor amboinensis* | Squat Anemone Shrimp | 25 Sep 2026 | `Found on` → anemone host taxon |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/739378207/thumb.jpg)](https://www.inaturalist.org/observations/402741993) | *Thor amboinensis* | Squat Anemone Shrimp | 23 Sep 2026 | `Found on` → anemone host taxon |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/742937659/thumb.jpg)](https://www.inaturalist.org/observations/404550216) | *Stenopus hispidus* | Banded Coral Shrimp | 29 Sep 2026 | `Cleaning` / `Associated organism` → fish taxon if present |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/735537983/thumb.jpg)](https://www.inaturalist.org/observations/400791237) | *Stenopus hispidus* | Banded Coral Shrimp | 16 Sep 2026 | `Cleaning` / `Associated organism` → fish taxon if present |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/740560159/thumb.jpg)](https://www.inaturalist.org/observations/403348936) | *Acanthaster benziei* | Red Sea Crown-of-thorns | 25 Sep 2026 | `Preying on` → coral taxon being eaten |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/734331816/thumb.jpg)](https://www.inaturalist.org/observations/400192874) | *Acanthaster benziei* | Red Sea Crown-of-thorns | 14 Sep 2026 | `Preying on` → coral taxon being eaten |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/737186678/thumb.jpg)](https://www.inaturalist.org/observations/401634005) | *Hexabranchus sanguineus* | Spanish Dancer | 19 Sep 2026 | `Eating` → sponge taxon if visible |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/735537149/thumb.jpg)](https://www.inaturalist.org/observations/400788359) | *Hexabranchus sanguineus* | Spanish Dancer | 16 Sep 2026 | `Eating` → sponge taxon if visible |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/741112339/thumb.jpg)](https://www.inaturalist.org/observations/403628743) | *Chromodoris quadricolor* | Pyjama Slug | 25 Sep 2026 | `Eating` → sponge taxon if visible |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/739377665/thumb.jpg)](https://www.inaturalist.org/observations/402741652) | *Chromodoris quadricolor* | Pyjama Slug | 23 Sep 2026 | `Eating` → sponge taxon if visible |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/738824921/thumb.jpg)](https://www.inaturalist.org/observations/402456682) | *Chromodoris quadricolor* | Pyjama Slug | 22 Sep 2026 | `Eating` → sponge taxon if visible |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/738269607/thumb.jpg)](https://www.inaturalist.org/observations/402175438) | *Chromodoris quadricolor* | Pyjama Slug | 21 Sep 2026 | `Eating` → sponge taxon if visible |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/740561878/thumb.jpg)](https://www.inaturalist.org/observations/403349976) | *Hypselodoris pulchella* | Beautiful Hypseldoris | 25 Sep 2026 | `Eating` → sponge taxon if visible |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/738824137/thumb.jpg)](https://www.inaturalist.org/observations/402456310) | *Hypselodoris pulchella* | Beautiful Hypseldoris | 22 Sep 2026 | `Eating` → sponge taxon if visible |

---

## Unusual OFVs found across all observations

A full audit of all 525 observations revealed the following non-standard or noteworthy fields.

### Needs action — non-standard interaction fields

| Photo | Species | Current OFV | Issue | Fix |
|-------|---------|-------------|-------|-----|
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/731361407/thumb.jpg)](https://www.inaturalist.org/observations/398670213) | *Pieris napi* (Green-veined White) | `Pollination interaction: Yes` | Free-text flag only, no linked taxon | Add `Visiting flower of` → plant taxon if identifiable in photo |
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/728084939/thumb.jpg)](https://www.inaturalist.org/observations/396998176) | *Bombus terrestris* (Buff-tailed Bumblebee) | `Pollen load?: yes` | Informal field, not harvested by GloBI | Add `Visiting flower of` → plant taxon if identifiable in photo |

> ✅ *Urocaridella antonbruunii* / *Gymnothorax javanicus* (obs [401538064](https://www.inaturalist.org/observations/401538064) & [417088244](https://www.inaturalist.org/observations/417088244)) — previously flagged here; now fixed with `Associated organism` + `Host` fields added. Moved to awaiting sync above.

### Interesting behavioural / ecological OFVs (no action needed)

| Photo | Species | OFV | Notes |
|-------|---------|-----|-------|
| [![](https://inaturalist-open-data.s3.amazonaws.com/photos/726544669/thumb.jpg)](https://www.inaturalist.org/observations/396190279) | *Scyliorhinus canicula* (Small-spotted Catshark) | `Behavior: mating: yes` + `Copulating: Yes` | Mating pair — well-documented behavioural record |
| — | *Aequorea vitrina* (3 obs) | `Planktonic: Yes` + `Plankton habitat: Marine plankton` | Correct ecological context for a hydromedusa |
| — | *Polybius* sp. | `Night Dive: yes` | Environmental/behavioural context |
| — | *Spilosoma lubricipeda* | `Insect life stage: larva` | Correct life stage tagging for a moth larva obs |
| — | Nudibranchia | `Substrate: Rock` + `Visibility (m): 4` | Environmental metadata |

### Standard dive metadata fields (routine, no action)

Applied consistently to recent dive sessions: `Depth (m)`, `Water temperature (C)`, `Underwater: Saltwater`.

---

## OFV workflow

To add an OFV on the iNaturalist web UI:

1. Open the observation page.
2. Scroll to **Observation Fields** → click **Add field**.
3. Search for the field name (e.g. `Preying on`).
4. In the value box, **search for the target taxon by name** — select the linked taxon result, not a free-text entry.
5. Save.

Repeat with `Eating` for the same target if the interaction is predation/herbivory (belt-and-braces for GloBI indexing, as both field names are harvested).

---

## Notes

- GloBI ingests iNaturalist via the [iNaturalist-to-GloBI pipeline](https://github.com/globalbioticinteractions/globalbioticinteractions/wiki/iNaturalist). The harvest uses the iNaturalist observation export, not the live API, so there is always a lag.
- Research Grade is not strictly required for GloBI indexing, but it ensures the observation also flows through GBIF, maximising reach.
- Both the source organism and the target taxon should be identified to at least genus level for GloBI to record a useful interaction pair.
- Total Research Grade observations as of investigation date: **372**
