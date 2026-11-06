# List Item

**`tile/listItem`**

Adds a single row inside a list. Use these child components: `tile/text`, `tile/link`, or `tile/icon`.

## Properties

This component has no configurable properties. Provide content through child components.

## Usage

Use a list item for a single row inside a `tile/list`. It carries the row's content with text, links, and icons while the parent list owns the spacing and markers. A list item has no attributes of its own. It shows content provided by its children.

:::note
Put the list item inside a [`tile/list`](/docs/platform/hxl/references/hxl-reference-about/list.md). Markers and density come from the parent list, not the item.
:::

```json
{
    "definition": "tile/list",
    "children": [
        {
            "definition": "tile/listItem",
            "children": [
                {
                    "definition": "tile/text",
                    "attributes": { "text": "Item content" }
                }
            ]
        }
    ]
}
```

A list item can hold several children to combine an icon, text, and a link in one row.

```json
{
    "definition": "tile/listItem",
    "children": [
        {
            "definition": "tile/icon",
            "attributes": { "name": "info", "size": "sm" }
        },
        {
            "definition": "tile/text",
            "attributes": { "text": "See the documentation for details: " }
        },
        {
            "definition": "tile/link",
            "attributes": { "text": "Read more", "href": "https://example.com" }
        }
    ]
}
```

## Design Guidelines

Consider these guidelines when working with list items.

- Compose each row from `tile/text`, `tile/link`, and `tile/icon` children rather than putting content directly on the item.
- To make a whole row clickable, attach an action to the item rather than wrapping its contents in a separate control.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/listItem` in Slackbot.

### ChatGPT

No known limitations for `tile/listItem` in ChatGPT.

### Agentforce

No known limitations for `tile/listItem` in Agentforce.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: List Item](https://www.headlessexperiencelayer.com/#components/listItem)
