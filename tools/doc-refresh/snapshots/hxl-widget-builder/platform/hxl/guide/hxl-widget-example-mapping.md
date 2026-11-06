# Example: Mapping a Hotel Card Widget for Agentforce

This example shows how Agentforce action output rendered in Lightning Experience flows through an Apex-based custom Lightning type named `hotelInfo` to the `hotelCard` widget.

This example uses two schema files that serve different purposes:

- The Lightning type schema describes the data shape—the data structure of hotel information returned by your data source
- The widget schema describes the UI shape—the attribute contract that defines what the card component needs to render

You map the data shape to the UI shape by using the renderer file.

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
          hotelInfo/
            schema.json
            renderer.json
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

The composition file (`uiWidgets/hotelCard/hotelCard.json`) defines the widget's visual structure and binds the widget’s schema attributes to UI components by using `{!$attrs.attributeName}` expressions.

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

The custom Lightning type schema file (`lightningTypes/hotelInfo/schema.json`) defines the data structure. This schema establishes the properties available for mapping to your widget.

```json
{
  "title": "Hotel Information",
  "description": "Structured hotel data returned by the booking agent",
  "lightning:type": "@apexClassType/c__HotelSearchResult$Hotel"
}
```

**See Also**

- [Core Concepts of Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-core.md)

## Map Lightning Type Data to the Widget

The renderer file (`lightningTypes/hotelInfo/renderer.json`) maps the Lightning type's data properties to the widget's attributes.

```json
{
  "renderer": {
    "componentOverrides": {
      "$": {
        "definition": "@widget/c/hotelCard",
        "attributes": {
          "hotelId": "{!$attrs.hotelId}",
          "name": "{!$attrs.name}",
          "city": "{!$attrs.city}",
          "checkInTime": "{!$attrs.checkInTime}",
          "checkOutTime": "{!$attrs.checkOutTime}",
          "pricePerNight": "{!$attrs.pricePerNight}",
          "rating": "{!$attrs.rating}"
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

To deploy both the Lightning type and Widget together, include them in a single `package.xml` manifest.

This example shows a manifest that includes both the `hotelCard` widget and `hotelInfo` Lightning type.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>hotelCard</members>
        <name>UiWidgetBundle</name>
    </types>
    <types>
        <members>hotelInfo</members>
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

After you deploy the widget and the custom Lightning type, the widget is ready to render Agentforce action output in Lightning Experience.

**See Also**

- [Use HXL Widgets as Agentforce Action Output](/docs/platform/hxl/guide/agentforce-action-output.md)
- [Core Concepts of Custom Lightning Types](https://developer.salesforce.com/docs/platform/lightning-types/guide/lightning-types-core.md)
- [Supported Applications and Platforms](/docs/platform/hxl/guide/hxl-rich-ui.md#supported-applications-and-platforms)
- [HXL Components](/docs/platform/hxl/references/hxl-reference-about/about-hxl-components.md#components)
