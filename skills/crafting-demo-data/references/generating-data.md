# Generating Data (CREATE mode)

The difference between useful demo data and obviously-fake data is **coherence**: values that hang together and dates that make sense relative to "today".

## Coherence rules

- **Names tell a story, not random strings.** Accounts: plausible company names in the demo's industry. Contacts: realistic person names with matching email domains (`first.last@account-domain.com`).
- **Geography is consistent.** Billing city/state/country, phone area code, and currency should agree.
- **Dates are relative to today, never hardcoded.** Compute from the current date at run time:
  - `CreatedDate`-style "age": spread historical records over the past 1–18 months.
  - Opportunity `CloseDate`: open deals close in the **near future** (next 1–4 quarters); won/lost deals closed in the recent past.
  - Activities: recent (last 30–90 days) so timelines look active.
- **Distributions look real on a dashboard.** A pipeline isn't 50 identical $100k deals — vary amounts, stages, and close dates so charts render believably. Skew stages toward the funnel shape (more early-stage than late-stage).
- **Ownership drives visibility.** A demo is a *persona* in a role — if every record is owned by the running/integration user, the persona's "my pipeline," manager roll-ups, and forecasts show nothing. Decide who should own the data and set `OwnerId` accordingly (spread across the demo's sales team if role hierarchy / forecasting is part of the story). Query the intended owners up front: `sf data query -o <alias> -q "SELECT Id, Name FROM User WHERE IsActive=true AND ..."`.
- **Respect the schema** (see schema-discovery.md): only valid picklist values, required fields populated, record type set, parents first.

> Get the current date from the session context or `date +%Y-%m-%d`, then compute offsets — do **not** bake in literal future/past years, or the data is stale the moment the calendar turns.

## Mechanism A — tree import (related records, preserves links)

Best for the demo "spine" (a few accounts with their contacts/opps). Reference IDs wire children to parents without knowing real IDs.

`accounts.json`:
```json
{ "records": [
  { "attributes": {"type":"Account","referenceId":"acct_northwind"},
    "Name":"Northwind Energy", "Industry":"Energy", "BillingCity":"Aberdeen", "BillingCountry":"United Kingdom",
    "Description":"[DEMODATA:run-2026-06-13] crafting-demo-data" }
]}
```
`opportunities.json` (references the account by `referenceId`):
```json
{ "records": [
  { "attributes": {"type":"Opportunity","referenceId":"opp_1"},
    "Name":"Northwind - Platform Expansion", "StageName":"Proposal/Price Quote",
    "CloseDate":"2026-09-30", "Amount":250000, "AccountId":"@acct_northwind",
    "Description":"[DEMODATA:run-2026-06-13]" }
]}
```
Import with a **plan file** so cross-file `@referenceId` links resolve:
```bash
sf data import tree --plan import-plan.json --target-org <alias>
```
`import-plan.json` (parents first; `saveRefs` exports a record's id, `resolveRefs` consumes `@ref`s):
```json
[
  { "sobject": "Account",     "files": ["accounts.json"],      "saveRefs": true,  "resolveRefs": false },
  { "sobject": "Contact",     "files": ["contacts.json"],      "saveRefs": true,  "resolveRefs": true },
  { "sobject": "Opportunity", "files": ["opportunities.json"], "saveRefs": false, "resolveRefs": true }
]
```
> **`--files a.json,b.json` does NOT resolve `@ref` across files** — children fail with `MALFORMED_ID: id value of incorrect type: @acct_x`. Cross-file references only resolve via `--plan`. (Tree import is also non-transactional across files: if the parents commit and the children bounce, the parents stay. Recover by attaching children to the now-real parent IDs via bulk/Apex rather than re-importing the parents.)

## Mechanism B — bulk CSV (volume)

For hundreds–thousands of flat records. Include the tag column.

`opps.csv`:
```csv
Name,StageName,CloseDate,Amount,AccountId,Description
"Acme - Renewal","Negotiation/Review",2026-08-15,75000,001XXXXXXXXXXXXAAA,"[DEMODATA:run-2026-06-13]"
```
```bash
sf data import bulk --sobject Opportunity --file opps.csv --target-org <alias> --wait 10
```
Parent `AccountId`s must be real IDs — query or create accounts first, then template them into the CSV.

> **Bulk CSV must use LF line endings, and field values must be single-line.** The job defaults to `lineEnding=LF`; a CRLF file fails with `ClientInputError: LineEnding is invalid on user data`. Most CSV writers emit CRLF by default (Python `csv` uses `\r\n`) — force LF (`lineterminator='\n'`). Embedded newlines inside a quoted field (e.g. a multi-line `Description`) trip the same error even on an LF file — flatten such values to one line before writing.

> **Duplicate rules block bulk insert** (`DUPLICATES_DETECTED:Use one of these records?`), and the CLI bulk/tree paths can't pass the allow-save header. When this fires, insert via anonymous Apex with the duplicate-rule header off — and **query first** to confirm the rows aren't already there, since a bulk job can report back slowly after actually committing (re-running then creates a second copy you must dedupe):
> ```apex
> Database.DMLOptions dml = new Database.DMLOptions();
> dml.DuplicateRuleHeader.allowSave = true;
> dml.DuplicateRuleHeader.runAsCurrentUser = true;
> Database.insert(records, dml);
> ```

## Mechanism C — single record

```bash
sf data create record --sobject Account \
  --values "Name='Acme Solar' Industry='Energy' Description='[DEMODATA:run-2026-06-13]'" \
  --target-org <alias>
```

## Make CREATE idempotent — External ID + upsert (preferred)
A plain insert is **not re-run safe**: run it twice and you get duplicates (and bulk jobs can report back *after* committing, so a "failed-looking" run may already have inserted). The fix is an **External ID** field holding a deterministic key per record (e.g. `Demo_Key__c = "energy-acct-aberdeen"`), then `upsert` against it — re-runs update in place instead of duplicating. The same field doubles as the teardown tag and is filterable (unlike `Account.Description`).

**This field may not exist — inspect first, then decide:**
```bash
# Does the object already have an external-id field we can reuse?
sf sobject describe --sobject Account --target-org <alias> --json \
  | jq -r '.result.fields[] | select(.externalId==true) | .name'
```
- **Exists** → use it as the upsert key.
- **Doesn't exist** → create one (a Text field with `externalId=true`, `unique=true`), then deploy it **before** loading data. Hand off to [generating-custom-field](../generating-custom-field/SKILL.md) + [deploying-metadata](../deploying-metadata/SKILL.md). One field per object you intend to upsert. Note this is a **metadata change**: it needs deploy/customize-app permission, and some SEs won't want demo prep altering the org's schema — confirm before creating fields.
- **Can't / shouldn't add a field** (read-only metadata, locked org) → fall back to the description-prefix tag below and accept that CREATE is not idempotent (query-before-insert and dedupe if you must re-run).

Upsert once the key field exists:
```bash
sf data upsert bulk --sobject Account --file accounts.csv \
  --external-id Demo_Key__c --target-org <alias> --wait 10
```

## Always tag
Even with an External ID, also carry `[DEMODATA:<run-id>]` in a description/long-text field where one exists — a human-readable marker for anyone browsing the org. The External ID is the precise, filterable teardown/upsert key; the description tag is the readable backup. See teardown-and-safety.md.

## Verify after insert
```bash
sf data query -o <alias> -q "SELECT COUNT() FROM Opportunity WHERE Description LIKE '[DEMODATA:run-2026-06-13]%'"
```
