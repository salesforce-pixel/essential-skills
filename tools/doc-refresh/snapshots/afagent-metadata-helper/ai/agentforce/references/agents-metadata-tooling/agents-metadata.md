# Agentforce Metadata Types (v68 and Later)

To manage agents, agent actions, and subagents, use the [Metadata API](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_intro.htm).

:::important
Agent metadata changed in v68. To learn more, see [Move an Agent to a New Org](/docs/ai/agentforce/guide/agent-dx-deploy-metadata.md).
:::

![Agent metadata hierarchy](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/bot-agent-metadata68.png)

## Metadata Types

- [AiAuthoringBundle](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_aiauthoringbundle.htm): Represents an AI authoring bundle, which contains the blueprint of an agent. For example, an AI authoring bundle for an Agentforce agent contains:
  - An [Agent Script](/docs/ai/agentforce/guide/agent-script.md) file, stored in `<bundle-api-name>.agent`
  - A Metadata API XML file, stored in `<bundle-api-name>.bundle-meta.xml`
- [AiAgentDefinition](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_AiAgentDefinition.htm): Represents the definition of an Agentforce agent, including its type, context variables, and conversation settings.
- [AiAgentDefinitionVersion](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_AiAgentDefinitionVersion.htm): Represents a version of an Agentforce agent definition, including its dialogs, conversation variables, planner configuration, and behavior settings.
- [GenAiFunction](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_genaifunction.htm): Represents an action that you can add to agents.
- [GenAiPlugin](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_genaiplugin.htm): Represents an agent's subagent.

## Metadata Types No Longer Used in Agentforce Agents

In v68 and later releases, these metadata types are no longer used to represent Agentforce agents:

- [Bot](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_bot.htm) and [BotVersion](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_botversion.htm): Used only by Einstein Bots, not by Agentforce agents.
- [GenAiPlannerBundle](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_genaiplannerbundle.htm): Doesn't exist in v68 and later releases.

## See Also

- [Agentforce DX](/docs/ai/agentforce/guide/agent-dx.md): Manage agents by using pro-code tools.
- [Move an Agent to a New Org](/docs/ai/agentforce/guide/agent-dx-deploy-metadata.md): Use Salesforce DX and agent metadata to move your agent to a new org.
