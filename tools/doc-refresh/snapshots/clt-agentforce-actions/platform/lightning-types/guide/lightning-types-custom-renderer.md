# Define a Top-Level Renderer Override

You can define a single renderer for your entire custom Lightning type. The renderer applies whenever an instance of the type is returned as output.

For example, you have a custom Lightning type named `taskCard` that corresponds to an Apex class `TaskRecord` with four properties: `cardName`, `cardId`, `createdDate`, and `lastUpdate`. You want to display the data by using a custom task board card that visually highlights recently updated items.

Here’s an example of what the `renderer.json` file can look like for the custom Lightning type `taskCard`.

```
+--lightningTypes
        +--taskCard
            +--schema.json
            +--lightningDesktopGenAi
               +--renderer.json
```

:::important
This example uses `lightningDesktopGenAi` to configure the custom Lightning type. Only specific channels support output overrides (`renderer.json`). Verify that your channel supports this feature before configuring the file.
:::

**Example: Basic Configuration Using the value Property**

This example shows you how to configure a component to handle the entire object via a single `@api` value property. The component receives the full object in one property.

:::note
To view a complete, working example of an LWC renderer implementation, see [Customize UI for Output](https://developer.salesforce.com/docs/ai/agentforce/guide/lightning-types-example-full-editor-renderer.md#customize-ui-for-output).
:::

1. [**Create the LWC**](https://developer.salesforce.com/docs/platform/lwc/guide/create-components-introduction.md).<br /><br />This sample code shows the LWC component `myCardRenderer`.

   ```js
   import { LightningElement, api } from "lwc";
   export default class MyCardRenderer extends LightningElement {
     // The framework populates this property with the output data to be displayed.
     @api value;

     // Example: { cardName: 'Review Q3 Metrics', cardId: 'TSK-00124', createdDate: '2026-04-20', lastUpdate: '2026-04-23' }

     // Add your custom UI event handlers here.
   }
   ```

2. **Update the js-meta.xml file.**<br /><br />Include the [`lightning__AgentforceOutput`](https://developer.salesforce.com/docs/platform/lwc/guide/targets-lightning-agentforce-output.md) target.<br /><br />This sample code shows the contents of the `myCardRenderer.js-meta.xml` file.

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
       <apiVersion>64.0</apiVersion>
       <isExposed>true</isExposed>
       <masterLabel>My Card Renderer</masterLabel>
       <targets>
         <target>lightning__AgentforceOutput</target>
       </targets>
   </LightningComponentBundle>
   ```

3. **Configure the renderer.json file.**<br /><br />Use the `$` keyword to map the type to the component.<br /><br />Here’s how to reference `myCardRenderer` to override the renderer for the `taskCard` custom Lightning type in the `renderer.json` file.

   ```json
   {
     "renderer": {
       "componentOverrides": {
         "$": {
           "definition": "c/myCardRenderer"
         }
       }
     }
   }
   ```

**Example: Attribute Mapping**

If you’re reusing an existing component and the property names don't match your schema (for example, the component uses `title` instead of `cardName`), you must map the properties.

1. **Create the LWC.**<br /><br />This sample code shows `myExistingCardRenderer`.

   ```js
   import { LightningElement, api } from "lwc";
   export default class MyExistingCardRenderer extends LightningElement {
     // The framework passes the mapped data into these properties.

     // Expected value example: 'Review Q3 Metrics'
     @api title;

     // Expected value example: 'TSK-00124'
     @api cardId;

     // Expected value example: '2026-04-20'
     @api createdDate;

     // Expected value example: '2026-04-23'
     @api lastUpdate;

     // Add your custom UI event handlers here.
   }
   ```

2. **Update the js-meta.xml file.**<br /><br />Expose the properties in `targetConfigs` to register them as valid input properties for the `lightning__AgentforceOutput` target.<br /><br />This sample code shows the contents of the`myExistingCardRenderer.js-meta.xml` file.

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
       <apiVersion>64.0</apiVersion>
       <isExposed>true</isExposed>
       <masterLabel>My Existing Card Renderer</masterLabel>
       <targets>
         <target>lightning__AgentforceOutput</target>
       </targets>
       <targetConfigs>
         <targetConfig targets="lightning__AgentforceOutput">
           <property name="title" type="lightning__textType" />
           <property name="cardId" type="lightning__textType" />
           <property name="createdDate" type="lightning__textType" />
           <property name="lastUpdate" type="lightning__textType" />
         </targetConfig>
       </targetConfigs>
   </LightningComponentBundle>
   ```

3. **Configure the renderer.json file with attribute mapping.**<br /><br />Use the `attributes` object to link schema fields to component properties.<br /><br />This sample code shows how to reference `myExistingCardRenderer` to override the renderer for the `taskCard` custom Lightning type in the `renderer.json` file.

   ```json
   {
     "renderer": {
       "componentOverrides": {
         "$": {
           "definition": "c/myExistingCardRenderer",
           "attributes": {
             "title": "{!$attrs.cardName}",
             "cardId": "{!$attrs.cardId}",
             "createdDate": "{!$attrs.createdDate}",
             "lastUpdate": "{!$attrs.lastUpdate}"
           }
         }
       }
     }
   }
   ```

:::note
You must map the component’s properties to the corresponding properties in the Apex class, even if they have the same name. However, if the component receives the entire Apex class object through a single value attribute, you don’t need to map the individual attributes.
:::

The expression `"title": "{!$attrs.cardName}"` links the `cardName` property of the `TaskRecord` Apex class to the `title` property of the LWC component `myExistingCardRenderer` (and vice versa).

Here’s what each element represents.

- `title`: Property in the LWC component `myExtistingCardRenderer`
- `{!$attrs}`: Pointer to the `TaskRecord` class
- `cardName`: Property in the `TaskRecord` class
- `{!$attrs.cardName}`: Evaluates to the specific value of the `cardName` property so it can be dynamically passed to the component

**See Also**

- [*Agentforce Developer Guide*: Custom Lightning Type Examples](https://developer.salesforce.com/docs/ai/agentforce/guide/lightning-types-examples.md)
- [*Salesforce Help*: Custom Lightning Types in the Salesforce Mobile App](https://help.salesforce.com/s/articleView?id=sf.salesforce_app_clt_mobile.htm\&type=5)
