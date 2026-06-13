---
name: crafting-demo-data
description: "Schema-aware synthetic data crafting for Salesforce demos. Use this skill when a Solution Engineer (or anyone preparing a demo org) needs to populate objects with realistic, narrative-coherent demo data, OR refresh existing stale demo data in place (bump close dates forward, re-time activities, re-randomize values) WITHOUT creating new records. Discovers object schema first (required fields, picklists, record types, validation rules, relationships), builds a dependency-ordered plan, previews it (dry-run), then drives sf data CLI commands to create or update records — every created record tagged for clean teardown. TRIGGER when: user wants demo data, synthetic data for a demo/POC, sample records that look realistic, to seed a demo org, to refresh/freshen stale demo data, to make old opportunities/dates look current, or to tear down previously generated demo data. DO NOT TRIGGER when: generating Apex TestDataFactory or unit-test fixtures (use handling-sf-data), writing SOQL only (use querying-soql), running Apex tests (use running-apex-tests), or the objects/fields don't exist yet (use generating-custom-object / generating-custom-field first)."
license: MIT
metadata:
  version: "0.2"
---

<!--
Changelog
0.2 — Hardened from real-run failures + added re-run safety.
      • Idempotent CREATE: External ID + `sf data upsert` is now the default
        pattern (inspect for the field → reuse → else create+deploy → else fall
        back to a description tag). Plain insert is documented as NOT re-run safe.
      • Tree import: cross-file `@referenceId` only resolves via `--plan`, not
        `--files` (which fails with MALFORMED_ID); noted non-transactional recovery.
      • Bulk CSV gotchas: must use LF line endings and single-line field values.
      • Duplicate rules block bulk/tree inserts (DUPLICATES_DETECTED) — documented
        the Apex `Database.DMLOptions.DuplicateRuleHeader.allowSave=true` workaround
        and the "bulk reports back slowly → query before re-running" dedupe trap.
      • Ownership coherence rule (set OwnerId to the demo persona/team for visibility).
      • Teardown: `Account.Description` is not filterable in SOQL — key on Name/External ID.
0.1 — Initial release: CREATE + REFRESH modes, schema discovery, scenario
      templates, org-safety check, tagged teardown.
-->

# Crafting Demo Data (crafting-demo-data)

Populate a Salesforce org with **realistic, story-coherent demo data**, or **refresh stale demo data in place** so an existing org looks current. Built for Solution Engineers prepping demos and POCs — not for Apex unit-test fixtures (that's [handling-sf-data](../handling-sf-data/SKILL.md)).

The CRUD calls are the easy part. This skill's job is everything around them: **read the schema so records don't bounce, order inserts so relationships resolve, make the data look real on screen, tag everything so it can be cleanly removed, and never write to the wrong org.**

---

## Two modes — decide first

| Mode | Use when | Net effect on the org |
|---|---|---|
| **CREATE** | The org is empty or needs more records for a scenario | New rows inserted (and tagged) |
| **REFRESH** | The org already has demo data but it looks *stale* — past close dates, old activity timestamps, last-modified months ago | Existing rows **updated in place**, no new rows |

Always confirm which mode the user wants. REFRESH is the lighter touch and is often what an SE actually needs before a demo ("my pipeline all has 2024 close dates"). When unsure, ask.

See [references/refreshing-stale-data.md](references/refreshing-stale-data.md) for the REFRESH playbook and [references/generating-data.md](references/generating-data.md) for CREATE.

---

## Non-negotiable guardrails

1. **Org safety check before any write.** Confirm the target org alias and verify it is not a production org the user didn't intend. Run the org-type check in [references/teardown-and-safety.md](references/teardown-and-safety.md). Warn loudly and require explicit confirmation before writing to a non-sandbox, non-scratch org.
2. **Dry-run before commit.** Always present the plan (objects, counts, sample rows, field values) and get approval *before* executing. For REFRESH, show before→after for a sample of records.
3. **Tag everything created.** Every record this skill inserts carries a teardown marker (see Tagging below) so it can be removed precisely later. Never create untagged demo data.
4. **Schema-first, never guess.** Read the object describe (and validation rules) before generating values. Do not invent picklist values, omit required fields, or write to non-createable fields.
5. **Synthetic, non-PII data only.** Demo data must be obviously fake and safe — no real customer PII.

---

## Workflow

### 1. Gather intent
- CREATE or REFRESH?
- Target object(s) and the demo story (e.g. "a healthy Q3 pipeline for an energy account", "service cases trending down").
- Target org alias.
- Volume (CREATE) or scope/filter (REFRESH — which existing records).
- Industry/vertical, if a scenario template applies.

### 2. Org safety check
Verify the target org and its type. See [references/teardown-and-safety.md](references/teardown-and-safety.md). Stop and confirm if it looks like production.

### 3. Discover the schema (always)
For each object, pull the describe and the active validation rules. Extract: required fields, createable/updateable flags, field types & lengths, picklist values (incl. dependent picklists), record types, and lookup/master-detail relationships. Build the **dependency graph** so parents insert before children.

See [references/schema-discovery.md](references/schema-discovery.md) — exact `sf sobject describe` + `jq` recipes and the Tooling API query for validation rules.

### 4. Build the plan
- **CREATE:** choose mechanism per the table below, generate coherent values, order by dependency.
- **REFRESH:** query the target records, compute new field values (date shifts, re-randomization), build an update set keyed by `Id`.

### 5. Dry-run / preview — STOP for approval
Show the plan and a representative sample. **Wait for the user to approve before executing.** Do not proceed on the same turn.

### 6. Execute
Run the chosen `sf data` commands against the approved org. Capture record IDs / job IDs.

### 7. Verify
Re-query counts and relationships. For REFRESH, confirm the date/value shifts landed.

### 8. Report + leave teardown instructions
Always output the exact teardown command for what was created. See Output Format.

---

## Choosing the mechanism (CREATE)

| Need | Default approach |
|---|---|
| A few related records that tell a story | `sf data import tree` (preserves parent→child links via reference IDs) |
| Volume (hundreds–thousands) | CSV + `sf data import bulk` (Bulk API 2.0) |
| One-off single record | `sf data create record` |
| Mixed hierarchy at volume | tree for the spine, bulk for the leaves |

## Choosing the mechanism (REFRESH)

| Need | Default approach |
|---|---|
| Shift dates / re-randomize a field across many existing rows | query → build CSV with `Id` + changed fields → `sf data update bulk` |
| A handful of records | `sf data update record` per row |

---

## Tagging (so teardown is precise)

Every created record must be identifiable later. In priority order:
1. **An External ID field** (e.g. `Demo_Key__c`) — best: filterable for precise teardown *and* lets you `upsert` so re-runs don't duplicate. Inspect the schema for one; create + deploy it if absent and the org allows schema changes (see teardown-and-safety.md / generating-data.md).
2. **A description/notes field prefix** when the object has a *filterable* long-text field (`Description` starts with `[DEMODATA:<run-id>]`) — note `Account.Description` is **not** filterable in SOQL.
3. **A created-date window** as a last resort (delete records created during the run's timestamp window) — least precise, document it clearly.

Pick the most precise option the object supports and record which tag was used in the final report. Plain insert is not re-run safe — prefer External ID + upsert for repeatable demo prep. REFRESH does **not** tag (it edits pre-existing records the skill didn't create) — instead, the report lists exactly which IDs were touched.

---

## Output Format

```text
Mode:        CREATE | REFRESH
Org:         <alias>  (type: Sandbox/Scratch/Production-CONFIRMED)
Objects:     <object> — <count created / updated>
Tag:         <marker field=value | description prefix | created-date window>   (CREATE only)
Artifacts:   <tree/CSV/job IDs / record IDs>
Verification:<passed / partial / failed>
Teardown:    <exact sf data delete command for the tagged records>            (CREATE only)
Touched IDs: <list or query>                                                  (REFRESH only)
```

---

## Cross-skill boundaries

| Situation | Go to |
|---|---|
| Apex `TestDataFactory` / unit-test fixtures, governor-limit bulk testing | [handling-sf-data](../handling-sf-data/SKILL.md) |
| Pure SOQL authoring | [querying-soql](../querying-soql/SKILL.md) |
| Objects/fields don't exist yet | [generating-custom-object](../generating-custom-object/SKILL.md) / [generating-custom-field](../generating-custom-field/SKILL.md) then [deploying-metadata](../deploying-metadata/SKILL.md) |

This skill reuses the same `sf data` primitives as `handling-sf-data` but owns the **demo-specific intelligence**: coherence, scenarios, refresh-in-place, and demo-safe teardown.

---

## Reference Map
- [references/schema-discovery.md](references/schema-discovery.md) — describe + validation rules + dependency graph (read in step 3)
- [references/generating-data.md](references/generating-data.md) — coherence rules, date strategy, mechanism recipes (CREATE)
- [references/refreshing-stale-data.md](references/refreshing-stale-data.md) — refresh-in-place playbook (REFRESH)
- [references/teardown-and-safety.md](references/teardown-and-safety.md) — org-type check + tagged teardown
- [references/scenario-templates.md](references/scenario-templates.md) — industry/vertical demo scenarios
