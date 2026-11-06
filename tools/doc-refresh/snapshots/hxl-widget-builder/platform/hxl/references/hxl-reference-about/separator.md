# Separator

**`tile/separator`**

Adds a visual boundary between content sections by using a horizontal or vertical line.

## Properties

| Name        | Required | Lightning Type        | Default      | Description                                                                               |
| ----------- | -------- | --------------------- | ------------ | ----------------------------------------------------------------------------------------- |
| orientation | No       | `lightning__textType` | `horizontal` | The axis of the dividing line. Valid values include `horizontal` (default) or `vertical`. |

## Usage

Use a separator to mark a boundary between sections of content with a visible line. A separator is useful as a thematic break between groups of related content, between list sections, or inside a toolbar.

:::note
The separator adds spacing with a visible line. To add spacing without a visible line, use [`tile/spacer`](/docs/platform/hxl/references/hxl-reference-about/spacer.md) instead.
:::

A separator inherits its length from the container it sits in: a `horizontal` separator spans the full width of its parent, and a `vertical` separator spans the full height.

To include a horizontal separator between vertical groups of text, use `tile/separator` as a child of `tile/column`.

```json
{
    "definition": "tile/column",
    "children": [
        { "definition": "tile/text", "attributes": { "text": "Account details" } },
        { "definition": "tile/separator" },
        { "definition": "tile/text", "attributes": { "text": "Billing details" } }
    ]
}
```

To place a vertical separator between items arranged in a row, use `tile/separator` as a child of `tile/row` and specify `"orientation": "vertical"`.

```json
{
    "definition": "tile/row",
    "attributes": { "gap": "sm" },
    "children": [
        { "definition": "tile/text", "attributes": { "text": "Drafts" } },
        { "definition": "tile/separator", "attributes": { "orientation": "vertical" } },
        { "definition": "tile/text", "attributes": { "text": "Sent" } }
    ]
}
```

## Orientation

Use `orientation` to set the axis of the dividing line. By default the separator is `horizontal`, matching the most common case of breaking up vertically stacked content.

- `horizontal`: A left-to-right line spanning the container width. Use to break between vertically stacked content, such as sections in a column.
- `vertical`: A top-to-bottom line spanning the container height. Use to break between horizontally arranged content, such as items in a row or a toolbar.

## Design Guidelines

Consider these guidelines when working with separators.

- Use a separator only when a visible line aids comprehension. For routine spacing between elements, use `gap` on the `tile/row` or `tile/column` parent container.
- Match `orientation` to the parent layout. For example, use `vertical` inside a row, and `horizontal` inside a column, so the line spans the intended axis.
- Avoid stacking multiple separators with no content between them.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/separator` in Slackbot.

### ChatGPT

No known limitations for `tile/separator` in ChatGPT.

### Agentforce

No known limitations for `tile/separator` in Agentforce.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Separator](https://www.headlessexperiencelayer.com/#components/separator)
