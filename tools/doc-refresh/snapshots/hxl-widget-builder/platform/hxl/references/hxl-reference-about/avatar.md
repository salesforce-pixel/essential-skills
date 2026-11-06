# Avatar

**`tile/avatar`**

Identifies a user, entity, or object visually. An avatar contains the image URL, text initials, icon name, alternative text, shape, and size.

## Properties

| Name     | Required | Lightning Type        | Default  | Description                                                                                                                                                              |
| -------- | -------- | --------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| alt      | No       | `lightning__textType` |          | An alternative text that identifies the entity. Maximum 125 characters, HTML-encoded.                                                                                    |
| iconName | No       | `lightning__iconName` |          | A semantic icon identifier representing the entity, appearing when image URL and initials are absent. For example: `user`, `users`, `building`.                          |
| initials | No       | `lightning__textType` |          | An abbreviation string up to 2 characters. Use Unicode characters up to a maximum of 3 characters. For example: `JD` for `John Doe`, `AM` for `Amazon`, `+5` for groups. |
| shape    | No       | `lightning__textType` | `circle` | The shape that indicates the entity category. Valid values include `circle` for people, `square` for objects or organizations, or `rounded` for hybrid entities.         |
| size     | No       | `lightning__textType` | `md`     | The size of the avatar. Valid values include `xs` for extra small, `sm` for small, `md` for medium (default), `lg` for large, or `xl` for extra large.                   |
| src      | No       | `lightning__urlType`  |          | The absolute or relative image URL, URL-encoded, referencing a JPEG, PNG, WebP, SVG, or GIF file.                                                                        |

## Usage

Use an avatar to display a visual identifier for a person, organization, or entity. Provide at least one of `src`, `initials`, or `iconName`. The avatar prioritizes the `src` value. If `src` and `iconName` are missing, the `initials` value is shown.

Use `shape` to signal entity category: `"circle"` (default) for people, `"square"` for organizations or objects, `"rounded"` for hybrid entities such as AI assistants or teams.

```json
{
    "definition": "tile/avatar",
    "attributes": {
        "src": "https://www.example.com/photo.jpg",
        "alt": "Sarah Johnson"
    }
}
```

When no image is available, use `initials` to provide a visible fallback.

```json
{
    "definition": "tile/avatar",
    "attributes": {
        "initials": "SJ",
        "alt": "Sarah Johnson"
    }
}
```

To build a user identity header that places an avatar next to a name, combine `tile/avatar` with `tile/text` inside a `tile/row`.

```json
{
    "definition": "tile/row",
    "attributes": { "align": "center", "gap": "sm" },
    "children": [
        {
            "definition": "tile/avatar",
            "attributes": {
                "initials": "SJ",
                "alt": "Sarah Johnson"
            }
        },
        {
            "definition": "tile/text",
            "attributes": { "text": "Sarah Johnson" }
        }
    ]
}
```

:::note
`tile/avatar` has the same image source and format restrictions as `tile/image`.
Additionally, the `src` attribute must reference a resource that's accessible without authentication. To enable access to the resource, add the domain as a trusted URL. For more information, see [Use Static Resources in Widgets](https://developer.salesforce.com/docs/platform/hxl/guide/hxl-widget-composition.md#use-static-resources-in-widgets).
:::

## Size

Use these `size` values to control the avatar's dimensions.

- `xs`: Extra small avatars for dense lists or inline mentions alongside text.
- `sm`: Small avatars for compact rows and secondary contexts.
- `md` (default): Medium avatars for most standalone and labeled uses.
- `lg`: Large avatars for profile headers and prominent identity displays.
- `xl`: Extra large avatars for a hero or focal identity such as a profile page.

## Design Guidelines

Consider these guidelines when working with avatars.

- Omit `shape` for people to use the default circle; set `shape: "square"` for organizations or objects, and `shape: "rounded"` for AI assistants or teams.
- Provide a meaningful `alt` value such as a user's first and last name. Use an empty string only for decorative avatars.
- Provide `initials` alongside `src` as a text fallback for when the image fails to load.
- Use `iconName: "users"` for groups and `iconName: "building"` for organizations when neither an image nor initials are available.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/avatar` in Slackbot.

### ChatGPT

No known limitations for `tile/avatar` in ChatGPT.

### Agentforce

`size: xl` falls back to `large`. `shape: rounded` falls back to `square` with custom CSS.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Avatar](https://www.headlessexperiencelayer.com/#components/avatar)
