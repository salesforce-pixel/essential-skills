# Get App Identity

Use `getCurrentApp()` to discover the identity of the app that your code runs in. The SDK resolves the running app's namespace, name, and an addressable qualified name, so you can scope requests and target features to the current app. For example, use the app identity in these cases:

- Scope a call to your app, such as when you run a CMS search
- Pass the qualified name of your app as an addressable app name

Import `getCurrentApp` from the `@salesforce/platform-sdk` package.

```typescript
import { getCurrentApp } from "@salesforce/platform-sdk";

const app = await getCurrentApp();
const identity = app.identity;
```

## getCurrentApp(options?)

Resolves the identity of the running app.

```typescript
async function getCurrentApp(options?: CurrentAppOptions): Promise<CurrentApp>;
```

### Parameters

| Parameter  | Type                | Description                                                             |
| :--------- | :------------------ | :---------------------------------------------------------------------- |
| `options?` | `CurrentAppOptions` | Optional configuration. Extends `SDKOptions` with a `surface` override. |

### Returns

```typescript
Promise<CurrentApp>
```

`getCurrentApp()` resolves to a `CurrentApp` object. If you use `getCurrentApp()` outside of a web app or micro-frontend, such as in local development, `CurrentApp` is returned without the `identity` object.

## CurrentApp Interface

Describes the running app. The `identity` object is present only when the runtime provides app identity. `identity` can be undefined, such as when it's called in local development, or if `appName` is missing.

```typescript
interface CurrentApp {
  readonly identity?: AppIdentity;
}
```

## AppIdentity Interface

Describes the identity of the running app.

```typescript
interface AppIdentity {
  namespace: string;
  appName: string;
  qualifiedName: string;
  bundleId?: string;
}
```

The `AppIdentity` interface has these properties.

| Property        | Type     | Description                                                                                            |
| :-------------- | :------- | :----------------------------------------------------------------------------------------------------- |
| `namespace`     | `string` | The app's namespace, which defaults to `c` when the org doesn't use a registered namespace.            |
| `appName`       | `string` | The developer name of the UI bundle.                                                                   |
| `qualifiedName` | `string` | The addressable app name in the format `namespace__appName`, for example, `MyNs__MyBundle`.            |
| `bundleId?`     | `string` | The record ID of the UI bundle, provided by the runtime. Defaults to `undefined` in local development. |

## Usage

Check that `identity` is defined before you use it. If an app identity isn't available, the SDK resolves to a `CurrentApp` without an `identity` object instead of throwing, so your app keeps rendering.

```typescript
import { getCurrentApp } from "@salesforce/platform-sdk";

const app = await getCurrentApp();

if (app.identity) {
  const targetIds = [app.identity.qualifiedName]; // ["MyNs__MyBundle"]
}
```

To use `bundleId`, read it with a fallback and validate it before you use it. `bundleId` defaults to `undefined` in local development.

```typescript
export async function getBundleId(): Promise<string> {
  const app = await getCurrentApp();
  return app.identity?.bundleId ?? "";
}
```

Since `getCurrentApp()` never rejects, you don't need a `.catch()` block. Handle the absence of identity in your code by checking that `identity` is defined, read `bundleId` with a fallback, and provide your default behavior when either is missing.

## Example: Use App Identity in a React Component

Resolve the app identity inside an effect, and guard the asynchronous result against a component that unmounts before the promise settles. It's recommended to gate your logic on the value as `identity` can be undefined, such as in local development or when `appName` is missing.

```typescript
import { useEffect, useState } from "react";
import { getCurrentApp } from "@salesforce/platform-sdk";

function useBundleId(): string | undefined {
  const [bundleId, setBundleId] = useState<string>();

  useEffect(() => {
    let cancelled = false;

    // getCurrentApp() resolves without rejecting, so you don't need a .catch().
    // Handle the realistic case instead: the app resolves, but identity
    // (and bundleId) can be undefined on surfaces that don't provide it.
    getCurrentApp().then((app) => {
      if (cancelled) return;

      if (!app.identity?.bundleId) {
        // No bundleId on this surface. Fall back to your default behavior.
        setBundleId(undefined);
        return;
      }

      setBundleId(app.identity.bundleId);
    });

    return () => {
      cancelled = true;
    };
  }, []);

  return bundleId;
}
```

Call `getCurrentApp()` where you need the identity. The SDK resolves the ambient app each time, so you don't cache the result in an app context or provider.

## See Also

- [Work with Data SDK](/docs/platform/multiframework/guide/data-sdk-intro.md)
- [GraphQL Queries in Data SDK](/docs/platform/multiframework/guide/data-sdk-graphql.md)
- [Access Record Data with Data SDK](/docs/platform/multiframework/guide/data-sdk-usage.md)
