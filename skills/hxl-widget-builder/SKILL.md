---
name: hxl-widget-builder
description: Build Salesforce Headless Experience Layer (HXL) widgets end to end — UiWidgetBundle (composition JSON, schema.json, uiwidget-meta.xml), the custom Lightning types (CLTs) and renderer.json that feed them, the Apex invocable action behind them, and the McpServerDefinition wiring that renders them in Claude, ChatGPT and Slackbot. Use this skill whenever the user mentions HXL, Headless Experience Layer, UiWidgetBundle, uiWidgets, tile/* components, "@widget/c/", rich UI or cards for Agentforce action output, rendering MCP tool output as UI, MCP Apps from Salesforce, or wants a card/widget/rich response for an Agentforce agent or a Salesforce hosted MCP server — even if they don't say "HXL" explicitly.
license: MIT
metadata:
  version: "0.2"
---
<!--
Changelog
0.2 (2026-09-21) Lessons from a real end-to-end build (Apex → widget → MCP → Claude web):
  - MCP channel: formulas over $attrs break at render time; the widget must use plain bindings only, with display values computed in Apex. Templates rewritten this way.
  - tile/row has no `wrap` (it is `isWrapped`); tile/link is href/text. Component attribute lists refreshed from the official docs.
  - Deployed widget schema.json is additive-only.
  - Editing or re-adding an MCP tool in Setup wipes <uiResource>; clients cache tools and widgets (reconnect needed).
  - Validator adds component-attributes, mcp-plain-bindings and mcp-ui-resource checks. A check-only deploy is now part of validation.
0.1 Initial version.
-->

# HXL Widget Builder

HXL widgets are declarative JSON UI compositions (`tile/*` components) that Salesforce renders natively in Agentforce (Lightning Experience) and in MCP Apps–compatible clients (Claude, ChatGPT, Slackbot). A widget never fetches data itself: a **custom Lightning type (CLT)** describes the data, and the CLT's `renderer.json` maps that data into the widget's **attribute contract** (`schema.json`).

```
Data source (Apex / Flow / Prompt) ──► CLT schema.json (data shape)
                                         │ renderer.json maps data → widget attrs
                                         ▼
                        UiWidgetBundle: schema.json (UI contract) + <name>.json (composition)
```

HXL is **Beta** (API 67.0+). Treat everything here as subject to change; when a doc page and this skill disagree, the doc page wins.

## Step 0 — Pick the scenario (decides everything downstream)

| Scenario | Trigger phrases | CLTs | Renderer binding | Reference |
|---|---|---|---|---|
| **A. Standalone widget** | "build a widget/card", no data source named | none yet | n/a | `references/composition.md` |
| **B. Agentforce action output** | agent action, Agentforce Builder, "Show in conversation" | **1 Apex-based CLT** (`@apexClassType/...`) | direct: `{!$attrs.field}` | `references/lightning-types.md` |
| **C. MCP tool output** (Claude/ChatGPT/Slackbot) | MCP server, MCP tool, outputValues | **2 object-based CLTs**: result wrapper + payload, both tagged `mcp` | nested: `{!$attrs.outputValues.<payloadProp>.<field>}` | `references/lightning-types.md` + `references/mcp-channel.md` |

If B vs C is unclear, ask one question. B and C can coexist for the same Apex class and the same widget — the widget schema is identical; only the CLTs differ.

## Step 1 — Resolve the data shape before writing any UI

Never invent fields. Source of truth, in priority order:
1. **Deployed invocable action describe** (if an org alias is available): `sf api request rest '/services/data/v67.0/actions/custom/apex/<ClassName>' -o <alias>` — use `outputs` only.
2. **Local Apex class**: top-level response = `@InvocableVariable` fields; inner/referenced classes = `@AuraEnabled` public fields.
3. **User-provided JSON sample or field list** (scenario A).

If no shape is resolvable, stop and ask. Print a short build plan (files, field list, scenario) before writing files.

## Step 2 — Author the widget bundle (all three files, same step)

Path: `<packageDir>/main/default/uiWidgets/<widgetName>/` where `<packageDir>` is the default entry in `sfdx-project.json` (dropping `main/default` is the #1 layout bug).

| File | Must contain |
|---|---|
| `<widgetName>.json` | `{"type":"lightning__agentforceWidget","contentBody":{"widgetBody":{"definition":"tile/widget","children":[...]}}}` |
| `schema.json` | root `title`, `"type":"object"`, `properties.attributes` with `"lightning:type":"lightning__objectType"` and a `properties` map; every leaf has `lightning:type` |
| `<widgetName>.uiwidget-meta.xml` | `<UiWidgetBundle>` with `<masterLabel>`, `<description>`, `<widgetType>JSON</widgetType>` |

Start from `templates/widget/`. Read `references/composition.md` before composing and `references/components.md` for the component palette. Read `references/formulas.md` (MCP caveat first) before writing any formula.

Composition rules that bite:
- First child of `tile/widget` should be one `tile/column`; put everything inside it.
- Bind with `{!$attrs.x}`; inside `meta.forEach` use the loop variable (`{!$opp.name}`), never `{!$attrs.list.name}`.
- `forItem` / `forIndex` must start with `$`; default item var is `$Item`; nested loops need distinct names.
- `meta.if` must evaluate to a real Boolean. Bind a `lightning__booleanType` attr computed in Apex (`{!$attrs.isOverdue}`). A comparison expression is a formula and breaks in scenario C.
- Every `tile/button` needs `attributes.actions.click[]` with `action/openLink` (`url`) or `action/sendMessage` (`content`), otherwise it renders disabled.
- Style semantically (`variant`, `gap`, `size`, `color: muted`) — no pixels, no hex colors. One `h1` max, one `primary` button per group.
- No `type` key on any node. Only the envelope has `type`.
- Prefer Beta components from `references/components.md`; Dev Preview components (e.g. `tile/card`, inputs) → sandbox only, and tell the user.
- Widget `schema.json` stays **flat** in scenario C — never reproduce `outputValues` inside it.
- **Scenario C (MCP): plain bindings only.** No `$attrs` reference inside a formula (`IF`, `BLANKVALUE`, `TEXT(ROUND(...))`, comparisons). The wrapper renderer rewrites plain `{!$attrs.x}`, and string interpolation like `"Due {!$attrs.closeDate}"`, to `$attrs.outputValues.<payload>.x`. It does **not** rewrite `$attrs` inside formulas, so the tool call fails in the client with an error that quotes the formula. Compute labels, colors/variants, fallback text and booleans in Apex (Step 4) and bind them plainly. Verified in Claude web, 2026-09-21. Scenario B may tolerate formulas, but plain bindings work in both scenarios, so default to them.
- **Only use attribute names from the component's official list.** Unknown attributes fail the deploy ("additionalProperties is set to false"). Examples: `tile/row` wraps with `isWrapped` (not `wrap`); `tile/link` uses `href`/`text`. Attributes marked "Required" in the docs are not enforced (rows without `gap` deploy fine).
- **A deployed widget's `schema.json` is additive-only.** Removing a property fails with "Schema update contains breaking changes: You can't delete …". Leave obsolete attributes declared (and mapped) and just stop binding them.

To confirm component attributes, use (in order):
1. `execute_metadata_action` (Salesforce metadata MCP), if available: `discoverUiComponents` / `getUiComponentSchemas` (`metadataType: "FRAGMENT"`, `parameters.pageType: "FRAGMENT"`).
2. The official reference page as raw markdown. Plain `curl` works: `curl -sL https://developer.salesforce.com/docs/platform/hxl/references/hxl-reference-about/<component>.md` (e.g. `row`, `progress`). Read its `## Properties` table.
3. `references/components.md`, last refreshed 2026-09-21. Suggest a Playground check for anything unverified.

## Step 3 — Wire the CLT(s)

Follow `references/lightning-types.md` exactly. Non-negotiables:
- `renderer.json` sits at the **root** of the CLT folder, parallel to `schema.json`. Never in `lightningDesktopGenAi/` (that's the LWC-override pattern) and never in `editor.json`.
- `componentOverrides["$"].definition` = `@widget/c/<widgetName>` — always `c`, even in namespaced orgs.
- Renderer attribute **keys** = widget schema attribute names; **values** = CLT property paths.
- Scenario C: renderer goes on the **wrapper** CLT only; payload CLT has no renderer; both CLTs have `"lightning:tags":["mcp"]`, `"unevaluatedProperties": false`, `lightning__objectType`; wrapper's `outputValues` is typed `c__<payloadCltName>`.
- Never create/edit these CLTs in Setup → Lightning Types. DX project + CLI only.

## Step 4 — Apex (when the data comes from Apex)

Use `templates/apex/AccountHealthService.cls` as the pattern: `global` class, `@InvocableMethod` returning `List<Response>`, response has `@InvocableVariable` holding an inner class whose fields are `@AuraEnabled`. Include a test class for production deploys.

The Apex owns the presentation logic the widget can't safely do in MCP. Add display fields next to the raw ones:
- formatted labels (`amountLabel` = "USD 1.85M", `closeDateLabel` = "2026-09-18 · 3 days overdue");
- semantic tokens (`statusVariant` = `warning`/`success`, `probabilityColor`);
- booleans for `meta.if` (`isOverdue`);
- fallback text in place of `BLANKVALUE` ("Unassigned").

After deploying, invoke the action once via REST to confirm its output before wiring the client:
```bash
echo '{"inputs":[{"<inputVar>":"<value>"}]}' > <scratch>/inv.json
sf api request rest '/services/data/v67.0/actions/custom/apex/<ClassName>' -X POST -b "@<scratch>/inv.json" -o <alias>
```

## Step 5 — Validate (run it; don't describe it)

```bash
python3 <skill-root>/scripts/validate_hxl.py <project-root-or-force-app-path>
```

Report every check by name (pass / fail / warn). Fix all FAILs before deploying. Never claim "validated" without running the script. It also checks `mcpServerDefinitions/*` if present: `<uiResource>` ↔ `<resourceName>`, and `resourceUri` → wrapper CLT.

Then run a **check-only deploy**. It catches schema rejections the static script can't (unknown attributes, breaking schema changes, CLT type errors) and changes nothing in the org:
```bash
sf project deploy validate -x <manifest> -o <alias>    # add -l RunSpecifiedTests -t <TestClass> when Apex is included
```

## Step 6 — Deploy in order

```bash
sf project deploy start --metadata ApexClass:<Class> --target-org <alias>        # 1. data source
sf project deploy start --metadata UiWidgetBundle:<widget> --target-org <alias>  # 2. widget
sf project deploy start --metadata LightningTypeBundle:<clt> --target-org <alias> # 3. CLTs (payload before wrapper)
```
Or one `package.xml` (see `templates/package.xml`) — Metadata API orders a single deploy correctly. To delete a widget, use `destructiveChanges.xml`.

Then:
- **Scenario B**: Setup → Agentforce Assets → Actions → action → edit output → **Show in conversation** → **Output Rendering** = the CLT → save → reload the agent.
- **Scenario C**: follow `references/mcp-channel.md` (Setup MCP server → retrieve `McpServerDefinition` → add `<resources>` + `<uiResource>` → deploy → Activate → ECA → connect client).
  - The Apex class must be deployed **before** the admin can pick it as a tool in Setup.
  - After deploying the server definition, re-retrieve it and diff it against what you sent.
  - Warn the user: **editing, removing or re-adding the tool in Setup wipes `<uiResource>`** (and resets `readOnly`/`idempotent`). The client then shows a plain markdown table instead of the widget. If that happens, retrieve, diff, re-add `<uiResource>` and redeploy.
  - After any widget or server change, the client must **disconnect and reconnect** the connector and start a new chat. Clients cache the tool list and the UI resource. An error that quotes an expression you already removed means a stale cache, not bad code: retrieve the org's widget to prove it.
  - The widget has rendered when the client shows the card with its badges, bars and buttons. A markdown table with the same data means the tool ran but no UI resource was attached.

## Step 7 — Hand-off summary

List files written, validator + check-only deploy results, deploy commands, and the manual Setup steps still required, including the "don't edit the tool in Setup" and "reconnect after changes" warnings for scenario C. Point to `references/troubleshooting.md` if rendering fails.

## Reference index

| File | Read when |
|---|---|
| `references/composition.md` | Writing `<widgetName>.json` — envelope, meta (if/forEach), actions, layout/styling |
| `references/components.md` | Choosing components and their attributes; enum values; icon names |
| `references/formulas.md` | Any `{!...}` beyond a plain field reference (read the MCP caveat first) |
| `references/lightning-types.md` | Scenario B or C — CLT schemas, renderer.json, Apex→lightning:type mapping |
| `references/mcp-channel.md` | Scenario C — MCP server metadata, org and client setup |
| `references/troubleshooting.md` | Deploy errors, blank widgets, stale renders |
| `templates/` | Starting points for every file type |
