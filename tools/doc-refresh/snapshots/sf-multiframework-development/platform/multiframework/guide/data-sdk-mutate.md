# GraphQL Mutate Parameters

The GraphQL `mutate()` method in the Data SDK includes several parameters.

```typescript
import { createDataSDK, gql } from "@salesforce/platform-sdk/data";

const dataSdk = await createDataSDK();

const result = await dataSdk.graphql?.mutate<ResponseType, VariablesType>({
    mutation: MUTATION_STRING,
    variables: { ... },
    operationName?: "...",
    headers?: { "My-Header": "value" }
  });
```

## `graphql.mutate<T, V = Record<string, unknown>>(options: MutateOptions<V>)`

Runs a GraphQL mutation without caching.

### Parameters

| Parameter        | Type                                       | Description                                                                                                                                 |
| :--------------- | :----------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `mutation`       | `string`                                   | The GraphQL mutation operation string.                                                                                                      |
| `variables?`     | `V`, defaults to `Record<string, unknown>` | Optional key-value map of GraphQL variables referenced by the mutation.                                                                     |
| `operationName?` | `string`                                   | Optional operation name for multi-operation documents.                                                                                      |
| `headers?`       | `HeadersInit`                              | Optional [per-request HTTP headers](/docs/platform/multiframework/guide/data-sdk-request-headers.md) merged over the SDK's default headers. |

## UI API Mutation Structure

All GraphQL mutations follow this UI API structure.

```typescript
mutation <OperationName>($input: <ObjectName><Operation>Input!) {
  uiapi {
    <ObjectName><Operation>(input: $input) {
      # Create/Update: return Record with selected fields
      Record {
        Id
        <FieldName> { value }
      }
      # Delete: return only Id
      Id
    }
  }
}
```

For more information, see [Mutations Schema](https://developer.salesforce.com/docs/platform/graphql/guide/mutations-schema.md) in the *GraphQL API Developer Guide*.

## Inline Mutations with gql Tag

For simple mutations without external `.graphql` files, use the `gql` template tag.

```typescript
import { createDataSDK, gql } from "@salesforce/platform-sdk/data";

const DELETE_ACCOUNT = gql`
  mutation DeleteAccount($id: ID!) {
    uiapi {
      AccountDelete(input: { Id: $id }) {
        Id
      }
    }
  }
`;

export async function deleteAccount(id: string) {
  const dataSdk = await createDataSDK();
  const result = await dataSdk.graphql?.mutate({
    mutation: DELETE_ACCOUNT,
    variables: { id },
  });

  if (result?.errors?.length) {
    throw new Error("Failed to delete account");
  }

  return result?.data?.uiapi?.AccountDelete?.Id;
}
```

### Inline Mutations

Use inline mutations when:

- Simple mutations without complex input structures
- Mutations used in only one place
- Rapid prototyping or testing

### External `.graphql` Files

Use external `.graphql` files when:

- Complex mutations with many fields
- Mutations shared across multiple files
- When you want full type generation from codegen

For more information on generating types and implementing a mutation operation, see [GraphQL Mutations in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql-mutation.md).

## Returns

```typescript
Promise<MutationResult<T>>;
```

The return type of `dataSdk.graphql?.mutate()`, which resolves to the typed GraphQL response payload.

```typescript
interface MutationResult<T> {
  data: T | undefined;
  errors?: GraphQLError[];
}
```

:::note
Mutations don't support `subscribe()` or `refresh()` like [GraphQL queries](/docs/platform/multiframework/guide/data-sdk-query.md). To update stale data after a mutation, use a query result reference to call `result.refresh()`.
:::

Consider these mutation response behavior:

- A successful mutation returns data with no errors.
- A partially successful mutation has both data and errors.
- Data SDK preserves the partial data payload, so callers can still use returned fields even when errors exist.

GraphQL mutation operations return these response structures.

### Record Create

A create operation returns the record ID and any queried fields.

```typescript
{
  data: {
    uiapi: {
      AccountCreate?: {
        Record?: {
          Id: string;
          Name?: { value?: string | null };
          Industry?: { value?: string | null };
          // other returned fields...
        } | null;
      } | null;
    };
  };
  errors?: Array<{
    message: string;
    locations?: Array<{ line: number; column: number }>;
    path?: string[];
  }>;
}
```

### Record Update

An update operation returns the record ID and the updated fields.

```typescript
{
  data: {
    uiapi: {
      AccountUpdate?: {
        Record?: {
          Id: string;
          Name?: { value?: string | null };
          // returned updated fields...
        } | null;
      } | null;
    };
  };
  errors?: Array<{
    message: string;
    locations?: Array<{ line: number; column: number }>;
    path?: string[];
  }>;
}
```

### Record Delete

A delete operation returns the deleted record ID only.

```typescript
{
  data: {
    uiapi: {
      AccountDelete?: {
        Id: string;
      } | null;
    };
  };
  errors?: [
    {
      message: string;
      locations?: [{ line: number; column: number }];
      path?: string[];
    }
  ];
}
```

## Example: Successful Create Record Response

A successful query response includes record data in the `RecordCreate` object.

```json
{
  "data": {
    "uiapi": {
      "AccountCreate": {
        "Record": {
          "Id": "001xx000003DHP0AAO",
          "Name": { "value": "Acme Corp" },
          "Industry": { "value": "Technology" }
        }
      }
    }
  }
}
```

## Example: Partially Successful Create Record Response

A partially successful query response includes errors and some data.

```json
{
  "data": {
    "uiapi": {
      "AccountCreate": {
        "Record": {
          "Id": "001xx000003DHP0AAO",
          "Name": { "value": "Acme Corp" }
        }
      }
    }
  },
  "errors": [
    {
      "message": "Insufficient access on field AnnualRevenue",
      "locations": [{ "line": 8, "column": 5 }],
      "path": ["uiapi", "AccountCreate", "Record", "AnnualRevenue"]
    }
  ]
}
```

## See Also

- [Error Handling in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql-error.md)
- [Cache Control in Data SDK](/docs/platform/multiframework/guide/data-sdk-cache-control.md)
- *GraphQL API Developer Guide*: [Send Mutation Requests](https://developer.salesforce.com/docs/platform/graphql/guide/mutations-use.md)
