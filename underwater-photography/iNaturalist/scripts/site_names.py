"""
Shared keyword → canonical site name mapping.

Maps raw place_guess fragments (from the iNaturalist API) to the canonical
names defined in Preferred_dive_site_names.txt.

── How this mapping was built ───────────────────────────────────────────────

Each entry was derived by running:

    .venv/bin/python scripts/my_locations.py

and inspecting the place_guess strings printed under each cluster.  For every
cluster the place_guess values were examined and the shortest substring that
uniquely identifies the site was chosen as the keyword.

Two kinds of entries exist:

  1. Direct matches — the place_guess contains a recognisable fragment of the
     canonical name (e.g. "barloge" in "Barloge, Co. Cork, Ireland").

  2. Townland / OSM aliases — the place_guess contains only an OSM townland
     that has no lexical overlap with the canonical name:
       "Councambeg"   → Simon's Cove
       "Knockaphuca"  → Gortdubh Pier
       "Derreenacarrin" → Zetland Pier
     These are verified geographically (the townland is the OSM area that
     contains the pier) and would not be discoverable automatically.

── When to refresh ──────────────────────────────────────────────────────────

This list MUST be re-verified whenever:
  - A new site is added to Preferred_dive_site_names.txt
  - New observations are uploaded for a site not yet in the list

To refresh:
  1. Run:  .venv/bin/python scripts/my_locations.py
  2. For any cluster labelled "Unknown" or showing a raw place_guess instead
     of a canonical name, inspect the printed place_guess strings.
  3. Add an entry here with the identifying fragment and the canonical name.
  4. Re-run my_locations.py to confirm the cluster resolves correctly.

── Rules ─────────────────────────────────────────────────────────────────────
  - More-specific / longer keywords first (e.g. "bank pier" before "bank").
  - Multiple keywords may map to the same canonical name.
  - Canonical names must match Preferred_dive_site_names.txt exactly.

Imported by:
  scripts/my_locations.py
  scripts/generate_location_ratings.py
"""

SITE_KEYWORDS = [
    # place_guess: "Seven Heads, Co. Cork" / "Seven Heads Pier, Co. Cork"
    ("seven heads",    "Seven Heads Pier"),
    # place_guess: "Barloge, Co. Cork, Ireland"
    ("barloge",        "Barloge Pier"),
    # place_guess: "Blind Strand, Co Cork"
    ("blind strand",   "Blind Strand Pier"),
    # place_guess: "Canty's Cove, Ireland" / "Canty's Cove, Cork, Co. Cork"
    ("canty",          "Canty's Cove"),
    # place_guess: "Councambeg, Simon's Cove, Co. Cork"
    ("councambeg",     "Simon's Cove"),
    ("simon",          "Simon's Cove"),
    # place_guess: "Gortdubh Pier, Co. Cork" / "Gortdubh Pier, Knockaphuca, Co. Cork"
    ("gortdubh",       "Gortdubh Pier"),
    ("knockaphuca",    "Gortdubh Pier"),
    # place_guess: "Gortnakilla Pier Sheeps Head, Co. Cork"
    ("gortnakilla",    "Gortnakilla Pier"),
    # place_guess: "Lough Hyne, Co. Cork"
    ("lough hyne",     "Lough Hyne"),
    # place_guess: "Bank Pier, Sandmount, Co. Cork" / "M665+44, Bank, Sandmount, Co. Cork"
    ("bank pier",      "Bank Pier"),
    ("sandmount",      "Bank Pier"),
    ("bank",           "Bank Pier"),
    # place_guess: "Rosscarbery, Cork, Co. Cork" — also "Cork, Co. Cork" (ambiguous, resolved by cluster)
    ("rosscarbery",    "Rosscarbery"),
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
    # place_guess: "UC42"
    ("uc42",           "UC42"),
    # Tragumna and Reenabulliga Pier — no observations yet; keywords kept for future use
    ("tragumna",       "Tragumna"),
    ("reenabulliga",   "Reenabulliga Pier"),
]
