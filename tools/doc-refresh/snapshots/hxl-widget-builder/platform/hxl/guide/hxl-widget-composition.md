# Composition File

The `{widgetName}.json` widget definition file is a required resource in every widget bundle. It defines the UI composition—specifying which components render, their layout hierarchy, ordering, and how they dynamically bind to widget attributes.

This table lists the properties that you can specify in a `{widgetName}.json` file.

| Property                 | Type   | Required or Optional | Description                                                                                                                                             |
| ------------------------ | ------ | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`                   | String | Required             | The content type identifier. Set this to `lightning__agentforceWidget`. This identifier applies to all supported Salesforce applications and platforms. |
| `contentBody`            | Object | Required             | The root content object containing the composition structure.                                                                                           |
| `contentBody.widgetBody` | Object | Required             | The root component that holds the widget's composition structure.                                                                                       |

This example shows a composition file for a hotel card widget (`hotelCard.json`) that defines the visual structure and data binding tokens. The `{!$attrs.attributeName}` expressions reference widget attributes defined in the widget's `schema.json` file.

```json
{
  "type": "lightning__agentforceWidget",
  "contentBody": {
    "widgetBody": {
      "definition": "tile/widget",
      "children": [
        {
          "definition": "tile/card",
          "attributes": {
            "padding": "lg",
            "variant": "default",
            "maxWidth": "full"
          },
          "children": [
            {
              "definition": "tile/image",
              "attributes": {
                "src": "{!$attrs.imageUrl}",
                "alt": "{!$attrs.title}"
              }
            },
            {
              "definition": "tile/text",
              "attributes": {
                "text": "{!$attrs.title}",
                "variant": "h3",
                "weight": "semibold"
              }
            },
            {
              "definition": "tile/text",
              "attributes": {
                "text": "{!$attrs.price}",
                "variant": "body",
                "weight": "medium"
              }
            },
            {
              "definition": "tile/text",
              "attributes": {
                "text": "{!$attrs.description}",
                "variant": "body"
              }
            }
          ]
        }
      ]
    }
  }
}
```

## Composition Building Blocks

To build the visual structure shown in the code example, understand these fundamental layout elements:

- **Components**: The atomic building units of a widget's visual layout. Each component specifies a `definition`. Depending on the component and its rendering behavior, it can also specify `attributes`, `children`, and `meta`.
  - **definition**: The specific component to render (such as `tile/card`, `tile/text`, or `title/image`).
  - **attributes**: Configuration key-value pairs applied directly to the component. These pairs can be static values or dynamic token expressions.
  - **children**: An array of nested child components rendered sequentially inside the parent component container.
  - **meta**: Rendering instructions that control whether a component renders or repeats for items in a collection.
- **Root Component Requirement**: Every widget structure requires a root `widgetBody` component with its definition set to `"tile/widget"`. This configuration serves as the primary wrapper holding all subsequent child components.
- **Data Binding Expressions**: Use the token syntax `{!$attrs.attributeName}` to reference widget attributes within component properties. The widget's `schema.json` defines these attributes. Attributes receive their values at run time when you connect the widget to a Lightning type through attribute mapping.

## Use Static Resources in Widgets

Widget attributes can reference external static resources, such as image URLs. To render, the static resource must be accessible without authentication.

To enable loading static resources from a specific domain via MCP servers, add the domain as a [Trusted URL](https://help.salesforce.com/s/articleView?id=xcloud.security_trusted_urls_manage.htm\&type=5) in your org. After you set up the Trusted URL, Salesforce automatically provisions the [Content Security Policy](https://help.salesforce.com/s/articleView?id=xcloud.shr_content_security_policy_csp_directive_rendering.htm\&type=5) setting for the MCP server.

## Use Salesforce Formulas in Widgets

Widget composition supports a formula language based on the [Salesforce formula engine](https://github.com/salesforce/formula-engine). Use formulas to automatically generate live results based on computed values and conditional statements. You can use infix operators for math, comparison, and logic, and built-in functions for conditionals, string operations, and so on.

For example, the formula `"text": "{!$order.subtotal * $order.taxRate}"` computes the amount of tax on an order. See the [HXL Playground](https://learnexperiencecloud.my.site.com/playground/#06-formulas) for more examples of formulas.

## Control Component Rendering with Meta Properties

Use the `meta` object in a widget composition to control whether a component renders and to repeat a component for items in a collection.

The `meta` object supports these properties.

| Property   | Required or optional | Description                                                                                                                                                                                                                                                                                                         |
| :--------- | :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `if`       | Optional             | References an expression that evaluates to a Boolean value. Includes the component only when the expression evaluates to `true`.<br><br>The `if` expression can reference a Boolean widget attribute, such as `{!$attrs.isVerified}`, or a Boolean property of the current item, such as `{!$amenity.isAvailable}`. |
| `forEach`  | Optional             | References the collection whose items the component renders.                                                                                                                                                                                                                                                        |
| `forItem`  | Optional             | Defines the variable used to reference the current item. The value must begin with `$`. If omitted, the value defaults to `$Item`.                                                                                                                                                                                  |
| `forIndex` | Optional             | Defines the variable used to reference the current item’s index. The value must begin with `$`.                                                                                                                                                                                                                     |

### Render a Component Conditionally

Use `meta.if` to control whether a component and its children render. The expression must evaluate to a Boolean value. If the expression evaluates to `true`, the component and its children render. If it evaluates to `false`, the component and its children aren’t included in the rendered output.

A non-Boolean result, such as a number, string, or empty array, isn’t supported and causes an evaluation error. A missing or null-valued reference is treated as `false`.

This example renders a message only when the `isVerified` widget attribute evaluates to `true`.

```json
{
  "definition": "tile/text",
  "meta": {
    "if": "{!$attrs.isVerified}"
  },
  "attributes": {
    "text": "Verified hotel",
    "variant": "body"
  }
}
```

In this example:

- `{!$attrs.isVerified}` references the `isVerified` attribute defined in the widget’s `schema.json` file.
- The `tile/text` component renders only when `isVerified` evaluates to `true`.

If the component contains children, excluding the component also excludes all its child components.

#### Use Complex Conditions

Use supported comparison operators and expression functions to combine conditions.

```json
{
  "definition": "tile/text",
  "meta": {
    "if": "{!AND($attrs.isAvailable, $attrs.price < 500)}"
  },
  "attributes": {
    "text": "Available within budget",
    "variant": "body"
  }
}
```

### Render a Component for Each Collection Item

Use `meta.forEach` to repeat a component for each item in a collection. Optionally, set `meta.forItem` to the variable that represents the current item. The `forItem` value must begin with `$`.If `forItem` is omitted, the current-item variable defaults to `$Item`.

This example renders a text component for each amenity in an `amenities` collection.

```json
{
  "definition": "tile/text",
  "meta": {
    "forEach": "{!$attrs.amenities}",
    "forItem": "$amenity"
  },
  "attributes": {
    "text": "{!$amenity.name}",
    "variant": "body"
  }
}
```

In this example:

- `{!$attrs.amenities}` references the `amenities` collection supplied through the widget’s attribute contract.
- `$amenity` represents the current item.
- `{!$amenity.name}` references the name property of the current item.
- The `tile/text` component renders once for each item in the collection.

This example omits `meta.forItem`, so the current-item variable defaults to `$Item`. The `{!$Item.name}` expression references the name property of the current item.

```json
{
  "definition": "tile/text",
  "meta": {
    "forEach": "{!$attrs.amenities}"
  },
  "attributes": {
    "text": "{!$Item.name}",
    "variant": "body"
  }
}
```

The optional `meta.forIndex` property defines a variable that represents the current item’s index. The value must begin with `$`.

This example uses `$amenityIndex` to reference the current item’s index:

```json
{
  "definition": "tile/text",
  "meta": {
    "forEach": "{!$attrs.amenities}",
    "forItem": "$amenity",
    "forIndex": "$amenityIndex"
  },
  "attributes": {
    "text": "{!$amenity.name}",
    "variant": "body"
  }
}
```

You can nest components that use `meta.forEach` to render multidimensional collections. Each iteration creates a separate scope for its item and index variables.

## Combine Conditional Rendering and List Iteration

When a component specifies both `meta.forEach` and `meta.if`, the condition is evaluated for each item in the collection. The component renders only for items whose condition evaluates to `true`.

This example renders only amenities whose `isAvailable` property evaluates to `true`.

```json
{
  "definition": "tile/text",
  "meta": {
    "forEach": "{!$attrs.amenities}",
    "forItem": "$amenity",
    "if": "{!$amenity.isAvailable}"
  },
  "attributes": {
    "text": "{!$amenity.name}",
    "variant": "body"
  }
}
```

In this example:

- `meta.forEach` iterates over the items in `amenities`.
- `$amenity` represents the current item.
- `meta.if` evaluates `$amenity.isAvailable` for the current item.
- The component renders for the current item only when `isAvailable` evaluates to `true`.

### Reference a Widget-Level Attribute in the Condition

When the `meta.if` condition references a widget-level attribute (such as `{!$attrs.showAmenities}`) instead of the scoped `forItem` variable, the condition evaluates once for the entire collection. As a result, the whole list either renders or is hidden—rather than being evaluated per item.

This example renders the entire list of amenities only when the widget-level `showAmenities` attribute evaluates to `true`.

```json
{
  "definition": "tile/text",
  "meta": {
    "forEach": "{!$attrs.amenities}",
    "forItem": "$amenity",
    "if": "{!$attrs.showAmenities}"
  },
  "attributes": {
    "text": "{!$amenity.name}",
    "variant": "body"
  }
}
```

In this example:

- `meta.if` evaluates the widget-level `{!$attrs.showAmenities}` attribute, not a property of the current item.
- Because the condition doesn't reference the `forItem` variable (`$amenity`), it's evaluated once for the whole collection.
- If `showAmenities` evaluates to `true`, all amenities render. If it evaluates to `false`, none render.

:::note
The scope of the `meta.if` condition determines the rendering behavior. When the condition references the `forItem` variable (such as `$amenity.isAvailable`), it's evaluated per item. When it references a widget-level attribute (such as `$attrs.showAmenities`), it's evaluated once for the entire collection.
:::

**See Also**

- [HXL Components](/docs/platform/hxl/references/hxl-reference-about/about-hxl-components.md#components)
