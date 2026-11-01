"""
Rate andreiastra's Research Grade underwater observations in Ireland by how many
Research Grade observations of the taxon exist worldwide on iNaturalist, and write
a Markdown report to OUTPUT/rarity_underwater_worldwide.md.

The observations are the same as in rarity_underwater_ireland.py (Irish dive
sites, Research Grade only). Only the comparison changes: the Irish report counts
distinct observers in Ireland, this one counts observations worldwide (fewest =
rarest). Ties go to the taxon with fewer distinct observers worldwide.

Worldwide counts are far larger than Irish ones, so the rating cut-offs are on a
log scale and differ from rarity_underwater_ireland.py.

Obscured observations are included and flagged, as in the Irish report.

Usage:
  .venv/bin/python scripts/rarity_underwater_worldwide.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from config import OUTPUT_DIR
from rarity_underwater_ireland import generate_report

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "rarity_underwater_worldwide.md")

# (max worldwide Research Grade observations, rating). The first matching row applies.
RATINGS = [
    (1, "Unique"),         # only your observation
    (100, "Very rare"),
    (1_000, "Rare"),
    (10_000, "Uncommon"),
]


def main():
    generate_report(
        place_id=None,
        metric="total",
        ratings=RATINGS,
        title="Rarity of underwater observations in Ireland, ranked worldwide",
        script="rarity_underwater_worldwide.py",
        intro="Rarity is the number of Research Grade observations of the taxon worldwide on "
              "iNaturalist (fewest = rarest). Ties go to the taxon with fewer distinct "
              "observers worldwide. Only your Irish underwater observations are rated.",
        scope="WW",
        output_file=OUTPUT_FILE,
    )


if __name__ == "__main__":
    main()
