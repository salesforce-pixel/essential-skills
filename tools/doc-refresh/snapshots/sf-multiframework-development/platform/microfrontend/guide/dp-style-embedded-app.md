# Match an Embedded App to the Salesforce Theme (Developer Preview)

Keep an embedded app visually consistent with the surrounding page by passing Salesforce theme values into it as CSS custom properties. The `<lwc-shell>` host reads the custom properties set on it and forwards them to your app.

:::note
This topic describes the Developer Preview API, including the host method `shell.refreshTheme()`. In the generally available release, theming moves to a reactive UI-state model rather than an imperative refresh call. To move an app to the generally available version, see [Migrate from the Developer Preview API](/docs/platform/microfrontend/guide/migrate-from-dev-preview.md).
:::

## How It Works

When the shell mounts, it reads the CSS custom properties (the `--*` variables) set on the shell element and passes their values to your app across the iframe boundary. Your app reads those values and applies them to its own styles, so its colors and spacing follow the page's theme.

The shell reads the custom properties once when it mounts. It doesn't automatically watch for later style changes on the host. If the theme changes at runtime, for example when a user switches to dark mode, call `refreshTheme()` to send the updated values.

## Set the Theme Values

Set CSS custom properties on the shell element, or on an ancestor the shell inherits from.

```css
lwc-shell {
  --brand-color: #0176d3;
  --background-color: #f3f3f3;
}
```

The shell reads these values at mount and forwards them to your app. In your app, read the forwarded custom properties and map them to your own styles.

:::note
Theming is scoped to CSS custom properties. Salesforce doesn't restyle your app's components for you. Your app decides how to apply the values it receives.
:::

## Update the Theme at Runtime

If the theme changes after the app has loaded, call `refreshTheme` on the shell to re-read the custom properties and send the new values.

```javascript
shell.refreshTheme();
```

## See Also

- [Embed an External Web App (Developer Preview)](/docs/platform/microfrontend/guide/dp-embed-external-web-app.md)
- [Exchange Data Between the Page and an Embedded App (Developer Preview)](/docs/platform/microfrontend/guide/dp-exchange-data.md)
