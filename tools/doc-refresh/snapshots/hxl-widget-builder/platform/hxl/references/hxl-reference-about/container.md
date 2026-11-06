# Container

**`tile/container`**

Creates a container with a rounded border that accepts any children.

## Properties

| Name       | Required | Lightning Type           | Default   | Description                                       |
| ---------- | -------- | ------------------------ | --------- | ------------------------------------------------- |
| borderless | No       | `lightning__booleanType` | false     | Specifies whether the container omits its border. |
| variant    | No       | `lightning__textType`    | `default` | Sets the visual variant of the container.         |

## Usage

Use a container to group related children inside a rounded, padded border. The container provides a card-like frame that visually separates a block of content from surrounding content.

To control layout in a container, use [`tile/column`](/docs/platform/hxl/references/hxl-reference-about/column.md) or [`tile/row`](/docs/platform/hxl/references/hxl-reference-about/row.md). Wrap children content in a `tile/column` for vertical stacking or a `tile/row` for a horizontal arrangement. Use the `gap` attribute to space them.

```json
{
    "definition": "tile/container",
    "children": [
        {
            "definition": "tile/column",
            "attributes": { "gap": "sm" },
            "children": [
                {
                    "definition": "tile/text",
                    "attributes": { "text": "Container", "variant": "h2" }
                },
                {
                    "definition": "tile/text",
                    "attributes": { "text": "A framed region that groups related content." }
                },
                {
                    "definition": "tile/button",
                    "attributes": { "label": "Action", "variant": "primary" }
                }
            ]
        }
    ]
}
```

:::note
For grouping that needs no frame at all, use a `tile/column` or `tile/row` directly instead of a borderless container.
:::

To remove the border on the container, set `borderless` to `true`.

```json
{
    "definition": "tile/container",
    "attributes": { "borderless": true },
    "children": [
        {
            "definition": "tile/text",
            "attributes": { "text": "A flat, frameless region." }
        }
    ]
}
```

## Variant

Set `variant` to tint the container's fill. Use it to group or emphasize a region, or to signal status. The default is `default`, which matches the surrounding background (no fill).

| Value      | Appearance                                            | Use for                                         |
| ---------- | ----------------------------------------------------- | ----------------------------------------------- |
| `default`  | Matches the surrounding background (no fill)          | The normal, unemphasized case                   |
| `emphasis` | A subtle neutral shade, slightly darker than the page | Setting a region apart without a status meaning |
| `info`     | Blue                                                  | Informational or in-progress content            |
| `warning`  | Yellow                                                | Cautions the user should notice                 |
| `error`    | Red                                                   | Problems or destructive context                 |
| `success`  | Green                                                 | Confirmations or completed states               |

The four status colors (`info`, `warning`, `error`, `success`) also tint the border to match the fill.

```json
{
    "definition": "tile/container",
    "attributes": { "variant": "info" },
    "children": [
        {
            "definition": "tile/text",
            "attributes": { "text": "Your changes are still syncing." }
        }
    ]
}
```

## Design Guidelines

Consider these guidelines when working with containers.

- To arrange the children inside, nest a `tile/column` or `tile/row` rather than relying on the container itself.
- Set `borderless` to `true` when a container is nested inside another framed surface, so the borders don't stack and compete.
- Avoid deeply nesting framed containers. Stacked borders and padding crowd the content in smaller screens.
- Reach for a status `variant` (`info`, `warning`, `error`, `success`) only when the color carries meaning — and always convey that meaning in the container's text content (e.g. a `tile/text` heading like "Warning" or "Completed with errors"), never through color alone (WCAG 2.2 SC 1.4.1, Use of Color). For a single titled status message with an icon, prefer `tile/callout`; use a tinted container to frame a broader region of content.
- Use `emphasis` for a neutral emphasis that groups content without implying a status.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/container` in Slackbot.

### ChatGPT

No known limitations for `tile/container` in ChatGPT.

### Agentforce

No known limitations for `tile/container` in Agentforce.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Container](https://www.headlessexperiencelayer.com/#components/container)
