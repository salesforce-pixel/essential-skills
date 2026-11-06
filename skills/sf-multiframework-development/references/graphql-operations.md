# GraphQL queries, mutations, errors, cache, headers

Sources: `data-sdk-query`, `data-sdk-mutate`, `data-sdk-graphql`, `data-sdk-graphql-mutation`, `data-sdk-graphql-error`, `data-sdk-cache-control`, `data-sdk-request-headers`.

Code below is copied from the docs. Where the docs had a mangled sample (Prettier turned generics into `<`/`>` comparisons), the corrected form is shown and marked.

## Query parameters

```typescript
import { createDataSDK, gql } from "@salesforce/platform-sdk/data";

const dataSdk = await createDataSDK();
const result = await dataSdk.graphql?.query<ResponseType, VariablesType>({
  query: QUERY_STRING,                 // gql`` or imported .graphql?raw
  variables: { ... },                  // optional
  operationName: "...",                // optional, multi-operation documents
  cacheControl: "no-cache" | "only-if-cached" | { type: "max-age", maxAge: 60 }, // optional
  headers: { "My-Header": "value" },   // optional, part of the cache key
});
```

### UI API query shape

```graphql
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

Every field is a `{ value, displayValue }` envelope, not a scalar: use `value` for logic and for writing back; `displayValue` (locale-formatted) for rendering. Connections also return `pageInfo { hasNextPage endCursor }`.

```typescript
interface UIAPIQueryResponse {
  uiapi: {
    query: {
      [ObjectName: string]: {
        edges?: Array<{
          node?: {
            Id: string;
            [FieldName: string]?: { value?: FieldType | null; displayValue?: string | null } | null;
          } | null;
        } | null> | null;
      } | null;
    };
  };
}
```

The docs' examples put `@optional` on fields (`Name @optional { value }`) without explaining it. In the Salesforce GraphQL API it leaves out a field the user can't access instead of failing the query; the GraphQL API Developer Guide has the details.

### Subscribe and refresh

```typescript
const result = await dataSdk.graphql?.query<AccountData>({
  query: GET_ACCOUNT,
  variables: { id: accountId },
});

const unsubscribe = result.subscribe((snapshot) => {
  setAccount(snapshot.data);
  if (snapshot.errors) console.warn("Errors:", snapshot.errors);
});

async function handleRefresh() {
  await result.refresh(); // bypasses cache, notifies subscribers
}

// on cleanup
unsubscribe();
```

### React list example

```tsx
import { useEffect, useState } from 'react';
import { createDataSDK, gql } from '@salesforce/platform-sdk/data'; // docs sample imported from '@salesforce/platform-sdk'

const QUERY = gql`
  query AccountList {
    uiapi {
      query {
        Account(first: 6, orderBy: { Name: { order: ASC } }) {
          edges {
            node {
              Id
              Name @optional { value }
              Industry @optional { value }
            }
          }
        }
      }
    }
  }
`;

interface QueryResponse {
  uiapi: { query: { Account: { edges: Array<{ node: {
    Id: string; Name: { value: string | null }; Industry: { value: string | null };
  } }> } } };
}

interface AccountFields { id: string; name: string; industry: string | null }

export default function ListOfAccounts() {
  const [accounts, setAccounts] = useState<AccountFields[]>();
  const [error, setError] = useState<string>();

  useEffect(() => {
    const fetchAccounts = async () => {
      const sdk = await createDataSDK();
      const result = await sdk.graphql?.query<QueryResponse>({ query: QUERY });
      if (result?.errors?.length) {
        throw new Error(result.errors.map((e: { message: string }) => e.message).join('; '));
      }
      const edges = result?.data?.uiapi?.query?.Account?.edges ?? [];
      setAccounts(
        edges.map(edge => edge?.node).filter(Boolean).map(node => ({
          id: node.Id,
          name: node.Name?.value ?? 'Unknown',
          industry: node.Industry?.value ?? null,
        }))
      );
    };
    fetchAccounts().catch(err => setError(err instanceof Error ? err.message : 'Request failed'));
  }, []);

  if (error) return <p className="text-destructive">{error}</p>;
  if (!accounts) return <p className="text-sm">Loading…</p>;
  return (
    <ul>
      {accounts.map(account => (
        <li key={account.id}>
          <p className="text-sm">{account.name}</p>
          {account.industry && <p className="text-xs text-muted-foreground">{account.industry}</p>}
        </li>
      ))}
    </ul>
  );
}
```

Responses: success has `data` only. Partial success has `data` **and** `errors`, e.g. `{"message": "Insufficient access on field AnnualRevenue", "path": ["uiapi","query","Account","edges",0,"node","AnnualRevenue"]}`.

## Two ways to define operations

**Inline `gql`**: simple operations without variables or fragments, used in one place, prototyping. Make the operation name match what codegen expects; import generated types from `graphql-operations-types.ts`.

```typescript
import { createDataSDK, gql } from "@salesforce/platform-sdk/data";
import type { CurrentUserQuery } from "../graphql-operations-types";

const CURRENT_USER_QUERY = gql`
  query CurrentUser {
    uiapi {
      currentUser {
        Id
        Name { value }
      }
    }
  }
`;

export async function getCurrentUser(): Promise<{ id: string; name: string } | null> {
  const dataSdk = await createDataSDK();
  // corrected: the docs sample is mangled as `(await dataSdk.graphql?.query) < CurrentUserQuery > {...}`
  const result = await dataSdk.graphql?.query<CurrentUserQuery>({ query: CURRENT_USER_QUERY });

  if (result?.errors?.length) {
    throw new Error(result.errors.map((e) => e.message).join("; "));
  }
  const userData = result?.data?.uiapi.currentUser;
  if (!userData) throw new Error("No user data found");
  return { id: userData.Id, name: userData.Name?.value || "User" };
}
```

**External `.graphql` file**: complex operations with variables or fragments, shared operations, full codegen types.

1. Create `src/api/utils/query/myQuery.graphql`:

```graphql
query GetMyData($myVariable: String) {
  uiapi {
    query {
      MyObject(first: 10, where: { Field: { eq: $myVariable } }) {
        edges { node { Id Name { value } } }
      }
    }
  }
}
```

2. `npm run graphql:codegen` → `src/api/graphql-operations-types.ts` with `GetMyDataQuery` and `GetMyDataQueryVariables`. (Run `npm run graphql:schema` first if the schema isn't current.)
3. Import with `?raw`:

```typescript
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
    throw new Error(`GraphQL Error: ${result.errors.map((e) => e.message).join("; ")}`);
  }
  return result?.data?.uiapi?.query?.MyObject?.edges?.map((edge) => edge?.node) || [];
}
```

Export your own app-facing interfaces (e.g. `Account`, `AccountsResult { accounts; pageInfo { hasNextPage; endCursor } }`, `GetAccountsQueryVariables { first?; after? }`) for reuse, or let codegen generate them so they stay in sync with the schema.

### Fragments with `@include`

```graphql
query GetAccountDetails($id: ID!, $includeFinancials: Boolean!, $includeContacts: Boolean!) {
  uiapi {
    query {
      Account(where: { Id: { eq: $id } }) {
        edges {
          node {
            Id
            Name { value }
            ...FinancialFields @include(if: $includeFinancials)
            ...ContactFields @include(if: $includeContacts)
          }
        }
      }
    }
  }
}

fragment FinancialFields on Account {
  AnnualRevenue { value }
  NumberOfEmployees { value }
}

fragment ContactFields on Account {
  Phone { value }
  Website { value }
}
```

```typescript
import QUERY from "./query/getAccountDetails.graphql?raw";
const result = await dataSdk.graphql?.query<GetAccountDetailsQuery, GetAccountDetailsQueryVariables>({
  query: QUERY,
  variables: { id: accountId, includeFinancials: userWantsFinancials, includeContacts: userWantsContacts },
});
```

### Do / don't

```typescript
// ❌ Direct axios/fetch for Salesforce APIs
await axios.post("/graphql", { query });
await fetch("/services/data/v{version}/...");
// ✅
await dataSdk.graphql?.query<ResponseType>({ query, variables });
await dataSdk.fetch?.("/services/data/v{version}/...");

// ❌ untyped                          ✅ typed
await dataSdk.graphql?.query({ query }); await dataSdk.graphql?.query<GetAccountsQuery>({ query });

// ❌ plain string                     ✅ gql or .graphql?raw
const q = `query { ... }`;              const q = gql`query { ... }`;

// ❌ non-null assertion               ✅ optional chaining
await dataSdk.graphql!.query<T>({ query }); await dataSdk.graphql?.query<T>({ query });
```

## Mutations

`mutate()` is never cached, never writes the cache (so subsequent queries don't see the change), has no `subscribe`/`refresh`, and returns `MutationResult<T>` (`data`, `errors`). Partial data is preserved alongside errors.

```typescript
const result = await dataSdk.graphql?.mutate<MutationResponse, MutationVariables>({
  mutation: MUTATION_STRING,
  variables: { ... },
  operationName: "...",          // optional
  headers: { "My-Header": "v" }, // optional
});
if (result?.errors?.length) throw new Error(result.errors.map((e) => e.message).join("; "));
```

### Mutation shape

```graphql
mutation <OperationName>($input: <ObjectName><Operation>Input!) {
  uiapi {
    <ObjectName><Operation>(input: $input) {
      Record { Id <FieldName> { value } }   # Create / Update
      Id                                    # Delete returns only Id
    }
  }
}
```

Operations are `<Object>Create`, `<Object>Update`, `<Object>Delete`. Input shapes:
- Create: `{ input: { Account: { Name, Industry, ... } } }`
- Update: `{ input: { Id, Account: { Name, ... } } }`
- Delete: `{ input: { Id } }` (or inline `AccountDelete(input: { Id: $id })`)

### Create

```graphql
# src/api/account/mutation/createAccount.graphql
mutation CreateAccount($input: AccountCreateInput!) {
  uiapi {
    AccountCreate(input: $input) {
      Record {
        Id
        Name { value }
        Industry { value }
        Phone { value }
        Website { value }
      }
    }
  }
}
```

```typescript
import { createDataSDK } from "@salesforce/platform-sdk/data";
import CREATE_ACCOUNT from "./mutation/createAccount.graphql?raw";
import type { CreateAccountMutation, CreateAccountMutationVariables } from "../graphql-operations-types";

export interface CreateAccountInput { name: string; industry?: string; phone?: string; website?: string }

export async function createAccount(input: CreateAccountInput) {
  const dataSdk = await createDataSDK();
  const result = await dataSdk.graphql?.mutate<CreateAccountMutation, CreateAccountMutationVariables>({
    mutation: CREATE_ACCOUNT,
    variables: {
      input: { Account: { Name: input.name, Industry: input.industry, Phone: input.phone, Website: input.website } },
    },
  });
  if (result?.errors?.length) {
    throw new Error(`Failed to create account: ${result.errors.map((e) => e.message).join("; ")}`);
  }
  return result?.data?.uiapi?.AccountCreate?.Record;
}
```

### Update

```graphql
mutation UpdateAccount($input: AccountUpdateInput!) {
  uiapi {
    AccountUpdate(input: $input) {
      Record { Id Name { value } Industry { value } AnnualRevenue { value } Phone { value } }
    }
  }
}
```

```typescript
export async function updateAccount(input: { id: string; name?: string; industry?: string; annualRevenue?: number; phone?: string }) {
  const dataSdk = await createDataSDK();
  const result = await dataSdk.graphql?.mutate<UpdateAccountMutation, UpdateAccountMutationVariables>({
    mutation: UPDATE_ACCOUNT,
    variables: {
      input: {
        Id: input.id,
        Account: { Name: input.name, Industry: input.industry, AnnualRevenue: input.annualRevenue, Phone: input.phone },
      },
    },
  });
  if (result?.errors?.length) {
    throw new Error(`Failed to update account: ${result.errors.map((e) => e.message).join("; ")}`);
  }
  return result?.data?.uiapi?.AccountUpdate?.Record;
}
```

### Delete

```graphql
mutation DeleteAccount($input: AccountDeleteInput!) {
  uiapi {
    AccountDelete(input: $input) { Id }
  }
}
```

```typescript
export async function deleteAccount(id: string): Promise<string> {
  const dataSdk = await createDataSDK();
  const result = await dataSdk.graphql?.mutate<DeleteAccountMutation, DeleteAccountMutationVariables>({
    mutation: DELETE_ACCOUNT,
    variables: { input: { Id: id } },
  });
  if (result?.errors?.length) {
    throw new Error(`Failed to delete account: ${result.errors.map((e) => e.message).join("; ")}`);
  }
  return result?.data?.uiapi?.AccountDelete?.Id || "";
}
```

Components wrap these in the usual pattern: `loading`/`error` state, `try { await createAccount(...); reset form; onSuccess?.() } catch (err) { setError((err as Error).message) } finally { setLoading(false) }`.

### Refresh after mutations (the cache isn't updated)

1. **Keep the `QueryResult` and call `refresh()`**:

```typescript
const result = await dataSdk.graphql?.query<AccountsData>({ query: GET_ACCOUNTS });
setAccountsResult(result);
result?.subscribe((snapshot) =>
  setAccounts(snapshot.data?.uiapi?.query?.Account?.edges?.map((e) => e.node) || []),
);
// after a mutation
await createAccount({ name });
await accountsResult?.refresh();
```

2. **Re-run the query** (e.g. `await loadAccounts()`), with `cacheControl: "no-cache"` if a default-cached copy would be returned.
3. **Optimistic update**: change local state first; on failure, `await accountsResult.refresh()` to revert.

Best practices: always select `Id` in returned `Record`; typed input interfaces; loading states; success/error feedback; reset forms on success; for dependent writes create the parent first, then children with `Promise.all`.

## Error handling

GraphQL can return `data` and `errors` together (e.g. the record write succeeded but a returned field isn't readable). Pick a strategy:

```typescript
// Strict: any error is failure (queries where incomplete data misleads)
if (result?.errors?.length) throw new Error(result.errors.map((e) => e.message).join("; "));

// Tolerant: log, use partial data (optional fields, graceful degradation)
if (result?.errors?.length) console.warn("GraphQL partial errors:", result.errors);
const data = result?.data;

// Fail only when no data (e.g. mutations whose write succeeded)
if (result?.errors?.length && !result?.data) throw new Error(result.errors.map((e) => e.message).join("; "));
if (result?.errors?.length) console.warn("Partial success with errors:", result.errors);
```

**Partial responses (data + errors) are never cached**: every later query goes to the network.

**Transport errors** (`fetch`): wrap in try/catch, then check `ok`:

```typescript
let response: Response | undefined;
try {
  response = await dataSdk.fetch?.("/services/apexrest/data-access/account-summary", {
    method: "GET",
    headers: { Accept: "application/json" },
  });
} catch (error) {
  throw new Error(`Network/transport failure: ${(error as Error).message}`);
}
if (!response?.ok) throw new Error(`Request failed: ${response?.status} ${response?.statusText}`);
const data = await response.json();
```

**HTTP errors**: handle `401` (sign-in / session expired) and `403` (permission guidance) explicitly, then `!response.ok`. Or set `createDataSDK({ webapp: { onStatus: { 401: () => reauthenticate() } } })`.

**Branch on `extensions.code`, not message text**:

```typescript
const result = await sdk.graphql?.query<AccountData>({
  query: GET_ACCOUNTS,
  variables: { first: 20 },
  cacheControl: "only-if-cached",
});
if (result?.errors?.[0]?.extensions?.code === "CACHE_MISS") {
  // cold cache: fetch from network or render empty state
} else if (result?.errors?.length) {
  // real failure
}
```

React: use promises/try-catch for SDK calls, plus error boundaries (`getDerivedStateFromError`, `componentDidCatch`) for render errors. (LWC equivalent: `errorCallback`, `@wire` error objects.)

## Cache control (`query()` only; ignored on uncached surfaces)

| Value | Behaviour | Use when |
|---|---|---|
| *(omitted)* | `max-age` 300 s. Fresh hit → returned immediately; stale → treated as a miss, fetched; miss → fetched and stored for 300 s | Default |
| `"no-cache"` | Always revalidates with the server before reuse; writes the fresh response back (300 s TTL) for default callers | Force refresh, e.g. after a known mutation |
| `"only-if-cached"` | Cache only, never the network. Miss **resolves** (doesn't throw) with an error on `result.errors`, `extensions.code === "CACHE_MISS"` (docs also call it `DataNotFoundError`) | Data known to be loaded; offline-first; avoid loading states |
| `{ type: "max-age", maxAge: N }` | Like default with an N-second TTL; writes with N | Fast-changing data (dashboards, notifications) |

- `maxAge` must be finite and ≥ 0. Negative/`NaN` silently fall back to 300. `maxAge: 0` = always stale (re-fetch every call).
- Cache key: `{query, variables, operationName, headers}`. `cacheControl` is **not** part of the key. The store is partitioned by base URL + API version.

## Per-request headers

Default headers on every `query()`/`mutate()` (POST to `/graphql`): `Content-Type: application/json`, `Accept: application/json`, `X-Chatter-Entity-Encoding: false` (no HTML entity encoding of strings).

```typescript
await dataSdk.graphql?.query<AccountsData>({
  query: GET_ACCOUNTS,
  variables: { first: 20 },
  headers: { Authorization: `Bearer ${token}` },
});

await dataSdk.graphql?.mutate<CreateAccountMutation>({
  mutation: CREATE_ACCOUNT,
  variables: { input },
  headers: { "X-Trace-Id": id },
});
```

- Accepts any `HeadersInit`. Duplicate names merge into one comma-separated value.
- Names are case-insensitive; yours override SDK defaults (don't override `Content-Type` by accident).
- **Headers are part of the cache key**: a unique per-request header (trace id) gives every call its own cache entry, so nothing is reused.
- `Accept-Language` is added automatically when the runtime has an active language. Override only on purpose. (`data-sdk-intro` says GraphQL *response* localisation isn't supported yet.)
- HTTP transports only.
