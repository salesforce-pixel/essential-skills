# Create the Apex Invocable Action

Your widget displays data from an object in your org, such as a HotelInfo custom object. While there are multiple ways to get the data, a standard approach is to create an Apex class that contains a SOQL query for the HotelInfo object. The Apex class returns the results in the shape of one of your custom Lightning types schema. You later use this Apex class to create an MCP tool in your custom MCP server.

1. In your local DX project, create the Apex class that queries your org and returns output shaped to the schema of one of your custom Lightning types. Remember, for channels that support MCP, you must create *two* custom Lightning types: one for the MCP result wrapper role and one for the MCP payload role.

   Make sure your Apex code meets the requirements for an Apex invocable action. For example, the Apex class must be `global` and the method that returns results must be annotated with `@InvocableMethod`. See these links for full details:

   - [Connect Your Widget to a Custom Lightning Type](/docs/platform/hxl/guide/hxl-rich-ui.md#connect-your-widget-to-a-custom-lightning-type) for details about the two required custom Lightning types.
   - [Apex Actions](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/invocable-actions.md)

2. Deploy your Apex class to your org. For example, to use a Salesforce CLI command to deploy to the org with alias `my-org`, run this command:

   ```bash
   sf project deploy start --metadata ApexClass:HotelSearchResult --target-org my-org
   ```

Your Apex invocable action is ready to become an MCP tool. See [Create a Custom MCP Server](/docs/platform/hxl/guide/hxl-mcp-server.md).

## See Also

- [Salesforce Dev Blog: Expose Custom Apex as a Hosted MCP Tool for Agents](https://developer.salesforce.com/blogs/2026/05/expose-custom-apex-as-a-hosted-mcp-tool-for-agents)
- [Trailhead: Agent Customization with Apex](https://trailhead.salesforce.com/content/learn/modules/agent-customization-with-apex)
- [Apex Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_dev_guide.htm)
- [Apex @InvocableMethod Annotation](https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_classes_annotation_InvocableMethod.htm)
- [Apex Actions](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/invocable-actions.md)
- [Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types.md)
- [*Salesforce CLI Command Reference*: project Commands](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_project.md)
