# Custom Lightning Types (CLTs) + renderer.json

Two schemas, two jobs:
- **CLT `schema.json`** = the *data* shape (what the action/tool returns).
- **Widget `schema.json`** = the *UI* attribute contract.
- **CLT `renderer.json`** = the mapping between them.

## Widget schema.json (both scenarios)

```json
{
  "title": "Account Health Card",
  "description": "One account's health: revenue, cases, open opportunities.",
  "type": "object",
  "properties": {
    "attributes": {
      "lightning:type": "lightning__objectType",
      "properties": {
        "accountName": { "title": "Account", "lightning:type": "lightning__textType" },
        "annualRevenue": { "title": "Annual Revenue", "lightning:type": "lightning__numberType" },
        "isAtRisk": { "title": "At Risk", "lightning:type": "lightning__booleanType" },
        "openOpportunities": {
          "title": "Open Opportunities",
          "lightning:type": "lightning__listType",
          "items": { "lightning:type": "@apexClassType/c__AccountHealthService$Opp" }
        }
      }
    }
  }
}
```

### Apex → `lightning:type` mapping

| Apex | Widget / CLT `lightning:type` |
|---|---|
| `String`, `Id` | `lightning__textType` (≤255) — long text: `lightning__multilineTextType` / `lightning__richTextType` |
| URL string | `lightning__urlType` |
| `Decimal`, `Double`, `Long` | `lightning__numberType` |
| `Integer` | `lightning__numberType` (or `lightning__integerType`) |
| `Boolean` | `lightning__booleanType` |
| `Date` / `Datetime` | `lightning__dateType` / `lightning__dateTimeType` (tip: returning ISO **strings** as `lightning__textType` is simpler for display + `DATEVALUE`) |
| `List<String>` | `lightning__listType` + `items.lightning:type: lightning__textType` |
| `List<Inner>` | `lightning__listType` + `items.lightning:type: @apexClassType/c__Outer$Inner` |
| `Inner` (single) | `@apexClassType/c__Outer$Inner` (bind `{!$attrs.field.sub}`) |
| Plain object list, no Apex | `lightning__listType` + `items: { "lightning:type": "lightning__objectType", "properties": {…} }` |

Keep Apex field names = widget attribute names where possible; labels go in `title`.

---

## Scenario B — Agentforce action output (1 Apex-based CLT)

```
lightningTypes/accountHealth/
  schema.json
  renderer.json      ← root, parallel to schema.json
```

`schema.json`
```json
{
  "title": "Account Health",
  "description": "Structured account health returned by the Get Account Health action",
  "lightning:type": "@apexClassType/c__AccountHealthService$AccountHealth"
}
```

`renderer.json` — direct mapping
```json
{
  "renderer": {
    "componentOverrides": {
      "$": {
        "definition": "@widget/c/accountHealthCard",
        "attributes": {
          "accountName": "{!$attrs.accountName}",
          "annualRevenue": "{!$attrs.annualRevenue}",
          "isAtRisk": "{!$attrs.isAtRisk}",
          "openOpportunities": "{!$attrs.openOpportunities}"
        }
      }
    }
  }
}
```

Then in Setup → **Agentforce Assets** → Actions → your action → edit the output → **Show in conversation** → **Output Rendering** = `accountHealth` → Save → reload the agent. The output's Data Type will show `@apexClassType/c__AccountHealthService$...` — the CLT must reference the same class the output carries.

---

## Scenario C — MCP tool output (2 object-based CLTs)

The MCP tool returns an envelope: `{ actionName, isSuccess, outputValues: { … } }`. A CLT can't reference itself, so:

| Role | Folder (convention) | Contains | renderer.json? |
|---|---|---|---|
| **Payload** | `<tool>OutputValues` | one property per `@InvocableVariable` on the response class | **No** |
| **Result wrapper** | `<tool>Result` | `actionName`, `isSuccess`, `outputValues → c__<payload>` | **Yes** |

Payload `lightningTypes/accountHealthOutputValues/schema.json`
```json
{
  "title": "Account Health Output Values",
  "description": "Payload fields from the Get Account Health invocable action",
  "type": "object",
  "lightning:type": "lightning__objectType",
  "lightning:tags": ["mcp"],
  "unevaluatedProperties": false,
  "properties": {
    "accountHealth": {
      "title": "Account Health",
      "lightning:type": "@apexClassType/c__AccountHealthService$AccountHealth"
    }
  }
}
```

Wrapper `lightningTypes/accountHealthResult/schema.json`
```json
{
  "title": "Account Health Result",
  "description": "Invocable-action result envelope for the Get Account Health MCP tool",
  "type": "object",
  "lightning:type": "lightning__objectType",
  "lightning:tags": ["mcp"],
  "unevaluatedProperties": false,
  "properties": {
    "actionName": { "title": "Action Name", "lightning:type": "lightning__textType" },
    "isSuccess": { "title": "Is Success", "lightning:type": "lightning__booleanType" },
    "outputValues": { "title": "Output Values", "lightning:type": "c__accountHealthOutputValues" }
  }
}
```

Wrapper `renderer.json` — nested mapping
```json
{
  "renderer": {
    "componentOverrides": {
      "$": {
        "definition": "@widget/c/accountHealthCard",
        "attributes": {
          "accountName": "{!$attrs.outputValues.accountHealth.accountName}",
          "isAtRisk": "{!$attrs.outputValues.accountHealth.isAtRisk}",
          "openOpportunities": "{!$attrs.outputValues.accountHealth.openOpportunities}"
        }
      }
    }
  }
}
```

Path anatomy: `outputValues` (wrapper prop) → `accountHealth` (payload prop = `@InvocableVariable` name) → `accountName` (Apex inner-class field).

MCP rules:
- Payload property names are **1:1 with the response class's `@InvocableVariable` names** — never invent a grouping key.
- Non-primitive payload properties are `@apexClassType/c__Outer$Inner` — never bare `{"type":"object"}`.
- Only CLT-reference prefix in `outputValues` is `c__` (or `<ns>__` in packaged orgs); widget references always use `@widget/c/…`.
- `actionName` / `isSuccess` never go into the widget.
- Beta models a single result, not a bulk `content[]` array.
- Deploy payload CLT before wrapper CLT (or in one package).

## Shared rules

- `renderer.json` at CLT root; not `lightningDesktopGenAi/`; `editor.json` can't reference widgets.
- `definition`: `@widget/c/<widgetName>` (always `c`).
- Every renderer key must exist in the widget schema; map every widget attribute you bind.
- Deploy widget before (or with) the CLT that references it.
- Don't create/edit widget-referencing CLTs in Setup's Lightning Types page.
- **Widget schema is additive-only once deployed.** Removing a property fails the deploy with "Schema update contains breaking changes: You can't delete the $.properties.attributes.properties.<x> property". When a redesign drops an attribute, keep it declared in the widget schema and still mapped in the renderer; just stop binding it. New attributes (e.g. Apex-computed labels) can be added freely. Adding fields to the Apex inner class and redeploying the CLTs worked without issue.
- In scenario C, map display-ready fields (labels, variants, booleans) computed in Apex. The widget can't compute them with formulas in this channel (see `formulas.md`).
