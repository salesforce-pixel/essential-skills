# Get Custom Labels with the Labels Extension

The `labels` extension is a Data SDK extension that reads custom labels from your org. Import it from `@salesforce/platform-sdk/data/extensions` and attach it to the SDK.

The `labels` extension requires Salesforce API version 64.0 or later. See [Minimum API Version](/docs/platform/multiframework/guide/data-sdk-extension-custom.md#set-a-minimum-api-version).

```typescript
import { createDataSDK } from "@salesforce/platform-sdk/data";
import { labels } from "@salesforce/platform-sdk/data/extensions";

const sdk = await createDataSDK({ extensions: [labels({ namespace: "MyApp" })] });

// Fall back to the label name when a label doesn't resolve
const greeting = (await sdk.ext.labels.get?.("greeting")) ?? "greeting";

// Override the configured options for a single call
const french = await sdk.ext.labels.get?.("greeting", { locale: "fr" });

// Resolve several labels in one batched load
const many = await sdk.ext.labels.getAll?.(["greeting", "farewell"]);
```

## labels(config?)

Creates the `labels` extension. Pass the optional `config` parameters to set default options for every call. Omit `config` to use the built-in defaults.

`config` is of type `LabelsOptions`.

## LabelsOptions

Sets where labels are read from and how they resolve. Supply these options when you configure the extension to set defaults, and again per call to override them for that call. Each field resolves independently as call value, then configured value, then built-in default.

| Parameter   | Type            | Description                                                                                                                                                                                                                                                                      |
| :---------- | :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `namespace` | `string`        | The custom-label namespace to read from. Omit it or pass an empty string to fall back per the precedence: in `labels()`, this falls back to the server's default namespace (`c`); per call, it falls back to the value configured in `labels()`, and then to the server default. |
| `locale`    | `string`        | The target locale, such as `fr` or `en-US`. Omit it or pass an empty string to fall back per the precedence: in `labels()`, this falls back to the logged-in user's locale; per call, it falls back to the value configured in `labels()`, and then to the user's locale.        |
| `fallback`  | `LabelFallback` | Specifies how the server resolves a label that has no translation for the requested locale. Defaults to `BASE_VALUE`.                                                                                                                                                            |

## LabelFallback

Sets how the server resolves a label that has no translation for the requested locale.

```typescript
type LabelFallback = "BASE_VALUE" | "USER_DEFAULT" | "NONE";
```

- `BASE_VALUE`—Returns the org-default (base) value. This is the default.
- `USER_DEFAULT`—Falls back to the logged-in user's language first, then the base value.
- `NONE`—Doesn't fall back. A label with no translation for the locale is treated as unresolved, so it's absent from the result.

## LabelsApi

The API returned under `sdk.ext.labels`. Both methods are optional and are absent on a surface whose Data SDK has no `graphql`. Use optional chaining (`sdk.ext.labels.get?.()`) to account for surfaces that don't support them.

### get()

Resolves a single label. Returns its value, or `undefined` if the server doesn't resolve it.

```typescript
get?(name: string, options?: LabelsOptions): Promise<string | undefined>;
```

| Parameter | Type            | Description                                             |
| :-------- | :-------------- | :------------------------------------------------------ |
| `name`    | `string`        | The developer name of the label to resolve.             |
| `options` | `LabelsOptions` | Optional. Per-call overrides of the configured options. |

Because an unresolved label returns `undefined`, provide your own fallback where you need one.

```typescript
const greeting = (await sdk.ext.labels.get?.("greeting")) ?? "greeting";
```

### getAll()

Resolves several labels in one batched load. Returns a map keyed only by the names that resolved. A name that doesn't resolve is absent from the map, which matches `get()` returning `undefined`.

```typescript
getAll?(names: readonly string[], options?: LabelsOptions): Promise<Record<string, string>>;
```

| Parameter | Type                | Description                                                                                                       |
| :-------- | :------------------ | :---------------------------------------------------------------------------------------------------------------- |
| `names`   | `readonly string[]` | The developer names of the labels to resolve. Names are deduped internally, so order and duplicates don't matter. |
| `options` | `LabelsOptions`     | Optional. Per-call overrides of the configured options.                                                           |

Use `getAll()` for a bounded label set, such as an app's manifest of dozens to low hundreds of labels. Names are split into batches of 100, the server's per-call limit, and fetched concurrently. If you expect to resolve thousands of labels at once, we recommend that you batch, cache, or throttle the calls in your own code.

## See Also

- [Data SDK Extensions](/docs/platform/multiframework/guide/data-sdk-extension.md)
- [Author a Custom Data SDK Extension](/docs/platform/multiframework/guide/data-sdk-extension-custom.md)
- [Work with Data SDK](/docs/platform/multiframework/guide/data-sdk-intro.md)
