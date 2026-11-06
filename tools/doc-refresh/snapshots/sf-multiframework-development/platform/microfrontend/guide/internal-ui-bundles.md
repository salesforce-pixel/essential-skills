# Embed an Internally Hosted App as a UI Bundle (Beta)

Host your app inside Salesforce infrastructure instead of on your own domain, and embed it with the same `lightning-ui-embedding` component you use for external apps. An internally hosted app is packaged as a UI Bundle, deployed to your org, and served from the Salesforce-managed `*.salesforce.app` domain.

:::note
*Embedding internally hosted UI Bundles is a pilot or beta service that is subject to the Beta Services Terms at [Agreements - Salesforce.com](https://www.salesforce.com/company/legal/agreements/) or a written Unified Pilot Agreement if executed by Customer, and applicable terms in the [Product Terms Directory](https://ptd.salesforce.com/). Use of this pilot or beta service is at the Customer's sole discretion.*

Some capabilities described elsewhere for UI Embedding aren't available for internally hosted bundles in this release, and embedding a bundle currently requires manual Trusted URL and CSP configuration. See the prerequisites and limitations below.
:::

## How It Works

An internally hosted UI Bundle is a React app that you deploy to your org. Salesforce serves it from its own `*.salesforce.app` domain. Instead of pointing the embedding component at an external URL, you reference the bundle by its explicit full `*.salesforce.app` URL, and Salesforce embeds it through the same `sf-embedding` protocol used for externally hosted apps.

Before you embed a bundle, confirm it runs on its own. Open the deployed app from the App Launcher and copy its `*.salesforce.app` URL from the browser address bar. That's the URL you hand to your wrapper component.

## Prerequisites

- You have a React UI Bundle deployed to your org.
- You can create Lightning web components and edit Lightning pages or Experience Cloud sites in your org.
- The UI Bundle launches on its own from the App Launcher. If it doesn't load, enable Salesforce Edge Network in your My Domain settings.

## Configure Trusted URLs and CSP

Because the bundle loads in an iframe from a different domain, you allow that domain (and the domains it redirects through to establish a session) in your org's Content Security Policy. The settings depend on where you embed the bundle.

### Lightning Experience pages

- In Setup, go to Trusted URLs and add `*.salesforce.app` with the `frame-src` directive.

### Experience Cloud sites (LWR-based and Aura-based)

Embedding on an Experience Cloud site requires more settings, because the bundle's session is established through a chain of Salesforce domains inside the iframe.

1. In Setup, go to Trusted URLs and add these three URLs with the `frame-src` directive:
   - `*.salesforce.app`
   - Your org's Lightning domain (for example, `*.lightning.force.com`)
   - Your My Domain URL (for example, `*.my.salesforce.com`)
2. In Session Settings, under Trusted Domains for Inline Frames, add your Experience Cloud site URL with the iframe type **UIEmbedding**. This allows the site to frame the bundle.
3. In My Domain, under Routing and Policies, turn off **Require first-party use of Salesforce cookies**. The bundle relies on Salesforce cookies to establish its session inside the iframe, and this setting blocks those cookies in a framed (third-party) context.

## Reference the UI Bundle by URL

In your wrapper component, set the embedding component's `src` to the bundle's full explicit `*.salesforce.app` URL, the same way you point it at an external app's URL.

## Limitations in This Release

- **React only.** As of now, React UI Bundles are generally available; Angular and Vue support is coming next.
- **Explicit URL only.** Dynamic URL resolution and packaging aren't available. You reference the bundle by its full `*.salesforce.app` URL.
- **App Builder supports Lightning web components only.** You can't drag React, Angular, or Vue UI Bundles onto a page in App Builder in this release.
- **Manual CSP configuration.** The Trusted URL and CSP settings above are configured manually in this release. Salesforce plans to handle them automatically in a later release.

## See Also

- [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md)
- [Build Embedded Apps in the Framework You Prefer](/docs/platform/microfrontend/guide/framework-support.md)
