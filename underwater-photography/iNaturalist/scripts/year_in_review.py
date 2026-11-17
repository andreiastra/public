"""
Write reports/year_in_review.html: a static one-page summary of andreiastra's
underwater observations in Ireland (open it in a browser, no scripts needed).

Highlights: species and observation totals, best dive, rarest find, most
photographed site, top identifier, when you dive, and how the life list grew.

Same observations as the other underwater reports (underwater_ireland.py).
"Rarest find" uses the Ireland-wide counts from rarity_underwater_ireland.py
(distinct observers with a verifiable record, Research Grade species only) and its
scripts/.cache/taxon_counts.json cache. Top identifier counts current identifications
other people made on these observations.

Usage:
  .venv/bin/python scripts/year_in_review.py [--refresh]
"""
import html
import os
import re
import sys
from collections import Counter
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from config import IRELAND_PLACE_ID, OUTPUT_DIR, USER_ID
from rarity_underwater_ireland import (
    cached_counts,
    load_counts_cache,
    rating,
    save_counts_cache,
)
from underwater_stats import (
    OBSCURED_LABEL,
    dives,
    pct,
    site_label,
    species_table,
    underwater_entries,
    weekday,
)

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "year_in_review.html")


def esc(text):
    return html.escape(str(text), quote=True)


def common_name(taxon):
    return taxon.get("preferred_common_name") or taxon.get("name") or "Unidentified"


def photo_url(obs, size="medium"):
    photos = obs.get("photos") or []
    if not photos:
        return None
    return re.sub(r"/square\.(jpe?g|png|gif)$", rf"/{size}.\1", photos[0].get("url") or "", flags=re.I)


def top_identifiers(entries, limit=5):
    """Count current identifications by other users on the user's observations."""
    counts = Counter()
    for _, obs in entries:
        for ident in obs.get("identifications") or []:
            login = (ident.get("user") or {}).get("login")
            if ident.get("current") and login and login != USER_ID:
                counts[login] += 1
    return counts.most_common(limit)


def rarest_find(table):
    """Return (info, observers) for the rarest Research Grade species, or None."""
    research = {tid: i for tid, i in table.items()
                if any(o.get("quality_grade") == "research" for _, o in i["entries"])}
    if not research:
        return None
    cache = load_counts_cache()
    try:
        for info in research.values():
            (info["observers"], info["total"]), _ = cached_counts(
                cache, info["taxon"]["id"], IRELAND_PLACE_ID, "--refresh" in sys.argv)
    finally:
        save_counts_cache(cache)
    return min(research.values(), key=lambda i: (i["observers"], i["total"]))


def growth(table):
    """Return [(month, new species, running total)] for the first record of each species."""
    first = Counter((i["entries"][0][1].get("observed_on") or "")[:7] for i in table.values())
    running, rows = 0, []
    for month in sorted(m for m in first if m):
        running += first[month]
        rows.append((month, first[month], running))
    return rows


def stat(value, caption):
    return f'<div class="stat"><div class="n">{esc(value)}</div><div class="c">{esc(caption)}</div></div>'


def card(title, image, body):
    img = f'<img src="{esc(image)}" alt="">' if image else ""
    return f'<div class="card">{img}<div><h3>{esc(title)}</h3>{body}</div></div>'


def bars(rows, max_value):
    """Horizontal bars as plain HTML/CSS. rows: [(label, value, text)]."""
    out = []
    for label, value, text in rows:
        width = 100 * value / max_value if max_value else 0
        out.append(f'<div class="bar"><span class="l">{esc(label)}</span>'
                   f'<span class="t"><span class="f" style="width:{width:.0f}%"></span></span>'
                   f'<span class="v">{esc(text)}</span></div>')
    return "\n".join(out)


def render(entries, table, notes):
    all_dives = dives(entries)
    by_site = Counter(site_label(s) for s, _ in entries)
    dates = sorted({d for d, _ in all_dives})
    species_by_site = Counter()
    for info in table.values():
        for site in {site_label(s) for s, _ in info["entries"]}:
            species_by_site[site] += 1

    best_key = max(all_dives, key=lambda k: len({(o.get("taxon") or {}).get("id") for o in all_dives[k]}))
    best_obs = all_dives[best_key]
    best_species = len({(o.get("taxon") or {}).get("id") for o in best_obs if o.get("taxon")})
    best_photo = next((photo_url(o) for o in best_obs if photo_url(o)), None)

    top_site, top_site_n = by_site.most_common(1)[0]
    once = sum(1 for i in table.values() if len(i["entries"]) == 1)
    weekdays = Counter(weekday(d) for d in dates)
    saturday = weekdays["Saturday"]
    hours = Counter((o.get("observed_on_details") or {}).get("hour") for _, o in entries)
    morning = sum(n for h, n in hours.items() if h is not None and 6 <= h < 12)
    research = sum(1 for _, o in entries if o.get("quality_grade") == "research")
    rare = rarest_find(table)
    identifiers = top_identifiers(entries)
    rows = growth(table)

    cards = [card(
        f"Best dive: {best_key[0]}", best_photo,
        f"<p><b>{best_species}</b> species at <b>{esc(site_label(best_key[1]))}</b> "
        f"on a {esc(weekday(best_key[0]))}, from {len(best_obs)} observations.</p>")]
    if rare:
        sites = sorted({site_label(s) for s, _ in rare["entries"]})
        obs = rare["entries"][0][1]
        cards.append(card(
            f"Rarest find: {common_name(rare['taxon'])}", photo_url(obs),
            f"<p><i>{esc(rare['taxon'].get('name') or '')}</i>. Only <b>{rare['observers']:,}</b> "
            f"observer{'' if rare['observers'] == 1 else 's'} in Ireland "
            f"{'has' if rare['observers'] == 1 else 'have'} a verifiable record "
            f"({esc(rating(rare['observers']).lower())}). Found at {esc(', '.join(sites))}.</p>"))

    site_rows = [(s, n, f"{n} obs · {species_by_site[s]} species") for s, n in by_site.most_common(8)]
    ident_rows = [(u, n, str(n)) for u, n in identifiers]
    growth_rows = [(m, total, f"+{new} → {total}") for m, new, total in rows]

    notes_html = "".join(f"<p class='warn'>⚠️ {esc(n)}</p>" for n in notes)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Underwater Ireland: year in review</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {{ font: 15px/1.6 -apple-system, "Segoe UI", system-ui, sans-serif; color: #1f2328; margin: 0; background: #fff; }}
main {{ max-width: 760px; margin: 0 auto; padding: 32px 20px 24px; }}
h1 {{ font-size: 26px; margin: 0 0 4px; }}
h2 {{ font-size: 17px; margin: 32px 0 12px; padding-bottom: 6px; border-bottom: 1px solid #e5e7eb; }}
h3 {{ font-size: 15px; margin: 0 0 4px; }}
p {{ margin: 0 0 8px; }}
.sub {{ color: #57606a; margin-bottom: 20px; }}
.stats {{ display: flex; flex-wrap: wrap; gap: 10px; }}
.stat {{ flex: 1 1 140px; background: #f7f8fa; border: 1px solid #e5e7eb; border-radius: 6px; padding: 12px; }}
.stat .n {{ font-size: 24px; font-weight: 600; color: #3b82d4; }}
.stat .c {{ color: #57606a; font-size: 13px; }}
.card {{ display: flex; gap: 14px; background: #f7f8fa; border: 1px solid #e5e7eb; border-radius: 6px; padding: 12px; margin-bottom: 10px; }}
.card img {{ width: 150px; height: 112px; object-fit: cover; border-radius: 4px; flex: none; }}
.bar {{ display: flex; align-items: center; gap: 10px; margin: 4px 0; font-size: 13px; }}
.bar .l {{ width: 170px; flex: none; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.bar .t {{ flex: 1; background: #f7f8fa; border: 1px solid #e5e7eb; height: 12px; border-radius: 3px; }}
.bar .f {{ display: block; height: 100%; background: #3b82d4; border-radius: 2px; }}
.bar .v {{ width: 140px; flex: none; color: #57606a; text-align: right; }}
.warn {{ color: #8a4b00; }}
footer {{ margin: 36px 0 0; padding-top: 10px; border-top: 1px solid #e5e7eb; text-align: center; color: #57606a; font-size: 12px; }}
</style>
</head>
<body>
<main>
<h1>Underwater Ireland: year in review</h1>
<p class="sub">{esc(USER_ID)} · {esc(dates[0])} to {esc(dates[-1])} · generated {date.today()}</p>
{notes_html}
<div class="stats">
{stat(len(table), "species")}
{stat(len(entries), "observations")}
{stat(len(dates), "dive days")}
{stat(sum(1 for s in species_by_site if s != OBSCURED_LABEL), "sites")}
{stat(pct(research, len(entries)), "Research Grade")}
{stat(pct(once, len(table)), "species seen once")}
</div>

<h2>Highlights</h2>
{"".join(cards)}
<div class="card"><div><h3>Most photographed site: {esc(top_site)}</h3>
<p>{top_site_n} observations of {species_by_site[top_site]} species.</p></div></div>

<h2>When you dive</h2>
<p><b>{pct(saturday, len(dates))}</b> of your dive days were Saturdays ({saturday} of {len(dates)}), and
<b>{pct(morning, len(entries))}</b> of observations were made before noon.</p>

<h2>Sites</h2>
{bars(site_rows, site_rows[0][1] if site_rows else 0)}

<h2>Life list growth</h2>
<p>New species recorded each month, with the running total.</p>
{bars(growth_rows, rows[-1][2] if rows else 0)}

<h2>Who identifies your observations</h2>
{bars(ident_rows, ident_rows[0][1] if ident_rows else 0)}

<footer>Made with IBM Bob</footer>
</main>
</body>
</html>
"""


def main():
    notes = []
    entries = underwater_entries(notes)
    table = species_table(entries)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(render(entries, table, notes))
    print(f"Saved {len(table)} species, {len(entries)} observations → {os.path.normpath(OUTPUT_FILE)}")
    for note in notes:
        print(f"WARNING: {note}")


if __name__ == "__main__":
    main()
