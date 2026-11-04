#!/usr/bin/env python3
"""Download the eOceanic Cork index page and every location page it links to.

Usage:
    python3 fetch_eoceanic.py

Output, in ../raw/ (relative to this script):
    index.html                  the Cork index page
    pages/<id>_<slug>.html      one raw HTML file per location, in index order
    links.txt                   the relative link of each location, one per line

Pages that already exist and are non-empty are skipped, so the script can be
re-run to resume an interrupted download. Delete a file to fetch it again.
"""

import re
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import unquote

BASE = "https://eoceanic.com/sailing/harbours/europe/ireland/cork/"
RAW = Path(__file__).resolve().parent.parent / "raw"
PAGES = RAW / "pages"
DELAY_SECONDS = 1.0
HEADERS = {"User-Agent": "Mozilla/5.0"}


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def main() -> int:
    PAGES.mkdir(parents=True, exist_ok=True)

    index_html = get(BASE)
    (RAW / "index.html").write_bytes(index_html)

    # Location links are relative, e.g. href='31/youghal'. Keep first occurrence.
    links = []
    for m in re.finditer(r"href='(\d+/[^']+)'", index_html.decode("utf-8", "ignore")):
        if m.group(1) not in links:
            links.append(m.group(1))
    (RAW / "links.txt").write_text("\n".join(links) + "\n")
    print(f"{len(links)} locations found on the index page")

    failed = []
    for n, link in enumerate(links, 1):
        loc_id, slug = link.split("/", 1)
        out = PAGES / f"{loc_id}_{unquote(slug)}.html"
        if out.exists() and out.stat().st_size > 0:
            continue
        try:
            out.write_bytes(get(BASE + link))
            print(f"[{n}/{len(links)}] {out.name}")
        except Exception as e:  # keep going; report at the end
            print(f"[{n}/{len(links)}] FAILED {link}: {e}", file=sys.stderr)
            failed.append(link)
        time.sleep(DELAY_SECONDS)

    if failed:
        print(f"{len(failed)} failed; re-run to retry: {failed}", file=sys.stderr)
        return 1
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
