# HXL Components

Headless Experience Layer (HXL) components are the building blocks that you compose into experiences. Each component defines a single piece of content or layout structure that you can combine. HXL renders each component natively on each supported channel.

:::note
For the beta release, HXL components are supported for Agentforce, ChatGPT, Claude, and Slackbot.
:::

The HXL component reference lists UI components you can use to build widgets. Use the reference to find the right component for your content, layout, or interaction. Review a component's page for its properties, known limitations, and usage examples.

For additional components that are in developer preview, see the [HXL Playground](https://www.headlessexperiencelayer.com/?tab=docs#components/). Developer preview components are for early access, and their APIs can still change. If you use developer preview components, we recommend that you use them in a sandbox org.

- [**Accordion**](/docs/platform/hxl/references/hxl-reference-about/accordion.md) (`tile/accordion`)

  Organizes content into vertically stacked, expandable sections. Each section has a header and nested content.

- [**Accordion Item**](/docs/platform/hxl/references/hxl-reference-about/accordionItem.md) (`tile/accordionItem`)

  Creates an individual expandable section within an accordion. Each section includes a clickable header with a title and optional icon.

- [**Avatar**](/docs/platform/hxl/references/hxl-reference-about/avatar.md) (`tile/avatar`)

  Identifies a user, entity, or object visually. An avatar contains the image URL, text initials, icon identifier, alternative text, shape, and size.

- [**Badge**](/docs/platform/hxl/references/hxl-reference-about/badge.md) (`tile/badge`)

  Presents a small inline indicator for categorization or status.

- [**Button**](/docs/platform/hxl/references/hxl-reference-about/button.md) (`tile/button`)

  Shows a clickable element that triggers an action. A button includes semantic and visual variants, optional icon decoration, and the loading state.

- [**Callout**](/docs/platform/hxl/references/hxl-reference-about/callout.md) (`tile/callout`)

  Highlights a content block for emphasis. The callout wraps child content with a semantic variant, optional title, and description.

- [**Code**](/docs/platform/hxl/references/hxl-reference-about/code.md) (`tile/code`)

  Shows preformatted source code content with an optional language label.

- [**Column**](/docs/platform/hxl/references/hxl-reference-about/column.md) (`tile/column`)

  Shows children components in a vertical container with a configurable gap, cross-axis alignment, and width.

- [**Container**](/docs/platform/hxl/references/hxl-reference-about/container.md) (`tile/container`)

  Creates a container with a rounded border that accepts any children.

- [**Icon**](/docs/platform/hxl/references/hxl-reference-about/icon.md) (`tile/icon`)

  Shows a standalone icon.

- [**Image**](/docs/platform/hxl/references/hxl-reference-about/image.md) (`tile/image`)

  Shows an image based on a source URL, a required alternative text for accessibility, and an optional size proxy.

- [**Link**](/docs/platform/hxl/references/hxl-reference-about/link.md) (`tile/link`)

  Shows a text-based hyperlink with a destination URL. Configure the visual style as needed.

- [**List**](/docs/platform/hxl/references/hxl-reference-about/list.md) (`tile/list`)

  Lists a series of related items in a column. Use the `tile/listitem` child component for a list item.

- [**List Item**](/docs/platform/hxl/references/hxl-reference-about/listItem.md) (`tile/listItem`)

  Adds a single row inside a list. Use these children components: `tile/text`, `tile/link`, or `tile/icon`.

- [**Markdown**](/docs/platform/hxl/references/hxl-reference-about/markdown.md) (`tile/markdown`)

  Shows markdown-formatted text content. Use headings, lists, links, images, code blocks, tables, and standard inline formatting.

- [**Progress**](/docs/platform/hxl/references/hxl-reference-about/progress.md) (`tile/progress`)

  Indicates the task completion percentage visually, which can be presented as a linear bar or circular ring shape.

- [**Row**](/docs/platform/hxl/references/hxl-reference-about/row.md) (`tile/row`)

  Shows children components in a horizontal container with a configurable gap, alignment, justification, and wrapping.

<!---->

- [**Separator**](/docs/platform/hxl/references/hxl-reference-about/separator.md) (`tile/separator`)

  Adds a visual boundary between content sections by using a horizontal or vertical line.

- [**Spacer**](/docs/platform/hxl/references/hxl-reference-about/spacer.md) (`tile/spacer`)

  Adds an empty layout element that creates explicit space or flexible fill between sibling components.

- [**Spinner**](/docs/platform/hxl/references/hxl-reference-about/spinner.md) (`tile/spinner`)

  Shows an indeterminate circular loading indicator. Configure the accessible label and an optional size setting on the spinner.

- [**Table**](/docs/platform/hxl/references/hxl-reference-about/table.md) (`tile/table`)

  Shows tabular data with column definitions and row data. Columns define the structure, and rows are key-value objects that map column keys to cell values.

- [**Text**](/docs/platform/hxl/references/hxl-reference-about/text.md) (`tile/text`)

  Shows text content with optional typography styling. Configure the appearance by using variant, weight, color, italic, and strikethrough settings.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [HXL Playground](ttps://www.headlessexperiencelayer.com/)
