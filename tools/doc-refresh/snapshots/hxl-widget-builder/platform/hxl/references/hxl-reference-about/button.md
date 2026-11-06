# Button

**`tile/button`**

Shows a clickable element that triggers an action. A button includes semantic and visual variants, optional icon decoration, and the loading state.

## Properties

| Name     | Required | Lightning Type        | Default   | Description                                                                                                                                                        |
| -------- | -------- | --------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| actions  | No       | `lightning__textType` |           | Actions invoked by user interaction, keyed by event name.                                                                                                          |
| iconName | No       | `lightning__iconName` |           | A semantic icon identifier shown next to the label.                                                                                                                |
| label    | Yes      | `lightning__textType` |           | The required text string for the button.                                                                                                                           |
| variant  | No       | `lightning__textType` | `primary` | Changes the appearance of the button. Valid values include `primary` for main actions, `secondary` for supporting actions, or `destructive` for dangerous actions. |

## Usage

Use a button for a user-initiated action. For the main call-to-action, use the `primary` variant. Use the `secondary` variant for supporting actions, and `destructive` for irreversible or dangerous actions. Avoid placing two primary buttons side by side.

:::note
To create a link for navigation, use [`tile/link`](/docs/platform/hxl/references/hxl-reference-about/link.md) instead.
:::

To reinforce the action, add an `iconName`. The value is an identifier such as `edit`, `trash`, or `plus`, which maps to an icon on each surface.

```json
{
    "definition": "tile/button",
    "attributes": { "label": "Delete", "variant": "destructive", "iconName": "trash" }
}
```

To lay out multiple buttons horizontally, wrap the buttons with [`tile/row`](/docs/platform/hxl/references/hxl-reference-about/row.md).

```json
{
    "definition": "tile/row",
    "attributes": { "gap": "sm" },
    "children": [
        {
            "definition": "tile/button",
            "attributes": { "label": "Save", "variant": "primary" }
        },
        {
            "definition": "tile/button",
            "attributes": { "label": "Cancel", "variant": "secondary" }
        }
    ]
}
```

## Variants

Use these `variant` values to convey the button's role and emphasis.

- `primary` (default): The main call-to-action in a view, such as "Save" or "Submit". Use one primary button per group of actions.
- `secondary`: A supporting action paired alongside a primary button, such as "Cancel" next to "Save".
- `destructive`: An irreversible or dangerous action, such as deleting a record or canceling a subscription.

## Design Guidelines

Consider these guidelines when working with buttons.

- Keep labels short and action-oriented, for example, "Save" or "Send Message".
- Pick an `iconName` that reinforces the label rather than replaces it; the label is always required, even for icon-led buttons.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/button` in Slackbot.

### ChatGPT

No known limitations for `tile/button` in ChatGPT.

### Agentforce

No known limitations for `tile/button` in Agentforce.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Button](https://www.headlessexperiencelayer.com/#components/button)
