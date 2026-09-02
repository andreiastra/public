# iNaturalist Overview & Resources

## Personal Profile & Project Links

* **iNaturalist Profile:** [andreiastra on iNaturalist](https://www.inaturalist.org/people/andreiastra)
* **Least Observed Wildflowers Tool:** [Wildflower Tracker (`andreiastra`)](https://elias.pschernig.com/wildflower/leastobserved.html?user=andreiastra)
* **Google Colab Notebook:** [iNaturalist Data & Analysis Notebook](https://colab.research.google.com/drive/1kVHbCJRIewDRhXd8-t0d67D-vpwy7aPl#scrollTo=flI4KNDDsCv_)
* West Cork Dive Highlights https://andreiastra.github.io/public/underwater-photography/iNaturalist/dive-highlights-west-cork.html
---

## What is iNaturalist?

**iNaturalist** is a leading global citizen science platform and biodiversity network. It enables naturalists, researchers, and nature enthusiasts to record, map, and share observations of living organisms worldwide.

### Key Highlights:
* **Community Identification:** Observations can be crowdsourced and verified by the community. When a community consensus is reached, an observation achieves **Research Grade** status and is shared with scientific repositories like the Global Biodiversity Information Facility (**GBIF**).
* **Automated Computer Vision:** Integrated AI suggestions assist in identifying plant, animal, and fungi species from uploaded photographs.
* **Conservation & Research:** Serves as a vital open-access ecological dataset used by researchers, conservationists, and wildlife managers to track species distribution, migration patterns, and phenology.

---

## iNaturalist API Summary

The **iNaturalist API** provides programmatic access to the platform's rich biodiversity database, enabling custom querying, data analysis, and application development.

### Core Capabilities:
* **Endpoints & Resources:**
  * `/v1/observations`: Search, filter, and fetch geo-located observation records.
  * `/v1/taxa`: Access taxonomic hierarchies, scientific and common names, and conservation status.
  * `/v1/identifications` & `/v1/users`: Track community contributions, user activity, and identification records.
  * `/v1/places`: Query geographic boundaries and location-based species lists.
* **Advanced Querying & Filtering:** Supports filtering by `user_id`, `taxon_id`, `place_id`, bounding boxes/polygons, date ranges, quality grade (`research`, `needs_id`), and media presence (photos/audio).
* **Formats & Pagination:** Returns data in standard JSON format with page-based or `id_above` pagination.
* **Usage & Rate Limits:** 
  * Public read access does not require authentication for basic endpoints.
  * Write actions (creating observations/comments) use OAuth2 authentication.
  * Recommended polite request throttling is roughly **1 request per second** (or up to ~60 requests per minute).

---

## Running Scripts

A Python virtual environment is set up at `.venv/` in this directory. All scripts should be run using it.

**One-off:**
```bash
.venv/bin/python my_projects.py
```

**Or activate for the session:**
```bash
source .venv/bin/activate
python my_projects.py
deactivate
```

**To install additional packages:**
```bash
.venv/bin/pip install <package>
```

---

## Recommended Actions

*Last reviewed against live API data — 93 observations across 14 sites.*

### ✅ Fixed: `Locations.sh` regenerated

[`Locations.sh`](Locations.sh) now reflects the current 93 observations across 14 sites.

### ✅ Fixed: Missing sites added to `my_locations.py`

`aghabeg`, `trafrask`, `adrigole`, and `derreenacarrin` keywords added to [`PREFERRED_NAME_KEYWORDS`](my_locations.py:25). All sites now cluster correctly.

### ✅ Fixed: `observations_raw.json` refreshed

[`observations_raw.json`](observations_raw.json) now contains all 93 current observations.

### 🟡 High value: Resolve 54 Needs ID observations (58%)

Only 39 of 93 observations (42%) have reached Research Grade. Adding a second ID agreement pushes an observation to Research Grade and contributes to GBIF.

**Quick link:** [View all Needs ID observations for andreiastra](https://www.inaturalist.org/observations/identify?user_id=andreiastra&quality_grade=needs_id)

Highest-priority clusters:

| Site | Needs ID | Notable species awaiting confirmation |
|------|----------|---------------------------------------|
| Lough Hyne | 17 | Cylinder Anemone, Gem Anemone, 6× spider crabs, Aeolidiella alderi/glauca, Thin Bubble-Shell ×2 |
| Gortdubh Pier | 8 | Portuguese Blenny, Tompot Blenny, Sandalled Anemone, Blue-rayed Limpet, Dead Man's Fingers |
| Zetland Pier | 5 | Sea Potato, Toothed Crab, Sea Vase, Connemarra Clingfish, Halichondria bowerbanki |
| Canty's Cove | 5 | Sea Lemon, Pink Coryphella, Aeolid Nudibranch, Atlantic Black Sea Cucumber |
| Seven Heads | 3 | Polycera faeroensis, Blood Stars, Topknot |

The second Football Jersey Worm observation ([395263077](https://www.inaturalist.org/observations/395263077)) is still Needs ID despite the species being Research Grade elsewhere — worth tagging for community attention.

### 🟡 High value: Revisit under-explored sites

| Site | Only find so far | Why go back |
|------|-----------------|-------------|
| Simon's Cove | Strawberry Anemone | 1 dive only — rocky crevices likely hold nudibranchs |
| Barloge Pier | Spiny Squat Lobster | Remote, barely explored — high potential |
| Blind Strand Pier | Tompot Blenny | Pier structure likely holds more fish |
| Trafrask Pier | Seabass + Pouting | 2 obs — fish activity suggests a productive site |
