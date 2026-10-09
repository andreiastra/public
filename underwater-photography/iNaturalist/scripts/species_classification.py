"""
Fetch all of andreiastra's iNaturalist observations in Ireland and write a species
classification and organism types report with photo thumbnails to OUTPUT/species_classification.md.

Usage:
  .venv/bin/python scripts/species_classification.py
"""
import collections
import os
import time
from datetime import date

import requests

from config import (
    IRELAND_PLACE_ID,
    OBSERVATIONS_URL,
    OUTPUT_DIR,
    PER_PAGE,
    THROTTLE_S,
    USER_ID,
)
from generate_location_ratings import photo_md

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "species_classification.md")


def fetch_ireland_observations(notes):
    """Fetch all observations for USER_ID in Ireland (place_id=IRELAND_PLACE_ID)."""
    print(f"Fetching observations in Ireland for '{USER_ID}' from iNaturalist…")
    all_obs, page = [], 1
    while True:
        try:
            r = requests.get(
                OBSERVATIONS_URL,
                params={
                    "user_id": USER_ID,
                    "place_id": IRELAND_PLACE_ID,
                    "per_page": PER_PAGE,
                    "page": page,
                },
                timeout=30,
            )
            r.raise_for_status()
        except requests.exceptions.Timeout:
            notes.append(f"API timeout on page {page} — output may be incomplete.")
            print(f"  WARNING: timeout on page {page}, stopping early.")
            break
        except requests.exceptions.HTTPError as exc:
            notes.append(f"API HTTP error on page {page}: {exc} — output may be incomplete.")
            print(f"  WARNING: HTTP error on page {page}: {exc}, stopping early.")
            break
        except requests.exceptions.RequestException as exc:
            notes.append(f"API network error on page {page}: {exc} — output may be incomplete.")
            print(f"  WARNING: network error on page {page}: {exc}, stopping early.")
            break

        data = r.json()
        results = data.get("results", [])
        all_obs.extend(results)
        print(f"  page {page}: {len(results)} obs  (running total: {len(all_obs)})")
        if not results or len(all_obs) >= data.get("total_results", 0):
            break
        page += 1
        time.sleep(THROTTLE_S)

    print(f"Total: {len(all_obs)} observations in Ireland\n")
    return all_obs


def obs_url(obs):
    return obs.get("uri") or f"https://www.inaturalist.org/observations/{obs['id']}"


def names(obs):
    taxon = obs.get("taxon") or {}
    sci   = taxon.get("name") or ""
    return taxon.get("preferred_common_name") or sci or "Unidentified", sci


def species_type(obs):
    """Categorize an observation into a clean, human-friendly organism type."""
    taxon = obs.get("taxon") or {}
    ancestors = set(taxon.get("ancestor_ids") or [])
    common = (taxon.get("preferred_common_name") or "").lower()
    sci = (taxon.get("name") or "").lower()

    # Birds, Mammals, Reptiles, Amphibians (check before generic chordates)
    if 3 in ancestors or taxon.get("iconic_taxon_name") == "Aves":
        return "Bird"
    if 40151 in ancestors or taxon.get("iconic_taxon_name") == "Mammalia":
        return "Mammal"
    if 26036 in ancestors or taxon.get("iconic_taxon_name") == "Reptilia":
        return "Reptile"
    if 20978 in ancestors or taxon.get("iconic_taxon_name") == "Amphibia":
        return "Amphibian"

    # Fish (Ray-finned fishes, Sharks/Rays, etc.)
    if 47178 in ancestors or 47273 in ancestors or 85497 in ancestors or taxon.get("iconic_taxon_name") == "Actinopterygii":
        return "Fish"

    # Tunicates / Sea Squirts
    if 47811 in ancestors or 130868 in ancestors or "ascidian" in common or "sea squirt" in common:
        return "Sea Squirt"

    # Nudibranchs & Sea Slugs / Sea Hares
    if 47113 in ancestors:
        return "Nudibranch"
    if 48656 in ancestors or 48657 in ancestors or 775800 in ancestors or "seahare" in common or "sea hare" in common:
        return "Sea Hare"
    if 551391 in ancestors or 482650 in ancestors or 482657 in ancestors or 482656 in ancestors or any(
        w in common for w in [
            "sea slug", "slug", "dorid", "aeolis", "coryphella", "cadlina",
            "limacia", "polycera", "janolus", "bubble-shell", "bubble shell", "lobe shell"
        ]
    ):
        return "Sea Slug"

    # Crustaceans
    if 121639 in ancestors or 123825 in ancestors:
        if "squat lobster" in common or "galathea" in sci or "munida" in sci:
            return "Squat Lobster"
        return "Crab"
    if 47186 in ancestors:  # Decapoda
        if "prawn" in common or "shrimp" in common or "palaemon" in sci:
            return "Shrimp"
        if "lobster" in common or "homarus" in sci or "palinurus" in sci:
            return "Lobster"
        if "crab" in common:
            return "Crab"
        return "Crustacean"
    if 47120 in ancestors:  # Arthropoda
        if 47158 in ancestors or taxon.get("iconic_taxon_name") == "Insecta":
            return "Insect"
        if 47119 in ancestors or taxon.get("iconic_taxon_name") == "Arachnida":
            return "Arachnid"
        if "barnacle" in common:
            return "Barnacle"
        return "Crustacean"

    # Worms & Flatworms
    if 52319 in ancestors:
        return "Flatworm"
    if 47491 in ancestors or 47492 in ancestors or 51280 in ancestors or "worm" in common:
        return "Worm"

    # Sponges
    if 48824 in ancestors:
        return "Sponge"

    # Echinoderms
    if 47720 in ancestors:
        return "Sea Cucumber"
    if 47668 in ancestors:
        return "Starfish"
    if 47651 in ancestors:
        return "Sea Urchin"
    if 47686 in ancestors:
        return "Brittle Star"
    if 47685 in ancestors:
        return "Feather Star"
    if 47549 in ancestors:
        return "Echinoderm"

    # Cnidarians
    if 47796 in ancestors or 47797 in ancestors or 47705 in ancestors or 152818 in ancestors or any(w in common for w in ["anemone", "snakelocks"]):
        return "Anemone"
    if 47532 in ancestors or 340493 in ancestors or 121454 in ancestors or 51198 in ancestors or "coral" in common or "sea fan" in common or "dead man" in common:
        return "Coral"
    if 48921 in ancestors or 48324 in ancestors or 48328 in ancestors or 48332 in ancestors or 551473 in ancestors or "jelly" in common:
        if "hydroid" in common or "halecium" in sci or "obelia" in sci:
            return "Hydroid"
        return "Jellyfish"
    if 51778 in ancestors:
        return "Comb Jelly"
    if 47534 in ancestors or 47533 in ancestors:
        return "Cnidarian"

    # Bryozoans
    if 47820 in ancestors or "bryozoan" in common:
        return "Bryozoan"

    # Molluscs
    if 47116 in ancestors or any(w in common for w in ["scallop", "mussel", "clam", "oyster"]):
        return "Bivalve"
    if 47459 in ancestors or any(w in common for w in ["octopus", "cuttlefish", "squid"]):
        return "Cephalopod"
    if 47114 in ancestors:
        if "limpet" in common:
            return "Limpet"
        if any(w in common for w in ["cowrie", "top shell", "periwinkle", "whelk", "snail", "tower shell"]):
            return "Sea Snail"
        return "Gastropod"
    if 47115 in ancestors:
        return "Mollusc"

    # Plants & Algae & Fungi
    if 47126 in ancestors or taxon.get("iconic_taxon_name") == "Plantae":
        return "Plant"
    if 47170 in ancestors or taxon.get("iconic_taxon_name") == "Fungi":
        return "Fungi"
    if 67333 in ancestors or any(w in common for w in ["algae", "kelp", "seaweed", "thongweed"]):
        return "Seaweed / Algae"
    if "beggiatoa" in sci:
        return "Bacteria"

    iconic = taxon.get("iconic_taxon_name")
    return iconic or "Other"


def render(obs_list, notes):
    research = sum(1 for o in obs_list if o.get("quality_grade") == "research")
    dates    = {o.get("observed_on") for o in obs_list if o.get("observed_on")}
    species  = collections.Counter((names(o)[0], names(o)[1], species_type(o)) for o in obs_list)
    type_counts = collections.Counter(species_type(o) for o in obs_list)

    lines = [
        f"# Species Classification & Organism Types (Ireland) for {USER_ID}\n",
        f"> Generated by `scripts/species_classification.py` on {date.today()} "
        f"from live iNaturalist data for `{USER_ID}` (Ireland observations, `place_id={IRELAND_PLACE_ID}`).\n",
    ]
    lines += [f"> ⚠️ {n}" for n in notes]
    lines += [
        f"\n**{len(obs_list)}** observations · **{len(species)}** taxa · "
        f"**{len(dates)}** dates · **{research}** Research Grade, "
        f"**{len(obs_list) - research}** need ID\n",
        "## Summary by Organism Type\n",
        "| Organism Type | Observations | Distinct Taxa |",
        "|---|---:|---:|",
    ]

    # Type breakdown table
    taxa_by_type = collections.defaultdict(set)
    for (common, sci, sp_type), _ in species.items():
        taxa_by_type[sp_type].add((common, sci))

    for sp_type, count in type_counts.most_common():
        distinct_taxa = len(taxa_by_type[sp_type])
        lines.append(f"| **{sp_type}** | {count} | {distinct_taxa} |")

    lines += [
        "\n## Species\n",
        "| Species | Type | Observations |",
        "|---|---|---:|",
    ]
    for (common, sci, sp_type), count in sorted(species.items(), key=lambda kv: (-kv[1], kv[0][0].lower())):
        label = f"**{common}**" + (f" (*{sci}*)" if sci and sci != common else "")
        lines.append(f"| {label} | {sp_type} | {count} |")

    lines += [
        "\n## Observations\n",
        "| Photo | Date | Species | Type | Location | Grade |",
        "|---|---|---|---|---|---|",
    ]
    for obs in sorted(obs_list, key=lambda o: o.get("observed_on") or "", reverse=True):
        common, sci = names(obs)
        sp_type = species_type(obs)
        label = f"[{common}]({obs_url(obs)})" + (f" (*{sci}*)" if sci and sci != common else "")
        place = obs.get("place_guess") or "—"
        grade = "Research" if obs.get("quality_grade") == "research" else "Needs ID"
        lines.append(f"| {photo_md(obs)} | {obs.get('observed_on') or '—'} | {label} | {sp_type} | {place} | {grade} |")

    return "\n".join(lines) + "\n"


def main():
    notes = []
    observations = fetch_ireland_observations(notes)
    if not observations:
        print(f"No observations found in Ireland for {USER_ID}.")
        return
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(render(observations, notes))
    print(f"Saved {len(observations)} observations → {os.path.normpath(OUTPUT_FILE)}")


if __name__ == "__main__":
    main()
