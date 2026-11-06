# Link

**`tile/link`**

Shows a text-based hyperlink with a destination URL. Configure the visual style as needed.

## Properties

| Name      | Required | Lightning Type        | Default   | Description                                                                                                                                                          |
| --------- | -------- | --------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| href      | Yes      | `lightning__urlType`  |           | The required absolute or relative URL string for the link destination.                                                                                               |
| text      | No       | `lightning__textType` |           | Plain text for the link. When omitted, the URL is used as the text.                                                                                                  |
| underline | No       | `lightning__textType` | `hover`   | The underline style for the link. Valid values include `always` for persistent underline, `hover` (default) for on-hover only, or `none` for no underline.           |
| variant   | No       | `lightning__textType` | `primary` | Changes the appearance of the link. Valid values include `default` for standard text, `muted` for de-emphasized text, or `primary` for brand-colored text (default). |

## Usage

Use a link to send a user to a URL destination, whether an external site or an in-app route. The link renders inline clickable text styled as a hyperlink.

:::note
For an action that runs logic rather than navigating to a URL, use `tile/button` instead.
:::

To provide a label, use the `text` attribute. For example, provide a concise action phrase such as "View pricing details", instead of a generic phrase such as "Click here".

```json
{
    "definition": "tile/link",
    "attributes": {
        "text": "View pricing details",
        "href": "https://example.com/pricing"
    }
}
```

To change the emphasis of the link, use the `variant` and `underline` attributes. For example, de-emphasize the link with the `muted` variant.

```json
{
    "definition": "tile/link",
    "attributes": {
        "text": "Terms of Service",
        "href": "/terms",
        "variant": "muted",
        "underline": "none"
    }
}
```

## Variants

Use these `variant` values to control the link's color and emphasis.

- `primary` (default): The brand accent color, for calls to action and prominent navigation.
- `default`: Inherits the surrounding text color, so the link blends into body copy and reads as running text.
- `muted`: A subdued, secondary color for supplementary or footer links that shouldn't compete with primary content.

## Underline

Use these `underline` values to control when the link's underline appears.

- `always`: Persistent underline, the traditional web-link style. Use `always` when a link sits in dense text and must be identifiable without relying on color.
- `hover` (default): Underline appears only on hover, for a cleaner default appearance.
- `none`: No underline. The link is distinguished by color alone. Use for navigation menus or styled link lists where the link role is already obvious.

## Opening in a new tab

Links always open in a new browser tab. To warn users of this context change (WCAG 3.2.2), the tile automatically appends a visible "opens in new tab" icon for sighted users and an "(opens in new tab)" cue on the accessible name for screen-reader users. You don't need to add either cue yourself — in particular, don't place your own `open-in-new` icon next to a link.

## Design Guidelines

Consider these guidelines when working with links.

- Use the `muted` variant on supplementary or footer links so they don't compete with primary content.
- Set `underline` to `always` when a link sits inside dense body text and must be identifiable without relying on color.
- Don't add an "opens in new tab" icon or phrase next to a link — the tile provides both cues automatically.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/link` in Slackbot.

### ChatGPT

No known limitations for `tile/link` in ChatGPT.

### Agentforce

`variant` and `underline` aren't supported.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Link](https://www.headlessexperiencelayer.com/#components/link)
