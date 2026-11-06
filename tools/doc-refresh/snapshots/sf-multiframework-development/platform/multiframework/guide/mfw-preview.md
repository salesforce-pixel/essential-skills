# Preview and Run Your App Locally

As you build a Multi-Framework app, you can run it locally and preview your changes without deploying to an org each time. You have two options: run the app on a local development server in your browser, or use Live Preview to render the app inside Visual Studio Code. Both give you a fast edit-and-refresh loop, and both work whether you develop with Agentforce Vibes, an agentic IDE, or any other editor.

## Run a Local Development Server

Each project template includes an npm script that starts a local development server. From your app's directory, run:

```bash
npm run dev
```

The server starts at `http://localhost:5173`, and your browser reloads automatically when you save a change. `npm run dev` is the dev-server command for both React and Angular apps. To use a different port, set the `SF_UIBUNDLE_PORT` environment variable—for example, `SF_UIBUNDLE_PORT=4200 npm run dev`.

For Angular apps, you can also start the server with the standard Angular CLI:

```bash
npx ng serve
```

## Preview Your App in VS Code with Live Preview

The Salesforce Live Preview extension renders your running app in a Visual Studio Code tab and updates it automatically as you save source changes, so you don't manually redeploy or refresh. Live Preview connects to your authorized org, so your app previews with real org data.

Before you start, install the Salesforce Extension Pack and the UI Bundle development plugin:

```bash
sf plugins install @salesforce/plugin-ui-bundle-dev
```

1. In VS Code, make sure that you've authorized the org you want to preview against.
2. Start Live Preview one of two ways:
   - Open the Command Palette and run **SFDX: Open in Live Preview**.
   - Right-click a source file (`.js`, `.jsx`, `.ts`, or `.tsx`) in the Explorer or editor and select **SFDX: Open in Live Preview**.
3. Select your app.

Your app opens in a VS Code tab. As Agentforce Vibes or you save changes to the source, the preview refreshes.

:::note
If your app embeds the Agentforce Conversation Client, register your local preview origin (for example, `http://localhost:5173`) in the Trusted Domains for Inline Frames registry in Session Settings. See [Set Up Your Org for Multi-Framework App Development](/docs/platform/multiframework/guide/mfw-setup.md).
:::

## Local Development Server or Live Preview

Both approaches support rapid iteration. Choose based on where you want to see your app and what data it needs.

| Consideration             | Local development server                                                            | Live Preview                                  |
| ------------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------- |
| **Where the app renders** | Your browser, at `http://localhost:5173`                                            | A tab inside Visual Studio Code               |
| **Data**                  | Your app's local or mocked data, plus any org connection your app code makes        | Your authorized Salesforce org                |
| **Best for**              | Fast UI iteration and framework tooling (hot reload, framework dev server features) | Previewing against real org data as you build |

## See Also

- [Deploy and Publish a UIBundle](/docs/platform/multiframework/guide/mfw-deploy.md)
- [Visual Marketplace: Salesforce Live Preview](https://marketplace.visualstudio.com/items?itemName=salesforce.salesforcedx-vscode-ui-preview)
