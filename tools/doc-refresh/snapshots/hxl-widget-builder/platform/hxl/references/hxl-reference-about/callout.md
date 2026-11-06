# Callout

**`tile/callout`**

Highlights a content block for emphasis. The callout wraps child content with a semantic variant, optional title, and description.

## Properties

| Name        | Required | Lightning Type        | Default   | Description                                                                                                                                                                                                                                   |
| ----------- | -------- | --------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| description | No       | `lightning__textType` |           | The body text below the title.                                                                                                                                                                                                                |
| iconAlt     | No       | `lightning__textType` |           | Alternative text describing what the leading variant icon conveys. When omitted or empty, the icon is treated as decorative and hidden from assistive technologies.                                                                           |
| title       | Yes      | `lightning__textType` |           | The heading text for the callout block.                                                                                                                                                                                                       |
| variant     | No       | `lightning__textType` | `default` | Changes the appearance of the callout. Valid values include `default` for neutral, `error` for a critical issue, `info` for context, `note` for an aside, `success` for a positive outcome, `tip` for a suggestion, or `warning` for caution. |

## Usage

Use a callout to draw attention to a piece of information that stands apart from the surrounding content, such as a tip, a warning, or a confirmation. It renders a titled block with a colored border, background tint, and icon set by its `variant`.

:::note
A callout is a container, so it can wrap richer body content as child blocks. For a plain run of body text with no emphasis, use [`tile/text`](/docs/platform/hxl/references/hxl-reference-about/text.md) instead.
:::

To create a callout, set a short `title` and choose a `variant` that matches the message. Use `description` for a single line of supporting body text.

```json
{
    "definition": "tile/callout",
    "attributes": {
        "title": "Did you know?",
        "description": "This feature is available in all plans.",
        "variant": "info"
    }
}
```

To flag something that's critical, use the `warning` or `error` variant.

```json
{
    "definition": "tile/callout",
    "attributes": {
        "title": "Important Notice",
        "description": "This action cannot be undone.",
        "variant": "warning"
    }
}
```

For richer body content, omit `description` and provide child blocks instead. The children render below the title inside the callout.

```json
{
    "definition": "tile/callout",
    "attributes": {
        "title": "Additional Information",
        "variant": "note"
    },
    "children": [
        {
            "definition": "tile/text",
            "attributes": { "text": "Review the steps below before continuing." }
        }
    ]
}
```

## Variants

Use `variant` to set the callout's semantic category, which determines its color, background tint, and icon. On text-only surfaces, the variant is conveyed with a label prefix such as "Warning:" instead of color.

- `default`: The default neutral styling with no specific status.
- `error`: A critical failure or blocking issue, which shows something that went wrong and needs attention.
- `info`: Supplementary context or background, which adds helpful detail that isn't urgent.
- `note`: A general aside or clarification, which shows a remark that sits alongside the main content.
- `success`: A positive outcome or confirmation, which confirms that an action completed.
- `tip`: A helpful suggestion or best practice, which provides a recommendation for something.
- `warning`: A potential issue or caution, which notifies the user before they take a risky action.

## Design Guidelines

Consider these guidelines when working with callouts.

- Choose a `variant` that matches the message's tone as the variant carries the meaning even when color isn't available.
- Use `description` for a single line of body text, and switch to child blocks when the content needs structure such as a list or code.
- Reserve callouts for information that genuinely needs to stand out.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/callout` in Slackbot.

### ChatGPT

No known limitations for `tile/callout` in ChatGPT.

### Agentforce

No known limitations for `tile/callout` in Agentforce.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Callout](https://www.headlessexperiencelayer.com/#components/callout)
