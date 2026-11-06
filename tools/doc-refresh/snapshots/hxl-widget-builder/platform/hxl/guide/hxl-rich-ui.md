# Build Rich UI Experiences with HXL Widgets

Widgets are platform-independent UI compositions. With widgets, you define rich, interactive interfaces once and deploy them across supported Salesforce applications and third-party platforms.

You build widgets by defining their composition in JSON files. Understand these core concepts to compose and deploy widgets.

## Supported Applications and Platforms

Widgets can be deployed to:

- Agentforce Employee agent in Lightning Experience
- ChatGPT (via Model Context Protocol)
- Claude (via Model Context Protocol)
- Slackbot (via Model Context Protocol)

## Building Blocks of a Widget

A widget consists of these building blocks.

- **Composition file** defines the visual UI composition. It specifies which components render, their hierarchical nesting, ordering, and data bindings by using `{!$attrs.attributeName}` token expressions.
- **Widget configuration file** defines the widget’s label, description, and type.
- **Schema file** defines the attribute contract. It outlines the attributes and their associated Lightning types that the widget accepts, including validation rules, data types, and display metadata.

## UiWidgetBundle Metadata Type

The UiWidgetBundle metadata type describes the widgets. It's available in API version 67.0 and later.

## Understand the UiWidgetBundle Structure

UiWidgetBundle components are stored in the `uiWidgets` folder and consist of a [composition file](/docs/platform/hxl/guide/hxl-widget-composition.md), [widget configuration file](/docs/platform/hxl/guide/hxl-widget-configuration.md), and optional [schema file](/docs/platform/hxl/guide/hxl-widget-schema.md). See [UiWidgetBundle](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_uiwidgetbundle.htm).

For a detailed example of this structure, see [Example: Mapping a Hotel Card Widget](/docs/platform/hxl/guide/hxl-widget-example-mapping.md).

### Use Salesforce CLI or Metadata API to Deploy UiWidgetBundles

To deploy a UiWidgetBundle to your Salesforce org, use Metadata API or Salesforce CLI commands. Metadata API uses a manifest file that defines the metadata that you want to deploy.

Here’s an example `package.xml` manifest file for a UiWidgetBundle that includes the widget `hotelCard`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>hotelCard</members>
        <name>UiWidgetBundle</name>
    </types>
    <version>67.0</version>
</Package>
```

To delete a widget, you must deploy a `destructiveChanges` package to your org that lists the widgets to delete.

**See Also**

- *Metadata API Developer Guide*: [Deploying and Retrieving Metadata with the Zip File](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/file_based_zip_file.htm)
- *Metadata API Developer Guide*: [Deleting Components from an Organization](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy_deleting_files.htm)

### Salesforce CLI Commands

Use the Salesforce CLI `project` commands to deploy, retrieve, and track the source files for the UiWidgetBundle metadata type in your Salesforce DX project. See [project Commands](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_project_commands_unified.htm#cli_reference_project_commands_unified) in the Salesforce CLI Command Reference.

This example shows how to deploy a UiWidgetBundle called `hotelCard` to an org with alias `my-org`:

```
sf project deploy start --metadata UiWidgetBundle:hotelCard --target-org my-org
```

## Connect Your Widget to a Custom Lightning Type

To render dynamic data in a widget, connect the widget to a custom Lightning type. In the custom Lightning type’s `renderer.json` file, reference the widget and map properties defined by the custom Lightning type to attributes defined in the widget’s `schema.json` file.

The widget bundle’s composition file, widget configuration file, and schema file don’t change based on the supported Salesforce application or third-party platform where the widget renders.

:::note
Don’t use the Lightning Types page in Setup to create or modify custom Lightning types that reference widgets. Define and update these custom Lightning types in your Salesforce DX project, and deploy the LightningTypeBundle metadata by using Salesforce CLI or Metadata API.
:::

### Choose the Custom Lightning Type Configuration

Choose the custom Lightning type configuration based on the scenario in which the widget renders.

| Rendering Scenario                                        | Custom Lightning Type Configuration                                                                         | Widget Attribute Mapping              |
| --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| Agentforce action output rendered in Lightning Experience | One Apex-based custom Lightning type                                                                        | Direct mapping                        |
| MCP server tool output rendered in an MCP channel         | Two object-based custom Lightning types, one in the MCP result wrapper role and one in the MCP payload role | Nested mapping through `outputValues` |

For Agentforce action output, the Apex-based custom Lightning type references the Apex class that defines the structured output’s schema. The custom Lightning type’s `renderer.json` file maps properties from that schema directly to attributes defined in the widget’s `schema.json` file.

For MCP server tool output from invocable actions, primarily Apex invocable actions exposed as MCP tools, create two object-based custom Lightning types. This configuration currently applies only to invocable actions exposed as MCP tools. Follow this fixed structure:

- The **MCP result wrapper custom Lightning type** represents the complete result returned by the MCP server tool, including `actionName`, `isSuccess`, and `outputValues`.
- The **MCP payload custom Lightning type** defines the structure referenced by the MCP result wrapper custom Lightning type’s `outputValues` property.

The terms [MCP result wrapper custom Lightning type](https://developer.salesforce.com/docs/platform/hxl/references/hxl-reference-about/hxl-widgets-glossary.md#mcp-result-wrapper-custom-lightning-type) and [MCP payload custom Lightning type](https://developer.salesforce.com/docs/platform/hxl/references/hxl-reference-about/hxl-widgets-glossary.md#mcp-payload-custom-lightning-type) describe roles in this configuration. They aren’t categories of custom Lightning types. Both are object-based custom Lightning types.

The `outputValues` property in the MCP result wrapper custom Lightning type references the MCP payload custom Lightning type. The MCP result wrapper custom Lightning type’s `renderer.json` file maps properties under `outputValues` to widget attributes.

For general information about creating custom Lightning types, see [Apex-Based Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-apex.md) and [Object-Based Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-object.md).

### Reference the Widget

Reference your widget in the Lightning type's `renderer.json` file by using the `componentOverrides` syntax. The `definition` field uses this format: `@widget/{namespace}/{widgetName}`

- Local Org (`@widget/c/hotelCard`): References a widget named `hotelCard` in your org’s namespace.

This example shows a basic widget reference:

```json
{
  "renderer": {
    "componentOverrides": {
      "$": {
        "definition": "@widget/c/hotelCard"
      }
    }
  }
}
```

For Agentforce action output, add `renderer.json` to the Apex-based custom Lightning type.

For MCP server tool output, add `renderer.json` to the MCP result wrapper custom Lightning type.

For widget references, create a `renderer.json` file at the root level (parallel to `schema.json`) in the Lightning type folder, without channel-specific subfolders.

:::note
Referencing widgets in `editor.json` isn’t currently supported. When you reference a widget in a Lightning type, create a `renderer.json` file at the root level (parallel to `schema.json`). Don’t use channel-specific subfolders. This structure differs from Lightning Web Component (LWC) overrides, which use channel-specific subfolders (such as `lightningDesktopGenAi/`). See [Lightning Type Structure for Widgets (Beta)](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-core.md#lightning-type-structure-for-hxl-widgets-beta).
:::

### Widget Attribute Mapping

Attribute mapping connects the data properties represented by a custom Lightning type to attributes defined in the widget’s `schema.json` file. Define the mapping in the attributes object of the custom Lightning type’s `renderer.json` file.

In the renderer’s attributes object, each entry maps a custom Lightning type property to a widget attribute.

- The key is an attribute defined in the widget’s `schema.json` file.
- The value references a property or nested property represented by the custom Lightning type. Use an expression such as `{!$attrs.propertyName}` for a direct property or `{!$attrs.parentProperty.propertyName}` for a nested property.

:::note
Attribute mapping requires a `schema.json` file in your widget to define the attributes. Widgets without a `schema.json` file can only display static content.
:::

The property reference depends on the rendering scenario:

- Agentforce action output uses direct property references.
- MCP server tool output uses nested property references through `outputValues`.

#### Map Agentforce Action Output

For Agentforce action output rendered in Lightning Experience, map properties represented by the Apex-based custom Lightning type directly to widget attributes.

This example shows attribute mapping in a `renderer.json` file that connects properties represented by the custom Lightning type to the `hotelCard` widget.

```json
{
  "renderer": {
    "componentOverrides": {
      "$": {
        "definition": "@widget/c/hotelCard",
        "attributes": {
          "hotelId": "{!$attrs.hotelId}",
          "name": "{!$attrs.name}",
          "city": "{!$attrs.city}",
          "checkInTime": "{!$attrs.checkInTime}",
          "checkOutTime": "{!$attrs.checkOutTime}",
          "pricePerNight": "{!$attrs.pricePerNight}",
          "rating": "{!$attrs.rating}"
        }
      }
    }
  }
}
```

In this example:

- The keys (`hotelId`, `name`, `city`, `checkInTime`, `checkOutTime`, `pricePerNight`, and `rating`) are attributes defined in the widget’s `schema.json` file.
- The values (`{!$attrs.hotelId}`, `{!$attrs.name}`, `{!$attrs.city}`, `{!$attrs.checkInTime}`, `{!$attrs.checkOutTime}`, `{!$attrs.pricePerNight}`, and `{!$attrs.rating}`) directly reference properties represented by the Apex-based custom Lightning type.

For information about creating the custom Lightning type, see [Apex-Based Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-apex.md).

#### Map MCP Server Tool Output

For a custom MCP server tool rendered in ChatGPT, Claude, or Slackbot, the MCP result wrapper custom Lightning type defines the `outputValues` property. The `lightning:type` value of `outputValues` references the MCP payload custom Lightning type.

In the MCP result wrapper custom Lightning type’s `renderer.json` file, use nested property references through `outputValues` to map MCP server tool output to widget attributes.

This example maps hotel information represented by an MCP result wrapper custom Lightning type to the `hotelCard` widget.

```json
{
  "renderer": {
    "componentOverrides": {
      "$": {
        "definition": "@widget/c/hotelCard",
        "attributes": {
          "hotelId": "{!$attrs.outputValues.hotelInfo.hotelId}",
          "name": "{!$attrs.outputValues.hotelInfo.name}",
          "city": "{!$attrs.outputValues.hotelInfo.city}",
          "checkInTime": "{!$attrs.outputValues.hotelInfo.checkInTime}",
          "checkOutTime": "{!$attrs.outputValues.hotelInfo.checkOutTime}",
          "pricePerNight": "{!$attrs.outputValues.hotelInfo.pricePerNight}",
          "rating": "{!$attrs.outputValues.hotelInfo.rating}"
        }
      }
    }
  }
}
```

In this example:

- The keys (`hotelId`, `name`, `city`, `checkInTime`, `checkOutTime`, `pricePerNight`, and `rating`) are attributes defined in the widget’s `schema.json` file.
- `$attrs.outputValues` references the `outputValues` property in the MCP result wrapper custom Lightning type. The `lightning:type` value of this property references the MCP payload custom Lightning type.
- `hotelInfo` is a property defined in the MCP payload custom Lightning type. Its `lightning:type` value references the `HotelSearchResult.Hotel` Apex class.
- The final segment of each property reference, such as `hotelId`, `name`, or `rating`, references a field in the `HotelSearchResult.Hotel` Apex class.

The widget schema remains a flat attribute contract. Don’t reproduce the `outputValues` structure in the widget’s `schema.json` file. Only the MCP result wrapper custom Lightning type’s `renderer.json` file references the nested MCP server tool result structure.

For the required custom Lightning type configuration and MCP-specific schema requirements, see [Configure Custom Lightning Types for an MCP Server Tool](/docs/platform/hxl/guide/hxl-rich-ui.md#configure-custom-lightning-types-for-an-mcp-server-tool).

**See Also**

- [Get Started with Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types.md)
- [Example: Mapping a Hotel Card Widget for Agentforce](/docs/platform/hxl/guide/hxl-widget-example-mapping.md)
- [Example: Mapping a Hotel Card Widget for MCP](/docs/platform/hxl/guide/hxl-widget-example-mapping-mcp.md)

## Configure Custom Lightning Types for an MCP Server Tool

To render MCP server tool output in a widget, create two object-based custom Lightning types: an MCP result wrapper custom Lightning type and an MCP payload custom Lightning type. These terms describe the roles of the custom Lightning types in this configuration, not categories of custom Lightning types.

For general information about object-based custom Lightning types, see [Object-Based Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-object.md).

### Understand the Custom Lightning Type Roles

A custom MCP server tool returns a result containing `actionName`, `isSuccess`, and `outputValues`. At runtime, the `outputValues` property contains the action-specific payload.

Because a custom Lightning type can’t reference itself, use a separate MCP payload custom Lightning type to define the structure of the payload. The `lightning:type` value of `outputValues` references this custom Lightning type.

The MCP result wrapper custom Lightning type represents the complete MCP server tool result. Its `outputValues` property references the MCP payload custom Lightning type.

### Define the MCP Payload Custom Lightning Type

The `lightning:type` value of the MCP result wrapper custom Lightning type’s `outputValues` property references the MCP payload custom Lightning type. The MCP payload custom Lightning type defines the structure of the action-specific payload. Its properties can use Apex class type references to describe values returned by the Apex invocable action.

This example defines a `hotelInfo` property whose `lightning:type` value references the `Hotel` inner class in the `HotelSearchResult` Apex class.

```json
{
  "title": "Hotel Info Output Values",
  "description": "Payload fields from the HotelSearchResult response",
  "type": "object",
  "lightning:type": "lightning__objectType",
  "lightning:tags": ["mcp"],
  "unevaluatedProperties": false,
  "properties": {
    "hotelInfo": {
      "title": "Hotel Info",
      "lightning:type": "@apexClassType/c__HotelSearchResult$Hotel"
    }
  }
}
```

For an MCP payload custom Lightning type:

- Set type to `object`.
- Set `lightning:type` to `lightning__objectType`.
- Include `mcp` in `lightning:tags`.
- Set `unevaluatedProperties` to `false`.
- Define the properties in the payload.

In this example, the `lightning:type` value of `hotelInfo` references the `Hotel` inner class in the `HotelSearchResult` Apex class.

### Define the MCP Result Wrapper Custom Lightning Type

The MCP result wrapper custom Lightning type represents the complete result returned by the MCP server tool.

Define these properties:

- `actionName`: The name of the invoked action.
- `isSuccess`: Indicates whether the action completed successfully.
- `outputValues`: The action-specific payload. Its `lightning:type` value references the MCP payload custom Lightning type.

```json
{
  "title": "Hotel Info Result",
  "description": "Invocable-action result envelope for the HotelSearchResult MCP tool",
  "type": "object",
  "lightning:type": "lightning__objectType",
  "lightning:tags": ["mcp"],
  "unevaluatedProperties": false,
  "properties": {
    "actionName": { "title": "Action Name", "lightning:type": "lightning__textType" },
    "isSuccess": { "title": "Is Success", "lightning:type": "lightning__booleanType" },
    "outputValues": { "title": "Output Values", "lightning:type": "c__hotelInfoOutputValues" }
  }
}
```

In this example, the `lightning:type` value of `outputValues` references `hotelInfoOutputValues`, the MCP payload custom Lightning type.

### Add the Renderer

Add `renderer.json` to the root of the MCP result wrapper custom Lightning type bundle, parallel to its `schema.json` file.

Map nested properties under `outputValues` to the flat attributes defined in the widget’s `schema.json` file.

This example maps hotel information under `outputValues.hotelInfo` to attributes defined in the `hotelCard` widget’s schema.

```json
{
  "renderer": {
    "componentOverrides": {
      "$": {
        "definition": "@widget/c/hotelCard",
        "attributes": {
          "hotelId": "{!$attrs.outputValues.hotelInfo.hotelId}",
          "name": "{!$attrs.outputValues.hotelInfo.name}",
          "city": "{!$attrs.outputValues.hotelInfo.city}",
          "checkInTime": "{!$attrs.outputValues.hotelInfo.checkInTime}",
          "checkOutTime": "{!$attrs.outputValues.hotelInfo.checkOutTime}",
          "pricePerNight": "{!$attrs.outputValues.hotelInfo.pricePerNight}",
          "rating": "{!$attrs.outputValues.hotelInfo.rating}"
        }
      }
    }
  }
}
```

In this example:

- The keys (`hotelId`, `name`, `city`, `checkInTime`, `checkOutTime`, `pricePerNight`, and `rating`) are attributes defined in the `hotelCard` widget’s `schema.json` file.
- `outputValues` is a property in the MCP result wrapper custom Lightning type.
- `hotelInfo` is a property in the MCP payload custom Lightning type.
- The final segment of each expression references a property in the `HotelSearchResult.Hotel` Apex class.

Don’t add `renderer.json` to the MCP payload custom Lightning type. The renderer applies to the complete MCP server tool result represented by the MCP result wrapper custom Lightning type.

### Understand the File Structure

This example uses an MCP server tool for hotel information and a widget named `hotelCard`.

```
myProject/
  force-app/
    main/
      default/
        uiWidgets/
          hotelCard/
            hotelCard.json
            hotelCard.uiwidget-meta.xml
            schema.json
        lightningTypes/
          hotelInfoResult/
            schema.json
            renderer.json
          hotelInfoOutputValues/
            schema.json
```

In this structure:

- `hotelInfoOutputValues` is the bundle for the MCP payload custom Lightning type.
- `hotelInfoResult` is the bundle for the MCP result wrapper custom Lightning type.
- The `hotelInfoResult` bundle contains `renderer.json`.
- `hotelCard` is the widget bundle.

**See Also**

- [Use HXL Widgets on MCP Channels](/docs/platform/hxl/guide/hxl-mcp-channels.md)
- [Example: Mapping a Hotel Card Widget for MCP](/docs/platform/hxl/guide/hxl-widget-example-mapping-mcp.md)

## Understand Namespace Prefixes for Widget References

When you reference a widget from a Lightning type, use the correct namespace prefix.

**For widgets created in your org**

Use the `c` namespace prefix. This rule applies even if your org has its own namespace. For example, if your org's namespace is `myOrgNamespace` and you create a widget named `hotelCard`, refer to it as `c/hotelCard`.

This `renderer.json` file uses the `c` namespace to reference a widget.

```json
{
  "renderer": {
    "componentOverrides": {
      "$": {
        "definition": "@widget/c/hotelCard"
      }
    }
  }
}
```

**See Also**

- [Get Started with Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types.md)
- [Core Concepts of Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-core.md)
