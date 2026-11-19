# Aligning iNaturalist Observations with Seasearch Standards

A consolidated field and metadata guide for underwater photographers and citizen scientists looking to bridge individual photographic records with formal benthic habitat surveying (Seasearch Ireland / UK).

---

## 1. Overview: Bridging Citizen Science and Benthic Ecology

Standard iNaturalist records capture a **2D geographic point**, a **timestamp**, and **taxonomic identity**[cite: 1, 2]. However, marine ecological research and benthic habitat classification (e.g., EUNIS / JNCC biotope mapping used by Seasearch and Ireland's National Biodiversity Data Centre) require **vertical zonation**, **substrate composition**, **relative abundance**, and **microhabitat associations**[cite: 1, 2].

By systematically enriching your iNaturalist observations with standardized Observation Field Values (OFVs) and structured field notes, your underwater photography directly feeds into statutory marine conservation monitoring, Marine Protected Area (MPA) assessments, and global trophic networks[cite: 1, 2].

---

## 2. Core Observation Fields (OFVs) to Match Seasearch

When creating or editing observations on iNaturalist, add the following community-standardized Observation Fields[cite: 1, 2]:

| Target Seasearch Metric | Recommended iNaturalist OFV | Standard Syntax / Allowed Values | Scientific Rationale |
| :--- | :--- | :--- | :--- |
| **Abundance** | `Abundance` or `SACFOR` | `S` (Superabundant), `A` (Abundant), `C` (Common), `F` (Frequent), `O` (Occasional), `R` (Rare), `P` (Present) | Standardizes population density across visual survey matrices[cite: 1]. |
| **Substratum (Seabed Type)** | `Substrate` | `Bedrock`, `Boulders (>200mm)`, `Cobbles (64–200mm)`, `Pebbles / Gravel`, `Coarse Sand`, `Fine Mud / Silt`, `Biogenic`, `Wreckage`[cite: 1] | Defines physical seabed foundation to determine littoral and sublittoral benthic zones[cite: 1]. |
| **Seabed Feature / Microhabitat** | `Microhabitat` | `Vertical Wall`, `Overhang`, `Crevice / Fissure`, `Under Boulder`, `Wave Surge Gully`, `Horizontal Reef Top`, `Sediment Plain`[cite: 1] | Explains shelter dependencies, surge exposure, and cryptic micro-niches[cite: 1]. |
| **Biological Canopy / Habitat** | `Habitat` or `Associated Taxon` | `Laminaria hyperborea forest`, `Kelp park`, `Foliose red algae turf`, `Encrusting coralline algae`, `Animal turf (hydroids/bryozoans)`, `Zostera bed`[cite: 1] | Enables classification into official JNCC / EUNIS marine biotope codes[cite: 1]. |
| **Vertical Zonation** | `Depth (m)` | Numeric (e.g., `5` or range `4-6`)[cite: 1] | Marine communities stratify steeply based on light attenuation and pressure[cite: 1, 2]. |
| **Water Temperature** | `Water temperature (°C)` | Numeric (e.g., `18`)[cite: 1] | Tracks localized thermoclines, seasonal shifts, and MPA thermal tolerances[cite: 1, 2]. |
| **Water Clarity** | `Visibility (m)` | Numeric (e.g., `4`, `8`)[cite: 1] | Assesses water column turbidity, surge suspension, and plankton blooms[cite: 1]. |
| **Survey Methodology** | `Survey Method` | `SCUBA`, `Snorkel`, `Seasearch Observer`, `Seasearch Surveyor`[cite: 1] | Defines observational effort and sampling gear for data filtering[cite: 1]. |

---

## 3. The SACFOR Abundance Scale

Seasearch uses the **SACFOR** scale to quantify species density without needing absolute individual counts: