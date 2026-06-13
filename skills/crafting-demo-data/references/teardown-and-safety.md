# Org Safety & Teardown

## Org-type safety check (run before any write)

Confirm the target org and refuse to silently write to production. The `Organization` object tells you what kind of org it is:

```bash
sf data query --target-org <alias> \
  --query "SELECT Name, IsSandbox, OrganizationType, TrialExpirationDate FROM Organization"
```

Interpretation:
- `IsSandbox = true` → sandbox. Safe for demo data.
- `TrialExpirationDate != null` → scratch/trial/demo org. Safe.
- `IsSandbox = false` AND `TrialExpirationDate = null` → **likely a production org.** STOP. Show the org name and require explicit, unambiguous confirmation ("yes, write demo data to production <Name>") before proceeding.

Also confirm the alias resolves to the org the user thinks it does:
```bash
sf org display --target-org <alias>
```

## Tagging strategy (CREATE only)

Pick the most precise marker the object supports, and record which one you used:

1. **External ID field** (best — also enables idempotent upsert): a unique, filterable key like `Demo_Key__c`. Inspect for one (or create + deploy it) per generating-data.md. Teardown filters on it exactly, and re-runs upsert instead of duplicating. Prefer this whenever you can add/find the field.
2. **Description/long-text prefix**: begin the field with `[DEMODATA:<run-id>]` where `<run-id>` is the run date or a short token. Works on most standard objects (Opportunity.Description, Contact.Description, Case.Description...). **Caveat:** not every long-text is filterable — `Account.Description` rejects `WHERE Description LIKE ...`. Confirm filterability or fall back to a keyed `Name`/created-date teardown for that object.
3. **Created-date window** (last resort): record the run's start/end timestamp and delete by `CreatedDate` range. Least precise — only when the object has no writable text/marker field.

Always state the chosen tag in the final report.

### By External ID
```bash
sf data delete bulk --sobject Account \
  --query "SELECT Id FROM Account WHERE Demo_Key__c LIKE 'energy-acct-%'" \
  --target-org <alias> --wait 10
```

## Teardown (delete exactly what was created)

### By marker field
```bash
sf data delete bulk --sobject Opportunity \
  --query "SELECT Id FROM Opportunity WHERE Demo_Source__c='crafting-demo-data'" \
  --target-org <alias> --wait 10
```

### By description prefix
```bash
sf data delete bulk --sobject Opportunity \
  --query "SELECT Id FROM Opportunity WHERE Description LIKE '[DEMODATA:run-2026-06-13]%'" \
  --target-org <alias> --wait 10
```
> **`Description` is not filterable on every object.** Notably `Account.Description` (a long textarea) rejects `WHERE Description LIKE ...` with `field 'Description' can not be filtered in a query call`. For those objects, tear down by another keyed field — e.g. the demo `Name` values you created — or by the created-date window below. Tag-by-Description still works for teardown on Opportunity, Contact, Case, etc.
> ```bash
> sf data delete bulk --sobject Account \
>   --query "SELECT Id FROM Account WHERE Name IN ('Aberdeen Offshore Wind plc','Helios Solar Energy Inc.')" \
>   --target-org <alias> --wait 10
> ```

### By created-date window
```bash
sf data delete bulk --sobject Opportunity \
  --query "SELECT Id FROM Opportunity WHERE CreatedDate >= 2026-06-13T10:00:00Z AND CreatedDate <= 2026-06-13T10:30:00Z" \
  --target-org <alias> --wait 10
```

## Teardown ordering
Delete **children before parents** — the reverse of insert order — or master-detail/required-lookup deletes will fail with reference errors. Example: OpportunityLineItem → Opportunity → Contact → Account.

## Dry-run a teardown
Before deleting, run the same WHERE as a `COUNT()` so the user sees how many rows will go:
```bash
sf data query -o <alias> -q "SELECT COUNT() FROM Opportunity WHERE Demo_Source__c='crafting-demo-data'"
```
Show the count, get approval, then delete.
