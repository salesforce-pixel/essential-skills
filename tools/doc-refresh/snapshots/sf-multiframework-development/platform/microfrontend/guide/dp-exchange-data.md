# Exchange Data Between the Page and an Embedded App (Developer Preview)

Pass data from the Salesforce page to your embedded app, and respond in the page to events your app raises. The `<lwc-shell>` host and the `@salesforce/experimental-mfe-bridge` running inside your app exchange messages across the iframe boundary.

:::note
This topic describes the Developer Preview API. The host method `shell.updateData()` and the `@salesforce/experimental-mfe-bridge` package are Developer Preview only. In the generally available release, data exchange moves to a reactive UI-state model rather than an imperative method call, so don't build long-term code around `updateData()`. To move an app to the generally available version, see [Migrate from the Developer Preview API](/docs/platform/microfrontend/guide/migrate-from-dev-preview.md).
:::

## How It Works

The page sends data to your app by calling a method on the shell. Your app receives that data through the bridge. When your app raises an event, the bridge forwards it across the iframe boundary, and the shell re-fires it in the page so your wrapper component can respond.

## Send Data to the Embedded App

Call `updateData` on the shell with the data your app needs.

```javascript
shell.updateData({ recordId: "001xx000003DGb2AAG", locale: "en_US" });
```

If you call `updateData` before the app's bridge has finished connecting, the shell holds the data and delivers it once the connection is ready. You don't have to wait for a ready signal before sending the first payload.

:::note
Data crosses the iframe boundary through the browser's messaging channel. Pass values that survive that boundary. Plain objects, strings, numbers, arrays, and booleans are safe. Values that can't be cloned, such as functions, cause an error.
:::

## Receive Data in the Embedded App

Inside your app, read data from the bridge as it arrives.

```javascript
import { bridge } from "@salesforce/experimental-mfe-bridge";

bridge.addEventListener("data", () => {
  const data = bridge.getData();
  // use data.recordId, data.locale, and so on
});
```

## Respond to Events from the Embedded App

When your app dispatches an event through the bridge, the shell re-fires it in the page. Subscribe with `addEventListener` on the shell element.

```javascript
shell.addEventListener("save-complete", (event) => {
  // handle event.detail
});
```

## See Also

- [Embed an External Web App (Developer Preview)](/docs/platform/microfrontend/guide/dp-embed-external-web-app.md)
- [Match an Embedded App to the Salesforce Theme (Developer Preview)](/docs/platform/microfrontend/guide/dp-style-embedded-app.md)
