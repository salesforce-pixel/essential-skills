# Resize an Embedded App to Fit Its Content (Developer Preview)

Let the embedding frame grow and shrink with your app's content so it renders without inner scrollbars or clipping. The embedded app reports its height, and the `<lwc-shell>` host sizes the iframe to match.

:::note
This topic describes the Developer Preview API. To move an app to the generally available version, see [Migrate from the Developer Preview API](/docs/platform/microfrontend/guide/migrate-from-dev-preview.md).
:::

## How It Works

Auto-resize is on by default. Inside the iframe, the bridge watches your app's content for size changes and reports the new height to the host. The host applies that height to the iframe. Resizing adjusts height only. The iframe width is always 100% of its container.

## Disable Auto-Resize

To take over sizing yourself, listen for the `resize` event on the shell and cancel it. The event is cancelable. When you cancel it, the host doesn't apply the height, and sizing becomes your responsibility.

```javascript
shell.addEventListener("resize", (event) => {
  event.preventDefault();
  // apply your own height policy here
});
```

:::important
If you cancel the `resize` event, you must apply a height yourself. If you cancel it and don't set a height, the iframe never gets sized.
:::

## Avoid Full-Viewport Heights

:::warning
Avoid full-viewport height styles, such as `height: 100vh` or `min-height: 100vh`, in your embedded app. When automatic resizing is on, a full-viewport height can create a feedback loop where the content height and the frame height keep growing. More generally, don't change the observed element's size from inside a resize handler, because it re-triggers the observer.
:::

## See Also

- [Embed an External Web App (Developer Preview)](/docs/platform/microfrontend/guide/dp-embed-external-web-app.md)
- [Match an Embedded App to the Salesforce Theme (Developer Preview)](/docs/platform/microfrontend/guide/dp-style-embedded-app.md)
