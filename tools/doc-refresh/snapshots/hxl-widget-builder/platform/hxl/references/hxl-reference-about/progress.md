# Progress

**`tile/progress`**

Indicates task completion as a percentage, shown as a linear bar or circular ring.

## Properties

| Name  | Required | Lightning Type          | Default   | Description                                                                                                                                                        |
| ----- | -------- | ----------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| color | No       | `lightning__textType`   | `default` | The semantic color for the progress fill. Valid values include `default`, `error`, `primary`, `success`, and `warning`.                                            |
| label | Yes      | `lightning__textType`   |           | The required text string for the progress indicator.                                                                                                               |
| max   | No       | `lightning__numberType` |           | A maximum value representing 100% completion. When omitted, the value is treated as a percentage.                                                                  |
| shape | No       | `lightning__textType`   | `linear`  | The shape for the progress indicator. Valid values include `linear` (default) for a horizontal bar, `circular` for a ring or arc.                                  |
| size  | Yes      | `lightning__sizeType`   |           | The size of the progress indicator. Valid values include `xs` for extra small, `sm` for small, `md` for medium (default), `lg` for large, or `xl` for extra large. |
| value | No       | `lightning__numberType` | 0         | The current progress value. To present a percentage (0-100), omit the max value. Or provide the max value to show the current amount toward that target value.     |

## Usage

Use a progress indicator to show how far along a task or process is, such as a file upload, an installation, or a quota toward a target. It renders a labeled bar or ring that fills to reflect the current `value`. The progress indicator is read-only; it reports status rather than collecting input.

:::note
For an indeterminate wait where progress can't be measured, use [`tile/spinner`](/docs/platform/hxl/references/hxl-reference-about/spinner.md) instead.
:::

To create a progress indicator, provide a `label` and a `value` from 0 to 100 as a percentage. Use a `label` that names the operation, such as "Uploading file", rather than restating the percentage.

```json
{
    "definition": "tile/progress",
    "attributes": {
        "label": "Uploading file",
        "value": 45
    }
}
```

To track progress toward a non-percentage target such as a quota or item count, set `max`. The indicator fill is then computed as `value` out of `max`.

```json
{
    "definition": "tile/progress",
    "attributes": {
        "label": "Sales quota",
        "value": 1500,
        "max": 2000,
        "size": "lg"
    }
}
```

To convey status, pair a `color` with the `value`. For example, set `color` to `success` when the task completes or `warning` as a limit approaches.

```json
{
    "definition": "tile/progress",
    "attributes": {
        "label": "Storage usage",
        "value": 85,
        "color": "warning"
    }
}
```

## Shape

Use `shape` to set the indicator's geometric form. Both shapes communicate the same value. Only the visual form differs.

- `linear` (default): A horizontal bar that fills left to right.
- `circular`: A ring or arc that fills clockwise, which is useful for compact spaces or overlay contexts where a bar doesn't fit.

## Size

Use `size` to set the indicator's thickness for a linear bar, or its diameter for a circular ring.

- `xs`: Extra small. Use `xs` to keep the indicator unobtrusive.
- `sm`: Small.
- `md` (default): Medium, which is suitable for most contexts.
- `lg`: Large, which gives an important or long-running task more presence.
- `xl`: Extra large, which creates a focal point when progress is the primary content.

## Color

Use `color` to set the semantic color of the progress fill. On surfaces that can't render semantic colors, the fill degrades to the default color.

- `default`: The default standard surface color with no specific status for ordinary, in-progress tasks.
- `error`: Indicates a failure or a critical threshold to reflect a problem state.
- `primary`: The brand or accent color to emphasize a featured task.
- `success`: Indicates positive completion when the task has finished successfully.
- `warning`: Indicates a caution state when a limit or threshold is approaching.

## Design Guidelines

Consider these guidelines when working with progress indicators.

- Omit `max` for a plain percentage; set it only when tracking progress toward a specific target.
- Use `color` to reinforce status, but don't rely on it alone as some surfaces render only the default fill.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/progress` in Slackbot.

### ChatGPT

No known limitations for `tile/progress` in ChatGPT.

### Agentforce

`color` is partially supported. Only `success` is native. `error` and `warning` use CSS overrides.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Progress](https://www.headlessexperiencelayer.com/#components/progress)
