# Define a Property-Level Editor Override

You can define a specific editor for an individual property within your custom Lightning type in the `editor.json` file. This editor applies only to the specified property, while default editors continue to handle the remaining properties.

For example, you have a custom Lightning type named `contactType` with two properties: `firstName` and `lastName`. You want to use a custom input component to handle the `lastName` property (perhaps to add specific validation or styling), while the default text editor handles the `firstName`.

Here’s an example of what the `editor.json` file organization looks like for the custom Lightning type `contactType`.

```
+--lightningTypes
        +--contactType
            +--schema.json
            +--experienceBuilder
               +--editor.json
```

**Example: Configuration Using Property Names**

This example shows you how to configure a component to handle a specific property. The component receives only the value for that property via an `@api` value property.

1. **Define the schema.json file.**<br></br>This schema defines the data structure. It defines a `firstName` and `lastName` property, but you override only the `lastName`.

   ```json
   {
     "title": "Contact Type",
     "description": "Contact of a Person",
     "lightning:type": "lightning__objectType",
     "properties": {
       "firstName": {
         "title": "First Name",
         "description": "First Name of person",
         "lightning:type": "lightning__textType",
         "maxLength": 50
       },
       "lastName": {
         "title": "Last Name",
         "description": "Last name of person",
         "lightning:type": "lightning__textType",
         "maxLength": 50
       }
     },
     "required": ["firstName", "lastName"]
   }
   ```

2. **Create the LWC Bundle.**<br></br>Create a custom Lightning Web Component (such as `c/customLastNameInput`) to handle the specific property.<br></br>The `customLastNameInput.html` template binds the standard input component to your custom logic.

   ```html
   <template>
     <lightning-input
       type="text"
       label={label}
       value={value}
       required={required}
       disabled={disabled}
       onchange={handleChange}
       placeholder="Enter Last Name (Custom)"
       message-when-value-missing="Last Name is required for this contact type."
     >
     </lightning-input>
   </template>
   ```

   The `customLastNameInput.js` file handles the data flow. The component exposes public properties—such as `value`, `label`, and `required`—to receive data. To capture the user's input, the component dispatches a `valuechange` event whenever the value updates.

   ```js
   import { LightningElement, api } from "lwc";

   export default class CustomLastNameInput extends LightningElement {
     @api value; // Receives the current value of 'lastName'
     @api label; // Receives the 'title' from the schema ("Last Name")
     @api required; // Receives the required state (true)
     @api disabled; // Handled by the panel (e.g., after submission)

     handleChange(event) {
       const newValue = event.detail.value;

       // Notify the system that the value has changed
       this.dispatchEvent(
         new CustomEvent("valuechange", {
           detail: {
             value: newValue,
             validity: event.target.checkValidity(), // Optional: pass validity state
           },
         }),
       );
     }
   }
   ```

   The `customLastNameInput.js-meta.xml` file exposes the component to the editor.

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
       <apiVersion>64.0</apiVersion>
       <isExposed>true</isExposed>
       <targets>
          <target>lightning__PropertyEditor</target>
       </targets>
   </LightningComponentBundle>
   ```

3. **Configure the editor.json file.**<br></br>Use the property name `lastName` as the key in the `componentOverrides` section.<br></br>Here’s how to reference `customLastNameInput` to override the editor in the `editor.json` file.

   ```json
   {
     "editor": {
       "componentOverrides": {
         "lastName": {
           "definition": "c/customLastNameInput"
         }
       }
     }
   }
   ```

**Example: Layout Configuration**

If you're reusing an existing component and decide to use layouts, you can combine the `layout` and `componentOverrides` sections in the `editor.json` file. With this approach, you control the visual arrangement of properties while simultaneously assigning a specific custom component to handle the behavior of an individual property.

In this scenario, you arrange the `firstName` and `lastName` properties horizontally by using a layout, while specifically overriding the `lastName` property to use a reused custom component (`c/customLastNameInput`).

1. **Define the schema.json file.**<br></br>This schema defines the data structure. It defines a `firstName` and `lastName` property, but you override only the `lastName`.

   ```json
   {
     "title": "Contact Type",
     "description": "Contact of a Person",
     "lightning:type": "lightning__objectType",
     "properties": {
       "firstName": {
         "title": "First Name",
         "description": "First Name of person",
         "lightning:type": "lightning__textType",
         "maxLength": 50
       },
       "lastName": {
         "title": "Last Name",
         "description": "Last name of person",
         "lightning:type": "lightning__textType",
         "maxLength": 50
       }
     },
     "required": ["firstName", "lastName"]
   }
   ```

2. **Create the LWC Bundle.**<br></br>Create a custom Lightning Web Component (such as `c/customLastNameInput`) to handle the specific property.<br></br>The `customLastNameInput.html` template binds the standard input component to your custom logic.

   ```html
   <template>
     <lightning-input
       type="text"
       label={label}
       value={value}
       required={required}
       disabled={disabled}
       onchange={handleChange}
       placeholder="Enter Last Name (Custom)"
       message-when-value-missing="Last Name is required for this contact type."
     >
     </lightning-input>
   </template>
   ```

   The `customLastNameInput.js` file handles the data flow. The component exposes public properties—such as `value`, `label`, and `required`—to receive data. To capture the user's input, the component dispatches a `valuechange` event whenever the value updates.

   ```js
   import { LightningElement, api } from "lwc";

   export default class CustomLastNameInput extends LightningElement {
     @api value; // Receives the current value of 'lastName'
     @api label; // Receives the 'title' from the schema ("Last Name")
     @api required; // Receives the required state (true)
     @api disabled; // Handled by the panel (e.g., after submission)

     handleChange(event) {
       const newValue = event.detail.value;

       // Notify the system that the value has changed
       this.dispatchEvent(
         new CustomEvent("valuechange", {
           detail: {
             value: newValue,
             validity: event.target.checkValidity(), // Optional: pass validity state
           },
         }),
       );
     }
   }
   ```

   The `customLastNameInput.js-meta.xml` file exposes the component to the editor.

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
       <apiVersion>64.0</apiVersion>
       <isExposed>true</isExposed>
       <targets>
          <target>lightning__PropertyEditor</target>
       </targets>
   </LightningComponentBundle>
   ```

3. **Configure the editor.json file.**<br></br>Use the property name `lastName` as the key in the `componentOverrides` section.<br></br>Here’s how to reference `customLastNameInput` to override the editor in the `editor.json` file.

   ```json
   {
     "editor": {
       "componentOverrides": {
         "lastName": {
           "definition": "c/customLastNameInput"
         }
       },
       "layout": {
         "definition": "lightning/verticalLayout",
         "children": [
           {
             "definition": "lightning/horizontalLayout",
             "children": [
               {
                 "definition": "lightning/propertyLayout",
                 "attributes": { "property": "firstName" }
               },
               {
                 // This will render the overridden c/customLastNameInput
                 // defined in componentOverrides above.
                 "definition": "lightning/propertyLayout",
                 "attributes": { "property": "lastName" }
               }
             ]
           }
         ]
       }
     }
   }
   ```

   :::note
   When you use `lightning/propertyLayout` to place a property, the editor checks for a corresponding `componentOverrides` definition. If an override exists (such as in the `lastName` example), the custom component renders. Otherwise, the default input renders.
   :::

**See Also**

- [*Lightning Web Components Developer Guide*: Overview: Creating Custom Property Types and Editors](https://developer.salesforce.com/docs/platform/lwc/guide/use-experience-cloud-overview-custom-property-types.md)
