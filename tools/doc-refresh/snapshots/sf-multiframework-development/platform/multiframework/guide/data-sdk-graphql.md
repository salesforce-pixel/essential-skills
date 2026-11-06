# GraphQL Queries in Data SDK

Use a GraphQL query to retrieve Salesforce data, such as from an Account or Contact record.

To access Salesforce data via GraphQL:

1. Define TypeScript interfaces for the response shape.
2. Write the GraphQL query using `uiapi` syntax.
3. Use `createDataSDK()` and `dataSdk.graphql?.()` with proper typing.
4. Extract and return the data from the response.

```typescript
import { createDataSDK, gql } from "@salesforce/platform-sdk/data";

const dataSdk = await createDataSDK();

// For queries: use dataSdk.graphql?.query() or dataSdk.fetch?() for API calls
const result = await dataSdk.graphql?.query<ResponseType, VariablesType>({
    query: QUERY_STRING,
    variables: { ... },
    operationName?: "...",
    cacheControl?: "no-cache" | "only-if-cached" | { type: "max-age", maxAge: 60 }
  });
const QUERY_STRING = gql`
 query MyQuery {
   uiapi {
     ...
   }
 }
`;
```

For more information about GraphQL usage, see the [GraphQL API Developer Guide](https://developer.salesforce.com/docs/platform/graphql/guide/).

Use one of these patterns for defining GraphQL queries.

- [Inline `gql` Tag](#inline-gql-tag)
- [External `.graphql` File](#external-graphql-file)

## Inline `gql` Tag

This pattern is useful for simple queries without variables or fragments.

- Use the gql template tag (never plain template literals)
- Ensure the query operation name matches what codegen expects
- Import generated types from graphql-operations-types.ts

```javascript
import { createDataSDK, gql } from "@salesforce/platform-sdk/data";
import type { CurrentUserQuery } from "../graphql-operations-types";
const CURRENT_USER_QUERY = gql`
  query CurrentUser {
    uiapi {
      currentUser {
        Id
        Name {
          value
        }
      }
    }
  }
`;

interface User {
  id: string;
  name: string;
}

export async function getCurrentUser(): Promise<User | null> {
  const dataSdk = await createDataSDK();
  const result =
    (await dataSdk.graphql?.query) <
    CurrentUserQuery >
    {
      query: CURRENT_USER_QUERY,
    };

  if (result?.errors?.length) {
    throw new Error(result.errors.map((e) => e.message).join("; "));
  }

  const userData = result?.data?.uiapi.currentUser;
  if (!userData) {
    throw new Error("No user data found");
  }

  return {
    id: userData.Id,
    name: userData.Name?.value || "User",
  };
}
```

## External .graphql File

This pattern is useful for complex queries with variables, fragments, or queries shared across files.

- Import `.graphql` files with the `?raw` suffix
- Import generated types from `graphql-operations-types.ts`
- Provide response and variables type generics to `dataSdk.graphql?.query<T, V>()`
- Use optional chaining for nested response data

To implement a query using a `.graphql` external file:

1. Create a `.graphql` file under `src/api/utils/query/`

```javascript

# src/api/utils/query/myQuery.graphql
query GetMyData($myVariable: String) {
  uiapi {
    query {
      MyObject(first: 10, where: { Field: { eq: $myVariable } }) {
        edges {
          node {
            Id
            Name {
              value
            }
          }
        }
      }
    }
  }
}

```

2. Generate the types using `npm run graphql:codegen`. The command generates the types in `src/api/graphql-operations-types.ts`. For example:
   1. Response type: `GetMyDataQuery`
   2. Variables type: `GetMyDataQueryVariables`
3. Implement the data access function.

```javascript
import { createDataSDK, type NodeOfConnection } from "@salesforce/platform-sdk/data";
import MY_QUERY from "./query/myQuery.graphql?raw";
import type { GetMyDataQuery, GetMyDataQueryVariables } from "../graphql-operations-types";

type MyNode = NodeOfConnection<GetMyDataQuery["uiapi"]["query"]["MyObject"]>;

export async function getMyData(variables: GetMyDataQueryVariables): Promise<MyNode[]> {
  const dataSdk = await createDataSDK();
  const result = await dataSdk.graphql?.query<GetMyDataQuery, GetMyDataQueryVariables>({
    query: MY_QUERY,
    variables,
  });

  if (result?.errors?.length) {
    const errorMessages = result.errors.map((e) => e.message).join("; ");
    throw new Error(`GraphQL Error: ${errorMessages}`);
  }

  return result?.data?.uiapi?.query?.MyObject?.edges?.map((edge) => edge?.node) || [];
}

```

## Export the GraphQL Return Type

To provide type safety for GraphQL operations, define your return type. These TypeScript interfaces define the shape of data flowing in (query variables) and out (query results) of your GraphQL operations.

```typescript
export interface Account {
  id: string;
  name: string;
  industry: string | null;
  type: string | null;
  annualRevenue: number | null;
  numberOfEmployees: number | null;
  billingCity: string | null;
  billingState: string | null;
  billingCountry?: string | null;
  phone: string | null;
  website: string | null;
  description?: string | null;
}

export interface AccountsResult {
  accounts: Account[];
  pageInfo: {
    hasNextPage: boolean;
    endCursor: string | null;
  };
}
export interface GetAccountsQueryVariables {
  first?: number | null;
  after?: string | null;
}
```

Export the interfaces so they can be imported and reused across components. You can also use graphql-codegen to generate the interfaces for the interfaces to stay in sync with your schema. Use the return types in your methods and variables.

```typescript
export async function getAccounts(first = 20, after?: string): Promise<AccountsResult> {
 const variables: GetAccountsQueryVariables = { first };
 if (after) variables.after = after;

 const dataSdk = await createDataSDK();
 const result = await dataSdk.graphql?.query<GetAccountsQuery, GetAccountsQueryVariables>({
   query: GET_ACCOUNTS,
   variables,
 });

 if (result?.errors?.length) {
   throw new Error(result.errors.map((e) => e.message).join("; "));
 }
```

## GraphQL Fragments

GraphQL fragments are reusable units of query logic that are used to define a set of fields.\
This example uses GraphQL fragments and directives to keep one query reusable while conditionally including fields.

- `FinancialFields` and `ContactFields` are reusable field groups for `Account`.
- In the main query, each fragment is attached with `@include(if: $...):`
  - `...FinancialFields @include(if: $includeFinancials)`
  - `...ContactFields @include(if: $includeContacts)`
- At runtime, variables (`includeFinancials, includeContacts`) decide whether those field blocks are fetched.

```javascript
query GetAccountDetails($id: ID!, $includeFinancials: Boolean!, $includeContacts: Boolean!) {
  uiapi {
    query {
      Account(where: { Id: { eq: $id } }) {
        edges {
          node {
            Id
            Name {
              value
            }
            ...FinancialFields @include(if: $includeFinancials)
            ...ContactFields @include(if: $includeContacts)
          }
        }
      }
    }
  }
}

fragment FinancialFields on Account {
  AnnualRevenue {
    value
  }
  NumberOfEmployees {
    value
  }
}

fragment ContactFields on Account {
  Phone {
    value
  }
  Website {
    value
  }
}

```

`dataSdk.graphql?.query<Response, Variables>({ query, variables })` executes the query with:

- explicit response type (`GetAccountDetailsQuery`)
- explicit variables type (`GetAccountDetailsQueryVariables`)
- runtime variables object (`id, includeFinancials, includeContacts`)

```typescript
import { createDataSDK } from "@salesforce/platform-sdk/data";
import QUERY from "./query/getAccountDetails.graphql?raw";
import type {
  GetAccountDetailsQuery,
  GetAccountDetailsQueryVariables,
} from "../graphql-operations-types";

const dataSdk = await createDataSDK();
const result = await dataSdk.graphql?.query<
  GetAccountDetailsQuery,
  GetAccountDetailsQueryVariables
>({
  query: QUERY,
  variables: {
    id: accountId,
    includeFinancials: userWantsFinancials,
    includeContacts: userWantsContacts,
  },
});
```

## GraphQL Usage Considerations

When using GraphQL via the Data SDK, consider these usage patterns.

Direct API calls aren't supported. Always use the Data SDK to make your API calls.

```typescript
// Don't do this: Direct axios/fetch for Salesforce APIs
const result = await axios.post("/graphql", { query });
const result = await fetch("/services/data/v{version}/...");
// Do this: Use the DataSDK
const dataSdk = await createDataSDK();
const result = await dataSdk.graphql?.query<ResponseType>({ query, variables });
const result = await dataSdk.fetch?.("/services/data/v{version}/...");
```

Provide the response type instead of making untyped GraphQL calls.

```typescript
// Don't do this: Untyped GraphQL calls
await dataSdk.graphql?.query({ query });
// Do this: Provide response type generic
await dataSdk.graphql?.query<GetAccountsQuery>({ query });
```

Use the gql template tag or an external .graphql file instead of plain string queries.

```typescript
// Don't do this: Plain string queries
const query = `query { ... }`;

// Do this: Use gql tag or .graphql file
const query = gql`query { ... }`;
// or do this: Import the query from an external .graphql file
import QUERY from "./query/myQuery.graphql?raw";
```

Use optional chaining instead of non-null assertion on a GraphQL call.

```typescript
// Don't do this: Non-null assertion on graphql
await dataSdk.graphql!.query<T>({ query });
// Do this: Optional chaining
await dataSdk.graphql?.query<T>({ query });
```

## See Also

- [GraphQL Mutations in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql-mutation.md)
- [Error Handling in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql-error.md)
- [Cache Control in Data SDK](/docs/platform/multiframework/guide/data-sdk-cache-control.md)
