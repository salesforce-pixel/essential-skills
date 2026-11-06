# Accordion

**`tile/accordion`**

Organizes content into vertically stacked, expandable sections. Each section has a header and nested content.

## Properties

This component has no configurable properties. Provide content through child components.

## Usage

Use an accordion to organize content into vertically stacked, expandable sections to reduce visual clutter on dense screens. An accordion has no attributes of its own. To provide content in an accordion, use [`tile/accordionItem`](/docs/platform/hxl/references/hxl-reference-about/accordionItem.md) child components.

```json
{
    "definition": "tile/accordion",
    "children": [
        {
            "definition": "tile/accordionItem",
            "attributes": { "title": "What is your refund policy?" },
            "children": [
                {
                    "definition": "tile/text",
                    "attributes": {
                        "text": "We offer a 30-day money-back guarantee on all purchases."
                    }
                }
            ]
        },
        {
            "definition": "tile/accordionItem",
            "attributes": { "title": "How long does shipping take?" },
            "children": [
                {
                    "definition": "tile/text",
                    "attributes": {
                        "text": "Standard shipping typically takes 5-7 business days."
                    }
                }
            ]
        }
    ]
}
```

To draw attention to the first section, open it by default with `isExpanded` and add an `iconName` for a visual cue in the header.

```json
{
    "definition": "tile/accordion",
    "children": [
        {
            "definition": "tile/accordionItem",
            "attributes": { "title": "Getting Started", "isExpanded": true, "iconName": "star" },
            "children": [
                {
                    "definition": "tile/text",
                    "attributes": { "text": "Follow the steps below to get started." }
                }
            ]
        },
        {
            "definition": "tile/accordionItem",
            "attributes": { "title": "Advanced Topics", "iconName": "settings" },
            "children": [
                {
                    "definition": "tile/text",
                    "attributes": { "text": "Explore more complex features and customizations." }
                }
            ]
        }
    ]
}
```

For richer sections, wrap multiple pieces in a `tile/column` to stack them, and mix in `tile/badge` or `tile/button`.

```json
{
    "definition": "tile/accordionItem",
    "attributes": { "title": "Product Features", "iconName": "heart" },
    "children": [
        {
            "definition": "tile/column",
            "attributes": { "gap": "sm" },
            "children": [
                {
                    "definition": "tile/text",
                    "attributes": { "text": "High-quality materials" }
                },
                {
                    "definition": "tile/badge",
                    "attributes": { "label": "New", "variant": "info" }
                }
            ]
        }
    ]
}
```

## Design Guidelines

Consider these guidelines when working with accordions.

- Keep section titles concise and descriptive so users can scan headers to find what they need.
- To surface the most important section immediately, set `isExpanded` on one item rather than leaving every section collapsed.
- Sections expand and collapse independently, so more than one can be open at once. Use per-item `isExpanded` to seed which sections start open.
- When content should always be visible or is short enough not to warrant collapsing, use a `tile/column` instead of hiding it behind an accordion.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/accordion` in Slackbot.

### ChatGPT

No known limitations for `tile/accordion` in ChatGPT.

### Agentforce

No known limitations for `tile/accordion` in Agentforce.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Accordion](https://www.headlessexperiencelayer.com/#components/accordion)
