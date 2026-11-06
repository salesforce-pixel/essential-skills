# Icon

**`tile/icon`**

Shows a standalone icon.

## Properties

| Name  | Required | Lightning Type        | Default   | Description                                                                                                                                                                                                                 |
| ----- | -------- | --------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| alt   | No       | `lightning__textType` |           | An alternative text that describes what the icon conveys, for accessibility. Recommended to be concise (under 125 characters); an empty string (the default) marks the icon as decorative and hides it from screen readers. |
| color | No       | `lightning__textType` | `default` | The color of the icon. Valid values include `default`, `error`, `muted`, `primary`, `success`, and `warning`.                                                                                                               |
| name  | Yes      | `lightning__iconName` |           | A semantic icon identifier specifying which icon symbol to show.                                                                                                                                                            |
| size  | No       | `lightning__textType` | `md`      | The size of the icon. Valid values include `xs` for extra small, `sm` for small, `md` for medium (default), `lg` for large, and `xl` for extra large.                                                                       |

## Usage

Use an icon to show a standalone symbol that conveys meaning instantly, such as with a status indicator, a visual cue next to a label, or a lightweight decorative mark. Set `name` to choose the symbol, and use `size` and `color` to fit it to its context.

```json
{
    "definition": "tile/icon",
    "attributes": { "name": "check-circle", "color": "success" }
}
```

To label an icon, place both in a [`tile/row`](/docs/platform/hxl/references/hxl-reference-about/row.md) and align them on the center axis.

```json
{
    "definition": "tile/row",
    "attributes": { "gap": "sm", "align": "center" },
    "children": [
        {
            "definition": "tile/icon",
            "attributes": { "name": "alert-triangle", "color": "warning" }
        },
        {
            "definition": "tile/text",
            "attributes": { "text": "Your trial ends in 3 days." }
        }
    ]
}
```

For available icons, see the [HXL Playground Editor](https://www.headlessexperiencelayer.com/playground/?renderer=acc\&theme=slack#components/icon/all-icons).

## Size

Use these `size` values to control the icon size.

- `xs`: Extra small icons for dense inline contexts where the icon accompanies small text.
- `sm`: Small icons for compact rows and secondary cues.
- `md` (default): Medium icons for most standalone and labeled uses.
- `lg`: Large icons for emphasis or when the icon is a focal point.
- `xl`: Extra large icons for hero-style or feature callouts where the icon leads.

## Color

Use these `color` values to convey status or match the icon to its surrounding context.

- `default` (default): Neutral foreground color for decorative or non-status icons.
- `error`: Signals a failure or destructive state, such as a validation error.
- `muted`: Subdued, low-emphasis color for secondary or supporting cues.
- `primary`: The brand accent color to highlight a key icon.
- `success`: Signals a positive or completed state, such as a confirmation.
- `warning`: Signals caution or a state that requires attention.

## Design Guidelines

Consider these guidelines when working with icons.

- Match `color` to meaning — use `success`, `warning`, and `error` for status and reserve `default` or `muted` for decorative marks.
- Pair an icon with a `tile/text` label when the symbol alone can be ambiguous. Wrap both in a `tile/row`.
- Keep `size` consistent with neighboring text so the icon aligns to the line rather than towering over it.
- To make an icon trigger an action, attach the base `action` attribute instead of using a `tile/button`.
- On surfaces with a limited icon set, choose common, well-known `name` values so they don't fall back to a generic symbol.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/icon` in Slackbot.

### ChatGPT

No known limitations for `tile/icon` in ChatGPT.

### Agentforce

No known limitations for `tile/icon` in Agentforce. `name` maps to an SLDS styled icon.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Icon](https://www.headlessexperiencelayer.com/#components/icon)
