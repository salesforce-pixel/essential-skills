# Warn Users About Unsaved Changes in an Embedded App (Developer Preview)

Protect users from losing unsaved work by telling Salesforce when your embedded app has unsaved changes. When the app is dirty and the user tries to navigate away, Salesforce shows a confirmation prompt.

:::note
This topic describes the Developer Preview API. Your app registers dirty state by dispatching a `trackdirtystate` event on the bridge, using the public `bridge.instanceId` value to identify the widget. In the generally available release, `instanceId` is no longer public and dirty state is registered through an SDK method instead, so this exact pattern doesn't carry forward. To move an app to the generally available version, see [Migrate from the Developer Preview API](/docs/platform/microfrontend/guide/migrate-from-dev-preview.md).
:::

## How It Works

Your embedded app tells the host when it becomes dirty or clean by dispatching a `trackdirtystate` event on the bridge. The shell forwards that event to the host platform. When a dirty app is registered and the user navigates away, the platform shows a single confirmation modal with cancel and discard options. If several embedded apps are dirty at once, the platform still shows one modal for all of them.

## Report Dirty State

When your app's state changes, dispatch a `trackdirtystate` event on the bridge. Guard the call with `bridge.isConnected()` so you only dispatch after the connection is ready.

```javascript
if (bridge.isConnected()) {
  bridge.dispatchEvent(
    new CustomEvent("trackdirtystate", {
      detail: {
        isDirty: true,
        instanceId: bridge.instanceId,
        label: "Registration form",
      },
    }),
  );
}
```

- `isDirty`: `true` when the app has unsaved changes, `false` when it's clean.
- `instanceId`: identifies the embedded app instance. Read it from `bridge.instanceId`.
- `label`: an optional, human-readable name for the app. The platform can show it in the confirmation modal so users know which app has unsaved work.

Dispatch the event again with `isDirty: false` when the user saves or the app returns to a clean state.

## Where It Works

Dirty-state protection works on Lightning Experience pages and on Experience Cloud sites, including both LWR-based and Aura-based sites.

## Known Limitations

:::note
The confirmation prompt is triggered by page navigation. Dismissing an embedded app that's hosted in a modal by clicking the modal's close (X) button isn't a navigation, so it doesn't trigger the prompt. If you embed an app in a modal, implement your own unsaved-changes check on modal close.
:::

## See Also

- [Embed an External Web App (Developer Preview)](/docs/platform/microfrontend/guide/dp-embed-external-web-app.md)
- [Exchange Data Between the Page and an Embedded App (Developer Preview)](/docs/platform/microfrontend/guide/dp-exchange-data.md)
