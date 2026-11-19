"""
Write reports/citations.md: research that GBIF links to the iNaturalist dataset,
and the papers that mention species andreiastra has recorded.

GBIF tracks citations per dataset and per taxon. It also indexes the occurrence
keys that a paper cites explicitly, but that is rare for iNaturalist records and
the search filter for it is broken (see direct_citations). The report checks it
and otherwise cannot say that one of your records was used. It shows:
  - the dataset as a whole: linked papers, by year, topics, downloads;
  - the papers linked to the dataset that also mention a species you recorded.
    A paper that studies a species you recorded may have used other people's
    records of it, so this is an upper bound on relevance, not proof of use.

Usage:
  ../.venv/bin/python scripts/citations.py
"""
import os
import sys
import time
from collections import Counter

import requests

sys.path.insert(0, os.path.dirname(__file__))
from config import (
    DATASET_URL,
    DOWNLOAD_DATASET_URL,
    INATURALIST_DATASET_KEY,
    LITERATURE_PAGE_SIZE,
    LITERATURE_SEARCH_URL,
    OCCURRENCE_FACET_LIMIT,
    OUTPUT_DIR,
    RECORDED_BY,
    TAXON_BATCH,
    THROTTLE_S,
)
from fetch_occurrences import cached, refresh

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "citations.md")
DATASET_PAGE = f"https://www.gbif.org/dataset/{INATURALIST_DATASET_KEY}"
TOP_PAPERS = 15
TOP_SPECIES = 15


def get(url, **params):
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    time.sleep(THROTTLE_S)
    return r.json()


def dataset_overview():
    """Totals and facets for every paper linked to the dataset."""
    print("Fetching dataset-level citations from GBIF…")
    lit = get(LITERATURE_SEARCH_URL, gbifDatasetKey=INATURALIST_DATASET_KEY, limit=0,
              facet=["year", "topics", "countriesOfResearcher", "peerReview", "openAccess"], facetLimit=50)
    facets = {f["field"]: {c["name"]: c["count"] for c in f["counts"]} for f in lit["facets"]}
    downloads = get(f"{DOWNLOAD_DATASET_URL}/{INATURALIST_DATASET_KEY}", limit=0)["count"]
    ireland = get(LITERATURE_SEARCH_URL, gbifDatasetKey=INATURALIST_DATASET_KEY,
                  countriesOfCoverage="IE", limit=0)["count"]
    dataset = get(f"{DATASET_URL}/{INATURALIST_DATASET_KEY}")
    return {"papers": lit["count"], "facets": facets, "downloads": downloads, "ireland": ireland,
            "doi": dataset.get("doi"), "citation": (dataset.get("citation") or {}).get("text")}


def direct_citations(occurrences):
    """Your occurrence keys that papers cite by key, as {key: papers}, and how many keys papers cite in all.

    /literature/search?gbifOccurrenceKey=... fails on the API ("Unknown SearchParameter data type
    java.lang.Long"), so the facet is used instead: it lists every occurrence key cited anywhere in
    the literature index, with the number of papers citing it.
    """
    print("Checking which occurrence keys papers cite directly…")
    data = get(LITERATURE_SEARCH_URL, limit=0, facet="gbifOccurrenceKey", facetLimit=OCCURRENCE_FACET_LIMIT)
    counts = data["facets"][0]["counts"] if data["facets"] else []
    if len(counts) >= OCCURRENCE_FACET_LIMIT:
        raise RuntimeError("gbifOccurrenceKey facet was truncated; raise OCCURRENCE_FACET_LIMIT")
    cited = {c["name"]: c["count"] for c in counts}
    mine = {str(o["key"]) for o in occurrences}
    return {k: cited[k] for k in sorted(mine & cited.keys())}, len(cited)


def species_names(occurrences):
    """GBIF taxon key -> species name, for every species and taxon key on your records."""
    names = {}
    for o in occurrences:
        name = o.get("species") or o.get("scientificName")
        for field in ("speciesKey", "taxonKey"):
            if o.get(field) and name:
                names[o[field]] = name
    return names


def papers_on_my_species(keys):
    """Papers linked to the dataset that mention any of the taxon keys, deduplicated by id."""
    print(f"Fetching papers that mention your {len(keys)} taxon keys…")
    keys, papers = sorted(keys), {}
    for i in range(0, len(keys), TAXON_BATCH):
        offset = 0
        while True:
            data = get(LITERATURE_SEARCH_URL, gbifDatasetKey=INATURALIST_DATASET_KEY,
                       gbifTaxonKey=keys[i:i + TAXON_BATCH], limit=LITERATURE_PAGE_SIZE, offset=offset)
            for p in data["results"]:
                papers[p["id"]] = p
            if data.get("endOfRecords", True):
                break
            offset += LITERATURE_PAGE_SIZE
    return list(papers.values())


def link(paper):
    doi = (paper.get("identifiers") or {}).get("doi")
    url = f"https://doi.org/{doi}" if doi else (paper.get("websites") or [None])[0]
    title = " ".join((paper.get("title") or "Untitled").split()).replace("|", "/")
    return f"[{title}]({url})" if url else title


def table(title, counter, header, limit=None):
    lines = [f"\n### {title}\n", f"| {header} | Papers |", "|---|--:|"]
    for k, v in sorted(counter.items(), key=lambda kv: (-kv[1], str(kv[0])))[:limit]:
        lines.append(f"| {k} | {v} |")
    return lines


def render(overview, papers, names, my_species, occurrences, direct, all_cited):
    mine = set(names)
    matched = {}  # paper id -> species names of yours that it mentions
    for p in papers:
        found = {names[k] for k in set(p.get("gbifTaxonKey") or []) & mine}
        if found:
            matched[p["id"]] = found
    by_id = {p["id"]: p for p in papers}
    species_papers = Counter(s for found in matched.values() for s in found)

    f = overview["facets"]
    lines = [
        "# GBIF citations: research linked to the iNaturalist dataset\n",
        f"> Generated by `scripts/citations.py` from live GBIF data. GBIF counts citations per dataset and per taxon, "
        f"and only rarely per occurrence, so this report can seldom show that a record by `{RECORDED_BY}` was used.\n",
        f"The [iNaturalist Research-grade Observations]({DATASET_PAGE}) dataset (DOI `{overview['doi']}`) is linked to "
        f"**{overview['papers']:,}** papers and **{overview['downloads']:,}** downloads. These figures cover every "
        f"iNaturalist contributor, not only you.\n",
        f"**{len(matched)}** of those papers mention at least one of the **{my_species}** species you have recorded on GBIF. "
        f"**{overview['ireland']}** cover Ireland.\n",
        "## Direct citations of your records\n",
        f"GBIF's literature index also stores the occurrence keys that a paper cites explicitly (as a gbif.org/occurrence "
        f"URL or ID). Across the whole index, papers cite **{all_cited:,}** distinct occurrence keys. "
        + (f"**{len(direct)}** of your {len(occurrences)} records {'is' if len(direct) == 1 else 'are'} among them:\n" if direct else
           f"**None** of your {len(occurrences)} records is among them.\n"),
    ]
    if direct:
        lines += ["| GBIF occurrence | Papers citing it |", "|---|--:|"]
        lines += [f"| [{k}](https://www.gbif.org/occurrence/{k}) | {n} |" for k, n in direct.items()]
        lines.append("")
    lines += [
        "This is rare for iNaturalist records. Museum specimens are routinely cited by occurrence ID, but iNaturalist "
        "observations are mostly used through bulk downloads, which link to the dataset or the download DOI, or are cited "
        "by their inaturalist.org URL, which GBIF does not read as an occurrence key. The search filter "
        "`/literature/search?gbifOccurrenceKey=` fails on the API, so this check reads the facet over all cited keys instead.\n",
        "## How to read the rest of this report\n",
        "- **Why the dataset, not your records:** your records on GBIF are not a dataset of their own. iNaturalist publishes "
        "all research-grade observations from every contributor as one dataset, and GBIF attaches most citations to a "
        "dataset and to the taxa a paper mentions. The dataset-wide figures below therefore count everyone's records.",
        "- **How your species are matched:** the GBIF taxon keys on your records are compared with the taxa GBIF found in "
        "each linked paper. A match means the paper mentions a species you recorded.",
        "- **What it cannot show:** whether your own records were used, unless they appear above. A paper on a species you "
        "recorded may have used only other people's records of it. The paper's methods or its GBIF download DOI are the "
        "only way to confirm.",
        "- **Stronger signals:** a paper on one of your species that also covers a country or period you recorded in is "
        "more likely to have used your records.\n",
        "## Dataset-wide\n",
        f"Peer reviewed: **{f.get('PEER_REVIEW', {}).get('1', 0):,}** · Open access: **{f.get('OPEN_ACCESS', {}).get('1', 0):,}**",
    ]
    lines += table("Papers by year published", f.get("YEAR", {}), "Year")
    lines += table("Papers by topic", f.get("TOPICS", {}), "Topic", 10)
    lines += table("Papers by researcher country", f.get("COUNTRIES_OF_RESEARCHER", {}), "Country", 10)

    lines += ["\n## Papers that mention species you recorded\n"]
    if matched:
        lines += ["A paper that studies a species you recorded may have used other people's records of it. "
                  "Papers are ranked by how many of your species they mention.\n",
                  "| Paper | Year | Your species mentioned |", "|---|---|--:|"]
        ranked = sorted(matched, key=lambda i: (-len(matched[i]), -(by_id[i].get("year") or 0), by_id[i].get("title") or ""))
        for i in ranked[:TOP_PAPERS]:
            lines.append(f"| {link(by_id[i])} | {by_id[i].get('year') or '—'} | {len(matched[i])} |")
        lines += [f"\nShowing {min(TOP_PAPERS, len(ranked))} of {len(ranked)}."]
        lines += table("Your species most often mentioned", species_papers, "Species", TOP_SPECIES)
    else:
        lines.append("None.")

    lines += ["\n## How to cite", "", overview["citation"] or f"See the [dataset page]({DATASET_PAGE}).", ""]
    return "\n".join(lines), len(matched)


def main():
    occurrences = cached()
    if occurrences is None:
        occurrences = refresh()
    names = species_names(occurrences)
    overview = dataset_overview()
    papers = papers_on_my_species(set(names))
    my_species = len({o["speciesKey"] for o in occurrences if o.get("speciesKey")})
    direct, all_cited = direct_citations(occurrences)
    text, matched = render(overview, papers, names, my_species, occurrences, direct, all_cited)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved citations ({overview['papers']} dataset papers, {matched} mention your species) → {os.path.normpath(OUTPUT_FILE)}")


if __name__ == "__main__":
    main()
