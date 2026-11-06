# GraphQL Mutations in Data SDK

GraphQL mutations are operations that create, update, or delete Salesforce records. Use the `graphql.mutate()` method for all mutation operations.

Unlike queries, mutations:

- Are never cached and don't write to the cache
- Return `MutationResult<T>` with only `data` and `errors` fields
- Don't provide subscription support
- Don't write to the cache, so they won't affect subsequent query results

```typescript
const result = await dataSdk.graphql?.mutate<MutationResponse, MutationVariables>({
  mutation: MUTATION_STRING,
  variables: { ... },
  operationName?: "..."
});

// Check for errors
if (result?.errors?.length) {
  throw new Error(result.errors.map((e) => e.message).join("; "));
}

// Use the returned data
const createdRecord = result?.data;
```

## Create Record

Create a new record using the `<ObjectName>Create` mutation.

### Step 1: Define the Mutation

A mutation operation follows the `RecordCreate` name pattern, for example, `AccountCreate`. See [Mutations Schema](https://developer.salesforce.com/docs/platform/graphql/guide/mutations-schema.md) in the *GraphQL API Developer Guide*.

```graphql
# uiBundles/yourAppName/src/api/account/query/createAccount.graphql
mutation CreateAccount($input: AccountCreateInput!) {
  uiapi {
    AccountCreate(input: $input) {
      Record {
        Id
        Name {
          value
        }
        Industry {
          value
        }
        Phone {
          value
        }
        Website {
          value
        }
      }
    }
  }
}
```

### Step 2: Generate Types

Run `npm run graphql:codegen` to generate TypeScript types.

```typescript
// Generated in src/api/graphql-operations-types.ts
export type CreateAccountMutation = {
  uiapi: {
    AccountCreate: {
      Record: {
        Id: string;
        Name: { value: string } | null;
        Industry: { value: string } | null;
        Phone: { value: string } | null;
        Website: { value: string } | null;
      };
    };
  };
};

export type CreateAccountMutationVariables = {
  input: AccountCreateInput;
};

export type AccountCreateInput = {
  Account: {
    Name?: string;
    Industry?: string;
    Phone?: string;
    Website?: string;
    // ... other fields
  };
};
```

### Step 3: Implement the Mutation Function

Implement the client-side mutation function that invokes `dataSdk.graphql?.mutate()` with the generated types.

```typescript
// uiBundles/yourAppName/src/api/account/accountCreate.ts
import { createDataSDK } from "@salesforce/platform-sdk/data";
import CREATE_ACCOUNT from "./mutation/createAccount.graphql?raw";
import type {
  CreateAccountMutation,
  CreateAccountMutationVariables,
} from "../graphql-operations-types";

export interface CreateAccountInput {
  name: string;
  industry?: string;
  phone?: string;
  website?: string;
}

export async function createAccount(input: CreateAccountInput) {
  const dataSdk = await createDataSDK();

  const result = await dataSdk.graphql?.mutate<
    CreateAccountMutation,
    CreateAccountMutationVariables
  >({
    mutation: CREATE_ACCOUNT,
    variables: {
      input: {
        Account: {
          Name: input.name,
          Industry: input.industry,
          Phone: input.phone,
          Website: input.website,
        },
      },
    },
  });

  if (result?.errors?.length) {
    const errorMessages = result.errors.map((e) => e.message).join("; ");
    throw new Error(`Failed to create account: ${errorMessages}`);
  }

  return result?.data?.uiapi?.AccountCreate?.Record;
}
```

### Step 4: Use in Your Component

This component example shows how to call `createAccount`, handle loading and error states, and react to the created result.

```typescript
import { useState } from "react";
import { createAccount } from "./api/accounts";

function CreateAccountForm() {
  const [name, setName] = useState("");
  const [industry, setIndustry] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const newAccount = await createAccount({ name, industry });
      console.log("Created account:", newAccount);
      // Clear form
      setName("");
      setIndustry("");
      // Optionally navigate or refresh data
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Account Name"
        required
      />
      <input
        value={industry}
        onChange={(e) => setIndustry(e.target.value)}
        placeholder="Industry"
      />
      <button type="submit" disabled={loading}>
        {loading ? "Creating..." : "Create Account"}
      </button>
      {error && <div className="error">{error}</div>}
    </form>
  );
}
```

## Update Record

Update an existing record using the `<ObjectName>Update` mutation.

### Step 1: Define the Mutation

```graphql
# uiBundles/yourAppName/src/api/account/query/updateAccount.graphql
mutation UpdateAccount($input: AccountUpdateInput!) {
  uiapi {
    AccountUpdate(input: $input) {
      Record {
        Id
        Name {
          value
        }
        Industry {
          value
        }
        AnnualRevenue {
          value
        }
        Phone {
          value
        }
      }
    }
  }
}
```

### Step 2: Implement the Mutation Function

Implement the update function: call `dataSdk.graphql?.mutate()` with the update payload, then check and handle any returned errors.

```typescript
import { createDataSDK } from "@salesforce/platform-sdk/data";
import UPDATE_ACCOUNT from "./mutation/updateAccount.graphql?raw";
import type {
  UpdateAccountMutation,
  UpdateAccountMutationVariables,
} from "../graphql-operations-types";

export interface UpdateAccountInput {
  id: string;
  name?: string;
  industry?: string;
  annualRevenue?: number;
  phone?: string;
}

export async function updateAccount(input: UpdateAccountInput) {
  const dataSdk = await createDataSDK();

  const result = await dataSdk.graphql?.mutate<
    UpdateAccountMutation,
    UpdateAccountMutationVariables
  >({
    mutation: UPDATE_ACCOUNT,
    variables: {
      input: {
        Id: input.id,
        Account: {
          Name: input.name,
          Industry: input.industry,
          AnnualRevenue: input.annualRevenue,
          Phone: input.phone,
        },
      },
    },
  });

  if (result?.errors?.length) {
    const errorMessages = result.errors.map((e) => e.message).join("; ");
    throw new Error(`Failed to update account: ${errorMessages}`);
  }

  return result?.data?.uiapi?.AccountUpdate?.Record;
}
```

### Step 3: Use in Your Component

This form component demonstrates using `updateAccount` and calling `onSuccess` after a successful update, while displaying errors when present.

```typescript
// uiBundles/yourAppName/src/api/account/accountUpdate.ts
import { useState, useEffect } from "react";
import { updateAccount } from "./api/accounts";

interface EditAccountFormProps {
  accountId: string;
  initialName: string;
  initialIndustry?: string;
  onSuccess?: () => void;
}

function EditAccountForm({
  accountId,
  initialName,
  initialIndustry,
  onSuccess,
}: EditAccountFormProps) {
  const [name, setName] = useState(initialName);
  const [industry, setIndustry] = useState(initialIndustry || "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await updateAccount({
        id: accountId,
        name,
        industry,
      });
      onSuccess?.();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Account Name"
        required
      />
      <input
        value={industry}
        onChange={(e) => setIndustry(e.target.value)}
        placeholder="Industry"
      />
      <button type="submit" disabled={loading}>
        {loading ? "Updating..." : "Update Account"}
      </button>
      {error && <div className="error">{error}</div>}
    </form>
  );
}
```

## Delete Record

Delete a record using the `<ObjectName>Delete` mutation.

### Step 1: Define the Mutation

Define the delete mutation in a `.graphql` file that accepts the delete input and returns the deleted record Id.

```graphql
# uiBundles/yourAppName/src/api/account/query/deleteAccount.graphql
mutation DeleteAccount($input: AccountDeleteInput!) {
  uiapi {
    AccountDelete(input: $input) {
      Id
    }
  }
}
```

:::note
Delete mutations only return the ID of the deleted record, not a `Record` object.
:::

### Step 2: Implement the Mutation Function

Implement the delete function that calls `dataSdk.graphql?.mutate()`, validates the result, and returns the deleted ID to callers.

```typescript
import { createDataSDK } from "@salesforce/platform-sdk/data";
import DELETE_ACCOUNT from "./mutation/deleteAccount.graphql?raw";
import type {
  DeleteAccountMutation,
  DeleteAccountMutationVariables,
} from "../graphql-operations-types";

export async function deleteAccount(id: string): Promise<string> {
  const dataSdk = await createDataSDK();

  const result = await dataSdk.graphql?.mutate<
    DeleteAccountMutation,
    DeleteAccountMutationVariables
  >({
    mutation: DELETE_ACCOUNT,
    variables: {
      input: {
        Id: id,
      },
    },
  });

  if (result?.errors?.length) {
    const errorMessages = result.errors.map((e) => e.message).join("; ");
    throw new Error(`Failed to delete account: ${errorMessages}`);
  }

  return result?.data?.uiapi?.AccountDelete?.Id || "";
}
```

### Step 3: Use in Your Component

This example shows a button component that calls `deleteAccount`, displays progress, and handles any error returned by the mutation.

```typescript
// uiBundles/yourAppName/src/api/account/accountDelete.ts
import { useState } from "react";
import { deleteAccount } from "./api/accounts";

interface DeleteAccountButtonProps {
  accountId: string;
  accountName: string;
  onSuccess?: () => void;
}

function DeleteAccountButton({ accountId, accountName, onSuccess }: DeleteAccountButtonProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleDelete() {
    const confirmed = window.confirm(`Are you sure you want to delete "${accountName}"?`);

    if (!confirmed) return;

    setLoading(true);
    setError(null);

    try {
      await deleteAccount(accountId);
      onSuccess?.();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <button onClick={handleDelete} disabled={loading} className="danger-button">
        {loading ? "Deleting..." : "Delete"}
      </button>
      {error && <div className="error">{error}</div>}
    </div>
  );
}
```

## Refresh Queries After Mutations

Since mutations don't update the cache, you need to manually refresh related queries to reflect the changes in the UI.

### Pattern 1: Refresh with QueryResult

If you have access to the `QueryResult` object from a previous query, call `refresh()`:

```typescript
import { useEffect, useState } from "react";
import { createDataSDK } from "@salesforce/platform-sdk/data";
import { createAccount } from "./api/accounts";
import type { QueryResult } from "@salesforce/platform-sdk/data";

function AccountManager() {
  const [accountsResult, setAccountsResult] = useState<QueryResult<AccountsData>>();
  const [accounts, setAccounts] = useState<Account[]>([]);

  useEffect(() => {
    async function loadAccounts() {
      const dataSdk = await createDataSDK();
      const result = await dataSdk.graphql?.query<AccountsData>({
        query: GET_ACCOUNTS,
      });

      setAccountsResult(result);
      setAccounts(result?.data?.uiapi?.query?.Account?.edges?.map((e) => e.node) || []);

      // Subscribe to updates
      result?.subscribe((snapshot) => {
        setAccounts(snapshot.data?.uiapi?.query?.Account?.edges?.map((e) => e.node) || []);
      });
    }
    loadAccounts();
  }, []);

  async function handleCreateAccount(name: string) {
    try {
      // Perform the mutation
      await createAccount({ name });

      // Refresh the query to show the new record
      if (accountsResult) {
        await accountsResult.refresh();
      }
    } catch (error) {
      console.error("Failed to create account:", error);
    }
  }

  return (
    <div>
      <button onClick={() => handleCreateAccount("New Account")}>Create Account</button>
      <ul>
        {accounts.map((account) => (
          <li key={account.Id}>{account.Name?.value}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Pattern 2: Re-query After Mutation

If you don't have access to the `QueryResult`, re-execute the query.

```typescript
async function handleCreateAccount(name: string) {
  try {
    // Perform the mutation
    await createAccount({ name });

    // Re-query
    await loadAccounts();
  } catch (error) {
    console.error("Failed to create account:", error);
  }
}
```

### Pattern 3: Optimistic Updates

You can choose to update the UI before the mutation completes.

```typescript
async function handleDeleteAccount(accountId: string) {
  // Optimistically remove from UI
  setAccounts((prev) => prev.filter((a) => a.Id !== accountId));

  try {
    await deleteAccount(accountId);
    // Success - optimistic update was correct
  } catch (error) {
    console.error("Failed to delete account:", error);
    // Revert optimistic update
    if (accountsResult) {
      await accountsResult.refresh();
    }
  }
}
```

## Mutation Best Practices

Here are several best practices for working with GraphQL mutation.

### Select Id in Return Fields

Include `Id` in your mutation return fields.

```graphql
mutation CreateAccount($input: AccountCreateInput!) {
  uiapi {
    AccountCreate(input: $input) {
      Record {
        Id # Always include this
        Name {
          value
        }
      }
    }
  }
}
```

### Use Type-Safe Input Interfaces

Define interfaces for mutation inputs for type safety.

```typescript
export interface CreateContactInput {
  firstName: string;
  lastName: string;
  accountId?: string;
  email?: string;
  phone?: string;
}

export async function createContact(input: CreateContactInput) {
  // Type-safe mutation implementation
}
```

### Handle Loading States

Show loading states during mutations to notify users on what to expect.

```typescript
const [isCreating, setIsCreating] = useState(false);

async function handleCreate() {
  setIsCreating(true);
  try {
    await createAccount({ name: "New Account" });
  } finally {
    setIsCreating(false);
  }
}
```

### Provide User Feedback

Show success and error messages to communicate expectations with users.

```typescript
const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

async function handleCreate() {
  try {
    await createAccount({ name: "New Account" });
    setMessage({ type: "success", text: "Account created successfully!" });
  } catch (error) {
    setMessage({ type: "error", text: (error as Error).message });
  }
}
```

### Clean Up Form State

Reset form fields after successful mutations.

```typescript
async function handleSubmit(e: React.FormEvent) {
  e.preventDefault();
  try {
    await createAccount({ name, industry });
    // Clear form on success
    setName("");
    setIndustry("");
  } catch (error) {
    // Handle error
  }
}
```

### Batch Related Mutations

If you must perform multiple mutations, consider batching them.

```typescript
async function createAccountWithContacts(
  accountData: CreateAccountInput,
  contacts: CreateContactInput[],
) {
  // Create account first
  const account = await createAccount(accountData);

  if (!account?.Id) {
    throw new Error("Failed to create account");
  }

  // Create contacts with the new account ID
  const contactPromises = contacts.map((contact) =>
    createContact({ ...contact, accountId: account.Id }),
  );

  await Promise.all(contactPromises);

  return account;
}
```

## See Also

- [GraphQL Queries in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql.md)
- [Error Handling in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql-error.md)
- [Cache Control in Data SDK](/docs/platform/multiframework/guide/data-sdk-cache-control.md)
