# Create a Data SDK Extension

Package your own reusable data logic behind a typed API on the SDK instance by authoring a custom extension. With an extension, you can:

- Wrap repeated GraphQL queries, a caching layer, a custom API client, telemetry, and so on into one reusable namespace instead of duplicating them.
- Get full type safety via `sdk.ext` for each extension's return type. Duplicate names or non-literal names are rejected at compile time.
- Isolate your capabilities from SDK evolution under the `sdk.ext` namespace, so you get future SDK changes easily.

## Define an Extension

Define a custom extension with `defineDataExtension`. Provide a name for your extension, and a `setup` function that receives the resolved `DataSDK` instance. `setup` can be synchronous or asynchronous, so you can `await` a dynamic import or a GraphQL query before you return the API.

```typescript
import { createDataSDK } from "@salesforce/platform-sdk/data";
import { defineDataExtension, type DataSDK } from "@salesforce/platform-sdk";

interface AccountApi {
  getName?(recordId: string): Promise<string | undefined>;
}

// The payload shape of the GraphQL query, as it appears under `data`.
interface AccountNameResult {
  uiapi: { query: { Account: { edges: { node: { Name: { value: string } } }[] } } };
}

const accountExtension = defineDataExtension({
  name: "account",
  setup: (sdk: DataSDK): AccountApi => {
    // GraphQL isn't available on every surface, so check for it during setup.
    // Omit getName when it isn't supported instead of returning undefined at call time.
    const graphql = sdk.graphql;
    if (!graphql) return {};

    return {
      async getName(recordId) {
        const result = await graphql.query<AccountNameResult>({
          query: GET_ACCOUNT_NAME,
          variables: { recordId },
        });
        return result?.data?.uiapi.query.Account.edges[0]?.node.Name.value;
      },
    };
  },
});

// Attach the extension, then call it under sdk.ext.
// getName is optional, so guard the call: it's absent when GraphQL isn't supported.
const sdk = await createDataSDK({ extensions: [accountExtension] });
const name = await sdk.ext.account.getName?.("001xx000003DGb2AAG");
```

Pass the `extensions` array inline, as in the example, so that the SDK types `sdk.ext.<name>` for each extension you attach. If you assign the array to a variable first, add `as const` to keep the `sdk.ext` types.

## defineDataExtension Fields

| Field           | Type                                    | Description                                                                                                                                                                                                                                                                                                            |
| :-------------- | :-------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`          | `string`                                | The name to refer to the extension using the `sdk.ext.<name>` format.                                                                                                                                                                                                                                                  |
| `setup`         | `(sdk: DataSDK) => Api \| Promise<Api>` | Builds the extension API. Runs when you create the SDK instance, with the resolved `DataSDK` passed in. Returns the API object under `name`.                                                                                                                                                                           |
| `minApiVersion` | `string`                                | Optional. The earliest Salesforce API version the extension supports, such as `"64.0"`. Specify an API version when the extension depends on a data shape or capability from a specific API version. See [Set a Minimum API Version](/docs/platform/multiframework/guide/data-sdk-intro.md#set-a-minimum-api-version). |

## Attach an Extension

Attach extensions by passing them to `createDataSDK()` in the `extensions` array. The SDK builds each extension's API when you create the instance, so the extensions are ready to use with `createDataSDK()`. Call an extension's API under the SDK's `ext` namespace using `sdk.ext.<name>`.

```typescript
import { createDataSDK } from "@salesforce/platform-sdk/data";
import { labels } from "@salesforce/platform-sdk/data/extensions";

const sdk = await createDataSDK({ extensions: [labels({ namespace: "MyApp" })] });

// Call the extension API under sdk.ext
const greeting = await sdk.ext.labels.get?.("Greeting_Label");
```

Pass the `extensions` array inline, as in the example, so that the SDK types `sdk.ext.<name>` for each extension you attach. If you assign the array to a variable first, add `as const` to keep the `sdk.ext` types.

## Specify Unique API Names

Add each extension using a unique API name. If two extensions use the same `name`, attach one with an alias so each has a distinct key. Pass `{ extension, as }` instead of the bare extension, and call the aliased extension under its `as` key.

```typescript
const sdk = await createDataSDK({
  extensions: [labels({ namespace: "MyApp" }), { extension: partnerLabels, as: "partnerLabels" }],
});

sdk.ext.labels.get?.("Greeting_Label");
sdk.ext.partnerLabels.get?.("Partner_Greeting");
```

## Set a Minimum API Version

An extension can declare a `minApiVersion`, the earliest Salesforce API version it supports. `minApiVersion` indicates whether the server operations the extension uses are supported at the resolved Salesforce API version. It's distinct from runtime capability checks, which determine whether functionality such as `graphql` or `fetch` is available on the surface.

When an extension declares `minApiVersion` and the runtime supplies an API version, `createDataSDK()` checks the `minApiVersion` against the API version the SDK resolves for the surface. If the resolved version is lower than the extension's `minApiVersion`, `createDataSDK()` rejects with an error and doesn't attach any extension in the array. If the runtime doesn't supply an API version, `createDataSDK()` skips the comparison.

```typescript
const sdk = await createDataSDK({
  extensions: [labels()], // requires API version 64.0 or later
});
```

## See Also

- [Data SDK Extensions](/docs/platform/multiframework/guide/data-sdk-extension.md)
- [Get Custom Labels with the Labels Extension](/docs/platform/multiframework/guide/data-sdk-extension-label.md)
- [Work with Data SDK](/docs/platform/multiframework/guide/data-sdk-intro.md)
- [GraphQL Queries in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql.md)
