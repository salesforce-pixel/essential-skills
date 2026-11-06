# Data SDK API reference

Sources: `data-sdk-usage`, `data-sdk-intro`, `data-sdk-connect`. GraphQL operation detail is in `graphql-operations.md`.

The Data SDK (`@salesforce/platform-sdk/data`) handles auth, CSRF tokens and base-path resolution. It detects the runtime surface and its capabilities, ships full TypeScript types, and uses Promises (try/catch) instead of events.

```typescript
import { createDataSDK, gql } from "@salesforce/platform-sdk/data";
import type { DataSDK, SDKOptions, NodeOfConnection } from "@salesforce/platform-sdk/data";
const dataSdk = await createDataSDK();
```

## Exports

| Export | Kind | Description |
|---|---|---|
| `createDataSDK` | async function | Factory for a DataSDK instance |
| `gql` | template tag | Inline GraphQL; enables editor highlighting and codegen detection |
| `DataSDK` | interface | `apiVersion?`, `graphql?`, `fetch?` |
| `SDKOptions` | interface | Base options with optional `surface` override |
| `GraphQLRequest` | interface | Raw request: `query`, `variables`, `operationName`, `headers` |
| `GraphQLResponse<T>` | interface | Raw envelope: `data`, `errors?` |
| `GraphQLRawDocument` | type alias | `string` (type of `query`/`mutation`) |
| `GraphQLRequestHeaders` | type alias | `HeadersInit` |
| `QuerySubscriber<T>` | type alias | Callback for `QueryResult.subscribe()`; receives `QuerySnapshot<T>` |
| `NodeOfConnection<T>` | utility type | Node type from an `edges { node }` connection |

## `createDataSDK(options?)`

```typescript
async function createDataSDK(options?: DataSDKOptions): Promise<DataSDK>;
```

**DataSDKOptions**

| Property | Type | Description |
|---|---|---|
| `surface` | `Surface` | Override auto-detection: `WebApp`, `Micro-Frontend`, `OpenAI` |
| `webapp` | `WebAppDataSDKOptions` | Web-app surface options (React/Angular) |
| `extensions` | `ExtensionsFor<DataSDK>` | Extensions attached as `sdk.ext.<name>` (see `platform-sdk-extras.md`) |

**WebAppDataSDKOptions**

| Property | Type | Description |
|---|---|---|
| `basePath` | `string` | Base URL prefix for API calls, e.g. `/services/data/v64.0` |
| `apiVersion` | `string` | e.g. `64.0`; used in the resolved `ui-api`, `graphql` and CSRF paths. Default: the runtime's default version |
| `onStatus` | `Partial<Record<number, () => Promise<unknown> \| void>>` | Per-HTTP-status callbacks, e.g. `{ 401: () => reauthenticate() }` |

**Cache sharing**: all instances that resolve to the same base URL and API version share one GraphQL cache (updates from one are visible to the others). Different API versions get isolated caches.

```typescript
const sdk1 = await createDataSDK();
const sdk2 = await createDataSDK();
await sdk1.graphql?.query<AccountData>({ query: GET_ACCOUNTS }); // populates cache
await sdk2.graphql?.query<AccountData>({ query: GET_ACCOUNTS }); // cache hit
const sdk3 = await createDataSDK({ webapp: { apiVersion: "63.0" } });
await sdk3.graphql?.query<AccountData>({ query: GET_ACCOUNTS }); // isolated cache, miss
```

## `gql`

Required for inline TypeScript queries: the SDK processes `gql` documents at several lifecycle stages, and it enables org-aware highlighting in Agentforce Vibes. Never use a plain template string.

```typescript
const MY_QUERY = gql`
  query MyQuery {
    uiapi { ... }
  }
`;
```

## Interfaces

```typescript
interface DataSDK {
  readonly apiVersion?: string; // resolved version, e.g. "64.0"; absent on unversioned surfaces
  graphql?: DataSDKGraphQL;
  fetch?: typeof fetch;
}

interface DataSDKGraphQL {
  // Resolves { data, errors, subscribe, refresh } from cache (cached surfaces) or network.
  query<T, V = Record<string, unknown>>(options: QueryOptions<V>): Promise<QueryResult<T>>;
  // Pass-through to transport; never reads or writes the cache.
  // Queries/subscriptions passed here are rejected via the resolved errors field.
  mutate<T, V = Record<string, unknown>>(options: MutateOptions<V>): Promise<MutationResult<T>>;
}

interface GraphQLRequest<V = Record<string, unknown>> {
  query: string;
  variables?: V;
  operationName?: string;
  headers?: GraphQLRequestHeaders;
}

interface GraphQLResponse<T> {
  data: T;
  errors?: GraphQLError[];
}

interface QueryOptions<V = Record<string, unknown>> {
  query: string;
  variables?: V;
  operationName?: string;
  cacheControl?: CacheControl;
  headers?: GraphQLRequestHeaders;
}

interface MutateOptions<V = Record<string, unknown>> {
  mutation: string;
  variables?: V;
  operationName?: string;
  headers?: GraphQLRequestHeaders;
}

type GraphQLRequestHeaders = HeadersInit; // object, [name, value][] or Headers

interface QuerySnapshot<T> {
  data: T | undefined;
  errors?: GraphQLError[];
}

interface QueryResult<T> extends QuerySnapshot<T> {
  subscribe(cb: QuerySubscriber<T>): Unsubscribe; // later resolutions (cache updates, refresh)
  refresh(): Promise<void>;                       // re-issue, bypass cache, notify subscribers
}

type QuerySubscriber<T> = (snapshot: QuerySnapshot<T>) => void;

interface MutationResult<T> {
  data: T | undefined;
  errors?: GraphQLError[];
}

interface GraphQLError {
  message: string;
  locations?: { line: number; column: number }[];
  path?: string[];
  extensions?: Record<string, unknown>; // server extensions passed through verbatim; SDK sets code "CACHE_MISS"
}

type Unsubscribe = () => void;
type CacheControl = "no-cache" | "only-if-cached" | { type: "max-age"; maxAge: number };
```

## `fetch()` for REST

Use `dataSdk.fetch?.()` only for REST endpoints GraphQL doesn't cover (Apex REST `/services/apexrest/...`, `/services/data/v{version}/...`). The wrapper handles CSRF, base path, 401/403 hooks, and language/locale. When the runtime has an active language it adds `Accept-Language` to REST requests (your own value is preserved).

```typescript
const dataSdk = await createDataSDK();

// Prefer GraphQL for record/user data
const me = await dataSdk.graphql?.query({
  query: gql`
    query {
      uiapi {
        currentUser {
          Id
          Name { value }
        }
      }
    }
  `,
});

// REST only where GraphQL doesn't reach. Replace {version}, e.g. 67.0
const res = await dataSdk.fetch?.("/services/data/v{version}/ui-api/records/{recordId}");
const userData = await res?.json();
```

Use `fetch?.()` (optional chaining), not `fetch!.()`, especially in shared or cross-surface utilities.

### Data-access order of preference

1. GraphQL `dataSdk.graphql?.query()` / `mutate()` (POST to Salesforce GraphQL).
2. UI API or other Salesforce REST via `sdk.fetch?.()` (`/services/data/v{version}/ui-api/*`, Apex REST).
3. GraphQL GET via `sdk.fetch?.()` when a GET is required (small query/variables that fit in the URL, or a dependency on a CSRF round trip).
4. Apex REST for custom logic GraphQL can't express.
5. **Never** call `fetch()` or `axios` directly for Salesforce endpoints.

## Endpoints

`v{version}` = e.g. `v66.0`.

| Endpoint | Purpose | Internal | External |
|---|---|:-:|:-:|
| `/services/apexrest/*` | Custom Apex REST | ✓ | ✓ |
| `/services/data/v{version}/graphql` | GraphQL API | ✓ | ✓ |
| `/services/data/v{version}/ui-api/records` | UI API records | ✓ | ✓ |
| `/services/data/v{version}/ui-api/search-info` | Search suggestions/scope | ✓ | ✓ |
| `/services/data/v{version}/ui-api/layout` | Layouts | ✓ | ✓ |
| `/services/data/v{version}/ui-api/session/csrf` | CSRF token | ✓ | ✓ |
| `/services/data/v{version}/ui-api/*` | Other UI API | ✓ | ✓ |
| `/services/data/v{version}/chatter/*` | Chatter Connect API | ✓ | ✓ |
| `/services/data/v{version}/chatter/users/me` | Running user's profile | ✓ | ✓ |
| `/services/data/v{version}/chatter/users/{userId}` | A user's profile | ✓ | ✓ |
| `/sfsites/c/_nc_external/system/security/session/SessionTimeServlet` | Remaining session time | ✓ | ✓ |
| `/secur/logout.jsp` | Logout | ✓ | ✓ |
| `/services/data/v{version}/connect/file/upload/config` | File upload settings | ✓ | ✓ |
| `/services/data/v{version}/connect/proxy/ui-telemetry` | Client telemetry | ✓ | ✓ |
| `/services/data/v{version}/connect/*` | Connect REST API (files, feeds, communities, …) | ✓ | |
| `/services/data/v{version}/connect/cms/delivery/channels/{channelId}/contents` | Published CMS content from a channel | | ✓ |
| `/services/data/v{version}/connect/cms/channels/{channelId}/searchable-content-types` | Searchable CMS content types | | ✓ |

Any Connect REST API family (Data 360, CRM Analytics, Industries, …) can be reached; check that feature's reference docs. The recipes repo (`trailheadapps/multiframework-recipes`) has Chatter, Apex REST and UI API REST examples.

## `NodeOfConnection<T>`

```typescript
import { type NodeOfConnection } from "@salesforce/platform-sdk/data";
type AccountNode = NodeOfConnection<GetHighRevenueAccountsQuery["uiapi"]["query"]["Account"]>;
```

Use it for `edges { node }` responses to get a clean node type for transforms, props and list rendering. Not needed for flat types.

## What's not available (vs LWC)

Only standard web APIs and npm packages. Unsupported: `@salesforce/*` scoped modules (except `@salesforce/platform-sdk/...`), Lightning base components and `lightning/*` modules, `@wire`.

| LWC-only | Multi-Framework replacement |
|---|---|
| `@salesforce/apex/Class.method` | `dataSdk.fetch?.()` to `/services/apexrest/...` |
| `@salesforce/schema/Object.Field` | Hard-code the API name in the GraphQL query |
| `@salesforce/user/Id`, `/CurrentUserId` | GraphQL `uiapi.currentUser` |
| `lightning/uiRecordApi` `getRecord`, `getListUi`, … | `dataSdk.graphql?.query(...)` |
| `lightning/uiRecordApi` `createRecord`/`updateRecord`/`deleteRecord` | `dataSdk.graphql?.mutate(...)` |
| `@wire` | React `useEffect` + `graphql?.query(...)`; `QueryResult.subscribe` for reactive updates |
| `@salesforce/label/c.X` | `labels` extension: `sdk.ext.labels.get?.()` / `getAll?.()` |

## Surface support

| Capability | WebApp | Micro-Frontend | OpenAI |
|---|:-:|:-:|:-:|
| GraphQL queries | ✅ | ✅ | ✅ |
| GraphQL mutations | ✅ | ✅ | ✅ |
| Response caching (`cacheControl`) | ✅ | ✅ | ❌ |
| `fetch()` for REST | ✅ | ✅ | ❌ |
| `apiVersion` on instance | ✅ | ✅ | ❌ |
| Per-request `headers` | ✅ | ✅ | ❌ |
| `webapp` options | ✅ | ✅ | ❌ |

On `OpenAI`, GraphQL is uncached: `subscribe()` only gets new snapshots when you call `refresh()`. On WebApp/Micro-Frontend it also gets cache-driven updates. Always use optional chaining (`sdk.graphql?.`, `sdk.fetch?.`) for portability.

Further reading linked from the docs but not captured here: `data-sdk-skills.md` ("Use Skills for Data Access").
