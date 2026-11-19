# Get the Agent ID for an Agent

Before you can use the [Agent API](/docs/ai/agentforce/guide/agent-api-get-started.md), you need the agent ID. The method for obtaining this ID depends on which builder you used to create your agent.

## Determine Your Agent Builder Type

Salesforce provides two different agent builders. To determine which one you're using:

- **New Agentforce Builder**: This newer builder features a configurable interface that allows you to switch between Canvas view and Script view. It includes built-in AI assistance and Agent Script support. You access this builder through Agentforce Studio in the App Launcher. See [Explore Agentforce Builder (Beta)](https://help.salesforce.com/s/articleView?id=ai.agent_builder_intro.htm).
- **Legacy Agentforce Builder**: This original builder features a visual subagent editor and dialog-based configuration. You access this builder through Setup > Agentforce Agents. See [Explore the Legacy Agentforce Builder](https://help.salesforce.com/s/articleView?id=ai.agent_builder_explore.htm).

Depending on which Agentforce Builder you're using, the method for acquiring the agent ID is different.

## Get Agent ID from Legacy Agentforce Builder

If you created your agent with the Legacy Agentforce Builder, you can find the agent ID directly in the URL of the Agent Overview Page.

1. From Setup, navigate to your agent.
2. When viewing the Agent Overview Page, look at the URL in your browser.
3. Copy the 18-character ID at the end of the URL.

For example, using this URL, `https://mydomain.salesforce-setup.com/lightning/setup/EinsteinCopilot/0XxSB000000IPCr0AO/edit`, the agent ID is `0XxSB000000IPCr0AO`.

## Get Agent ID from New Agentforce Builder

If you created your agent with the new Agentforce Builder, you need the bot ID from the [Bot](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_bot.htm) metadata type or the [BotDefinition](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_botdefinition.htm) standard object. The bot ID represents the agent ID in this case. In this example, we get the BotDefinition standard object in a [SOQL](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm) query using the agent's developer name:

```sfdocs-code {"lang":"sql", "title": "Query for Agent ID"}
SELECT Id, DeveloperName
FROM BotDefinition
WHERE DeveloperName = 'Agentforce_Service_Agent'
```

The `Id` field in the query result is your agent ID.

## See Also

- Agentforce Developer Guide: [Get Started with the Agent API](/docs/ai/agentforce/guide/agent-api-get-started.md)
- Metadata API Developer Guide: [Bot](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_bot.htm)
- Standard Object Reference: [BotDefinition](https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_botdefinition.htm)
- Salesforce Help: [Explore Agentforce Builder (Beta)](https://help.salesforce.com/s/articleView?id=ai.agent_builder_intro.htm)
- Salesforce Help: [Explore the Legacy Agentforce Builder](https://help.salesforce.com/s/articleView?id=ai.agent_builder_explore.htm)
