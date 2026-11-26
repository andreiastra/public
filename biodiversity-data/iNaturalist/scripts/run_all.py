"""
Run every script in order, downloading the observations only once.

fetch_observations.refresh() downloads all observations, rewrites
scripts/.cache/observations.json and caches them in memory.  The scripts then read that
cache instead of calling the API again, and the Ireland, nudibranch and bird
scripts filter it locally.  The only API calls left are the per-taxon rarity
counts (cached for 90 days) and the per-site species lists of the gap analysis
(cached for 30 days), which no download can replace.

A failing script doesn't stop the run: the others still run and the failures are
listed at the end (exit code 1).

A step can also return a warning string (for example crabs_not_in_project.py when
crabs are missing from the project).  Warnings are repeated in the summary at the
end; they don't change the exit code.

Usage:
  ../.venv/bin/python scripts/run_all.py
"""
import importlib
import os
import sys
import time
import traceback

sys.path.insert(0, os.path.dirname(__file__))
import fetch_observations


def run_site_observations():
    """site_observations.py --all"""
    import site_observations
    argv, sys.argv = sys.argv, ["site_observations.py", "--all"]
    try:
        site_observations.main()
    finally:
        sys.argv = argv


# (label, callable)
STEPS = [
    ("fetch_observations.py", fetch_observations.refresh),
    ("generate_location_ratings.py", lambda: importlib.import_module("generate_location_ratings").main()),
    ("nudibranch_ireland.py", lambda: importlib.import_module("nudibranch_ireland").main()),
    ("crabs_not_in_project.py", lambda: importlib.import_module("crabs_not_in_project").main()),
    ("species_classification.py", lambda: importlib.import_module("species_classification").main()),
    ("underwater_ireland.py", lambda: importlib.import_module("underwater_ireland").main()),
    ("not_research_grade_ireland.py", lambda: importlib.import_module("not_research_grade_ireland").main()),
    ("rarity_underwater_ireland.py", lambda: importlib.import_module("rarity_underwater_ireland").main()),
    ("rarity_underwater_worldwide.py", lambda: importlib.import_module("rarity_underwater_worldwide").main()),
    ("rare_birds_ireland.py", lambda: importlib.import_module("rare_birds_ireland").main()),
    ("one_and_done_ireland.py", lambda: importlib.import_module("one_and_done_ireland").main()),
    ("rarity_by_site_ireland.py", lambda: importlib.import_module("rarity_by_site_ireland").main()),
    ("gap_analysis_ireland.py", lambda: importlib.import_module("gap_analysis_ireland").main()),
    ("cork_species.py", lambda: importlib.import_module("cork_species").main()),
    ("year_in_review.py", lambda: importlib.import_module("year_in_review").main()),
    # Last: writes reports/sites/
    ("site_observations.py --all", run_site_observations),
]


def main():
    results = []
    warnings = []
    for label, step in STEPS:
        print(f"\n{'=' * 78}\n▶ {label}\n{'=' * 78}", flush=True)
        start = time.time()
        try:
            warning = step()
            error = None
            if isinstance(warning, str):
                warnings.append((label, warning))
        except Exception:  # keep going, report at the end
            error = traceback.format_exc()
            print(error)
        results.append((label, time.time() - start, error))

    print(f"\n{'=' * 78}\nSummary\n{'=' * 78}")
    for label, secs, error in results:
        print(f"  {'FAILED' if error else 'ok':6s} {secs:6.1f}s  {label}")
    for label, warning in warnings:
        print(f"\n⚠️  {label}: {warning}")
    failed = [label for label, _, error in results if error]
    if failed:
        print(f"\n{len(failed)} script(s) failed: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
