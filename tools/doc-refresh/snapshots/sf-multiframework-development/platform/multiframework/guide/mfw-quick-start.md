# Quick Start: Build and Run Your First App

Scaffold a Salesforce Multi-Framework app, run it locally against your org, and deploy it in about 10 minutes. This quick start uses React and the `reactinternalapp` template, which generates a complete Salesforce DX project, including the CustomApplication metadata that makes your app appear in the App Launcher.

For the concepts behind each step, and for options this quick start doesn't cover (such as external apps or Agentforce Vibes), see [Salesforce Multi-Framework Overview](/docs/platform/multiframework/guide/multiframework-overview.md).

## Before You Begin

Before starting, make sure that you:

- [Set up your org for Multi-Framework app development](/docs/platform/multiframework/guide/mfw-setup.md).
- Install the latest [Salesforce CLI](https://developer.salesforce.com/docs/atlas.en-us.sfdx_setup.meta/sfdx_setup/sfdx_setup_update_cli.htm) and [Salesforce Extension Pack](https://marketplace.visualstudio.com/items?itemName=salesforce.salesforcedx-vscode) versions.
- [Connect to a Salesforce org and set it as your default](https://developer.salesforce.com/docs/platform/sfvscode-extensions/guide/default-org.md).

## Step 1: Generate the Project

Generate a new Salesforce DX project from the internal React app template.

```shell
sf template generate project --name MyFirstApp --template reactinternalapp
cd MyFirstApp
```

The generated project includes the UIBundle that holds your React app and the CustomApplication metadata that surfaces it in the App Launcher.

## Step 2: Install Dependencies

Install the app's dependencies from inside the UIBundle directory, not the project root.

```shell
cd force-app/main/default/uiBundles/MyFirstApp
npm install
```

## Step 3: Run the App Locally

Start the local dev server.

```shell
npm run dev
```

Open `http://localhost:5173` in your browser to see the app. To run against live org data, authenticate an org and set it as your default before you start the dev server.

## Step 4: See a Live Change

With the dev server running, edit a component or page under `src/` and save. The browser hot-reloads so you can see your change immediately. In VS Code, you can also open the Command Palette and run **SFDX: Open in Live Preview** to preview your app with org context. See [Preview and Run Your App Locally](/docs/platform/multiframework/guide/mfw-preview.md).

## Step 5: Deploy to Your Org

When you're ready, build the production assets and deploy the project.

```shell
npm run build
sf project deploy start --target-org MyOrg
```

Deploying the project deploys both the UIBundle and its CustomApplication metadata. To open your app, grant your user access to it through a permission set, and then find it in the App Launcher.

1. Assign the app's permission set to your user. If the template generated one, run `sf org assign permset --name MyFirstApp_Access`. Otherwise, in Setup, use **Permission Sets** or the app's profile to grant access to the CustomApplication.
2. Open the App Launcher, search for **MyFirstApp**, and open it.

For the full deployment, versioning, and publication workflow, see [Deploy and Publish a UIBundle](/docs/platform/multiframework/guide/mfw-deploy.md).

## Next Steps

- Access Salesforce data: [Access Data and Platform Capabilities](/docs/platform/multiframework/guide/data-sdk-usage.md)
- Match the Salesforce look and feel: [Style Your App](/docs/platform/multiframework/guide/mfw-styling.md)
- Add conversational AI: [Integrate Agentforce Conversation Client](/docs/platform/multiframework/guide/reactdev-acc.md)
- Explore working examples: [Multi-Framework recipes repo](https://github.com/trailheadapps/multiframework-recipes)
