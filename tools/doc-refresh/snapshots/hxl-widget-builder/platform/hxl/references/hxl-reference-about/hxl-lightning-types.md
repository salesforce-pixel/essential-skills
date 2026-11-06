# HXL Lightning Types Reference

Headless Experience Layer (HXL) components use Lightning types in their property definitions. Each type defines the shape and allowed values of a property. The types describe layout, formatting, and structured data for HXL components. HXL renders each type natively on supported surfaces.

For input-focused Lightning types, see the [Lightning Types Reference](https://developer.salesforce.com/docs/platform/lightning-types/references/lightning-types/lightning-types-reference.md) instead.

HXL Lightning types include:

- [Layout and sizing types](#layout-and-sizing-types)
- [Content and display types](#content-and-display-types)
- [Interaction types](#interaction-types)
- [Table types](#table-types)

***

## Layout and Sizing Types

Control how components are sized, spaced, aligned, and positioned within their containers.

### lightning\_\_alignmentType

Use the `lightning__alignmentType` type to control the cross-axis alignment of a container's children. The type is a string enumeration.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

The `lightning__alignmentType` type accepts these values. The default is `stretch`.

| Value               | Description                                     |
| ------------------- | ----------------------------------------------- |
| `start`             | Aligns children to the start of the cross axis. |
| `center`            | Centers children on the cross axis.             |
| `end`               | Aligns children to the end of the cross axis.   |
| `stretch` (default) | Stretches children to fill the cross axis.      |

### lightning\_\_extentType

Use the `lightning__extentType` type to specify how much space a block occupies within its container. The type is a string enumeration.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

The `lightning__extentType` type accepts these values. The default is `auto`.

| Value            | Description                            |
| ---------------- | -------------------------------------- |
| `auto` (default) | Sizes the block to fit its content.    |
| `xs`             | Extra small extent.                    |
| `sm`             | Small extent.                          |
| `md`             | Medium extent.                         |
| `lg`             | Large extent.                          |
| `xl`             | Extra large extent.                    |
| `full`           | Occupies the full available extent.    |
| `stretch`        | Stretches to fill the available space. |

### lightning\_\_gapType

Use the `lightning__gapType` type to control the space between child elements in a container. The type is a string enumeration.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

The `lightning__gapType` type accepts these values. The default is `md`.

| Value          | Description                |
| -------------- | -------------------------- |
| `none`         | No space between children. |
| `xs`           | Extra small gap.           |
| `sm`           | Small gap.                 |
| `md` (default) | Medium gap.                |
| `lg`           | Large gap.                 |
| `xl`           | Extra large gap.           |

### lightning\_\_sizeType

Use the `lightning__sizeType` type to specify the size of a block on a shared t-shirt-size scale. The type is a string enumeration.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

The `lightning__sizeType` type accepts these values. The default is `md`.

| Value          | Description       |
| -------------- | ----------------- |
| `xs`           | Extra small size. |
| `sm`           | Small size.       |
| `md` (default) | Medium size.      |
| `lg`           | Large size.       |
| `xl`           | Extra large size. |

### lightning\_\_orientationType

Use the `lightning__orientationType` type to set the layout orientation of a component. The type is a string enumeration.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

The `lightning__orientationType` type accepts these values. The default is `horizontal`.

| Value                  | Description                    |
| ---------------------- | ------------------------------ |
| `horizontal` (default) | Lays out content horizontally. |
| `vertical`             | Lays out content vertically.   |

### lightning\_\_justifyType

Use the `lightning__justifyType` type to control the horizontal distribution of children within a container. The type is a string enumeration.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

The `lightning__justifyType` type accepts these values. The default is `start`.

| Value             | Description                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------------------ |
| `start` (default) | Packs children toward the start.                                                                 |
| `center`          | Centers children along the main axis.                                                            |
| `end`             | Packs children toward the end.                                                                   |
| `between`         | Distributes children with equal space between them.                                              |
| `around`          | Distributes children with equal space around each.                                               |
| `evenly`          | Distributes children so that spacing between any two adjacent items, and to the edges, is equal. |
| `space-between`   | Alias for `between`.                                                                             |
| `space-around`    | Alias for `around`.                                                                              |
| `space-evenly`    | Alias for `evenly`.                                                                              |

### lightning\_\_positionType

Use the `lightning__positionType` type to specify a preferred position, such as the placement of a tooltip relative to its anchor. The type is a string enumeration.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

The `lightning__positionType` type accepts these values. The default is `top`.

| Value           | Description                           |
| --------------- | ------------------------------------- |
| `top` (default) | Positions above the anchor.           |
| `right`         | Positions to the right of the anchor. |
| `bottom`        | Positions below the anchor.           |
| `left`          | Positions to the left of the anchor.  |

***

## Content and Display Types

Format text, icons, and status indicators shown to users.

### lightning\_\_iconName

Use the `lightning__iconName` type to specify a semantic icon identifier. Renderers map this identifier to a concrete icon in their own icon system. The type is a string enumeration.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

The `lightning__iconName` type accepts these values.

|                                  |                 |                  |                                |
| -------------------------------- | --------------- | ---------------- | ------------------------------ |
| `activity`                       | `alert-circle`  | `alert-triangle` | `align-center`                 |
| `align-horizontal-space-between` | `align-left`    | `align-right`    | `align-vertical-space-between` |
| `bell`                           | `bookmark`      | `box`            | `braces`                       |
| `briefcase`                      | `building`      | `calculator`     | `calendar`                     |
| `caret-down`                     | `caret-left`    | `caret-right`    | `caret-up`                     |
| `check`                          | `check-circle`  | `chevron-down`   | *`chevron-left`*               |
| `chevron-right`                  | `chevron-up`    | `circle`         | `circle-dot`                   |
| `clock`                          | `cloud`         | `code`           | `component`                    |
| `copy`                           | `credit-card`   | `crown`          | `database`                     |
| `dashboard`                      | `divide`        | `dollar-sign`    | `dot`                          |
| `download`                       | `edit`          | `equal`          | `equal-not`                    |
| `eye`                            | `eye-off`       | `file`           | `file-edit`                    |
| `file-text`                      | `filter`        | `folder`         | `gauge`                        |
| `git-branch`                     | `git-compare`   | `globe`          | `grid`                         |
| `hash`                           | `headset`       | `heart`          | `help-circle`                  |
| `home`                           | `image`         | `inbox`          | `info`                         |
| `layers`                         | `layout`        | `lightbulb`      | `lightning`                    |
| `link`                           | `list`          | `list-checks`    | `list-checks-rtl`              |
| `loader`                         | `lock`          | `mail`           | `map`                          |
| `map-pin`                        | `maximize`      | `megaphone`      | `message`                      |
| `microphone`                     | `minus`         | `minus-circle`   | `mouse-pointer-click`          |
| `open-in-new`                    | `package`       | `palette`        | `pencil`                       |
| `phone`                          | `plane`         | `plus`           | `plus-circle`                  |
| `plug`                           | `refresh`       | `repeat`         | `rotate-ccw`                   |
| `rotate-cw`                      | `search`        | `send`           | `server`                       |
| `settings`                       | `share`         | `shield`         | `shield-alert`                 |
| `shield-check`                   | `shopping-cart` | `space`          | `square`                       |
| `square-dashed`                  | `star`          | `sticky-note`    | `table`                        |
| `tag`                            | `target`        | `television`     | `thumb-down`                   |
| `thumb-up`                       | `ticket`        | `toggle-left`    | `trash`                        |
| `trending-up`                    | `upload`        | `user`           | `user-circle`                  |
| `users`                          | `video`         | `wifi`           | `x`                            |
| `x-circle`                       |                 |                  |                                |

For available icons, see the [HXL Playground Editor](https://www.headlessexperiencelayer.com/playground/?renderer=acc\&theme=slack#components/icon/all-icons).

### lightning\_\_markdownTextType

Use the `lightning__markdownTextType` type for text content formatted as Markdown. The type corresponds to the string type in a JSON schema.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

The `lightning__markdownTextType` type supports these configurable keywords.

| Keyword       | Required | Type   | Description                                     |
| ------------- | -------- | ------ | ----------------------------------------------- |
| `title`       | Yes      | String | The label text for the field                    |
| `description` | No       | String | The help text that describes the expected input |

### lightning\_\_textalignType

Use the `lightning__textalignType` type to control the horizontal alignment of text content. The type is a string enumeration.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

The `lightning__textalignType` type accepts these values. The default is `left`.

| Value            | Description               |
| ---------------- | ------------------------- |
| `left` (default) | Aligns text to the left.  |
| `center`         | Centers text.             |
| `right`          | Aligns text to the right. |

### lightning\_\_severityType

Use the `lightning__severityType` type to indicate an alert type or severity level. The type is a string enumeration.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

The `lightning__severityType` type accepts these values. The default is `info`.

| Value            | Description                      |
| ---------------- | -------------------------------- |
| `info` (default) | Informational severity.          |
| `success`        | Positive or successful severity. |
| `warning`        | Cautionary or advisory severity. |
| `error`          | Urgent or critical severity.     |

***

## Interaction Types

Describe the events dispatched when a user interacts with a component.

### lightning\_\_actionType

Use the `lightning__actionType` type to describe an action performed when a user interacts with a component. Because `lightning__actionType` is a complex type, its value is represented as an object.

This table shows the properties of the object that the `lightning__actionType` type describes.

| Property     | Required or Optional | Type                  | Description                                                                                                                                                    |
| ------------ | -------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `definition` | Required             | `lightning__textType` | The action identifier. Valid values include [`action/openLink`](#actionopenlink) and [`action/sendMessage`](#actionsendmessage), each with its own attributes. |
| `attributes` | Required             | Object                | Action-specific payload. A predefined action carries its typed payload here; a local action an arbitrary bag.                                                  |

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

HXL provides these predefined actions. Each is identified by its `definition` value and takes a specific set of `attributes`.

#### action/openLink

The `action/openLink` action opens a URL in the browser. It executes synchronously to preserve the user gesture context that the browser requires to open a window.

The `action/openLink` action takes these attributes.

| Attribute | Required or Optional | Type   | Description      |
| --------- | -------------------- | ------ | ---------------- |
| `url`     | Required             | String | The URL to open. |

This example shows a button that opens a link when clicked.

```json
{
  "definition": "tile/button",
  "attributes": {
    "label": "Open Link",
    "variant": "primary",
    "actions": {
      "click": [
        {
          "definition": "action/openLink",
          "attributes": {
            "url": "https://www.example.com"
          }
        }
      ]
    }
  }
}
```

#### action/sendMessage

The `action/sendMessage` action sends a message to the host or agent. The message goes directly to the agent rather than being displayed to the user. The agent processes it like a user message and responds with results. The agent may ask for confirmation before executing risky actions.

The `action/sendMessage` action takes these attributes.

| Attribute | Required or Optional | Type   | Description               |
| --------- | -------------------- | ------ | ------------------------- |
| `content` | Required             | String | The message text to send. |

This example shows a button that sends a message when clicked.

```json
{
  "definition": "tile/button",
  "attributes": {
    "label": "Yes, proceed",
    "actions": {
      "click": [
        {
          "definition": "action/sendMessage",
          "attributes": {
            "content": "Yes, proceed with the update"
          }
        }
      ]
    }
  }
}
```

### lightning\_\_eventType

Use the `lightning__eventType` type to describe an event dispatched when a user interacts with a tile. Because `lightning__eventType` is a complex type, its value is represented as an object.

This table shows the properties of the object that the `lightning__eventType` type describes.

| Property     | Required or Optional | Type                  | Description                                                          |
| ------------ | -------------------- | --------------------- | -------------------------------------------------------------------- |
| `definition` | Required             | `lightning__textType` | Action identifier. Maximum 255 characters.                           |
| `attributes` | Optional             | Object                | Event-specific attributes. The object accepts additional properties. |

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

This example shows an event with a definition and event-specific attributes.

```json
{
  "definition": "myAction",
  "attributes": {
    "recordId": "001XXXXXXXXXXXXXXX"
  }
}
```

***

## Table Types

Structure the columns and cell values rendered by the table component.

The table types define how the `tile/table` component structures its columns and cells. Each column type is a discriminated object identified by its `type` property.

### lightning\_\_cellValueType

Use the `lightning__cellValueType` type to represent a single table cell value. A cell holds exactly one value at a time — a string or a number, but never both.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

The `lightning__cellValueType` type accepts one of these value types.

| Type   | Description                         |
| ------ | ----------------------------------- |
| String | Short text — up to 255 characters.  |
| Number | Numeric value — integer or decimal. |

### lightning\_\_dateColumnType

Use the `lightning__dateColumnType` type to format table cell values as localized dates or datetimes. The type accepts ISO 8601 strings (for example, `2024-01-15T14:30:00Z` or `2024-01-15`) and numeric Unix timestamps in milliseconds (for example, `1705312200000`). Non-parseable cell values fall back to plain text display.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

Because `lightning__dateColumnType` is a complex type, its value is represented as an object.

This table shows the properties of the object that the `lightning__dateColumnType` type describes.

| Property    | Required or Optional | Type   | Description                                                                                                                     |
| ----------- | -------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------- |
| `type`      | Required             | String | Discriminator field. Always the string `date`.                                                                                  |
| `format`    | Optional             | String | The date format to show. `date` (default) shows only the date; `datetime` shows both date and time.                             |
| `dateStyle` | Optional             | String | Date formatting verbosity: `full`, `long`, `medium`, or `short`. Defaults to `short`.                                           |
| `timeStyle` | Optional             | String | Time formatting verbosity: `full`, `long`, `medium`, or `short`. Applies only when `format` is `datetime`. Defaults to `short`. |

This example shows a date column that displays both date and time.

```json
{
  "type": "date",
  "format": "datetime",
  "dateStyle": "medium",
  "timeStyle": "short"
}
```

### lightning\_\_numberColumnType

Use the `lightning__numberColumnType` type to format numeric table cell values with locale-aware decimal, percent, or currency formatting. Row values must be raw numeric strings,for example, `1234.56` or `0.75`. The renderer handles all formatting. Non-numeric cell values fall back to plain text display.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

Because `lightning__numberColumnType` is a complex type, its value is represented as an object.

This table shows the properties of the object that the `lightning__numberColumnType` type describes.

| Property                | Required or Optional | Type                     | Description                                                                                                                        |
| ----------------------- | -------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| `type`                  | Required             | String                   | Discriminator field. Always the string `number`.                                                                                   |
| `format`                | Optional             | String                   | Number formatting style: `decimal` (default), `percent`, or `currency`.                                                            |
| `currencyCode`          | Optional             | String                   | ISO 4217 currency code (for example, `USD` or `EUR`). Used only when `format` is `currency`. Defaults to `USD`.                    |
| `currencyCodeKey`       | Optional             | String                   | Row field key that supplies a per-row ISO 4217 currency code. Used only when `format` is `currency`. Falls back to `currencyCode`. |
| `currencyDisplayAs`     | Optional             | String                   | How the currency is displayed: `symbol`, `narrowSymbol`, `code`, or `name`. Used only when `format` is `currency`.                 |
| `minimumFractionDigits` | Optional             | `lightning__integerType` | Minimum number of decimal places to display. An integer between 0 and 20.                                                          |
| `maximumFractionDigits` | Optional             | `lightning__integerType` | Maximum number of decimal places to display. An integer between 0 and 20.                                                          |

This example shows a currency column formatted in euros.

```json
{
  "type": "number",
  "format": "currency",
  "currencyCode": "EUR",
  "currencyDisplayAs": "symbol",
  "minimumFractionDigits": 2,
  "maximumFractionDigits": 2
}
```

### lightning\_\_linkColumnType

Use the `lightning__linkColumnType` type to render table cell values as clickable hyperlinks. When applied to a column, cell values become anchor elements.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

Because `lightning__linkColumnType` is a complex type, its value is represented as an object.

This table shows the properties of the object that the `lightning__linkColumnType` type describes.

| Property | Required or Optional | Type   | Description                                                                                                        |
| -------- | -------------------- | ------ | ------------------------------------------------------------------------------------------------------------------ |
| `type`   | Required             | String | Discriminator field. Always the string `link`.                                                                     |
| `urlKey` | Optional             | String | Row field key containing the URL. When omitted, the column key value is used as both the display text and the URL. |

This example shows a link column that displays a person's name and links to a separate profile URL.

```json
{
  "type": "link",
  "urlKey": "profileUrl"
}
```

### lightning\_\_picklistColumnType

Use the `lightning__picklistColumnType` type to render table cell values by resolving row data values to human-readable labels from a defined set of options. Each cell value in row data is a canonical value string that maps to a label from the options array. The table displays the label. When a row value doesn't match any option, the raw value is displayed as a fallback.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

Because `lightning__picklistColumnType` is a complex type, its value is represented as an object.

This table shows the properties of the object that the `lightning__picklistColumnType` type describes.

| Property  | Required or Optional | Type                                     | Description                                                   |
| --------- | -------------------- | ---------------------------------------- | ------------------------------------------------------------- |
| `type`    | Required             | String                                   | Discriminator field. Always the string `picklist`.            |
| `options` | Required             | Array of `lightning__picklistOptionType` | Available picklist choices. Must contain at least one option. |

This example shows a picklist column that maps status values to labels.

```json
{
  "type": "picklist",
  "options": [
    { "label": "Active", "value": "active" },
    { "label": "Inactive", "value": "inactive" }
  ]
}
```

### lightning\_\_picklistOptionType

Use the `lightning__picklistOptionType` type to define a single picklist option with a display label and a canonical data value. This type is the item type in a picklist column's `options` array. Separating the label from the value supports localization (labels change per locale, values stay constant) and programmatic operations such as filtering and sorting.

**For Use In**

Agentforce, ChatGPT, Claude, Slackbot

Because `lightning__picklistOptionType` is a complex type, its value is represented as an object.

This table shows the properties of the object that the `lightning__picklistOptionType` type describes.

| Property | Required or Optional | Type                  | Description                                                                                                          |
| -------- | -------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `label`  | Required             | `lightning__textType` | Human-readable display text for this option. Maximum 255 characters.                                                 |
| `value`  | Required             | `lightning__textType` | Canonical value stored in row data for this option. Must be unique within the options array. Maximum 255 characters. |

This example shows a single picklist option.

```json
{
  "label": "In Progress",
  "value": "in_progress"
}
```
