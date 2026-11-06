# LightningTypeBundle and schema.json

## Building blocks

| Artifact | File | Role |
|---|---|---|
| **Schema** | `schema.json` (required) | Data structure + validation (type, format, max length) |
| **Editor** | `<channel>/editor.json` (optional) | Input UI: the LWC that captures or edits data |
| **Renderer** | `<channel>/renderer.json` (optional) | Output UI: the LWC that displays data. Supports single (`$`) and **collection** overrides |

`LightningTypeBundle` is the metadata type (API **64.0+**). It extends `Metadata`. Fields:
`masterLabel` (required), `description`, `resources` (`LightningTypeBundleResource[]`, each with
`fileName`, `filePath`, `fileType`, `source` base64 JSON). In a DX project you only
write the folder. The CLI builds the resources.

## Folder structure

```
force-app/main/default/
  lightningTypes/
    <typeName>/                 ← folder name = type API name → referenced as c__<typeName>
      schema.json
      lightningDesktopGenAi/    ← optional, one folder per channel
        editor.json   and/or  renderer.json
      enhancedWebChat/
        renderer.json
      lightningMobileGenAi/
        renderer.json
```

HXL widget variant (Beta): `renderer.json` sits at the **type root**, parallel to
`schema.json`, with no channel folder and no `editor.json`. See `hxl-widget-builder`.

## Channels (Salesforce applications you can override)

| Application | Channel folder | CLT category |
|---|---|---|
| Agentforce Employee agent in Lightning Experience | `lightningDesktopGenAi` | Apex |
| Agentforce Service agent via Enhanced Chat v2 | `enhancedWebChat` | Apex |
| Agentforce Employee agent on Mobile (iOS/Android) **and** Service agent via Enhanced Chat v2 on Mobile | `lightningMobileGenAi` | Apex |
| Experience Builder | `experienceBuilder` (`editor.json` only; no `renderer.json`) | Object |
| Prompt Builder | n/a (no channel folder) | Object |
| Flows via Structured Outputs | n/a | Object |

A channel only uses overrides in its own folder. If a user tests in Enhanced Chat but
you only wrote `lightningDesktopGenAi/`, they get the default UI. Copy the JSON into every
channel you need.

## Apex-based schema.json

| Keyword | Required | Notes |
|---|---|---|
| `title` | Yes | String or custom label `{!$Label.c.Name}` |
| `description` | No | String or custom label |
| `lightning:type` | Yes | `@apexClassType/<ns>__<ClassName>`. Shorthand for JSON Schema `$ref` |

```json
{
  "title": "My Flight Response",
  "description": "My Flight Response",
  "lightning:type": "@apexClassType/c__AvailableFlight"
}
```

Use only those keys. The properties are **projected** from the class's `@AuraEnabled`
members at runtime. Inner classes are written `@apexClassType/c__Outer$Inner` (sf-skills
and `hxl-widget-builder` use this form). The Lightning Types guide says to make every class
top-level, so prefer top-level classes, especially in namespaced orgs and packages.

## Object-based schema.json

| Keyword | Required | Notes |
|---|---|---|
| `title` | Yes | |
| `description` | No | |
| `lightning:type` | Yes | `lightning__objectType` |
| `properties` | Yes | Map of name → `{ "title", "lightning:type", constraints… }` |
| `required` | No | Array of property names |

Doc example:

```json
{
  "title": "customerFeedback",
  "description": "Structured format for capturing customer feedback received.",
  "lightning:type": "lightning__objectType",
  "properties": {
    "customerName":      { "title": "customerName",      "lightning:type": "lightning__textType" },
    "feedbackDate":      { "title": "feedbackDate",      "lightning:type": "lightning__dateType" },
    "satisfactionScore": { "title": "satisfactionScore", "lightning:type": "lightning__numberType" }
  },
  "required": ["customerName"]
}
```

Creating or updating an object-based CLT **auto-generates a matching Apex class**.

Stricter rules from sf-skills (`platform-custom-lightning-type-generate`). The docs example
above doesn't follow them. Apply them when a deploy rejects a schema:

- Root: add `"type": "object"` and `"unevaluatedProperties": false` (the metaschema enforces
  `false`). Then **any unknown keyword fails**, and `examples` isn't allowed.
- **Never** include `"$schema"`.
- Nested object properties must **not** use `lightning__objectType`. Reference another CLT
  (`"lightning:type": "c__<otherType>"`, which must be deployed first) or an Apex class type.
- Arrays: treat `items` as disallowed. Root-level list: `"lightning:type": "lightning__listType"`
  (optional `"type": "array"`). Nested list: `"type": "array"` only.
- Allowed property keywords: `title`, `description`, `einstein:description`, `type`,
  `lightning:type`, `maximum`, `minimum`, `multipleOf`, `maxLength`, `minLength`, `const`,
  `enum`, `lightning:textIndexed`, `lightning:supportsPersonalization`,
  `lightning:localizable`, `lightning:uiOptions`, `lightning:allowedUrlSchemes`,
  `lightning:tags` (`flow`, `mcp`).

## Standard Lightning types

`lightning__booleanType`, `lightning__dateType`, `lightning__dateTimeType`,
`lightning__dateTimeStringType`, `lightning__integerType`, `lightning__multilineTextType`,
`lightning__numberType`, `lightning__objectType`, `lightning__richTextType`,
`lightning__textType`, `lightning__timeType`, `lightning__urlType`. Agent actions also use
`lightning__listType` (lists) and `lightning__recordInfoType`. Support varies by application.

| Type | Constraints (sf-skills) |
|---|---|
| `lightning__textType` | max length 255 |
| `lightning__multilineTextType` | max length 2000 |
| `lightning__richTextType` | max length 100000 |
| `lightning__urlType` | max 2000; `lightning:allowedUrlSchemes`: `https`, `http`, `relative`, `mailto`, `tel` |
| `lightning__dateType` | `YYYY-MM-DD` |
| `lightning__timeType` | `HH:MM:SS.sssZ` |
| `lightning__dateTimeType` | object `{ dateTime (required), timeZone }` |
| `lightning__numberType` | decimals; `maximum`, `minimum`, `multipleOf` |
| `lightning__integerType` | whole numbers; `maximum`, `minimum` |
| `lightning__booleanType` | true/false |

Spell type names exactly. `lightning__richtextType` (lower-case `t`) fails.

## Namespaces

- Metadata **created in your org** (or new metadata in the **same** managed package): prefix
  `c`, even if the org has its own namespace. Use `c/flightDetails` (LWC) and
  `@apexClassType/c__Flight` / `c__flightResponse` (types).
- Metadata **installed from a managed package**: that package's namespace, e.g. `isv/flightDetails`.

## Custom labels

Setup → Custom Labels → create a label, then in `schema.json` use `"title": "{!$Label.c.MyLabel1}"`
(also works for `description`). Translations come from the label's translations.

## Safe changes

**Apex-based** (the class behind `lightning:type`):

| Change | Status |
|---|---|
| Add new `@AuraEnabled` fields | Permitted. Projection picks them up |
| Rename / delete the class | Prohibited. Runtime failures |
| Change a field's data type | Breaking |
| Remove an `@AuraEnabled` field an action uses | Breaking. Invocation errors |
| `global` → `public` in a managed package | Prohibited |

**Object-based**: free to change until a Salesforce application references the type. After that:

| Keyword | Rule |
|---|---|
| `title`, `description` (of a property) | Can change |
| `lightning:type` | Can't change |
| `properties` | Can add **optional** properties. Can't remove/rename or add a **required** one |
| `required` | Can remove entries. Can't add |
| `maximum` / `maxLength` | Can only increase |
| `minimum` / `minLength` | Can only decrease |
| `multipleOf` | The existing value must be divisible by the new one (20 → 2, 4, 5, 10 OK; 15, 40 not OK) |
| `lightning:allowedUrlSchemes` | Can only add schemes |

## Deploy, retrieve, delete

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>flightResponse</members>   <!-- or * : wildcard supported -->
        <name>LightningTypeBundle</name>
    </types>
    <version>64.0</version>
</Package>
```

```bash
sf project deploy start --metadata LightningTypeBundle:flightResponse --target-org <alias>
sf project retrieve start --metadata "LightningTypeBundle:*" --target-org <alias>
```

- Deploy the Apex classes and LWCs **before or with** the bundle that references them.
  Deploy a referenced CLT (`c__other`) before the CLT that uses it.
- Delete: deploy a `destructiveChanges.xml` listing the type (`<members>flightResponse</members>`
  under `LightningTypeBundle`).
- Packaging: 1GP and 2GP managed packages support it. Source tracking works with `sf project` commands.

## Verify and discover

- **Setup → Quick Find "Lightning Types"**: lists standard and custom types. The **Source** column
  shows Standard or Custom. Click a label to see its schema, namespace and config. **New Lightning
  Type** creates one in the UI.
- **Connect REST API**: `GET /services/data/vXX.X/connect/lightning-types` lists the standard and
  custom types in the org (part of the Type System resources).
