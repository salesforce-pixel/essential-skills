# Error Handling in Data SDK

GraphQL can return both data and errors in the same response for queries or mutation operations that result in partial success. For example, the record operation succeeds, but some return fields aren't accessible due to the user's permission.

Follow these error-handling strategies.

## Strict: Treat Any Errors as Failure

This strategy ensures a complete failure if any GraphQL errors are present in the response, regardless of whether partial data was also returned. As the most conservative approach, it guarantees that the app processes data only when the request was entirely successful. Use this strategy with queries where incomplete data is misleading.

```javascript
if (result?.errors?.length) {
  throw new Error(result.errors.map((e) => e.message).join("; "));
}
const data = result?.data;
```

## Tolerant: Log Errors but Use Partial Data

Data SDK preserves partial data from GraphQL error responses. When the server returns both `data` and `errors`, both fields are available in the result. This strategy allows you to gracefully degrade the UI by rendering the fetched data while logging errors for fields that failed.

:::note
Partial success responses where both `data` and `errors` are present aren't cached. Each subsequent query re-fetches data from the network.
:::

This strategy is suitable for cases where partial data is still usable by the app, even if the GraphQL request returns errors. The errors are logged for review, but the app continues to process the available data. Use this strategy when partial data is still useful and the UI can degrade gracefully, such as with an error on an optional field.

```javascript
const result =
  (await dataSdk.graphql?.query) <
  AccountData >
  {
    query: GET_ACCOUNT,
    variables: { id: accountId },
  };

if (result?.errors?.length) {
  console.warn("GraphQL partial errors:", result.errors);
}

// result.data may contain partial data even when errors are present
const data = result?.data;
```

## Fail Only When No Data is Returned

This is the least restrictive strategy. It permits the app to use any data that was successfully retrieved, even if partial errors occurred during the GraphQL request. The app throws an error only and fails if the response contains errors and no usable data was returned. For example, you can use this strategy in mutations where the operations succeed but some return fields aren't accessible.

```javascript
// Fail only when no data is returned
if (result?.errors?.length && !result?.data) {
  throw new Error(result.errors.map((e) => e.message).join("; "));
}
if (result?.errors?.length) {
  console.warn("Partial success with errors:", result.errors);
}
const data = result?.data;
```

## Network and Runtime Transport Errors

When handling `fetch()` errors for the Data SDK, consider transport and runtime errors where no responses are returned. For example, transport errors can include network failures, aborted requests, or runtime exceptions.

Wrap transport errors and check the response.

```typescript
const dataSdk = await createDataSDK();
let response: Response | undefined;
try {
  response = await dataSdk.fetch?.("/services/apexrest/data-access/account-summary", {
    method: "GET",
    headers: { Accept: "application/json" },
  });
} catch (error) {
  throw new Error(`Network/transport failure: ${(error as Error).message}`);
}
if (!response?.ok) {
  throw new Error(`Request failed: ${response?.status} ${response?.statusText}`);
}
const data = await response.json();
```

## HTTP Errors

When handling fetch() errors for the Data SDK, you can run into HTTP app errors with a non-2XX response that includes an error payload. For auth-sensitive flows, consider handling 401 and 403 errors with dedicated user actions, such as a sign-in refresh or a permission guidance message.

```typescript
const dataSdk = await createDataSDK();
const response = await dataSdk.fetch?.("/services/apexrest/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json", Accept: "application/json" },
  body: JSON.stringify(payload),
});

if (response.status === 401) {
  throw new Error("Authentication required or session expired.");
}
if (response.status === 403) {
  throw new Error("You do not have permission to perform this action.");
}
if (!response.ok) {
  throw new Error(`Request failed: ${response.status} ${response.statusText}`);
}
```

To recover from an expired session automatically instead of failing the request, see [Handle an Expired Session](/docs/platform/multiframework/guide/data-sdk-session-expiry.md).

## Extensions Errors

Each entry in `result.errors` is a `GraphQLError` that can carry an `extensions` object. When present, `extensions.code` provides a stable value to branch on for a specific error, rather than matching on `message` text.

```typescript
const result = await sdk.graphql?.query<AccountData>({
  query: GET_ACCOUNTS,
  variables: { first: 20 },
  cacheControl: "only-if-cached",
});

if (result?.errors?.[0]?.extensions?.code === "CACHE_MISS") {
  // Cold cache — fall back to a network fetch or render an empty state.
} else if (result?.errors?.length) {
  // A different failure — handle it through your normal error path.
}
```

The SDK sets `extensions.code === "CACHE_MISS"` when a request using `only-if-cached` finds nothing in the cache, so you can tell an empty cache apart from a real failure. Check the code first, then handle anything else with your usual error path. For more information, see [Cache Control in Data SDK](/docs/platform/multiframework/guide/data-sdk-cache-control.md).

## Example: Partial Success in Update

This example shows how to handle partial success in an update operation.

```typescript
async function updateAccount(id: string, updates: Partial<Account>) {
  const dataSdk = await createDataSDK();

  const result = await dataSdk.graphql?.mutate<UpdateAccountMutation>({
    mutation: UPDATE_ACCOUNT,
    variables: {
      input: {
        Id: id,
        Account: updates,
      },
    },
  });

  // Check if the mutation succeeded
  if (result?.errors?.length && !result?.data) {
    // Total failure - mutation didn't execute
    throw new Error(result.errors.map((e) => e.message).join("; "));
  }

  // Partial success - mutation executed but some fields had errors
  if (result?.errors?.length) {
    console.warn("Account updated with warnings:", result.errors);
    // You can still use result.data
  }

  return result?.data?.uiapi?.AccountUpdate?.Record;
}
```

## Error Handling in LWC and React

The approach to error handling in LWC and other frameworks such as React differs due to their distinct architectural models.

- LWC: In addition to standard JavaScript error handling patterns, LWC provides an `errorCallback(error, stack)` lifecycle method in a parent component to catch errors from its children. When making @wire calls, errors are returned in an error object, which standardizes error handling in LWC.
- React: Error handling typically relies on standard JavaScript mechanisms like promises for asynchronous Data SDK calls. You can also use error boundaries, which are special components (`componentDidCatch`, `getDerivedStateFromError`) that catch JavaScript errors in the component tree and display a fallback UI.

:::tip
The error handling examples in the [Multi-framework recipes repo](https://github.com/trailheadapps/multiframework-recipes) demonstrate how to use error boundaries, handle GraphQL errors, and handle the loading, error, and empty states.
:::

## See Also

- [GraphQL Queries in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql.md)
- [GraphQL Mutations in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql-mutation.md)
- [Cache Control in Data SDK](/docs/platform/multiframework/guide/data-sdk-cache-control.md)
