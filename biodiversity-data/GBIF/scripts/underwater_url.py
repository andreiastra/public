"""
Print a gbif.org occurrence search URL for the underwater species recorded in an area.

GBIF occurrences have no habitat field, so "underwater" comes from the taxon, as in
cork_underwater.py (marine.py): a species counts when a GBIF species profile marks it as marine,
without birds and flowering plants. This script does that for the area you give it:

  1. one /occurrence/search call with `geometry`, occurrenceStatus=PRESENT, mediaType=StillImage,
     limit=0 and facet=speciesKey lists the species that have a photo in the area
  2. the marine check keeps the underwater ones
  3. the URL has one `taxonKey` per species. gbif.org takes a Catalogue of Life ID there
     (`DXNZ`), not the numeric GBIF key, so the IDs come from cork_underwater.col_id

Checking each species, rather than whole groups, keeps snails, crabs, worms and wrasse in and
land species out, so no underwater species recorded in the area is missed. A species with no
exact Catalogue of Life match is left out, with a warning on stderr. Records identified only
above species (a genus, say) have no speciesKey and are not in the URL. A species first
recorded in the area after the run is not in the URL until it is run again.

The URL has the filters occurrenceStatus=DETECTED and mediaType=StillImage, the same as the links
in reports/cork_underwater.md. The first run for an area fetches names and IDs for its species,
which are kept in scripts/.cache/west_cork_species.json (shared with cork_underwater.py).

Usage:
  ../.venv/bin/python scripts/underwater_url.py --geometry "POLYGON((-9.29748 51.51075,-9.3163 51.50589,-9.30232 51.48843,-9.28454 51.49507,-9.29748 51.51075))"
"""
import argparse
import os
import sys
from urllib.parse import quote_plus

sys.path.insert(0, os.path.dirname(__file__))
from config import OCCURRENCE_SEARCH_URL
import cork_underwater as cu
from marine import get

SEARCH_URL = "https://www.gbif.org/occurrence/search"


def species_in_area(geometry):
    """{speciesKey: photos} for present occurrences with a photo inside the geometry."""
    data = get(OCCURRENCE_SEARCH_URL, geometry=geometry, occurrenceStatus="PRESENT", mediaType="StillImage",
               limit=0, facet="speciesKey", facetLimit=cu.FACET_LIMIT, facetMincount=1)
    return {c["name"]: c["count"] for c in data["facets"][0]["counts"]} if data["facets"] else {}


def underwater_url(geometry):
    """(url, species, [names without an ID]) for the underwater species with a photo inside `geometry`."""
    counts = species_in_area(geometry)
    species = cu.marine_species(list(counts))
    ids = list(dict.fromkeys(s["col"] for s in species.values() if s.get("col")))  # a synonym shares its accepted name's ID
    missing = [s["name"] for s in species.values() if not s.get("col")]
    url = (SEARCH_URL + "?geometry=" + quote_plus(geometry) + "&occurrenceStatus=DETECTED&mediaType=StillImage"
           + "".join(f"&taxonKey={i}" for i in ids))
    return url, species, missing


def main():
    parser = argparse.ArgumentParser(description="Print a gbif.org search URL for the underwater species in an area.")
    parser.add_argument("--geometry", required=True,
                        help='WKT polygon, longitude first, e.g. "POLYGON((-9.5 51.8,-9.4 51.8,-9.4 51.7,-9.5 51.8))"')
    args = parser.parse_args()
    url, species, missing = underwater_url(args.geometry)
    for name in missing:
        print(f"Warning: no exact Catalogue of Life match for {name}, left out", file=sys.stderr)
    print(f"{len(species)} underwater species with a photo in the area, {len(url)} characters in the URL", file=sys.stderr)
    print(url)


if __name__ == "__main__":
    main()
