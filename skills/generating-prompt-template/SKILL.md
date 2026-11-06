---
name: generating-prompt-template
description: "Author, generate, and validate Salesforce GenAiPromptTemplate metadata (Einstein/Agentforce Prompt Templates) as deployable .genAiPromptTemplate-meta.xml files. TRIGGER when the user wants to create/build/author/edit a Prompt Template, a Flex/Sales Email/Field Generation/Record Summary/Case Email prompt template, write prompt template metadata, add inputs or data providers (Apex/Flow grounding) to a template, or scaffold genAiPromptTemplates for deployment. Covers template types, input definition URIs (primitive://, SOBJECT://), merge/reference expressions ({!$Input:...}, {!$Apex:X.Prompt}, {!$Flow:X.Prompt}), models, visibility, versioning, and package.xml. DO NOT TRIGGER when: invoking/calling an existing template from Apex (use calling-prompt-templates-apex), building an Agentforce agent .agent file (use developing-agentforce), or authoring a Flow/Apex class that a template merely references (use generating-flow / generating-apex)."
metadata:
  version: "1.0"
---

<!--
Changelog
1.0 — Imported into essential-skills (2026-11-06) from the personal
      ~/.claude/skills copy. Doc sources tracked by tools/doc-refresh.
-->

# Generating Prompt Templates (GenAiPromptTemplate)

Author deployable **Prompt Template** metadata for Einstein / Agentforce Prompt Builder. The
output is a `*.genAiPromptTemplate-meta.xml` file under `force-app/main/default/genAiPromptTemplates/`.

This skill covers **authoring the template metadata itself**. To *call* an existing template
from Apex, use `calling-prompt-templates-apex`. To author the Apex class or Flow that a template
grounds on, use `generating-apex` / `generating-flow`.

> Grounded in the Metadata API Developer Guide (`GenAiPromptTemplate`, API v60.0+, doc v262.0)
> and verified against real deployed templates.

---

## When to Use This Skill

- Create a new prompt template (Flex, Sales Email, Field Generation, Record Summary, Case Email Draft)
- Add **inputs** (record, field, or primitive) to a template
- Add **data providers** — ground a template on an Apex class or Flow
- Wire merge fields / reference expressions into the prompt body
- Validate or fix an existing `.genAiPromptTemplate-meta.xml`
- Scaffold the `package.xml` entry and deploy

**Prereqs in the org:** Prompt Builder enabled and the **Prompt Template Manager** permission.

---

## File Location & Naming

| | |
|---|---|
| **Suffix** | `.genAiPromptTemplate` (source files use `.genAiPromptTemplate-meta.xml`) |
| **Directory** | `force-app/main/default/genAiPromptTemplates/` |
| **API version** | 60.0 and later |
| **File name** | Must equal the template's API name, e.g. `Recommend_Relevant_Products.genAiPromptTemplate-meta.xml` |

The file name (minus suffix) **is** the `fullName`/`developerName`. Keep them identical.

---

## Top-Level Structure (`GenAiPromptTemplate`)

| Field | Type | Req | Notes |
|---|---|---|---|
| `developerName` | string | ✓* | API name. Match the file name. (Used in source format; corresponds to inherited `fullName`.) |
| `masterLabel` | string | ✓ | User-friendly name shown in Prompt Builder. |
| `description` | string | | Optional description. |
| `type` | string | ✓ | Template type — see table below. |
| `visibility` | enum | | `Global` or `API`. Default to `Global`. |
| `activeVersionIdentifier` | string | ✓* | `versionIdentifier` of the active version. Must point at a **Published** version. |
| `activeVersion` | int | | **Deprecated** (removed in 64.0). Use `activeVersionIdentifier`. |
| `relatedEntity` | string | | SObject the template is associated with (mainly Field Generation / Record Summary). |
| `relatedField` | string | | Field the template targets (Field Generation). |
| `templateVersions` | `GenAiPromptTemplateVersion[]` | ✓ | One or more versions (see below). |

\* In practice both `developerName` and `activeVersionIdentifier` are required for a usable,
deployable template.

### Template types (`type`)

| Value | Use for |
|---|---|
| `einstein_gpt__flex` | **Most common / general purpose.** Freeform prompt with any inputs + grounding. Use this unless a specialized type is explicitly needed. |
| `einstein_gpt__salesEmail` | Sales email drafting (Sender/Recipient inputs). |
| `einstein_gpt__fieldCompletion` | Field Generation — fill a specific `relatedField` on a `relatedEntity`. |
| `einstein_gpt__recordSummary` | Summarize a record. |
| `einstein_gpt__caseEmailDraft` | Draft a case email reply. |

---

## Version (`templateVersions` → `GenAiPromptTemplateVersion`)

| Field | Type | Req | Notes |
|---|---|---|---|
| `content` | string | ✓ | The prompt text. XML-escape `<`, `>`, `&`, `"` (use `&lt; &gt; &amp; &quot;`). Embed merge expressions — see below. |
| `status` | enum | ✓ | `Published` or `Draft`. The active version must be `Published`. **Published versions can't be edited via UI or Metadata API** — bump a new version to change content. |
| `versionIdentifier` | string | | Unique per version. Auto-generated on deploy/retrieve if omitted; if you set it, it must be unique. The active version's id goes in top-level `activeVersionIdentifier`. |
| `versionNumber` | int | | **Deprecated** (removed in 64.0). Use `versionIdentifier`. |
| `description` | string | | Version description. |
| `primaryModel` | string | | LLM for this version — see Models below. |
| `inputs` | `GenAiPromptTemplateInput[]` | | Parameters passed in — see below. |
| `templateDataProviders` | `GenAiPromptTemplateDataProvider[]` | | Apex/Flow grounding — see below. |
| `generationTemplateConfigs` | `GenAiPromptTemplateGenerationConfig[]` | | Policy refs (`generationConfigDeveloperName`). Rarely needed. |

---

## Inputs (`inputs` → `GenAiPromptTemplateInput`)

Each input is a parameter you reference in `content` as `{!$Input:<referenceName-suffix>}`.

| Field | Type | Req | Notes |
|---|---|---|---|
| `apiName` | string | ✓ | Parameter name, e.g. `Recipient`. |
| `definition` | string | ✓ | URI of the input's data type — see URIs below. |
| `referenceName` | string | ✓ | Expression handle, conventionally `Input:<apiName>`. |
| `required` | boolean | ✓ | `true` / `false`. |
| `masterLabel` | string | | Friendly label. |
| `description` | string | | Optional. |

### Input `definition` URIs

| URI | Meaning |
|---|---|
| `SOBJECT://Account` | A whole record of that SObject. Reference fields with dot paths: `{!$Input:Recipient.Name}`, `{!$Input:Recipient.Income__c}`. |
| `SOBJECT://Contact` | Standard or custom object record. |
| `SOBJECT://ContentDocument` | A file/image record (e.g. business-card image for multimodal). |
| `primitive://String` | Plain string scalar. Reference as `{!$Input:companyName}`. |
| `primitive://Boolean`, `primitive://Integer`, `primitive://Number`, etc. | Other primitives. |

---

## Data Providers — Grounding (`templateDataProviders` → `GenAiPromptTemplateDataProvider`)

Ground the prompt on live data from an **Apex** class or a **Flow**. Reference the returned text
in `content` with `{!$Apex:<name>.Prompt}` or `{!$Flow:<name>.Prompt}`.

| Field | Type | Req | Notes |
|---|---|---|---|
| `definition` | string | ✓ | `apex://ClassName` or `flow://FlowApiName`. |
| `referenceName` | string | ✓ | Expression handle, conventionally `Apex:ClassName` or `Flow:FlowApiName`. |
| `parameters` | `GenAiPromptTemplateDataProviderParam[]` | | Inputs passed to the provider. |

### Provider parameters (`parameters` → `GenAiPromptTemplateDataProviderParam`)

| Field | Type | Req | Notes |
|---|---|---|---|
| `parameterName` | string | ✓ | Name of the provider's input param. |
| `definition` | string | ✓ | URI of the param type, e.g. `SOBJECT://Contact`, `primitive://String`. |
| `isRequired` | boolean | ✓ | `true` / `false`. |
| `valueExpression` | string | | Value piped in, usually a template input: `{!$Input:Recipient}`. |

**Apex provider contract:** the class is an `@InvocableMethod` (or prompt-template-capable Apex)
returning a `Prompt` string. Author it with `generating-apex` if it doesn't exist yet.
**Flow provider contract:** an autolaunched Flow with a text output exposed as `.Prompt`.

---

## Merge / Reference Expressions (inside `content`)

| Expression | Resolves to |
|---|---|
| `{!$Input:companyName}` | A primitive input value. |
| `{!$Input:Recipient.Name}` | A field on a record input (dot traversal). |
| `{!$Input:Recipient.Financial_Goals__c}` | A custom field on a record input. |
| `{!$Apex:MyClass.Prompt}` | Grounding text returned by the Apex data provider. |
| `{!$Flow:My_Flow.Prompt}` | Grounding text returned by the Flow data provider. |

Remember `content` is inside XML — escape literal `{` JSON braces are fine, but escape `<`, `>`,
`&`, and `"` as entities.

---

## Models (`primaryModel`)

Use a standard model alias. Verified values seen in real orgs:

| Alias | Notes |
|---|---|
| `sfdc_ai__DefaultOpenAIGPT4` | GPT-4 class. |
| `sfdc_ai__DefaultOpenAIGPT4OmniMini` | GPT-4o-mini class, cost-efficient. |
| `sfdc_ai__DefaultGPT5Mini` | GPT-5-mini class. |

Omit `primaryModel` to use the org default. Model availability varies by org/region — if a deploy
rejects a model alias, query available models in the org or drop the tag.

---

## Worked Example 1 — Flex template with a primitive input + Apex grounding

```xml
<?xml version="1.0" encoding="UTF-8"?>
<GenAiPromptTemplate xmlns="http://soap.sforce.com/2006/04/metadata">
    <activeVersionIdentifier>Qt8GV/Q4xnRAm8SOP6MDIrOwFQOATLORaOIuqADi7lk=_1</activeVersionIdentifier>
    <developerName>AI_Perplexity_Risk_Analysis</developerName>
    <masterLabel>AI Perplexity Risk Analysis</masterLabel>
    <templateVersions>
        <content>Act as a Risk &amp; Regulatory Intelligence Analyst. Perform an external risk assessment.

Web Search Results:
{!$Apex:PerplexityRiskAssessment.Prompt}

Return only valid JSON. Company: {!$Input:companyName}</content>
        <inputs>
            <apiName>companyName</apiName>
            <definition>primitive://String</definition>
            <masterLabel>companyName</masterLabel>
            <referenceName>Input:companyName</referenceName>
            <required>true</required>
        </inputs>
        <primaryModel>sfdc_ai__DefaultOpenAIGPT4OmniMini</primaryModel>
        <status>Published</status>
        <templateDataProviders>
            <definition>apex://PerplexityRiskAssessment</definition>
            <parameters>
                <definition>primitive://String</definition>
                <isRequired>true</isRequired>
                <parameterName>companyName</parameterName>
                <valueExpression>{!$Input:companyName}</valueExpression>
            </parameters>
            <referenceName>Apex:PerplexityRiskAssessment</referenceName>
        </templateDataProviders>
        <versionIdentifier>Qt8GV/Q4xnRAm8SOP6MDIrOwFQOATLORaOIuqADi7lk=_1</versionIdentifier>
    </templateVersions>
    <type>einstein_gpt__flex</type>
    <visibility>Global</visibility>
</GenAiPromptTemplate>
```

## Worked Example 2 — Sales Email with record inputs + Flow grounding

```xml
<?xml version="1.0" encoding="UTF-8"?>
<GenAiPromptTemplate xmlns="http://soap.sforce.com/2006/04/metadata">
    <activeVersionIdentifier>a94ACO8feseESrBtllQUNLvKEqlCHiPSDLX5rXUnvPs=_1</activeVersionIdentifier>
    <developerName>Recommend_Relevant_Products</developerName>
    <description>Recommend relevant financial products to a client based on their needs</description>
    <masterLabel>Recommend Relevant Products</masterLabel>
    <relatedEntity>Contact</relatedEntity>
    <templateVersions>
        <content>You are a financial advisor at {!$Input:Sender.CompanyName}, name {!$Input:Sender.Name}.
Write an email to {!$Input:Recipient.Name} (age {!$Input:Recipient.Age__c}) recommending products.
Goals: {!$Input:Recipient.Financial_Goals__c}

{!$Flow:Fetch_Products.Prompt}

Be concise.</content>
        <inputs>
            <apiName>Sender</apiName>
            <definition>SOBJECT://User</definition>
            <referenceName>Input:Sender</referenceName>
            <required>true</required>
        </inputs>
        <inputs>
            <apiName>Recipient</apiName>
            <definition>SOBJECT://Contact</definition>
            <referenceName>Input:Recipient</referenceName>
            <required>true</required>
        </inputs>
        <primaryModel>sfdc_ai__DefaultOpenAIGPT4</primaryModel>
        <status>Published</status>
        <templateDataProviders>
            <definition>flow://Fetch_Products</definition>
            <parameters>
                <definition>SOBJECT://Contact</definition>
                <isRequired>true</isRequired>
                <parameterName>Recipient</parameterName>
                <valueExpression>{!$Input:Recipient}</valueExpression>
            </parameters>
            <referenceName>Flow:Fetch_Products</referenceName>
        </templateDataProviders>
        <versionIdentifier>a94ACO8feseESrBtllQUNLvKEqlCHiPSDLX5rXUnvPs=_1</versionIdentifier>
    </templateVersions>
    <type>einstein_gpt__salesEmail</type>
    <visibility>Global</visibility>
</GenAiPromptTemplate>
```

## Worked Example 3 — Multimodal (image / file input)

For vision use cases, take a `SOBJECT://ContentDocument` input:

```xml
        <inputs>
            <apiName>Image</apiName>
            <definition>SOBJECT://ContentDocument</definition>
            <referenceName>Input:Image</referenceName>
            <required>true</required>
        </inputs>
```

Use a vision-capable model (e.g. `sfdc_ai__DefaultGPT5Mini`) and instruct the model to read the
attached file in `content`.

---

## Deployment

### package.xml entry

```xml
<types>
    <members>*</members>          <!-- or a specific name, e.g. Recommend_Relevant_Products -->
    <name>GenAiPromptTemplate</name>
</types>
```

`GenAiPromptTemplate` supports the `*` wildcard. Use API version `60.0`+ in the manifest.

### Deploy commands

```bash
# Deploy a single template
sf project deploy start \
  --source-dir force-app/main/default/genAiPromptTemplates/Recommend_Relevant_Products.genAiPromptTemplate-meta.xml \
  --target-org <alias>

# Or via the manifest
sf project deploy start --manifest manifest/package.xml --target-org <alias>
```

For deployment troubleshooting and scratch-org/CI workflows, hand off to `deploying-metadata`.

---

## Authoring Checklist

1. **File name == `developerName` == `masterLabel`-derived API name.** All three aligned.
2. **`type` chosen** — default `einstein_gpt__flex` unless a specialized type is required.
3. **At least one `templateVersions`** with `status` and a non-empty `content`.
4. **Active version is `Published`**, and `activeVersionIdentifier` == that version's `versionIdentifier`.
5. **Every `{!$Input:X}`** in `content` has a matching `<inputs>` entry (and dot-fields exist on the SObject).
6. **Every `{!$Apex:X.Prompt}` / `{!$Flow:X.Prompt}`** has a matching `templateDataProviders` entry, and the Apex class / Flow actually exists and returns a `Prompt`.
7. **Provider `parameters`** each map a `parameterName` to a `valueExpression` (usually `{!$Input:...}`) with the right `definition` URI.
8. **`content` is XML-escaped** (`&lt; &gt; &amp; &quot;`).
9. **`primaryModel`** is a valid alias for the org, or omitted.
10. **package.xml** includes `GenAiPromptTemplate` at version ≥ 60.0.

---

## Gotchas

- **Published is immutable via API.** You cannot edit a `Published` version's `content` through
  Metadata API or UI. To change a live template, add a new version and repoint `activeVersionIdentifier`.
- **`versionIdentifier` is auto-generated** on first deploy/retrieve. When hand-authoring a brand-new
  template you may set a placeholder; safest is to deploy, retrieve, then read back the generated id
  and set it as `activeVersionIdentifier`.
- **Deprecated tags:** avoid `activeVersion` (int) and `versionNumber` (int) — both removed in API 64.0.
  Use `activeVersionIdentifier` and `versionIdentifier`.
- **Data-provider direction:** `valueExpression` flows a template *input* into the provider; the
  provider's returned text flows back into `content` via `{!$Apex:X.Prompt}` / `{!$Flow:X.Prompt}`.
- **Org prerequisites:** Prompt Builder must be enabled and the deploying user needs the
  **Prompt Template Manager** permission, or the deploy/activation fails.

---

## Reference

- Metadata API Developer Guide — `GenAiPromptTemplate`:
  https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_genaiprompttemplate.htm
- Related: `calling-prompt-templates-apex` (invoke a template from Apex),
  `developing-agentforce` (agents that use templates), `deploying-metadata` (deploy/CI).
