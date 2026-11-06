# UI Embedding Recipes

Explore working sample apps that embed a web app in Salesforce with `lightning-ui-embedding`. The recipes show complete, runnable patterns you can read, run in a scratch org, and adapt for your own app, so you don't start from a blank file.

The samples live in the Multi-Framework Recipes repository on GitHub, `trailheadapps/multiframework-recipes`, alongside recipes for other ways to bring web frameworks into Salesforce.

:::note
The UI Embedding samples live in the `microfrontend-recipes` folder of that repository, which is a Developer Preview. Developer Preview samples show the approach, but the API surface they use can differ from the generally available `lightning-ui-embedding` component. Read them as patterns to learn from, and follow [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md) for the generally available API.
:::

## What You Can Learn

The recipes show how to:

- Embed an externally hosted app on a Salesforce page with a thin Lightning web component wrapper.
- Read host-driven data and UI state in the embedded app, and send events back to the host.
- Access Salesforce data indirectly through a host Lightning web component rather than from inside the embedded app.
- Compare the embedding approach with a native Lightning web component alternative for full-screen and inline layouts.

## Before You Start

The repository README lists the current prerequisites and setup, including the Node.js and Salesforce CLI versions, how to create the scratch org, and any optional tooling. Follow the README, because the exact versions change over time.

## Use the Recipes

1. Open the `trailheadapps/multiframework-recipes` repository on GitHub.
2. Follow the README to install the prerequisites and create the scratch org.
3. Open the `microfrontend-recipes` folder and run the sample you want to study.
4. Compare the sample against [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md) so you build on the generally available API.

## See Also

- [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md)
- [Build Embedded Apps in the Framework You Prefer](/docs/platform/microfrontend/guide/framework-support.md)
- [Exchange Data Between the Page and an Embedded App](/docs/platform/microfrontend/guide/exchange-data.md)
