# Table

**`tile/table`**

Shows tabular data with column definitions and row data. Columns define structure (key, header, alignment). Rows are key-value objects mapping column keys to cell values.

## Properties

| Name           | Required | Lightning Type           | Default   | Description                                                                                                                                                        |
| -------------- | -------- | ------------------------ | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| appearance     | No       | `lightning__textType`    | `default` | The visual style for the table. Valid values include `default` for standard, `bordered` for emphasized cell borders, or `striped` for alternating row backgrounds. |
| caption        | Yes      | `lightning__textType`    |           | Accessible description of the table content and purpose.                                                                                                           |
| columns        | Yes      | `lightning__listType`    |           | Defines the column with a key (data field identifier), header (display text), and optional alignment. The column order determines the display order.               |
| isStickyHeader | No       | `lightning__booleanType` | false     | Specifies whether the header row remains fixed at the top during vertical scrolling.                                                                               |
| pagination     | No       | `lightning__objectType`  |           | Optional pagination configuration. When provided, the table shows pagination controls and one page of data at a time.                                              |
| rows           | Yes      | `lightning__listType`    |           | Array of data objects. Each object's keys correspond to column key values; values are cell content strings.                                                        |
| size           | No       | `lightning__textType`    | `md`      | The cell density for the table. Valid values include `sm` for compact, or `md` (default) for standard.                                                             |
| sort           | No       | `lightning__objectType`  |           | Initial sort state identifying a column key and direction. When present, a sort indicator appears in the column header.                                            |

## Usage

Use a table to present structured data across rows and columns, such as a list of records, a price sheet, or a status report.

Define the shape with `columns`. Each column has a `key` that maps to a field in the row data and a `header` for the display label. Provide the data as `rows`, where each object's keys match the column keys. Always set `caption` to describe the table's contents for accessibility.

```json
{
    "definition": "tile/table",
    "attributes": {
        "columns": [
            { "key": "name", "header": "Name" },
            { "key": "email", "header": "Email" },
            { "key": "role", "header": "Role" }
        ],
        "rows": [
            { "name": "John Doe", "email": "john@example.com", "role": "Admin" },
            { "name": "Jane Smith", "email": "jane@example.com", "role": "User" }
        ],
        "caption": "Employee contact information"
    }
}
```

To render a column as something other than plain text, set its `columnType` value as described in the [Column Type](#column-type) section. Right-align numeric columns with `align` so the digits line up.

```json
{
    "definition": "tile/table",
    "attributes": {
        "columns": [
            { "key": "id", "header": "ID" },
            { "key": "product", "header": "Product" },
            {
                "key": "price",
                "header": "Price",
                "align": "right",
                "columnType": {
                    "type": "number",
                    "format": "currency",
                    "currencyCode": "USD",
                    "minimumFractionDigits": 2
                }
            }
        ],
        "rows": [
            { "id": "1", "product": "Widget A", "price": 29.99 },
            { "id": "2", "product": "Widget B", "price": 39.99 }
        ],
        "caption": "Product price list",
        "appearance": "striped"
    }
}
```

To break a long data set into pages, add `pagination` with a `pageSize`.

```json
{
    "definition": "tile/table",
    "attributes": {
        "columns": [{ "key": "name", "header": "Name" }],
        "rows": [],
        "caption": "Team members",
        "pagination": { "pageSize": 20 }
    }
}
```

To keep column headers visible while the body scrolls, set `isStickyHeader` to `true`.

```json
{
    "definition": "tile/table",
    "attributes": {
        "columns": [{ "key": "name", "header": "Name" }],
        "rows": [],
        "caption": "Team members",
        "isStickyHeader": true
    }
}
```

To show which column the data is sorted by, set `sort` to a `{ key, direction }` object, and mark columns `isSortable` so users can re-sort by clicking a header.

```json
{
    "definition": "tile/table",
    "attributes": {
        "columns": [
            { "key": "name", "header": "Name", "isSortable": true },
            { "key": "createdDate", "header": "Created", "isSortable": true }
        ],
        "rows": [],
        "caption": "Records",
        "sort": { "key": "createdDate", "direction": "desc" }
    }
}
```

To enable row filtering, mark columns `isFilterable`, which adds each one to a filter panel with an input matched to its type: text search for text and link columns, a dropdown for picklist columns, a min-max range for number columns, and a date range for date columns.

```json
{
    "definition": "tile/table",
    "attributes": {
        "columns": [
            { "key": "name", "header": "Name", "isFilterable": true },
            {
                "key": "status",
                "header": "Status",
                "isFilterable": true,
                "columnType": {
                    "type": "picklist",
                    "options": [
                        { "label": "Open", "value": "open" },
                        { "label": "Closed", "value": "closed" }
                    ]
                }
            }
        ],
        "rows": [],
        "caption": "Support tickets"
    }
}
```

## Column Type

Set the `columnType` on a column to render its cells as something other than plain text. If you don't set `columnType`, cells render as plain text by default.

- `date`: Formats ISO 8601 date strings or numeric timestamps as localized dates or datetimes. Control the output with `format`, `dateStyle`, and `timeStyle`.
- `link`: Renders cell values as clickable hyperlinks. Set `urlKey` to point at a separate row field for the URL when the display text and the URL destination differ. Otherwise, the cell value serves as both.
- `number`: Formats numeric values with locale-aware `decimal`, `percent`, or `currency` formatting, and sorts numerically rather than lexicographically. Currency accepts `currencyCode` and `currencyDisplayAs`. Set fraction digits with `minimumFractionDigits` and `maximumFractionDigits`.
- `picklist`: Resolves stored row values to human-readable labels from a defined set of `options`, each a `{ label, value }` pair. A value with no matching option falls back to the raw value.

## Appearance

Use these `appearance` values to control the table's border and row treatment.

- `default` (default): Standard presentation with minimal horizontal row dividers, for most tables.
- `bordered`: Emphasized borders on all cell edges. Use `bordered` for dense data where clear cell boundaries aid readability.
- `striped`: Alternating row background colors. Use `striped` for wide tables where the shading helps readers track across a row.

## Size

Use these `size` values to control the cell density.

- `sm`: Compact cell padding for space-constrained contexts such as chat, or for dense data that fits more rows at once.
- `md` (default): Standard, comfortable cell padding for most tables.

## Design Guidelines

Consider these guidelines when working with tables.

- Always write a `caption` that names what the table contains, such as "Open support tickets," which identifies its purpose.
- Match each column `key` to a field present in every row. A key with no matching field renders as an empty cell.
- Right-align numeric columns with `align: "right"` so decimal points line up, and reserve `center` for short categorical values.
- Use `pagination` and `isStickyHeader` on long data sets, so the table stays scannable rather than overwhelming the surface.

## Limitations

Note any limitations that apply to this component.

### Slackbot

No known limitations for `tile/table` in Slackbot.

### ChatGPT

No known limitations for `tile/table` in ChatGPT.

### Agentforce

Per-column `isSortable` and `isFilterable` properties require imperative handlers. `pagination` is handled via manual data slicing rather than a built-in control.

## See Also

- [HXL Lightning Types Reference](/docs/platform/hxl/references/hxl-reference-about/hxl-lightning-types.md)
- [*HXL Playground*: Table](https://www.headlessexperiencelayer.com/#components/table)
