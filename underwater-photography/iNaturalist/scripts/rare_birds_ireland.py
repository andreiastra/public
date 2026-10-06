"""
Fetches all bird (Aves) observations for a given iNaturalist user in Ireland
and ranks each species by how rarely it is recorded in Ireland overall.

Rarity is measured by the number of distinct observers who have recorded the
species in Ireland on iNaturalist — a species seen by only a handful of people
is genuinely rare, independent of how many times any one person photographed it.

Uses the iNaturalist API endpoints:
  GET /v1/observations?user_id={user_id}&taxon_id=3&place_id={ireland_id}
  GET /v1/observations/observers?taxon_id={taxon_id}&place_id={ireland_id}

Throttle: ~0.5 s between per-taxon requests to respect the API rate limit.

Usage:
  .venv/bin/python scripts/rare_birds_ireland.py
"""

import time

import requests

BASE = "https://api.inaturalist.org/v1"
USER = "andreiastra"
IRELAND_PLACE_ID = 6718  # https://www.inaturalist.org/places/6718


def fetch_bird_observations(user: str, place_id: int) -> list[dict]:
    """Return all Aves observations for *user* within *place_id*."""
    observations: list[dict] = []
    page = 1
    while True:
        r = requests.get(
            f"{BASE}/observations",
            params={
                "user_id": user,
                "taxon_id": 3,  # Aves
                "place_id": place_id,
                "per_page": 200,
                "page": page,
            },
        )
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])
        observations.extend(results)
        if not results or len(observations) >= data.get("total_results", 0):
            break
        page += 1
        time.sleep(1)
    return observations


def ireland_observer_count(taxon_id: int, place_id: int) -> int:
    """Return the number of distinct observers for *taxon_id* in *place_id*."""
    r = requests.get(
        f"{BASE}/observations/observers",
        params={"taxon_id": taxon_id, "place_id": place_id, "per_page": 1, "verifiable": "any"},
    )
    r.raise_for_status()
    return r.json().get("total_results", 0)


def main() -> None:
    print(f"Fetching bird observations for {USER} in Ireland (place {IRELAND_PLACE_ID})…")
    observations = fetch_bird_observations(USER, IRELAND_PLACE_ID)
    print(f"  {len(observations)} observations found.")

    # Collect unique taxa
    taxa: dict[int, dict] = {}
    for obs in observations:
        t = obs.get("taxon")
        if not t:
            continue
        tid: int = t["id"]
        if tid not in taxa:
            taxa[tid] = {
                "common": t.get("preferred_common_name") or t.get("name"),
                "name": t.get("name"),
                "my_observations": [],
            }
        taxa[tid]["my_observations"].append(
            {
                "id": obs["id"],
                "date": obs.get("observed_on"),
                "place": obs.get("place_guess"),
                "quality": obs.get("quality_grade"),
            }
        )

    print(f"  {len(taxa)} unique taxa. Fetching Ireland-wide observer counts…")
    for tid, info in taxa.items():
        info["ireland_observers"] = ireland_observer_count(tid, IRELAND_PLACE_ID)
        time.sleep(0.5)

    # Sort rarest first (fewest distinct observers in Ireland)
    ranked = sorted(taxa.items(), key=lambda x: x[1]["ireland_observers"])

    print(
        f"\n{'Rank':<5} {'Common Name':<40} {'Scientific Name':<35} {'IE observers':>12}  {'My obs':>6}  Observation IDs & Dates & Locations"
    )
    print("-" * 150)
    for rank, (tid, info) in enumerate(ranked, start=1):
        my = info["my_observations"]
        obs_ids = ", ".join(str(o["id"]) for o in sorted(my, key=lambda o: o["date"] or ""))
        dates = ", ".join(sorted({o["date"] for o in my if o["date"]}))
        places = ", ".join(sorted({o["place"] for o in my if o["place"]}))
        print(
            f"{rank:<5} {info['common']:<40} {info['name']:<35} {info['ireland_observers']:>12}  {len(my):>6}  [{obs_ids}] {dates} | {places}"
        )


if __name__ == "__main__":
    main()
