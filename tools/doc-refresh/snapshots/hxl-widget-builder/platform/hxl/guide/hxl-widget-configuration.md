# Widget Configuration File

The `{widgetName}.uiwidget-meta.xml` file is a required resource in every widget bundle that specifies the widget type.

This table lists the configuration fields that you specify inside the `{widgetName}.uiwidget-meta.xml` file.

| Field         | Required or Optional | Description                                                                                                                |
| ------------- | -------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `widgetType`  | Required             | The widget implementation type. JSON is currently the only supported widget type and indicates a composition-based widget. |
| `masterLabel` | Optional             | Name for the widget                                                                                                        |
| `description` | Optional             | Description for the widget                                                                                                 |

This code example shows the required configuration structure for a widget configuration file.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<UiWidgetBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <masterLabel>Hotel Card</masterLabel>
    <description>Displays hotel information as a visual card.</description>
    <widgetType>JSON</widgetType>
</UiWidgetBundle>
```
