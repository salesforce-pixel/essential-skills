# Schema Discovery

Read the schema **before** generating any value. Guessing causes `REQUIRED_FIELD_MISSING`, invalid-picklist, and non-createable-field errors.

## 1. Describe the object

```bash
sf sobject describe --sobject Opportunity --target-org <alias> --json > /tmp/opp-describe.json
```

### Required, createable fields (must be supplied on insert)
A field is effectively required on create when `nillable=false`, `defaultedOnCreate=false`, and `createable=true`.

```bash
jq -r '.result.fields[]
  | select(.createable==true and .nillable==false and .defaultedOnCreate==false)
  | "\(.name)\t\(.type)\t\(.length)"' /tmp/opp-describe.json
```

### Non-createable / non-updateable fields (NEVER put these in a payload)
```bash
# not createable
jq -r '.result.fields[] | select(.createable==false) | .name' /tmp/opp-describe.json
# not updateable (matters for REFRESH)
jq -r '.result.fields[] | select(.updateable==false) | .name' /tmp/opp-describe.json
```

### Picklist values (use these verbatim — never invent)
```bash
jq -r '.result.fields[] | select(.type=="picklist")
  | "\(.name): " + ([.picklistValues[] | select(.active==true) | .value] | join(", "))' \
  /tmp/opp-describe.json
```

### Dependent picklists
A dependent picklist has `dependentPicklist=true` and a `controllerName`. The valid child values depend on the controlling field's value (encoded in `validFor`). When you hit one, pick a controlling value first, then a child value valid for it. If `validFor` decoding is needed, prefer choosing a controlling value whose children are obvious, or fall back to the API default.

### Record types
```bash
jq -r '.result.recordTypeInfos[] | select(.available==true)
  | "\(.name)\t\(.recordTypeId)\t(default: \(.defaultRecordTypeMapping // false))"' \
  /tmp/opp-describe.json
```
If the object has >1 active record type, set `RecordTypeId` explicitly — picklist availability and page layout depend on it.

### Relationships (drives insert ordering)
```bash
jq -r '.result.fields[] | select(.type=="reference")
  | "\(.name) -> \(.referenceTo | join(",")) (required=\(.nillable==false))"' \
  /tmp/opp-describe.json
```
- `master-detail`-style required references (`nillable=false`, `type=reference`) mean the **parent must exist first**.
- `relationshipName` is what you use in tree-import reference syntax.

## 2. Validation rules (the silent killer — NOT in describe)

Validation rules live in metadata/Tooling, not in `sobject describe`. Query them so generated data actually satisfies them:

```bash
sf data query --use-tooling-api --target-org <alias> \
  --query "SELECT ValidationName, Active, ErrorMessage, ErrorDisplayField FROM ValidationRule WHERE EntityDefinition.QualifiedApiName='Opportunity' AND Active=true"
```

To read the actual formula (so you can generate conforming values), retrieve the metadata:
```bash
sf project retrieve start --metadata "ValidationRule:Opportunity.*" --target-org <alias>
```
Then read the `errorConditionFormula` in the retrieved `.validationRule-meta.xml`. Generate field values that make the formula evaluate to **false** (rule does not fire).

### Duplicate rules (the other silent killer)
Active duplicate rules reject inserts with `DUPLICATES_DETECTED` — and the CLI bulk/tree import paths can't pass the allow-save header to override them. Check before a CREATE so you know whether to route through Apex:
```bash
sf data query --use-tooling-api --target-org <alias> \
  --query "SELECT DeveloperName, IsActive, SobjectType FROM DuplicateRule WHERE IsActive=true"
```
If an active rule covers your target object, insert via anonymous Apex with `Database.DMLOptions.DuplicateRuleHeader.allowSave=true` (see generating-data.md, Mechanism B). Contact/Account/Lead commonly ship with a standard active rule.

## 3. Build the dependency graph

From the required `reference` fields, produce a topological order. Standard CRM spine:

```
Account → Contact → Opportunity → OpportunityContactRole / OpportunityLineItem
Account → Case
Product2 → PricebookEntry → OpportunityLineItem
```

Insert parents first; capture their IDs (or use tree-import reference IDs) to populate child lookups. For `OpportunityLineItem` you also need an active `Pricebook2` + `PricebookEntry` for the product — query the standard pricebook:
```bash
sf data query -o <alias> -q "SELECT Id FROM Pricebook2 WHERE IsStandard=true LIMIT 1"
```

## Pre-flight checklist (per object)
- [ ] required createable fields enumerated and will be populated
- [ ] picklist values pulled from describe (not guessed)
- [ ] record type chosen if multiple exist
- [ ] required parent references resolved / ordered first
- [ ] active validation rules read and generated values conform
- [ ] non-createable fields excluded from payload
