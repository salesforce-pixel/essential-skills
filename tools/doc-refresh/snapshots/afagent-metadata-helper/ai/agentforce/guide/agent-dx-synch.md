# Synchronize Your Development Org with Your DX Project

Whether you use pro-code or low-code tools to modify your agent, you always want to keep your development org and your Salesforce DX project synchronized. Agents are made of metadata, just like any other Salesforce customization, so you use the standard Salesforce DX CLI and VS Code commands to retrieve, deploy, and delete agents.

## Basic Retrieval and Deployment of Metadata: A Refresher

Let's first go over the standard way you use Salesforce DX to retrieve or deploy any metadata between your DX project and your org.

If your development org is enabled for source tracking, and you change metadata in your org, use these standard CLI commands to first check for changes and then retrieve them to your DX project.

```bash
sf project retrieve preview --target-org my-dev-org
sf project retrieve start --target-org my-dev-org
```

Because you didn't specify which metadata components to retrieve, then the preceding commands preview or retrieve anything that changed, including agents.

Deploying is similar, except you use the `project deploy` commands:

```bash
sf project deploy preview --target-org my-dev-org
sf project deploy start --target-org my-dev-org
```

Again, because you didn't specify which metadata components to deploy, the preceding commands preview or deploy anything that changed, including agents.

In VS Code, use the equivalent **SFDX: Retrieve This Source from Org** or **SFDX: Deploy This Source to Org** commands.

If your development org isn’t enabled for source tracking, you're required to specify the specific metadata that you want to retrieve or deploy using one of these flags: `--metadata`, `--source-dir`, or `--manifest`. For example:

```bash
sf project retrieve start --metadata ApexClass --target-org my-dev-org
sf project retrieve start --source-dir force-app --target-org my-dev-org
sf project retrieve start --manifest package.xml --target-org my-dev-org
```

Agents are a bit more complex than standard Salesforce metadata types, so continue reading to understand the nuances when using `--metadata` or `--manifest` with them.

## Deploy, Retrieve, and Delete Agent Metadata

As we've discussed in this guide, agents use Agent Script as their underlying blueprint. The Agent Script file is stored in the agent's associated `AiAuthoringBundle` metadata component. When you code an agent, either in VS Code or the in-org Agentforce Builder, you update its Agent Script file.

When you later publish this agent, several things happen both in your DX project and in your org. Read these sections before you continue so you understand how all this works:

- The introduction of [Publish an Agent](/docs/ai/agentforce/guide/agent-dx-nga-publish.md)
- [Agentforce Metadata Types](/docs/ai/agentforce/references/agents-metadata-tooling/agents-metadatav67.md)

Now that you understand the metadata associated with authoring bundles and published agents, let's learn how to synchronize both between your DX project and org.

### Synchronize Authoring Bundle Metadata

Use `--metadata AiAuthoringBundle:<api-name>` to specify an authoring bundle by its API name. Use a wildcard to specify all versions of an authoring bundle (`--metadata AiAuthoringBundle:Local_Info_Agent*`).

**Retrieve**

To retrieve an agent's associated authoring bundle to your DX project, use the `project retrieve start` CLI command. Run this command from the VS Code integrated terminal or by using a terminal (macOS, Linux) or command prompt (Windows) from your DX project. For example:

```bash
sf project retrieve start --metadata AiAuthoringBundle:Local_Info_Agent --target-org my-dev-org
```

**Deploy**

This command deploys the `Local_Info_Agent` authoring bundle to your org:

```bash
sf project deploy start --metadata AiAuthoringBundle:Local_Info_Agent --target-org my-dev-org
```

**Delete**

This command deletes the `Local_Info_Agent` authoring bundle:

```bash
sf project delete source --metadata AiAuthoringBundle:Local_Info_Agent --target-org my-dev-org
```

The command prompts you before it deletes anything. If you confirm, it deletes the authoring bundle and any associated agent metadata (`Bot`, `BotVersion`, and `GenAiPlannerBundle`). It doesn't delete any Apex classes or flows that implement the agent actions.

### Synchronize Published Agent Metadata

To make it easier to deploy, retrieve, and delete published agents when your org doesn’t use source tracking, use the “pseudo” metadata type called `Agent`. `Agent` isn’t a real metadata type, it’s just a shorthand way to tell the relevant CLI commands to work on all the metadata components that make up the agent. The syntax is `Agent:Agent_API_Name`.

**Retrieve**

To retrieve all metadata associated with a published agent to your DX project, use the `project retrieve start` CLI command and specify the `Agent` pseudo metadata type with the `--metadata` flag. Run this command from the VS Code integrated terminal or by using a terminal (macOS, Linux) or command prompt (Windows) from your DX project. For example:

```bash
sf project retrieve start --metadata Agent:Local_Info_Agent --target-org my-dev-org
```

In addition to the agent metadata (`Bot`, `BotVersion`, and `GenAIXXX`), the command also retrieves Apex classes and flows that implement any of the agent actions.

**Deploy**

To deploy local metadata associated with the same agent back to the org, run a command like this:

```bash
sf project deploy start --metadata Agent:Local_Info_Agent --target-org my-dev-org
```

The command deploys the agent metadata (`Bot`, `BotVersion`, and `GenAiXXX`), but not the Apex classes or flows that implement the agent actions.

**Delete**

Next let’s look at deleting. If you tried to create an agent and it was only partly created in the development org, use the `delete` command to clean up everything, both in your org and in your DX project. You can also use this command to delete an inactive agent in your org.

```bash
sf project delete source --metadata Agent:Local_Info_Agent --target-org my-dev-org
```

The command prompts you before it deletes anything. If you confirm, it then deletes only the agent metadata (`Bot`, `BotVersion`, and `GenAiXXX`); it doesn't delete any Apex classes or flows that implement the agent actions.

### See Also

- [*Salesforce CLI Command Reference*: project Commands](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_project_commands_unified.htm)
- [Agentforce Metadata Types](/docs/ai/agentforce/references/agents-metadata-tooling/agents-metadatav67.md)
