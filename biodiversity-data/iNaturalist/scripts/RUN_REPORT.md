# How to create a run report

A run report is the dated write-up in [`../reports/runs/`](../reports/runs), for example [`2026-11-13.md`](../reports/runs/2026-11-13.md). It records how a full run went and what changed in the reports since the last one. It is written by hand from the numbers below. Nothing generates it.

## 1. Keep the baseline

The report compares the new reports with the **last committed** ones, so don't commit before you have the numbers. Check what the baseline is:

```bash
git status --short reports      # should be clean, or only contain the last run's files
git log -1 --format='%h %cs %s' -- reports/Location_ratings.md
```

If the reports have uncommitted changes from an earlier run, commit or discard them first. Otherwise the comparison mixes two runs.

## 2. Run everything

From `iNaturalist/`:

```bash
.venv/bin/python scripts/run_all.py > /tmp/run_all.log 2>&1; echo "exit=$?"
```

The rarity reports make 2 API calls per species and take about 3 minutes each, so expect about 6 minutes in total. `gap_analysis_ireland.py` adds a few minutes on its first run (at least 2 calls per dive site, then cached for 30 days). `rarity_by_site_ireland.py` reuses the counts the two rarity reports just fetched, so it adds almost nothing.

From the log, record:
- the exit code and whether every step is `ok` (the table at the end of the log),
- the number of observations (`Total: N observations`),
- the time per step, and the total.

```bash
sed -n '/^Summary/,$p' /tmp/run_all.log
grep "Total:" /tmp/run_all.log
```

## 3. Get the before and after numbers

Every report prints its totals in a header line. Compare the committed version with the new one:

```bash
for f in Location_ratings nudibranch_ireland species_classification rarity_underwater_ireland rarity_underwater_worldwide; do
  echo "--- $f"
  git diff -U0 -- reports/$f.md | grep -E '^[-+]' | grep -E 'total observations|observations ·|taxa ·|\*\*[0-9]+\*\* observations' | cut -c1-160
done
```

`-` lines are before, `+` lines are after. `underwater_ireland.md` prints no difference when its header is unchanged, so read its header and count the grade rows instead (its header has no grade counts):

```bash
for v in old new; do
  if [ $v = old ]; then t=$(git show HEAD:./reports/underwater_ireland.md); else t=$(cat reports/underwater_ireland.md); fi
  echo "$v research=$(echo "$t" | grep -c '✅ Research Grade') needsid=$(echo "$t" | grep -c '🔍 Needs ID')"
done
head -8 reports/underwater_ireland.md | tail -3
```

The underwater life-list reports have different headers, so they need their own commands. `one_and_done_ireland.md` and `rarity_by_site_ireland.md` print their totals in a bold line near the top. `gap_analysis_ireland.md` has no total, so compare the rows of its Sites table (the "New for you" column). `year_in_review.html` has no header line: open it and compare the stat tiles by eye.

```bash
for f in one_and_done_ireland rarity_by_site_ireland; do
  echo "--- $f"
  git diff -U0 -- reports/$f.md | grep -E '^[-+]\*\*[0-9]+\*\*' | cut -c1-160
done
git diff -U0 -- reports/gap_analysis_ireland.md | grep -E '^[-+]\| \[' | cut -c1-120
```

Until these reports are committed there is nothing to diff against. The first run after committing them is the baseline.

Fill in the summary table with Before, After and Change for each metric. Include the metrics that didn't change, with 0, so a reader can see they were checked.

## 4. Find out why the numbers moved

Totals alone don't say what happened. Check these three causes.

**New observations.** The download is kept in `scripts/.cache/observations.json`. List what was uploaded since the last run (use the date of the last run):

```bash
.venv/bin/python - <<'EOF'
import collections, json
obs = json.load(open("scripts/.cache/observations.json"))
new = [o for o in obs if (o.get("created_at") or "") >= "2026-11-09"]   # day after the last run
print(len(new), collections.Counter(o.get("place_guess") for o in new), collections.Counter(o.get("quality_grade") for o in new))
EOF
```

Note whether the places are dive sites. Places in `IGNORED_KEYWORDS` (for example your home patch) only change the totals in `Location_ratings.md` and `species_classification.md`, and never appear in the underwater reports.

**Grade changes.** An observation can become Research Grade without being new. Compare the rows of the old and new `underwater_ireland.md`:

```bash
git diff -U0 -- reports/underwater_ireland.md | grep -E '^[-+]\|' | sed -E 's/\[!\[[^]]*\]\([^)]*\)\]\([^)]*\)//g; s/\]\(https[^)]*\)/]/g' | cut -c1-170
```

Each `-`/`+` pair is one observation. The same name with `Needs ID` before and `Research Grade` after is an upgrade. A different name is an identification change. Count the upgrades. The rarity reports count Research Grade only, so upgrades are the usual reason they gain taxa.

**Rarity reports.** Compare taxa, ratings and your own counts between the old and new rarity reports:

```bash
.venv/bin/python - <<'EOF'
import re, subprocess
def rows(txt):
    out = {}
    for l in txt.splitlines():
        m = re.match(r'\| *\d+ \| .*?\| \[([^\]]+)\]\(https://www.inaturalist.org/taxa/(\d+)\)(?: \(\*([^*]+)\*\))? \| (\w[\w ]*) \| ([\d,]+) \| ([\d,]+) \| (\S+) \| (\d+) \| (.*) \|$', l)
        if m:
            out[m.group(2)] = dict(name=m.group(1), rating=m.group(4), mine=int(m.group(8)), sites=m.group(9))
    return out
for f in ["rarity_underwater_ireland", "rarity_underwater_worldwide"]:
    old = rows(subprocess.run(["git", "show", f"HEAD:./reports/{f}.md"], capture_output=True, text=True).stdout)
    new = rows(open(f"reports/{f}.md").read())
    print("==", f, len(old), "->", len(new))
    print(" added:", [(new[k]["name"], new[k]["rating"], new[k]["sites"]) for k in new if k not in old])
    print(" removed:", [old[k]["name"] for k in old if k not in new])
    print(" rating changed:", [(new[k]["name"], old[k]["rating"], new[k]["rating"]) for k in new if k in old and old[k]["rating"] != new[k]["rating"]])
    print(" my obs changed:", [(new[k]["name"], old[k]["mine"], new[k]["mine"]) for k in new if k in old and old[k]["mine"] != new[k]["mine"]])
EOF
```

Other people's counts change on every run, because anyone can upload. Report that they moved, but don't list them.

**Nudibranchs and sites.** Check the changed rows the same way:

```bash
git diff -U0 -- reports/nudibranch_ireland.md | grep -E '^[-+]\|' | sed -E 's/\!\[[^]]*\]\([^)]*\)//g; s/\]\(https[^)]*\)/]/g' | cut -c1-170
git diff --stat -- reports/sites
git status --short reports/sites       # new files are untracked, so they don't show in git diff
```

## 5. Write the report

Copy the latest file in [`../reports/runs/`](../reports/runs) to `YYYY-MM-DD.md` and replace the numbers. Keep this order:

1. **The run**: command, result, observations downloaded, total time, a table of time per step, and anything that differed in how it ran.
2. **Summary table**: one row per metric, with Before, After and Change.
3. **The main result**: lead with the change the reader cares about most. For this project that is observations that became Research Grade, because they decide what the rarity reports rate.
4. **Other new observations**: with the place, and whether it is in the underwater reports.
5. **Identification changes**: a before and after table.
6. **Per-report changes**: nudibranchs, the two rarity reports, `reports/sites/`.
7. **To check**: uncommitted files, and anything inferred and not verified (say so, as the Crimora note in the 2026-11-13 report does).

Then add a row for the new file to the catalog in [`../reports/README.md`](../reports/README.md) only if the `runs/` row doesn't already cover it.

## Checks before you finish

- The arithmetic adds up. For example, the change in Research Grade in `species_classification.md` should equal the underwater upgrades plus the new Research Grade observations from places outside the underwater reports.
- The same-named rows in the Ireland and worldwide rarity reports are identical. They use the same observations.
- Every number came from a command above, not from memory. State anything inferred as inferred.
