"""
Run every GBIF script that writes a report, with a single download of the
occurrences.

fetch_occurrences.refresh() runs first and keeps the occurrences in memory; the
report scripts read them through cached() instead of calling GBIF again. A failing
script doesn't stop the run: failures are listed at the end and the exit code is 1.

Usage:
  ../.venv/bin/python scripts/run_all.py
"""
import importlib
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(__file__))
import fetch_occurrences

REPORT_SCRIPTS = ["gbif_summary", "sync_status", "underwater_ireland", "citations"]


def main():
    fetch_occurrences.refresh()
    failed = []
    for name in REPORT_SCRIPTS:
        print(f"\n=== {name}")
        try:
            importlib.import_module(name).main()
        except Exception:
            traceback.print_exc()
            failed.append(name)
    if failed:
        print(f"\nFAILED: {', '.join(failed)}")
        sys.exit(1)
    print("\nAll reports written.")


if __name__ == "__main__":
    main()
