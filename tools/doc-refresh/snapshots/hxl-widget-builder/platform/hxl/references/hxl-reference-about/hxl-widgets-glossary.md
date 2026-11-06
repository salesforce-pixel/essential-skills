# Widgets Glossary of Terms

Learn more about the terms that are used for Headless Experience Layer (HXL) Widgets.

## Attribute Contract

The attributes and their associated Lightning types that a widget accepts, defined in the widget's `schema.json` file. The attribute contract specifies the Lightning types and display metadata for each widget attribute.

## Channel

The application or interaction experience, such as Claude or ChatGPT, which users interact with through different [surfaces](#surface).

See [Supported Applications and Platforms](/docs/platform/hxl/guide/hxl-rich-ui).

## Component

The atomic building unit of a widget's visual layout. Each component specifies a `definition`. Depending on the component and its rendering behavior, it can also specify `attributes`, `children`, and `meta`.

See [HXL Components](/docs/platform/hxl/references/hxl-reference-about/).

## Composition File

A required JSON file (`{widgetName}.json`) in every widget bundle that defines the widget's visual structure. It specifies which components render, their hierarchical nesting, ordering, and how they bind to data by using `{!$attrs.attributeName}` expressions.

## Conditional Rendering

A composition behavior that uses `meta.if` to include a component and its children when an expression evaluates to `true`. If the expression evaluates to `false`, the component and its children aren’t included in the rendered output.

## Data Binding Expression

A token expression with the syntax `{!$attrs.attributeName}` for referencing widget attributes that are defined in `schema.json`. These expressions receive actual values at run time when you connect the widget to a Lightning type through attribute mapping.

## List Iteration

A composition behavior that uses `meta.forEach` to repeat a component for each item in a collection. Use the optional `meta.forItem` property to define the current-item variable. If `meta.forItem` is omitted, the variable defaults to `$Item`.

## Meta Properties

Properties in a component’s `meta` object that control rendering behavior, such as conditional rendering and list iteration.

## MCP Payload Custom Lightning Type

An object-based custom Lightning type that defines the structure referenced by an MCP result wrapper custom Lightning type’s `outputValues` property. This term describes the custom Lightning type’s role in an MCP server tool configuration, not a category of custom Lightning type.

## MCP Result Wrapper Custom Lightning Type

An object-based custom Lightning type that represents the complete result returned by an MCP server tool, including `actionName`, `isSuccess`, and `outputValues`. This custom Lightning type contains the `renderer.json` file that maps nested payload properties to widget attributes. This term describes the custom Lightning type’s role in an MCP server tool configuration, not a category of custom Lightning type.

## Metadata API

A Salesforce API used for retrieving, deploying, creating, updating, or deleting customization information, such as UiWidgetBundles and LightningTypeBundles.

See [Understanding Metadata API](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_intro.htm).

## Namespace

A unique identifier used to distinguish metadata components. Use the default `c` namespace for widgets created in your org (for example, `@widget/c/hotelCard`).

## Root Component

The required `widgetBody` component that serves as the primary wrapper for a widget's composition. Its definition must be set to `"tile/widget"` and contains all subsequent child components.

## Schema File

An optional JSON file (`schema.json`) in a widget bundle that defines the widget's attribute contract—the attributes the widget accepts, including their associated Lightning types and display metadata. Required for widgets that use attribute mapping to connect to Lightning types. The schema validates data connections at design time.

## Surface

The visual or tactile area where users interact with HXL widgets. A surface is the specific device or environment on which a channel is rendered, such as mobile or desktop. For example, ChatGPT on mobile and ChatGPT on desktop refer to the same channel presented on different surfaces.

## Widget Bundle

The metadata component, with the API name UiWidgetBundle, used to create and deploy widgets. It's stored in the `uiWidgets` folder and contains the composition file (`{widgetName}.json`), configuration file (`{widgetName}.uiwidget-meta.xml`), and optionally a `schema.json` file.

## Widget

A platform-independent, reusable UI composition built by assembling components in a JSON file. You can deploy widgets across supported Salesforce applications and third-party platforms.

## Widget Attribute Mapping

The configuration in a Lightning type's `renderer.json` file that connects Lightning type data properties to widget schema attributes. The mapping uses the attributes object with widget attribute names as keys and `{!$attrs.propertyName}` expressions (referencing Lightning type properties) as values.

## Widget Configuration File

A required XML file (`{widgetName}.uiwidget-meta.xml`) in every widget bundle that specifies the widget type. The `widgetType` field set to JSON indicates a composition-based widget.

## See Also

[Lightning Types Glossary](https://developer.salesforce.com/docs/platform/lightning-types/references/lightning-types/lightning-types-glossary.md)
