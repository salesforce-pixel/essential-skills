# Use HXL Widgets with Agents That Support MCP

Some AI agents use MCP to interact with data in your org, such as Claude Desktop, Slackbot, and ChatGPT. HXL widgets are compatible with the [MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview) industry standard, which means that the widget works in any agent that is MCP Apps compatible.

:::warning
HXL widgets don't currently render when using [Block Kit for Slackbot](https://docs.slack.dev/block-kit/). Block Kit extends the MCP Apps protocol so MCP servers can return native Slack Block Kit JSON when Slackbot is the agent.
:::

To use an HXL widget on channels that support MCP, you must create a custom MCP server and add associated tools and resources. You can also update an existing custom MCP server if you prefer.

:::note
In the HXL setup with MCP, we use the term *client* to mean an external *agent* that interacts with your Salesforce org. We also use the terms *channel* and *surface* to refer to the application in which that agent operates and the area encompassing its UI. For definitions, see the [Glossary](/docs/platform/hxl/references/hxl-reference-about/hxl-widgets-glossary.md).
:::

## Before You Begin

It's assumed that you've already:

- Set up your local DX developer environment, such as installing Salesforce CLI and the VS Code Salesforce extensions. See [Get Started by Creating a New DX Project](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_get_started_dx.htm). (You can ignore the Dev Hub instructions unless you plan to create a scratch org.)

- Created a local Salesforce DX project that contains the metadata files for your widget and custom lightning types.

  For channels that support MCP, be sure you've created two object-based custom Lightning types. See [Connect Your Widget to a Custom Lightning Type](/docs/platform/hxl/guide/hxl-rich-ui.md#connect-your-widget-to-a-custom-lightning-type).

- Authorized your Salesforce development org so you can deploy and retrieve metadata to and from it.

  Use the VS Code **SFDX: Authorize an Org** command or the `org login web` Salesforce CLI command. In the Salesforce CLI command examples, we assume you gave your org the alias `my-org`.

- Deployed the widget and custom Lightning types from your DX project to your Salesforce org.

## General Workflow

Here are the general steps to use your widget on channels that support MCP:

1. [Create the Apex invocable action](/docs/platform/hxl/guide/hxl-mcp-apex.md) that returns data from your org for your widget to display.
2. [Create or modify a custom MCP server](/docs/platform/hxl/guide/hxl-mcp-server.md). This step includes creating the MCP tool that uses the Apex invocable action and wiring it up to the widget.
3. [Configure your org so your AI clients can access it through the custom MCP server](/docs/platform/hxl/guide/hxl-mcp-setup-org.md).
4. [Connect your MCP client to your org](/docs/platform/hxl/guide/hxl-mcp-setup-client.md) and test your widget on it.

## Vibe Code

These MCP topics show how to complete tasks manually, such as using a Salesforce CLI command to deploy metadata and editing XML files in the VS Code editor. We think it's useful to document all these details because you learn how all the HXL building blocks fit together, which makes it easier to troubleshoot problems. And saves you tokens.

However, you can also use Agentforce Vibes to complete many of these tasks. For example, rather than run the `project deploy start` Salesforce CLI command in a terminal to deploy new metadata, run this prompt in the Agentforce Vibes chat interface:

*Deploy the Apex class I just created.*

## See Also

- [Agentforce Vibes Developer Guide](https://developer.salesforce.com/docs/platform/agentforcevibes/guide/afv-overview.md)
