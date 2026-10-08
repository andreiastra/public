"""
Shared constants for the iNaturalist scripts.

Import from here rather than redefining values in each script:

    from config import USER_ID, OBSERVATIONS_URL, PER_PAGE

── Verify IDs before adding them ────────────────────────────────────────────
A wrong place_id or taxon_id does not raise an error — the API silently
returns data for a different place or taxon (e.g. place 6788 is Chuquisaca,
Bolivia, not Ireland).  Confirm every new ID against the API and record the
source URL in the comment beside it:

    curl -s "https://api.inaturalist.org/v1/places/autocomplete?q=Ireland"
    curl -s "https://api.inaturalist.org/v1/taxa?q=Nudibranchia&rank=order"
    curl -s "https://api.inaturalist.org/v1/places/6718"
"""

import os

# ── Output ────────────────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "OUTPUT")  # generated reports

# ── User ──────────────────────────────────────────────────────────────────────
USER_ID = "andreiastra"  # numeric ID 10958443

# ── API ───────────────────────────────────────────────────────────────────────
API_BASE         = "https://api.inaturalist.org/v1"
OBSERVATIONS_URL = f"{API_BASE}/observations"
PER_PAGE         = 200   # API maximum
THROTTLE_S       = 1     # recommended ~1 request/second

# ── Geospatial clustering ─────────────────────────────────────────────────────
CLUSTER_RADIUS_M = 500   # observations within this distance form one location

# ── Places ────────────────────────────────────────────────────────────────────
IRELAND_PLACE_ID = 6718  # https://www.inaturalist.org/places/6718

# ── Taxa ──────────────────────────────────────────────────────────────────────
AVES_TAXON_ID         = 3      # https://www.inaturalist.org/taxa/3 (birds)
NUDIBRANCHIA_TAXON_ID = 47113  # https://www.inaturalist.org/taxa/47113 (nudibranchs)
