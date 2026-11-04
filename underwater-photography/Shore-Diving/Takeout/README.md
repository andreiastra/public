# Cork shore diving list (Google Maps export)

My saved Google Maps list "Cork Shore Diving", exported with Google Takeout. It holds the shore dive entry points I've pinned in Cork, mostly piers, slips, coves and beaches in West Cork.

## How it was exported

1. Go to [Google Takeout](https://takeout.google.com).
2. Select **Saved**, described by Google as "Collections of saved links (images, places, web pages, etc.) from Google Search and Maps."
3. Download the export. Each saved list comes out as a `.csv` named after the list, so the "Cork Shore Diving" list became `Cork_Shore_Diving.csv` (I replaced the spaces with underscores).

## Files

| File | What it is |
|---|---|
| [`Cork_Shore_Diving.csv`](Cork_Shore_Diving.csv) | The exported list: 52 places |

## Columns

The CSV has the columns `Title`, `Note`, `URL`, `Tags` and `Comment`. The first row after the header is empty, so skip it when reading the file.

| Column | What it holds |
|---|---|
| `Title` | The Google Maps place name, or for a pin with no place, its coordinates in degrees, minutes and seconds (for example `51°31'05.2"N 9°31'40.0"W`) |
| `Note` | My own note on the pin. Only 4 rows have one, listed below |
| `URL` | A Google Maps link. See [Coordinates](#coordinates) |
| `Tags`, `Comment` | Empty in every row |

## What is in the list

| | Rows |
|---|---|
| Named Google Maps places | 41 |
| Dropped pins with only a coordinate as the title | 11 |
| **Total** | **52** |

## Coordinates

Only the 11 dropped pins have coordinates in the file. They are in the `URL` column as `https://www.google.com/maps/search/<latitude>,<longitude>`. The 41 named places link by Google place id and the file doesn't give their coordinates. To cross-reference them by position you need to look them up (for example by opening the link), or match by name.

Dropped pins, with the decimal coordinates from the URL. The row number is the pin's position in the CSV, not counting the empty row.

| Row | Title | Latitude, longitude | Note |
|---|---|---|---|
| 2 | 51°31'05.2"N 9°31'40.0"W | 51.51811, -9.527766 |  |
| 6 | 51°31'40.9"N 9°09'03.1"W | 51.528036, -9.150846 |  |
| 8 | 51°33'21.8"N 9°04'02.9"W | 51.556067, -9.067463 | Tralong Bay |
| 9 | 51°32'25.2"N 8°56'38.0"W | 51.540328, -8.943884 | Dirk Bay |
| 11 | 51°42'46.8"N 9°33'35.9"W | 51.712987, -9.559968 | Secret Pier |
| 12 | 51°39'22.1"N 9°48'04.4"W | 51.656131, -9.801208 | Sandmount |
| 14 | 51°35'39.2"N 8°49'26.1"W | 51.594219, -8.823924 |  |
| 15 | 51°35'42.9"N 8°48'27.9"W | 51.595247, -8.807735 |  |
| 25 | 51°34'54.1"N 8°45'03.3"W | 51.581694, -8.750916 |  |
| 28 | 51°32'24.0"N 9°07'22.9"W | 51.539992, -9.12303 |  |
| 40 | 51°33'35.3"N 9°45'23.8"W | 51.559811, -9.756601 |  |

The four notes name the pin (Tralong Bay, Dirk Bay, Secret Pier, Sandmount), so those four dropped pins are known sites.

## Related

- [`../eOceanic/`](../eOceanic/README.md) has data for the 91 eOceanic Cork locations, which I'll cross-reference against this list.
- [`../README.md`](../README.md) has notes on the shore diving spots and the zone map.
