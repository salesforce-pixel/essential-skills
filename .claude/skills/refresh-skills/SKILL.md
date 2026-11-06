---
name: refresh-skills
description: >-
  Fixed routine that refreshes the essential-skills repo against the live Salesforce
  documentation and pushes the result to GitHub main. TRIGGER when the user (or the
  scheduled run) asks to refresh / update / sync the skills from the docs, run the doc
  refresh, or "run /refresh-skills". Only valid inside the essential-skills repo
  (tools/doc-refresh/sources.json must exist). DO NOT TRIGGER for editing a single skill
  by hand, adding a new skill, or fetching one doc page (use fetching-salesforce-docs).
---

# refresh-skills — the doc refresh routine

Run these steps **in order, every time**. Don't skip, reorder or improvise; if a step's
stop condition hits, stop and report. The point of this routine is that every run
behaves the same, whether a person typed `/refresh-skills` or launchd started it via
`tools/doc-refresh/run.sh`.

Paths are relative to the repo root. `$TODAY` = today's date, `YYYY-MM-DD`.

## 1. Preflight

```bash
test -f tools/doc-refresh/sources.json   # else STOP: not in the essential-skills repo
git status --porcelain                   # must be empty, else STOP (don't stash or commit someone's work)
git switch main && git pull --ff-only    # if pull isn't fast-forward, STOP
```

## 2. Refresh (script; deterministic)

```bash
python3 -I tools/doc-refresh/refresh.py --bump \
  --summary tools/doc-refresh/.out/summary.md --json tools/doc-refresh/.out/result.json
```

- Exit code 1 = a **mirror** skill failed to fetch and nothing was written for it. Keep
  going with the rest; record the error for the report.
- Read `tools/doc-refresh/.out/summary.md`. Then `git status --porcelain`. If nothing changed,
  report "No upstream changes" (plus any fetch failures) and **STOP — no commit**.

## 3. Mirror skills (e.g. `agentscript`)

The script already overwrote the pages and bumped `metadata.version` + changelog.

- **New pages**: add one line for each to the matching section of that skill's
  `SKILL.md` index (use the page's `#` title and first paragraph), then edit the
  auto-generated changelog line "New (add to the SKILL.md index)" to "New (indexed)".
- **Removed upstream**: don't delete the file. Mention it in the report.
- Don't otherwise edit the refreshed pages — they're the docs, verbatim.

## 4. Curated skills (hand-written; snapshots in `tools/doc-refresh/snapshots/<skill>/`)

For each curated skill with changed / new / removed snapshots:

1. **Baseline check.** If the skill's snapshot folder isn't in `HEAD`
   (`git ls-tree -d HEAD tools/doc-refresh/snapshots/<skill>` prints nothing), this is
   its first snapshot. Don't edit the skill; just report it as "baseline created".
2. Otherwise, read what changed: `git diff -- tools/doc-refresh/snapshots/<skill>/`
   (and read new snapshot files in full).
3. Compare against the skill's `SKILL.md` and `references/`. Edit the skill **only** when
   the docs now contradict it or add something within its stated scope: syntax, field or
   parameter names, required settings, limits, API versions, deprecations, new
   components/endpoints. Rewording, typo fixes, layout and nav changes → **no edit**.
4. Edit minimally, in the skill's existing style. **Tested findings win over docs:** if the
   skill marks something as verified/observed in an org and the docs now disagree, keep it
   and add a one-line note ("docs now say X — re-verify"), don't overwrite it.
5. If you edited the skill: bump its `metadata.version` minor (`1.4` → `1.5`) and add a
   changelog entry at the top of its `Changelog` comment:
   `X.Y — Doc refresh ($TODAY): <what changed> (source: <snapshot paths>).`
6. If no edit was needed, still list the skill and the changed pages in the report with
   "reviewed, no skill change" and a few words on why.

Removed snapshots: the script already deleted them. If the skill cites that page, flag it
in the report; don't remove guidance on that basis alone.

## 5. Validate

```bash
python3 -I tools/doc-refresh/check.py
```

Fix whatever it reports in files you touched in this run. If it fails on something you
didn't touch, don't fix it — report it and continue. Never push with a failure you
introduced.

## 6. Commit and push to main

Stage only `skills/`, `tools/doc-refresh/` and `README.md`. Never stage anything else.

```bash
git add skills tools/doc-refresh README.md
git commit -F tools/doc-refresh/.out/commit.txt
git push origin main
```

Commit message (`tools/doc-refresh/.out/commit.txt`):

```
Doc refresh $TODAY: <comma-separated skills whose SKILL.md or references changed>

<contents of tools/doc-refresh/.out/summary.md, trimmed to changed skills>

Skill edits:
- <skill> X.Y → X.Z: <one line>
- <skill>: reviewed, no skill change (<why>)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

If only snapshots changed and no skill was edited, the subject is
`Doc refresh $TODAY: snapshots only`.

If the push is rejected: `git pull --rebase` once, rerun step 5, push again. If it still
fails, STOP and report. **Never** force-push, never push to another branch, never amend
published commits.

## 7. Report

Finish with a short report (this is also what the headless log records):

- Commit hash pushed, or "nothing to commit".
- For each skill: version change, or "unchanged", or "reviewed, no skill change".
- Fetch failures, removed-upstream pages, baselines created, check.py issues left.
- Anything that needs a person (e.g. a doc change you weren't sure how to apply).
