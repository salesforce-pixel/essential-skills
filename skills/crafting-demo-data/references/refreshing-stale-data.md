# Refreshing Stale Data (REFRESH mode)

The common SE problem: a demo org already has good data, but it's **stale** — opportunity close dates are in the past, the pipeline shows nothing closing "this quarter," activities are months old, and "Last Modified" looks abandoned. REFRESH fixes this **in place** by updating existing records — no new rows, no broken relationships, no re-seeding.

REFRESH never creates records and never tags (it edits records the skill didn't create). Instead, the final report lists exactly which IDs were touched.

## The playbook

### 1. Identify the stale scope
Query the records that look old. Examples:
```bash
# Open opps whose close date is already in the past
sf data query -o <alias> \
  -q "SELECT Id, Name, StageName, CloseDate, Amount FROM Opportunity WHERE IsClosed=false AND CloseDate < TODAY"

# Activities older than 90 days
sf data query -o <alias> \
  -q "SELECT Id, Subject, ActivityDate FROM Task WHERE ActivityDate < LAST_N_DAYS:90"
```

### 2. Confirm the field is updateable
Check `updateable=true` in the describe (see schema-discovery.md). Skip non-updateable / formula / rollup fields — they can't be written.

### 3. Compute new values (relative to today)
Pick a refresh strategy per field:

| Field kind | Strategy |
|---|---|
| Open opp `CloseDate` in the past | Roll forward into the current/next quarter, preserving relative spacing |
| Activity dates (`Task.ActivityDate`, `Event.StartDateTime`) | Shift the whole set forward by a constant offset so timelines stay coherent |
| `Amount` / numeric | Optionally re-randomize within ±X% to vary dashboards |
| Stage | Usually leave as-is unless the story needs movement |

**Date-shift approach (preserves relative spacing):** compute `offset = today - max(old date in set)` (rounded), then add `offset` to every record's date. The pipeline keeps its shape; it just slides to "now."

### 4. Build the update set keyed by Id
Bulk update needs a CSV with an `Id` column plus only the changed fields:

`refresh-opps.csv`:
```csv
Id,CloseDate
006XXXXXXXXXXXXAAA,2026-09-15
006YYYYYYYYYYYYAAA,2026-10-30
```
```bash
sf data update bulk --sobject Opportunity --file refresh-opps.csv --target-org <alias> --wait 10
```

For a handful of records, single updates are fine:
```bash
sf data update record --sobject Opportunity --record-id 006XX... --values "CloseDate=2026-09-15" -o <alias>
```

### 5. Dry-run before committing
Show a **before → after** sample (5–10 rows) so the user can sanity-check the shift:
```
Opp "Northwind Expansion": CloseDate 2024-11-30 → 2026-09-30   (open)
Opp "Acme Renewal":        CloseDate 2024-08-15 → 2026-06-15   (open)
```
Wait for approval before running the update.

### 6. Verify
```bash
sf data query -o <alias> -q "SELECT COUNT() FROM Opportunity WHERE IsClosed=false AND CloseDate < TODAY"
```
Should return 0 (no open opps left in the past) after a close-date refresh.

## Cautions
- **Watch validation rules and triggers** — updating a record fires them. If an update bounces, read the rule (schema-discovery.md) and adjust the value.
- **Don't touch audit fields** — `CreatedDate`/`LastModifiedDate` aren't updateable through normal DML (they need `--use-tooling-api` audit-field create permission and are out of scope here). Refresh business dates (CloseDate, ActivityDate), not system audit stamps.
- **Bulk update replaces only the columns present** in the CSV — include `Id` + the fields you intend to change, nothing else.
