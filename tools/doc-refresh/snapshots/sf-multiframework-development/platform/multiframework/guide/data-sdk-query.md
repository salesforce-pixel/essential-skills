# GraphQL Query Parameters

The GraphQL `query()` method in the Data SDK includes several parameters.

```typescript
import { createDataSDK, gql } from "@salesforce/platform-sdk/data";

const dataSdk = await createDataSDK();

const result = await dataSdk.graphql?.query<ResponseType, VariablesType>({
    query: QUERY_STRING,
    variables: { ... },
    operationName?: "...",
    cacheControl?: "no-cache" | "only-if-cached" | { type: "max-age", maxAge: 60 },
    headers?: { "My-Header": "value" }
  });
const QUERY_STRING = gql`
 query MyQuery {
   uiapi {
     ...
   }
 }
`;

```

## `graphql.query<T, V = Record<string, unknown>>(options: QueryOptions<V>)`

Runs a GraphQL query with reactive capabilities.

### Parameters

| Parameter        | Type                                       | Description                                                                                                                                                                                                                                                                                                                             |
| :--------------- | :----------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `query`          | `string`                                   | The GraphQL query operation string, which accepts an [inline `gql` template tag or an external `.graphql` file](/docs/platform/multiframework/guide/data-sdk-graphql.md).                                                                                                                                                               |
| `variables?`     | `V`, defaults to `Record<string, unknown>` | Optional key-value map of GraphQL variables referenced by the query.                                                                                                                                                                                                                                                                    |
| `operationName?` | `string`                                   | Optional operation name for multi-operation documents.                                                                                                                                                                                                                                                                                  |
| `cacheControl?`  | `CacheControl`                             | Optional [cache control settings](/docs/platform/multiframework/guide/data-sdk-cache-control.md) for the GraphQL request.                                                                                                                                                                                                               |
| `headers?`       | `HeadersInit`                              | Optional [per-request HTTP headers](/docs/platform/multiframework/guide/data-sdk-request-headers.md) merged over the SDK's default headers. Because they can scope the response (for example, `Authorization`), `headers` is part of the cache key. See [Cache Control](/docs/platform/multiframework/guide/data-sdk-cache-control.md). |

## UI API Query Structure

All GraphQL queries follow this UI API structure.

```javascript
query {
  uiapi {
    query {
      <ObjectName>(
        first: Int           # pagination limit
        after: String        # pagination cursor
        where: <Object>_Filter
        orderBy: <Object>_OrderBy
      ) {
        edges {
          node {
            Id
            <FieldName> { value }
          }
        }
      }
    }
  }
}
```

For more information, see [Query Objects](https://developer.salesforce.com/docs/platform/graphql/guide/query-record-objects.md) in the *GraphQL API Developer Guide*.

## Returns

### **`Promise<QueryResult<T>>`**

The return type of `dataSdk.graphql?.query()`, which resolves to the typed GraphQL response payload.

```typescript
interface QueryResult<T> {
  data: T | undefined;
  errors?: GraphQLError[];
  subscribe(cb: QuerySubscriber<T>): Unsubscribe;
  refresh(): Promise<void>;
}
```

GraphQL record queries return this response structure.

```typescript
interface UIAPIQueryResponse {
  uiapi: {
    query: {
      [ObjectName: string]: {
        edges?: Array<{
          node?: {
            Id: string;
            // Every field is a { value, displayValue } envelope, not a bare scalar.
            // - value: raw value — use for logic and for writing back to the server
            // - displayValue: locale-formatted string — use for rendering in the UI
            [FieldName: string]?: { value?: FieldType | null; displayValue?: string | null } | null;
          } | null;
        } | null> | null;
      } | null;
    };
  };
}
```

## Subscribe to Query Updates

Query results from `graphql.query()` are reactive and support real-time updates through subscriptions, which you can use to update your UI automatically when data changes.

The `subscribe()` method listens for updates to a query result. Subscribers are notified when the data changes due to cache updates or explicit refreshes.

```typescript
const result = await dataSdk.graphql?.query<AccountData>({
  query: GET_ACCOUNT,
  variables: { id: accountId },
});

// Subscribe to updates
const unsubscribe = result.subscribe((snapshot) => {
  console.log("Updated data:", snapshot.data);
  if (snapshot.errors) {
    console.warn("Errors:", snapshot.errors);
  }
  // Update your UI here
});

// Clean up when done
unsubscribe();
```

## Refresh Query Data

Use the `refresh()` method to manually re-fetch data, bypassing the cache.

```typescript
const result = await dataSdk.graphql?.query<AccountData>({
  query: GET_ACCOUNT,
  variables: { id: accountId },
});

// Subscribe to updates
result.subscribe((snapshot) => {
  // UI update logic
  setAccount(snapshot.data);
});

// Later, refresh the data (e.g., on button click)
async function handleRefresh() {
  await result.refresh(); // Notify subscribers
}
```

## Example: Query Records from a React App

Here's an example on how to query records. The example uses the [`useState`](https://react.dev/reference/react/useState) and [`useEffect`](https://react.dev/reference/react/useEffect) React hooks to manage the component state and respond to data changes.

```java title="List of records"
/**
 * List Rendering with Salesforce Records
 *
 * Fetches Accounts via UIAPI GraphQL and renders them using .map().
 * Each item needs a stable key prop; here we use the record Id.
 *
 * LWC equivalent: list rendering uses for:each / lwc:for directives on
 * template elements with a key attribute. React uses .map() in JSX with
 * a key prop.
 *
 * @see ParentToChild — passing data from parent to child components via props
 */
import { useEffect, useState } from 'react';
import { createDataSDK, gql } from '@salesforce/platform-sdk';

const QUERY = gql`
  query AccountList {
    uiapi {
      query {
        Account(first: 6, orderBy: { Name: { order: ASC } }) {
          edges {
            node {
              Id
              Name @optional {
                value
              }
              Industry @optional {
                value
              }
            }
          }
        }
      }
    }
  }
`;

interface QueryResponse {
  uiapi: {
    query: {
      Account: {
        edges: Array<{
          node: {
            Id: string;
            Name: { value: string | null };
            Industry: { value: string | null };
          };
        }>;
      };
    };
  };
}

interface AccountFields {
  id: string;
  name: string;
  industry: string | null;
}

export default function ListOfAccounts() {
  const [accounts, setAccounts] = useState<AccountFields[]>();
  const [error, setError] = useState<string>();

  useEffect(() => {
    const fetchAccounts = async () => {
      const sdk = await createDataSDK();
      const result = await sdk.graphql?.query<QueryResponse>({ query: QUERY });

      if (result?.errors?.length) {
        throw new Error(
          result.errors.map((e: { message: string }) => e.message).join('; ')
        );
      }

      const edges = result?.data?.uiapi?.query?.Account?.edges ?? [];
      setAccounts(
        edges
          .map(edge => edge?.node)
          .filter(Boolean)
          .map(node => ({
            id: node.Id,
            name: node.Name?.value ?? 'Unknown',
            industry: node.Industry?.value ?? null,
          }))
      );
    };

    fetchAccounts().catch(err => {
      setError(err instanceof Error ? err.message : 'Request failed');
    });
  }, []);

  if (error) return <p className="text-destructive">{error}</p>;
  if (!accounts) return <p className="text-sm">Loading…</p>;

  return (
    <ul>
      {/* .map() replaces LWC's for:each directive. The key must be stable — record Id is ideal. */}
      {accounts.map(account => (
        <li
          key={account.id}
          className="py-2 -mx-2 px-2 rounded-md transition-colors hover:bg-accent/50"
        >
          <p className="text-sm">{account.name}</p>
          {account.industry && (
            <p className="text-xs text-muted-foreground">{account.industry}</p>
          )}
        </li>
      ))}
    </ul>
  );
}

```

:::tip
For more examples, see the [Multi-framework recipes repo](https://github.com/trailheadapps/multiframework-recipes).
:::

## Example: Successful GraphQL Query Response

A successful query response includes record data in the `node` object.

```json
{
  "data": {
    "uiapi": {
      "query": {
        "Account": {
          "edges": [
            {
              "node": {
                "Id": "001xx000003DHP0AAO",
                "Name": { "value": "Acme Corp" },
                "Industry": { "value": "Technology" }
              }
            }
          ],
          "pageInfo": {
            "hasNextPage": false,
            "endCursor": null
          }
        }
      }
    }
  }
}
```

## Example: Partial Success Response

A partially successful query response includes errors and some data.

```json
{
  "data": {
    "uiapi": {
      "query": {
        "Account": {
          "edges": [
            {
              "node": {
                "Id": "001xx000003DHP0AAO",
                "Name": { "value": "Acme Corp" }
              }
            }
          ]
        }
      }
    }
  },
  "errors": [
    {
      "message": "Insufficient access on field AnnualRevenue",
      "path": ["uiapi", "query", "Account", "edges", 0, "node", "AnnualRevenue"]
    }
  ]
}
```

## See Also

- [Error Handling in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql-error.md)
- [Cache Control in Data SDK](/docs/platform/multiframework/guide/data-sdk-cache-control.md)
- [GraphQL Queries in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql.md)
- *GraphQL API Developer Guide*: [Query Objects Examples](https://developer.salesforce.com/docs/platform/graphql/guide/query-record-examples.md)
