# West Cork iNaturalist & Underwater Photography — Summary Notes

A consolidated reference document summarizing the observations, dive site biodiversity ratings, scientific highlights, field metadata standards, and developer tools for **Andre Astra** (`andreiastra` / User ID `10958443`) in **West Cork, Ireland**.

---

## 1. Profile & Key Reference Links

* **Account Overview:** `andreiastra` (`ID: 10958443`) — **479+ total observations** across **296+ species**, including **129 subtidal marine records** spanning **20 West Cork dive sites**, plus seasonal coastal wetland and inland Cork sightings.
* **Licensing & Open Science Pipeline:** Default license set to **CC BY-NC** with open geoprivacy. All **Research Grade** observations automatically export weekly to the **Global Biodiversity Information Facility (GBIF)** and feed into Ireland's **National Biodiversity Data Centre (NBDC)**.

| Resource | URL | Purpose |
| :--- | :--- | :--- |
| **iNaturalist Profile** | [inaturalist.org/people/andreiastra](https://www.inaturalist.org/people/andreiastra) | Public observations, species counts, identifications, and journal posts. |
| **Needs ID Verification Queue** | [inaturalist.org/observations/identify?user_id=andreiastra](https://www.inaturalist.org/observations/identify?user_id=andreiastra) | Filtered identification console for promoting unconfirmed records to Research Grade. |
| **Least-Observed Taxa Explorer** | [elias.pschernig.com/wildflower/leastobserved.html?user=andreiastra](https://elias.pschernig.com/wildflower/leastobserved.html?user=andreiastra) | Ranks logged taxa by global rarity on iNaturalist. |
| **True Crabs Gallery (`Brachyura`)** | [inaturalist.org/observations?user_id=andreiastra&taxon_id=121639](https://www.inaturalist.org/observations?user_id=andreiastra&taxon_id=121639) | Live filtered gallery of logged true crab observations. |
| **Decapods Gallery (`Decapoda`)** | [inaturalist.org/observations?user_id=andreiastra&taxon_id=47424](https://www.inaturalist.org/observations?user_id=andreiastra&taxon_id=47424) | Live filtered gallery covering true crabs, squat lobsters, hermit crabs, and lobsters. |
| **Google Colab Workspace** | [colab.research.google.com/drive/1kVHbCJRIewDRhXd8-t0d67D-vpwy7aPl](https://colab.research.google.com/drive/1kVHbCJRIewDRhXd8-t0d67D-vpwy7aPl#scrollTo=flI4KNDDsCv_) | Python workspace for running iNaturalist v1 API extraction and analysis scripts. |

---

## 2. West Cork Dive Site Scorecard (129 Records / 20 Sites)

| Rank | Dive Site | Dives | Total Obs | Unique Species ($S$) | Species / Dive | Primary Ecological Niche | Notable Recorded Taxa |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | **Gortdubh Pier** | 1 | 13 | 12 | **12.0** | Exposed Atlantic bedrock & rich encrusting reef | *Parablennius ruber*, *Alcyonium digitatum*, *Henricia sanguinolenta* |
| 2 | **Aghabeg Pier** | 1 | 7 | 6 | **6.0** | Open pelagic drift & pier epifauna | Pelagic & epifaunal assemblages |
| 3 | **Canty's Cove** | 2 | 8 | 8 | **4.0** | Mixed macro reef & opisthobranch turf | *Edmundsella pedata*, *Prostheceraeus vittatus* |
| 4 | **Lough Hyne** | 6 | 26 | 21 | **3.5** | Sheltered marine reserve; soft silt & steep walls | *Philine quadripartita*, *Akera bullata*, *Anthopleura ballii*, *Tubulanus annulatus* |
| 5 | **Garnish Island** | 1 | 4 | 3 | **3.0** | Sheltered bay & sponge-dominated walls | Encrusting & massive Porifera |
| 6 | **Bank Pier** | 4 | 11 | 11 | **2.8** | Pier pilings & macro opisthobranch habitat | *Triophinae*, *Aplysia punctata*, *Trivia monacha*, *Corella parallelogramma* |
| 7 | **Seven Heads Pier** | 3 | 6 | 6 | **2.0** | Surge crevices & flatworm/crustacean habitat | *Polycera faeroensis* |
| 8 | **Kilcrohane Pier** | 4 | 8 | 7 | **1.8** | Infralittoral macro reef & aeolid nudibranchs | *Facelina annulicornis*, blennies |
| — | **Zetland Pier** | — | — | — | — | Dark rock crevices & under-boulder microhabitat | *Lepadogaster candolii* (Connemarra Clingfish) |
| — | **UC42 Wreck** | 1 | — | — | — | Offshore artificial reef / wreck structure | *Conger conger*, *Trisopterus luscus* |
| — | **Reenabulliga Pier** | 0 | 0 | 0 | **0.0** | *Survey Target (Unlogged)* | Pending exploratory dive |
| — | **Sandmount** | 0 | 0 | 0 | **0.0** | *Survey Target (Unlogged)* | Pending exploratory dive |
| — | **Tragumna** | 0 | 0 | 0 | **0.0** | *Survey Target (Unlogged)* | Pending exploratory dive |

---

## 3. Flagship Scientific & Conservation Highlights

* **Direct Trophic Predation ([Obs #395271306](https://www.inaturalist.org/observations/395271306)):** Football Jersey Worm (*Tubulanus annulatus*) actively extracting a fan worm (*Sabellidae*) from its tube. Rare inter-polychaete predation evidence indexed for **Global Biotic Interactions (GloBI)**.
* **Global Platform Rarities:**
  * **Lobe Shell (*Philine quadripartita*):** Cryptic sand-dwelling bubble snail in Lough Hyne ([Obs #396151006](https://www.inaturalist.org/observations/396151006), [#395268141](https://www.inaturalist.org/observations/395268141); ~143 global iNaturalist records).
  * **Pimplet Anemone (*Anthopleura ballii*):** Logged at $5\text{ m}$ in Lough Hyne ([Obs #396151001](https://www.inaturalist.org/observations/396151001); ~513 global records).
  * **Connemarra Clingfish (*Lepadogaster candolii*):** Crytobenthic crevice-dwelling fish recorded at Zetland Pier ([Obs #395276891](https://www.inaturalist.org/observations/395276891)).
  * **Specialist Opisthobranchs:** *Facelina annulicornis* (Kilcrohane Pier), *Polycera faeroensis* (Seven Heads Pier), and *Aeolidiella alderi* / *A. glauca* (Lough Hyne).
* **Subtidal Thermal & Depth Profiling:** Lough Hyne series (*Inachus phalangium*, *Necora puber*, *Gobius niger*) records quantitative **Depth (`5 m`)** and **Water Temperature (`18°C`)**, supporting vertical zonation and MPA thermal tracking.
* **Coastal Conservation & Terrestrial Phenology:**
  * **IUCN Near Threatened (NT) Waders:** Un-obscured foraging records for **Black-tailed Godwit** (*Limosa limosa*) and **Eurasian Oystercatcher** (*Haematopus ostralegus*) at Courtmacsherry and Rosscarbery estuaries, supporting Irish wetland censuses (I-WeBS).
  * **Terrestrial & Pollinator Records:** Late-summer migrant **Eurasian Hummingbird Hawkmoth** (*Macroglossum stellatarum*), foraging bumblebees (*Bombus* sp. with `Pollen Load: YES`), and rapid same-day Research Grade passerines (European Starling, Great Tit, House Sparrow) in Coolanagh.

---

## 4. Active iNaturalist Collection Projects

All joined projects are dynamic **Collection Projects** that automatically aggregate matching records by GPS coordinates and taxonomy without manual tagging:

* [Biodiversity of Ireland](https://www.inaturalist.org/projects/biodiversity-of-ireland)
* [Wildlife of the UK and Ireland (UK+)](https://www.inaturalist.org/projects/wildlife-of-the-uk-and-ireland-uk)
* [Marine Invertebrates of Britain and Ireland (UK+)](https://www.inaturalist.org/projects/marine-invertebrates-of-britain-and-ireland-uk)
* [Seaslugs of the World](https://www.inaturalist.org/projects/seaslugs-of-the-world)
* [Homoscleromorpha (Marine Sponges) of Britain and Ireland (UK+)](https://www.inaturalist.org/projects/homoscleromorpha-marine-sponges-of-britain-and-ireland-uk)

*(Complementary Irish marine schemes: **Seasearch Ireland**, **Explore Your Shore!**, **Purse Search Ireland**, and **IWDG**.)*

---

## 5. Field Standards, Verification & Seasearch Alignment

### Accelerating `Needs ID` $\rightarrow$ Research Grade
1. **Assign a Higher Taxon ID:** Never leave records as `Unknown`; tag at least `Brachyura`, `Anomura`, `Nudibranchia`, `Doridina`, or `Caprellidae` so specialists see them in filtered queues.
2. **Upload Diagnostic Crops (Photo 2) & Habitat Context (Photo 3):**
   * *Sea slugs:* Rhinophores, oral tentacles, cerata tips, and foot margins.
   * *Spider crabs (`Inachus` / `Macropodia`):* Rostrum tip between eyes, frontal carapace spines, and chelipeds.
   * *Fish (`Blenniidae` / `Gobiidae`):* Orbital tentacles, dorsal fin rays, and facial markings.
   * *Seascape context:* Wider angle ($0.5\text{–}1.5\text{ m}$) showing surrounding substrate or kelp canopy.
3. **Tag Top Identifiers:** Check each taxon page's **Top Identifiers** leaderboard and mention `@username` in comments with depth and substrate context.

### Seasearch-Aligned Observation Fields (OFVs) & Annotations
* **Core GBIF Annotations:** `Life Stage` (`Adult`, `Juvenile`, `Egg`), `Alive or Dead` (`Alive` vs. `Dead`), `Evidence of Organism` (`Organism` vs. `Evidence` for molts/shells/tubes).
* **Physical & Biotope OFVs:** `Depth (m)`, `Water temperature (°C)`, `Visibility (m)`, `Substrate` (`Bedrock`, `Boulders`, `Cobbles`, `Coarse Sand`, `Fine Mud / Silt`, `Biogenic`, `Wreckage`), `Microhabitat` (`Vertical Wall`, `Overhang`, `Crevice / Fissure`, `Under Boulder`, `Sediment Plain`), and `Abundance` / `SACFOR` (`S`, `A`, `C`, `F`, `O`, `R`, `P`).
* **Interactions & Record Linking:** Use `Eating / Preying on` and `Associated Taxon` for trophic/host links, and `Similar Observation Set` or `Associated observation` to link separate encounters without duplicating records.

### Quick Field Note Template
```markdown
**Seasearch Habitat Summary:**
- Dive Profile: Depth [X] m | Temp [X] °C | Vis [X] m
- Seabed Substratum: [Bedrock / Boulder / Mixed Cobble / Fine Silt]
- Microhabitat: [Vertical wall / Surge fissure / Sediment plain]
- Dominant Biotope / Cover: [Laminaria forest / Foliose red algae / Coralline crust / Animal turf]
- Abundance (SACFOR): [S / A / C / F / O / R]
- Survey Method: SCUBA / Seasearch Observer
```

---

## 6. iNaturalist API & Developer Quick Reference

* **Public REST API (`api.inaturalist.org/v1`):** Free JSON endpoints without authentication for read queries (keep rate under **60 requests/min** with a custom `User-Agent`):
  * `GET /v1/observations?user_login=andreiastra`
  * `GET /v1/observations/species_counts?user_login=andreiastra`
  * `GET /v1/users/andreiastra`
  * `GET /v1/projects/user/10958443`
* **Python SDK & MCP Integration:** Use `pyinaturalist` for rate-limited API scripts, or connect AI agents via `uvx inaturalist-mcp` / `npx -y inaturalist-mcp`.