"""
Shared data preparation for the underwater life-list reports:
one_and_done_ireland.py, rarity_by_site_ireland.py, gap_analysis_ireland.py and
year_in_review.py.

Everything here works on the observations from underwater_ireland.underwater_observations()
(clustered onto a dive site, plus the obscured ones whose site is unknown, whose
site is None). "Species" means an observation identified to species rank; the
observations identified only to genus or higher are left out of the species counts.

Importing this module only defines functions.
"""
import os
import sys
from collections import defaultdict
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from underwater_ireland import underwater_observations  # noqa: E402

OBSCURED_LABEL = "Obscured location"


def underwater_entries(notes):
    """Return [(site, obs)] for every underwater observation in Ireland. site is None if obscured."""
    site_obs, obscured = underwater_observations(notes)
    entries = [(site, o) for site, obs_list in site_obs.items() for o in obs_list]
    entries += [(None, o) for o in obscured]
    return entries


def species_table(entries):
    """Return {taxon_id: {"taxon": taxon, "entries": [(site, obs)]}} for species-rank taxa.

    Entries are sorted by observation date, oldest first.
    """
    table = {}
    for site, obs in entries:
        taxon = obs.get("taxon") or {}
        if taxon.get("rank") != "species":
            continue
        info = table.setdefault(taxon["id"], {"taxon": taxon, "entries": []})
        info["entries"].append((site, obs))
    for info in table.values():
        info["entries"].sort(key=lambda e: e[1].get("observed_on") or "")
    return table


def dives(entries):
    """Return {(date, site): [obs]}. Each distinct date at a site is one dive."""
    result = defaultdict(list)
    for site, obs in entries:
        if obs.get("observed_on"):
            result[(obs["observed_on"], site)].append(obs)
    return dict(result)


def site_label(site):
    return site or OBSCURED_LABEL


def taxon_link(taxon):
    """Markdown link to the taxon page: 'Common name (*Scientific name*)'."""
    sci = taxon.get("name") or ""
    common = taxon.get("preferred_common_name") or sci or "Unidentified"
    label = f"[{common}](https://www.inaturalist.org/taxa/{taxon['id']})"
    return label + (f" (*{sci}*)" if sci and sci != common else "")


def weekday(iso_date):
    return date.fromisoformat(iso_date).strftime("%A")


def pct(part, whole):
    return f"{100 * part / whole:.0f}%" if whole else "—"
