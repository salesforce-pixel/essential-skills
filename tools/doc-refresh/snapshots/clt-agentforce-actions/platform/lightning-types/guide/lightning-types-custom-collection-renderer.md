# Define a Top-Level Collection Renderer Override

Associate a custom LWC for rendering structured lists of data.

For example, you have a custom Lightning type named `hotelResponse` that returns a list of hotels. You configure `renderer.json` to render the entire list of hotel data.

Here’s an example of what the `renderer.json` file can look like for the custom Lightning type `hotelResponse`.

```
+--lightningTypes
        +--hotelResponse
            +--schema.json
            +--lightningDesktopGenAi
               +--renderer.json
```

:::important
This example uses `lightningDesktopGenAi` to configure the custom Lightning type. Only specific channels support output overrides (`renderer.json`). Verify that your channel supports this feature before configuring the file.
:::

**Example: Basic Configuration Using the value Property**

This example shows you how to configure a component to handle the entire object via a single `@api` value property. The component receives the list via the value property.

:::note
To view a complete, working example of an LWC collection renderer implementation, see [Customize UI for Output](https://developer.salesforce.com/docs/ai/agentforce/guide/lightning-types-example-collection-renderer.md#customize-ui-for-output).
:::

1. [**Create the LWC**](https://developer.salesforce.com/docs/platform/lwc/guide/create-components-introduction.md).<br /><br />This sample code shows the LWC component `hotelDetails`.

   ```js
   import { LightningElement, api } from "lwc";
   export default class HotelDetails extends LightningElement {
     @api value;
   }
   ```

2. **Configure the renderer.json file.**<br /><br />Use the `collection` key to specify that this override applies to lists.<br /><br />Here’s how to reference `hotelDetails` to override the renderer for the `Hotel` output in the `renderer.json` file.

   ```json
   {
     "collection": {
       "renderer": {
         "componentOverrides": {
           "$": {
             "definition": "c/hotelDetails"
           }
         }
       }
     }
   }
   ```

**See Also**

- [*Agentforce Developer Guide*: Custom Lightning Type Examples](https://developer.salesforce.com/docs/ai/agentforce/guide/lightning-types-examples.md)
- [*Salesforce Help*: Custom Lightning Types in the Salesforce Mobile App](https://help.salesforce.com/s/articleView?id=sf.salesforce_app_clt_mobile.htm\&type=5)
