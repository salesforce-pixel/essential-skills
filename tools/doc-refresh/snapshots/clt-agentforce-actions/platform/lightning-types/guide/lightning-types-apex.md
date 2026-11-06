# Apex-Based Custom Lightning Types

With Apex-based custom Lightning types, you can define the structure of a custom Lightning type by referencing an Apex class code. Instead of manually defining every field and property in a JSON schema, the custom Lightning type inherits its structure directly from the Apex class member variables, specifically the variables annotated with `@AuraEnabled`. Use this approach when your agent action returns complex data that you have already modeled in your Apex logic. This method maintains a single source of truth for the data structure.

**Supported in**:

- Agentforce Employee agent in Lightning Experience
- Agentforce Service agent via Enhanced Chat v2
- Agentforce Employee agent on Mobile (iOS and Android)
- Agentforce Service agent via Enhanced Chat v2 on Mobile (iOS and Android)

:::note
Apex-based types aren’t supported in Experience Builder sites.
:::

## Schema.json for Apex-Based Custom Lightning Types

For Apex-based types, the schema references an Apex class. You don’t define properties here. Instead, you point to the class that contains the data structure.

This table lists the keywords that you can specify in a `schema.json` file.

| Keyword          | Required or Optional | Type   | Description                                                                                                                                                                                                                                                                                                                                           |
| ---------------- | -------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `title`          | Required             | String | Name for the Lightning type                                                                                                                                                                                                                                                                                                                           |
| `description`    | Optional             | String | Description for the Lightning type                                                                                                                                                                                                                                                                                                                    |
| `lightning:type` | Required             | String | Refers to `@apexClassType` types by using fully qualified names<br></br>This keyword is syntactic sugar for the `$ref` keyword in JSON Schema, which links together schemas.<br></br>For information about `$ref`, see [Understanding JSON Schema: The Sref keyword](https://json-schema.org/understanding-json-schema/structuring?highlight=ref#ref) |

Unless noted otherwise, the keywords follow the JSON Schema specification.

Here’s a sample code that shows the contents of the `schema.json` file for a custom Lightning type `flightResponse`.

```json
{
  "title": "My Flight Response",
  "description": "My Flight Response",
  "lightning:type": "@apexClassType/c__AvailableFlight"
}
```

**See Also**

- [Create Custom Labels for Custom Lightning Types](/docs/platform/lightning-types/guide/lightning-types-core.md#create-custom-labels-for-custom-lightning-types)

### Apex Class Requirements

To ensure successful invocation and rendering within Agentforce—especially in namespaced orgs or managed packages—configure your Apex classes according to these requirements.

**Class Definition and Visibility**

- **Top-level definition**. Define every class as a top-level class in its own file. Don’t use nested (inner) classes.
- **Global visibility**. Mark all classes as `global`. Using `public` or `private` modifiers can cause failures in namespaced orgs or managed packages.

**Annotations**

- **@AuraEnabled**. Apply this annotation to every field required in the response, including fields inside objects used as `@InvocableVariable`.
- **@JsonAccess**. Annotate every class with `@JsonAccess(serializable='always' deserializable='always')`. This annotation ensures that the internal invocation layer can process the data.

**Namespace Prefixes**

- **Local org classes**. Use the “c” prefix for classes in your local org.
- **Managed packages**. Use the specific registered namespace for the package. <br></br>See [Understand Namespace Prefixes for Metadata References](/docs/platform/lightning-types/guide/lightning-types-core.md#understand-namespace-prefixes-for-metadata-references)

**Supported Types**

Not all data types that you use in an Apex class are supported in Lightning types.

Lightning types support these data types.

- Primitives, including Integer, Double, Long, Date, Datetime, Time, String, ID, and Boolean
- sObjects, either a generic or specific sObject, such as Account, Contact, and MyCustomObject\_\_c
- Collections
  - A list or array of primitives, sObjects, user-defined Apex classes, and collections
  - A map, represented as `Map<key, value>`, where the key is always a string and the value can be a primitive, sObject, or collection
- User-defined Apex classes

:::important
If you created an agent action before meeting these requirements, delete and recreate the agent action after updating the Apex classes. This step correctly registers the changes.
:::

### Schema Projection

Schema projection is the automated process that evaluates an Apex class to generate a runtime JSON schema.

**How It Works**

- **API Evaluation**. The internal [LightningTypeBundle](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_lightningtypebundle.htm) API introspects the referenced Apex class. The projection process scans for the `@AuraEnabled` annotation on member variables to determine which properties to expose.
- **Dynamic Translation**. The projection layer automatically translates Apex primitives (such as String and Integer) and complex types (such as nested classes or sObjects) into the corresponding Lightning type schema. This automation eliminates manual variable mapping.
- **Single Source of Truth**. Because the schema projects directly from the code, changes to the Apex class automatically update the Lightning type’s structure. This automation eliminates manual updates to the `schema.json` file.

## UI Configuration for Apex-Based Custom Lightning Types

While `schema.json` defines the data structure, the UI configuration files in the Lightning Type Bundle control the visual representation. Organize these files by channel to support specific Salesforce applications.

[**Channels**](/docs/platform/lightning-types/guide/lightning-types-ui-config.md#channels)

Store UI overrides in channel-specific subfolders to target different Salesforce applications.

- **lightningDesktopGenAi**. Use this folder for Agentforce Employee agents in Lightning Experience.
- **enhancedWebChat**. Use this folder for Agentforce Service agents via Enhanced Chat v2.
- **lightningMobileGenAi**. Use this folder for Agentforce Employee agents on Mobile (iOS and Android) and Agentforce Service agents via Enhanced Chat v2 on Mobile (iOS and Android).

[**Configuration Files**](/docs/platform/lightning-types/guide/lightning-types-ui-config.md#ui-configuration-files)

Configure input and output UI overrides by using these JSON files.

- **editor.json**. Configures the UI when the custom Lightning type is an input parameter. It points to a Lightning Web Component (LWC) that serves as a custom form for data entry.
- **renderer.json**. Configures the UI when the custom Lightning type is an output parameter. It points to an LWC that renders the returned data (for example, as a custom card or list).

[**Component Override**](/docs/platform/lightning-types/guide/lightning-types-ui-config.md#component-override)

You can customize the visual presentation by adding component overrides to your `editor.json` and `renderer.json` files.

- **Top-Level Override**. A top-level override replaces the default UI for the entire custom Lightning type. To configure this override, use the `$` symbol as the key in the `componentOverrides` section of your `editor.json` or `renderer.json`. This approach is useful for creating specialized interfaces, such as a custom card or a multi-property form handled by a single component.

[**Attribute Mapping**](/docs/platform/lightning-types/guide/lightning-types-ui-config.md#lightning-web-component-attribute-mapping)

In both configuration files, map schema properties to LWC component properties by using the `{!$attrs.PropertyName}` syntax.

:::note
For a complete list of supported channels and detailed JSON syntax, see [Lightning Type UI Configuration](/docs/platform/lightning-types/guide/lightning-types-ui-config.md).
:::

**LWC Target Requirements**

To use a component as an override, include the appropriate target in the component’s `js-meta.xml` file.

- [`lightning__AgentforceInput`](https://developer.salesforce.com/docs/platform/lwc/guide/targets-lightning-agentforce-input.md) for input overrides
- [`lightning__AgentforceOutput`](https://developer.salesforce.com/docs/platform/lwc/guide/targets-lightning-agentforce-output.md) for output overrides

**See Also**

- [Lightning Types Configuration Files](/docs/platform/lightning-types/guide/lightning-types-core.md#lightning-types-configuration-files)
- [Lightning Type UI Configuration](/docs/platform/lightning-types/guide/lightning-types-ui-config.md)

## Apex Class Modification Guidelines

To maintain the integrity of active agent actions and prevent runtime failures, adhere to these restrictions when you modify Apex classes referenced by a custom Lightning type.

| Change Type                | Status     | Impact                                                                                                                 |
| -------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------- |
| Additive Changes           | Permitted  | Adding new `@AuraEnabled` fields to an existing class is safe. Schema projection picks up these changes automatically. |
| Class Renaming or Deletion | Prohibited | Renaming or deleting an Apex class that a `lightning:type` schema references causes runtime failures.                  |
| Data Type Changes          | Breaking   | Changing a variable’s type, for example, from `Integer` to `String`, breaks the integration.                           |
| Field Removal              | Breaking   | Removing an `@AuraEnabled` field that an agent action uses causes invocation errors.                                   |
| Visibility Downgrade       | Prohibited | Changing a class from `global` to `public` in a managed package breaks external references.                            |
