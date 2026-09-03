"""
Fetches all observations for a given user and groups them by geolocation.
Observations within 500 metres of each other are treated as the same location.
Each cluster is labelled with a preferred name from Preferred_location_names.txt
matched by keyword against the cluster's constituent place_guess values.

Uses the iNaturalist API endpoint:
  GET /v1/observations?user_id={user_id}&per_page=200&page={n}

Algorithm: greedy clustering — each observation is assigned to the first
existing cluster whose centroid is within 500 m; otherwise a new cluster
is started. The cluster label is then resolved to a preferred name.
"""
import math
import requests

USER_ID = "andreiastra"
BASE_URL = "https://api.inaturalist.org/v1/observations"
PER_PAGE = 200
CLUSTER_RADIUS_M = 500

# Keyword fragments (lowercase) that map to each preferred name.
# Preferred dive site names are listed in Preferred_dive_site_names.txt (alphabetical).
# Preferred non-dive location names are listed in Preferred_other_location_names.txt (alphabetical).
# Site ratings and notes are maintained in Location_ratings.md.
# Order matters — more specific entries first.
PREFERRED_NAME_KEYWORDS = [
    ("seven heads",     "Seven Heads Pier"),
    ("barloge",         "Barloge Pier"),
    ("blind strand",    "Blind Strand Pier"),
    ("canty",           "Canty's Cove"),
    ("simon",           "Simon's Cove"),
    ("councambeg",      "Simon's Cove"),
    ("gortdubh",        "Gortdubh Pier"),
    ("knockaphuca",     "Gortdubh Pier"),
    ("lough hyne",      "Lough Hyne"),
    ("sandmount",       "Bank Pier"),
    ("bank",            "Bank Pier"),
    ("rosscarbery",     "Rosscarbery"),
    ("dooneen",         "Dooneen Pier"),
    ("derreenacarrin",  "Zetland Pier"),
    ("zetland",         "Zetland Pier"),
    ("kilcrohane",      "Kilcrohane Pier"),
    ("aghabeg",         "Aghabeg Pier"),
    ("trafrask",        "Trafrask Pier"),
    ("adrigole",        "Trafrask Pier"),
]


def resolve_preferred_name(place_guesses):
    """Return the preferred name for a cluster given all its place_guess values."""
    combined = " ".join(place_guesses).lower()
    for keyword, preferred in PREFERRED_NAME_KEYWORDS:
        if keyword in combined:
            return preferred
    return place_guesses[0] if place_guesses else "Unknown"


def haversine(lat1, lon1, lat2, lon2):
    """Return the great-circle distance in metres between two points."""
    R = 6_371_000  # Earth radius in metres
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


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


def cluster_observations(observations):
    """
    Group observations into clusters where every member is within
    CLUSTER_RADIUS_M metres of the cluster centroid.
    Returns a list of clusters, each a dict with:
      - label:    place name of the first observation in the cluster
      - centroid: (lat, lon) mean of all members
      - obs:      list of observation dicts
    """
    clusters = []

    for obs in observations:
        lat = obs.get("geojson", {}).get("coordinates", [None, None])[1]
        lon = obs.get("geojson", {}).get("coordinates", [None, None])[0]
        if lat is None or lon is None:
            # No coordinates — put in a catch-all group
            place = obs.get("place_guess") or "Unknown"
            for c in clusters:
                if c["label"] == place and c["centroid"] is None:
                    c["obs"].append(obs)
                    break
            else:
                clusters.append({"label": place, "centroid": None, "obs": [obs]})
            continue

        # Find the nearest cluster whose centroid is within the threshold
        nearest = None
        nearest_dist = float("inf")
        for c in clusters:
            if c["centroid"] is None:
                continue
            clat, clon = c["centroid"]
            dist = haversine(lat, lon, clat, clon)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest = c

        if nearest and nearest_dist <= CLUSTER_RADIUS_M:
            nearest["obs"].append(obs)
            # Recalculate centroid as mean of all member coordinates
            lats = [o["geojson"]["coordinates"][1] for o in nearest["obs"] if o.get("geojson")]
            lons = [o["geojson"]["coordinates"][0] for o in nearest["obs"] if o.get("geojson")]
            nearest["centroid"] = (sum(lats) / len(lats), sum(lons) / len(lons))
        else:
            label = obs.get("place_guess") or f"{lat:.4f}, {lon:.4f}"
            clusters.append({"label": label, "centroid": (lat, lon), "obs": [obs]})

    return clusters


def main():
    print(f"Fetching observations for user '{USER_ID}'...")
    observations = fetch_all_observations(USER_ID)
    print(f"Total observations fetched: {len(observations)}\n")

    clusters = cluster_observations(observations)
    # Resolve each cluster to a preferred name
    for c in clusters:
        place_guesses = [obs.get("place_guess") or "" for obs in c["obs"]]
        c["preferred"] = resolve_preferred_name(place_guesses)

    clusters.sort(key=lambda c: c["preferred"])

    print(f"Location clusters within {CLUSTER_RADIUS_M} m ({len(clusters)} total):")
    for c in clusters:
        centroid_str = f"{c['centroid'][0]:.4f}, {c['centroid'][1]:.4f}" if c["centroid"] else "no coords"
        print(f"\n  {c['preferred']} ({len(c['obs'])}) [{centroid_str}]")
        for obs in c["obs"]:
            print(f"    {obs.get('place_guess') or 'Unknown'}  {obs.get('uri', '')}")


if __name__ == "__main__":
    main()
