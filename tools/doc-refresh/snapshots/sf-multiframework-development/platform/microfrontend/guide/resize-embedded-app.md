# Resize an Embedded App to Fit Its Content

Avoid inner scrollbars and clipped content by letting the embedding frame grow and shrink to fit your app. The embedded app reports its size to Salesforce, and Salesforce sizes the iframe to match, so your app renders as if it were a native part of the page.

## How It Works

The embedded app (the guest) reports its height to Salesforce through the embedding protocol. Salesforce applies that height to the iframe. Automatic height reporting is on by default: the embedding resizer starts when your app bootstraps (when you import `@salesforce/platform-sdk/ui-embedding`) and reports the new height as your content changes. There's no SDK method to turn it on or configure it. You can also report a size yourself with the view SDK, which layers on top of the resizer, for example to set an explicit width.

## Prerequisites

- Your app is embedded with `lightning-ui-embedding` and loads successfully.

## Report the Size

To report your app's size directly, call `resize` from the view SDK. Pass the width and height as pixel strings, such as `"480px"`. Pass an empty string for an axis you don't want to change.

```javascript
import "@salesforce/platform-sdk/ui-embedding";
import { createViewSDK } from "@salesforce/platform-sdk/view";

const viewSdk = await createViewSDK();

// Set the height and leave the width unchanged.
await viewSdk.resize?.("", "480px");
```

You don't need to enable automatic height reporting. The embedding resizer runs by default and reports the new height whenever your content changes, so it settles on the right height on its own.

:::important
Avoid full-viewport height styles, such as `height: 100vh` or `min-height: 100vh`, in your embedded app. Inside the iframe, `100vh` resolves to the iframe's own current height, not the height of the full Salesforce page. So a full-viewport height can't grow to fit your content and usually just clips it.
:::

## See Also

- [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md)
- [Style an Embedded App to Match Salesforce](/docs/platform/microfrontend/guide/style-embedded-app.md)
