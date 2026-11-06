# Composition File (`<widgetName>.json`)

## Envelope

```json
{
  "type": "lightning__agentforceWidget",
  "contentBody": {
    "widgetBody": {
      "definition": "tile/widget",
      "children": [
        { "definition": "tile/column", "attributes": { "gap": "md" }, "children": [ /* everything */ ] }
      ]
    }
  }
}
```

- `type` is always `lightning__agentforceWidget` — same value for every channel (Agentforce, Claude, ChatGPT, Slackbot).
- `contentBody.widgetBody` is the root and must be `tile/widget`.
- Label/description live in the `.uiwidget-meta.xml`, not here.

## Node shape

```ts
interface Node {
  definition: string                 // "tile/<name>"
  attributes?: Record<string, any>   // static values or {!...} expressions
  meta?: { if?: string; forEach?: string; forItem?: string; forIndex?: string }
  children?: Node[]                  // rendered in order
}
```
No `type` key on any node.

## Data binding

| Where | Syntax | Resolves to |
|---|---|---|
| Anywhere in the tree | `{!$attrs.name}` | `schema.json` → `properties.attributes.properties.name` |
| Nested object attr | `{!$attrs.owner.name}` | field of an object-typed attribute |
| Inside a `forEach` | `{!$opp.name}` | current item (loop var declared in `forItem`) |
| Index inside a loop | `{!$i}` | declared in `forIndex` |
| String interpolation | `"Total: {!$attrs.amount}"` | mixed literal + expression |
| Formula | `{!ROUND($attrs.score, 1)}` | see `formulas.md`. **Breaks in the MCP channel**, see below |

A widget **without** `schema.json` can only render static values.

> **MCP channel (Claude/ChatGPT/Slackbot): plain bindings only.** The wrapper CLT's renderer rewrites each plain `{!$attrs.x}`, including inside string interpolation, to `$attrs.outputValues.<payload>.x`. It leaves `$attrs` inside a formula untouched, and the render then fails. Any `IF(...)`, `BLANKVALUE(...)`, `TEXT(ROUND(...))` or comparison over `$attrs` is affected. Put labels, variants/colors, fallbacks and booleans in Apex and bind them plainly: `"label": "{!$attrs.statusLabel}"`, `"variant": "{!$attrs.statusVariant}"`, `"color": "{!$attrs.probabilityColor}"`. Semantic attribute values (variants, colors) can themselves be bound. Verified in Claude web, 2026-09-21.

## meta — conditional rendering

```json
{ "definition": "tile/callout", "meta": { "if": "{!$attrs.isAtRisk}" },
  "attributes": { "variant": "warning", "title": "At risk" } }
```
- Must evaluate to Boolean. Missing/null reference → `false`. String/number/array → evaluation error.
- Comparisons and logic like `{!AND($attrs.isAvailable, $attrs.price < 500)}` evaluate in scenarios A/B, but they are formulas and **break in the MCP channel**. For widgets rendered via MCP, compute the Boolean in Apex (`isOverdue`, `isAtRisk`) and bind it plainly.
- `false` removes the node **and its children**.

## meta — iteration

```json
{ "definition": "tile/row",
  "meta": { "forEach": "{!$attrs.openOpportunities}", "forItem": "$opp", "forIndex": "$i" },
  "children": [ { "definition": "tile/text", "attributes": { "text": "{!$opp.name}" } } ] }
```
- The node carrying `forEach` repeats (with its children). For a container of repeated items, put `forEach` on the child, not the container.
- `forItem` default is `$Item`; `forItem` and `forIndex` must start with `$`.
- Nested loops: inner `forEach` references the outer var (`{!$order.lines}`) and uses a different `forItem`.
- `if` + `forEach` on the same node:
  - condition references the loop var (`{!$opp.isWon}`) → evaluated **per item** (filter);
  - condition references only `$attrs` (`{!$attrs.showList}`) → evaluated **once** (show/hide whole list).

## Actions (buttons)

```json
{
  "definition": "tile/button",
  "attributes": {
    "label": "Open in Salesforce",
    "variant": "secondary",
    "actions": { "click": [ { "definition": "action/openLink", "attributes": { "url": "{!$attrs.recordUrl}" } } ] }
  }
}
```

| Action | Attributes | Behavior |
|---|---|---|
| `action/openLink` | `url` (required); `target` `_blank`/`_self` (per sf-skills) | Opens URL synchronously; no agent turn |
| `action/sendMessage` | `content` (required) | Sends text to the agent as if the user typed it (not shown to user); agent reasons and responds; may ask confirmation for risky actions |

A button without `actions.click` renders disabled. For `sendMessage` to do something useful, the agent/subagent (or MCP client LLM) must have the follow-up action available and instructions to handle that message.

## Layout & styling conventions

- Vertical groups → `tile/column`; same-line items → `tile/row` (`justify: "between"`, `align: "center"` for label/value rows); breathing room → `tile/spacer`; section boundary → `tile/separator`; bordered group → `tile/container`.
- Keep nesting shallow; nest row-in-column only when orientation changes.
- Typography through `tile/text` `variant` (`h1`–`h4`, `body`, `caption`), `weight`, `color` (`muted`, `primary`, …).
- One `h1` per widget; use `h2`/`h3` for cards.
- Semantic variants on stateful components (`tile/badge`, `tile/callout`: `info`/`success`/`warning`/`error`).
- Accept defaults for `gap`/`size` unless there's a reason.
- Icons: names from the `lightning__iconName` list (Lucide-style) — see `components.md`.
- Images: URL must be reachable **without authentication**. For MCP channels, add the image domain as a Trusted URL in Setup (CSP is auto-provisioned for the MCP server).

## Workflow tip

Prototype in HXL Playground (https://www.headlessexperiencelayer.com → Widgets → New widget), toggle the preview across Agentforce/Slackbot/ChatGPT, then paste the JSON into `<widgetName>.json`. Playground widgets live in browser local storage — use **Share** links as backup.
