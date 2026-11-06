# Spinner

**`tile/spinner`**

Shows an indeterminate circular loading indicator. Configure the accessible label and an optional size.

## Properties

| Name  | Required | Lightning Type        | Default | Description                                                                                                                                             |
| ----- | -------- | --------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| label | Yes      | `lightning__textType` |         | The accessible text that identifies the operation that's in progress.                                                                                   |
| size  | No       | `lightning__textType` | `md`    | The size of the spinner. Valid values include `xs` for extra small, `sm` for small, `md` for medium (default), `lg` for large, or `xl` for extra large. |

## Usage

Use a spinner to show an indeterminate loading indicator for an operation whose duration or completion can't be measured, such as a network request, a page load, or server processing. The spinner renders a circular animation without a percentage.

:::note
For measurable progress such as uploads or multi-step flows, use [`tile/progress`](/docs/platform/hxl/references/hxl-reference-about/progress.md) instead.
:::

Provide a `label` describing what's loading so the operation is announced to assistive technology.

```json
{
    "definition": "tile/spinner",
    "attributes": { "label": "Loading results" }
}
```

To pair a spinner with status text, place both in a row.

```json
{
    "definition": "tile/row",
    "attributes": { "gap": "sm" },
    "children": [
        {
            "definition": "tile/spinner",
            "attributes": { "size": "sm", "label": "Saving changes" }
        },
        {
            "definition": "tile/text",
            "attributes": { "text": "Saving changes…" }
        }
    ]
}
```

## Size

Use these `size` values to set the spinner's relative scale. The default is `md`.

- `xs`: Extra small spinner for inline or compact contexts such as inside a button or a form field.
- `sm`: Small spinner for inline or alongside short status text.
- `md` (default): Medium spinner for standard, in-content loading.
- `lg`: Large spinner for prominent or section-level loading.
- `xl`: Extra large spinner for page-level loading indicators.

## Design Guidelines

Consider these guidelines when working with spinners.

- Set a concise, action-oriented `label` such as "Loading results" or "Processing payment".
- Use a small spinner (`xs` or `sm`) next to buttons or form fields, and a larger size (`lg` or `xl`) for page- or section-level loading.
- Avoid placing multiple spinners in the same view — a single loading indicator reads more clearly than several competing animations.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/spinner` in Slackbot.

### ChatGPT

No known limitations for `tile/spinner` in ChatGPT.

### Agentforce

`size: xl` renders the same as `size: lg`. SLDS provides four spinner sizes only.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Spinner](https://www.headlessexperiencelayer.com/#components/spinner)
