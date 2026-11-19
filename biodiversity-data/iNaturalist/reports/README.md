# Generated Reports

This directory contains generated Markdown reports, species lists, site breakdowns, and rarity analyses produced by the data pipeline scripts in [`../scripts/`](../scripts/README.md).

All reports are generated from live [iNaturalist](https://www.inaturalist.org) data for user [`andreiastra`](https://www.inaturalist.org/people/andreiastra) and can be regenerated at any time.

---

## Report Catalog

| Report | Description | Generator Script |
|---|---|---|
| **[`Location_ratings.md`](Location_ratings.md)** | Master dive site index ranking all Irish dive sites by dive session counts, observation totals, and species sightings with photo thumbnails. | [`generate_location_ratings.py`](../scripts/README.md#generate_location_ratingspy) |
| **[`species_classification.md`](species_classification.md)** | Comprehensive classification of all Irish observations categorized into clean organism types (Fish, Nudibranch, Crab, Anemone, Sponge, Bird, etc.). | [`species_classification.py`](../scripts/README.md#species_classificationpy) |
| **[`underwater_ireland.md`](underwater_ireland.md)** | All underwater observations in Ireland grouped by dive site (most observations first), with a separate section for threatened species with obscured coordinates. | [`underwater_ireland.py`](../scripts/README.md#underwater_irelandpy) |
| **[`rarity_underwater_ireland.md`](rarity_underwater_ireland.md)** | Ranks Research Grade underwater species by Irish rarity (fewest distinct observers across Ireland, rarest first) with rarity tiers and IUCN status. | [`rarity_underwater_ireland.py`](../scripts/README.md#rarity_underwater_irelandpy) |
| **[`rarity_underwater_worldwide.md`](rarity_underwater_worldwide.md)** | Ranks the same Irish underwater species by worldwide observation frequency on a logarithmic scale. | [`rarity_underwater_worldwide.py`](../scripts/README.md#rarity_underwater_worldwidepy) |
| **[`rare_birds_ireland.md`](rare_birds_ireland.md)** | Ranks the bird species observed in Ireland by Irish rarity (fewest distinct observers across Ireland, rarest first) with rarity tiers. | [`rare_birds_ireland.py`](../scripts/README.md#rare_birds_irelandpy) |
| **[`nudibranch_ireland.md`](nudibranch_ireland.md)** | Dedicated showcase of all Irish sea slug & nudibranch observations (order *Nudibranchia*) grouped by dive site. | [`nudibranch_ireland.py`](../scripts/README.md#nudibranch_irelandpy) |
| **[`one_and_done_ireland.md`](one_and_done_ireland.md)** | Underwater species in Ireland recorded in only one observation, by site and organism type. The species to look for again. | [`one_and_done_ireland.py`](../scripts/README.md#one_and_done_irelandpy) |
| **[`rarity_by_site_ireland.md`](rarity_by_site_ireland.md)** | Dive sites ranked by how many Rare, Very rare and Unique species you found there, plus the rarest finds. | [`rarity_by_site_ireland.py`](../scripts/README.md#rarity_by_site_irelandpy) |
| **[`gap_analysis_ireland.md`](gap_analysis_ireland.md)** | Per dive site, the species other observers have recorded within 1 km that are new for you (not on your Irish underwater list at any site). | [`gap_analysis_ireland.py`](../scripts/README.md#gap_analysis_irelandpy) |
| **[`year_in_review.html`](year_in_review.html)** | One-page HTML summary of the underwater life list: totals, best dive, rarest find, top site, when you dive, growth, identifiers. Open in a browser. | [`year_in_review.py`](../scripts/README.md#year_in_reviewpy) |
| **[`sites/<site_name>.md`](sites/bank_pier.md)** | Individual dive site reports detailing site species lists and observation galleries (e.g., [`sites/bank_pier.md`](sites/bank_pier.md), [`sites/canty_s_cove.md`](sites/canty_s_cove.md), [`sites/gortdubh_pier.md`](sites/gortdubh_pier.md), [`sites/kilcrohane_pier.md`](sites/kilcrohane_pier.md)). | [`site_observations.py`](../scripts/README.md#site_observationspy) |
| **[`runs/<date>.md`](runs/2026-11-13.md)** | One dated write-up per full run: how it went and what changed in the reports. Written by hand, not regenerated. | [`run_all.py`](../scripts/README.md#run_allpy) |

---

For script usage, generator parameters, and execution instructions, see [`../scripts/README.md`](../scripts/README.md).
