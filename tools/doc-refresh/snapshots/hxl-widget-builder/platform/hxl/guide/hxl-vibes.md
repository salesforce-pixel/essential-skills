# Use Agentforce Vibes to Build HXL Widgets

Agentforce Vibes provides the `platform-widget-generate` skill that generates HXL widgets. The skill drafts a complete `UiWidgetBundle`, which includes the widget composition file, the `schema.json` attribute contract, and the `.uiwidget-meta.xml` configuration file.

For full details on the specific instructions and the skill's capabilities, see the `platform-widget-generate` skill in the [Salesforce Skills Library on GitHub](https://github.com/forcedotcom/sf-skills/tree/main/skills/platform-widget-generate).

## Supported Capabilities for the HXL Widget Skill

When you build HXL widgets with Agentforce Vibes, you can:

- **Generate complete bundles**: Describe a widget in natural language, and the skill outputs the composition file, `schema.json`, and `.uiwidget-meta.xml` file together in the `uiWidgets` folder.
- **Bind to your data**: The skill maps each attribute in `schema.json` to a component in the composition file and wires the bindings with `{!$attrs.attributeName}` token expressions.
- **Iterate in real time**: Refine a widget through follow-up prompts in your active session, and the skill updates the local files as you go.
- **Reuse existing metadata**: Generate a widget from metadata that you retrieve and provide, such as a custom Lightning type's `schema.json`.

## Set Up Your Development Environment

1. Install the Salesforce Extension Pack for Visual Studio Code (VS Code). See [Set Up the Agentforce Vibes Extension](https://developer.salesforce.com/docs/platform/agentforcevibes/guide/afv-get-started.md).

2. Complete the HXL prerequisites, including a connected Salesforce DX project with a `uiWidgets` folder. See [Prerequisites](/docs/platform/hxl/guide/prerequisites.md).

To verify which skills are active, click the **Skills** icon at the bottom of the Agentforce Vibes panel.

## Create a Lightning Type

A widget is useful only when it's associated with something that produces data, such as an action in Agentforce, or a tool on a custom MCP server. The custom Lightning type is what makes that association possible.

:::note
Vibe coding an MCP server isn't currently supported.
:::

Consider these differences.

- The `schema.json` file in the **Lightning type** defines the **data structure** and the rules for its validation, such as maximum length, type, and format. See [Building Blocks of a Lightning Type](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-core.md#building-blocks-of-a-lightning-type).
- The `schema.json` file in **widgets** defines the **attribute contract**. It outlines the attributes and their associated Lightning types that the widget accepts, including validation rules, data types, and display metadata. See [Attribute Contract](/docs/platform/hxl/references/hxl-reference-about/hxl-widgets-glossary.md#attribute-contract).

### Generate an Apex-Based Lightning Type

Before you generate a widget, [generate the custom Lightning type](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-skills.md). When you later prompt Agentforce Vibes to generate a widget, the `platform-widget-generate` skill discovers the existing Lightning type in your local project and maps its properties to the widget's attributes.

For example, run this prompt in the Agentforce Vibes chat interface to generate an Apex-based Lightning type and its supporting Apex classes:

**Create an Apex-based Lightning type hotelInfo with hotel name, image URL, price, and description as its attributes.**

Agentforce Vibes invokes the `platform-custom-lightning-type-generate` skill to create the Lightning type bundle.

:::note
The `platform-custom-lightning-type-generate` skill generates the Apex-based custom Lightning types based on an Apex class that's already present in the org. If the Apex class doesn't exist, Agentforce Vibes provides you the option to create the Apex class by using a different skill.
:::

To connect a widget to a Lightning type's dynamic data through [attribute mapping](/docs/platform/hxl/guide/hxl-rich-ui.md#connect-your-widget-to-a-custom-lightning-type), the widget bundle must include a `schema.json` file. Without it, the widget displays only static, hardcoded values.

## Generate a Widget

After the Lightning type exists in your local project, open the Agentforce Vibes panel, and enter a prompt that describes the widget that you want. Start your prompt with an action verb, and clearly describe the attributes that the widget accepts.

Based on your prompt, Agentforce Vibes automatically loads the `platform-widget-generate` skill and writes the UiWidgetBundle files to your local workspace.

Based on the previous prompt to create a Lightning type, you can run a prompt that creates a widget.

**Create a widget for the hotelInfo lightning type.**

:::note
Alternatively, you can build widgets in the [HXL Playground](/docs/platform/hxl/guide/playground.md) instead of entering a prompt in Agentforce Vibes, then copy and paste its JSON to use as the renderer for any action or property type.
:::

## Deploy the Metadata and Widget Bundles

To deploy your files to an org, start with the Apex class folder, followed by the `uiWidgets` folder and then the `lightningTypes` folder. You can run a Salesforce CLI `project deploy start` command, but you can also ask Agentforce Vibes to deploy and retrieve metadata for you. For example, run this prompt in the Agentforce Vibes chat interface:

**Deploy the Apex class and Lightning type I just created.**

For the CLI workflow and more on deploying and retrieving HXL metadata, see [Use HXL Widgets on MCP Channels](/docs/platform/hxl/guide/hxl-mcp-channels.md).

## Next Steps

After you deploy the metadata bundles:

- Review the generated files to understand the widget structure. See [Build Rich UI](/docs/platform/hxl/guide/hxl-rich-ui.md).
- Preview and refine widgets in the [HXL Playground](/docs/platform/hxl/guide/playground.md).

## Limitations

The skill has these constraints:

- The skill generates widgets from the properties that you describe or provide. It doesn't scan your org to discover existing widgets or metadata.
- The skill can't detect similar widgets or recommend them for reuse before you create a widget.
- You can't perform bulk updates across multiple widgets at the same time.
- The skill uses semantic styling, such as component variants and sizes, rather than pixel values.
