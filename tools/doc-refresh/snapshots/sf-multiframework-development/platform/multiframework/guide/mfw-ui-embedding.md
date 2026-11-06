# Embed Your App in Salesforce with Microfrontends (Beta)

You can embed a Multi-Framework app directly in Salesforce so your users work in one place instead of switching to a separate tab or window. This pattern of running your app as a component inside a Salesforce page is called a microfrontend. On the platform, you build it with UI Embedding. Salesforce hosts your app inside a secure, sandboxed iframe using the `lightning-ui-embedding` base component, and gives your app a typed channel to exchange styling, sizing, and lifecycle signals with the surrounding page.

To embed an app, write a thin Lightning web component (LWC) that renders `lightning-ui-embedding` and points its `src` at your app's URL. Then add that component to a Lightning page or an Experience Cloud site page.

The app you build is a deployed UIBundle, which Salesforce hosts on the `*.salesforce.app` domain. To embed it, point the embedding component at the bundle's `*.salesforce.app` URL, which is the same URL the app opens from the App Launcher.

## Before You Embed Your App

To embed your UIBundle, first get it running as a standalone app:

1. Deploy your UIBundle and grant access. See [Deploy and Publish a UIBundle](/docs/platform/multiframework/guide/mfw-deploy.md) and [Manage Your App and Grant User Access](/docs/platform/multiframework/guide/mfw-manage.md).
2. Open the app from the App Launcher and copy its full `*.salesforce.app` URL from the browser address bar. That's the URL you give the embedding component.

## Learn More

Learn more about microfrontends, including building the wrapper component, handling error states, and using the view SDK.

- *Salesforce Microfrontend (UI Embedding)*: [Get Started with UI Embedding](https://developer.salesforce.com/docs/platform/microfrontend/guide/get-started.md)
- *Salesforce Microfrontend (UI Embedding)*: [Embed an Internally Hosted App as a UI Bundle](https://developer.salesforce.com/docs/platform/microfrontend/guide/internal-ui-bundles.md)
