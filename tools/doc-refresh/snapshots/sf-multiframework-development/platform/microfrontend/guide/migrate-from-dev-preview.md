# Migrate from the Developer Preview API

UI Embedding was first released as a Developer Preview. The generally available version changes the host element, how you pass the app URL, and how the host communicates with the embedded app. If you built an embedding against the Developer Preview, use this guide to move to the generally available component.

:::important
The Developer Preview and generally available APIs aren't compatible. An app built for one doesn't run under the other without the changes described here.
:::

## What Changed

| Area                      | Developer Preview                     | Generally Available                                                          |
| ------------------------- | ------------------------------------- | ---------------------------------------------------------------------------- |
| Host element              | `<lwc-shell>`                         | `<lightning-ui-embedding>`                                                   |
| App URL                   | Set through the shell's configuration | `src` attribute (required, read once at mount)                               |
| Host-to-app communication | Imperative `bridge` object            | DOM events on the host element and the `sf-embedding` protocol channel       |
| Lifecycle signals         | `bridge` callbacks                    | `sf-embedding.component.ready` and `sf-embedding.component.error` DOM events |

## Update the Host Element

Replace the Developer Preview host element with `lightning-ui-embedding`, and move the app URL to the `src` attribute.

Before (Developer Preview):

```html
<template>
  <lwc-shell></lwc-shell>
</template>
```

After (generally available):

```html
<template>
  <lightning-ui-embedding src="{appUrl}"></lightning-ui-embedding>
</template>
```

The `src` attribute is required and binds the session to a specific app. Salesforce reads it once when the component mounts. Don't change `src`, `sandbox`, or `removeSandboxTokens` after the component renders. The host rejects a mid-session change with a `SESSION_BINDING_MUTATED` error.

## Replace the Imperative Bridge with DOM Events

The Developer Preview exposed an imperative `bridge` object for communication. The generally available version uses DOM events on the host element for lifecycle signals.

Listen for these events on `lightning-ui-embedding`:

- `sf-embedding.component.ready` fires when the embedded app finishes the handshake and is ready.
- `sf-embedding.component.error` fires when embedding fails. The event detail includes the `phase` (`configuration` or `bootstrap`), a `code`, a `message`, and a `retryable` flag. See [UI Embedding Error Codes](https://developer.salesforce.com/docs/platform/microfrontend/references/microfrontend-error-codes/error-codes.md).

These event names contain dots, so you can't bind them declaratively with `on*` attributes in the template. Add `lwc:ref` to the embedding element and attach the listeners imperatively in `renderedCallback`.

```html
<!-- myEmbeddedApp.html -->
<template>
  <lightning-ui-embedding src="{appUrl}" lwc:ref="embedding"></lightning-ui-embedding>
</template>
```

```javascript
// myEmbeddedApp.js
import { LightningElement } from "lwc";

export default class MyEmbeddedApp extends LightningElement {
  appUrl = "https://app.example.com";
  hasWiredEvents = false;

  renderedCallback() {
    if (this.hasWiredEvents) {
      return;
    }
    this.hasWiredEvents = true;

    const el = this.refs.embedding;
    el.addEventListener("sf-embedding.component.ready", this.handleReady);
    el.addEventListener("sf-embedding.component.error", this.handleError);
  }

  handleReady = () => {
    // The embedded app is ready.
  };

  handleError = (event) => {
    const { code, message } = event.detail;
    // Handle the failure.
  };
}
```

## Update Data Exchange, Styling, and Resizing

In the generally available version, the page and the embedded app exchange state through the embedding's typed channel rather than the Developer Preview `bridge`. Review these tasks for the current approach:

- [Style an Embedded App to Match Salesforce](/docs/platform/microfrontend/guide/style-embedded-app.md)
- [Resize an Embedded App to Fit Its Content](/docs/platform/microfrontend/guide/resize-embedded-app.md)
- [Track Unsaved Changes in an Embedded App](/docs/platform/microfrontend/guide/track-unsaved-changes.md)

## Next Steps

- [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md) for the full generally available setup path.
- [UI Embedding Error Codes](https://developer.salesforce.com/docs/platform/microfrontend/references/microfrontend-error-codes/error-codes.md) to handle failures in your event listeners.
