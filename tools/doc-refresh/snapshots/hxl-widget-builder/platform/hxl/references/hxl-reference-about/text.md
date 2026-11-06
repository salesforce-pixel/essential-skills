# Text

**`tile/text`**

Shows text content with optional typography styling. Configure the appearance by using variant, weight, color, italic, and strikethrough settings.

## Properties

| Name            | Required | Lightning Type                 | Default   | Description                                                                                       |
| --------------- | -------- | ------------------------------ | --------- | ------------------------------------------------------------------------------------------------- |
| color           | No       | `lightning__textType`          | `default` | A semantic color for the text, which defaults to the surface's standard text color.               |
| isItalic        | No       | `lightning__booleanType`       | false     | Specifies whether the text is rendered in an italic style.                                        |
| isStrikethrough | No       | `lightning__booleanType`       | false     | Specifies whether the text is rendered with a strikethrough.                                      |
| text            | Yes      | `lightning__multilineTextType` |           | Plain text in a paragraph by default. Any inline markup or formatting syntax are removed.         |
| variant         | No       | `lightning__textType`          | `body`    | The semantic typography level to determine the heading level or text role. The default is `body`. |
| weight          | No       | `lightning__textType`          |           | The font weight for the text. Omit this setting to use the variant's default weight.              |

## Usage

Use `tile/text` for plain, styled text content or a simple string without markup.

:::note
For rich formatted content with markup, lists, or links, use [`tile/markdown`](/docs/platform/hxl/references/hxl-reference-about/markdown.md) instead.
:::

```json
{
    "definition": "tile/text",
    "attributes": {
        "text": "Your order has shipped."
    }
}
```

To specify a semantic role, use the `variant` attribute to specify a value for body text, code, or a heading level. You can also specify the font weight using the `weight` attribute.

```json
{
    "definition": "tile/text",
    "attributes": {
        "text": "Account balance",
        "variant": "h2",
        "weight": "semibold"
    }
}
```

## Variants

Use these `variant` values to express hierarchy or role. Styling on variants can vary across surfaces.

- `body` (default): Standard paragraph text
- `caption`: Small supplementary text
- `code`: Text that represents code, technical identifiers, or commands
- `h1`: The main heading on a page
- `h2`: The second heading
- `h3`: The third heading
- `h4`: The fourth heading
- `h5`: The fifth heading
- `h6`: The sixth heading

Consider these guidelines when working with text.

- Use `color` for semantic states like `error`, `success`, or `muted` instead of embedding presentational styling in the string.
- Use `isItalic` for emphasis and `isStrikethrough` for content that's superseded or deleted.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/text` in Slackbot.

### ChatGPT

No known limitations for `tile/text` in ChatGPT.

### Agentforce

No known limitations for `tile/text` in Agentforce.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Text](https://www.headlessexperiencelayer.com/#components/text)
