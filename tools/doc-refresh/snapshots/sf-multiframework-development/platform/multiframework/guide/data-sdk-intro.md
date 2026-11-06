# Work with Data SDK

The Data SDK handles authentication, CSRF tokens, and base path resolution internally. To work with Data SDK, import the functions from `@salesforce/platform-sdk/data`.

```javascript
import { createDataSDK, gql } from "@salesforce/platform-sdk/data";
import type { DataSDK, SDKOptions, NodeOfConnection } from "@salesforce/platform-sdk/data";
const dataSdk = await createDataSDK();
```

:::important
Data SDK doesn’t incur any API usage calls when used with Salesforce Multi-Framework apps that are hosted on Salesforce. However, Data SDK is subject to general limits like the number of records returned.
:::

## Data SDK Reference

Query and update Salesforce records extensively from your web app by using simple bindings for running GraphQL queries and mutations.

| Export                  | Type             | Description                                                                                                               |
| :---------------------- | :--------------- | :------------------------------------------------------------------------------------------------------------------------ |
| `createDataSDK`         | `async function` | Factory that creates a new DataSDK instance                                                                               |
| `gql`                   | template tag     | Identity template literal for inline GraphQL queries, which also enables editor syntax highlighting and codegen detection |
| `DataSDK`               | `interface`      | The SDK surface type with an optional `apiVersion` and `graphql` and `fetch` methods                                      |
| `SDKOptions`            | `interface`      | Base options type with optional surface override                                                                          |
| `GraphQLRequest`        | `interface`      | The raw GraphQL request shape (`query`, `variables`, `operationName`, and `headers`) sent to the transport                |
| `GraphQLResponse<T>`    | `interface`      | The raw GraphQL response envelope with `data` and optional `errors`                                                       |
| `GraphQLRawDocument`    | type alias       | The type of the `query` and `mutation` fields; an alias for `string`                                                      |
| `GraphQLRequestHeaders` | type alias       | Type of the per-request `headers` option; an alias for the standard `HeadersInit`                                         |
| `QuerySubscriber<T>`    | type alias       | The callback type passed to `QueryResult.subscribe()`; receives a `QuerySnapshot<T>`                                      |
| `NodeOfConnection<T>`   | utility type     | Extracts the node type from a GraphQL connection with edges and node response                                             |

## createDataSDK(options?)

Creates a new DataSDK instance.

```typescript
async function createDataSDK(options?: DataSDKOptions): Promise<DataSDK>;
```

### DataSDKOptions

| Property     | Type                     | Description                                                                                                                                                                                                            |
| :----------- | :----------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `surface`    | `Surface`                | Overrides the auto-detected surface. When set, the SDK uses this value instead of running surface detection. Supported values are `WebApp`, `Micro-Frontend`, and `OpenAI`. See [Data SDK Support](#data-sdk-support). |
| `webapp`     | `WebAppDataSDKOptions`   | Options specific to the web app surface, such as for React or Angular.                                                                                                                                                 |
| `extensions` | `ExtensionsFor<DataSDK>` | Extensions to attach as `sdk.ext.<name>`. See [Data SDK Extensions](/docs/platform/multiframework/guide/data-sdk-extension.md).                                                                                        |

### WebAppDataSDKOptions

| Property     | Type                                                      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| :----------- | :-------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `basePath`   | `string`                                                  | Base URL prefix for Salesforce API calls, for example `/services/data/v64.0`.                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `apiVersion` | `string`                                                  | Salesforce API version to target, for example `64.0`. The SDK uses this version in the resolved `ui-api`, `graphql`, and CSRF request paths. If omitted, the SDK uses the runtime environment's default API version.                                                                                                                                                                                                                                                                                                              |
| `onStatus`   | `Partial<Record<number, () => Promise<unknown> \| void>>` | Optional map of per-HTTP-status callbacks. The SDK calls the callback when a request gets a response with that status. Each callback receives no arguments and can be synchronous or asynchronous. The SDK waits for the callback, then completes the request with the original response. It doesn't retry the request. For example, pass `{ 401: () => window.location.reload() }` to reload the page when the session expires. See [Handle an Expired Session](/docs/platform/multiframework/guide/data-sdk-session-expiry.md). |

### Returns

```typescript
Promise<DataSDK>
```

The return type for `createDataSDK(options?)`, which resolves to a promise with the `DataSDK` object.

The [GraphQL cache](/docs/platform/multiframework/guide/data-sdk-cache-control.md) is shared across all DataSDK instances that target the same base URL and API version, which improves performance and consistency when multiple components query the same data. Multiple calls to `createDataSDK()` that resolve to the same base URL and API version share the same GraphQL cache, and cache updates from one SDK instance are visible to all other instances that share that cache. Instances that target different API versions get isolated caches, so a query response cached under one version is never served to an instance on another version.

```javascript
// Both instances resolve to the same base URL and API version,
// so they share the same GraphQL cache
const sdk1 = await createDataSDK();
const sdk2 = await createDataSDK();

// Query from sdk1 populates the cache
await sdk1.graphql?.query<AccountData>({ query: GET_ACCOUNTS });

// Query from sdk2 can read from the same cache (cache hit)
await sdk2.graphql?.query<AccountData>({ query: GET_ACCOUNTS });

// An instance on a different API version has an isolated cache,
// so this query does not hit the cache populated above
const sdk3 = await createDataSDK({ webapp: { apiVersion: "63.0" } });
await sdk3.graphql?.query<AccountData>({ query: GET_ACCOUNTS });
```

## gql Template Tag

The `gql` tag is a template literal for inline GraphQL query definitions. When GraphQL queries are defined with TypeScript code, the Data SDK requires the use of `gql` to understand and apply special processing to your GraphQL queries at different stages of the component lifecycle. The use of the `gql` tag enables org-aware GraphQL syntax highlighting when using Agentforce Vibes.

```javascript
import { createDataSDK, gql } from "@salesforce/platform-sdk/data";

const MY_QUERY = gql`
  query MyQuery {
    uiapi {
      ...
    }
  }
`;
```

See [GraphQL Queries in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql.md).

## DataSDK Interface

Defines the top-level SDK surface that exposes an optional API version along with optional GraphQL and fetch APIs. The `apiVersion`, `graphql`, and `fetch` members are all optional as they're supported in specific environments only.

```javascript
interface DataSDK {
  readonly apiVersion?: string;
  graphql?: DataSDKGraphQL;
  fetch?: typeof fetch;
}
```

- `apiVersion`: `string`—Read-only. The Salesforce API version the SDK resolved for the current environment, such as `64.0`. Set it with the `apiVersion` option on `createDataSDK()`. It's absent in environments that don't resolve to a versioned API path.

### graphql()

GraphQL is the preferred way to work with record data.

```javascript
import { createDataSDK } from "@salesforce/platform-sdk/data";
const dataSdk = await createDataSDK();
// GraphQL — use optional chaining
const result = await dataSdk.graphql?.query<MyQueryType>({
  query,
  variables,
});
```

To account for the lack of availability of GraphQL in some environments, use optional chaining (`graphql?`). See [GraphQL Queries in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql.md).

Pass options in several ways:

- Use `graphql.query()` based on the [QueryOptions Interface](#queryoptions-interface).
- Use `graphql.mutate()` based on the [MutateOptions Interface](#mutateoptions-interface).

### fetch()

Use `dataSdk.fetch?.()` for Salesforce REST endpoints that aren't covered by GraphQL. Use optional chaining to account for environments that don't support `fetch()`.

```javascript
import { createDataSDK } from "@salesforce/platform-sdk/data";
const dataSdk = await createDataSDK();
// Prefer GraphQL for record/user data:
const me = await dataSdk.graphql?.query({
  query: gql`
    query {
      uiapi {
        currentUser {
          Id
          Name {
            value
          }
        }
      }
    }
  `,
});

// Use fetch only for REST endpoints that GraphQL doesn't cover.
// Replace {version} with the API version you want to use, for example `67.0`.

// Example: UI API
const result2 = await dataSdk.fetch?.("/services/data/v{version}/ui-api/records/{recordId}");
const userData = await result2?.json();
```

The fetch wrapper handles:

- CSRF token management
- Base path resolution
- Per-status callbacks (`onStatus`), such as for an [expired session](/docs/platform/multiframework/guide/data-sdk-session-expiry.md)
- Language and locale preferences

:::note
When the runtime environment provides an active language, the SDK adds an `Accept-Language` header to REST requests so responses are localized. If you set `Accept-Language` yourself, the SDK preserves your value. Response localization for GraphQL isn't currently supported.
:::

Consider using the `dataSdk.fetch()` call for:

- Apex REST endpoints (e.g. /services/apexrest/auth/...)
- Salesforce REST endpoints (e.g. /services/data/v{version}/...)

## DataSDKGraphQL Interface

Defines the GraphQL methods available on the Data SDK, including queries and mutations.

```javascript
interface DataSDKGraphQL {
  /**
   * Runs a GraphQL query.
   *
   * Resolves with { data, errors, subscribe, refresh } once the underlying
   * request settles — either from the cache (cached surfaces only) or from
   * the network. subscribe() streams subsequent snapshots; refresh() re-issues
   * the request, bypassing the cache where one exists and propagating the
   * result to subscribers.
   */
  query<T, V = Record<string, unknown>>(options: QueryOptions<V>): Promise<QueryResult<T>>;

  /**
   * Runs a GraphQL mutation. Pass-through to the underlying transport — does
   * not read or write the cache. Queries and subscriptions passed here are
   * rejected via the resolved errors field.
   */
  mutate<T, V = Record<string, unknown>>(options: MutateOptions<V>): Promise<MutationResult<T>>;
}
```

## GraphQLRequest Interface

Describes the raw GraphQL request that the SDK sends to the transport. `QueryOptions` and `MutateOptions` are the method-specific options. `GraphQLRequest` is the underlying request shape they resolve to.

```javascript
interface GraphQLRequest<V = Record<string, unknown>> {
  query: string;
  variables?: V;
  operationName?: string;
  headers?: GraphQLRequestHeaders;
}
```

## GraphQLResponse Interface

Describes the raw GraphQL response envelope that the transport returns, before the SDK wraps it in a reactive [`QueryResult<T>`](#queryresultt-interface) or a [`MutationResult<T>`](#mutationresultt-interface).

```javascript
interface GraphQLResponse<T> {
  data: T;
  errors?: GraphQLError[];
}
```

## QueryOptions Interface

Describes the options for `graphql.query()`. See [GraphQL Query Parameters](/docs/platform/multiframework/guide/data-sdk-query.md).

```javascript
interface QueryOptions<V = Record<string, unknown>> {
  query: string;
  variables?: V;
  operationName?: string;
  cacheControl?: CacheControl;
  headers?: GraphQLRequestHeaders;
}
```

## MutateOptions Interface

Describes the options for `graphql.mutate()`. See [GraphQL Mutate Parameters](/docs/platform/multiframework/guide/data-sdk-mutate.md).

```javascript
interface MutateOptions<V = Record<string, unknown>> {
  mutation: string;
  variables?: V;
  operationName?: string;
  headers?: GraphQLRequestHeaders;
}
```

## GraphQLRequestHeaders

The type of the per-request `headers` option on `QueryOptions`, `MutateOptions`, and `GraphQLRequest`. It's an alias for the standard [`HeadersInit`](https://developer.mozilla.org/en-US/docs/Web/API/Headers), so you can pass a plain object, an array of `[name, value]` tuples, or a `Headers` instance.

```javascript
type GraphQLRequestHeaders = HeadersInit;
```

For more information, see [Per-Request Headers](/docs/platform/multiframework/guide/data-sdk-request-headers.md).

## QueryResult<T> Interface

Describes the reactive query result that's returned by `graphql.query()`. It extends [`QuerySnapshot<T>`](#querysnapshott-interface), so it carries the same `data` and `errors` fields and adds `subscribe()` and `refresh()`.

```javascript
interface QueryResult<T> extends QuerySnapshot<T> {
  subscribe(cb: QuerySubscriber<T>): Unsubscribe;
  refresh(): Promise<void>;
}
```

- `data`: `T | undefined`—The resolved query data, or `undefined` when the query didn't resolve data.
- `errors`: `GraphQLError[]`—Optional. Any GraphQL or transport errors.
- `subscribe(cb)`: `(cb: QuerySubscriber<T>) => Unsubscribe`—Registers a callback that receives a [`QuerySnapshot<T>`](#querysnapshott-interface) on each subsequent resolution. Returns an `Unsubscribe` function.
- `refresh()`: `() => Promise<void>`—Re-issues the underlying request and propagates the result to subscribers.

## QuerySubscriber<T>

The callback type passed to `QueryResult.subscribe()`. It receives a [`QuerySnapshot<T>`](#querysnapshott-interface) on each new resolution.

```javascript
type QuerySubscriber<T> = (snapshot: QuerySnapshot<T>) => void;
```

## MutationResult<T> Interface

Describes the one-shot result returned by `graphql.mutate()`.

```javascript
interface MutationResult<T> {
  data: T | undefined;
  errors?: GraphQLError[];
}
```

## QuerySnapshot<T> Interface

Describes the snapshot object passed to `subscribe()` callbacks.

```javascript
interface QuerySnapshot<T> {
  data: T | undefined;
  errors?: GraphQLError[];
}
```

## GraphQLError Interface

Defines the shape of GraphQL error objects returned by the Data SDK. See [Error Handling in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql-error.md).

```javascript
interface GraphQLError {
  message: string;
  locations?: { line: number, column: number }[];
  path?: string[];
  extensions?: Record<string, unknown>;
}
```

- `message`: `string`—The error message.
- `locations`: `{ line: number, column: number }[]`—Optional. Where in the query the error occurred.
- `path`: `string[]`—Optional. The response path to the field that errored.
- `extensions`: `Record<string, unknown>`—Optional. Free-form error metadata, the GraphQL `extensions` slot. Server-returned errors carry whatever `extensions` the resolver attached, verbatim.

## CacheControl

Describes supported cache control values for `graphql.query()`. See [Cache Control in Data SDK](/docs/platform/multiframework/guide/data-sdk-cache-control.md).

```javascript
type Unsubscribe = () => void;

type CacheControl = "no-cache" | "only-if-cached" | { type: "max-age", maxAge: number };
```

## Salesforce API Calls

These API endpoints are supported.

- /services/apexrest
- /services/data/v{version}/ui-api/records
- /services/data/v{version}/ui-api/search-info
- /services/data/v{version}/ui-api/layout
- /services/data/v{version}/ui-api/session/csrf
- /services/data/v{version}/connect/file/upload/config
- /services/data/v{version}/connect/proxy/ui-telemetry
- /services/data/v{version}/chatter/users/me
- /services/data/v{version}/chatter/users/{userId}
- /sfsites/c/\_nc_external/system/security/session/SessionTimeServlet
- /secur/logout.jsp

We recommend that you use optional chaining `fetch?.()` instead of a non-null assertion `fetch!.()`. Optional chaining is useful when you want to use fetch in a shared or cross-surface utility. If you're not sure where your code is run, use optional chaining and handle the response appropriately.

:::tip
The read-data examples in the [Multi-framework recipes repo](https://github.com/trailheadapps/multiframework-recipes) demonstrate how to call Chatter Connect API, Apex REST, and UI API REST.
:::

## `NodeOfConnection<T>`

Extracts the node type from a UIAPI connection response shape with the edges and node pattern.

```typescript
import { type NodeOfConnection } from "@salesforce/platform-sdk/data";
// Extract Account node type from the query response
type AccountNode = NodeOfConnection<GetHighRevenueAccountsQuery["uiapi"]["query"]["Account"]>;
```

Use `NodeOfConnection` when your GraphQL response uses the Salesforce connection shape (edges and node) and you want a clean, strongly-typed node type. For example:

- Query returns: `Account { edges { node { ... } } }`
- You define: `type AccountNode = NodeOfConnection<MyQuery["uiapi"]["query"]["Account"]>`
- Use `AccountNode` for transforms, props, and list rendering

If your query doesn't use connection fields or you already have simple flat generated types, you don’t need to use `NodeOfConnection`.

## Data SDK Considerations

When using the Data SDK to access Salesforce data use standard web APIs and npm packages only. These functionalities aren't supported:

- `@salesforce` scoped modules, except `@salesforce/platform-sdk/data`
- Lightning base components and `lightning/*` modules
- `@wire` service

If you're familiar with Lightning Web Components (LWC), here's what to use instead in Multi-Framework.

| Don't use (LWC-only)                                                                               | Use instead in Multi-Framework                                                                                                                                             |
| :------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `@salesforce/apex/Class.method`                                                                    | `dataSdk.fetch?.()` against `/services/apexrest/...`                                                                                                                       |
| `@salesforce/schema/Object.Field`                                                                  | Hardcode the API name as a string in your GraphQL query                                                                                                                    |
| `@salesforce/user/Id`, `/CurrentUserId`                                                            | GraphQL `uiapi.currentUser` query via `dataSdk.graphql?.query(...)`                                                                                                        |
| `lightning/uiRecordApi`: `get*` calls such as `getRecord` and `getListUi`                          | `dataSdk.graphql?.query(...)`                                                                                                                                              |
| `lightning/uiRecordApi`: mutation calls such as `createRecord`, `updateRecord`, and `deleteRecord` | `dataSdk.graphql?.mutate(...)`                                                                                                                                             |
| `@wire` decorator                                                                                  | React `useEffect` hook and `dataSdk.graphql?.query(...)`; `QueryResult.subscribe` for reactive updates                                                                     |
| `@salesforce/label/*` (custom label imports such as `@salesforce/label/c.Greeting`)                | The `labels` Data SDK extension: `sdk.ext.labels.get?.(...)` or `getAll?.(...)`. See [Get Custom Labels](/docs/platform/multiframework/guide/data-sdk-extension-label.md). |

Use `@salesforce/platform-sdk/data` for all Salesforce API calls. The SDK handles authentication and CSRF validation. Follow these data access guidelines in order of preference.

- Use GraphQL queries and mutations as the preferred way to access data. `dataSdk.graphql?.query()` and `dataSdk.graphql?.mutate()` send a POST request to Salesforce GraphQL.
- Use UI API via `sdk.fetch?.()` for data access that calls `/services/data/v{version}/ui-api/*` or another Salesforce REST endpoint, such as an Apex controller that's exposed via Apex REST.
- Use GraphQL with `sdk.fetch?.()` if GET request is required, such as when your query and variables are small enough to fit in URL constraints. Or use a GraphQL GET request if you have a dependency on a roundtrip fetch of a CSRF token.
- Use Apex REST when you want custom logic that GraphQL doesn't support.
- Don't call `fetch()` or `axios` directly for Salesforce endpoints.

## Data SDK Support

Data SDK support differs by surface. Data SDK supports web apps, such as those built using React or Angular. It also fully support micro-frontends.

| Data SDK Support                                        | WebApp | Micro-Frontend | OpenAI |
| :------------------------------------------------------ | :----: | :------------: | :----: |
| GraphQL queries                                         |    ✅   |        ✅       |    ✅   |
| GraphQL mutations                                       |    ✅   |        ✅       |    ✅   |
| GraphQL response caching (`cacheControl`)               |    ✅   |        ✅       |    ❌   |
| `fetch()` for Salesforce REST endpoints                 |    ✅   |        ✅       |    ❌   |
| `apiVersion` on the SDK instance                        |    ✅   |        ✅       |    ❌   |
| Per-request `headers` on a query or mutation            |    ✅   |        ✅       |    ❌   |
| `webapp` options (`basePath`, `apiVersion`, `onStatus`) |    ✅   |        ✅       |    ❌   |

Because Data SDK support varies, use optional chaining (`sdk.graphql?.`, `sdk.fetch?.`) so your code stays portable across surfaces.

:::note
On the `OpenAI` surface, `graphql` is uncached, so a query result's `subscribe()` callback receives new snapshots only when you call `refresh()`. On the `WebApp` and `Micro-Frontend` surfaces, `subscribe()` also receives cache-driven updates. See [Cache Control in Data SDK](/docs/platform/multiframework/guide/data-sdk-cache-control.md).
:::

## Data SDK Examples

Review the examples in the [React App Recipes GitHub repo](https://github.com/trailheadapps/multiframework-recipes). Install the app in a scratch org and explore each recipe to understand how to complete a specific task, whether it's querying data with GraphQL or handling loading, an empty state, or error responses.
