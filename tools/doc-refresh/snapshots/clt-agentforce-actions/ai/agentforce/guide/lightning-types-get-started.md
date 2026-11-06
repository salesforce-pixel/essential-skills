# Get Started with Custom Lightning Types

These resources are available to help you customize your agent’s interface.

| I want to...                                                                                                                                          | Recommended Content                                                                                                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Build using the Setup UI**<br></br>Create and configure custom Lightning types directly in Setup.                                                   | [Create a Custom Lightning Type](https://help.salesforce.com/s/articleView?id=platform.lt_intro.htm&type=5)                                                                                                   |
| **Understand the architecture**<br></br>Learn the core concepts, file structure, and how schema projection works.                                     | [Core Concepts of Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-core.md)                                                                       |
| **Choose my approach**<br></br>Decide whether to use an Apex class or define a manual JSON schema.                                                    | [Categories of Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types.md#categories-of-custom-lightning-types)                                          |
| **Start building**<br></br>Create the definition by structuring the LightningTypeBundle metadata.                                                     | [Get Started with Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types.md)                                                                                   |
| **Build with AI**<br></br>Use the Lightning Types skill in Agentforce Vibes to generate schemas and UI configurations using natural language prompts. | [Use Agentforce Vibes to Build Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-skills.md)                                                        |
| **Customize the UI**<br></br>Build `editor.json` and `renderer.json` files to override the default interface with your own Lightning web components.  | [UI Configuration for Apex-Based Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-apex.md#ui-configuration-for-apex-based-custom-lightning-types) |
| **Deploy and manage**<br><br>Deploy your custom Lightning types and Lightning web components using Metadata API or Salesforce CLI.                    | [LightningTypeBundle Metadata Type](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-core.md#lightningtypebundle-metadata-type)                                           |
| **Integrate and test**<br></br>Assign your custom Lightning type to an agent action, and verify the behavior in Agentforce Builder.                   | [Integrate a Custom Lightning Type with an Agent Action](/docs/ai/agentforce/guide/lightning-types-standard.md#integrate-a-custom-lightning-type-with-an-agent-action)                                        |

## Developer Resources

Use these resources to automate, deploy, and reference custom Lightning types.

**Metadata API and Deployment**

Use the LightningTypeBundle metadata type to define and deploy your custom Lightning types. Understand the required file structure, supported fields, and how to structure your `package.xml` manifest for deployment.

- *Metadata API Developer Guide*: [LightningTypeBundles](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_lightningtypebundle.htm)

**Standard Lightning Type References**

Review the keywords and default behaviors for the Salesforce types.

- *Lightning Types Developer Guide*: [Standard Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/references/lightning-types/lightning-types-reference.md)

**Connect API**

Retrieve information about the types available in your org by using Connect REST API.

- *Connect REST API Developer Guide*: [Type System Resources](https://developer.salesforce.com/docs/atlas.en-us.chatterapi.meta/chatterapi/connect_resources_type_system_resources.htm)

**Lightning Types Skill**

Accelerate development by using Agentforce Vibes to generate LightningTypeBundle metadata files through natural language prompts.

- *Lightning Types Developer Guide*: [Use Agentforce Vibes to Build Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-skills.md)

**See Also**

- [Get Started with Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types.md)
- [Apex-Based Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-apex.md)
- [Salesforce Applications That You Can Override](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-core.md#salesforce-applications-that-you-can-override)
