# Cork shore diving list (Google Maps export)

My saved Google Maps list "Cork Shore Diving", exported with Google Takeout. It holds the shore dive entry points I've pinned in Cork, mostly piers, slips, coves and beaches in West Cork.

## How it was exported

1. Go to [Google Takeout](https://takeout.google.com).
2. Select **Saved**, described by Google as "Collections of saved links (images, places, web pages, etc.) from Google Search and Maps."
3. Download the export. Each saved list comes out as a `.csv` named after the list, so the "Cork Shore Diving" list became `Cork_Shore_Diving.csv` (I replaced the spaces with underscores).

## Files

| File | What it is |
|---|---|
| [`Cork_Shore_Diving.csv`](Cork_Shore_Diving.csv) | The exported list of shore diving places |

## Columns

The CSV has the columns `Title`, `Note`, `URL`, `Tags` and `Comment`. The first row after the header is empty, so skip it when reading the file.

| Column | What it holds |
|---|---|
| `Title` | The Google Maps place name, or coordinates in degrees, minutes and seconds for dropped pins (e.g. `51°33'03.6"N 9°26'02.1"W`) |
| `Note` | Optional custom note attached to the pin (see [Dropped pins](#dropped-pins)) |
| `URL` | A Google Maps link (see [Coordinates](#coordinates)) |
| `Tags`, `Comment` | Empty in every row |

## What is in the list

| Category | Rows |
|---|---|
| Named Google Maps places | 44 |
| Dropped pins with coordinates | 12 |
| **Total** | **56** |

## Coordinates

Dropped pins carry decimal coordinates directly in their `URL` column (`https://www.google.com/maps/search/<latitude>,<longitude>`). Named places link by Google Place ID without embedded coordinates; cross-referencing them requires matching by name or looking up their location.

### Dropped pins

Decimal coordinates extracted from the URL. Row numbers reflect position in the CSV (excluding the initial empty row).

| Row | Title | Latitude, longitude | Note |
|---|---|---|---|
| 3 | 51°33'03.6"N 9°26'02.1"W | 51.551011, -9.433913 | Skeaghanore West Pier |
| 4 | 51°31'50.0"N 9°28'29.0"W | 51.530562, -9.47472 | Rossbrin Pier |
| 10 | 51°31'40.9"N 9°09'03.1"W | 51.528036, -9.150846 |  |
| 12 | 51°33'21.8"N 9°04'02.9"W | 51.556067, -9.067463 | Tralong Bay |
| 13 | 51°32'25.2"N 8°56'38.0"W | 51.540328, -8.943884 | Dirk Bay |
| 15 | 51°42'46.8"N 9°33'35.9"W | 51.712987, -9.559968 | Secret Pier |
| 16 | 51°39'22.1"N 9°48'04.4"W | 51.656131, -9.801208 | Sandmount |
| 18 | 51°35'39.2"N 8°49'26.1"W | 51.594219, -8.823924 |  |
| 19 | 51°35'42.9"N 8°48'27.9"W | 51.595247, -8.807735 |  |
| 29 | 51°34'54.1"N 8°45'03.3"W | 51.581694, -8.750916 |  |
| 32 | 51°32'24.0"N 9°07'22.9"W | 51.539992, -9.12303 |  |
| 44 | 51°33'35.3"N 9°45'23.8"W | 51.559811, -9.756601 |  |

## Related

- [`../eOceanic/`](../eOceanic/README.md) has data for the 91 eOceanic Cork locations, which I'll cross-reference against this list.
- [`../README.md`](../README.md) has notes on the shore diving spots and coastal zones.
