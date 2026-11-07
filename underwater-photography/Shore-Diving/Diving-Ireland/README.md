# Diving Ireland (CFT) slipway & dive site data

Dive slipway and site access data sourced from Diving Ireland ([CFT / Comhairle Fo-Thuinn](https://divingireland.ie/) – the Irish Underwater Council). It documents primary dive launch slips and alternative slipways around Ireland, complete with coordinates, safety plans, nautical chart links, and weather references.

## Files

| File | What it is |
|---|---|
| [`Diving_Ireland_Primary_Slips.csv`](Diving_Ireland_Primary_Slips.csv) | Primary dive sites and main boat launch slips across Ireland (34 sites) with emergency plans, CFT dive guides, Navionics charts, wind and tide links |
| [`Diving_Ireland_Alternative_Slips.csv`](Diving_Ireland_Alternative_Slips.csv) | Comprehensive catalogue of secondary and alternative slipways across Ireland (253 slips) with WKT geometry and coordinates |

## Primary slips (`Diving_Ireland_Primary_Slips.csv`)

### Columns

| Column | Description |
|---|---|
| `WKT` | Well-Known Text geometry (`POINT (long lat)`) |
| `Name` | Site or slipway name (e.g. Baltimore, Kinsale, Bantry) |
| `Lat`, `Long` | Decimal coordinates (WGS 84) |
| `Emergency Plan` | Link to CFT emergency response plan PDF (Google Drive) |
| `CFT Dive Site Guide` | Link to CFT dive site briefing and guide PDF (Google Drive) |
| `Chart` | Link to Navionics web chart centered on the site |
| `Wind` | Link to XCWeather localized wind forecast |
| `Tides` | Link to local tide table (Tide Times / Windfinder / Surf-Forecast) |

### Key South & Southwest sites in the primary list

- **Cork**: Baltimore, Bantry, Kinsale, Crookhaven / Mizen Head, Unionhall, Allihies
- **Kerry**: Derrynane, Valentia

## Alternative slips (`Diving_Ireland_Alternative_Slips.csv`)

A wider reference list of 253 coastal and estuarine slipways across Ireland. Useful for finding alternative entry/exit points, sheltered backups when primary slips are busy or exposed, and local pier ramps in West Cork and Kerry (e.g. Cunnamore, Rossbrin, Ahakista, Kilcrohane, Adrigole, Castletownbere, East Ferry, Monkstown, Gyleen).

### Columns

| Column | Description |
|---|---|
| `WKT` | Well-Known Text geometry (`POINT (long lat)`) |
| `Name` | Local slipway or quay name |
| `Lat`, `Long` | Decimal coordinates (WGS 84) |
| `Emergency Plan`, `Dive Site Info`, `Chart` | Reference links where populated |
| `Wind`, `Tides` | Weather and tide forecast links where populated |

## Related

- [`../Google-Maps/`](../Google-Maps/README.md) has saved shore diving pins and coordinates exported from Google Maps.
- [`../eOceanic/`](../eOceanic/README.md) has detailed harbour, pier, anchorage, and shelter data for 91 Cork locations.
- [`../README.md`](../README.md) has the main shore diving overview and zone breakdown for West Cork.
