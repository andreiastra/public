# Coordinate matching: Cork shore diving list

How the coordinates for the 55 entries in [`Cork_Shore_Diving.csv`](Cork_Shore_Diving.csv) were obtained, and how they were checked.

The final coordinates are in [`cork_shore_diving_verification.md`](cork_shore_diving_verification.md). Row numbers in this document follow that table (east to west along the coast), not the order of the CSV.

## Summary

| Group | Rows | Source of coordinates |
|---|---|---|
| Dropped pins | 12 | Copied exactly from the `/maps/search/<lat>,<lng>` URL in the export |
| Named places | 43 | Estimated with Gemini, then checked against the pin Google Maps shows. All 43 are marked verified, 33 of them after correction |

Google's export holds no coordinates for named places. Their URLs carry only a feature ID (`!1s0x…:0x…`). The Gemini values were estimates, not something Google returned.

In the verification table, the `Method` column shows how each value was set:

| Method | Rows | Meaning |
|---|---|---|
| URL Parameter | 12 | Dropped pin, taken from the URL |
| Corrected | 33 | Gemini's estimate was replaced with the coordinates Google Maps shows. These are given to 6 decimals |
| Maps Entity | 10 | Gemini's estimate kept |

## What the checks found

Gemini's first estimates were often wrong. Corrected rows moved by these distances:

| Place | Moved by |
|---|---|
| Toor Pier | 9.1 km |
| Canty's Cove | 7.2 km |
| Zetland Pier | 6.8 km |
| Old head pier | 3.0 km |
| Kilkilleen Strand | 2.6 km |
| Trá an Oileáin | 2.4 km |
| Snave Pier | 1.9 km |
| Audley Cove | 1.2 km |
| Nohaval cove | 0.8 km |

Toor Pier, Canty's Cove, Kilkilleen Strand, Trá an Oileáin, Audley Cove, Nohaval cove and Dunnycove Slipway were also compared with the pin Google Maps showed when I loaded each place page in a browser. The corrected values are 1 to 56 m from it.

## Reference sources

None of these is ground truth. They were used to find rows to check, and the Google Maps pin decides.

| Source | What it gives | Limits |
|---|---|---|
| Google Maps place page, loaded in a browser | The pin Google shows for the place (`!3d…!4d…` in the final URL) | Needs a browser that accepts the consent prompt. Plain `curl` or Python requests get no coordinates, because Google puts them in page JavaScript |
| OpenStreetMap Nominatim and Photon | Named piers, beaches and slips | Many small Cork piers are not mapped. Photon often returns the nearest village instead |
| S2 cell in the feature ID | The first half of `0x<cell>:0x…` decodes to an approximate location | Coarse. It was exact for Dreenatra Pier but 4.5 km off for Lough Hyne. Use as a hint only |

## Rows checked last

Four rows were still marked 🔴 after the first round. All four are now verified:

| Row | Place | Result |
|---|---|---|
| 1 | Nohaval cove | Corrected to 51.713833, -8.384667. It moved 0.8 km and is about 30 m from the pin Google showed in my browser check |
| 2 | Roberts Cove Beach | Corrected to 51.742194, -8.310500. It differs from Gemini's value by under 1 m, so this is a precision change only |
| 3 | Oysterhaven slip | Gemini's value kept (51.6935, -8.4422), confirmed by you |
| 4 | Old head pier | Corrected to 51.641778, -8.549389. It moved 3.0 km. OSM has no pier of this name, so I could not check this value independently |

## Verified but with a coarse value

These rows are marked verified and still have Gemini's 4-decimal estimates (about 10 m). Their checks agree, so I'd leave them:

- Oysterhaven slip (3), confirmed by you
- Blind Strand pier (5), 0.3 km from OSM's Blind Strand beach
- Tragumna Bay slip (23), unconfirmed beyond reverse geocoding to Tragumna
- Dooneen Pier (41) and Bank Pier (53), no independent data
- Atlantic Sea Kayaking - Reen Pier (20), 184 m from the pin Google showed. The separate Reen Pier entry (21) was corrected to 51.528472, -9.166806

## Names

The first Gemini file had added names to six untitled dropped pins, such as Myross Island Cove and Sheep Cove West. Those names are no longer in the verification table. Only the notes you wrote in the export remain (Skeaghanore West Pier, Rossbrin Pier, Tralong Bay, Dirk Bay, Secret Pier and Sandmount).

## Notes on the list

- Travara Bay was in the earlier export and is not in the current one, so the list has 55 rows, not 56.
- The earlier resolved CSVs (`Cork_Shore_Diving_Resolved_Coordinates.csv` and `Cork_Shore_Diving_Google_Maps_Resolved.csv`) have been deleted. The verification table now holds the coordinates.
- To decode the S2 cell of a feature ID (`pip install s2sphere`):

```python
import s2sphere
cell = s2sphere.CellId(int("0x4845a3c11d402a29", 16))
print(cell.to_lat_lng().lat().degrees, cell.to_lat_lng().lng().degrees)
```
