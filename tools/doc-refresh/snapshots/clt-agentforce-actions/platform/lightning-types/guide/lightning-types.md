# Get Started with Lightning Types

Lightning Types are JSON-based data types to structure, validate, and display data.

With Lightning Types, you can manage the representation and shape of data types. You can use Lightning types to create consistent and flexible data interactions.

Salesforce provides standard Lightning types, such as [text](/docs/platform/lightning-types/guide/lightning-types-references.md#lightning\_\_texttype) and [multiline](/docs/platform/lightning-types/guide/lightning-types-references.md#lightning\_\_multilinetexttype) text, to structure your data type. Additionally, you can create custom Lightning types to customize the UI experience based on your business requirements.

## Standard Lightning Types

Salesforce provides some Lightning types out of the box that act as the basic types that you can reference to structure a more complex schema.

To understand how a Lightning type is validated, you must identify the underlying type used for each Lightning type.

Each standard Lightning type includes a default editor and renderer, so there’s no need for you to create those components.

Similar to JSON Schema types, each Lightning type has its own type-specific keywords that apply only to that type.

You can use these standard Lightning types. However, support for specific types varies by application.

- `lightning__booleanType`
- `lightning__dateType`
- `lightning__dateTimeType`
- `lightning__dateTimeStringType`
- `lightning__integerType`
- `lightning__multilineTextType`
- `lightning__numberType`
- `lightning__objectType`
- `lightning__richTextType`
- `lightning__textType`
- `lightning__timeType`
- `lightning__urlType`

For information about the keywords available and the default editor and renderer associated with each of the Lightning types, see [Lightning Types Reference](/docs/platform/lightning-types/guide/lightning-types-references.md#lightning-types).

## Custom Lightning Types

Create custom Lightning types to customize the appearance of the UI. With custom Lightning types, you override the default user interface to manage complex interactions within Salesforce.

To create custom lightning types in Salesforce, use the LightningTypeBundle metadata component. For information about how to create custom Lightning types, see [LightningTypeBundle Metadata API](/docs/platform/lightning-types/guide/lightning-types-core.md#lightningtypebundle-metadata-type).

Benefits:

- **Enhanced UI Customization**

  Standard Lightning types have predefined UI components. However, they don’t always fit your design needs or the user experience. Custom Lightning types give you full control over the UI. You can create tailored components that match your specific styling and behavior requirements. This customization ensures that the interface looks and functions exactly as you need for your application.

- **Handling Complex Data Structures**

  Standard Lightning types sometimes can’t handle complex data, but custom Lightning types can manage and render complex data structures. For example, they can handle deeply nested objects, complex arrays, and dynamic fields that change based on user input. With custom Lightning types, you can build UIs that display complex data smoothly. Customize your UI to handle complex data structures, and you ensure that your Salesforce actions can accommodate even the most detailed and dynamic workflows.

## Categories of Custom Lightning Types

Custom Lightning types fall into two categories based on how you define their schema.

- [**Apex-based custom Lightning types**](/docs/platform/lightning-types/guide/lightning-types-apex.md). Use these types when you define the schema by referencing an Apex class. This method is for when you have a complex data structure already defined in an Apex class code. These types can be used for Agentforce Employee agents in Lightning Experience, Agentforce Service agents through [Enhanced Chat v2](https://help.salesforce.com/s/articleView?id=service.enhanced_chat_v2\_intro.htm\&type=5), Agentforce Employee agents on Mobile, and Agentforce Service agents via Enhanced Chat v2 on Mobile.
- [**Object-based custom Lightning types**](/docs/platform/lightning-types/guide/lightning-types-object.md). Use these types when you define a custom schema by specifying its properties directly. This method is for defining a custom JSON object structure without referencing an Apex class. These types can be used in Experience Builder and Prompt Builder.
