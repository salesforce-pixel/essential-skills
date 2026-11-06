# Embed an External Web App (Developer Preview)

Embed an externally hosted web app inside a Salesforce page with the `<lwc-shell>` host component. Salesforce loads your app in a sandboxed iframe and manages the connection between the page and your app.

:::note
This topic describes the Developer Preview API (`<lwc-shell>`, package `@salesforce/experimental-mfe-lwc-shell`). The generally available release replaces this with the `<lightning-ui-embedding>` component and a different SDK. Treat every API name in this topic as Developer Preview only. To move an app to the generally available version, see [Migrate from the Developer Preview API](/docs/platform/microfrontend/guide/migrate-from-dev-preview.md).
:::

## How It Works

Salesforce embeds your externally hosted app in an iframe managed by the `<lwc-shell>` custom element. You generate a deployable Lightning web component from the shell package, wrap it in your own component, point it at your app's URL, and add it to the page. The shell applies a sandbox policy to the iframe and opens a message channel to your app.

## Prerequisites

- An externally hosted web app served over HTTPS.
- The `@salesforce/experimental-mfe-lwc-shell` package (Developer Preview).
- Permission to create Lightning web components and edit Lightning pages in your org.

## Generate the Deployable Component

Run the vendor build to generate a deployable Lightning web component from the shell package.

```bash
npx lwc-shell-vendor-build
```

This creates a component at `force-app/main/default/lwc/vendorLwcShell/` that you can deploy and reference from your wrapper component.

## Create the Shell in a Wrapper Component

Create the shell imperatively, and set its attributes before you add it to the DOM.

```javascript
const shell = document.createElement("lwc-shell");
shell.title = "Loan application";
shell.src = appUrl;
shell.sandbox = "allow-forms allow-modals";
container.appendChild(shell);
```

:::important
Create the shell with `document.createElement('lwc-shell')` and set `src`, `title`, and any `sandbox` tokens before you call `appendChild`. A declarative `<lwc-shell>` tag placed directly in an LWC template doesn't upgrade to the custom element, so the imperative pattern is required.
:::

## Sandbox Policy

The shell applies a tiered iframe sandbox policy:

- **Base tokens**, always applied: `allow-scripts`, `allow-pointer-lock`, `allow-same-origin`.
- **Optional tokens**, which you opt into through the `sandbox` attribute: `allow-forms`, `allow-modals`, `allow-downloads`.
- **Blocked tokens**, which the host removes even if you request them: `allow-top-navigation`, `allow-popups`.

The host blocks `allow-top-navigation` and `allow-popups` so an embedded app can't navigate the top-level window or escape the sandbox through a popup.

:::warning
`allow-same-origin` for a third-party embedded app works only on Experience Cloud sites that have Locker or Lightning Web Security disabled. It doesn't work on Lightning Experience pages in Developer Preview. Cookies and `localStorage` in the embedded app depend on `allow-same-origin`, so they're subject to the same limitation. This limitation is resolved in the generally available release, where the shell becomes a first-party component.
:::

## Allowlist Your App's Domain

Before Salesforce can load your app, add your app's domain to the org's allowlist in Setup.

## See Also

- [Exchange Data Between the Page and an Embedded App (Developer Preview)](/docs/platform/microfrontend/guide/dp-exchange-data.md)
- [Match an Embedded App to the Salesforce Theme (Developer Preview)](/docs/platform/microfrontend/guide/dp-style-embedded-app.md)
