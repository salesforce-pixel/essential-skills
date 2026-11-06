# Cache Control in Data SDK

The `cacheControl` parameter on the GraphQL `query` method overrides the default caching behavior for individual queries. Cache control is available on web apps and it's ignored on uncached surfaces. Valid `cacheControl` values include:

- `no-cache`: Stores a response but requires revalidation before reuse.
- `only-if-cached`: Returns a stored response, or a `DataNotFoundError` on a cache miss.

:::note
`cacheControl` doesn't affect the cache key. Within a single cache store, the per-entry cache key is `{query, variables, operationName, headers}`. Two calls that are identical except for their [per-request `headers`](/docs/platform/multiframework/guide/data-sdk-request-headers.md) resolve to different cache entries to ensure that a response scoped by a header, such as `Authorization`, isn't served to a later caller that passed a different value. Calls with equivalent headers, including calls that pass no `headers` at all, share an entry.

The cache store itself is partitioned by base URL and API version, so SDK instances that target different API versions never share cache entries, even for otherwise identical queries. See [Work with Data SDK](/docs/platform/multiframework/guide/data-sdk-intro.md#createdatasdkoptions).
:::

## Default Behavior (300s TTL)

If a `cacheControl` value isn't provided, the SDK applies a default `max-age` strategy with a 300-second (5-minute) time to live (TTL). After the `max-age` expires, the next call fetches fresh data from the network. A stale entry is treated as a cache miss.

```typescript
const result = await dataSdk.graphql?.query<AccountData>({
  query: GET_ACCOUNTS,
  variables: { first: 20 },
});
```

The default caching behavior covers these scenarios.

- Cache hit: Cached responses that are less than 300 seconds are returned immediately.
- Stale cache: Responses that are more than 300 seconds are considered stale; the SDK fetches fresh data from the network.
- Cache miss: The SDK fetches data from the network and stores the response in the cache with a 300-second TTL.

## `cacheControl: "no-cache"`

To skip the cache and always fetch fresh data from the server, use `cacheControl: "no-cache"`.

```typescript
const result = await sdk.graphql?.query<AccountData>({
  query: GET_ACCOUNTS,
  variables: { first: 20 },
  cacheControl: "no-cache",
});
```

When you use `no-cache`, the SDK:

- Writes the response back to cache (with 300s TTL) for subsequent default callers
- Revalidates the cached response with the origin server before reusing it

Use `no-cache` when you want to trigger a force-refresh or reload on a page, such as after a known mutation operation.

## `cacheControl: "only-if-cached"`

To read from the cache only, use `cacheControl: "only-if-cached"`. The SDK reads from the cache only and never hits the network, even for a cache miss situation.

```typescript
const result = await sdk.graphql?.query<AccountData>({
  query: GET_ACCOUNTS,
  variables: { first: 20 },
  cacheControl: "only-if-cached",
});
```

When you use `only-if-cached`, the caching behavior covers these scenarios.

- Cache hit: Returns cached data
- Cache miss: Returns error (`DataNotFoundError`)

A cache miss isn't thrown. The Promise resolves and the cache miss surfaces on `result.errors`, carrying a [typed discriminator](/docs/platform/multiframework/guide/data-sdk-graphql-error.md) so you can tell it apart from a server-returned error.

Use `only-if-cached` when you know the data was already fetched. `only-if-cached` is also useful in offline-first patterns, avoiding loading states when stale data is acceptable.

## `cacheControl: { type: "max-age", maxAge: 60 }`

To change the default 300s TTL value, pass in your own `maxAge` value in seconds with `type: "max-age"`.

```typescript
const result = await sdk.graphql?.query<AccountData>({
  query: GET_ACCOUNTS,
  variables: { first: 20 },
  cacheControl: { type: "max-age", maxAge: 60 },
});
```

When you pass in your own `maxAge` value, the caching behavior looks like this.

- Same as the default behavior, but the data goes stale after the `maxAge` value you provide, instead of the default 300s TTL value
- Writes to cache with the `maxAge` value you provide

Use this pattern when your data changes frequently, such as in dashboards or notifications.

:::note
`maxAge` must be a finite non-negative number. Invalid values such as negative numbers and `NaN` fall back to 300s silently. `maxAge: 0` is valid and means the cache is always stale, resulting in a re-fetch on every call.
:::

## See Also

- [GraphQL Queries in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql.md)
- [GraphQL Mutations in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql-mutation.md)
- [Error Handling in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql-error.md)
