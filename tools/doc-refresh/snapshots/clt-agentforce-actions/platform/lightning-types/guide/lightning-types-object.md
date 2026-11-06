# Object-Based Custom Lightning Types

With object-based custom Lightning types, you can define a custom data structure entirely within a JSON schema, without relying on an Apex class. You explicitly define every property, data type, and validation rule in the `schema.json` file. Use this approach when you need a lightweight, flexible data model for UI configuration or prompt definitions that don’t require an Apex backend.

**Supported in**:

- Prompt Builder
- Experience Builder

## Schema.json for Object-Based Custom Lightning Types

For object-based types, you define the data structure directly in the `schema.json` file by using the `lightning__objectType` value and a `properties` block.

This table lists the keywords that you can specify in a `schema.json` file.

| Keyword          | Required or Optional | Type   | Description                                                                                                                                                                                                                                                                                          |
| ---------------- | -------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `title`          | Required             | String | Name for the Lightning type                                                                                                                                                                                                                                                                          |
| `description`    | Optional             | String | Description for the Lightning type                                                                                                                                                                                                                                                                   |
| `lightning:type` | Required             | String | Refers to lightning__objectType type by fully qualified name                                                                                                                                                                                                                                         |
| `properties`     | Required             | Object | Defines the fields for the object. Each key is a field name, and its value is an object defining that field’s `title` and `lightning:type`.<br></br>For a list of valid values, see [Lightning Types Reference](/docs/platform/lightning-types/guide/lightning-types-references.md#lightning-types). |
| `required`       | Optional             | Array  | An array of property names that must be present in the data                                                                                                                                                                                                                                          |

Here’s a sample code that shows the contents of the `schema.json` file for a custom Lightning type `customerFeedback`.

```json
{
  "title": "customerFeedback",
  "description": "Structured format for capturing customer feedback received.",
  "lightning:type": "lightning__objectType",
  "properties": {
    "customerName": {
      "title": "customerName",
      "lightning:type": "lightning__textType"
    },
    "feedbackDate": {
      "title": "feedbackDate",
      "lightning:type": "lightning__dateType"
    },
    "satisfactionScore": {
      "title": "satisfactionScore",
      "lightning:type": "lightning__numberType"
    }
  },
  "required": ["customerName"]
}
```

:::note
When you create or update an object-based custom Lightning type, an Apex class is automatically generated that matches your schema.
:::

**See Also**

- [Create Custom Labels for Custom Lightning Types](/docs/platform/lightning-types/guide/lightning-types-core.md#create-custom-labels-for-custom-lightning-types)

## UI Configuration for Object-Based Custom Lightning Types

While `schema.json` defines the data structure, the UI configuration files in the LightningTypeBundle control the visual representation. Organize these files by channel to support specific Salesforce applications.

[**Channels**](/docs/platform/lightning-types/guide/lightning-types-ui-config.md#channels)

Store UI overrides in channel-specific subfolders to target different applications.

- **experienceBuilder**. Use this folder for Experience Builder sites.

[**Configuration Files**](/docs/platform/lightning-types/guide/lightning-types-ui-config.md#ui-configuration-files)

Configure the UI override by using this JSON file.

- **editor.json**. Points to a Lightning Web Component (LWC) that serves as a custom form for data entry.

[**Component Override**](/docs/platform/lightning-types/guide/lightning-types-ui-config.md#component-override)

You can customize the visual presentation by adding component overrides to your `editor.json` file.

- **Top-Level Override**. A top-level override replaces the default UI for the entire custom Lightning type. To configure this override, use the `$` symbol as the key in the `componentOverrides` section of your `editor.json`. This approach is useful for creating specialized interfaces, such as a custom card or a multi-property form handled by a single component.
- **Property-Level Override**. A property-level override replaces the default UI for specific properties of a schema within a complex type, while default editors handle the rest of the type. Instead of using `$`, specify the exact property name (such as address or phoneNumber) as the key in the `componentOverrides` section. Use property overrides when specific data requires specialized input. Default editors apply to any properties that don’t have a defined override.

[**Layout Configuration**](/docs/platform/lightning-types/guide/lightning-types-ui-config.md#layout-configuration)

Defines the visual arrangement and hierarchy of schema properties. By default, the UI renders properties in a vertical stack matching the schema order. Use the `layout` section in `editor.json` to create complex arrangements, such as grouping properties horizontally or organizing them into tabs.

[**Attribute Mapping**](/docs/platform/lightning-types/guide/lightning-types-ui-config.md#lightning-web-component-attribute-mapping)

In both configuration files, map schema properties to LWC component properties by using the `{!$attrs.PropertyName}` syntax.

:::note
For a complete list of supported channels and detailed JSON syntax, see [Lightning Type UI Configuration](/docs/platform/lightning-types/guide/lightning-types-ui-config.md).
:::

**LWC Target Requirements**

To use a component as an override, include the appropriate target in the component’s `js-meta.xml` file.

- [`lightning__PropertyEditor`](https://developer.salesforce.com/docs/platform/lwc/guide/targets-lightning-property-editor.md) for overrides

**See Also**

- [Lightning Types Configuration Files](/docs/platform/lightning-types/guide/lightning-types-core.md#lightning-types-configuration-files)
- [Lightning Type UI Configuration](/docs/platform/lightning-types/guide/lightning-types-ui-config.md)

## Object-Based Custom Lightning Types Modification Guidelines

You can modify custom Lightning types freely until they’re referenced in a Salesforce application. When they’re referenced, follow these guidelines to maintain the integrity of the type across Salesforce applications, such as Experience Builder and Prompt Builder.

| Keyword                       | Status                  | Guideline                                                                                                                                                                            |
| ----------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `title`                       | Permitted               | You can change the title of an individual property.                                                                                                                                  |
| `description`                 | Permitted               | You can change the description of an individual property.                                                                                                                            |
| `lightning:type`              | Prohibited              | You can’t change the `lightning:type` value.                                                                                                                                         |
| `properties`                  | Conditionally Permitted | **Additive changes**: You can add new optional properties.<br></br>**Destructive changes**: You can’t remove or rename an existing property. You can’t add a new required property.  |
| `required`                    | Conditionally Permitted | You can make existing required properties optional (remove them from the required list).<br></br>You can’t add properties to the required list.                                      |
| `maximum`                     | Conditionally Permitted | You can increase the value. You can’t decrease it.                                                                                                                                   |
| `minimum`                     | Conditionally Permitted | You can decrease the value. You can’t increase it.                                                                                                                                   |
| `maxLength`                   | Conditionally Permitted | You can increase the value. You can’t decrease it.                                                                                                                                   |
| `minLength`                   | Conditionally Permitted | You can decrease the value. You can’t increase it.                                                                                                                                   |
| `multipleOf`                  | Conditionally Permitted | The existing value must be divisible by the new value.<br></br>**Example**: If the existing value is 20, valid new values include 2, 4, 5, and 10. Invalid values include 15 and 40. |
| `lightning:allowedUrlSchemes` | Conditionally Permitted | You can add new schemes to the array. You can’t remove existing schemes.                                                                                                             |
