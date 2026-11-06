# Style an Embedded App to Match Salesforce

Keep an embedded app visually consistent with the surrounding Salesforce experience. Salesforce passes styling values to the embedded app as CSS custom properties, so your app can read them and match the page's colors, spacing, and other theme values.

## How It Works

Salesforce composes a UI state for each embedded app and pushes it to the guest through the embedding protocol. That UI state includes a `styles` object with two parts: a `variables` object built from CSS custom properties (styling tokens) and an `attributes` object of allowlisted HTML attributes. Your embedded app reads these values from the current state and applies them to its own styles. When the values change, Salesforce pushes an updated UI state, and your app restyles by subscribing to those updates.

The host sets both parts on the `lightning-ui-embedding` element itself. Inline CSS custom properties (`style="--x: y"`) become `styles.variables`, and the allowlisted HTML attributes become `styles.attributes`. The component reads them off the element and forwards them to your embedded app.

:::note
Theming is scoped to CSS custom properties. Salesforce doesn't automatically restyle your app's components or replicate the full design system inside your app. Your app decides how to apply the token values.
:::

## Prerequisites

- Your app is embedded with `lightning-ui-embedding` and loads successfully.

## Read the Styling Tokens

1. In your embedded app, create the view SDK and read the current UI state. `createViewSDK` is asynchronous, so await it. `getUiState` returns the current state and a `subscribe` function you use to react to later updates.

```javascript
import "@salesforce/platform-sdk/ui-embedding";
import { createViewSDK } from "@salesforce/platform-sdk/view";

const viewSdk = await createViewSDK();

// Off an embedding surface, createViewSDK resolves to an empty object,
// so guard the call before you use it.
const uiState = viewSdk.getUiState?.();
if (uiState) {
  applyStyles(uiState.state.styles?.variables);
}
```

2. Apply the CSS custom properties from `state.styles.variables` to your app.

The variables arrive as name-value pairs. Map them to your app's styles so your colors and spacing follow the Salesforce theme.

3. Apply the allowlisted HTML attributes from `state.styles.attributes` to your app.

Along with the variables, `styles.attributes` mirrors these attributes so your app can match the host: `autocapitalize`, `autocorrect`, `dir`, `enterkeyhint`, `inputmode`, `lang`, `spellcheck`, `title`, and `translate`. Applying `dir` (RTL or LTR) and `lang` is especially important for matching the Salesforce experience.

```javascript
const { variables, attributes } = uiState.state.styles ?? {};
applyStyles(variables);
applyAttributes(attributes);
```

4. Restyle when the theme changes. Salesforce pushes an updated UI state when styling values change, so subscribe and reapply.

```javascript
const unsubscribe = uiState.subscribe((next) => {
  applyStyles(next.styles?.variables);
  applyAttributes(next.styles?.attributes);
});
```

:::note
The embedded app resolves its own platform context, such as locale and form factor. Salesforce doesn't send `theme`, `locale`, or `formFactor` as part of the UI state.
:::

## See Also

- [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md)
- [Resize an Embedded App to Fit Its Content](/docs/platform/microfrontend/guide/resize-embedded-app.md)
