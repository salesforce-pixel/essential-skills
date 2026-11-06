# HXL Component Palette (Beta)

Beta components render on Agentforce, ChatGPT, Claude and Slackbot. The attribute names below are the **complete** lists from each component's official reference page, fetched 2026-09-21. The deploy rejects any other attribute name ("additionalProperties is set to false"), and `validate_hxl.py` enforces these lists (`component-attributes`).

Re-verify when in doubt. The pages are plain markdown, and `curl` works:
`curl -sL https://developer.salesforce.com/docs/platform/hxl/references/hxl-reference-about/<component>.md` → read the `## Properties` table. You can also use `getUiComponentSchemas` if the metadata MCP tool is available. Don't guess.

"Required" in the docs is not enforced by deploy (rows and columns without `gap`/`align` deploy and render fine), so the lists below are names only.

| Component | Definition | Use for | Attributes (complete) |
|---|---|---|---|
| Widget | `tile/widget` | Required root only | — |
| Column | `tile/column` | Vertical stack | `align`, `gap`, `width` |
| Row | `tile/row` | Horizontal stack | `align`, `gap`, `isWrapped`, `justify`. **Not** `wrap` (deploy fails) |
| Container | `tile/container` | Rounded-border group (children) | `borderless`, `variant` |
| Spacer | `tile/spacer` | Explicit space / flex fill | `size` |
| Separator | `tile/separator` | Divider line | `orientation` (`horizontal`/`vertical`) |
| Text | `tile/text` | Any text | `text`, `variant` (`h1`–`h4`,`body`,`caption`), `weight`, `color` (`default`,`muted`,`primary`,`success`,`warning`,`error`), `isItalic`, `isStrikethrough` |
| Markdown | `tile/markdown` | Rich prose (headings, lists, links, tables, code) | `source` |
| Badge | `tile/badge` | Status/category chip | `label`, `variant` (`secondary` default, `primary`, `outline`, `info`, `success`, `warning`, `error`) |
| Callout | `tile/callout` | Emphasized block | `title` (req), `description`, `variant` (`default`,`info`,`note`,`tip`,`success`,`warning`,`error`), `iconAlt`. Put body text in `description` |
| Icon | `tile/icon` | Standalone icon | `name`, `size`, `color` (`default`,`muted`,`primary`,`success`,`warning`,`error`), `alt` |
| Image | `tile/image` | Image | `src`, `alt` (a11y), `size` |
| Avatar | `tile/avatar` | Person/entity | `src`, `initials`, `iconName`, `alt`, `shape`, `size` |
| Link | `tile/link` | Hyperlink | `href` (req), `text`, `underline`, `variant`. **Not** `url`/`label` |
| Button | `tile/button` | Action trigger | `label`, `variant` (`primary`,`secondary`,`destructive`…), `iconName`, `actions` |
| List | `tile/list` | Column of items (children `tile/listItem`) | `marker` |
| List Item | `tile/listItem` | One list row | children only: `tile/text`, `tile/link`, `tile/icon` |
| Accordion | `tile/accordion` | Expandable sections | children `tile/accordionItem` |
| Accordion Item | `tile/accordionItem` | One section | `title`, `subtitle`, `iconName`, `iconAlt`, `isExpanded` |
| Progress | `tile/progress` | Completion % | `value` (0–100, or toward `max`), `max`, `label` (req), `size` (req), `color` (`default`,`primary`,`success`,`warning`,`error`), `shape` (`linear`/`circular`) |
| Spinner | `tile/spinner` | Loading indicator | `label`, `size` |
| Code | `tile/code` | Preformatted code | `code`, `language` |
| Table | `tile/table` | Tabular data | `columns`, `rows`, `caption`, `appearance`, `isStickyHeader`, `pagination`, `size`, `sort`. Column types below |

Verified rendering in Claude web (2026-09-21): row, column, container, text, icon, badge, callout, progress, separator, button (openLink + sendMessage).

**Dev Preview** (Playground only, API may change → sandbox only): e.g. `tile/card` (seen in docs with `padding`, `variant`, `maxWidth`) and interactive inputs. Prefer `tile/container` + `tile/column` for a card look in production.

## Shared enum types

| Type | Values (default **bold**) |
|---|---|
| `lightning__gapType` | none, xs, sm, **md**, lg, xl |
| `lightning__sizeType` | xs, sm, **md**, lg, xl |
| `lightning__extentType` | **auto**, xs, sm, md, lg, xl, full, stretch |
| `lightning__alignmentType` (cross-axis) | start, center, end, **stretch** |
| `lightning__justifyType` (main-axis) | **start**, center, end, between, around, evenly (+ `space-*` aliases) |
| `lightning__orientationType` | **horizontal**, vertical |
| `lightning__positionType` | **top**, right, bottom, left |
| `lightning__textalignType` | **left**, center, right |
| `lightning__severityType` | **info**, success, warning, error |

## Table column types (`tile/table`)

| Column type | Key props |
|---|---|
| `{ "type": "date" }` | `format` `date`/`datetime`, `dateStyle`, `timeStyle` (`full`/`long`/`medium`/`short`); ISO strings or epoch ms |
| `{ "type": "number" }` | `format` `decimal`/`percent`/`currency`, `currencyCode` (ISO 4217, default USD), `currencyCodeKey` (per-row), `currencyDisplayAs`, `min/maximumFractionDigits`; row values = raw numeric strings |
| `{ "type": "link" }` | `urlKey` (row field with the URL; else cell value is both text and URL) |
| `{ "type": "picklist" }` | `options: [{label, value}]` |

Cell values: string (≤255 chars) or number. Unparseable values fall back to plain text. Confirm the exact `columns`/`rows` attribute names in the Table reference page before first use.

## Icon names (`lightning__iconName`)

activity, alert-circle, alert-triangle, align-center, align-horizontal-space-between, align-left, align-right, align-vertical-space-between, bell, bookmark, box, braces, briefcase, building, calculator, calendar, caret-down, caret-left, caret-right, caret-up, check, check-circle, chevron-down, chevron-left, chevron-right, chevron-up, circle, circle-dot, clock, cloud, code, component, copy, credit-card, crown, database, dashboard, divide, dollar-sign, dot, download, edit, equal, equal-not, eye, eye-off, file, file-edit, file-text, filter, folder, gauge, git-branch, git-compare, globe, grid, hash, headset, heart, help-circle, home, image, inbox, info, layers, layout, lightbulb, lightning, link, list, list-checks, list-checks-rtl, loader, lock, mail, map, map-pin, maximize, megaphone, message, microphone, minus, minus-circle, mouse-pointer-click, open-in-new, package, palette, pencil, phone, plane, plus, plus-circle, plug, refresh, repeat, rotate-ccw, rotate-cw, search, send, server, settings, share, shield, shield-alert, shield-check, shopping-cart, space, square, square-dashed, star, sticky-note, table, tag, target, television, thumb-down, thumb-up, ticket, toggle-left, trash, trending-up, upload, user, user-circle, users, video, wifi, x, x-circle

## Channel caveats

- Slackbot: HXL widgets don't render when the MCP server returns **Block Kit** — use the standard MCP Apps path.
- Rendering is native per channel, so spacing/typography differ slightly across Agentforce, Claude, ChatGPT and Slack. Preview all targets in the Playground.
