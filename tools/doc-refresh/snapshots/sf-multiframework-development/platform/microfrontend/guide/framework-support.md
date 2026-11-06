# Build Embedded Apps in the Framework You Prefer

UI Embedding works with externally hosted apps regardless of the front-end framework they're built in. You can reuse an app you already have instead of rebuilding it in a Salesforce-specific framework.

## Framework Compatibility

Because Salesforce embeds your app as an externally hosted app in a sandboxed iframe, it interacts with your app through the standards-based embedding protocol rather than through framework-specific code. Any standards-based web app works.

Externally hosted embedding has been validated with React, Angular, and Vue apps. Automated test coverage is React-based.

:::note
Framework compatibility applies to externally hosted apps. Internally hosted UI Bundles have their own framework support details.
:::

## How to Use It

Point the `src` attribute of `lightning-ui-embedding` at your hosted app, regardless of the framework your app uses. To build and embed the wrapper component, see [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md).

## See Also

- [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md)
- [Embed an Internally Hosted App as a UI Bundle](/docs/platform/microfrontend/guide/internal-ui-bundles.md)
