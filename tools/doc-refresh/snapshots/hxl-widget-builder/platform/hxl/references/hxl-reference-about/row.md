# Row

**`tile/row`**

Arranges child components horizontally with a configurable gap, alignment, justification, and wrapping.

## Properties

| Name      | Required | Lightning Type             | Default  | Description                                                                                                                                         |
| --------- | -------- | -------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| align     | No       | `lightning__alignmentType` | `center` | The cross-axis alignment for children within the row. Valid values include  `start`, `center` (default), `end`, or `stretch`.                       |
| gap       | Yes      | `lightning__gapType`       |          | The spacing between child components. Valid values include `none` for zero, `xs` through `xl` for increasing space. The default is `md` for medium. |
| isWrapped | No       | `lightning__booleanType`   | true     | Specifies whether the children content wrap to the next line when they exceed the row width. Default true (content-aware wrapping).                 |
| justify   | No       | `lightning__textType`      | `start`  | The main-axis distribution for children within the row. Valid values include `start` (default), `center`, `end`, `between`, `around`, or `evenly`.  |

## Usage

Arrange child tiles horizontally, side by side, with consistent spacing between them. Use a row to make content flow left to right.

:::note
To stack content vertically instead, use [`tile/column`](/docs/platform/hxl/references/hxl-reference-about/column.md).
:::

For example, a row can include a label next to a value, a status badge beside a title, or a group of buttons.

```json
{
    "definition": "tile/row",
    "attributes": { "gap": "sm" },
    "children": [
        {
            "definition": "tile/text",
            "attributes": { "text": "Acme Corp", "variant": "h4" }
        },
        {
            "definition": "tile/badge",
            "attributes": { "label": "Active", "variant": "success" }
        }
    ]
}
```

To place content on opposite ends, set `justify` to `between`. Placing content on opposite ends is a common header pattern, for example, a title on one side and an action on the other.

```json
{
    "definition": "tile/row",
    "attributes": { "justify": "between", "align": "center" },
    "children": [
        {
            "definition": "tile/text",
            "attributes": { "text": "Product Name", "variant": "h4" }
        },
        {
            "definition": "tile/text",
            "attributes": { "text": "$99.99", "variant": "h4", "weight": "bold" }
        }
    ]
}
```

To build multi-column layouts, place [`tile/column`](/docs/platform/hxl/references/hxl-reference-about/column.md) tiles as the direct children of a row and specify the `width` on each column. Use `width: "stretch"` on one of the columns so it absorbs the remaining horizontal space while the other columns stay content-sized.

```json
{
    "definition": "tile/row",
    "attributes": { "gap": "md" },
    "children": [
        {
            "definition": "tile/column",
            "attributes": { "width": "md" },
            "children": [{ "definition": "tile/text", "attributes": { "text": "Sidebar" } }]
        },
        {
            "definition": "tile/column",
            "attributes": { "width": "stretch" },
            "children": [{ "definition": "tile/text", "attributes": { "text": "Main content" } }]
        }
    ]
}
```

## Alignment

Use these `align` values to position child content along the row's cross axis (vertical). This attribute applies to all child content uniformly.

- `start`: Content aligns to the top edge.
- `center` (default): Content centers vertically.
- `end`: Content aligns to the bottom edge.
- `stretch`: Content expands to fill the full row height.

## Gap

Use these `gap` values to set the spacing between child content. The gap applies uniformly between all child content. For individual spacing, use [`tile/spacer`](/docs/platform/hxl/references/hxl-reference-about/spacer.md) instead.

- `none`: No spacing between child content.
- `xs`: Extra small spacing.
- `sm`: Small spacing.
- `md` (default): Medium spacing.
- `lg`: Large spacing.
- `xl`: Extra large spacing.

## Justification

Use these `justify` values to distribute child content along the row's main axis (horizontal).

- `start` (default): Content packs to the leading edge.
- `center`: Content centers as a group.
- `end`: Content packs to the trailing edge.
- `between`: Content spreads with equal space between them, with the first and last flush to the edges.
- `around`: Content spreads with equal space around each, leaving half-size space at the edges.
- `evenly`: Content spreads with exactly equal space between them and at the edges.

## Design Guidelines

Consider these guidelines when working with rows.

- Use [`tile/column`](/docs/platform/hxl/references/hxl-reference-about/column.md) to make content flow top to bottom rather than left to right.
- Use `justify: "between"` for header layouts that pin a title to one side and actions to the other.
- Set `isWrapped` to `true` when a row holds a variable number of items, such as tags or badges, making the items flow onto multiple lines when space runs out.
- Nest [`tile/column`](/docs/platform/hxl/references/hxl-reference-about/column.md) tiles as children and specify `width: "stretch"` on one of the columns to build a sidebar-and-main layout.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/row` in Slackbot.

### ChatGPT

No known limitations for `tile/row` in ChatGPT.

### Agentforce

No known limitations for `tile/row` in Agentforce.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Row](https://www.headlessexperiencelayer.com/#components/row)
