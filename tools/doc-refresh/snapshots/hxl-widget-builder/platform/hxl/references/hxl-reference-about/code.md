# Code

**`tile/code`**

Shows preformatted source code content with an optional language label.

## Properties

| Name     | Required | Lightning Type                 | Default | Description                                                                                            |
| -------- | -------- | ------------------------------ | ------- | ------------------------------------------------------------------------------------------------------ |
| code     | Yes      | `lightning__multilineTextType` |         | The source code text string, which includes any programming or markup language.                        |
| language | No       | `lightning__textType`          |         | A programming language identifier shown as a header label. For example: `javascript`, `python`, `sql`. |

## Usage

Display a block of preformatted source code in a monospace font, preserving whitespace, indentation, and line breaks exactly as written. Use `tile/code` to show a snippet, command, config file, or query.

:::note
For inline code within a sentence, use [`tile/text`](/docs/platform/hxl/references/hxl-reference-about/text.md) with `variant: "code"` instead. For rich-formatted content, use [`tile/markdown`](/docs/platform/hxl/references/hxl-reference-about/markdown.md) instead.
:::

Embed newlines as `\n` and include any indentation directly in the `code` string. Whitespace is preserved exactly as you entered it.

```json
{
    "definition": "tile/code",
    "attributes": {
        "code": "const greeting = 'Hello, World!';\nconsole.log(greeting);",
        "language": "javascript"
    }
}
```

When the snippet doesn't match a supported language, omit `language` to hide the header.

```json
{
    "definition": "tile/code",
    "attributes": {
        "code": "some_command --flag value\nanother_command | pipe_to_here"
    }
}
```

## Languages

Use the `language` attribute with these languages.

- `javascript`
- `typescript`
- `python`
- `java`
- `c`
- `cpp`
- `csharp`
- `go`
- `rust`
- `ruby`
- `php`
- `sql`
- `html`
- `css`
- `json`
- `yaml`
- `xml`
- `bash`
- `markdown`

Consider these guidelines when working with code.

- Set `language` to a lowercase identifier such as `"python"` or `"sql"`, so the header label appears.
- Code highlighting isn't supported.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/code` in Slackbot.

### ChatGPT

No known limitations for `tile/code` in ChatGPT.

### Agentforce

`language` isn't supported. The code block renders as monospace text without syntax highlighting.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Code](https://www.headlessexperiencelayer.com/#components/code)
