# Image

**`tile/image`**

Shows an image from a source URL, with required alternative text for accessibility and an optional size.

## Properties

| Name | Required | Lightning Type        | Default | Description                                                                                                                            |
| ---- | -------- | --------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| alt  | Yes      | `lightning__textType` |         | An alternative text that describes the image content for accessibility. Maximum 125 characters; an empty string for decorative images. |
| size | No       | `lightning__textType` | `auto`  | The size of the image. Valid values include `auto`, `sm`, `md`, `lg`, or `full`.                                                       |
| src  | Yes      | `lightning__urlType`  |         | The absolute or relative image URL, URL-encoded.                                                                                       |

## Usage

Use an image to display a graphic referenced by a URL, such as a photo, illustration, diagram, or logo.

:::note
For a circular profile photo of a user or entity, use [`tile/avatar`](/docs/platform/hxl/references/hxl-reference-about/avatar.md) instead.
:::

Set `src` to the image URL and always provide `alt` text that describes the content for accessibility.

```json
{
    "definition": "tile/image",
    "attributes": {
        "src": "https://cdn.example.com/photo.jpg",
        "alt": "Bar chart showing Q3 revenue by region"
    }
}
```

Use `size` to control the image footprint. For a purely decorative image that conveys no information, set `alt` to an empty string so assistive technologies skip it.

```json
{
    "definition": "tile/image",
    "attributes": {
        "src": "https://cdn.example.com/banner.jpg",
        "alt": "",
        "size": "full"
    }
}
```

## Image Source

The `src` attribute must reference a resource that's accessible without authentication. To enable access to the resource, add the domain as a trusted URL. For more information, see [Use Static Resources in Widgets](https://developer.salesforce.com/docs/platform/hxl/guide/hxl-widget-composition.md#use-static-resources-in-widgets).

## Image Format

Consider these valid and invalid image types.

Valid image formats include:

- PNG
- JPEG
- GIF
- WebP

Invalid image types include:

- Vector and active content, such as `image/svg+xml`
- Non-image MIME types, such as `text/html`, `text/plain`, `application/octet-stream`, `image/bmp`, or omitted media types

### Image Schemes

`data:` scheme isn't supported when used in a link (href) context. To pass URL validation, use the `data:` scheme by following these guidelines.

### Format Requirements

Follow the `data:<mediatype>;base64,<payload>` syntax. The `;base64` flag is mandatory. Plain-text or raw URL-encoded data is rejected.

### Magic-Byte Signature Matching

The decoded leading bytes must match the magic bytes of the declared MIME type. For example, PNG header corresponds to `89 50 4E 47`, JPEG header `FF D8 FF`, GIF header `GIF8`, or WebP `RIFF....WEBP`.

### Decoded Size Cap

Payload must be within an 8 MiB decoded size limit (`MAX_DATA_IMAGE_BYTES`) to prevent memory amplification attacks.

### No Dynamic Expressions

Unresolved template expressions, such as `{!expr}` in either the media-type or payload slots aren't supported.

## Size

Use these `size` values to control the image footprint. The aspect ratio is always preserved. The width is fixed and the height scales to match.

- `auto` (default): Preserves the image's intrinsic dimensions.
- `sm`: Small fixed width for thumbnails and inline graphics.
- `md`: Medium fixed width for standalone images within a block of content.
- `lg`: Large fixed width for prominent, focal images.
- `full`: Fills the parent container's width, for banners and hero images.

## Design Guidelines

Consider these guidelines when working with images.

- Set `alt` to an empty string only for decorative, redundant, or structural images.
- Specify `full` to span the parent width, and `auto` when the image's own dimensions are already correct.
- Don't depend on a fixed height. The height always scales from the width to preserve the aspect ratio.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/image` in Slackbot.

### ChatGPT

No known limitations for `tile/image` in ChatGPT.

### Agentforce

No known limitations for `tile/image` in Agentforce.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Image](https://www.headlessexperiencelayer.com/#components/image)
