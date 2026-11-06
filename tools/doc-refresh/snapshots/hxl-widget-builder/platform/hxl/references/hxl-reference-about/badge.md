# Badge

**`tile/badge`**

Presents a small inline indicator for categorization or status.

## Properties

| Name    | Required | Lightning Type        | Default     | Description                             |
| ------- | -------- | --------------------- | ----------- | --------------------------------------- |
| label   | Yes      | `lightning__textType` |             | Short text content for the badge.       |
| variant | No       | `lightning__textType` | `secondary` | Visual style and status classification. |

## Usage

Use a badge to display a short inline label for categorization or status. For semantic states such as a record's health or pipeline stage, use a status variant such as `success`, `warning`, `error`, or `info`.

:::note
Avoid using a badge for interactive elements. To create a clickable label, use [`tile/button`](/docs/platform/hxl/references/hxl-reference-about/button.md) or [`tile/link`](/docs/platform/hxl/references/hxl-reference-about/link.md) instead.
:::

To create a badge, provide a short label. A label without a variant displays the badge in the default style.

```json
{
    "definition": "tile/badge",
    "attributes": {
        "label": "Basic",
        "variant": "success"
    }
}
```

To present the badge with a different style, use the `variant` attribute. For example, use `"variant": "success"` to convey a positive status.

```json
{
    "definition": "tile/badge",
    "attributes": {
        "label": "Active",
        "variant": "success"
    }
}
```

To annotate a name or title with a status label, place `tile/badge` inline with `tile/text` in a `tile/row`.

```json
{
    "definition": "tile/row",
    "attributes": { "align": "center", "gap": "sm" },
    "children": [
        {
            "definition": "tile/text",
            "attributes": { "text": "Acme Corp" }
        },
        {
            "definition": "tile/badge",
            "attributes": { "label": "New", "variant": "primary" }
        }
    ]
}
```

## Variants

Use these `variant` values to express different badge states.

- `error`: Indicates an urgent or critical status.
- `info`: Indicates informational status that's useful for supplemental items.
- `outline`: Indicates a subtle status to describe items that are less prominent but helpful.
- `primary`: Indicates non-urgent information for general statuses that don't require immediate attention.
- `secondary` (default): Indicates a neutral label without status emphasis, for general categorization and tags.
- `success`: Indicates a positive status to highlight successful actions or items.
- `warning`: Indicates a cautionary or advisory status to represent items that need action or review but aren't critical.

Consider these guidelines when working with badges.

- Keep labels short. Use one or two words to convey the intent of the badge. Consider using [`tile/text`](/docs/platform/hxl/references/hxl-reference-about/text.md) for longer text.
- Use status variants (`"success"`, `"warning"`, `"error"`, `"info"`) only when the label communicates a meaningful state, not for decorative color.
- Use `"primary"` for high-emphasis labels such as "New" or "Featured"; use `"outline"` for a subtle bordered appearance.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/badge` in Slackbot.

### ChatGPT

No known limitations for `tile/badge` in ChatGPT.

### Agentforce

Semantic `variant` colors rely on SLDS styling hooks. Without the styling hooks, badges fall back to the default gray styling.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Badge](https://www.headlessexperiencelayer.com/#components/badge)
