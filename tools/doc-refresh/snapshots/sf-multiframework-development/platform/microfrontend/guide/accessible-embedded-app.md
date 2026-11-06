# Make an Embedded App Accessible to Screen Reader Users

Give an embedded app an accessible name so screen reader users understand what the embedded region contains. The embedding component exposes this name to assistive technology, and screen readers announce it when users reach the embedded region.

## How It Works

Salesforce renders your embedded app inside an iframe. An iframe needs an accessible name so that screen readers can announce the region instead of leaving it unlabeled. You set a descriptive name on the embedding component, and Salesforce applies it to the frame.

:::note
The generally available embedding component passed accessibility review with no violations. Focus moving into and out of the iframe is handled natively by the browser through standard iframe tabbing. The component doesn't add a custom focus manager.
:::

:::note
Salesforce gives the embedded frame an accessible name and relies on native browser focus, but accessibility of the app *inside* the iframe is your responsibility as the app owner. Make sure your app's own semantics are accessible: headings, ARIA, keyboard operability, color contrast, and applying the forwarded `lang` and `dir` attributes.
:::

## Prerequisites

- Your app is embedded with `lightning-ui-embedding` and loads successfully.

## Set the Accessible Name

Set a descriptive name on the embedding component. Screen readers announce this name when users reach the embedded region.

```html
<!-- myEmbeddedApp.html -->
<template>
  <lightning-ui-embedding src="{appUrl}" title="Loan application"> </lightning-ui-embedding>
</template>
```

Use a name that describes the app's purpose, such as "Loan application" or "Order status", so users know what the region does before they enter it.

If you don't set `title`, the frame uses the default accessible name `Embedded widget`. Set a specific `title` so screen reader users hear a name that reflects your app.

## See Also

- [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md)
