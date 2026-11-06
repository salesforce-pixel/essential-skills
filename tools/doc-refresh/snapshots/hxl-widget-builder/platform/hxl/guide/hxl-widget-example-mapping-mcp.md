# Example: Mapping a Hotel Card Widget for MCP

This example shows how output from a custom MCP server tool flows through two object-based custom Lightning types to the `hotelCard` widget in ChatGPT, Claude, or Slackbot.

This example uses three schema files that serve different purposes:

- The `hotelInfoResult` MCP result wrapper custom Lightning type schema describes the complete result returned by the MCP server tool, including `actionName`, `isSuccess`, and `outputValues`.
- The `hotelInfoOutputValues` MCP payload custom Lightning type schema describes the action-specific hotel data referenced by `outputValues`.
- The widget schema describes the UI shape, which is the attribute contract that defines the hotel information the card needs to render.

You map the nested data shape to the UI shape by using the `hotelInfoResult` custom Lightning type’s `renderer.json` file.

## Before You Begin

Download these sample data files.

- [hotelCardWidget.zip](https://resources.docs.salesforce.com/rel1/doc/en-us/static/misc/HotelCardWidget1.zip)
- [hotelInfoLightningType.zip](https://resources.docs.salesforce.com/rel1/doc/en-us/static/misc/HotelInfoLightningTypes1.zip)
- [hotelSearchResultApexClass.zip](https://resources.docs.salesforce.com/rel1/doc/en-us/static/misc/HotelSearchResultApexClassBundle1.zip)

## Project Directory Workspace Structure

This layout shows where the custom UiWidgetBundle and related LightningTypeBundle component files belong in your Salesforce DX project.

```
myProject/
  force-app/
    main/
      default/
        uiWidgets/
          hotelCard/
            hotelCard.json
            hotelCard.uiwidget-meta.xml
            schema.json
        lightningTypes/
          hotelInfoResult/
            schema.json
            renderer.json
          hotelInfoOutputValues/
            schema.json
```

:::note
In this directory structure, `renderer.json` sits directly parallel to `schema.json`. For widget references, create this file at the root level without using channel-specific subfolders. See [Connect Your Widget to a Custom Lightning Type](/docs/platform/hxl/guide/hxl-rich-ui.md#connect-your-widget-to-a-custom-lightning-type).
:::

**See Also**

- [UiWidgetBundle](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_uiwidgetbundle.htm)

## Declare the Widget Attribute Contract

The widget schema file (`uiWidgets/hotelCard/schema.json`) defines the attributes that your widget accepts. These attributes become available as `{!$attrs.attributeName}` bindings in your widget's composition file and as mapping targets in the Lightning type's `renderer.json` file.

```json
{
  "title": "Get Hotel Details Widget",
  "description": "Displays hotel details including name, city, check-in and check-out times, nightly price, and rating.",
  "type": "object",
  "properties": {
    "attributes": {
      "lightning:type": "lightning__objectType",
      "properties": {
        "hotelId": {
          "title": "Hotel ID",
          "description": "Unique hotel identifier (e.g. HTL-101)",
          "lightning:type": "lightning__textType"
        },
        "name": {
          "title": "Name",
          "description": "Hotel name",
          "lightning:type": "lightning__textType"
        },
        "city": {
          "title": "City",
          "description": "City where the hotel is located",
          "lightning:type": "lightning__textType"
        },
        "checkInTime": {
          "title": "Check-In Time",
          "description": "Standard check-in time",
          "lightning:type": "lightning__textType"
        },
        "checkOutTime": {
          "title": "Check-Out Time",
          "description": "Standard check-out time",
          "lightning:type": "lightning__textType"
        },
        "pricePerNight": {
          "title": "Price Per Night",
          "description": "Nightly price in USD",
          "lightning:type": "lightning__numberType"
        },
        "rating": {
          "title": "Rating",
          "description": "Guest rating out of 5",
          "lightning:type": "lightning__numberType"
        }
      }
    }
  }
}
```

**See Also**

- [Schema File](/docs/platform/hxl/guide/hxl-widget-schema.md)

## Build the Widget Composition

The composition file (`uiWidgets/hotelCard/hotelCard.json`) defines the widget's visual structure and binds widget’s schema attributes to UI components by using `{!$attrs.attributeName}` expressions.

```json
{
  "type": "lightning__agentforceWidget",
  "contentBody": {
    "widgetBody": {
      "definition": "tile/widget",
      "children": [
        {
          "definition": "tile/column",
          "attributes": {
            "gap": "md"
          },
          "children": [
            {
              "definition": "tile/container",
              "children": [
                {
                  "definition": "tile/text",
                  "attributes": {
                    "text": "{!$attrs.name}",
                    "variant": "h2"
                  }
                },
                {
                  "definition": "tile/row",
                  "attributes": {
                    "gap": "sm"
                  },
                  "children": [
                    {
                      "definition": "tile/text",
                      "attributes": {
                        "text": "{!$attrs.city}",
                        "variant": "caption",
                        "color": "muted"
                      }
                    },
                    {
                      "definition": "tile/text",
                      "attributes": {
                        "text": "•",
                        "variant": "caption",
                        "color": "muted"
                      }
                    },
                    {
                      "definition": "tile/text",
                      "attributes": {
                        "text": "{!$attrs.hotelId}",
                        "variant": "caption",
                        "color": "muted"
                      }
                    }
                  ]
                }
              ]
            },
            {
              "definition": "tile/container",
              "children": [
                {
                  "definition": "tile/column",
                  "attributes": {
                    "gap": "sm"
                  },
                  "children": [
                    {
                      "definition": "tile/row",
                      "attributes": {
                        "gap": "sm"
                      },
                      "children": [
                        {
                          "definition": "tile/text",
                          "attributes": {
                            "text": "Check-In",
                            "variant": "body",
                            "weight": "semibold"
                          }
                        },
                        {
                          "definition": "tile/text",
                          "attributes": {
                            "text": "{!$attrs.checkInTime}",
                            "variant": "body"
                          }
                        }
                      ]
                    },
                    {
                      "definition": "tile/row",
                      "attributes": {
                        "gap": "sm"
                      },
                      "children": [
                        {
                          "definition": "tile/text",
                          "attributes": {
                            "text": "Check-Out",
                            "variant": "body",
                            "weight": "semibold"
                          }
                        },
                        {
                          "definition": "tile/text",
                          "attributes": {
                            "text": "{!$attrs.checkOutTime}",
                            "variant": "body"
                          }
                        }
                      ]
                    },
                    {
                      "definition": "tile/row",
                      "attributes": {
                        "gap": "sm"
                      },
                      "children": [
                        {
                          "definition": "tile/text",
                          "attributes": {
                            "text": "Price / Night (USD)",
                            "variant": "body",
                            "weight": "semibold"
                          }
                        },
                        {
                          "definition": "tile/text",
                          "attributes": {
                            "text": "{!$attrs.pricePerNight}",
                            "variant": "body"
                          }
                        }
                      ]
                    },
                    {
                      "definition": "tile/row",
                      "attributes": {
                        "gap": "sm"
                      },
                      "children": [
                        {
                          "definition": "tile/text",
                          "attributes": {
                            "text": "Rating",
                            "variant": "body",
                            "weight": "semibold"
                          }
                        },
                        {
                          "definition": "tile/text",
                          "attributes": {
                            "text": "{!$attrs.rating}",
                            "variant": "body"
                          }
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  }
}
```

**See Also**

- [Composition File](/docs/platform/hxl/guide/hxl-widget-composition.md)

## Define Widget Configuration

The configuration file (`uiWidgets/hotelCard/hotelCard.uiwidget-meta.xml`) declares the widget bundle type required for deployment.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<UiWidgetBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <masterLabel>Hotel Card</masterLabel>
    <description>Displays hotel details including name, city, check-in and check-out times, nightly price, and rating.</description>
    <widgetType>JSON</widgetType>
</UiWidgetBundle>
```

**See Also**

- [Widget Configuration File](/docs/platform/hxl/guide/hxl-widget-configuration.md)

## Define the Lightning Type Schema

Define two object-based custom Lightning type schemas for the MCP server tool output. The MCP result wrapper schema represents the complete tool result, and its `outputValues` property references the MCP payload schema that defines the action-specific output.

### Define the MCP Payload Custom Lightning Type

The custom Lightning type schema file (`lightningTypes/hotelInfoOutputValues/schema.json`) defines the hotel-information payload referenced by the result wrapper’s `outputValues` property. Its `hotelInfo` property references the `HotelSearchResult.Hotel` Apex class.

```json
{
  "title": "Hotel Info Output Values",
  "description": "Payload fields from the HotelSearchResult response",
  "type": "object",
  "lightning:type": "lightning__objectType",
  "unevaluatedProperties": false,
  "lightning:tags": ["mcp"],
  "properties": {
    "hotelInfo": {
      "title": "Hotel Info",
      "lightning:type": "@apexClassType/c__HotelSearchResult$Hotel"
    }
  }
}
```

### Define the MCP Result Wrapper Custom Lightning Type

The custom Lightning type schema file (`lightningTypes/hotelInfoResult/schema.json`) represents the complete MCP server tool result. Its `outputValues` property references the `hotelInfoOutputValues` MCP payload custom Lightning type.

```json
{
  "title": "Hotel Info Result",
  "description": "Invocable-action result envelope for the HotelSearchResult MCP tool",
  "type": "object",
  "lightning:type": "lightning__objectType",
  "unevaluatedProperties": false,
  "lightning:tags": ["mcp"],
  "properties": {
    "actionName": {
      "title": "Action Name",
      "lightning:type": "lightning__textType"
    },
    "isSuccess": {
      "title": "Is Success",
      "lightning:type": "lightning__booleanType"
    },
    "outputValues": {
      "title": "Output Values",
      "lightning:type": "c__hotelInfoOutputValues"
    }
  }
}
```

**See Also**

- [Core Concepts of Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-core.md)

## Map Lightning Type Data to the Widget

The `renderer.json` file (`lightningTypes/hotelInfoResult/renderer.json`) maps nested hotel properties under `outputValues` to attributes defined in the `hotelCard` widget’s `schema.json` file.

```json
{
  "renderer": {
    "componentOverrides": {
      "$": {
        "definition": "@widget/c/hotelCard",
        "attributes": {
          "hotelId": "{!$attrs.outputValues.hotelInfo.hotelId}",
          "name": "{!$attrs.outputValues.hotelInfo.name}",
          "city": "{!$attrs.outputValues.hotelInfo.city}",
          "checkInTime": "{!$attrs.outputValues.hotelInfo.checkInTime}",
          "checkOutTime": "{!$attrs.outputValues.hotelInfo.checkOutTime}",
          "pricePerNight": "{!$attrs.outputValues.hotelInfo.pricePerNight}",
          "rating": "{!$attrs.outputValues.hotelInfo.rating}"
        }
      }
    }
  }
}
```

:::note
For detailed information about widget references and attribute mapping, see [Connect Your Widget to a Custom Lightning Type](/docs/platform/hxl/guide/hxl-rich-ui.md#connect-your-widget-to-a-custom-lightning-type).
:::

**See Also**

- [Connect Your Widget to a Custom Lightning Type](/docs/platform/hxl/guide/hxl-rich-ui.md#connect-your-widget-to-a-custom-lightning-type)

## Package Deployment Management

To deploy the widget and both custom Lightning types together, include them in a single `package.xml` manifest.

This manifest includes the `hotelCard` widget, the `hotelInfoOutputValues` MCP payload custom Lightning type, and the `hotelInfoResult` MCP result wrapper custom Lightning type.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>hotelCard</members>
        <name>UiWidgetBundle</name>
    </types>
    <types>
        <members>hotelInfoOutputValues</members>
        <members>hotelInfoResult</members>
        <name>LightningTypeBundle</name>
    </types>
    <version>67.0</version>
</Package>
```

### Deployment Order

When you deploy a Lightning type that references a widget, deploy the widget first or include it in the same package. Metadata API resolves deployment ordering automatically within a single package.

If you deploy the components independently across separate deployments, maintain this sequential order:

1. Deploy the UiWidgetBundle package to your target org first.
2. Deploy the LightningTypeBundle package to your target org second.

## After Deployment

After you deploy the widget and both custom Lightning types, the widget is ready to render MCP server tool output in ChatGPT, Claude, or Slackbot.

**See Also**

- [Use HXL Widgets on MCP Channels](/docs/platform/hxl/guide/hxl-mcp-channels.md)
- [Core Concepts of Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-core.md)
- [Supported Applications and Platforms](/docs/platform/hxl/guide/hxl-rich-ui.md#supported-applications-and-platforms)
- [HXL Components](/docs/platform/hxl/references/hxl-reference-about/about-hxl-components.md#components)
