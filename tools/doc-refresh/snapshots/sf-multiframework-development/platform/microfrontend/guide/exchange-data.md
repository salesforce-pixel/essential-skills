# Exchange Data Between the Page and an Embedded App

Move data both ways between Salesforce and an embedded app so the two stay in sync. The Salesforce host sends the embedded app its current data and UI state, and the embedded app sends values and events back to the host. Both directions travel over the same versioned `sf-embedding` channel, so you don't manage `postMessage` calls or origins yourself.

## How It Works

Salesforce composes a UI state for each embedded app and pushes it to the guest over the embedding protocol. The UI state carries the host-driven data your app reads, such as the `props` the page passes in and the `styles` it applies. Your app reads the current snapshot and subscribes to receive later snapshots when the data changes. Snapshots are full replacements, not diffs.

In the other direction, your app sends data and custom events back to the host. Events surface on the host `lightning-ui-embedding` element, where a Lightning web component on the page can listen for them. Every value that crosses the channel travels by structured clone.

:::important
Values that cross the channel must be structured-clone-safe. Structured clone preserves `Date`, `Map`, `Set`, and typed arrays, so a `Date` arrives as a `Date`, not as an ISO string. Don't `JSON.stringify` a payload before you send it, and don't send values that can't be cloned, such as functions or DOM nodes.
:::

## Prerequisites

- Your app is embedded with `lightning-ui-embedding` and loads successfully.
- Your app can read the platform SDK, or you build the embedding bridge yourself. See [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md) for the two configuration paths.

## Read Host Data in the Embedded App

1. In your embedded app, create the view SDK and read the current UI state. `createViewSDK` is asynchronous, so await it. `getUiState` returns the current state and a `subscribe` function you use to react to later updates.

```javascript
import "@salesforce/platform-sdk/ui-embedding";
import { createViewSDK } from "@salesforce/platform-sdk/view";

const viewSdk = await createViewSDK();

// Off an embedding surface, createViewSDK resolves to an empty object,
// so guard the call before you use it.
const uiState = viewSdk.getUiState?.();
if (uiState) {
  render(uiState.state.props);
}
```

2. Read the host-driven data from `state.props` and use it in your app.

3. Subscribe so your app updates when the host data changes. Salesforce pushes a new snapshot on every change, so reapply the values each time.

```javascript
const unsubscribe = uiState.subscribe((next) => {
  render(next.props);
});
```

:::note
There's at most one active UI-state subscription per session, and each snapshot is a full replacement of the previous one. To match the host's styling from the same UI state, see [Style an Embedded App to Match Salesforce](/docs/platform/microfrontend/guide/style-embedded-app.md).
:::

## Send Data and Events Back to the Host

Your app sends a custom event to the host, and a Lightning web component on the page listens for it. Use this to notify the page when a user selects a record, completes a step, or changes a value the page needs.

The event surfaces on the host `lightning-ui-embedding` element as a DOM event that carries your event type and detail. Add a listener to your wrapper component to receive it.

:::note
Because the embedding event names contain dots, bind them imperatively with `addEventListener` rather than declaratively with `on*` template attributes, the same way you handle the `sf-embedding.component.ready` and `sf-embedding.component.error` events in [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md).
:::

To build the data exchange yourself without a Salesforce package, send and receive the underlying `ui/events/dispatch` and `ui/subscribe/ui-state` messages directly over the protocol. See [Build the Embedding Bridge Without a Salesforce Package](/docs/platform/microfrontend/guide/package-free-bridge.md).

## Show the Embedded App in the User's Language

Your app controls its own UI, so localizing that UI is your app's job. To render in the same language as Salesforce, your app needs the host's locale. Pass it from your wrapper component to the app over the same custom-event channel you use to exchange data.

In your wrapper component, import the Salesforce locale and dispatch it to the embedding element as a custom event. Pick an event name that your app listens for, such as `localeInformation`. Add `lwc:ref` to the embedding element the same way you do to listen for its lifecycle events. Send the locale after the embedding component reports that it's ready, so the app has it before it renders.

```javascript
// myEmbeddedApp.js
import { LightningElement } from "lwc";
import locale from "@salesforce/i18n/locale";

export default class MyEmbeddedApp extends LightningElement {
  appUrl = "https://app.example.com";

  sendLocale() {
    this.refs.embedding.dispatchEvent(new CustomEvent("localeInformation", { detail: { locale } }));
  }
}
```

In your embedded app, listen for that same event, read the locale from its detail, and render your UI in that language.

:::note
Passing the locale tells your app which language to render in. Translating the app's own content, labels, and number and date formats stays your app's responsibility. The Salesforce unsaved-changes modal is already shown in the user's language.
:::

## See Also

- [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md)
- [Style an Embedded App to Match Salesforce](/docs/platform/microfrontend/guide/style-embedded-app.md)
- [Build the Embedding Bridge Without a Salesforce Package](/docs/platform/microfrontend/guide/package-free-bridge.md)
