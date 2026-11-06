# Core Concepts of Custom Lightning Types

You build all custom Lightning types, whether Apex-based or object-based, by using a common set of foundational components. Understand these core concepts to create, customize, and deploy your types.

## Building Blocks of a Lightning Type

Lightning Type consists of these artifacts.

- **Schema** defines the data structure and the rules for its validation, such as maximum length, type, and format.
- **Editor** defines the input UI component that you use to enter or edit data.
- **Renderer** defines the output UI component that displays data.

## LightningTypeBundle Metadata Type

The LightningTypeBundle metadata type describes the custom Lightning types. It’s available in API version 64.0 and later.

To get a list of the custom and standard Lightning types deployed in your org, make a call to the [`/connect/lightning-types`](https://developer.salesforce.com/docs/atlas.en-us.chatterapi.meta/chatterapi/connect_resources_lightning_types.htm) resource.

For more information about the resources available in the Type System Connect REST API, see the [Type System Resources](https://developer.salesforce.com/docs/atlas.en-us.chatterapi.meta/chatterapi/connect_resources_type_system_resources.htm).

## Understand the LightningTypeBundle Structure

LightningTypeBundle components are stored in the lightningTypes folder.

Here’s an example of the LightningTypeBundle structure.

```
+--myMetadataPackage
    +--lightningTypes (1)
        +--TYPE_NAME (2)
           +--schema.json (3)
           +--CHANNEL_NAME (4)
              +--editor.json (5) OR +--renderer.json (6)
```

The bundle includes these resources.

- The `lightningTypes` folder (1) contains a folder for each custom Lightning type created in the format `{typeName}` (2).
- Each custom Lightning type folder contains a [`schema.json`](#lightning-types-configuration-files) file (3) that defines the JSON schema that drives the custom Lightning type validation.
- Optional channel-specific folders (4). To override the default UI for a specific Salesforce application, the bundle contains a folder named after that channel. The supported channel folders are:

  - `lightningDesktopGenAi` (Agentforce Employee agent in Lightning Experience)
  - `enhancedWebChat` (Agentforce Service agent via Enhanced Chat v2)
  - `lightningMobileGenAi` (Agentforce Employee agent on Mobile and Agentforce Service agent via Enhanced Chat v2 on Mobile)
  - `experienceBuilder` (Experience Builder)

  Inside the `{channelName}` folder, you can configure:

  - The [`editor.json`](#lightning-types-configuration-files) file (5) containing custom user interface and editor information
  - The [`renderer.json`](#lightning-types-configuration-files) file (6) containing custom user interface and renderer information

    :::note
    This file isn’t supported in `experienceBuilder`.
    :::

### Lightning Type Structure for HXL Widgets (Beta)

When you reference a widget in a custom Lightning type, create a `renderer.json` file at the root level (parallel to `schema.json`) without channel-specific folders. Don't add an `editor.json` file or a channel subfolder.

```
+--myMetadataPackage
    +--lightningTypes
        +--TYPE_NAME
           +--schema.json
           +--renderer.json
```

For details about widgets, see [Build Rich UI Experiences with HXL Widgets](https://developer.salesforce.com/docs/platform/hxl/guide/hxl-rich-ui.md).

### Use SF Commands or Metadata API to Deploy LightningTypeBundles

To deploy a LightningTypeBundle to your Salesforce org, use Metadata API or SF Commands. The Metadata API uses a manifest file that defines the metadata that you want to deploy.

Here’s an example `package.xml` manifest file for a LightningTypeBundle that includes the custom Lightning type `myFlight`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>myFlight</members>
        <name>LightningTypeBundle</name>
    </types>
    <version>64.0</version>
</Package>
```

To delete a custom Lightning type, you must deploy a destructiveChanges package to your org that lists the types to delete.

**See Also**

- *Metadata API Developer Guide*: [Deploying and Retrieving Metadata with the Zip File](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/file_based_zip_file.htm)
- *Metadata API Developer Guide*: [Deleting Components from an Organization](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy_deleting_files.htm)

### SF Commands and Packaging Support

Use the Salesforce CLI `project` commands to deploy, retrieve, and track the source files for the LightningTypeBundle metadata type in your Salesforce DX project. See [project Commands](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_project_commands_unified.htm#cli_reference_project_commands_unified) in the Salesforce CLI Command Reference.

Packaging supports the LightningTypeBundle metadata type that describes custom Lightning types. You can include the LightningTypeBundle in first-generation (1GP) and second-generation (2GP) packages. See the [First-Generation Managed Packaging Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.pkg1\_dev.meta/pkg1\_dev/first_gen_packageable_components.htm#mdc_lightning_types) and the [Second-Generation Managed Packaging Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.pkg2\_dev.meta/pkg2\_dev/packaging_packageable_components.htm#mdc_lightning_types).

**See Also**

- [Metadata Coverage Report](https://developer.salesforce.com/docs/metadata-coverage/64)
- [Salesforce CLI Command Reference](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_top.htm)
- [Use Managed Packages to Develop Your AppExchange Solution](https://developer.salesforce.com/docs/atlas.en-us.packagingGuide.meta/packagingGuide/managed_packaging_intro.htm)

## Lightning Types Configuration Files

The LightningTypeBundle includes these configuration files.

**Schema.json**

The `schema.json` file is a required resource in every Lightning Type Bundle. It defines the data structure, validation rules (such as type, format, and maximum length), and constraints for your custom Lightning type by using the JSON Schema specification.

**Editor.json**

With the optional `editor.json` file, you can override the default input UI. Use this file to define the specific custom LWC component for entering or editing data.

The `editor.json` file supports this type of override.

- **Editor Override**. Defines the custom editor for the custom Lightning type. Use the `$` keyword to specify an LWC component that captures or edits data for the entire type. Alternatively, use property names to specify LWC components that capture or edit data for individual properties while default editors handle the rest.

**Renderer.json**

With the optional `renderer.json` file, you can override the default output UI. Use this file to define the custom LWC component used to present or display data to the user.

The `renderer.json` file supports two types of overrides.

- **Renderer Override**. Defines a single renderer for the entire custom Lightning type. You use the `$` keyword to specify the LWC component that renders the data for a single instance of the type.
- **Collection Renderer Override**. Defines a renderer for a structured list or array of data. This approach uses the `collection` keyword to associate a custom LWC component that renders the entire list of data at once.

**See Also**

- [Component Override](/docs/platform/lightning-types/guide/lightning-types-ui-config.md#component-override)

## Understand Namespace Prefixes for Metadata References

When you reference metadata such as a custom label or a component in your custom Lightning type, use the correct namespace prefix. This prefix applies to metadata references in your schema, editor, and renderer files.

**For metadata created in your org**

Use the “c” namespace prefix. This rule applies even if your org has its own namespace. For example, if your org’s namespace is `myOrgNamespace` and you create an LWC component named `flightDetails`, refer to it as `c/flightDetails`.

:::note
This rule also applies to custom Lightning types in managed packages. Reference any new metadata in the same package by using the “c” prefix.
:::

**For metadata installed via a managed package**

Use the package’s unique namespace as the prefix. For example, if a package has the namespace `isv` and includes an LWC component named `flightDetails`, refer to it as `isv/flightDetails`.

**Example of Local Org Metadata References**

This `schema.json` file uses the “c” namespace to reference a custom label and the `@apexClassType` reference of an Apex class.

```json
{
  "title": "{!$Label.c.FlightTitle}",
  "description": "My Flight Response",
  "lightning:type": "@apexClassType/c__AvailableFlight"
}
```

This `renderer.json` file uses the “c” namespace to reference a Lightning Web Component.

```json
{
  "renderer": {
    "componentOverrides": {
      "$": {
        "definition": "c/flightDetails"
      }
    }
  }
}
```

## Create Custom Labels for Custom Lightning Types

You can customize labels for the title and description values in the `schema.json` file for a custom Lightning type.

To create and use a translated custom label in a custom Lightning type, complete these steps.

1. From Setup, enter `Labels` in the Quick Find box, and then select **Custom Labels**.
2. Create a custom label.
3. In the `schema.json` file for the custom Lightning type that you created, use the expression `{!$Label.c.MyLabel1}` for the title and description values. Here, “c” is the namespace prefix and “MyLabel1” is the API name of the custom label.

**See Also**

- [Create and Edit Custom Labels](https://help.salesforce.com/s/articleView?id=platform.cl_edit.htm\&type=5)
- [Translate Custom Labels](https://help.salesforce.com/s/articleView?id=platform.cl_translate_edit.htm\&type=5)

## Salesforce Applications That You Can Override

You can override the default UI of some Salesforce applications by using a custom Lightning type. Each Salesforce application listens to a specific channel that you specify in your [LightningTypeBundle](#understand-the-lightningtypebundle-structure).

You can override these Salesforce applications.

- Agentforce Employee agent in Lightning Experience
- Agentforce Service agent via Enhanced Chat v2
- Agentforce Employee agent on Mobile (iOS and Android)
- Agentforce Service agent via Enhanced Chat v2 on Mobile (iOS and Android)
- Experience Builder
- Prompt Builder
- Flows via Structured Outputs

To override the UI, create a folder in your LightningTypeBundle with the application’s corresponding channel name.

| Salesforce Application                                                                                                                   | Channel Folder          | Category |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- | -------- |
| Agentforce Employee agent in Lightning Experience                                                                                        | `lightningDesktopGenAi` | Apex     |
| Agentforce Service agent via Enhanced Chat v2                                                                                            | `enhancedWebChat`       | Apex     |
| Agentforce Employee agent on Mobile (iOS and Android)<br><br />Agentforce Service agent via Enhanced Chat v2 on Mobile (iOS and Android) | `lightningMobileGenAi`  | Apex     |
| Experience Builder                                                                                                                       | `experienceBuilder`     | Object   |
| Prompt Builder                                                                                                                           | Not Applicable          | Object   |
| Flows via Structured Outputs                                                                                                             | Not Applicable          | Object   |

**See Also**

- [Channels](/docs/platform/lightning-types/guide/lightning-types-ui-config.md#channels)
- [*Agentforce Developer Guide*: Custom Lightning Type Examples](https://developer.salesforce.com/docs/ai/agentforce/guide/lightning-types-examples.md)
- [*Lightning Web Components Developer Guide*: Overview: Creating Custom Property Types and Editors](https://developer.salesforce.com/docs/platform/lwc/guide/use-experience-cloud-overview-custom-property-types.md)
- [*Salesforce Help*: Build and Manage Lightning Types for Prompt Templates](https://help.salesforce.com/s/articleView?id=ai.prompt_builder_build_manage_lt.htm\&type=5)
- [*Salesforce Help*: Flow Core Action: AI Agent Actions](https://help.salesforce.com/s/articleView?id=platform.automate_flow_ref_elements_actions_generate_ai_agent_response.htm\&type=5)
- [*Salesforce Help*: Custom Lightning Types in the Salesforce Mobile App](https://help.salesforce.com/s/articleView?id=sf.salesforce_app_clt_mobile.htm\&type=5)
