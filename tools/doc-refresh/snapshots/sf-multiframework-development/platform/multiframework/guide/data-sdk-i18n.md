# Localize Your App

Get the logged-in user's Salesforce locale context from the `i18n` module. With locale-aware formatters, the dates, numbers, and currency in your web app follow the user's Salesforce Locale setting instead of the browser default.

To localize your app, import the locale context and formatters from `@salesforce/platform-sdk/i18n`.

```typescript
import { createDataSDK } from "@salesforce/platform-sdk/data";
import { fetchI18nContext, createI18nFormatters } from "@salesforce/platform-sdk/i18n";

const dataSdk = await createDataSDK();

// Resolve the user's locale context, then build formatters bound to it
const ctx = await fetchI18nContext(dataSdk);
const { formatDate, formatNumber, formatCurrency } = createI18nFormatters(ctx);

formatDate(new Date()); // returns the formatted date based on the user's locale
formatNumber(1234567.89); // grouped per the user's locale
formatCurrency(1000); // uses the org currency from the context
```

The i18n context is fetched over GraphQL only.

The i18n runtime requires Salesforce API version 68.0 or later.

| Export                     | Type             | Description                                                                                  |
| :------------------------- | :--------------- | :------------------------------------------------------------------------------------------- |
| `fetchI18nContext`         | `async function` | Resolves the user's locale context over GraphQL and caches it for the page                   |
| `reloadI18nContext`        | `async function` | Clears the cached context and re-queries it, for in-session locale changes                   |
| `createI18nFormatters`     | `function`       | Builds locale-aware date, number, and currency formatters bound to a resolved context        |
| `createSalesforceDetector` | `function`       | Builds a language detector that reports the resolved language, for use with i18next          |
| `SalesforceBackend`        | `class`          | An i18next backend plugin that fetches your custom labels over GraphQL, for use with i18next |
| `SalesforceBackendOptions` | `interface`      | The options passed to `SalesforceBackend` (Data SDK, label manifest, fallback strategy)      |
| `LabelFallback`            | `type`           | How the server resolves a label with no translation for the requested locale                 |
| `I18nContext`              | `interface`      | The resolved locale context (`lang`, `locale`, `dir`, `currency`, `timeZone`)                |
| `I18nFormatters`           | `interface`      | The set of formatting functions returned by `createI18nFormatters`                           |

## I18nContext Interface

The resolved locale context for the logged-in user.

```typescript
interface I18nContext {
  lang: string;
  locale: string;
  dir: string;
  currency: string;
  timeZone: string;
}
```

| Property   | Type     | Description                                                                                                                                                                                                                                                           |
| :--------- | :------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `lang`     | `string` | The translation language, such as `en`, which is used to resolve translated text.                                                                                                                                                                                     |
| `locale`   | `string` | The formatting locale as a BCP 47 tag, such as `en-US` or `en-GB`, which is used for formatting. It carries the region that decides date order and digit grouping. A user can share a language but differ in locale, for example `lang: "en"` with `locale: "en-GB"`. |
| `dir`      | `string` | The text direction, such as `ltr` or `rtl`.                                                                                                                                                                                                                           |
| `currency` | `string` | The org's currency code, such as `USD`. The currency tracks the org setting and can differ from the locale's region.                                                                                                                                                  |
| `timeZone` | `string` | The user's time zone, such as `America/Los_Angeles`.                                                                                                                                                                                                                  |

## fetchI18nContext(dataSDK)

Resolves the logged-in user's locale context over GraphQL. The context is cached for the lifetime of the page, so repeated calls return the same value without re-querying. To re-query after an in-session locale change, use [`reloadI18nContext`](#reloadi18ncontextdatasdk) with a Data SDK instance. If the surface has no GraphQL support, the returned promise rejects.

```typescript
function fetchI18nContext(dataSDK: DataSDK): Promise<I18nContext>;
```

## reloadI18nContext(dataSDK)

Clears the cached context and immediately re-queries the platform, resolving to the fresh context. Because the context is cached for the lifetime of the page, a locale change otherwise takes effect only on a full page reload. Call this after an in-session locale change with a Data SDK instance. If the surface has no GraphQL support, the returned promise rejects.

```typescript
function reloadI18nContext(dataSDK: DataSDK): Promise<I18nContext>;
```

:::note
The cache is cleared before the re-query runs. If the re-query fails, the returned promise rejects and the context is left empty until a later successful fetch. Handle rejection rather than assume a reload always repopulates the context.
:::

## createI18nFormatters(ctx)

Builds locale-aware formatters bound to a resolved [`I18nContext`](#i18ncontext-interface). This factory is synchronous and takes an already-fetched context, so call [`fetchI18nContext`](#fetchi18ncontextdatasdk) first.

The formatters are built from `ctx.locale`, the formatting axis, not `ctx.lang`, the translation axis. Each formatter derives its defaults from the context:

- `formatDate` uses the locale and the time zone.
- `formatNumber` uses the locale.
- `formatCurrency` uses the locale and the currency.

To override a default, pass options for that call. The options you pass are merged last.

```typescript
function createI18nFormatters(ctx: I18nContext): I18nFormatters;
```

`I18nContext` is the resolved context to format against. Locale, currency, and time zone are read from it as defaults.

### I18nFormatters Interface

```typescript
interface I18nFormatters {
  formatDate(value: Date | number, options?: Intl.DateTimeFormatOptions): string;
  formatNumber(value: number, options?: Intl.NumberFormatOptions): string;
  formatCurrency(value: number, options?: Intl.NumberFormatOptions): string;
}
```

| Method                            | Description                                                                                                                                                                                                                                                  |
| :-------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `formatDate(value, options?)`     | Formats a `Date` or timestamp using the context's locale and time zone. Pass `Intl.DateTimeFormatOptions` to override the defaults for a call.                                                                                                               |
| `formatNumber(value, options?)`   | Formats a number using the context's locale. Pass `Intl.NumberFormatOptions` to override the defaults for a call.                                                                                                                                            |
| `formatCurrency(value, options?)` | Formats a number as currency using the context's locale and currency. Pass a `currency` in `Intl.NumberFormatOptions` to override the context's currency for a call. If neither the context nor the options supply a currency code, `formatCurrency` throws. |

```typescript
const ctx = await fetchI18nContext(dataSdk);
const { formatDate, formatCurrency } = createI18nFormatters(ctx);

// Use the context defaults
formatDate(new Date());

// Override per call
formatDate(new Date(), { dateStyle: "full" });
formatCurrency(1000, { currency: "EUR" });
```

:::note
The formatters are separate from label text. If a label uses positional placeholders (`{0}`, `{1}`), substituting a raw `Date` or number inserts its default `toString()`, not a locale-aware value. To interpolate a localized number or date, format it with `createI18nFormatters` first and pass the resulting string as the placeholder value.
:::

## createSalesforceDetector(dataSDK)

Builds a language detector that reports the resolved language (`I18nContext.lang`). The returned object is structurally compatible with the i18next language-detector plugin slot, so you can pass it to i18next's `.use()` if your app uses i18next for translations. The detector reports the language only after a context has been resolved with [`fetchI18nContext`](#fetchi18ncontextdatasdk).

```typescript
function createSalesforceDetector(dataSDK: DataSDK): LanguageDetectorModule;
```

## SalesforceBackend

An [i18next](https://www.i18next.com) backend plugin that fetches your org's custom labels over GraphQL at runtime and hands them to i18next to render. Use `SalesforceBackend` when your app translates UI text with i18next. Register it as an i18next backend and give it the list of labels your app uses.

The class is structurally compatible with i18next's backend plugin slot, so you pass it to i18next's `backend` configuration. `platform-sdk` does not take a hard dependency on i18next.

```typescript
import { createDataSDK } from "@salesforce/platform-sdk/data";
import { SalesforceBackend } from "@salesforce/platform-sdk/i18n";
import i18next from "i18next";

const dataSDK = await createDataSDK();

await i18next.use(SalesforceBackend).init({
  defaultNS: "c", // "c" is your org's custom-label namespace
  backend: {
    dataSDK,
    labelManifest: ["c:Welcome_Text", "c:Save_Button"],
  },
  interpolation: {
    // Salesforce labels interpolate with {0}, {1}, … — map i18next to that syntax
    prefix: "{",
    suffix: "}",
  },
});
```

The backend reads the label manifest, groups the entries by namespace, deduplicates the names, and fetches them over GraphQL. A namespace with more than 100 labels is split into batches automatically, so your manifest can list any number of labels without extra configuration. A label whose value doesn't resolve is left out of the result, so the i18n library falls back to its own key-name fallback for that key.

The label runtime path requires Salesforce API version 68.0 or later. On an earlier org, labels don't resolve and the affected text renders as its raw key name.

### SalesforceBackendOptions

The options object passed to `SalesforceBackend` through i18next's `backend` configuration.

```typescript
interface SalesforceBackendOptions {
  dataSDK: DataSDK;
  labelManifest?: string[];
  labelFallback?: LabelFallback;
}
```

| Property        | Type            | Description                                                                                                                                                            |
| :-------------- | :-------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dataSDK`       | `DataSDK`       | The Data SDK instance whose GraphQL surface fetches the labels.                                                                                                        |
| `labelManifest` | `string[]`      | The labels your app uses, each as `"namespace:Key"` (for example `"c:Welcome_Text"`). `c` is your org's custom-label namespace. Labels not listed here aren't fetched. |
| `labelFallback` | `LabelFallback` | How the server resolves a label with no translation for the requested locale. Defaults to `BASE_VALUE`.                                                                |

### LabelFallback

Sets how the server resolves a label that has no translation for the requested locale.

```typescript
type LabelFallback = "BASE_VALUE" | "USER_DEFAULT" | "NONE";
```

- `BASE_VALUE`—Returns the org-default (base) value. This is the default.
- `USER_DEFAULT`—Falls back to the logged-in user's language first, then the base value.
- `NONE`—Doesn't fall back. A label with no translation for the locale is left unresolved and is absent from the result.

## See Also

- [Work with Data SDK](/docs/platform/multiframework/guide/data-sdk-intro.md)
- [Get Custom Labels](/docs/platform/multiframework/guide/data-sdk-extension-label.md)
