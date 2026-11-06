# Set Up Your Org for Multi-Framework App Development

Before you begin working with Multi-Framework apps, configure the Salesforce app domain and review the prerequisites for your org. If you want to add an Agentforce Conversation Client, complete the additional configuration steps.

If you're using Agentforce Vibes to build your app and you want to use content from Salesforce CMS, complete the steps to set up the Content Read-Only MCP Server.

## Review Prerequisites and Considerations

**Available in**: Salesforce Multi-Framework is available in Enterprise, Performance, Unlimited, Developer, and Partner Developer editions hosted on Hyperforce. Unavailable in Alibaba Cloud or Salesforce Government Cloud.

Before you begin:

- Confirm that your org is hosted on Hyperforce. Salesforce Multi-Framework is available only on Hyperforce.
  1. From Setup, in the Quick Find box, enter `Company Information`, and then select **Company Information**.
  2. In the Organization Detail section, if the instance name has a three-letter prefix followed by a number, such as abc123, your org is on Hyperforce.
- Confirm that you have the latest versions of [Salesforce CLI](https://developer.salesforce.com/docs/atlas.en-us.sfdx_setup.meta/sfdx_setup/sfdx_setup_update_cli.htm) and the [Salesforce Extension Pack](https://marketplace.visualstudio.com/items?itemName=salesforce.salesforcedx-vscode) installed. This step ensures that you have the latest Agentforce Vibes and CLI capabilities, such as updated Salesforce skills and Live Preview.
- To create an external Multi-Framework app, such as a public-facing portal for customers or partners, make sure that:
  - Digital Experiences is enabled in your org. See [Enable Digital Experiences](https://help.salesforce.com/s/articleView?id=experience.networks_enable.htm\&type=5) in Salesforce Help.
  - You have the correct user licenses. You need Customer Community or Customer Community Plus user licenses for B2C portal users, and Partner Community and Channel Account for B2B users.

Keep these limitations and considerations in mind:

- Packaging is unsupported for external-facing apps.
- For developer orgs, only `c` namespaces are supported.

## Configure the Salesforce App Domain

| USER PERMISSIONS NEEDED              |                           |
| ------------------------------------ | ------------------------- |
| To enable the Salesforce App Domain: | **Customize Application** |

To create an internal Multi-Framework app for employees who log in with their Salesforce credentials, confirm that the Salesforce app domain is enabled. This separate, top-level domain hosts web apps on Salesforce while enforcing strong browser-native isolation boundaries. The domain is automatically enabled for most orgs and serves internal apps from `.my.salesforce.app`.

For the Salesforce app domain to function correctly, Salesforce Edge Network is also required. See [Salesforce Edge Network](https://help.salesforce.com/s/articleView?id=xcloud.domain_name_edge_network.htm\&type=5) in Salesforce Help.

1. From Setup, in the Quick Find box, enter `Salesforce Multi-Framework`, and then select **Salesforce Multi-Framework Apps**.
2. If you see the **Enable Domain** button, click it and confirm your change. If not, the domain is already enabled.
3. In the Quick Find box, enter `My Domain`, and then select **My Domain**.
4. In the Routing and Policies section, if Salesforce Edge Network isn’t enabled, click **Edit**, enable the setting, and save your changes.

## (Optional) Set Up the Content Read-Only MCP Server and Tools

When you vibe code a Multi-Framework app, Agentforce Vibes can use the Content Read-Only MCP server and the Content Write MCP server to access, manage, and apply Salesforce CMS resources, such as content, images, or brands to your app.

- Use the Content Read-Only server to search for, retrieve, and apply images, documents, or other content types to your Multi-Framework app.
- Use the Content Write MCP server to edit existing CMS content, create content, and publish content, so that you can flexibly create CMS content for your app as you build and save it to your Salesforce org.

See the Salesforce Hosted MCP Servers developer guide for information about how to set up the [Content Read-Only](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/content-readonly.md) and [Content Write MCP](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/content-write.md) servers and for more details on the available tools within each server.

## (Optional) Configure Agentforce Conversation Client

With the Agentforce Conversation Client (ACC), you can integrate conversational AI interactions into your Multi-Framework apps for internal employee use cases. For more details on Agentforce Conversation Client, check out the [Agentforce Conversation Client (ACC) Developer Guide](https://developer.salesforce.com/docs/platform/accsdk/overview).

Your Salesforce org must meet specific architectural requirements to support session persistence between Salesforce and the Multi-Framework app.

### Set Up Agentforce Employee Agent

You must have at least one Agentforce Employee Agent (AEA) configured with topics and actions. Additionally, ensure that the global Agentforce preference is enabled:

1. From Setup, in the Quick Find box, enter `Agentforce Agents` and then select **Agentforce Agents**.
2. Enable the **Agentforce** preference.

### Configure Routing and Policies

To ensure that the ACC can maintain state within the Multi-Framework app, the Salesforce org must permit the use of cookies for the integration path.

**Cookie Policy:** The requirement for first-party use of Salesforce cookies must be disabled within the My Domain settings.

1. From Setup, in the Quick Find box, enter `My Domain`, and then select **My Domain**.
2. In the Routing and Policies section, if **Require first-party use of Salesforce cookies** is enabled, click **Edit**, and then deselect the setting.
3. Save your changes.

### Set Up Trusted Domains for Agentforce Conversation Client

Because Multi-Framework apps are typically hosted on origins external to Salesforce (including localhost during development), the Salesforce iframe must be explicitly authorized to render on those domains.

**Domain Authorization:** The application's hosting domain (for example, `https://myapp.com` or `localhost:<PORT>`) must be registered in the Trusted Domains for Inline Frames registry within Salesforce Session Settings.

1. From Setup, in the Quick Find box, enter `Session`, and then select **Session Settings**.
2. In the Trusted Domains for Inline Frames section, click **Add Domain**.
3. Enter the domain for your web app, such as `http://localhost:<PORT_NUMBER>`. For example, `http://localhost:5173`.
4. Select **Lightning Out** for the iFrame type and save your changes.
