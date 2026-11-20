"""
Shared constants for the GBIF scripts.

Import from here rather than redefining values in each script:

    from config import RECORDED_BY, OCCURRENCE_SEARCH_URL, PAGE_SIZE

── Verify IDs before adding them ────────────────────────────────────────────
Confirm every new key against the API and record the source URL in the comment
beside it:

    curl -s "https://api.gbif.org/v1/dataset/50c9509d-22c7-4a22-a47d-8c48425ef4a7"
    curl -s "https://api.gbif.org/v1/species/match?name=Tubulanus%20annulatus"
"""

import os

# ── Output ────────────────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports"))  # generated reports, for the reader
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache")  # working data, git-ignored
# The iNaturalist scripts decide what "underwater" means (underwater_ireland.py).
INATURALIST_SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "iNaturalist", "scripts"))

# ── Recorder ──────────────────────────────────────────────────────────────────
# GBIF has no user id for iNaturalist records. The iNaturalist display name is
# stored in the Darwin Core field recordedBy, so this is a text match, not an id.
# iNaturalist login: andreiastra (numeric ID 10958443).
RECORDED_BY = "Andre Astra"
INATURALIST_USER_ID = "andreiastra"  # used only to compare against iNaturalist (sync_status.py)

# ── API ───────────────────────────────────────────────────────────────────────
API_BASE              = "https://api.gbif.org/v1"
OCCURRENCE_URL        = f"{API_BASE}/occurrence"
OCCURRENCE_SEARCH_URL = f"{OCCURRENCE_URL}/search"
SPECIES_MATCH_URL     = f"{API_BASE}/species/match"
DATASET_URL           = f"{API_BASE}/dataset"
SPECIES_URL           = f"{API_BASE}/species"
LITERATURE_SEARCH_URL = f"{API_BASE}/literature/search"
DOWNLOAD_DATASET_URL  = f"{API_BASE}/occurrence/download/dataset"
INATURALIST_OBSERVATIONS_URL = "https://api.inaturalist.org/v1/observations"
INATURALIST_PER_PAGE         = 200   # iNaturalist API maximum
PAGE_SIZE             = 300   # API maximum for /occurrence/search
LITERATURE_PAGE_SIZE  = 500   # /literature/search accepts at least 500 (1000 fails)
TAXON_BATCH           = 100   # taxon keys per /literature/search request (keeps the URL short)
OCCURRENCE_FACET_LIMIT = 100000  # facetLimit for gbifOccurrenceKey; the whole index cites about 1,300 keys

THROTTLE_S            = 1     # be polite; GBIF asks for reasonable request rates

# ── Datasets ──────────────────────────────────────────────────────────────────
# https://api.gbif.org/v1/dataset/50c9509d-22c7-4a22-a47d-8c48425ef4a7
# "iNaturalist Research-grade Observations". Only research-grade iNaturalist
# observations with an open licence reach GBIF.
INATURALIST_DATASET_KEY = "50c9509d-22c7-4a22-a47d-8c48425ef4a7"

# ── Countries (ISO 3166-1 alpha-2) ────────────────────────────────────────────
IRELAND = "IE"

# ── Sites ─────────────────────────────────────────────────────────────────────
# Lough Hyne, Co. Cork (centre 51°30'10.5"N 9°18'10.4"W): the polygon drawn around the lough
# in the GBIF occurrence search (Location filter). WKT, longitude first.
LOUGH_HYNE_POLYGON = "POLYGON((-9.29748 51.51075,-9.3163 51.50589,-9.30232 51.48843,-9.28454 51.49507,-9.29748 51.51075))"
