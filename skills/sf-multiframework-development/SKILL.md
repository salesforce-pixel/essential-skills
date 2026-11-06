---
name: sf-multiframework-development
description: Build, run, deploy and package Salesforce Multi-Framework apps — React/Angular SPAs deployed as UIBundle metadata (uiBundles/, ui-bundle.json, .uibundle-meta.xml) that read and write Salesforce data through the Data SDK (@salesforce/platform-sdk). TRIGGER when the user mentions Multi-Framework, UIBundle, the reactinternalapp/reactexternalapp/angularinternalapp/angularexternalapp/reactbasic templates, *.salesforce.app, createDataSDK, gql, graphql.query/mutate, cacheControl, graphql:codegen, Data SDK extensions or labels, getCurrentApp, View SDK, platform-sdk i18n, styling a React app on Salesforce (SLDS, shadcn), CSP for scripts in a UIBundle, ACC in a React UIBundle, or embedding a UIBundle with lightning-ui-embedding. DO NOT TRIGGER for LWC or Aura components, @wire/lightning/* work, LWR sites without a UIBundle, ACC in standalone non-Salesforce apps or lightning/accApi (use agentforce-conversation-client), or externally hosted React apps using their own OAuth.
metadata:
  version: "1.0"
---

<!--
Changelog
1.0 — Imported into essential-skills (2026-11-06) from the personal
      ~/.claude/skills copy. Doc sources tracked by tools/doc-refresh.
-->

# Salesforce Multi-Framework development

Multi-Framework is a framework-agnostic runtime: a React or Angular SPA, built with standard tooling (Vite / Angular CLI), deployed as a **UIBundle** metadata component in a Salesforce DX project. It gets platform SSO, and its data requests go through UI API, which enforces OLS, FLS, sharing and validation rules on the server.

This skill digests the official guide (32 pages, fetched 2026-10-21). Generated projects also ship an `AGENT.md`, and Salesforce publishes its own changing skills library (`npx skills add forcedotcom/sf-skills`). If those are installed, follow them first; use this skill as the consolidated reference.

## Pick the app type first

| | Internal (B2E) | External (B2C / B2B) |
|---|---|---|
| Users | Employees, Salesforce login (SSO) | Customers/partners via Experience Cloud (guest or authenticated) |
| Templates | `reactinternalapp`, `angularinternalapp` | `reactexternalapp`, `angularexternalapp` |
| Extra metadata | CustomApplication (`uiBundle` = `c__AppName`) + `<AppName> Access` permset | DigitalExperience, DigitalExperienceConfig, Network, CustomSite |
| bundle `<target>` | `CustomApplication` (default) | `Experience` |
| Opens from | App Launcher → `*.salesforce.app` in a new tab | Site URL (App Launcher opens the site in a new tab) |
| Prebuilt | ACC, object search | Navigation, auth, object search |
| 3rd-party JS | Must be bundled | Bundled or static resource |
| 2GP packaging | ✅ unlocked / managed | ❌ unsupported |

To add an app to an existing DX project instead, use `sf template generate ui-bundle --name X --template reactbasic|angularbasic`, and supply the CustomApplication or site metadata yourself.

Choose **LWC** instead for reusable components that live natively inside Lightning pages. Multi-Framework is for self-contained full-page apps; to put one inside a Lightning page you need UI Embedding (Beta).

## Workflow

1. **Org setup** (once): Enterprise/Performance/Unlimited/Developer/Partner Developer edition on **Hyperforce** only. Enable the **Salesforce app domain** (Setup → *Salesforce Multi-Framework Apps* → Enable Domain, if the button shows) and **Salesforce Edge Network** (My Domain → Routing and Policies). External apps also need Digital Experiences and community licences. → `references/setup-and-project.md`
2. **Scaffold**: `sf template generate project --name MyApp --template reactinternalapp`
3. **Install inside the bundle dir**: `cd force-app/main/default/uiBundles/MyApp && npm install`. Run all npm scripts from here, never from the project root.
4. **Run**: `npm run dev` → `http://localhost:5173` (`SF_UIBUNDLE_PORT` to change it). For Live Preview with org data: `sf plugins install @salesforce/plugin-ui-bundle-dev`, then *SFDX: Open in Live Preview*.
5. **Data**: `npm run graphql:schema` → write `.graphql` operations → `npm run graphql:codegen` → call through the Data SDK. → `references/data-sdk-api.md`, `references/graphql-operations.md`
6. **Test**: `npm run test` (Vitest or `ng test`); `npm run build:e2e` then `npx playwright test` (React) / `npm run e2e` (Angular). No org needed. → `references/lifecycle.md`
7. **Build and deploy**: `npm run build` (must produce `outputDir`, default `dist`), then `sf project deploy start --source-dir force-app` so the CustomApplication or site metadata goes with it.
8. **Grant access**: `sf org assign permset --name MyApp_Access` (deploying doesn't assign it), plus object/field access to the data the app uses.

## Rules for writing code

- **All Salesforce calls go through the Data SDK.** Never use raw `fetch`/`axios` against Salesforce endpoints. Order of preference: `dataSdk.graphql?.query/mutate` → `dataSdk.fetch?.()` for UI API / Connect / Apex REST (`/services/apexrest/...`) → Apex REST for custom logic.
- **Optional chaining everywhere**: `sdk.graphql?.`, `sdk.fetch?.`, `viewSDK.displayToast?.`, `sdk.ext.labels.get?.`. Members are absent on surfaces that don't support them, and the SDK factories don't throw for that.
- **Operations are `gql`-tagged or imported `.graphql?raw` files.** Never plain strings. Always pass the response (and variables) generic: `query<GetXQuery, GetXQueryVariables>`.
- **UI API shape**: reads are `uiapi { query { Obj(first, after, where, orderBy) { edges { node { Id Field { value } } } } } }`; every field is `{ value, displayValue }`. Writes are `uiapi { ObjCreate|ObjUpdate|ObjDelete(input: $input) { Record { Id ... } } }`, and Delete returns only `Id`.
- **Mutations never touch the cache.** After a write, call `queryResult.refresh()`, re-query with `cacheControl: "no-cache"`, or update optimistically and refresh on failure.
- **Default query cache is 300 s max-age.** The cache key is `{query, variables, operationName, headers}`, so unique per-call headers (trace ids) defeat caching. Partial responses (data + errors) are never cached.
- **Check `errors` even when `data` is present.** Choose strict, tolerant or fail-only-without-data. Branch on `errors[i].extensions.code` (e.g. `CACHE_MISS`), not on message text.
- **No LWC imports**: no `@salesforce/apex|schema|user|label/*`, no `lightning/*`, no `@wire`, no base components. The mapping table is in `references/data-sdk-api.md`.
- **No external `<script src>`.** The CSP blocks it, and Trusted URLs or Experience Builder CSP settings don't help. Bundle the library and everything it loads, or (external apps only) use static resources at `SITE/PREFIX/sfsites/c/resource/NAME`.
- **SPAs need `"routing": { "fallback": "index.html" }`** in `ui-bundle.json`, or deep-link refreshes return 404.
- **Don't edit generated files** such as `schema.graphql`. Regenerate them.
- A bundle holds at most **2,500 files**.

## Minimum API versions

| Feature | Min API |
|---|---|
| `labels` Data SDK extension | 64.0 |
| 2GP packaging (`sourceApiVersion` in `sfdx-project.json`) | 67.0 |
| i18n (`fetchI18nContext`, formatters, `SalesforceBackend` labels) | 68.0 |

`ui-bundle.json` `apiVersion` (`"vXX.X"`) should match the target org, or be omitted to use the org default.

## Troubleshooting

| Symptom | Check |
|---|---|
| App not in App Launcher | bundle `target` = `CustomApplication`; CustomApplication `uiBundle` = `c__App`; permset assigned or profile visible; deployed with `isActive` true |
| App opens, but no or partial data, no error | User lacks object/field access (separate from app visibility). Also check API Enabled |
| Deep link 404 on refresh | `routing.fallback: "index.html"` |
| Third-party script blocked | CSP: bundle it or use a static resource (external only) |
| ACC won't render or keep a session | Employee Agent + Agentforce pref; untick *Require first-party use of Salesforce cookies*; add the origin (incl. `localhost:5173`) to Trusted Domains for Inline Frames, type Lightning Out |
| `identity` / `bundleId` undefined | Normal in local dev; guard and fall back |
| Labels render as raw keys | Org below API 68 (i18next backend) or 64 (`labels` ext); label missing from `labelManifest` |
| `createDataSDK()` rejects | An extension's `minApiVersion` is above the resolved API version (none get attached) |
| New package version not served after upgrade | Upgrades don't overwrite `IsActive`; activate manually |
| Can't edit the external site in Experience Builder | By design; edit the metadata |

## References (load as needed)

- `references/setup-and-project.md`: concepts, org setup, templates, quick start, folder tree, full `ui-bundle.json` and `.uibundle-meta.xml` reference, internal/external metadata, AGENT.md, sf-skills, Salesforce DX MCP config, dev server and Live Preview.
- `references/data-sdk-api.md`: `createDataSDK` options, every interface and type, the `fetch` wrapper, the supported endpoint table (internal vs external), LWC → Multi-Framework mapping, the surface support matrix (WebApp / Micro-Frontend / OpenAI).
- `references/graphql-operations.md`: query/mutate parameters, inline vs `.graphql` + codegen, fragments, full create/update/delete code, refresh-after-mutation patterns, error strategies, cache control, per-request headers.
- `references/platform-sdk-extras.md`: extensions (`labels`, `defineDataExtension`, aliases, `minApiVersion`), `getCurrentApp()`, View SDK (toast, alert, modal, navigate, dirty state, UI state, theme, resize, events), i18n and the i18next `SalesforceBackend`.
- `references/styling-libraries-acc.md`: SLDS blueprints, design-system-react, shadcn/Tailwind `global.css` theming, lightning-card → shadcn Card conversion, CSP rules, ACC org setup and the React `embedAgentforceClient` component.
- `references/lifecycle.md`: testing, deploy and versioning, App Manager, access grants, microfrontend embedding, 2GP packaging (sourcemaps, `sf code-analyzer run --rule-selector uibundle`, Tooling API verification).
- `references/sources.md`: the 32 source URLs, and **known inconsistencies in the official docs** (mangled generics, `createAccWidget` vs `embedAgentforceClient`, import-path drift, `getTheme` shape, and others). Read it before copying a sample that looks wrong.

Working examples: <https://github.com/trailheadapps/multiframework-recipes>.
