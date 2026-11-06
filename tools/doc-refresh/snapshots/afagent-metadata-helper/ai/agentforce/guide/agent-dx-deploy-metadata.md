# Move an Agent to a New Org

After you've created an agent in an org, move the agent to another org by retrieving and deploying its metadata. For example, to move an agent from sandbox to production, first retrieve the agent's metadata from the sandbox org to your local machine. Then, deploy the agent's metadata to the production org.

Agent metadata is [updated in API v68](/docs/ai/agentforce/references/agents-metadata-tooling/agents-metadata.md) and automatically includes the correct versions of all flow, Apex, and prompt template metadata that your specified agent uses. Although you no longer specify metadata for your agent's flow, Apex, and prompt templates, specify any other metadata that your agent uses, such as custom objects or fields.

:::important
To use v68 metadata to move agents between orgs, **both** orgs must be in API v68. While your sandbox org is in Winter '27 (v68) and your production org is in Summer '26 (v67), continue to use the previous metadata types. See [Define Agent Metadata (v67 and Earlier)](/docs/ai/agentforce/guide/agent-dx-api-v67-earlier.md).
:::

### Use a Manifest or the project retrieve start --metadata Command

This document shows you how to create a manifest file that defines the metadata you want to move. To define metadata on the command line, see [project retrieve start --metadata](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_project_retrieve_start.md#examples-for-project-retrieve-start).

For example:

```sfdocs-code {"lang":"bash", "title": "Use --metadata to Retrieve Version 3 of MyServiceAgent Plus Dependent Actions"}
sf project retrieve start --metadata AiAgentDefinitionVersion:MyServiceAgent#3 --root-type-with-dependencies AiAgentDefinitionVersion
```

## Step 1: Set Up Your Local Development Environment

1. Install [Salesforce CLI](https://developer.salesforce.com/docs/atlas.en-us.sfdx_setup.meta/sfdx_setup/sfdx_setup_install_cli.htm) or run `sf update` to install the latest version.

   :::important
   You need the latest version of Salesforce CLI to retrieve and deploy the latest version of Salesforce metadata.
   :::

2. [Authorize](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_auth.htm) your source and target orgs:

   ```sfdocs-code {"lang":"bash", "title": "Authorize an org with Salesforce CLI"}
   sf org login web --alias <org alias>
   ```

   When the login window appears, log in to your org and click **Allow**.

3. Ensure that you've enabled [Einstein and Agentforce](/docs/ai/agentforce/guide/agent-dx-set-up-env.md#agentforce-developer-environments) in your source and target orgs.

4. Ensure that you have the [required permissions](/docs/ai/agentforce/guide/agent-dx-set-up-env.md#assign-system-permissions) to publish and preview an agent in your source and target orgs.

## Step 2: Create a Salesforce DX Project

Create a Salesforce DX project to define your `package.xml` manifest and contain the retrieved metadata. First, change to the directory where you want to store the project. Then, use [`sf template generate project`](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_template_commands_unified.htm#cli_reference_template_generate_project_unified).

In this example, we use the standard project template because we don't need an example agent. We also use `--manifest` to create a sample `package.xml` file, which contains example metadata.

```sfdocs-code {"lang":"bash", "title": "Create a Standard Salesforce DX project with a Manifest"}
sf template generate project --name <name> --template standard --manifest
```

The command creates a Salesforce DX project on your local machine in the `<project name>` directory. The project contains an example `package.xml` manifest file.

## Step 3: Define Metadata in the Manifest File (v68 and Later)

Create a manifest to define the metadata you want to retrieve. You can copy and edit the default manifest that was created in your project at `manifest/package.xml`. To learn more about agent metadata, see [Agentforce Metadata Types (v68 and Later)](/docs/ai/agentforce/references/agents-metadata-tooling/agents-metadata.md). For example manifests, see [Specify All Versions of MyServiceAgent](#example-specify-all-versions-of-myserviceagent) and [Specify Versions 2 and 3 of MyServiceAgent](#example-specify-versions-2-and-3-of-myserviceagent).

For a successful deployment, define metadata correctly:

- The agent's top-level definition, `AiAgentDefinition`, must either exist in the target org or be defined in the same deploy.
- When deploying `AiAgentDefinition`, use `AiAgentDefinitionVersion` to include at least one agent version.
- A version can't be deployed in the same package as the matching legacy BotVersion.
- Agents built with Agent Script must include their `AiAuthoringBundle`.

If you're using API v67 or earlier, see [Define Agent Metadata (v67 and Earlier)](/docs/ai/agentforce/guide/agent-dx-api-v67-earlier.md).

### Specify Agent and Agent Version

- To specify an agent version, use `#<number>`.
- To specify all agent versions, use `#*`.

| Version to Specify         | Example     |
| -------------------------- | ----------- |
| Version 2 of MyAgent       | `MyAgent#2` |
| All versions of MyAgent    | `MyAgent#*` |
| All versions of all agents | `*`         |

### Use AiAgentDefinitionVersion to Define Actions

Don't define the metadata for your agent's flow, Apex, and prompt template actions. Instead, use the `--root-type-with-dependencies AiAgentDefinitionVersion` flag when you run the retrieve or deploy command to automatically retrieve the correct version of the agent's actions.

You must define other metadata types that your agent needs, such as custom fields or the `AiAuthoringBundle` for Agent Script agents.

### Example: Specify All Versions of MyServiceAgent

To deploy all versions of MyServiceAgent to a new org, use this manifest.

```xml
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <!-- The agent's top-level definition, AiAgentDefinition, must either exist in the target org or be defined in the same deploy. -->
        <members>MyServiceAgent</members>
        <name>AiAgentDefinition</name>
    </types>
    <types>
        <!-- When deploying AiAgentDefinition, use AiAgentDefinitionVersion to include at least one agent version. -->
        <members>MyServiceAgent#*</members>
        <name>AiAgentDefinitionVersion</name>
    </types>
    <!-- Include the AiAuthoringBundle for Agent Script-based agents. -->
    <types>
        <members>MyServiceAgent</members>
        <name>AiAuthoringBundle</name>
    </types>
    <version>68.0</version>
</Package>
```

### Example: Specify Versions 2 and 3 of MyServiceAgent

This manifest file defines version 2 and version 3 of MyServiceAgent.

```xml
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>MyServiceAgent</members>
        <name>AiAgentDefinition</name>
    </types>
    <types>
        <members>MyServiceAgent#2</members>
        <members>MyServiceAgent#3</members>
        <name>AiAgentDefinitionVersion</name>
    </types>
    <version>68.0</version>
</Package>
```

## Step 4: Retrieve Agent Metadata

After you define the metadata in your project's manifest (for example, `package.xml`), retrieve the agent's metadata to your local machine. Use the org's alias that you configured when [authorizing your org](#step-1-set-up-your-local-development-environment).

```sfdocs-code {"lang":"bash", "title": "Retrieve Agent Metadata from the Source Org"}
sf project retrieve start --manifest manifest/package.xml --root-type-with-dependencies AiAgentDefinitionVersion --target-org <org alias>
```

## Step 5: (Optional) Update Your Draft Agent's Username

Your retrieved metadata contains the agent usernames from the source org. To make your draft agent run on the target org without manual changes, use [string replacement](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_ws_string_replace.htm) to replace the username with the target org's username. Agents run in the context of a user, and the usernames on your source and target orgs are different. You can't use string replacement to update a committed agent's username, because committed agents can't be edited.

:::warning
Don't modify any other agent metadata that you retrieved. Deploying edited metadata can corrupt your org.
:::

If you deploy a draft agent to your target org without replacing the username, [manually update the agent's username](#set-the-agent-user-and-assign-permissions) before the agent can run on the target org.

See [Example: Configure String Replacement for Agent Username](/docs/ai/agentforce/guide/string-replace-example.md).

## Step 6: Deploy Agent Metadata to a New Org

After you retrieve your agent's metadata to your local project, deploy the metadata to the target org with the [deploy](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_project_commands_unified.htm#cli_reference_project_deploy_start_unified) command.

```sfdocs-code {"lang":"bash", "title": "Deploy agent metadata to the target org"}
sf project deploy start --manifest manifest/package.xml --root-type-with-dependencies AiAgentDefinitionVersion --target-org <org alias>
```

### Set the Agent User and Assign Permissions

Before you use your agent in the new org, assign the agent user. If you didn't replace the username during deployment, assign the agent user manually.

:::tip
You can't edit a **committed** agent. To add an agent user to a committed agent, first create a new agent version. Then, add the user to the new version.

After you've deployed an agent on your target org, the agents in both your source and target orgs must match, or future deployments are blocked. If you create a new version in your target org, create a corresponding version in your source org.
:::

Ensure that the agent user has sufficient permissions to carry out the agent's tasks. For example, if the agent reads a custom contact field, the agent user must have view permission on the custom field.

To learn more about agent users, see [create or assign the default agent user](/docs/ai/agentforce/guide/agent-dx-set-up-env.md#create-the-default-agent-user).
