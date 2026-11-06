# Per-Request Headers

GraphQL requests in the Data SDK uses HTTP POST to a `/graphql` endpoint. Request headers are key-value metadata sent in an HTTP request. For multi-framework apps, these default headers apply to every `query()` and `mutate()` requests.

- [`Content-Type: application/json`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Type)
- [`Accept: application/json`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Accept)
- `X-Chatter-Entity-Encoding: false`

Multi-framework apps include the `X-Chatter-Entity-Encoding: false` header, which disables HTML entity encoding of string fields in the response.

To provide your own header on a per-request basis for `query()` or `mutate()`, pass in the optional `headers` parameter on a single request. If you pass in a duplicate header that collides with a default header, such as `Content-Type`, your header value replaces the default value.

```typescript
const dataSdk = await createDataSDK();
const result = await dataSdk.graphql?.query<AccountsData>({
  query: GET_ACCOUNTS,
  variables: { first: 20 },
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
```

You can use `headers` to pass an authorization token, a trace ID, or another per-request header.

```typescript
const dataSdk = await createDataSDK();
const result = await dataSdk.graphql?.mutate<CreateAccountMutation>({
  mutation: CREATE_ACCOUNT,
  variables: { input },
  headers: {
    "X-Trace-Id": id,
  },
});
```

Unique headers such as per-request trace IDs create a distinct cache entry and eliminate cache reuse.

`headers` accepts any [`HeadersInit`](https://developer.mozilla.org/en-US/docs/Web/API/Headers) value: a plain object, an array of `[name, value]` tuples, or a `Headers` instance. If you use the same header name more than once, the values for that header are merged into a single comma-separated value.

The `headers` parameter applies only to HTTP requests. Review these usage considerations for `headers`.

- Header names are case-insensitive. Your header can override the SDK's default of the same name, so avoid overriding transport headers such as `Content-Type` unless you intend to.
- `headers` is part of the cache key. For `query()`, two calls that are identical except for their `headers` resolve to different cache entries. This behavior prevents a response that's scoped by a header, such as `Authorization`, from being served to a later caller that passed a different value. Calls with equivalent headers still share an entry. See [Cache Control in Data SDK](/docs/platform/multiframework/guide/data-sdk-cache-control.md).
- `Accept-Language` is automatically appended. When the runtime environment provides an active language, the SDK adds an `Accept-Language` header to REST and GraphQL requests. Provide your own `Accept-Language` in `headers` only if you want to override the environment default.
