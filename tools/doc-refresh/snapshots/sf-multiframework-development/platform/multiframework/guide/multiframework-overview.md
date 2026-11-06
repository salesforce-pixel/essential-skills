# Salesforce Multi-Framework Overview

Use Salesforce Multi-Framework, a framework-agnostic runtime, to build Salesforce apps with frontend frameworks, such as React or Angular, and run them directly on the Salesforce Platform. Your app has access to your Salesforce data through GraphQL and the Salesforce Data SDK, along with built-in platform features, such as authentication, security, and governance. Build modern frontends backed by the trust and data of the platform.

Whether you speed up development with Agentforce Vibes or use your own tooling, with Salesforce Multi-Framework you can:

- Jump-start app development with ready-to-use templates for React and Angular.
- Include Salesforce data and Salesforce CMS content in the app.
- Add features including search, authentication, and the Agentforce Conversation Client.
- Preview, deploy, and manage your app, and then access it from the App Launcher or the Salesforce mobile app.
- Embed your app as a microfrontend in Lightning Experience or Experience Cloud site pages (Beta).

## How Salesforce Multi-Framework Works

A few platform concepts explain how a Multi-Framework app runs on Salesforce, including the metadata type your app becomes, the kinds of apps you can build, the domain it runs on, and the security model it inherits.

### The UIBundle Metadata Type

When you build a Multi-Framework app for the Salesforce Platform, your app becomes a piece of Salesforce metadata called a UIBundle. A UIBundle is a self-contained unit that holds your app's source, configuration, and routing rules. It represents your app's UI and works with several other metadata types to define your app in Salesforce.

Because the UIBundle is metadata, it behaves like other Salesforce metadata. Your app is:

- **Stored and versioned**: Your app's files are stored in Salesforce, and each UIBundle has a version. You manage the publication lifecycle on the platform rather than on an external web server.
- **Managed with Salesforce DX**: An app is part of a Salesforce DX project. You use familiar Salesforce DX workflows, CLI commands, and project structures to manage the app alongside your other metadata, such as custom objects and Apex classes.
- **Deployed as metadata**: You deploy a UIBundle to an org the same way you deploy any other source, and you can include it in your deployment pipeline.

Your app’s files live in the Salesforce DX project under the `force-app/main/default/uiBundles/` directory.

### Internal Vs External Apps

With Salesforce Multi-Framework, you can build two kinds of apps based on the audience.

- **Internal apps** are for employees (B2E) who sign in with their Salesforce credentials. After you deploy an internal app, users open it from the Salesforce App Launcher on desktop or in the Salesforce mobile app. Permission sets or user profiles control app access, just like with Lightning apps.
- **External apps** are for people outside your Salesforce org, such as customers (B2C) and partners (B2B). External apps are surfaced through an Experience Cloud site, so visitors don't need to be logged in to Salesforce. The app also appears in the App Launcher for Salesforce users, where selecting it opens the site's URL in a new tab.

An internal app and an external app use different project templates and platform configuration, and require some additional metadata types to integrate with the Salesforce Platform. Each audience has its own set of templates, which determine the metadata and prebuilt features your app starts with. For the full template and metadata comparison, see [Generate an App from a Template](/docs/platform/multiframework/guide/mfw-generate-app.md).

### The Salesforce App Domain

Internal Multi-Framework apps run on the Salesforce app domain, a separate, top-level domain that hosts web apps on Salesforce and isolates them with strong, browser-native boundaries. Because each app runs on its own origin under `*.salesforce.app`, the browser's same-origin policy separates it from the core Salesforce runtime, so your app and its third-party dependencies can't directly access the Lightning DOM, browser storage, or Salesforce session cookies. That isolation limits the risk from vulnerable third-party code. Users still get seamless single sign-on through a scoped session that lets your app securely access supported platform APIs.

### Built-In Platform Security and Governance

Your app's data requests flow through the User Interface API, which enforces the same security and governance rules that apply everywhere else in Salesforce:

- Object-level security (OLS) controls which objects a user can access.
- Field-level security (FLS) controls which fields a user can view and edit.
- Sharing rules control which records a user can access.
- Validation rules run when a user creates or updates a record.

Because these rules are enforced on the server for every query and mutation, you don't reimplement access control in your frontend code. Your app inherits Salesforce trust instead of managing it externally.

## Multi-Framework Vs LWC

LWC remains the optimal framework for building integrated, reusable components within the Salesforce Platform. While Multi-Framework broadens developer choice, they serve different purposes:

- **LWC:** Choose LWC for native Salesforce platform integration. With LWC, you get built-in security, data binding, and the ability to create highly reusable, composable components that function seamlessly within Lightning Experience, Experience Builder sites, and Salesforce mobile apps.

- **Multi-Framework:** Choose React or Angular for self-contained single-page applications (SPAs) or highly customized experiences using Salesforce as the host and data source.

| Feature                    | Lightning Web Components (LWC)                                                                                                                                    | Multi-Framework                                                                                                                                                                                       |   |
| :------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | - |
| **Salesforce Integration** | Deep, native integration with the Salesforce Platform. Automatic data binding, security, and access to platform services such as Lightning Data Service and Apex. | Excellent for building full page applications or custom experiences hosted via Salesforce Multi-Framework, giving developers the choice to leverage their existing framework expertise and libraries. |   |
| **Performance**            | Optimized for the Salesforce Platform, often leading to better performance within the Salesforce UI.                                                              | High performance for complex UIs, but performance within the Salesforce ecosystem depends heavily on API design and data retrieval strategies.                                                        |   |
| **Security & Governance**  | Enforces platform security and compliance standards automatically. Built-in mechanisms for managing state and platform interaction.                               | Data requests flow through the User Interface API, which enforces the same object-, field-, and record-level security as the rest of Salesforce.                                                      |   |
| **Learning Curve**         | Relatively low for developers familiar with modern JavaScript and HTML; syntax is standard-based.                                                                 | Low to moderate, depending on familiarity with their framework of choice                                                                                                                              |   |
| **Component Reuse**        | Excellent component-level reuse, referential integrity, and seamless integration within the Lightning Experience and across LWC projects.                         | Component reuse is fundamental within a web app or static site. Integration of those components in Lightning Experience and other LWC-based environments requires Micro-Frontend support.             |   |

## Choose Your Development Approach

Salesforce Multi-Framework gives you flexible options for building apps or reusing your existing frontend assets on the Salesforce Platform.

With Agentforce Vibes, you can accelerate the entire development lifecycle. Because Agentforce Vibes is connected to your Salesforce org, it understands your org's metadata, objects, and Apex dependencies. And because it operates entirely within the Salesforce Trust Boundary, your schema, business logic, and source code never leave your Salesforce environment to reach an external model. You describe what you want to build in natural language, and Agentforce Vibes handles scaffolding, metadata, and business logic. Use a template to get started, and add Salesforce data, Salesforce CMS content, and features such as search. Alternatively, for low-code users, you can use Builder Central (Beta) to create apps using natural language prompts in an intuitive user interface that's available in Setup.

If you prefer to use your own tooling or you want to reuse existing apps, you can manually integrate your apps with the Salesforce Platform. Because a Multi-Framework app is a standard Salesforce DX project with an npm-based build, you can develop it with whatever tools you already use, including agentic coding tools such as Claude Code and Cursor. Familiar Salesforce DX workflows, CLI commands, and project structures let you manage your app alongside your other Salesforce metadata.

## Add Data, Content, and Features

After you scaffold an app, you connect it to Salesforce and extend it with platform features:

- **Salesforce data**: Query and mutate records with the Data SDK (`@salesforce/platform-sdk/data`), which is framework-agnostic and sends GraphQL operations through the User Interface API.
- **Salesforce CMS content**: Bring images, branding, and other managed content into your app.
- **Object search**: Add search over your Salesforce records.
- **Authentication**: Use Salesforce credentials for internal apps, or Experience Cloud guest and authenticated access for external apps.
- **Agentforce Conversation Client**: Embed conversational AI interactions in your app.

## Embed Your App in Other Salesforce Experiences (Beta)

Beyond running as a standalone app, you can use Salesforce Microfrontends (UI Embedding) to embed your deployed internal app as a microfrontend inside a Lightning page or an Experience Cloud site. Salesforce hosts your app in a secure, sandboxed iframe and gives it a channel to exchange data, styling, and lifecycle events with the surrounding page.

## See Also

- *React Documentation*: [Quick Start](https://react.dev/learn)
- *Agentforce Vibes Developer Guide*: [Build a React App with Agentforce Vibes](https://developer.salesforce.com/docs/platform/agentforcevibes/guide/afv-reactdev-overview.md)
- *Salesforce Help*: [Get Started with Builder Central (Beta)](https://help.salesforce.com/s/articleView?id=platform.builder_central_get_started.htm\&type=5)
- [Multi-Framework recipes repo](https://github.com/trailheadapps/multiframework-recipes)
- *Salesforce Developers Blog*: [Build with React, Run on Salesforce: Introducing Salesforce Multi-Framework](https://developer.salesforce.com/blogs/2026/04/build-with-react-run-on-salesforce-introducing-salesforce-multi-framework)
