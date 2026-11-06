# Set Up Your Org for MCP Access

Before AI clients can connect to your Salesforce org through MCP, configure authentication and access. This one-time setup enables any MCP-compatible client to connect securely using OAuth 2.0. If you're using an existing MCP server, you've likely already completed these tasks.

Configure these items in your org:

- **External Client App** — Register an External Client App (ECA) in your org to handle OAuth authentication. This provides the authentication credentials that clients use to connect to your org.
- **OAuth Scopes** — Grant the permissions that MCP servers need to access Salesforce data and operations on behalf of authenticated users.
- **Security Settings** — Enable Proof Key for Code Exchange (PKCE) and JWT-based tokens to ensure secure, standards-based authentication.

See [Set Up Your Org](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/setup-overview.md) in the *Hosted MCP Servers* guide for complete details.

:::important
When you create the ECA, note the OAuth consumer key (also known as client ID) because you'll use it later to configure your MCP client.
:::

After your org is configured for MCP access, connect your MCP clients (Claude, Slackbot, etc) to it. Then test the widget! See [Connect your MCP client to your org](/docs/platform/hxl/guide/hxl-mcp-setup-client.md).

## See Also

- [Salesforce Hosted MCP Servers](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/hosted-mcp-servers-overview.md)
- [Salesforce Help: External Client Apps](https://help.salesforce.com/s/articleView?id=xcloud.external_client_apps.htm\&type=5)
