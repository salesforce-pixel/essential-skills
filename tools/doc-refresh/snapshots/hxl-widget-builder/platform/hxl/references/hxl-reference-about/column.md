# Column

**`tile/column`**

Arranges child components vertically with a configurable gap, cross-axis alignment, and width.

## Properties

| Name  | Required | Lightning Type             | Default | Description                                                                                                                                                                      |
| ----- | -------- | -------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| align | Yes      | `lightning__alignmentType` |         | The cross-axis alignment of children within the column. Valid values include `start`, `center`, `end`, or `stretch` (default).                                                   |
| gap   | Yes      | `lightning__gapType`       |         | The spacing between child components. Valid values include `none` for zero, `xs` through `xl` for increasing space. The default is `md` for medium.                              |
| width | No       | `lightning__extentType`    |         | The horizontal space the column occupies. Valid values include `auto` for content-sized, `xs` through `xl` for fixed widths, `full` for 100%, `stretch` to fill remaining space. |

## Usage

Stack child tiles vertically, top to bottom, with consistent spacing between them. Use a column to make content flow down the page. For example, a column can include a heading before body text that precedes a button.

```json
{
    "definition": "tile/column",
    "children": [
        {
            "definition": "tile/text",
            "attributes": { "text": "Column Header", "variant": "h3" }
        },
        {
            "definition": "tile/text",
            "attributes": { "text": "Vertically stacked content." }
        },
        {
            "definition": "tile/button",
            "attributes": { "label": "Action", "variant": "primary" }
        }
    ]
}
```

To build multi-column layouts where each column controls its own `width`, use
the column with [`tile/row`](/docs/platform/hxl/references/hxl-reference-about/row.md). Use `gap` for uniform spacing between all child content. Place each column inside `tile/row` for a side-by-side layout. Give each column a `width` to control how it shares the horizontal space.

```json
{
    "definition": "tile/row",
    "attributes": { "gap": "sm" },
    "children": [
        {
            "definition": "tile/column",
            "attributes": { "width": "md" },
            "children": [
                { "definition": "tile/text", "attributes": { "text": "Left", "variant": "h5" } }
            ]
        },
        {
            "definition": "tile/column",
            "attributes": { "width": "stretch" },
            "children": [
                { "definition": "tile/text", "attributes": { "text": "Right", "variant": "h5" } }
            ]
        }
    ]
}
```

## Alignment

Use these `align` values to specify how the column positions the content. This attribute applies to all child content uniformly.

- `start`: Content aligns to the leading edge.
- `center`: Content centers horizontally.
- `end`: Content aligns to the trailing edge.
- `stretch`: Content expands to fill the full column width.

## Width

Use these `width` values to specify the content width in a column. By default, the column has no width constraint and behaves like `auto`. The width can vary across surfaces.

- `auto`: Content sizes automatically with no explicit width constraint.
- `xs`: Extra small fixed width, or 3 out of a 12-column grid.
- `sm`: Small fixed width, or 4 out of a 12-column grid.
- `md`: Medium fixed width, or 6 out of a 12-column grid.
- `lg`: Large fixed width, or 8 out of a 12-column grid.
- `xl`: Extra large fixed width, or 9 out of a 12-column grid.
- `full`: Takes 100% of the parent width. Use `full` for single-column layouts or to make the column occupy the entire line.
- `stretch`: Grows to fill remaining available space in the parent, which is similar to the flex-grow behavior. Use `stretch` for fluid layouts like the sidebar or main content. Multiple columns that use `stretch` in the same row share remaining space equally.

## Design Guidelines

Consider these guidelines when working with columns.

- For a one-off gap between two specific children, insert a [`tile/spacer`](/docs/platform/hxl/references/hxl-reference-about/spacer.md) instead.
- Use [`tile/row`](/docs/platform/hxl/references/hxl-reference-about/row.md) to make content flow left to right rather than top to bottom.
- Set `align` to `center` to horizontally center children, or leave it at the default for the child content to fill the column width.
- Inside a row, give one column `width: "stretch"` so it absorbs the remaining space while the sibling rows stay content-sized.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/column` in Slackbot.

### ChatGPT

No known limitations for `tile/column` in ChatGPT.

### Agentforce

No known limitations for `tile/column` in Agentforce.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Column](https://www.headlessexperiencelayer.com/#components/column)
