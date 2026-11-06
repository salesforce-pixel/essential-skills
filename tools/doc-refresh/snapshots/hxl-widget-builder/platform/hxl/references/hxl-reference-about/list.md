# List Tile

**`tile/list`**

Shows a series of related items in a column. Use the `tile/listItem` child component for each item.

## Properties

| Name   | Required | Lightning Type        | Default | Description                                                                                      |
| ------ | -------- | --------------------- | ------- | ------------------------------------------------------------------------------------------------ |
| marker | No       | `lightning__textType` | `none`  | The leading marker style for each list item. Valid values include `none`, `bullet`, or `number`. |

## Usage

Use a list to arrange a series of related items in a single vertical column with consistent spacing that reads top to bottom. The list provides only the structural framing and optional leading markers. Each row is a `tile/listItem` that carries the actual content. Keep lists to between 1 and 10 items.

:::note
A list itself holds no content. Put text, links, and icons inside each [`tile/listItem`](/docs/platform/hxl/references/hxl-reference-about/listItem.md), not directly on the list.
:::

By default, the list doesn't use a marker, such as a bullet or number. To use a disc-style bullet, specify `"marker": "bullet"`.

```json
{
    "definition": "tile/list",
    "attributes": { "marker": "bullet" },
    "children": [
        {
            "definition": "tile/listItem",
            "children": [
                {
                    "definition": "tile/text",
                    "attributes": { "text": "Set up your environment" }
                }
            ]
        },
        {
            "definition": "tile/listItem",
            "children": [
                {
                    "definition": "tile/text",
                    "attributes": { "text": "Install dependencies" }
                }
            ]
        }
    ]
}
```

A list item can hold more than one child to show a title with supporting detail. For a title plus supporting line, stack two `tile/text` children within the item rather than splitting across rows. The two text children stack horizontally inside the single list item.

```json
{
    "definition": "tile/list",
    "children": [
        {
            "definition": "tile/listItem",
            "children": [
                {
                    "definition": "tile/text",
                    "attributes": { "text": "Set up your environment", "variant": "bold" }
                },
                {
                    "definition": "tile/text",
                    "attributes": {
                        "text": "Install Node.js 20+ and pnpm",
                        "variant": "caption",
                        "color": "muted"
                    }
                }
            ]
        }
    ]
}
```

## Marker

Use these `marker` values to set the marker shown on each list item.

- `none` (default): No marker. Use the default for plain stacks of rows where order and decoration don't add meaning.
- `bullet`: A bullet before each item for unordered sets where items are peers, such as features or options.
- `number`: Sequential numbering (1, 2, 3…) for ordered sequences such as steps or rankings where position matters.

## Design Guidelines

Consider these guidelines when working with lists.

- Keep lists short. Consider a "see more" or a summarized view if there are more than 10 items.
- For a horizontal arrangement of items rather than a vertical column, use `tile/row` instead.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/list` in Slackbot.

### ChatGPT

No known limitations for `tile/list` in ChatGPT.

### Agentforce

No known limitations for `tile/list` in Agentforce.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: List Tile](https://www.headlessexperiencelayer.com/#components/list)
