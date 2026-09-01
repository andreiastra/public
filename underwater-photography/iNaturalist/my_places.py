"""
Fetches and prints all distinct places associated with observations by a given user.

Uses the iNaturalist API endpoint:
  GET /v1/observations?user_id={user_id}&per_page=200&page={n}

Paginates through all observations, groups them by place name ('place_guess'),
and prints each place with a count and links to individual observations.
"""
import requests

USER_ID = "andreiastra"
BASE_URL = "https://api.inaturalist.org/v1/observations"
PER_PAGE = 200


def fetch_all_observations(user_id):
    observations = []
    page = 1
    while True:
        response = requests.get(BASE_URL, params={
            "user_id": user_id,
            "per_page": PER_PAGE,
            "page": page,
        })
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        observations.extend(results)
        print(f"  Fetched page {page} ({len(results)} observations)...")
        if len(observations) >= data.get("total_results", 0):
            break
        page += 1
    return observations


def main():
    print(f"Fetching observations for user '{USER_ID}'...")
    observations = fetch_all_observations(USER_ID)
    print(f"Total observations fetched: {len(observations)}\n")

    place_obs = {}
    for obs in observations:
        place = obs.get("place_guess") or "Unknown"
        place_obs.setdefault(place, []).append(obs.get("uri", ""))

    places = sorted(place_obs.items(), key=lambda x: x[0])
    print(f"Distinct places ({len(places)}):")
    for place, links in places:
        print(f"\n  {place} ({len(links)})")
        for link in links:
            print(f"    {link}")


if __name__ == "__main__":
    main()
