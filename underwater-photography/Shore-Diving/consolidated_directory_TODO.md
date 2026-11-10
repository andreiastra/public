# Consolidated directory: required fixes

Review of [`consolidated_shore_diving_coastal_directory.md`](consolidated_shore_diving_coastal_directory.md) against the source data in this folder. Nothing in the directory has been changed yet.

## Sources of truth

| Directory section | Source file |
|---|---|
| 1. Cork shore dive sites (56) | [`Google-Maps/Cork_Shore_Diving_Google_Maps_Resolved.csv`](Google-Maps/Cork_Shore_Diving_Google_Maps_Resolved.csv) |
| 2. CFT primary hubs (34) | [`Diving-Ireland/Diving_Ireland_Primary_Slips.csv`](Diving-Ireland/Diving_Ireland_Primary_Slips.csv) |
| 1. CFT alternative slips column | [`Diving-Ireland/Diving_Ireland_Alternative_Slips.csv`](Diving-Ireland/Diving_Ireland_Alternative_Slips.csv) (253 slips) |
| 3. eOceanic havens (91) | [`eOceanic/eoceanic_cork_sites.json`](eOceanic/eoceanic_cork_sites.json), mirrored in [`eOceanic/Locations.md`](eOceanic/Locations.md) |

## Verified as correct (no action)

- Counts: 56 sites, 91 eOceanic locations, 34 primary hubs, 253 alternative slips (34 + 253 = 287).
- Section 1 latitude/longitude match the resolved Google Maps CSV for all 56 rows (within 1e-4).
- Section 2 hub names and coordinates match the primary slips CSV. Crookhaven and Mizen Head are one source row, reported once.

## Tasks

### 1. Regenerate Section 3 from the JSON (high priority)

Section 3 does not reproduce eOceanic. About 30 of its 91 names do not exist in the JSON, and most rows that do exist differ in stars, depth or position.

- [ ] Write a script (for example `eOceanic/scripts/build_section3.py`) that emits the table directly from `eoceanic_cork_sites.json`.
- [ ] Use the JSON's own numbering (`no`), `name`, `latitude`, `longitude`, `shelter_stars`, `approaches_stars`, `min_depth_m`. Do not hand-edit values.
- [ ] Keep the JSON's order (clockwise from Youghal to Ardgroom). Take the zone grouping from [`Locations.md`](eOceanic/Locations.md).
- [ ] Reuse the 🚫 rule from `Locations.md` (names containing "Island") and state that rule in the footnote.
- [ ] Display `min_depth_m` of `0.0` as "Dries" only if the JSON or source page supports it. Otherwise show the number.

Examples of wrong values in the current table:

| Site | Directory | JSON |
|---|---|---|
| Roberts Cove | 4★ | 2★ Exposed |
| Seven Heads Bay | 2★, 2.5 m | 4★, 7.0 m |
| Dirk Bay | 4★, 1.5 m | 3★, 3.0 m |
| Mill Cove | 4★ | 3★ |
| Blind Harbour | 3★, dries | 4★, 2.0 m |
| Garnish Bay | 2★ | 3★ |
| Youghal | 4★, 1.8 m | 5★, 3.0 m |

Names in the directory with no JSON entry: Monkstown, Rocky Bay, Summercove, South Ring Pier, Union Hall, Tragumna, Church Strand Bay, The Cove, Sherkin Island, Heir Island, Cunnamore Point, Audley Cove, Colla Pier, Cape Clear (North), Skeaghanore / Ballydehob, Rock Island Pier, Dunlough Bay, Canty's Cove, Ahakista, Whiddy Island, Snave Pier, Zetland Pier, Trafrask, Berehaven Harbour, Bank Pier, Pulleen Harbour, Ballydonegan Bay, Allihies Slip, Cod's Head Bight, Coulagh Bay, Kilmakilloge Harbour.

### 2. Rebuild the eOceanic column in Section 1

Section 1 cites havens and ratings that do not exist, for example "Audley Cove Haven 5★", "Bantry Bay South Haven (6.0 m LWS)", "Roaringwater Bay Haven", "Snave Haven / Bantry Head".

- [ ] For each of the 56 sites, find the nearest real haven in the JSON by haversine distance on the resolved coordinates.
- [ ] Print the haven name, `shelter_stars`, `min_depth_m` and the distance to the haven.
- [ ] If the nearest haven is farther than a threshold (suggest 2 km), show "No close eOceanic haven" and the nearest name instead of a rating.
- [ ] Add a note that eOceanic ratings are for anchored boats, as `Locations.md` already says.

### 3. Fix the CFT infrastructure column in Section 1

- [ ] Match each site to the nearest primary hub and the nearest alternative slip by distance, using the two Diving-Ireland CSVs.
- [ ] Replace "Alternative Slipway network" style wording with the actual slip name and distance.
- [ ] Check every "Primary Hub" claim: only Baltimore, Bantry, Kinsale, Crookhaven/Mizen, Unionhall and Allihies are primary hubs in Cork. Note the CSV spells Allihies as "Alihies".
- [ ] Fix "Emergency Plan active" wording. All 34 hubs link to the same PDF, so say "CFT emergency plan (shared document)".

### 4. Resolve the duplicate Reen Pier row

- [ ] Rows 6 and 33 have identical coordinates (51.5318, -9.1658). Either merge them and report 55 unique sites, or keep both and say the count includes one duplicate pin.
- [ ] Update the intro count of 56 to match.

### 5. Rewrite the dive-profile text

The "Diving Profile" column and Section 4 contain depths, species and entry descriptions that come from none of the source files.

- [ ] Decide whether to keep them as personal notes. If kept, label the column "Notes (unverified)".
- [ ] Otherwise remove depths, species and "Excellent visibility" style claims that cannot be traced to a source.
- [ ] Keep the Lough Hyne NPWS permit warning. Verify the current permit rules before relying on it.

### 6. Correct Section 4 after Sections 1 and 3 are fixed

- [ ] Replace the "heavy storm" list. Zetland Pier and Snave Pier are not in eOceanic. Choose sites from the regenerated 5★ list.
- [ ] Remove Holeopen Bay West as an E/SE fallback, since eOceanic rates it 2★ Exposed.
- [ ] Fix the contradiction on tide timing. Section 4.2 says slack water, Section 4.3 says 1.5–2 h before high water, and Section 1 says high water slack. Pick one rule per case: drying sites at or near high water, headland sites at slack.
- [ ] Remove Dursey Sound from the shore-diving tidal list, or mark it as boat-only.
- [ ] Replace the "40 minutes around slack" figure with a sourced figure, or mark it as a rule of thumb.
- [ ] Wind-direction fallbacks should be derived from site orientation. Mark them as guidance, not verified.

### 7. Add a safety disclaimer

- [ ] Add a short header note: this document is planning reference only, not a substitute for local knowledge, tide tables, the marine forecast or a dive plan.

### 8. Validation before closing

- [ ] Script check that every Section 3 row equals its JSON record (stars, depth, lat/lon).
- [ ] Script check that every Section 1 coordinate equals the resolved CSV row.
- [ ] Script check that every named hub or slip in Section 1 exists in the Diving-Ireland CSVs.
- [ ] Spot-check 5 rows against the original eOceanic pages in `eOceanic/raw/pages/`.
- [ ] Check that all counts in the intro match the tables.

## Suggested order

1. Task 1, then Task 2 (they depend on the correct JSON data).
2. Task 3, Task 4.
3. Task 5, Task 6, Task 7.
4. Task 8.

Put the build script in `scripts/` so the directory can be regenerated rather than edited by hand.
