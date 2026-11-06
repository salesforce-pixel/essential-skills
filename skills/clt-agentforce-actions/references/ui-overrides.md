# UI overrides: editor.json, renderer.json, and the LWC contracts

Each file lives in a channel folder (`lightningTypes/<type>/<channel>/`). See
[bundle-and-schema.md](bundle-and-schema.md#channels-salesforce-applications-you-can-override).

## Override kinds

| Kind | File / key | When |
|---|---|---|
| **Top-level editor** | `editor.componentOverrides.$` | One LWC captures the whole input object |
| **Property-level editor** | `editor.componentOverrides.<propertyName>` | Custom input for one property. Defaults handle the rest |
| **Top-level renderer** | `renderer.componentOverrides.$` | One LWC displays one output instance |
| **Collection renderer** | `collection.renderer.componentOverrides.$` | One LWC displays the whole list at once |
| **Layout** | `editor.layout` / `renderer.layout` | Arrange properties (vertical/horizontal groups) |

Use `componentOverrides` and `layout`. The legacy keys `propertyRenderers` and `view` are rejected.

## Top-level renderer (single object output)

`lightningTypes/taskCard/lightningDesktopGenAi/renderer.json`
```json
{
  "renderer": {
    "componentOverrides": {
      "$": { "definition": "c/myCardRenderer" }
    }
  }
}
```

```js
import { LightningElement, api } from "lwc";
export default class MyCardRenderer extends LightningElement {
  // The framework sets this to the output data, e.g.
  // { cardName: 'Review Q3 Metrics', cardId: 'TSK-00124', createdDate: '2026-04-20', lastUpdate: '2026-04-23' }
  @api value;
}
```

```xml
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>64.0</apiVersion>
    <isExposed>true</isExposed>
    <masterLabel>My Card Renderer</masterLabel>
    <targets>
        <target>lightning__AgentforceOutput</target>
    </targets>
</LightningComponentBundle>
```

The full-example LWC also adds a `targetConfig` that names the CLT it renders:
```xml
<targetConfigs>
  <targetConfig targets="lightning__AgentforceOutput">
    <sourceType name="c__flightResponse"/>
  </targetConfig>
</targetConfigs>
```
Only the docs' full examples include it. The minimal examples work without it.

If the data needs to be reshaped (formatting, derived fields), do it in `connectedCallback()`
or in a getter. If `value` can change after the first render, a getter is safer.

## Collection renderer (list output)

```json
{
  "collection": {
    "renderer": {
      "componentOverrides": {
        "$": { "definition": "c/hotelDetails" }
      }
    }
  }
}
```

- The CLT's `schema.json` references the **item** class (`@apexClassType/c__Hotel`). The action
  output is a list (`list[object]` in Agent Script).
- The LWC gets the **array** in `@api value`, so iterate with `<template for:each={value} for:item="hotel">`.
- Example `js-meta.xml` targetConfig:
  `<sourceType name="lightning__listType" itemTypeName="c__hotelResponse"/>`

## Top-level editor (input form)

```json
{
  "editor": {
    "componentOverrides": {
      "$": { "definition": "c/flightRequestFilter" }
    }
  }
}
```

Editor LWC contract:

```js
import { api, LightningElement } from "lwc";
export default class FlightRequestFilter extends LightningElement {
  @api readOnly = false;            // set by the panel after submission
  @api value;                       // NOT pre-populated by the agent; capture-only
  price; discountPercentage;

  handleInputChange(event) {
    event.stopPropagation();        // don't let the inner input's change event bubble
    const { name, value } = event.target;
    this[name] = value;
    this.dispatchEvent(new CustomEvent("valuechange", {
      detail: { value: { price: this.price, discountPercentage: this.discountPercentage } }
    }));
  }
}
```

- Target: `lightning__AgentforceInput`. Example targetConfig: `<targetType name="c__flightFilter"/>`.
- **`value` doesn't support data injection.** The agent can't pre-fill it from the conversation
  or defaults. The framework sends what the user entered to the action **only when they submit**
  in the chat.
- Dispatch `valuechange` with the **whole** object in `detail.value` on every change. You can add
  `detail.validity` (e.g. `event.target.checkValidity()`).
- Bind `read-only={readOnly}` (or `disabled`) on inputs so the form locks after submit.

## Property-level editor

Overrides one property. The default editors handle the others.

```json
{
  "editor": {
    "componentOverrides": {
      "lastName": { "definition": "c/customLastNameInput" }
    }
  }
}
```

The property LWC receives `@api value` (that property's value), `@api label` (the schema
`title`), `@api required` and `@api disabled`. It reports changes the same way:

```js
handleChange(event) {
  this.dispatchEvent(new CustomEvent("valuechange", {
    detail: { value: event.detail.value, validity: event.target.checkValidity() }
  }));
}
```

The docs' property-level example is an **object-based** type in `experienceBuilder` with the
target `lightning__PropertyEditor`.

sf-skills lists built-in property components you can use instead of a custom LWC. Editors:
`es_property_editors/inputText`, `inputNumber`, `inputRichText`, `inputImage`, `inputTextarea`
(not `inputList`, and no `itemSchema` attributes). Renderers: `es_property_editors/outputText`,
`outputNumber`, `outputImage`, and `genericListTypeRenderer` for lists.

## Layout

```json
{
  "editor": {
    "componentOverrides": { "lastName": { "definition": "c/customLastNameInput" } },
    "layout": {
      "definition": "lightning/verticalLayout",
      "children": [
        { "definition": "lightning/horizontalLayout",
          "children": [
            { "definition": "lightning/propertyLayout", "attributes": { "property": "firstName" } },
            { "definition": "lightning/propertyLayout", "attributes": { "property": "lastName" } }
          ] }
      ]
    }
  }
}
```

- By default, properties render in a vertical stack in schema order.
- `lightning/propertyLayout` takes **only** the `property` attribute. Adding `label`/`title` fails
  with `additionalProperties`.
- When `propertyLayout` places a property, a matching `componentOverrides` entry wins. Otherwise
  the default input renders.
- JSON doesn't allow comments. Remove any `//` lines you copied from the docs.

## Attribute mapping (`{!$attrs.…}`)

Use this when an existing LWC's `@api` names differ from the schema. Map in the override and expose
the properties in `targetConfig`:

```json
{
  "editor": {
    "componentOverrides": {
      "$": {
        "definition": "c/myExistingTaskComponent",
        "attributes": { "urgency": "{!$attrs.priorityLevel}", "dueDate": "{!$attrs.dueDate}" }
      }
    }
  }
}
```

```xml
<targetConfigs>
  <targetConfig targets="lightning__AgentforceInput">
    <property name="urgency" type="lightning__textType" />
    <property name="dueDate" type="lightning__textType" />
  </targetConfig>
</targetConfigs>
```

- `{!$attrs}` points to the type's data object. `{!$attrs.priorityLevel}` gets that property's
  value and binds both ways.
- If you map at all, map **every** component property, even ones with the same name. If the
  LWC takes the whole object via `@api value`, don't map anything.
- Every `$attrs.<name>` must exist in the type schema, and the value types must match what the
  component expects.
- **Apex-based types:** sf-skills says the root override must **not** have `attributes`, because
  the projected schema has no `properties` block and `unevaluatedProperties: false` rejects every
  key. The docs show it working on an Apex class (`TaskRecord`). The `hxl-widget-builder` org
  testing maps `$attrs` on an Apex type for **widget** renderers. Default: no `attributes`, read
  `value`. If you need mapping, check-only deploy first.

## Global copy (`getFormattedValue`)

To make the chat's **copy** button copy your component's content, expose a public method that
returns a string (plain text or rich-text HTML). The system calls it when the user clicks copy.

```js
@api
getFormattedValue() {
  let table = '<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse;">';
  table += "<thead><tr>";
  this.fields.forEach((f) => { table += `<th style="background-color:#f2f2f2;text-align:left;">${f.label}</th>`; });
  table += "</tr></thead><tbody>";
  this.records.forEach((r) => {
    table += "<tr>";
    this.fields.forEach((f) => { table += `<td>${r.fields[f.apiName].value}</td>`; });
    table += "</tr>";
  });
  return table + "</tbody></table>";
}
```

The docs snippet is written `getFormattedValue = () {`, which isn't valid JavaScript. Use a
method (above) or an arrow-function property `getFormattedValue = () => { … }`, decorated with `@api`.
Escape record values if they can contain HTML.

## LWC target summary

| Role | Target | Typical targetConfig |
|---|---|---|
| Renderer (agent output) | `lightning__AgentforceOutput` | `<sourceType name="c__type"/>` or `<sourceType name="lightning__listType" itemTypeName="c__type"/>` |
| Editor (agent input) | `lightning__AgentforceInput` | `<targetType name="c__type"/>`, or `<property …/>` for attribute mapping |
| Experience Builder / object-type editor | `lightning__PropertyEditor` | — |

`isExposed` must be `true`. LWC API version 64.0 or later.
