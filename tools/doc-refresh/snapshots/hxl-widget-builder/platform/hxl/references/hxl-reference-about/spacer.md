# Spacer

**`tile/spacer`**

Adds an empty layout element that creates explicit space or flexible fill between sibling components.

## Properties

| Name | Required | Lightning Type        | Default | Description                                                                                                                                                                                 |
| ---- | -------- | --------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| size | No       | `lightning__textType` | `md`    | The amount of space to insert between content sections. Valid values include `xs` through `xl` for fixed sizes, `fill` to grow and consume remaining space. The default is `md` for medium. |

## Usage

Use a spacer to add explicit, invisible space between sibling components, or to push siblings apart so they sit at opposite edges of their container. A spacer is purely a layout element with no visible appearance and no semantic meaning.

:::note
For even spacing applied to every child at once, set `gap` on the parent [`tile/row`](/docs/platform/hxl/references/hxl-reference-about/row.md) or [`tile/column`](/docs/platform/hxl/references/hxl-reference-about/column.md) instead of inserting spacers between them. To add space with a visible dividing line, use [`tile/separator`](/docs/platform/hxl/references/hxl-reference-about/separator.md).
:::

A spacer expands along the parent's main axis, which results in horizontal spacing inside a row, and vertical spacing inside a column.

To add a fixed amount of vertical space between stacked components, use `tile/spacer` as a child of `tile/column`.

```json
{
    "definition": "tile/column",
    "attributes": { "gap": "none" },
    "children": [
        { "definition": "tile/text", "attributes": { "text": "Account details" } },
        { "definition": "tile/spacer", "attributes": { "size": "lg" } },
        { "definition": "tile/text", "attributes": { "text": "Billing details" } }
    ]
}
```

To pin one component to the start and another to the end of a row, place a `fill` spacer between them.

```json
{
    "definition": "tile/row",
    "attributes": { "align": "center" },
    "children": [
        { "definition": "tile/text", "attributes": { "text": "Page Title", "variant": "h3" } },
        { "definition": "tile/spacer", "attributes": { "size": "fill" } },
        { "definition": "tile/button", "attributes": { "label": "Action" } }
    ]
}
```

## Size

Use `size` to control how much space the spacer occupies. Each renderer maps the fixed sizes to its own spacing scale, so exact pixel amounts vary across surfaces.

- `xs`: Extra small fixed space. Use for the tightest separation between closely related elements.
- `sm`: Small fixed space.
- `md` (default): Medium fixed space, the default.
- `lg`: Large fixed space.
- `xl`: Extra large fixed space. Use to set apart major sections.
- `fill`: Grows to consume all remaining space in the parent, pushing adjacent siblings to opposite edges. Multiple `fill` spacers in the same parent share the remaining space equally. For example, placing one on each side of an element centers it.

## Design Guidelines

Consider these guidelines when working with spacers.

- For uniform spacing between all child content, use `gap` on the `tile/row` or `tile/column` parent container.
- Use a spacer for spacing or for `fill` behavior that `gap` can't express.
- Use `size: fill` to push siblings to opposite edges of a row or column rather than guessing a fixed size that only works at one width.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/spacer` in Slackbot.

### ChatGPT

No known limitations for `tile/spacer` in ChatGPT.

### Agentforce

No known limitations for `tile/spacer` in Agentforce.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Spacer](https://www.headlessexperiencelayer.com/#components/spacer)
