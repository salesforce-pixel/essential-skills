# Get Started with UI Embedding

Embed an existing external web app directly in Salesforce so your users work in one place instead of switching to a separate tab or window. With UI Embedding, Salesforce hosts your app inside a secure, sandboxed iframe by using the `lightning-ui-embedding` base component. This guide sets up the shared foundation, then walks you through the two configuration paths so you can choose the one that fits your project.

:::note
UI Embedding was previously available as a Developer Preview. The Developer Preview used a different host element and setup flow. If you built against the preview, see [Migrate from the Developer Preview API](/docs/platform/microfrontend/guide/migrate-from-dev-preview.md) before you move to the generally available version.
:::

## Prerequisites

- Your web app is hosted at an HTTPS URL that you control.
- You have permission to create Lightning web components and edit Lightning pages or Experience Cloud sites in your Salesforce org.
- Your Salesforce org is on a release where UI Embedding is generally available. You don't need to set a specific API version on the `lightning-ui-embedding` component.
- UI Embedding is available in Enterprise, Performance, Unlimited, Developer, and Partner Developer editions, in orgs hosted on Hyperforce where English is the default language.

## Choose a Configuration Path

You embed an app the same way in every case: you trust the app's domain, add the `lightning-ui-embedding` component to a page, and point it at your app. What differs is how your app talks back to Salesforce. Pick the path that matches how much you want to depend on a Salesforce package.

| Path                         | Use when                                                                                                                      | How the app communicates                                                                       |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| With a Salesforce package    | You want the fastest setup and a supported, typed API.                                                                        | Your app imports the platform SDK, which manages the communication channel for you.            |
| Without a Salesforce package | You can't or don't want to add a Salesforce package to your app's build, or you want full control of the communication layer. | Your app implements the `sf-embedding` protocol directly over the channel Salesforce provides. |

Both paths use the same host component and the same underlying protocol, so you can start with one and move to the other later without re-architecting the embedding.

## Trust Your App's Domain

This step is the same for both paths. Salesforce loads your app in an iframe, so you first tell Salesforce to trust your app's origin. From Setup, add your app's origin to your trusted URL settings for inline frames.

:::important
Use the exact origin that serves your app, including the scheme and any subdomain. An origin that doesn't match the app's real origin prevents the app from loading. The app's origin must also differ from your Salesforce org's origin. A same-origin `src` is rejected with a `SAME_ORIGIN_SRC` error, so host the app on a different origin.
:::

## Add the Embedding Component

This step is also the same for both paths. Create a Lightning web component that renders `lightning-ui-embedding` and points it at your app's URL.

1. In your Salesforce DX project, create a Lightning web component. This component is a thin wrapper around the embedding component.
2. In the component's template, add `lightning-ui-embedding` and set the required `src` attribute to your app's URL.

```html
<!-- myEmbeddedApp.html -->
<template>
  <lightning-ui-embedding src="{appUrl}"></lightning-ui-embedding>
</template>
```

```javascript
// myEmbeddedApp.js
import { LightningElement } from "lwc";

export default class MyEmbeddedApp extends LightningElement {
  appUrl = "https://app.example.com";
}
```

:::note
This code is a starting sketch. Replace `https://app.example.com` with your app's URL. To give the embedded frame an accessible name, set the `title` attribute; if you don't, the frame uses the default name `Embedded widget`.
:::

The `src` attribute is required, and Salesforce reads it when the component mounts. Because `src` binds the session to a specific app, don't change it after the component renders. This is enforced: changing `src` (or `sandbox`) after mount fires an `sf-embedding.component.error` with the code `SESSION_BINDING_MUTATED`. To load a different URL, unmount and remount the component.

Then place your wrapper on a page like any other Lightning web component.

1. Open Lightning App Builder for a Lightning page, or open your Experience Cloud site in Experience Builder.
2. Drag your custom component onto the page.
3. Save and activate the page.

Your embedded app now renders inside Salesforce. Next, choose a configuration path to connect your app to Salesforce.

## Path 1: Configure With a Salesforce Package

On this path, your app depends on the Salesforce platform SDK, which manages the communication channel for you. You get a supported, typed API for the lifecycle, UI state, resizing, and dirty-state features without writing any protocol code.

1. Add the platform SDK to your app and import the UI Embedding entry point.

```javascript
import "@salesforce/platform-sdk/ui-embedding";
```

2. Handle the component's ready and error lifecycle events on your wrapper. The embedding component reports its lifecycle through DOM events, so listen for them so your wrapper can respond when the app is ready or when embedding fails.

- `sf-embedding.component.ready` fires when the embedded app finishes loading and is ready to interact with Salesforce.
- `sf-embedding.component.error` fires when embedding fails. The event detail includes the phase (`configuration` or `bootstrap`), an error code, a message, and whether the error is retryable. For the full list of codes, see [UI Embedding Error Codes](https://developer.salesforce.com/docs/platform/microfrontend/references/microfrontend-error-codes/error-codes.md).

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

3. In your embedded app, create the view SDK to read UI state and use the embedding features. `createViewSDK` is asynchronous, and off an embedding surface it resolves to an empty object, so guard the calls you make on it.

```javascript
import { createViewSDK } from "@salesforce/platform-sdk/view";

const viewSdk = await createViewSDK();
const uiState = viewSdk.getUiState?.();
```

With the view SDK in place, continue with the common tasks:

- [Exchange Data Between the Page and an Embedded App](/docs/platform/microfrontend/guide/exchange-data.md)
- [Style an Embedded App to Match Salesforce](/docs/platform/microfrontend/guide/style-embedded-app.md)
- [Resize an Embedded App to Fit Its Content](/docs/platform/microfrontend/guide/resize-embedded-app.md)
- [Warn Users About Unsaved Changes in an Embedded App](/docs/platform/microfrontend/guide/track-unsaved-changes.md)

## Path 2: Configure Without a Salesforce Package

On this path, your app doesn't take a dependency on any Salesforce package. Instead, your app implements the `sf-embedding` protocol directly: it completes the handshake, then sends and receives the protocol messages itself. Choose this path when you can't add a Salesforce package to your app's build, or when you want full control of the communication layer.

The `lightning-ui-embedding` component and the domain-trust and page setup are identical to the with-package path. The difference is entirely inside your app, where you build the communication bridge by hand.

For the full walkthrough, including the handshake, the protocol message catalog, error handling, and security requirements, see [Build the Embedding Bridge Without a Salesforce Package](/docs/platform/microfrontend/guide/package-free-bridge.md).

## Scaffold a Starter Component from the CLI

Instead of writing the wrapper by hand, generate one with the Salesforce CLI. The `sf template generate ui-embedding` command scaffolds an embedding-ready Lightning web component bundle.

```bash
sf template generate ui-embedding --name myEmbeddedApp --src https://app.example.com
```

The command creates a Lightning web component bundle configured for embedding. The bundle includes the HTML, JavaScript, metadata, and CSS files. Then edit the generated component and add it to a page as described earlier.

:::note
This command requires a recent version of the Salesforce CLI. If the command isn't available, update the CLI, then run `sf template generate ui-embedding --help` to see the current flags and syntax.
:::

## See Also

- [Exchange Data Between the Page and an Embedded App](/docs/platform/microfrontend/guide/exchange-data.md)
- [Build the Embedding Bridge Without a Salesforce Package](/docs/platform/microfrontend/guide/package-free-bridge.md)
- [UI Embedding Error Codes](https://developer.salesforce.com/docs/platform/microfrontend/references/microfrontend-error-codes/error-codes.md)
