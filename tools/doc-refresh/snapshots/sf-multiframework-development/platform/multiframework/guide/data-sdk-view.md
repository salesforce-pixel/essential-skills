# Manage the Host UI

Use the View SDK to interact with the host's UI layer from a UI bundle.
The host is the application that embeds and runs your UI bundle, such as a parent Lightning web component that embeds your app or an agent host. The View SDK is how your app coordinates with that host.

With the View SDK, you can display alerts, toasts, and modals, read and subscribe to host UI state, For example, you can also get the current theme, mark unsaved changes, exchange events with the host, and more.

Create an instance with `createViewSDK()`, then call its methods under the returned SDK.

```typescript
import { createViewSDK } from "@salesforce/platform-sdk";

const viewSDK = await createViewSDK();

await viewSDK.displayToast?.({
  message: "Operation completed successfully",
  level: "success",
});
```

Every method is optional and resolves only on surfaces that support it. On web apps without an embedding host, `createViewSDK()` returns an empty SDK and doesn't return an error. Use optional chaining (`viewSDK.displayToast?.(...)`) to account for the absence of a host UI.

## createViewSDK(options?)

Creates and initializes a View SDK instance.

```typescript
async function createViewSDK(options?: ViewSDKOptions): Promise<ViewSDK>;
```

### Parameters

| Parameter  | Type             | Description                                                             |
| :--------- | :--------------- | :---------------------------------------------------------------------- |
| `options?` | `ViewSDKOptions` | Optional configuration. Extends `SDKOptions` with a `surface` override. |

### Returns

```typescript
Promise<ViewSDK>
```

`createViewSDK()` never rejects on an unusable surface. Every surface degrades to an empty SDK so that the embedding host always renders.

## Get a Shared Instance

To reuse one View SDK instance across your app, use `getViewSDK()`. It creates the instance on the first call and returns the same cached instance on later calls. Only the first call's `options` take effect.

```typescript
import { getViewSDK } from "@salesforce/platform-sdk";

const viewSDK = await getViewSDK();
```

Where an async call isn't available, use `getViewSDKSync()`. It returns the resolved instance if `getViewSDK()` has already completed, or `null` if the instance isn't ready.

```typescript
import { getViewSDKSync } from "@salesforce/platform-sdk";

const viewSDK = getViewSDKSync();
if (viewSDK) {
  const theme = viewSDK.getTheme?.();
}
```

## ViewSDK Interface

The API returned by `createViewSDK()`. All methods are optional and are absent on a surface that doesn't support them. The View SDK is also a DOM `EventTarget`, so it optionally exposes `addEventListener`, `removeEventListener`, and `dispatchEvent`.

| Method            | Description                                                                                             |
| :---------------- | :------------------------------------------------------------------------------------------------------ |
| `displayAlert`    | Displays a modal alert that requires user acknowledgment. Use it for important messages.                |
| `displayToast`    | Displays a non-blocking toast that auto-dismisses. Use it for confirmations and status updates.         |
| `displayModal`    | Displays a modal dialog with custom HTML loaded from a UI resource.                                     |
| `navigateTo`      | Navigates to a URL in the host environment.                                                             |
| `markDirtyState`  | Notifies the host that the app has unsaved changes.                                                     |
| `clearDirtyState` | Notifies the host that all changes are saved.                                                           |
| `getUiState`      | Returns the current host UI state snapshot and a `subscribe` function for future changes.               |
| `getTheme`        | Returns the current theme (`light` or `dark`), or `null` if the host doesn't provide theme information. |
| `resize`          | Requests the host to resize the app container.                                                          |

## displayAlert()

Displays a modal alert in the host environment. Alerts block interaction until the user acknowledges them.

```typescript
displayAlert?(options: AlertOptions): Promise<void>;
```

`AlertOptions` has a required `message` string and an optional `level` of `"info"`, `"success"`, `"warning"`, or `"error"`. The `level` defaults to `"info"`.

```typescript
await viewSDK.displayAlert?.({
  message: "Save your work before continuing.",
  level: "warning",
});
```

## displayToast()

Displays a non-blocking toast notification that dismisses automatically.

```typescript
displayToast?(options: ToastOptions): Promise<void>;
```

`ToastOptions` has the same shape as `AlertOptions`: a required `message` and an optional `level`.

```typescript
await viewSDK.displayToast?.({
  message: "File uploaded successfully.",
  level: "success",
});
```

## displayModal()

Displays a modal dialog with custom HTML loaded from a UI resource.

```typescript
displayModal?(options: ModalOptions): Promise<void>;
```

| Parameter            | Type                      | Description                                                                           |
| :------------------- | :------------------------ | :------------------------------------------------------------------------------------ |
| `componentReference` | `string`                  | URI of the HTML template to load, in the format `ui://widget/[name].html`.            |
| `params`             | `Record<string, unknown>` | Optional. Parameters passed to the modal template, accessible through the host's API. |

```typescript
await viewSDK.displayModal?.({
  componentReference: "ui://widget/settings.html",
  params: { theme: "dark" },
});
```

## navigateTo()

Navigates to a URL in the host environment. The exact behavior depends on the surface, such as a full-page navigation or an iframe navigation.

```typescript
navigateTo?(url: string): Promise<void>;
```

```typescript
await viewSDK.navigateTo?.("/dashboard");
```

## markDirtyState()

Notifies the host that the app has unsaved changes. When the state is dirty, the host can show an indicator and warn the user before they navigate away. Pass an optional `label` to track multiple concurrent dirty regions.

```typescript
markDirtyState?(label?: string): Promise<void>;
```

```typescript
form.addEventListener("input", () => viewSDK.markDirtyState?.("PrimaryForm"));
```

## clearDirtyState()

Notifies the host that the app's unsaved changes are resolved. Pass the same `label` that you passed to `markDirtyState()` to clear that dirty region.

```typescript
clearDirtyState?(label?: string): Promise<void>;
```

```typescript
async function saveForm(data) {
  await api.save(data);
  await viewSDK.clearDirtyState?.("PrimaryForm");
}
```

## getUiState()

Returns the current host UI state snapshot and a `subscribe` function for future changes. The snapshot has `props`, the host-configurable inputs such as theme, locale, and mode, and `styles`, the CSS custom properties and attributes the host mirrors onto the surface. Call `subscribe` with a handler to be notified on each later host push. `subscribe` returns an `unsubscribe` function that detaches that one handler.

```typescript
getUiState?<State extends UiState = UiState>(): {
  state: State;
  subscribe: (handler: (state: State) => void) => () => void;
};
```

```typescript
const { state, subscribe } = viewSDK.getUiState?.() ?? {
  state: { props: {}, styles: {} },
  subscribe: () => () => {},
};

applyProps(state.props);
const unsubscribe = subscribe((next) => applyProps(next.props));
// Call unsubscribe() when you no longer need updates.
```

To type the snapshot for a known host contract, pass a type that extends `UiState` as the type parameter. `State` is erased at runtime, so pin only what the host guarantees.

## getTheme()

Returns the current theme, or `null` if the host doesn't provide theme information. `getTheme()` is the synchronous sibling of the theme data in `getUiState()`.

```typescript
getTheme?(): Theme | null;
```

```typescript
const theme = viewSDK.getTheme?.();
if (theme) {
  document.body.classList.toggle("dark", theme.mode === "dark");
}
```

### resize()

Requests the host to resize the app container. Pass a width and a height as CSS length strings, or `"auto"` to size to the content.

```typescript
resize?(width: string, height: string): Promise<void>;
```

```typescript
await viewSDK.resize?.("800px", "600px");
await viewSDK.resize?.("auto", "auto");
```

## Exchange Events with the Host

The View SDK is a DOM `EventTarget`. On surfaces backed by a host bridge, `dispatchEvent` notifies local listeners and forwards the event to the host, and events the host pushes are re-dispatched onto the SDK so `addEventListener` hears them. The result is one unified stream of host-pushed and same-document events.

The `EventTarget` members are optional, because a surface without an event bus is a bare SDK. Feature-detect before you use them.

```typescript
viewSDK.addEventListener?.("user-action", (e) => {
  console.log("received:", (e as CustomEvent).detail);
});

viewSDK.dispatchEvent?.(new CustomEvent("user-action", { detail: { action: "click" } }));
```

## Example: React to the Host Theme in a React Component

This example reads the theme inside an effect and subscribes to later changes. Guard the async result against a component that unmounts before the promise settles, and detach the subscription on cleanup.

```typescript
import { useEffect, useState } from "react";
import { createViewSDK, type ThemeMode } from "@salesforce/platform-sdk";

function useHostTheme(): ThemeMode {
  const [mode, setMode] = useState<ThemeMode>("light");

  useEffect(() => {
    let cancelled = false;
    let unsubscribe: (() => void) | undefined;

    createViewSDK().then((viewSDK) => {
      if (cancelled) return;

      const initial = viewSDK.getTheme?.();
      if (initial) setMode(initial.mode);

      const uiState = viewSDK.getUiState?.();
      unsubscribe = uiState?.subscribe((next) => {
        const themeMode = next.props.theme;
        if (themeMode === "light" || themeMode === "dark") setMode(themeMode);
      });
    });

    return () => {
      cancelled = true;
      unsubscribe?.();
    };
  }, []);

  return mode;
}
```

## See Also

- [Work with the Data SDK](/docs/platform/multiframework/guide/data-sdk-intro.md)
- [App Identity](/docs/platform/multiframework/guide/data-sdk-identity.md)
- [Style Your React Apps](/docs/platform/multiframework/guide/mfw-styling.md)
