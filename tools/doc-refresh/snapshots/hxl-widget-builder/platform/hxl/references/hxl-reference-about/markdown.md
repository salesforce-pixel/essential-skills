# Markdown

**`tile/markdown`**

Shows Markdown-formatted text content, including headings, lists, links, images, code blocks, tables, and standard inline formatting.

## Properties

| Name   | Required | Lightning Type                | Default | Description                                                                                                               |
| ------ | -------- | ----------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------- |
| source | Yes      | `lightning__markdownTextType` |         | A raw Markdown text string. Use Markdown syntax for headings, links, lists, code blocks, tables, and standard formatting. |

## Usage

Render a block of markdown-formatted text — headings, emphasis, links, images, lists, code blocks, blockquotes, and GFM tables — from a single `source` string. Use markdown when you have rich, formatted text to display.

:::note
For preformatted source code or a fenced code block, use [`tile/code`](/docs/platform/hxl/references/hxl-reference-about/code.md) instead. For plain, unformatted text, use [`tile/text`](/docs/platform/hxl/references/hxl-reference-about/text.md) instead.
:::

Embed newlines as `\n` in the `source` string. Extra whitespace is removed from the formatted text.

```json
{
    "definition": "tile/markdown",
    "attributes": {
        "source": "# Heading\n\nSome **bold** and _italic_ text with a [link](https://example.com).\n\n- First item\n- Second item"
    }
}
```

To create a table, use standard CommonMark syntax or GitHub-flavored markdown.

```json
{
    "definition": "tile/markdown",
    "attributes": {
        "source": "| Tile | Status |\n| --- | --- |\n| Text | Beta |\n| Markdown | Beta |"
    }
}
```

Consider these guidelines when working with markdown.

- Task lists (`- [ ]`) aren't supported.
- Don't use inline HTML because some tags are removed from the output.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/markdown` in Slackbot.

### ChatGPT

No known limitations for `tile/markdown` in ChatGPT.

### Agentforce

No known limitations for `tile/markdown` in Agentforce.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Markdown](https://www.headlessexperiencelayer.com/#components/markdown)
