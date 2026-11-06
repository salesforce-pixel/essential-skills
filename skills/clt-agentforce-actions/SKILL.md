---
name: clt-agentforce-actions
description: >-
  Build Custom Lightning Types (CLTs) that replace the default Agentforce chat UI for an
  agent action's input or output with your own Lightning Web Components — the
  LightningTypeBundle (schema.json + per-channel editor.json / renderer.json), the Apex
  classes the type projects from, the LWC (lightning__AgentforceInput /
  lightning__AgentforceOutput targets, valuechange event, getFormattedValue global copy),
  and wiring the type to the action (Input/Output Rendering, Agent Script
  complex_data_type_name, is_displayable). Also covers object-based CLTs, collection
  renderers, property-level editors and layouts, channels (lightningDesktopGenAi,
  enhancedWebChat, lightningMobileGenAi, experienceBuilder), namespaces, custom labels,
  deploy/package.xml, safe-change rules, and citations in Apex actions. TRIGGER when the
  user mentions CLT, custom Lightning type, LightningTypeBundle, lightningTypes folder,
  schema.json / editor.json / renderer.json, @apexClassType, lightning__objectType,
  componentOverrides, $attrs, Input Rendering / Output Rendering, a custom card/form/list
  for agent action input or output, or a CLT deploy/validation error. DO NOT TRIGGER for
  HXL widgets (@widget/c/…, UiWidgetBundle, MCP tool UI — use hxl-widget-builder), writing
  Agent Script beyond the action parameter wiring (use agentscript), or generic LWC work
  unrelated to agent actions.
metadata:
  version: "1.0"
---

<!--
Changelog
1.0 — Initial version (2026-11-06). Built from 17 Salesforce doc pages (Agentforce
      Developer Guide lightning-types*, global-copy, citations; Lightning Types Developer
      Guide; Metadata API LightningTypeBundle) and forcedotcom/sf-skills
      platform-custom-lightning-type-generate. Sources tracked by tools/doc-refresh
      (see references/sources.md).
-->

# Custom Lightning Types for Agentforce Actions

A **Lightning type** is a JSON-Schema-based data type that defines the shape of the data,
how it's validated, and how it's displayed. Every agent action input/output is already
mapped to a **standard** type (`lightning__textType`, `lightning__dateType`, …), and each
standard type has a default editor (input UI) and renderer (output UI). A **custom
Lightning type (CLT)** lets you replace those defaults with your own LWC so the agent
shows a branded card, list or form instead of a raw dump of fields.

```
Apex @InvocableMethod ──► output/input Apex class (global, @JsonAccess, @AuraEnabled fields)
                                │  "lightning:type": "@apexClassType/c__MyClass"
                                ▼
lightningTypes/<typeName>/schema.json            ← data shape (projected from Apex)
lightningTypes/<typeName>/<channel>/renderer.json ← output UI → c/myRendererLwc
lightningTypes/<typeName>/<channel>/editor.json   ← input UI  → c/myEditorLwc
                                │
                                ▼
Agent action parameter → Output Rendering / Input Rendering = <typeName>
  (Agent Script: complex_data_type_name: "c__<typeName>")
```

**Hard limit:** you can override the UI **only for agent actions whose input or output is
an Apex class.** Flow, prompt-template and standard actions keep the default UI.

## Choose the right kind

| Need | Use | Where it works |
|---|---|---|
| Custom UI for an **Agentforce agent action** | **Apex-based CLT** — `"lightning:type": "@apexClassType/c__Class"` | Employee agent (Lightning Experience + mobile), Service agent via Enhanced Chat v2 (web + mobile) |
| Lightweight structure with no Apex, for **Prompt Builder**, **Experience Builder**, Flow structured outputs | **Object-based CLT** — `"lightning:type": "lightning__objectType"` + `properties` | Experience Builder (`experienceBuilder` editor only), Prompt Builder, Flows |
| A declarative HXL widget card (also renders in Claude/ChatGPT/Slackbot via MCP) | Root-level `renderer.json` with `@widget/c/…` | Use [`hxl-widget-builder`](../hxl-widget-builder/SKILL.md) |

Apex-based types **aren't supported in Experience Builder**; object-based types aren't the
agent-action path. This skill is mostly about the Apex-based path.

## Required inputs

Gather or infer before generating:

1. **The action's Apex class** and which parameter to customize — **output** (renderer),
   **input** (editor), or both. Note whether the output is a single object or a **list**
   (list → collection renderer).
2. **Channel(s)**: `lightningDesktopGenAi` (Employee agent, Lightning Experience — default),
   `enhancedWebChat` (Service agent, Enhanced Chat v2), `lightningMobileGenAi` (both, on
   mobile). Each channel needs its own copy of `editor.json` / `renderer.json`.
3. **Type name** (folder name, camelCase, e.g. `flightResponse`) — this becomes
   `c__flightResponse` everywhere it's referenced.
4. **Namespace**: always `c` for metadata in this org/package, even in a namespaced org;
   the package namespace (`isv/…`, `isv__…`) only for metadata installed from another
   managed package.

If the request is clear, generate immediately — don't over-ask.

## Workflow

1. **Shape the Apex** to the CLT rules (details: [references/apex-and-actions.md](references/apex-and-actions.md)):
   - Every class the type references is **`global`**, **top-level** (own file), annotated
     `@JsonAccess(serializable='always' deserializable='always')`, and every field the UI
     needs is **`@AuraEnabled`** (plus `@InvocableVariable` on the action's request/response wrapper fields).
   - Supported field types: primitives (Integer, Double, Long, Date, Datetime, Time,
     String, ID, Boolean), sObjects, lists, `Map<String, …>`, user-defined classes.
   - **If the agent action already exists, delete and recreate it after changing the Apex
     to meet these rules** — otherwise the change isn't registered.
2. **Write `schema.json`** — for Apex-based types, *only* these three keys:
   ```json
   { "title": "Flight Response", "description": "Available flights", "lightning:type": "@apexClassType/c__AvailableFlight" }
   ```
   No `$schema`, `type`, `properties`, `required` or `unevaluatedProperties` — the schema
   is **projected** from the class's `@AuraEnabled` members at runtime. `title` /
   `description` may be custom labels: `"{!$Label.c.FlightTitle}"`.
   Object-based schemas: [references/bundle-and-schema.md](references/bundle-and-schema.md).
3. **Write the UI override** in `lightningTypes/<type>/<channel>/` (details:
   [references/ui-overrides.md](references/ui-overrides.md)):
   - Output, single object → `renderer.json`:
     `{"renderer":{"componentOverrides":{"$":{"definition":"c/flightDetails"}}}}`
   - Output, list → collection renderer:
     `{"collection":{"renderer":{"componentOverrides":{"$":{"definition":"c/hotelDetails"}}}}}`
   - Input → `editor.json`:
     `{"editor":{"componentOverrides":{"$":{"definition":"c/flightRequestFilter"}}}}`
4. **Build the LWC**:
   - Renderer: target `lightning__AgentforceOutput`; receives the whole object (or the
     array, for collections) in `@api value`.
   - Editor: target `lightning__AgentforceInput`; `@api value` + `@api readOnly`; on every
     change dispatch `new CustomEvent('valuechange', { detail: { value: {...} } })` and
     `event.stopPropagation()` on the inner input event. **The agent can't pre-populate
     `value`** — the editor only captures user input, sent on submit.
   - Optional: `@api getFormattedValue()` returning plain text or HTML enables the chat's
     **copy** button for the component (see ui-overrides.md).
5. **Validate locally**, then deploy: `python3 -I scripts/validate_clt.py <project-or-force-app-dir>`
   (this skill's folder). Deploy order: **Apex → LWC → LightningTypeBundle**
   (or all in one deploy). Check-only first:
   ```bash
   sf project deploy start --dry-run --source-dir force-app --target-org <alias>
   sf project deploy start --source-dir force-app --target-org <alias>
   ```
   Confirm in **Setup → Lightning Types** (Source column = Custom).
6. **Wire it to the action**:
   - **Builder / Setup:** open the agent action → for the output, edit **Output Rendering**
     (enable *Show in conversation*) → select the CLT; for the input, edit **Input
     Rendering** → select the CLT → Save.
   - **Agent Script:** on the action parameter set
     `complex_data_type_name: "c__<typeName>"` (replacing the default
     `"@apexClassType/c__Class"`), keep the parameter type `object` (`list[object]` for
     lists), set **`is_displayable: True`** on outputs (required to show a CLT) and
     `is_user_input: True` on inputs the user fills in. Script validation fails if the type
     name doesn't exist in the org. See [references/apex-and-actions.md](references/apex-and-actions.md#wire-the-type-to-the-agent-action).
   - Tell the subagent instructions to collect the input through the form — the LLM may
     otherwise ask for it as text.
7. **Test**: Agentforce Builder → Preview → run an utterance → check the custom form/card
   renders. Then **Commit Version** and **Activate** (after committing, changes need a new draft).

Full working examples (Flight editor + renderer, Hotel collection renderer):
[references/worked-examples.md](references/worked-examples.md). Deployable copy of the
Flight example: [`templates/`](templates/README.md).

## Critical rules

- **Bundle layout:** `lightningTypes/<type>/schema.json` (required) + optional
  `<channel>/editor.json` and/or `<channel>/renderer.json`. Channel folder names are exact:
  `lightningDesktopGenAi`, `enhancedWebChat`, `lightningMobileGenAi`, `experienceBuilder`.
  `renderer.json` isn't supported in `experienceBuilder`. A root-level `renderer.json`
  (no channel folder) is **only** for HXL widgets.
- **Namespace:** `c/` for LWC definitions and `c__` for type/class references created in
  this org or this package; `<ns>/`, `<ns>__` only for another installed package.
- **LWC target must match the role** or the deploy fails ("Invalid target configuration"):
  editor → `lightning__AgentforceInput`, renderer → `lightning__AgentforceOutput`,
  Experience Builder / object-type property editor → `lightning__PropertyEditor`.
- **Keys:** use `componentOverrides` and `layout`. `propertyRenderers` and `view` are
  legacy keys and get rejected.
- **`$` vs property name:** `$` = override the whole type; a property name (e.g.
  `"lastName"`) = override that property only, defaults render the rest.
- **Apex-based type + `attributes` mapping:** prefer `$` with **no `attributes`**, so the LWC
  reads everything from `@api value`. The docs show `{!$attrs.field}` mapping on Apex types, but
  sf-skills reports it is rejected (`unevaluatedProperties`) because the Apex schema has no
  `properties` block. If you map anyway, check-only deploy first. When you map, **every** LWC
  property must be mapped, even if the names match.
- **Breaking changes:** never rename/delete a referenced Apex class, change a field's type,
  remove a used `@AuraEnabled` field, or downgrade `global` → `public`. Adding fields is
  safe. Object-based rules: [references/bundle-and-schema.md](references/bundle-and-schema.md#safe-changes).
- **Delete** a CLT with a `destructiveChanges.xml` listing `LightningTypeBundle:<type>`.

## Common errors

| Symptom | Cause | Fix |
|---|---|---|
| `Invalid target configuration. To use 'c/x' as a renderer/editor, your js-meta.xml file must include valid target …` | LWC missing `lightning__AgentforceOutput` / `…Input` | Add the target matching the role |
| Schema rejected: unknown keyword / `unevaluatedProperties` | Extra keys (`$schema`, `type`, `properties`, `examples`, `items`) or `attributes` on an Apex-based type | Apex schema = `title`, `description`, `lightning:type` only; drop `attributes` |
| Agent Script validation fails on `complex_data_type_name` | CLT not deployed or wrong name (`title` instead of folder name, missing `c__`) | Deploy the bundle; use `c__<folderName>` |
| Default UI still shows | Output Rendering/Input Rendering not set; `is_displayable` not `True`; wrong channel folder for the surface you test in; action created before Apex met the rules | Set rendering; add the channel folder; delete + recreate the action |
| Editor submits nothing / stale values | LWC doesn't dispatch `valuechange` with `detail.value` | Dispatch on every change with the full object |
| Agent asks for the input as chat text | Instructions don't steer to the form | Tell the subagent to collect it through the action's input form |
| Runtime failure in namespaced org / package | Class `public`, nested, or missing `@JsonAccess` | `global`, top-level, `@JsonAccess(serializable='always' deserializable='always')` |
| Renderer shows empty | Field not `@AuraEnabled`; LWC reading wrong path (`value.flights` vs `value`) | Annotate; log `JSON.stringify(this.value)` in Preview |

## References

- [references/bundle-and-schema.md](references/bundle-and-schema.md) — bundle structure,
  channels, Apex vs object schemas, standard types + constraints, namespaces, labels,
  safe-change rules, package.xml, deploy/delete, Setup page, Connect API.
- [references/ui-overrides.md](references/ui-overrides.md) — editor.json / renderer.json /
  collection, property-level overrides, layouts, attribute mapping, LWC contracts, global copy.
- [references/apex-and-actions.md](references/apex-and-actions.md) — Apex class rules,
  schema projection, wiring in Builder and Agent Script, citations (`AiCopilot.GenAiCitationInput/Output`).
- [references/worked-examples.md](references/worked-examples.md) — Flight (editor +
  renderer) and Hotel (collection renderer), end to end.
- [references/sources.md](references/sources.md) — tracked source URLs and known doc inconsistencies.
- [`templates/`](templates/README.md) — deployable Flight example (Apex, LWCs, two CLTs, package.xml).
- `scripts/validate_clt.py` — static checks for a `lightningTypes` folder and the LWCs it references.

Related skills: [`agentscript`](../agentscript/SKILL.md) (action syntax),
[`hxl-widget-builder`](../hxl-widget-builder/SKILL.md) (widget renderers),
[`afagent-metadata-helper`](../afagent-metadata-helper/SKILL.md) (moving agents between orgs).
