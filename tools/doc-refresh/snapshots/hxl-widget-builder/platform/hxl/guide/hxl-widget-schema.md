# Schema File

The optional `schema.json` file defines the widget's attribute contract. It specifies the attributes and their associated Lightning types that the widget accepts, including display metadata (such as title and description for attribute). The Lightning types determine validation rules and data types for each attribute.

:::note
To use attribute mapping to connect your widget to a Lightning type's dynamic data, include a `schema.json` file. Without it, the widget can only display static, hardcoded values.
:::

The schema file enables:

- Design-time validation of data bindings between Lightning types and Widgets
- Runtime binding of attributes to enable dynamic widget behavior

This table lists the keywords that you can specify for individual widget attributes.

| Keyword          | Description                                                                                                                      |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `title`          | The display name for the attribute.                                                                                              |
| `description`    | A brief explanation of the attribute's purpose.                                                                                  |
| `lightning:type` | The Lightning type reference for the attribute, such as `lightning__textType`, `lightning__numberType`, or `lightning__urlType`. |

This template shows the standard structural composition for defining a widget schema file.

```json
{
  "title": "Widget Schema Title",
  "description": "Description of the widget's attribute contract",
  "properties": {
    "attributes": {
      "type": "object",
      "properties": {
        "Name": {
          "title": "Display Name",
          "description": "Description shown in Widget Builder",
          "lightning:type": "lightning__textType"
        }
      }
    }
  }
}
```

This example shows a `schema.json` configuration file for a hotel card widget, establishing the expected data types and display metadata for the widget attributes.

```json
{
  "title": "Hotel Card Widget",
  "description": "Displays hotel information as a visual card",
  "type": "object",
  "properties": {
    "attributes": {
      "lightning:type": "lightning__objectType",
      "properties": {
        "title": {
          "title": "Hotel Name",
          "description": "Primary heading displayed at the top",
          "lightning:type": "lightning__textType"
        },
        "imageUrl": {
          "title": "Image URL",
          "description": "URL of the hotel image",
          "lightning:type": "lightning__urlType"
        },
        "price": {
          "title": "Price Per Night",
          "description": "Nightly rate displayed as currency",
          "lightning:type": "lightning__numberType"
        },
        "description": {
          "title": "Description",
          "description": "Short description of the hotel",
          "lightning:type": "lightning__textType"
        }
      }
    }
  }
}
```
