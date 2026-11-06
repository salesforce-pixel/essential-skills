# Make an Embedded App Accessible to Screen Reader Users (Developer Preview)

Give an embedded app an accessible name so screen reader users understand what the embedded region contains, and let users move into and out of the app with the keyboard.

:::note
This topic describes the Developer Preview API. The accessible name is set through `shell.title`. In the generally available release, this becomes a plain `title` attribute on the `<lightning-ui-embedding>` component. To move an app to the generally available version, see [Migrate from the Developer Preview API](/docs/platform/microfrontend/guide/migrate-from-dev-preview.md).
:::

## How It Works

Salesforce renders your embedded app in an iframe. An iframe needs an accessible name so screen readers can announce the region instead of leaving it unlabeled. You set a descriptive name on the shell, and the shell applies it to the iframe as its title. Keyboard users tab into and out of the embedded app in natural document order, using the browser's built-in iframe tabbing.

## Set the Accessible Name

Set a descriptive name on the shell's `title` property. Screen readers announce this name when users reach the embedded region.

```javascript
shell.title = "Loan application";
```

Use a name that describes the app's purpose, such as "Loan application" or "Order status", so users know what the region does before they enter it.

## Keyboard Navigation

Users move through the embedded app in natural tab order. The host relies on the browser's native iframe tabbing rather than a custom focus manager, so focus flows into the app and back out to the page as users tab.

## See Also

- [Embed an External Web App (Developer Preview)](/docs/platform/microfrontend/guide/dp-embed-external-web-app.md)
- [Warn Users About Unsaved Changes in an Embedded App (Developer Preview)](/docs/platform/microfrontend/guide/dp-track-unsaved-changes.md)
