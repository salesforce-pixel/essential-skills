# Sources and known doc inconsistencies

Built on 2026-10-21 from the Salesforce Multi-Framework Developer Guide. Every page is served as Markdown at `https://developer.salesforce.com/docs/platform/multiframework/guide/<slug>.md`, including pages whose public link ends in `.html`. Use `curl -sL <url>` to re-check a page; the docs change often.

| # | Slug | Topic | Reference file |
|---|---|---|---|
| 1 | `multiframework-overview` | Concepts, UIBundle, internal vs external, app domain, vs LWC | setup-and-project |
| 2 | `mfw-setup` | Org prerequisites, app domain, CMS MCP, ACC setup | setup-and-project, styling-libraries-acc |
| 3 | `mfw-quick-start` | 10-minute React quick start | setup-and-project |
| 4 | `mfw-generate-app` | Templates, `sf template generate` | setup-and-project |
| 5 | `mfw-project-structure` | Folder tree, `.uibundle-meta.xml`, `ui-bundle.json`, internal/external metadata | setup-and-project |
| 6 | `mfw-agentic-tools` | AGENT.md, `forcedotcom/sf-skills`, Salesforce DX MCP | setup-and-project |
| 7 | `mfw-preview` | Dev server, Live Preview | setup-and-project |
| 8 | `mfw-styling` | SLDS blueprints, SLDS for React, shadcn/Tailwind | styling-libraries-acc |
| 9 | `mfw-third-party-libraries` | CSP, bundling vs static resources | styling-libraries-acc |
| 10 | `reactdev-acc` | Agentforce Conversation Client in React | styling-libraries-acc |
| 11 | `data-sdk-usage` | Data SDK index page | data-sdk-api |
| 12 | `data-sdk-intro` | Data SDK exports, interfaces, preferences, LWC mapping, surfaces | data-sdk-api |
| 13 | `data-sdk-connect` | Supported REST/Connect endpoints | data-sdk-api |
| 14 | `data-sdk-query` | `query()` parameters, response shape, subscribe/refresh | graphql-operations |
| 15 | `data-sdk-mutate` | `mutate()` parameters, response shapes | graphql-operations |
| 16 | `data-sdk-graphql` | Inline vs `.graphql`, codegen, fragments, do/don't | graphql-operations |
| 17 | `data-sdk-graphql-mutation` | Create/update/delete walkthroughs, refresh patterns | graphql-operations |
| 18 | `data-sdk-graphql-error` | Error strategies, transport/HTTP errors, `extensions.code` | graphql-operations |
| 19 | `data-sdk-cache-control` | Cache values, TTL, cache key | graphql-operations |
| 20 | `data-sdk-request-headers` | Default and per-request headers | graphql-operations |
| 21 | `data-sdk-extension` | Extensions concept | platform-sdk-extras |
| 22 | `data-sdk-extension-label` | `labels` extension | platform-sdk-extras |
| 23 | `data-sdk-extension-custom` | `defineDataExtension` | platform-sdk-extras |
| 24 | `data-sdk-identity` | `getCurrentApp()` | platform-sdk-extras |
| 25 | `data-sdk-view` | View SDK | platform-sdk-extras |
| 26 | `data-sdk-i18n` | i18n context, formatters, i18next backend | platform-sdk-extras |
| 27 | `mfw-lifecycle` | Lifecycle index | lifecycle |
| 28 | `mfw-testing` | Vitest/ng test, Playwright | lifecycle |
| 29 | `mfw-deploy` | Deploy, versioning, verify | lifecycle |
| 30 | `mfw-manage` | App Manager, permission sets, troubleshooting | lifecycle |
| 31 | `mfw-ui-embedding` | Microfrontends (Beta) | lifecycle |
| 32 | `mfw-packaging` | 2GP, sourcemaps, Code Analyzer, verification | lifecycle |

Linked from the docs but not captured: `data-sdk-skills` (Use Skills for Data Access), the Microfrontend guide, the ACC Developer Guide, the Metadata API `UIBundle` page, and the CLI reference for `template generate ui-bundle`.

Other resources: recipes repo <https://github.com/trailheadapps/multiframework-recipes>; official skills <https://github.com/forcedotcom/sf-skills>; launch blog "Build with React, Run on Salesforce" (developer.salesforce.com/blogs, 2026-04).

## Known inconsistencies in the source docs

The reference files show the corrected or safer form. Check against the installed package before relying on any of these.

1. **Mangled TypeScript generics** (Prettier artefacts): `useRef < HTMLDivElement > null` (reactdev-acc) and `(await dataSdk.graphql?.query) < CurrentUserQuery > { query }` (data-sdk-graphql, data-sdk-graphql-error). Correct forms: `useRef<HTMLDivElement>(null)` and `await dataSdk.graphql?.query<CurrentUserQuery>({ query })`.
2. **ACC entry point**: the prose says `createAccWidget`, but the code imports and calls `embedAgentforceClient`. Use `embedAgentforceClient`.
3. **Import paths vary**: the React list example imports `createDataSDK, gql` from `@salesforce/platform-sdk` (everywhere else it's `@salesforce/platform-sdk/data`). `defineDataExtension`, `getCurrentApp` and the View SDK come from `@salesforce/platform-sdk`. Check the package's `exports` map.
4. **`getTheme()`**: the method table says it returns `light`/`dark` (or `null`), but the examples read `theme.mode`. Treat it as an object with `.mode: ThemeMode`, and guard for both shapes if unsure.
5. **`only-if-cached` miss**: cache-control calls it a `DataNotFoundError`; error-handling shows `result.errors[0].extensions.code === "CACHE_MISS"`. Both agree it resolves rather than throws. Branch on `extensions.code`.
6. **`no-cache` wording**: described both as "skip the cache and always fetch fresh" and as "store, but revalidate before reuse". In practice the request goes to the server and the result is written back to the cache.
7. **`Accept-Language`**: data-sdk-intro says it's added to REST requests and that GraphQL response localisation isn't supported; request-headers says it's added to REST **and** GraphQL requests.
8. **Mutation file paths**: the comments say `src/api/account/query/createAccount.graphql`, but the imports use `./mutation/createAccount.graphql?raw`. Keep mutations in a `mutation/` folder and make the import match.
9. **Minimum API versions differ by feature**: `labels` extension 64.0; packaging `sourceApiVersion` 67.0; i18n runtime and `SalesforceBackend` labels 68.0. The `ui-bundle.json` example uses `v66.0`.
10. **Styling page**: says SLDS-for-React icons "you get via the `lightning-icon` LWC component. With shadcn, wrap your icon using `IconSettings`". The sample actually uses `IconSettings` from `@salesforce/design-system-react`.
11. **Typos in the source**: "namaly" (`mfw-generate-app`), "third-pary" (`mfw-third-party-libraries`).
