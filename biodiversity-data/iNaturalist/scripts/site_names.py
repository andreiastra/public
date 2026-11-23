"""
Shared keyword → canonical site name mapping.

Maps raw place_guess fragments (from the iNaturalist API) to the canonical
names defined in DIVE_SITES.txt.

── Where the keywords come from ─────────────────────────────────────────────

SITE_KEYWORDS is built from two parts:

  1. Full names, read from DIVE_SITES.txt.  Each site
     gets its own lower-cased name as a keyword ("lough hyne" → Lough Hyne).
     Adding a site to the file is enough for place_guess values that contain
     its full name.

  2. SITE_ALIASES below, written by hand.  These cover place_guess values that
     do not contain the full name:

       Short fragments — "barloge" in "Barloge, Co. Cork, Ireland".

       Townland / OSM aliases — the place_guess contains only an OSM townland
       that has no lexical overlap with the canonical name:
         "Councambeg"     → Simon's Cove
         "Derreenacarrin" → Zetland Pier
       These are verified geographically (the townland is the OSM area that
       contains the pier) and would not be discoverable automatically.

     Aliases need judgement (a bare "simon" matches "Cloghmacsimon, Bandon"),
     so they are not generated.  An alias whose site name is not in the file
     raises a warning when this module is imported.

── When to refresh ──────────────────────────────────────────────────────────

SITE_ALIASES MUST be re-checked whenever new observations are uploaded for a
site whose place_guess does not contain its full name.

To refresh:
  1. Run:  ../.venv/bin/python scripts/generate_location_ratings.py
  2. For each cluster in the warning block at the top of
     reports/Location_ratings.md, inspect the sample place_guess.
  3. Add an alias here with the identifying fragment and the canonical name.
  4. Re-run generate_location_ratings.py to confirm the warning is gone.

── Non-dive locations ────────────────────────────────────────────────────────

IGNORED_KEYWORDS lists place_guess fragments for known terrestrial, birding,
or otherwise non-dive locations.  Any cluster whose place_guess matches one of
these is silently skipped by generate_location_ratings.py — no unresolved-
cluster warning is raised.

Most of the list is read from LAND_SITES.txt (one name per
line, matched case-insensitively).  To silence a new non-dive place, add its
name to that file.  Only keywords that are not place names there (the Egypt
trip, "derrigra") are listed in this module.

── Rules ─────────────────────────────────────────────────────────────────────
  - Full names are matched before aliases.
  - Within SITE_ALIASES, longer / more specific keywords go first.
  - Multiple keywords may map to the same canonical name.
  - Canonical names must match DIVE_SITES.txt exactly.

Imported by:
  scripts/generate_location_ratings.py
"""

import os
import unicodedata
import warnings

_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DIVE_SITES_FILE = os.path.join(_ROOT, "DIVE_SITES.txt")
OTHER_LOCATIONS_FILE = os.path.join(_ROOT, "LAND_SITES.txt")


def _read_names(path):
    """Return the non-empty lines of a names file, stripped and NFC-normalised."""
    with open(path, encoding="utf-8") as f:
        return [unicodedata.normalize("NFC", line.strip()) for line in f if line.strip()]


def load_other_locations(path=OTHER_LOCATIONS_FILE):
    """Return the lower-cased place names in LAND_SITES.txt."""
    return [name.lower() for name in _read_names(path)]


# Fragments that identify non-dive locations.  Clusters whose combined
# place_guess contains any of these are silently excluded from the output.
# The names in LAND_SITES.txt are appended below.
IGNORED_KEYWORDS = [
    # Egypt trip (Red Sea) — not tracked in the West Cork site list
    "egypt",
    "janub sina",      # "Janub Sina', EG"
    "saudi arabia",
    "sharm el sheikh",
    "derrigra",        # inland townland, Co. Cork
] + load_other_locations()

# Short fragments and townland aliases that the full names in
# DIVE_SITES.txt do not cover.
SITE_ALIASES = [
    # place_guess: "Seven Heads, Co. Cork" / "Seven Heads Pier, Co. Cork"
    ("seven heads",    "Seven Heads Pier"),
    # place_guess: "Barloge, Co. Cork, Ireland"
    ("barloge",        "Barloge Pier"),
    # place_guess: "Blind Strand, Co Cork"
    ("blind strand",   "Blind Strand Pier"),
    # place_guess: "Canty's Cove, Ireland" / "Canty's Cove, Cork, Co. Cork"
    ("canty",          "Canty's Cove"),
    # place_guess: "Councambeg, Simon's Cove, Co. Cork"
    # Not a bare "simon": it also matches "Cloghmacsimon, Bandon" (birding).
    ("councambeg",     "Simon's Cove"),
    # place_guess: "Gortdubh Pier, Co. Cork" / "Gortdubh Pier, Knockaphuca, Co. Cork"
    ("gortdubh",       "Gortdubh Pier"),
    # place_guess: "Gortnakilla Pier Sheeps Head, Co. Cork"
    ("gortnakilla",    "Gortnakilla Pier"),
    # place_guess: "M665+44, Bank, Sandmount, Co. Cork"
    ("bank",           "Bank Pier"),
    # Sandmount Bay Beach (M54X+FG3) is ~680 m from Bank Pier and a separate
    # dive site.  Do not add a bare "sandmount" keyword: both sites contain
    # "Sandmount" in their place_guess, so it would merge them.
    # place_guess: "Unnamed Road, Dooneen, Co. Cork"
    ("dooneen",        "Dooneen Pier"),
    # place_guess: "Zetland Pier, Co. Cork" / "Zetland Pier, Derreenacarrin" / "Derreenacarrin, Co. Cork"
    ("derreenacarrin", "Zetland Pier"),
    ("zetland",        "Zetland Pier"),
    # place_guess: "Kilcrohane Pier, Kilcrohane, Co. Cork" / "Unnamed Rd Co. Ireland, Kilcrohane, Co. Cork"
    ("kilcrohane",     "Kilcrohane Pier"),
    # place_guess: "Aghabeg Pier, Knockane, Co. Cork"
    ("aghabeg",        "Aghabeg Pier"),
    # place_guess: "Trafrask Pier, Adrigole, Co. Cork" / "Trafrask Pier, Trafrask, Co. Cork"
    ("trafrask",       "Trafrask Pier"),
    # place_guess: "Garnish Island, Co. Cork"
    ("garnish",        "Garnish Island"),
    # place_guess: "Snave, Ballylickey, Co. Cork"
    ("snave",          "Snave Pier"),
    # place_guess: "Small Sovereign Island, Ireland" / "Small Sovereign Island, Cork, Co. Cork, Ireland"
    ("small sovereign", "Small Sovereign Island"),
    # place_guess: "Audley Cove, Co. Cork" (verify against the generate_location_ratings.py warning block)
    ("audley",         "Audley Cove"),
    # place_guess: "Scapa Flow, United Kingdom"
    ("scapa",          "Scapa Flow"),
    # Reenabulliga Pier — no observations yet; keyword kept for future use
    ("reenabulliga",   "Reenabulliga Pier"),
]

_DIVE_SITES = _read_names(DIVE_SITES_FILE)

for _kw, _name in SITE_ALIASES:
    if _name not in _DIVE_SITES:
        warnings.warn(
            f"site_names.py: alias {_kw!r} points to {_name!r}, "
            f"which is not in {os.path.basename(DIVE_SITES_FILE)}",
            stacklevel=2,
        )

# Full names first, then aliases.  First match wins in every consumer.
SITE_KEYWORDS = [(name.lower(), name) for name in _DIVE_SITES] + SITE_ALIASES
