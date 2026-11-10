# Coordinate matching: Cork shore diving list

How the coordinates for the 56 entries in [`Cork_Shore_Diving.csv`](Cork_Shore_Diving.csv) were obtained, and how well they match independent sources.

Date of the cross-check: 2026-11-09.

## Summary

| Group | Rows | Source of coordinates | Confidence |
|---|---|---|---|
| Dropped pins | 12 | Copied exactly from the `/maps/search/<lat>,<lng>` URL in the export | Exact |
| Named places | 44 | Produced by Gemini, then checked manually in Google Maps | About 10 m precision at best (4 to 5 decimals). Not exported by Google, and not retrieved through the Places API |

Google's export holds no coordinates for named places. Their URLs carry only a feature ID (`!1s0x…:0x…`), so the 44 values are estimates.

## Files

| File | Role |
|---|---|
| [`Cork_Shore_Diving.csv`](Cork_Shore_Diving.csv) | Original Google Takeout export |
| [`Cork_Shore_Diving_Resolved_Coordinates.csv`](Cork_Shore_Diving_Resolved_Coordinates.csv) | First Gemini result. It also adds names to 6 untitled dropped pins |
| [`Cork_Shore_Diving_Google_Maps_Resolved.csv`](Cork_Shore_Diving_Google_Maps_Resolved.csv) | Second Gemini result. It keeps the original `Note` column and changes 2 coordinates (rows 1 and 9) |
| [`cork_shore_diving_verification.md`](cork_shore_diving_verification.md) | Side-by-side link table for manual comparison. Its coordinates match the first Gemini file |

## Integrity checks

- All three CSVs have 56 rows in the same order.
- In the second file, `Title`, `Note` and `Google_Maps_URL` match the original export on every row.
- The 12 dropped-pin coordinates differ from their URLs by 0 m.
- Compared with the first Gemini file, only rows 1 and 9 changed.
- Two rows share one coordinate: rows 6 and 33 (both Reen Pier, 51.5318, -9.1658). They are different Google places.

## Reference sources used

None of these is ground truth. They are independent hints.

| Source | What it gives | Limits |
|---|---|---|
| OpenStreetMap Nominatim, forward and reverse | Named piers, beaches and slips, plus the area a coordinate falls in | Many small Cork piers and slips are not mapped, so there are no hits for them |
| Photon (Komoot, OSM-based) | Fuzzier name matches, including localities | Often returns the nearest village, not the pier |
| S2 cell in the feature ID | The first half of `0x<cell>:0x…` decodes to an S2 cell with a location | Coarse. It was 0 m off for Dreenatra Pier but 4.5 km off for Lough Hyne. Use as a hint only |

To decode the S2 cell (Python, `pip install s2sphere`):

```python
import s2sphere
cell = s2sphere.CellId(int("0x4845a3c11d402a29", 16))
print(cell.to_lat_lng().lat().degrees, cell.to_lat_lng().lng().degrees)
```

## Results for the named places

### Matches an independent source (within about 1 km)

Rows 2, 5, 6, 7, 21, 22, 23, 24, 36, 42, 47, 52, 53, 55 and 9 (second file).

Rows 2, 7, 22, 23 and 42 are within about 150 m of an OSM feature with the same name. Row 9 (Audley Cove, 51.52895, -9.45195) is about 140 m from OSM and Photon (51.5278, -9.4511). The first file's value was about 1 km off.

### Plausible, not contradicted

Rows 14, 25, 26, 27, 31, 35, 37, 40 and 41. Each is within about 1 km of a matching OSM or Photon feature. Row 40 (Dunmanus Pier) is within 0.3 km of Dunmanus Point and Dunmanus Harbour. Row 37 (Lough Hyne) is the right area, but no source gave an exact point.

### Probably wrong, needs a manual check

| Row | Place | Current value | Reference suggests | Offset |
|---|---|---|---|---|
| 1 | Castlehaven Strand | 51.5206, -9.1755 | 51.5180, -9.1887 (OSM and Photon agree) | about 1 km. The first file was within 20 m, so row 1 may have got worse. |
| 17 | Canty's Cove | 51.5832, -9.6641 | 51.5260, -9.7098 (OSM and Photon agree) | about 7 km |
| 50 | Zetland Pier | 51.7385, -9.5280 | 51.6952, -9.5975 (OSM) | about 6.8 km |
| 8 | Kilkilleen Strand | 51.5124, -9.4312 | about 51.529, -9.396 (the Kilkilleen place; the S2 cell is similar) | about 3 km |
| 38 | Toor Pier | 51.5218, -9.6784 | about 51.490, -9.805 (the Toor locality; the S2 cell also lies west) | about 9 km |
| 48 | Snave Pier | 51.7248, -9.4795 | 51.7277, -9.4525 (OSM pier) | about 1.9 km |

### Uncertain

| Row | Place | Note |
|---|---|---|
| 6, 33 | Reen Pier | Two Google places with identical coordinates. OSM puts Reen Pier at 51.5284, -9.1666, about 0.4 km away. |
| 11 | Trá an Oileáin | OSM and Photon point about 2.3 km north-east, but only to farmland areas. |
| 39 | Gortdubh Pier | The nearest name match is Gortduff, about 4 km south-west. This may be a different place. |
| 20, 28, 30 | Travara Bay, Seven Heads Pier, Lehenagh Slip Way | No solid match. The nearby results are a guest house, a peninsula and a locality 5 km away. |

### No independent data

Rows 43, 45, 46, 49, 51, 54 and 56 have no OSM or Photon match. A missing match is not evidence that a value is wrong.

Row 34 (Tragumna Bay slip) also has no OSM match. Photon returned only unrelated results ("Slip Heights" and "Slip Park", about 24 km away), and the S2 cell is about 3 km away. The point reverse-geocodes to Tragumna, so I did not flag it.

## Dropped pins with Gemini-added names

The first Gemini file named 6 dropped pins that have no name in the export. The names are guesses, except where noted.

| Row | Added name |
|---|---|
| 10 | Myross Island Cove |
| 18 | Sheep Cove West |
| 19 | Sheep Cove East |
| 29 | Dunworly Bay (reverse geocode gives "Dunworley Slipway", so partly supported) |
| 32 | Rabbit Island Sound |
| 44 | Ballynatra / Trá Ruaim Cove |

## Open items

- Check rows 1, 8, 17, 38, 48 and 50 in Google Maps and record the correct coordinates.
- Decide whether rows 6 and 33 should share one point.
- Change `Resolution_Method` in the second file from "Google Maps Place entity resolution" to something like "Gemini-estimated, manually checked". Google did not return these values.
- Pick one resolved CSV as canonical.
