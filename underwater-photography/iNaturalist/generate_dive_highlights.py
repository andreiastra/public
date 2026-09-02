"""
Generates dive-highlights-west-cork.html from live iNaturalist API data.

Usage:
    .venv/bin/python generate_dive_highlights.py

The script fetches all observations for USER_ID, then builds the HTML using
the curated configuration below (DIVE_SITES, STANDOUT_SIGHTINGS, HERO).
Update those sections when new standout finds are worth featuring.

Output: dive-highlights-west-cork.html (overwrites in place)
"""

import math
import requests

# ── Configuration ──────────────────────────────────────────────────────────

USER_ID = "andreiastra"
OUTPUT_FILE = "dive-highlights-west-cork.html"
PREPARED_FOR = "Sean Hallahan"

# Keywords mapping place_guess fragments → preferred site name
SITE_KEYWORDS = [
    ("seven heads",    "Seven Heads Pier"),
    ("barloge",        "Barloge Pier"),
    ("blind strand",   "Blind Strand Pier"),
    ("canty",          "Canty's Cove"),
    ("simon",          "Simon's Cove"),
    ("councambeg",     "Simon's Cove"),
    ("gortdubh",       "Gortdubh Pier"),
    ("knockaphuca",    "Gortdubh Pier"),
    ("lough hyne",     "Lough Hyne"),
    ("sandmount",      "Bank Pier"),
    ("bank",           "Bank Pier"),
    ("rosscarbery",    "Rosscarbery"),
    ("dooneen",        "Dooneen Pier"),
    ("derreenacarrin", "Zetland Pier"),
    ("zetland",        "Zetland Pier"),
    ("kilcrohane",     "Kilcrohane Pier"),
    ("aghabeg",        "Aghabeg Pier"),
    ("trafrask",       "Trafrask Pier"),
    ("adrigole",       "Trafrask Pier"),
]

# Dive-only sites (excludes Rosscarbery which is birds, Coolanagh/Derrigra land)
DIVE_SITES = [
    "Lough Hyne", "Gortdubh Pier", "Zetland Pier", "Canty's Cove",
    "Kilcrohane Pier", "Seven Heads Pier", "Aghabeg Pier", "Dooneen Pier",
    "Bank Pier", "Trafrask Pier", "Simon's Cove", "Barloge Pier",
    "Blind Strand Pier",
]

# Sites worth revisiting (low obs count, not in Best Sites table)
REVISIT_SITES = {
    "Trafrask Pier":   ("European Seabass, Pouting",      "Only 2 obs — fish activity suggests a productive site"),
    "Simon's Cove":    ("Strawberry Anemone",              "Only 1 dive logged — rocky crevices likely hold more"),
    "Bank Pier":       ("European Cowrie + Spotted Seahare","Unusual invertebrates suggest rich hidden life"),
    "Blind Strand Pier":("Tompot Blenny",                  "Single visit; pier structure likely holds more fish"),
    "Barloge Pier":    ("Spiny Squat Lobster",             "Remote location, barely explored — high potential"),
}

# Site descriptions shown under the site name in the Best Sites table
SITE_DESCS = {
    "Lough Hyne":       "Co. Cork — Marine Nature Reserve",
    "Gortdubh Pier":    "Knockaphuca, Co. Cork",
    "Zetland Pier":     "Co. Cork",
    "Canty's Cove":     "Co. Cork",
    "Kilcrohane Pier":  "Co. Cork",
    "Seven Heads Pier": "Co. Cork",
    "Aghabeg Pier":     "Knockane, Co. Cork",
    "Dooneen Pier":     "Co. Cork",
}

# Site star ratings (★ = 1, ★★ = 2, ★★★ = 3)
SITE_RATINGS = {
    "Lough Hyne":       3,
    "Gortdubh Pier":    3,
    "Zetland Pier":     3,
    "Canty's Cove":     2,
    "Kilcrohane Pier":  2,
    "Seven Heads Pier": 2,
    "Aghabeg Pier":     2,
    "Dooneen Pier":     2,
}

# Site "why it stands out" descriptions (keep up to date manually)
SITE_WHY = {
    "Lough Hyne":       "Ireland's only saltwater lake. Home of the <strong>Football Jersey Worm</strong> (community faved), Cylinder Anemone, Gem Anemone, Great Scallop, Velvet Swimming Crab, Chamaeleon Prawn, and 6 species of spider crab. The richest single site.",
    "Gortdubh Pier":    "Portuguese Blenny ×2, Tompot Blenny, Atlantic Black Sea Cucumber, Dead Man's Fingers, Sandalled Anemone, Blue-rayed Limpet, Grey Colonial Ascidian (rare genus ID). Excellent fish life under the pier.",
    "Zetland Pier":     "<strong>Small-spotted Catshark ×2</strong>, European Seabass (Near Threatened), Mauve Stinger, Connemarra Clingfish, Toothed Crab, Common Hermit Crab, Sea Potato. Highest surprise value of any site.",
    "Canty's Cove":     "Candy Stripe Flatworm, Sea Lemon, Pink Coryphella, Aeolid Nudibranch, Atlantic Black Sea Cucumber, Snakelocks Anemone. Most consistent nudibranch and flatworm site.",
    "Kilcrohane Pier":  "<strong>Facelina annulicornis ×2</strong>, Orange-clubbed Sea Slug, Spotted Seahare, Tompot Blenny, Aequorea vitrina. Best site for hunting nudibranchs on the Mizen Peninsula.",
    "Seven Heads Pier": "<strong>European Lobster</strong> and <strong>Spiny Squat Lobster</strong> in the same session, Candy Stripe Flatworm, Blood Stars, Topknot, Polycera faeroensis nudibranch. Best for large crustaceans.",
    "Aghabeg Pier":     "<strong>Small-spotted Catshark</strong>, Compass Jelly ×2, Aequorea vitrina, Flag-mouth Jellies, Spiny Starfish. Excellent open-water encounters in a single session.",
    "Dooneen Pier":     "Blood Stars, Orange-clubbed Sea Slug ×2, Common Brittle Star, Ballan Wrasse. Quiet site, underrated.",
}

# Hero observation — the single most impressive find
HERO = {
    "name":    "Football Jersey Worm",
    "sci":     "Tubulanus annulatus",
    "photo":   "https://inaturalist-open-data.s3.amazonaws.com/photos/724746232/medium.jpg",
    "desc":    "A vividly banded ribbon worm — striking orange, white, and dark stripes along its long, flattened body. This observation attracted community comments and was <strong>favourited</strong> by the iNaturalist community, making it the standout find of the season. Ribbon worms of this size and colour are rarely photographed well underwater.",
    "badges":  [
        ("research", "Research Grade"),
        ("faved",    "⭐ Community Favourite"),
        ("",         "2 Comments"),
        ("",         "Lough Hyne · Mar 2026"),
    ],
}

# Standout sightings grid — curated list of (name, sci, photo_url, site_label, badge_list)
# badge_list: list of (css_class, label) — css_class one of: "research", "threatened", ""
STANDOUT_SIGHTINGS = [
    ("Small-spotted Catshark",    "Scyliorhinus canicula",    "https://inaturalist-open-data.s3.amazonaws.com/photos/724751029/medium.jpg",   "Zetland Pier · Sep 2025",    [("research","Research Grade"),("","Shark ×2 at Zetland")]),
    ("Small-spotted Catshark",    "Scyliorhinus canicula",    "https://inaturalist-open-data.s3.amazonaws.com/photos/726544669/medium.jpg",   "Aghabeg Pier · Jul 2025",    [("research","Research Grade"),("","Shark")]),
    ("Orange-clubbed Sea Slug",   "Limacia clavigera",        "https://inaturalist-open-data.s3.amazonaws.com/photos/724749530/medium.jpg",   "Kilcrohane Pier · Jan 2026", [("research","Research Grade"),("","Nudibranch")]),
    ("European Lobster",          "Homarus gammarus",         "https://inaturalist-open-data.s3.amazonaws.com/photos/724693602/medium.jpg",   "Seven Heads · Jul 2026",     [("research","Research Grade")]),
    ("Compass Jelly",             "Chrysaora hysoscella",     "https://inaturalist-open-data.s3.amazonaws.com/photos/726520118/medium.jpg",   "Aghabeg Pier · Jul 2025",    [("research","Research Grade"),("","Jellyfish ×2")]),
    ("Candy Stripe Flatworm",     "Prostheceraeus vittatus",  "https://inaturalist-open-data.s3.amazonaws.com/photos/724735849/medium.jpg",   "Canty's Cove · Mar 2026",    [("research","Research Grade")]),
    ("Portuguese Blenny",         "Parablennius ruber",       "https://inaturalist-open-data.s3.amazonaws.com/photos/725226402/medium.jpg",   "Gortdubh Pier · Aug 2026",   [("research","Research Grade")]),
    ("Tompot Blenny",             "Parablennius gattorugine", "https://inaturalist-open-data.s3.amazonaws.com/photos/725225882/medium.jpg",   "Gortdubh Pier · Aug 2026",   [("research","Research Grade")]),
    ("Atlantic Black Sea Cucumber","Holothuria forskali",     "https://inaturalist-open-data.s3.amazonaws.com/photos/725728812/medium.jpg",   "Gortdubh Pier · Aug 2026",   [("research","Research Grade")]),
    ("Spiny Squat Lobster",       "Galathea strigosa",        "https://inaturalist-open-data.s3.amazonaws.com/photos/724692861/medium.jpg",   "Seven Heads · Aug 2026",     [("research","Research Grade")]),
    ("Tompot Blenny",             "Parablennius gattorugine", "https://inaturalist-open-data.s3.amazonaws.com/photos/724712257/medium.jpg",   "Kilcrohane Pier · May 2026", [("research","Research Grade")]),
    ("Facelina annulicornis",     "Facelina annulicornis",    "https://inaturalist-open-data.s3.amazonaws.com/photos/724709431/medium.jpg",   "Kilcrohane Pier · May 2026", [("research","Research Grade"),("","Nudibranch ×2")]),
    ("Spotted Seahare",           "Aplysia punctata",         "https://inaturalist-open-data.s3.amazonaws.com/photos/724704135/medium.jpg",   "Kilcrohane Pier · Jan 2026", [("","Nudibranch")]),
    ("Polycera faeroensis",       "Polycera faeroensis",      "https://inaturalist-open-data.s3.amazonaws.com/photos/724701007/medium.jpg",   "Seven Heads · Aug 2026",     [("","Nudibranch")]),
    ("Great Scallop",             "Pecten maximus",           "https://inaturalist-open-data.s3.amazonaws.com/photos/724481836/medium.jpg",   "Lough Hyne · Aug 2026",      [("research","Research Grade")]),
    ("Velvet Swimming Crab",      "Necora puber",             "https://inaturalist-open-data.s3.amazonaws.com/photos/726464205/medium.jpg",   "Lough Hyne · Aug 2026",      [("research","Research Grade")]),
    ("Cylinder Anemone",          "Cerianthus membranaceus",  "https://inaturalist-open-data.s3.amazonaws.com/photos/724748563/medium.jpg",   "Lough Hyne · Jan 2026",      [("","Rare find")]),
    ("Mauve Stinger",             "Pelagia noctiluca",        "https://inaturalist-open-data.s3.amazonaws.com/photos/726552889/medium.jpg",   "Zetland Pier · Sep 2025",    [("research","Research Grade"),("","Jellyfish")]),
    ("Sea Lemon",                 "Doris pseudoargus",        "https://inaturalist-open-data.s3.amazonaws.com/photos/724735398/medium.jpg",   "Canty's Cove · Mar 2026",    [("","Nudibranch")]),
    ("European Cowrie",           "Trivia monacha",           "https://inaturalist-open-data.s3.amazonaws.com/photos/724713295/medium.jpg",   "Bank Pier · May 2026",       [("research","Research Grade")]),
    ("Ballan Wrasse",             "Labrus bergylta",          "https://inaturalist-open-data.s3.amazonaws.com/photos/724695640/medium.jpg",   "Dooneen Pier · Jul 2026",    [("research","Research Grade")]),
    ("European Seabass",          "Dicentrarchus labrax",     "https://inaturalist-open-data.s3.amazonaws.com/photos/726537592/medium.jpg",   "Trafrask Pier · Aug 2026",   [("threatened","Near Threatened ⚠️"),("","New site")]),
    ("European Seabass",          "Dicentrarchus labrax",     "https://inaturalist-open-data.s3.amazonaws.com/photos/727116530/medium.jpg",   "Zetland Pier · Aug 2026",    [("threatened","Near Threatened ⚠️"),("","New at Zetland")]),
    ("Common Hermit Crab",        "Pagurus bernhardus",       "https://inaturalist-open-data.s3.amazonaws.com/photos/727118200/medium.jpg",   "Zetland Pier · Aug 2026",    [("","New at Zetland")]),
    ("Strawberry Anemone",        "Actinia fragacea",         "https://inaturalist-open-data.s3.amazonaws.com/photos/724705630/medium.jpg",   "Simon's Cove · Jun 2026",    [("research","Research Grade")]),
]

# ── API helpers ─────────────────────────────────────────────────────────────

def fetch_all_observations(user_id):
    obs = []
    page = 1
    while True:
        r = requests.get(
            "https://api.inaturalist.org/v1/observations",
            params={"user_id": user_id, "per_page": 200, "page": page},
        )
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])
        obs.extend(results)
        print(f"  Fetched page {page} ({len(results)} obs)...")
        if len(obs) >= data.get("total_results", 0):
            break
        page += 1
    return obs

def resolve_site(place_guess):
    pg = (place_guess or "").lower()
    for kw, name in SITE_KEYWORDS:
        if kw in pg:
            return name
    return None  # non-dive location

# ── Stats computation ────────────────────────────────────────────────────────

def compute_stats(obs):
    total = len(obs)
    dive_obs = [o for o in obs if resolve_site(o.get("place_guess","")) in DIVE_SITES]

    sharks = sum(
        1 for o in dive_obs
        if "catshark" in ((o.get("taxon") or {}).get("preferred_common_name") or "").lower()
    )

    # Count nudibranch species by name (known list)
    NUDI_NAMES = {
        "Orange-clubbed Sea Slug", "Facelina annulicornis", "Spotted Seahare",
        "Sea Lemon", "Pink Coryphella", "Aeolid Nudibranchs", "Aeolidiella alderi",
        "Aeolidiella glauca", "Candy Stripe Flatworm",
    }
    nudi_found = set()
    for o in dive_obs:
        name = (o.get("taxon") or {}).get("preferred_common_name") or ""
        if name in NUDI_NAMES:
            nudi_found.add(name)

    faved = sum(1 for o in dive_obs if (o.get("faves_count") or 0) > 0)

    by_site = {}
    for o in dive_obs:
        s = resolve_site(o.get("place_guess",""))
        if s:
            by_site.setdefault(s, []).append(o)

    return {
        "total": total,
        "dive_sites": len(by_site),
        "sharks": sharks,
        "nudibranchs": len(nudi_found),
        "faved": faved,
        "by_site": by_site,
    }

# ── HTML builders ────────────────────────────────────────────────────────────

CSS = """
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, "Segoe UI", system-ui, sans-serif;
    font-size: 14px; line-height: 1.6; color: #1f2328;
    background: #ffffff; padding: 32px 16px 48px;
  }
  .page { max-width: 760px; margin: 0 auto; }
  .header { border-bottom: 2px solid #1f2328; padding-bottom: 20px; margin-bottom: 32px; }
  .header h1 { font-size: 26px; font-weight: 700; letter-spacing: -0.5px; }
  .header .sub { color: #57606a; margin-top: 4px; font-size: 13px; }
  .header .meta { margin-top: 10px; display: flex; gap: 24px; flex-wrap: wrap; }
  .header .meta span { font-size: 12px; color: #57606a; }
  .header .meta strong { color: #1f2328; }
  h2 { font-size: 16px; font-weight: 700; margin: 36px 0 14px; padding-bottom: 6px;
       border-bottom: 1px solid #e5e7eb; text-transform: uppercase; letter-spacing: 0.5px; }
  .hero-card { background: #f7f8fa; border: 1px solid #e5e7eb; border-left: 4px solid #3b82d4;
               border-radius: 6px; padding: 20px; display: flex; gap: 20px; align-items: flex-start; }
  .hero-card img { width: 160px; height: 120px; object-fit: cover; border-radius: 4px;
                   flex-shrink: 0; border: 1px solid #e5e7eb; }
  .hero-card .hero-body h3 { font-size: 18px; font-weight: 700; }
  .hero-card .hero-body .sci { font-style: italic; color: #57606a; font-size: 13px; }
  .hero-card .hero-body .desc { margin-top: 8px; font-size: 13px; color: #1f2328; }
  .hero-card .hero-body .badges { margin-top: 10px; display: flex; gap: 8px; flex-wrap: wrap; }
  .badge { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 10px;
           background: #e5e7eb; color: #1f2328; }
  .badge.research  { background: #dcfce7; color: #166534; }
  .badge.faved     { background: #fef9c3; color: #713f12; }
  .badge.threatened{ background: #fee2e2; color: #991b1b; }
  .sightings-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
                    gap: 14px; margin-top: 4px; }
  .sight-card { border: 1px solid #e5e7eb; border-radius: 6px; overflow: hidden; background: #fff; }
  .sight-card img { width: 100%; height: 140px; object-fit: cover; display: block; background: #f7f8fa; }
  .sight-card .sight-body { padding: 10px 12px 12px; }
  .sight-card .sight-body h4 { font-size: 13px; font-weight: 700; margin-bottom: 2px; }
  .sight-card .sight-body .sci { font-style: italic; color: #57606a; font-size: 11px; }
  .sight-card .sight-body .where { margin-top: 6px; font-size: 11px; color: #57606a; }
  .sight-card .sight-body .sight-badges { margin-top: 6px; display: flex; gap: 6px; flex-wrap: wrap; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  thead th { background: #f7f8fa; font-weight: 700; font-size: 11px; text-transform: uppercase;
             letter-spacing: 0.4px; color: #57606a; padding: 8px 10px;
             border-bottom: 2px solid #e5e7eb; text-align: left; }
  tbody tr { border-bottom: 1px solid #e5e7eb; }
  tbody tr:last-child { border-bottom: none; }
  tbody td { padding: 9px 10px; vertical-align: top; }
  .stars { color: #3b82d4; font-size: 13px; }
  .obs-count { font-weight: 700; font-size: 15px; }
  .site-name { font-weight: 600; }
  .site-desc { color: #57606a; font-size: 12px; margin-top: 2px; }
  .stats { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 28px; }
  .stat { background: #f7f8fa; border: 1px solid #e5e7eb; border-radius: 6px;
          padding: 14px 20px; flex: 1 1 120px; }
  .stat .num { font-size: 28px; font-weight: 700; color: #3b82d4; line-height: 1; }
  .stat .label { font-size: 12px; color: #57606a; margin-top: 4px; }
  footer { margin-top: 48px; padding-top: 12px; border-top: 1px solid #e5e7eb;
           text-align: center; font-size: 12px; color: #57606a; }
"""

def badges_html(badges, container_class="badges"):
    parts = [f'<div class="{container_class}">']
    for cls, label in badges:
        cls_str = f' {cls}' if cls else ''
        parts.append(f'<span class="badge{cls_str}">{label}</span>')
    parts.append('</div>')
    return "\n        ".join(parts)

def build_html(stats):
    by_site = stats["by_site"]

    # ── Header ──
    header = f"""  <div class="header">
    <h1>🤿 West Cork Dive Highlights</h1>
    <p class="sub">Prepared for <strong>{PREPARED_FOR}</strong> — diving buddy recap</p>
    <div class="meta">
      <span><strong>Observer:</strong> {USER_ID} (iNaturalist)</span>
      <span><strong>Region:</strong> West Cork, Ireland</span>
      <span><strong>Dive Sites:</strong> {stats['dive_sites']} locations</span>
    </div>
  </div>"""

    # ── Stats bar ──
    stat_bar = f"""  <div class="stats">
    <div class="stat"><div class="num">{stats['total']}</div><div class="label">Total observations</div></div>
    <div class="stat"><div class="num">{stats['dive_sites']}</div><div class="label">Dive sites visited</div></div>
    <div class="stat"><div class="num">{stats['sharks']}</div><div class="label">Shark encounters</div></div>
    <div class="stat"><div class="num">{stats['nudibranchs']}</div><div class="label">Nudibranch species</div></div>
    <div class="stat"><div class="num">{stats['faved']}</div><div class="label">Community-faved find</div></div>
  </div>"""

    # ── Hero ──
    hero_badges = badges_html(HERO["badges"], "badges")
    hero = f"""  <h2>⭐ Most Impressive Sighting</h2>
  <div class="hero-card">
    <img src="{HERO['photo']}" alt="{HERO['name']}" loading="lazy" />
    <div class="hero-body">
      <h3>{HERO['name']}</h3>
      <div class="sci">{HERO['sci']}</div>
      <div class="desc">{HERO['desc']}</div>
      {hero_badges}
    </div>
  </div>"""

    # ── Sightings grid ──
    cards = []
    for name, sci, photo, where, bdgs in STANDOUT_SIGHTINGS:
        sight_badges = badges_html(bdgs, "sight-badges")
        cards.append(f"""    <div class="sight-card">
      <img src="{photo}" alt="{name}" loading="lazy" />
      <div class="sight-body">
        <h4>{name}</h4>
        <div class="sci">{sci}</div>
        <div class="where">📍 {where}</div>
        {sight_badges}
      </div>
    </div>""")
    sightings = "  <h2>Standout Sightings</h2>\n  <div class=\"sightings-grid\">\n\n" + \
                "\n\n".join(cards) + "\n\n  </div>"

    # ── Best Sites table ──
    rows = []
    ranked = [s for s in DIVE_SITES if s in SITE_WHY]
    for i, site in enumerate(ranked, 1):
        obs_count = len(by_site.get(site, []))
        stars = "★" * SITE_RATINGS.get(site, 1)
        desc = SITE_DESCS.get(site, "Co. Cork")
        why = SITE_WHY.get(site, "")
        rows.append(f"""      <tr>
        <td>{i}</td>
        <td>
          <div class="site-name">{site}</div>
          <div class="site-desc">{desc}</div>
        </td>
        <td><span class="stars">{stars}</span></td>
        <td><span class="obs-count">{obs_count}</span></td>
        <td>{why}</td>
      </tr>""")
    best_sites = """  <h2>Best Dive Sites</h2>
  <table>
    <thead>
      <tr>
        <th>#</th><th>Site</th><th>Rating</th><th>Obs</th><th>Why it stands out</th>
      </tr>
    </thead>
    <tbody>\n""" + "\n".join(rows) + "\n    </tbody>\n  </table>"

    # ── Worth Revisiting table ──
    revisit_rows = []
    for site, (find, reason) in REVISIT_SITES.items():
        revisit_rows.append(f"""      <tr>
        <td><strong>{site}</strong></td>
        <td>{find}</td>
        <td>{reason}</td>
      </tr>""")
    revisit = """  <h2>Worth Revisiting</h2>
  <table>
    <thead>
      <tr>
        <th>Site</th><th>Standout find so far</th><th>Why revisit</th>
      </tr>
    </thead>
    <tbody>\n""" + "\n".join(revisit_rows) + "\n    </tbody>\n  </table>"

    footer = f'  <footer>\n    <p>All observations recorded on <a href="https://www.inaturalist.org/people/{USER_ID}">iNaturalist · {USER_ID}</a>  |  Made with IBM Bob</p>\n  </footer>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Dive Highlights — West Cork</title>
<style>
{CSS}
</style>
</head>
<body>
<div class="page">

{header}

{stat_bar}

{hero}

{sightings}

{best_sites}

{revisit}

{footer}

</div>
</body>
</html>
"""

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print(f"Fetching observations for '{USER_ID}'...")
    obs = fetch_all_observations(USER_ID)
    print(f"Total: {len(obs)}\n")

    stats = compute_stats(obs)
    print(f"Dive sites: {stats['dive_sites']}")
    print(f"Sharks: {stats['sharks']}, Nudibranchs: {stats['nudibranchs']}, Faved: {stats['faved']}")
    print(f"Site obs counts: { {s: len(v) for s, v in stats['by_site'].items()} }\n")

    html = build_html(stats)
    with open(OUTPUT_FILE, "w") as f:
        f.write(html)
    print(f"Written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
