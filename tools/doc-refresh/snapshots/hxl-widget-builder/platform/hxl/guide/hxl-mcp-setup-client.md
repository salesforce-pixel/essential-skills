# Connect Your MCP Client to Your Org

The process for connecting MCP clients to use your HXL widget differs depending on the client.

## Connect Claude Desktop or ChatGPT

Connect Claude Desktop or ChatGPT as MCP clients by adding the custom MCP server URL and ECA consumer key that you previously noted. For details, see:

- [Configure Claude](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/claude.md)
- [Configure ChatGPT](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/chatgpt.md)

## Connect Slackbot

To render your widget in Slackbot, add and configure your custom Salesforce MCP server in Slack.

For complete details, see [Connecting an MCP server to the Slackbot MCP Client](https://docs.slack.dev/ai/slackbot-mcp-client/). These options are relevant for Salesforce MCP servers:

- **Auth Type**: Specify Manual OAuth.
- **URL**: Specify the MCP Server URL you noted previously, such as `https://api.salesforce.com/platform/mcp/v1/custom/HotelInfoMCPServer`.
- **Client ID**: When configuring the OAuth provider, specify the consumer key you noted when you configured the external client app (ECA) in your org.

:::warning
HXL widgets don't currently render when using [Block Kit for Slackbot](https://docs.slack.dev/block-kit/). Block Kit extends the [MCP Apps protocol](https://modelcontextprotocol.io/extensions/apps/overview) so MCP servers can return native Slack Block Kit JSON when Slackbot is the client.
:::

## Test the Widget on Your MCP Client

After you connect your MCP client to your org, test that the widget renders the data correctly by running a prompt that invokes it. Each client is different, though most have a chatbot window or UI element where you can enter a prompt.

For example, to see the hotel info widget in action, try this prompt:

*Tell me about the Four Seasons Resort in Maui.*

:::warning
If you update your widget in your org after you've rendered it on an MCP client, it can take a while for the updated widget to refresh on the MCP client.
:::

For more robust testing, check out [MCPJam](https://www.mcpjam.com/) which helps you test, debug, and evaluate MCP servers, MCP apps, and ChatGPT apps.

## See Also

- [Salesforce Dev Blog: Connect Claude with Salesforce Hosted MCP Servers](https://developer.salesforce.com/blogs/2026/05/connect-claude-with-salesforce-hosted-mcp-servers)
- [Salesforce Hosted MCP Servers](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/hosted-mcp-servers-overview.md)
- [Connecting an MCP server to the Slackbot MCP Client](https://docs.slack.dev/ai/slackbot-mcp-client/)
