# Retrieve and Deploy Agent Metadata

Agents are made of metadata, just like any other Salesforce customization. So you use the standard Salesforce CLI `project retrieve` and `project deploy` commands, or their VS Code equivalents, to move agents between your Salesforce DX project and your orgs. This approach lets you store your agents in source control, review changes before you deploy them, and promote agents through your environments the same way that you promote the rest of your app.

How you retrieve and deploy depends on what you're trying to do.

| If you want to...                                                                                                 | See                                                                                      |
| ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Keep your development org and your DX project in sync while you build an agent, using pro-code or low-code tools. | [Synchronize Your Org with Your DX Project](/docs/ai/agentforce/guide/agent-dx-synch.md) |
| Move a finished agent from one org to another, such as from a sandbox to production.                              | [Move an Agent to a New Org](/docs/ai/agentforce/guide/agent-dx-deploy-metadata.md)      |

## See Also

- [*Salesforce CLI Command Reference*: project Commands](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_project_commands_unified.htm)
- [Agentforce Metadata Types](/docs/ai/agentforce/references/agents-metadata-tooling/agents-metadata.md)
- [Publish an Agent](/docs/ai/agentforce/guide/agent-dx-nga-publish.md)
