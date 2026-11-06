# Define a Top-Level Editor Override

You can define a single editor for your entire custom Lightning type in the `editor.json` file. This editor applies whenever an instance of the type is used as an input parameter.

For example, you have a custom Lightning type named `taskFilter` that corresponds to the Apex class `TaskCriteria` with two properties: `priorityLevel` and `dueDate`. You want to use a custom dropdown to select the priority level and a calendar picker for the due date.

Here’s an example of what the `editor.json` file can look like for the custom Lightning type `taskFilter`.

```
+--lightningTypes
        +--taskFilter
            +--schema.json
            +--lightningDesktopGenAi
               +--editor.json
```

:::note
This example uses `lightningDesktopGenAi` to configure the custom Lightning type. To configure the type for a different channel, create the `editor.json` file inside the folder that corresponds to that channel.
:::

**Example: Basic Configuration Using the value Property**

This example shows you how to configure a component to handle the entire object via a single `@api` value property. The component receives the full object in one property.

:::note
To view a complete, working example of an LWC editor implementation, see [Customize UI for Input](https://developer.salesforce.com/docs/ai/agentforce/guide/lightning-types-example-full-editor-renderer.md#customize-ui-for-input).
:::

1. [**Create the LWC**](https://developer.salesforce.com/docs/platform/lwc/guide/create-components-introduction.md).<br /><br />This sample code shows the LWC component `myTaskComponent`.

   ```js
   import { LightningElement, api } from "lwc";
   export default class MyTaskComponent extends LightningElement {
     // This property doesn’t accept inbound context or default values from the agent. Use it strictly to capture user input. The framework sends this data to the agent action only when the user submits the response in the chat interface.
     @api value;

     // Example: { priorityLevel: 'High', dueDate: '2026-05-15' }

     // Add your custom UI event handlers here.
   }
   ```

   :::note
   The `@api` value property in custom Lightning type editors doesn’t support data injection, so the agent can’t pre-populate it with conversational context or default values. Use it only to capture user input. The framework returns this data to the agent action only after the user submits a response in the chat interface.
   :::

2. **Update the js-meta.xml file.**<br /><br />Include the [`lightning__AgentforceInput`](https://developer.salesforce.com/docs/platform/lwc/guide/targets-lightning-agentforce-input.md) target.<br /><br />This sample code shows the contents of the `myTaskComponent.js-meta.xml` file.

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
       <apiVersion>64.0</apiVersion>
       <isExposed>true</isExposed>
       <masterLabel>My Task Component</masterLabel>
       <targets>
         <target>lightning__AgentforceInput</target>
       </targets>
   </LightningComponentBundle>
   ```

3. **Configure the editor.json file.**<br /><br />Use the `$` keyword to map the type to the component.<br /><br />Here’s how to reference `myTaskComponent` to override the editor for the `taskFilter` custom Lightning type in the `editor.json` file.

   ```json
   {
     "editor": {
       "componentOverrides": {
         "$": {
           "definition": "c/myTaskComponent"
         }
       }
     }
   }
   ```

**Example: Attribute Mapping**

If you’re reusing an existing component and the property names don't match your schema (for example, the component uses `urgency` instead of `priorityLevel`), you must map the properties.

1. **Create the LWC.**<br /><br />This sample code shows `myExistingTaskComponent`.

   ```js
   import { LightningElement, api } from "lwc";
   export default class MyExistingTaskComponent extends LightningElement {
     // The framework passes the mapped data into these properties.

     // Expected value example: 'High'
     @api urgency;

     // Expected value example: '2026-05-15'
     @api dueDate;

     // Add your custom UI event handlers here.
   }
   ```

2. **Update the js-meta.xml file.**<br /><br />Expose the properties in `targetConfigs` to register them as valid input properties for the `lightning__AgentforceInput` target.<br /><br />This sample code shows the contents of the `myExistingTaskComponent.js-meta.xml` file.

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
       <apiVersion>64.0</apiVersion>
       <isExposed>true</isExposed>
       <masterLabel>My Existing Task Component</masterLabel>
       <targets>
         <target>lightning__AgentforceInput</target>
       </targets>
       <targetConfigs>
         <targetConfig targets="lightning__AgentforceInput">
           <property name="urgency" type="lightning__textType" />
           <property name="dueDate" type="lightning__textType" />
         </targetConfig>
       </targetConfigs>
   </LightningComponentBundle>
   ```

3. **Configure the editor.json file with attribute mapping.**<br /><br />Use the attributes object to link schema properties to component properties.<br /><br />This sample code shows how to reference `myExistingTaskComponent` to override the editor for the `taskFilter` custom Lightning type in the `editor.json` file.

   ```json
   {
     "editor": {
       "componentOverrides": {
         "$": {
           "definition": "c/myExistingTaskComponent",
           "attributes": {
             "urgency": "{!$attrs.priorityLevel}",
             "dueDate": "{!$attrs.dueDate}"
           }
         }
       }
     }
   }
   ```

:::note
You must map the component’s properties to the corresponding properties in the Apex class, even if they have the same name. However, if the component receives the entire Apex class object through a single value attribute, you don’t need to map the individual attributes.
:::

The expression `"urgency": "{!$attrs.priorityLevel}"` links the `priorityLevel` property of the `TaskCriteria` Apex class to the `urgency` property of the LWC component `myExistingTaskComponent` (and vice versa).

Here’s what each element represents.

- `urgency`: Property in the LWC component `myExistingTaskComponent`
- `{!$attrs}`: Pointer to the `TaskCriteria` class
- `priorityLevel`: Property in the `TaskCriteria` class
- `{!$attrs.priorityLevel}`: Evaluates to the specific value of the `priorityLevel` property so it can be dynamically passed to the component

**See Also**

- [*Agentforce Developer Guide*: Custom Lightning Type Examples](https://developer.salesforce.com/docs/ai/agentforce/guide/lightning-types-examples.md)
- [*Salesforce Help*: Custom Lightning Types in the Salesforce Mobile App](https://help.salesforce.com/s/articleView?id=sf.salesforce_app_clt_mobile.htm\&type=5)
