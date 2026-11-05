#!/usr/bin/env python3
"""Extract structured data from the saved eOceanic Cork pages.

Reads ../raw/index.html and ../raw/pages/*.html (written by fetch_eoceanic.py)
and writes, in the parent folder:
    eoceanic_cork_sites.json   all fields, one object per location, in index order
    Locations.md               a table of every location, grouped into zones, for reading

Nothing is fetched from the network.
"""

import html
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw"

# Zones: see the intro written to Locations.md below. Each is a contiguous range
# of `no` (position on eOceanic's index page, which follows the coast).
ZONES = [
    (1, 15, "East Cork & Cork Harbour"),
    (16, 23, "Kinsale & South Cork Coast"),
    (24, 29, "Seven Heads"),
    (30, 32, "Clonakilty"),
    (33, 35, "Rosscarbery"),
    (36, 40, "Unionhall"),
    (41, 42, "Lough Hyne & Baltimore"),
    (43, 72, "Mizen, Roaringwater Bay & Skibbereen"),
    (73, 79, "Sheep's Head & Dunmanus Bay"),
    (80, 91, "Beara Peninsula & Bantry Bay"),
]


def zone_of(no: int) -> str:
    for first, last, name in ZONES:
        if first <= no <= last:
            return name
    raise ValueError(f"no zone for location no. {no}")
BASE = "https://eoceanic.com/sailing/harbours/europe/ireland/cork/"

# Colour markers for the 1-5 Shelter and Approaches ratings (1 worst, 5 best).
DOTS = {1: "⚫", 2: "🔴", 3: "🟠", 4: "🟡", 5: "🟢"}


def clean(fragment: str) -> str:
    """HTML fragment -> plain text with collapsed whitespace."""
    fragment = re.sub(r"<script.*?</script>", "", fragment, flags=re.S)
    fragment = re.sub(r"<style.*?</style>", "", fragment, flags=re.S)
    fragment = re.sub(r"<br\s*/?>", " ", fragment)
    text = re.sub(r"<[^>]+>", " ", fragment)
    text = html.unescape(text).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def section(page: str, heading: str) -> str:
    """Text under an <h5> heading, up to the next <h5>/<h4>."""
    m = re.search(r"<h5[^>]*>\s*" + re.escape(heading) + r"\s*</h5>", page)
    if not m:
        return ""
    rest = page[m.end():]
    end = re.search(r"<h[45][ >]", rest)
    return clean(rest[: end.start() if end else len(rest)])


def symbols(block: str) -> list[str]:
    return [html.unescape(a) for a in re.findall(r"<img src='/images/harboursymbols/[^']*' alt='([^']*)'", block)]


def parse_index() -> list[dict]:
    idx = (RAW / "index.html").read_text(errors="ignore")
    items = []
    for m in re.finditer(r"<p class='item'><a href='(\d+)/([^']+)'>(.*?)</a><br />", idx, flags=re.S):
        items.append(
            {
                "id": int(m.group(1)),
                "name": clean(m.group(3)),
                "url": f"{BASE}{m.group(1)}/{m.group(2)}",
            }
        )
    return items


def parse_page(path: Path) -> dict:
    page = path.read_text(errors="ignore")
    page = re.sub(r"onclick=\"[^\"]*\"", "", page)
    page = re.sub(r"<script.*?</script>", "", page, flags=re.S)

    out: dict = {}

    # Decimal position from the embedded map link.
    m = re.search(r"map\.php\?latitude=(-?[\d.]+)&longitude=(-?[\d.]+)", page)
    out["latitude"] = float(m.group(1)) if m else None
    out["longitude"] = float(m.group(2)) if m else None

    # Haven position as printed (degrees, decimal minutes) and the note after it.
    m = re.search(r"Haven position</h4>(.*?)<h4", page, flags=re.S)
    pos = clean(m.group(1)) if m else ""
    m2 = re.match(r"(\d+°\s*[\d.]+'\s*[NS],\s*\d+°\s*[\d.]+'\s*[EW])\s*(.*)", pos)
    out["position_dm"] = m2.group(1) if m2 else pos
    out["position_note"] = m2.group(2) if m2 else ""

    m = re.search(r"What (?:is the initial fix|are the initial fixes)\?</h4>(.*?)<div id='manualtides'", page, flags=re.S)
    out["initial_fix"] = clean(m.group(1)) if m else ""

    m = re.search(r"id='summary'.*?</h4>(.*?)<span id='warnings'>", page, flags=re.S)
    out["summary"] = clean(m.group(1)) if m else ""

    m = re.search(r"Minimum depth</div>\s*([\d.]+)\s*metres", page)
    out["min_depth_m"] = float(m.group(1)) if m else None

    # The page lists the Approaches rating first and the Shelter rating second.
    stars = re.findall(r"stars/(\d)star\.svg' alt=\"\d stars: ([^;\"]*)", page)
    out["approaches_stars"] = int(stars[0][0]) if len(stars) > 0 else None
    out["approaches"] = stars[0][1].strip() if len(stars) > 0 else ""
    out["shelter_stars"] = int(stars[1][0]) if len(stars) > 1 else None
    out["shelter"] = stars[1][1].strip() if len(stars) > 1 else ""

    # Symbol lists (the page repeats them for small screens; the first set is enough).
    fac = re.search(r"id='facilitiessummary'>(.*?)<div id='naturesummary'>", page, flags=re.S)
    nat = re.search(r"id='naturesummary'>(.*?)Considerations</b>", page, flags=re.S)
    con = re.search(r"Considerations</b><br /></div>(.*?)</div>", page, flags=re.S)
    out["facilities_symbols"] = symbols(fac.group(1)) if fac else []
    out["nature_symbols"] = symbols(nat.group(1)) if nat else []
    out["considerations_symbols"] = symbols(con.group(1)) if con else []

    m = re.search(r"Last modified.*?<span[^>]*>\s*([A-Za-z]+ \d+\w+ \d{4})", page, flags=re.S)
    out["last_modified"] = m.group(1) if m else ""

    m = re.search(r"id='keyinfo'>(.*?)</div>", page, flags=re.S)
    out["contact"] = clean(m.group(1)) if m else ""

    out["overview"] = ""
    m = re.search(r"Overview(.*?)Keyfacts for", page, flags=re.S)
    if m:
        paras = [clean(p) for p in re.split(r"<br\s*/?>\s*<br\s*/?>|</p>", m.group(1))]
        paras = [p for p in paras if len(p) > 40]
        out["overview"] = paras[0] if paras else ""

    out["how_to_get_in"] = section(page, "How to get in?")
    out["why_visit"] = section(page, "Why visit here?")
    out["facilities_text"] = section(page, "What facilities are available?")
    out["security"] = section(page, "Any security concerns?")
    m = re.search(r"With thanks to:</h5>(.*?)</p>", page, flags=re.S)
    out["thanks_to"] = clean(m.group(1)) if m else ""

    m = re.search(r"Ten nearest havens by straight line.*?:(.*?)These havens are ordered", page, flags=re.S)
    near = []
    if m:
        for a in re.finditer(r"([^\n<>]+?)\s*-\s*([\d.]+)\s*nautical miles?\s*(\w+)", clean(m.group(1))):
            near.append({"name": a.group(1).strip(), "nm": float(a.group(2)), "bearing": a.group(3)})
    out["nearest_havens"] = near
    return out


def main() -> None:
    sites = []
    for item in parse_index():
        files = list((RAW / "pages").glob(f"{item['id']}_*.html"))
        if not files:
            print(f"missing page for {item['id']} {item['name']}")
            continue
        no = len(sites) + 1
        sites.append({"no": no, "zone": zone_of(no), **item, **parse_page(files[0])})

    (ROOT / "eoceanic_cork_sites.json").write_text(json.dumps(sites, indent=2, ensure_ascii=False) + "\n")

    rows = [
        "# eOceanic Cork locations",
        "",
        "In eOceanic's order, which follows the coast clockwise from Youghal to Ardgroom, so roughly east to west. "
        "It is not strictly sorted by longitude: the list follows the shoreline, so it doubles back where the coast does, such as up Bantry Bay. "
        "Generated from [`eoceanic_cork_sites.json`](eoceanic_cork_sites.json) by `scripts/extract_eoceanic.py`; "
        "edit the script, not this file.",
        "",
        "The zones are my own grouping, not eOceanic's, which has none. Each is one unbroken stretch of the coast "
        "in eOceanic's order, so places on the same bay stay together, and where one ends and the next begins is a judgement call. "
        "They are geographic only, say nothing about swell, shelter or dive conditions, and are not the 4 drive-time zones "
        "in the [parent README](../README.md#zones). The boundaries are the `ZONES` list in the script.",
        "",
        "Positions are eOceanic's haven position, which can be some distance from where a diver would enter the water. "
        "Each position links to Google Maps. "
        "Depth is at the anchorage at low water springs. See the [README](README.md).",
        "",
        "## Ratings",
        "",
        "Shelter and Approaches are eOceanic's 1-5 ratings, written for a boat at anchor, not a shore diver. "
        "Higher is better.",
        "",
        "| Rating | Shelter: how well protected the anchorage is | Approaches: how hard the entrance is to navigate |",
        "|---|---|---|",
        "| 🟢 5 | Complete protection: all-round shelter in all reasonable conditions | Safe access: all reasonable conditions |",
        "| 🟡 4 | Good: assured night's sleep except from specific quarters | Straightforward: no overly complex dangers when unaffected by weather from difficult quadrants or tidal consideration |",
        "| 🟠 3 | Tolerable: in suitable conditions a vessel may be left unwatched for an overnight stay | Attentive navigation: daylight access, with dangers that need attention |",
        "| 🔴 2 | Exposed: unattended vessels should be watched from the shore, and a comfortable overnight stay is unlikely | Careful navigation: good visibility and conditions needed, with dangers that require careful navigation |",
        "| ⚫ 1 | Stay-aboard: lunch stop or tide-wait only, exposed or tenuous holding, vessel should not be left unattended | Highly involved navigation: complex dangers that require arduous navigation, good visibility and settled conditions |",
    ]
    for first, last, name in ZONES:
        members = [x for x in sites if first <= x["no"] <= last]
        rows += [
            "",
            f"## {name}",
            "",
            f"Locations {first}-{last}: {len(members)} sites.",
            "",
            "| # | Location | Position (lat, lon) | Shelter | Approaches | Min depth (m) |",
            "|---|---|---|---|---|---|",
        ]
        for x in members:
            rows.append(
                f"| {x['no']} | [{x['name']}]({x['url']}) "
                f"| [{x['latitude']:.5f}, {x['longitude']:.5f}]"
                f"(https://www.google.com/maps/search/?api=1&query={x['latitude']:.5f},{x['longitude']:.5f}) "
                f"| {DOTS[x['shelter_stars']]} {x['shelter_stars']}: {x['shelter']} "
                f"| {DOTS[x['approaches_stars']]} {x['approaches_stars']}: {x['approaches']} "
                f"| {x['min_depth_m']:g} |"
            )
    (ROOT / "Locations.md").write_text("\n".join(rows) + "\n")
    print(f"wrote {len(sites)} sites")


if __name__ == "__main__":
    main()
