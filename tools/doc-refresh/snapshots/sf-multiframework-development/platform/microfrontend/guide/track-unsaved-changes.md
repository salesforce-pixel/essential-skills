# Track Unsaved Changes in an Embedded App

When a user edits data inside an embedded app and then tries to navigate away, Salesforce shows its standard unsaved-changes warning. It's the same prompt users see on native Salesforce pages. Your embedded app tells Salesforce when it has unsaved work, and the platform handles the confirmation prompt.

## How It Works

From inside the embedded app (the guest), you use the view SDK to mark the view as dirty when the user makes an unsaved change, and to clear that state when the user saves. Salesforce re-bubbles this state to the platform navigation guard, which shows the standard confirmation when the user navigates away. Your app doesn't manage the browser's `beforeunload` event. The platform does that.

## Prerequisites

- Your app is embedded with `lightning-ui-embedding` and loads successfully.
- Your app runs in Lightning Experience or an LWR-based Experience Cloud site. These surfaces observe the dirty-state signal natively.

:::note
Dirty-state tracking isn't supported in the Salesforce mobile app.
:::

## Mark and Clear the Dirty State

1. In your embedded app, import and create the view SDK.

```javascript
import "@salesforce/platform-sdk/ui-embedding";
import { createViewSDK } from "@salesforce/platform-sdk/view";

const viewSdk = await createViewSDK();
```

2. When the user makes an unsaved change, mark the view as dirty.

```javascript
await viewSdk.markDirtyState?.("profileForm");
```

3. When the user saves, clear the dirty state.

```javascript
await viewSdk.clearDirtyState?.("profileForm");
```

The `label` argument identifies a specific region of unsaved work, so you can track more than one independently.

:::note
On an embedding surface, `markDirtyState` and `clearDirtyState` are always available. Off an embedding surface, `createViewSDK` resolves to an empty object and these methods are `undefined`. Guard every call with optional chaining, as shown with `viewSdk.markDirtyState?.(...)`, so your app works predictably across surfaces.
:::

## Known Limitation

The unsaved-changes confirmation doesn't appear when a user closes an embedded app that's inside a modal by clicking the modal's close (X) button. Dismissing a modal isn't a navigation, so the platform navigation guard doesn't run. If your app runs inside a modal, implement your own confirm-on-close.

## See Also

- [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md)
