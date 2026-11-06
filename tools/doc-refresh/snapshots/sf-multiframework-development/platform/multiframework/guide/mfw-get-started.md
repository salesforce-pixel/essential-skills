# Get Started

Go from an empty project to a running app on the Salesforce Platform. With Salesforce Multi-Framework, you build a web app with a frontend framework, such as React or Angular, run it locally against your org, and deploy it as a UIBundle. A UIBundle is a piece of Salesforce metadata that you manage with familiar Salesforce DX workflows.

The fastest way to see how it fits together is the quick start, which scaffolds, runs, and deploys your first app in about 10 minutes. When you're ready to build your own app, work through the setup and development tasks in order.

## Build Your First App

1. **Set up your org.** Confirm prerequisites, enable the Salesforce app domain, and complete any optional configuration for Agentforce Conversation Client or Salesforce CMS. See [Set Up Your Org for Multi-Framework App Development](/docs/platform/multiframework/guide/mfw-setup.md).
2. **Run the quick start.** Scaffold an app from a template, run it locally, and deploy it to your org. See [Quick Start: Build and Run Your First App](/docs/platform/multiframework/guide/mfw-quick-start.md).

## The Multi-Framework App Lifecycle

Whether you build in React or Angular, every Multi-Framework app follows the same path from an empty project to a published app that users can access. You often move back and forth between stages as your app evolves, but the overall journey is the same. Use this map to see where each topic in the guide fits.

1. **Set up your org.** Confirm prerequisites and enable the Salesforce app domain so that your org can host Multi-Framework apps. See [Set Up Your Org for Multi-Framework App Development](/docs/platform/multiframework/guide/mfw-setup.md).
2. **Generate an app.** Scaffold a React or Angular app from a project template, either with an agentic coding tool or the Salesforce CLI. See [Generate an App from a Template](/docs/platform/multiframework/guide/mfw-generate-app.md) and [Build with Agentic Coding Tools](/docs/platform/multiframework/guide/mfw-agentic-tools.md).
3. **Learn your project structure.** Get to know the UIBundle project layout and the metadata that defines your app. See [Project Structure and Metadata](/docs/platform/multiframework/guide/mfw-project-structure.md).
4. **Preview and run locally.** Run your app on your machine against your org for a fast feedback loop as you build. See [Preview and Run Your App Locally](/docs/platform/multiframework/guide/mfw-preview.md).
5. **Add data, features, and style.** Connect to Salesforce data, integrate platform capabilities, and style your app. See [Access Salesforce Data and Platform Capabilities](/docs/platform/multiframework/guide/data-sdk-usage.md), [Style Your React Apps](/docs/platform/multiframework/guide/mfw-styling.md), and [Integrate Agentforce Conversation Client](/docs/platform/multiframework/guide/reactdev-acc.md).
6. **Test your app.** Run the unit and end-to-end tests that ship with your template before you deploy. See [Test Your App](/docs/platform/multiframework/guide/mfw-testing.md).
7. **Deploy and publish.** Deploy the UIBundle to your org as metadata and publish a version so that users can access it. See [Deploy and Publish a UIBundle](/docs/platform/multiframework/guide/mfw-deploy.md).
8. **Grant access and manage.** Manage the deployed app in Setup and give users access. See [Manage Your App and Grant User Access](/docs/platform/multiframework/guide/mfw-manage.md).
9. **Distribute your app (optional).** Embed your app in Salesforce or package it for distribution to other orgs. See [Embed Your App in Salesforce with UI Embedding](/docs/platform/multiframework/guide/mfw-ui-embedding.md) and [Package and Distribute Your App](/docs/platform/multiframework/guide/mfw-packaging.md).

## See Also

- [Salesforce Multi-Framework Overview](/docs/platform/multiframework/guide/multiframework-overview.md)
- [Multi-Framework recipes repo](https://github.com/trailheadapps/multiframework-recipes)
