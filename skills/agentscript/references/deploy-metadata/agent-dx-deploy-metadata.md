# Use Metadata to Move an Agent to a New Org

After you've created an agent in an org, either by using the [Agentforce UI](https://help.salesforce.com/s/articleView?id=ai.copilot_intro.htm&type=5) or [Agentforce DX](../agent-dx.md), you can move the agent to another org by retrieving and deploying its metadata. For example, to move an agent from a sandbox org to a production org, first retrieve the agent's metadata from the sandbox org to your local machine. Then, deploy the agent's metadata to the production org.

This document uses [Salesforce CLI commands](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_top.htm) to retrieve and deploy the agent's metadata. To use VS Code, see [Salesforce Extensions for VS Code](https://developer.salesforce.com/docs/platform/sfvscode-extensions/guide/deploy-changes.html).

## Step 1: Set Up Your Local Development Environment

1. Install [Salesforce CLI](https://developer.salesforce.com/docs/atlas.en-us.sfdx_setup.meta/sfdx_setup/sfdx_setup_install_cli.htm).

   To test your setup, run `sf search` and see the list of CLI commands.

2. [Authorize](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_auth.htm) your source and target orgs by using Salesforce CLI:

```sfdocs-code {"lang":"bash", "title": "Authorize an Org with Salesforce CLI"}
sf org login web --alias <org alias>
```

When the login window appears, log in to your org and click **Allow**.

1. Ensure you've enabled [Einstein and Agentforce](../agent-dx-set-up-env.md#agentforce-developer-environments) in your source and target orgs.
2. Ensure that you have the [required permissions](../agent-dx-set-up-env.md#assign-system-permissions) to publish and preview an agent in your source and target orgs.

## Step 2: Create a Salesforce DX project

Create a Salesforce DX project to define your `package.xml` manifest and contain the retrieved metadata. First, change to the directory where you want to store the project. Then, use [`sf template generate project`](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_template_commands_unified.htm#cli_reference_template_generate_project_unified).

In this example, we use the standard project template because we don't need an example agent. We also use `--manifest` to create a sample `package.xml` file, which contains example metadata.

```sfdocs-code {"lang":"bash", "title": "Create a Standard Salesforce DX project with a Manifest"}
sf template generate project --name <name> --template standard --manifest
```

A Salesforce DX project is created on your local machine in the `<project name>` directory; the project contains an example `package.xml` manifest file.

## Step 3: Define Metadata in the Manifest File

Create a manifest to define the metadata you want to retrieve. You can copy and edit the default manifest that was created in your project at `manifest/package.xml`.

### Understand Agent and Legacy Agent Metadata

- Draft (uncommitted) agents and agent versions are represented by `AiAuthoringBundle`. A draft agent is editable until it's committed.
- Committed agents and agent versions are represented by `AiAuthoringBundle`, plus `Bot` and `BotVersion`. You can't change a committed agent. Instead, create a new version.
- Legacy agents don't have a commit stage, and are represented by `Bot` and `BotVersion` (not `AiAuthoringBundle`). You can edit and overwrite an active legacy agent.

| Agent Type      | Metadata Representation                      |
| :-------------- | :------------------------------------------- |
| Draft Agent     | `AiAuthoringBundle`                          |
| Committed Agent | `AiAuthoringBundle` + `Bot` and `BotVersion` |
| Legacy Agent    | `Bot` and `BotVersion`                       |

For more details, see [Agent Metadata: A Shallow Dive](../agent-dx-metadata.md) and [Agentforce Metadata Types](/docs/ai/agentforce/references/agents-metadata-tooling/agents-metadata.html).

### Example Package.xml Manifest Files

Use these examples to get started:

- Replace the version number (for example, `<version>65.0</version>`) with your required metadata version. Your project's sample `package.xml` manifest contains the most recent version number.
- Add any other metadata types that your agent needs, such as Data 360 dependencies.

| Example Manifest                                                                                   | Description                                                                                                                               | Notes                                                                                                                                                                                                                                                               |
| -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [All Agents](./package-allagents.md)                                                               | Defines metadata for all agents, including legacy agents. Includes metadata for all flows, prompt templates, and Apex classes in the org. | Replace the `*` wildcard with the API names of the ApexClass, Flows, and GenAiPromptTemplates that your agents use. Using wildcards for these types can pull excessive data, leading to very long deployments or timeouts.                                          |
| [Single Agent Version](./package-singleagent.md)                                                   | Defines a single version of an agent, plus the flows, prompt templates, and Apex class types that the agent version uses.                 | Before deploying a single agent version into an org (using `BotVersion`), you must have deployed the full agent to the org. Deploying the agent before deploying a specific version ensures that all required metadata and artifacts are created in the target org. |
| [Single Agent Version with Different Bot/AiAuthoringBundle Versions](./package-single-mismatch.md) | Defines a single agent version when the `AiAuthoringBundle` version doesn't match the `Bot`/`BotVersion` version.                         | This difference can happen when you save more versions than you commit. See [Step 4 - Update Your Manifest for Different Bot/AiAuthoringBundle Versions](#step-4-optional---update-your-manifest-for-different-botaiauthoringbundle-versions).                      |

#### Update Your Manifest

To define a single agent version, make these changes to your manifest.

1. Instead of `Bot`, which is the top-level representation of an agent, use `BotVersion`, which represents the configuration for a specific agent version. Include the agent version's name and version number. For example:

```sfdocs-code {"lang":"xml", "title": "Specify a BotVersion in the Manifest"}
<types>
   <members>NGA_Service_Agent.v2</members>
   <name>BotVersion</name>
</types>
```

2. Instead of using the agent's name to specify `AiAuthoringBundle` and `GenAiPlannerBundle`, use the agent's versioned name. For example:

```sfdocs-code {"lang":"xml", "title": "Reference an Agent Version by Its Versioned Name"}
<types>
   <members>NGA_Service_Agent_2</members>
   <name>AiAuthoringBundle</name>
<types>
   <members>AgentforceServiceAgent_v2</members>
   <name>GenAiPlannerBundle</name>
</types>
</types>
```

## Step 4: (Optional) - Update Your Manifest for Different Bot/AiAuthoringBundle Versions

Use these steps to specify the correct versions for your agent's metadata.

### What are mismatched `Bot`/`AiAuthoringBundle` versions?

When you save an agent version, Agentforce creates `AiAuthoringBundle` metadata. When you commit an agent version, Agentforce creates Bot/BotVersion metadata. If you save more versions than you commit, the version of your `AiAuthoringBundle` won't match the version of your Bot/BotVersion.

For example, this agent has 11 versions of an agent and 7 committed versions. Therefore, the agent's metadata contains 11 versions of `AiAuthoringBundle` and 7 versions of `Bot` and `BotVersion`. You'll need to specify the correct version numbers to match the correct `AiAuthoringBundle` to the correct `Bot` and `BotVersion`.

> *[Image removed — see online documentation]*

To find the matching `Bot` version, open the AiAuthoringBundle folder for your desired version. In the agent version's `bundle-meta.xml` file, the `target` metadata shows the version to use for the `GenAiPlannerBundle` and `BotVersion`.

For example, version 9 of the agent "TestAgentFromSource" uses version 7 of `GenAiPlannerBundle` and `BotVersion`.

> *[Image removed — see online documentation]*

Use these versions to specify your manifest, for example [Manifest for Different Bot/AiAuthoringBundle Versions](./package-single-mismatch.md)

## Step 5: Retrieve Agent Metadata

After defining the metadata in your project's manifest (for example, `package.xml`), retrieve the agent's metadata to your local machine. Use the org's alias that you configured when [authorizing your org](#step-1-set-up-your-local-development-environment).

```sfdocs-code {"lang":"bash", "title": "Retrieve Agent Metadata from the Source Org"}
sf project retrieve start --manifest manifest/package.xml --target-org <org alias>
```

For more information about retrieving and deploying metadata, see [Basic Retrieval and Deployment of Metadata: A Refresher](../agent-dx-synch.md#basic-retrieval-and-deployment-of-metadata-a-refresher).

## Step 6: (Optional) Update Agent Username

Your retrieved metadata contains the agent username(s) from the source org. To enable your agent to run out-of-the-box on the target org, use [string replacement](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_ws_string_replace.htm) to update the username with the target org's username. Agents run in the context of a user, and the usernames on your source and target orgs are different.

:::note
If you deploy an agent to your target org without replacing the username, you'll need to [manually update the agent's username](#set-the-agent-user-and-assign-permissions) before it can run on the target org.
:::

See [Example - Configure String Replacement for Agent Username](string-replace-example.md).

## Step 7: Deploy Agent Metadata to a New Org

Once you've retrieved your agent's metadata to your local project, you can deploy the metadata to a new org.

:::important
Don't modify the metadata that you retrieved. Uploading edited metadata to an org can corrupt your org. )
:::

Use the right [deploy](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_project_commands_unified.htm#cli_reference_project_deploy_start_unified) command for your project.

```sfdocs-code {"lang":"bash", "title": "Deploy Agent Metadata to the Target Org"}
sf project deploy start  --source-dir force-app --target-org my-target
```

### Set the Agent User and Assign Permissions

Before using your agent in the new org, you must assign the agent user. If you didn't configure the agent's user during deployment, manually configure the agent's user.

:::tip
You can't edit a **committed** agent. To add an agent user to a committed agent, first create a new agent version. Then, add the user to the new version.
:::

Ensure the agent user has sufficient permissions to carry out the agent's tasks. For example, if the agent reads a custom contact field, the agent user must have view permission on the custom field.

To learn more about agent users, see [create or assign the default agent user](../agent-dx-set-up-env.md#create-the-default-agent-user).
