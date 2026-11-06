# Publish an Agent

Publishing an agent refers to using the Agent Script file to generate agent metadata, either the initial version of that metadata or new versions, which in turn results in either a new agent or a new version of an existing agent. The type of metadata depends on the API version:

- For Winter ‘27 (v68) or later, see [Agentforce Metadata Types (v68 and Later)](/docs/ai/agentforce/references/agents-metadata-tooling/agents-metadata.md).
- For Summer ‘26 (v67) or earlier, see [Agentforce Metadata Types (v67 and Earlier)](/docs/ai/agentforce/references/agents-metadata-tooling/agents-metadatav67.md)

You can then test this published agent, and later deploy it to your production org so you can activate it and make it available to your users. Publishing an agent is the pro-code equivalent of using the **Commit Version** button in your org's Agentforce Builder UI.

Let's drill down into what exactly happens when you publish an authoring bundle.

- The Agent Script file is first validated to make sure that it successfully compiles. If there are compilation errors, you must fix the Agent Script file before you can continue.
- When the Agent Script file successfully compiles, it's published to your org, which in turn creates the new associated metadata or new versions of the metadata if the agent exists in the org.
- The new or changed agent metadata is retrieved back to your DX project. You can skip this retrieval step if you want.
- The `<target>` element in the local authoring bundle's `*.bundle-meta.xml` metadata file is populated with information about the agent metadata, which is how an authoring bundle maps to its agent. Then the authoring bundle metadata component (`AiAuthoringBundle`) is deployed to your org.
- A new version of the authoring bundle is created in your org, although it's not retrieved back to the DX project. If you want all versions of your authoring bundle in your DX project, you must explicitly retrieve them as described in later tasks.

  After retrieving versioned authoring bundles, you can easily identify them because they have a version number appended to their directory (`My_Bundle_1`) in your package directory, and their `*-bundle-meta.xml` files contain the `<target>` element. Unversioned bundles are considered *draft*; you can publish only draft authoring bundles. You get an error if you try to publish a non-draft (versioned) authoring bundle.

:::tip
Because an *agent* is defined by its *authoring bundle*, this documentation and the Agentforce DX tools use the two terms interchangeably.

For example, the CLI command discussed in this topic uses the term *authoring bundle*, such as `agent publish authoring-bundle`. However, the equivalent VS Code command uses the term *agent*, such as **AFDX: Publish This Agent**.
:::

## Use VS Code to Publish an Authoring Bundle

1. In VS Code, open your Salesforce DX project and be sure you've authorized your development org.

2. If you want the publish command to skip the step of retrieving the new or changed metadata from the org to your DX project, enable the **Salesforce > Agentforce DX: Skip Retrieve** VS Code setting. The setting is disabled by default.

3. If you made any local changes in your Salesforce DX project to Apex classes or flows that implement your agent actions, then deploy them to your org using the **SFDX: Deploy This Source to Org** command.

4. Open the agent's `*.agent` file, which is located in the `aiAuthoringBundles/<API-name>` directory of your package directory, such as `force-app/main/default/aiAuthoringBundles/My_Bundle/My_Bundle.agent`.

5. Right-click inside the `*.agent` file and run the **AFDX: Publish this Agent** command.

   You can also run this command from the VS Code Command Palette or from the file explorer by right-clicking the `*.agent` file in your agent's authoring bundle.

   If the publish succeeds, you get a success message in the lower-right. If the **Skip Retrieve** setting is enabled, then your DX project and development org are synced with all the new or updated agent metadata. You can also now see your agent, or a new version of your agent, in the Agentforce Builder UI in your org.

6. If you want your DX project to contain all versions of an authoring bundle, retrieve them using a wildcard (`*`). For example, to retrieve all versions of the `My_Bundle` authoring bundle, run this command in the VS Code integrated terminal:

   ```bash
   sf project retrieve start --metadata "AiAuthoringBundle:My_Bundle*"
   ```

## Use a CLI Command to Publish an Authoring Bundle

1. Open a terminal (macOS/Linux) or command prompt (Windows) and change to your Salesforce DX project. Be sure you've authorized your development org.

   You can also run CLI commands from VS Code's integrated terminal.

2. If you made any local changes in your Salesforce DX project to Apex classes or flows that implement your agent actions, then deploy them to your org using the `project deploy start` command. For example, to deploy Apex classes, use this command:

   ```bash
   sf project deploy start --metadata ApexClass
   ```

3. Run this command:

   ```bash
   sf agent publish authoring-bundle
   ```

   The command displays a list of authoring bundle API names it found in the DX project and prompts you to choose the one you want to publish.

   If you haven't set a default org in your project, use the `--target-org` flag to specify the org's username or alias. Specify the `--skip-retrieve` flag to skip the step of retrieving the new or changed metadata from the org to your DX project. For more information, see [`agent publish authoring-bundle`](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_agent_publish_authoring-bundle.md) in the Salesforce CLI Command Reference.

   If the publish succeeds, you get a success message. If you didn't specify `--skip-retrieve`, then your DX project and development org are synced with all the new or updated agent metadata. You can also now see your agent, or a new version of your agent, in the Agentforce Builder UI in your org.

4. If you want your DX project to contain all versions of an authoring bundle, retrieve them using a wildcard (`*`). For example, to retrieve all versions of the `My_Bundle` authoring bundle, run this command:

   ```bash
   sf project retrieve start --metadata "AiAuthoringBundle:My_Bundle*"
   ```

## Next Steps

- [Preview and Debug an Agent](/docs/ai/agentforce/guide/agent-dx-nga-preview.md)
- [Test an Agent with Agentforce DX](/docs/ai/agentforce/guide/agent-dx-test.md)

## See Also

- [Agentforce Metadata Types](/docs/ai/agentforce/references/agents-metadata-tooling/agents-metadatav67.md)
- [*Salesforce CLI Command Reference*: agent Commands](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_agent_commands_unified.htm)
- [*Salesforce CLI Command Reference*: project Commands](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_project_commands_unified.htm)
