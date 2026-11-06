# Accordion Item

**`tile/accordionItem`**

Creates an expandable section within an accordion. Each section has a clickable header with a title and optional icon.

## Properties

| Name       | Required | Lightning Type           | Default | Description                                                                                                                                                |
| ---------- | -------- | ------------------------ | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| iconAlt    | No       | `lightning__textType`    |         | Alternative text describing what the header icon conveys. When omitted or empty, the icon is treated as decorative and hidden from assistive technologies. |
| iconName   | No       | `lightning__iconName`    |         | An icon identifier shown in the section header next to the title.                                                                                          |
| isExpanded | No       | `lightning__booleanType` | false   | Specifies whether this section is currently expanded to show its content.                                                                                  |
| subtitle   | No       | `lightning__textType`    |         | Secondary text shown beneath the title in the accordion section header.                                                                                    |
| title      | Yes      | `lightning__textType`    |         | The header text for the clickable trigger on the accordion section.                                                                                        |

## Usage

Use an accordion item to define a section within a `tile/accordion`. Each item renders a clickable header with its `title`, optional `subtitle`, and optional `iconName`, and reveals its child content when expanded. Accordion items are only valid as direct children of a [`tile/accordion`](/docs/platform/hxl/references/hxl-reference-about/accordion.md).

```json
{
    "definition": "tile/accordion",
    "children": [
        {
            "definition": "tile/accordionItem",
            "attributes": { "title": "Shipping Details", "iconName": "settings" },
            "children": [
                {
                    "definition": "tile/text",
                    "attributes": { "text": "Standard shipping takes 5-7 business days." }
                }
            ]
        }
    ]
}
```

Add a `subtitle` to show secondary text under the title, useful for a short preview of the section's content.

```json
{
    "definition": "tile/accordionItem",
    "attributes": { "title": "Shipping Details", "subtitle": "Rates, timelines, and tracking" },
    "children": [
        {
            "definition": "tile/text",
            "attributes": { "text": "Standard shipping takes 5-7 business days." }
        }
    ]
}
```

To draw a section open on first render, set `isExpanded` to `true`.

```json
{
    "definition": "tile/accordionItem",
    "attributes": { "title": "Getting Started", "isExpanded": true },
    "children": [
        {
            "definition": "tile/text",
            "attributes": { "text": "Follow the steps below to get started." }
        }
    ]
}
```

To stack multiple pieces of content in one section, wrap them in a `tile/column`, and mix in components like `tile/badge` or `tile/button` for richer sections.

```json
{
    "definition": "tile/accordionItem",
    "attributes": { "title": "Beginner Level", "iconName": "star" },
    "children": [
        {
            "definition": "tile/column",
            "attributes": { "gap": "sm" },
            "children": [
                {
                    "definition": "tile/text",
                    "attributes": { "text": "Introduction to basic concepts." }
                },
                {
                    "definition": "tile/badge",
                    "attributes": { "label": "5 lessons", "variant": "info" }
                }
            ]
        }
    ]
}
```

## Design Guidelines

Consider these guidelines when working with accordion items.

- Keep each `title` concise and descriptive so users can scan headers and find the right section quickly.
- Use `subtitle` for a short, scannable preview of a section's content so users can decide whether to expand it without guessing from the title alone.
- To highlight the most important section, set `isExpanded` on it rather than leaving every section collapsed.
- Do not depend on whether opening one section collapses the others — each surface decides that expansion behavior, so use `isExpanded` only to seed the initial state.
- Add an `iconName` when a visual cue helps users recognize the section immediately, but omit it when titles are already clear.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/accordionItem` in Slackbot.

### ChatGPT

No known limitations for `tile/accordionItem` in ChatGPT.

### Agentforce

No known limitations for `tile/accordionItem` in Agentforce.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Accordion Item](https://www.headlessexperiencelayer.com/#components/accordionItem)
