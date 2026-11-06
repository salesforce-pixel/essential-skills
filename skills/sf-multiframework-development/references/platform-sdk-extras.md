# Extensions, custom labels, app identity, View SDK, i18n

Sources: `data-sdk-extension`, `data-sdk-extension-label`, `data-sdk-extension-custom`, `data-sdk-identity`, `data-sdk-view`, `data-sdk-i18n`.

Import paths as the docs show them:
- `createDataSDK`, `gql`: `@salesforce/platform-sdk/data`
- `labels`: `@salesforce/platform-sdk/data/extensions`
- `defineDataExtension`, `getCurrentApp`, `createViewSDK`, `getViewSDK`, `getViewSDKSync`, type `ThemeMode`: `@salesforce/platform-sdk`
- i18n: `@salesforce/platform-sdk/i18n`

If one doesn't resolve, check the installed package's `exports` / `.d.ts`.

## Extensions

An extension is a named, self-contained API attached at runtime: you pass it to `createDataSDK({ extensions: [...] })` and use it as `sdk.ext.<name>`. LWC `@salesforce/*` modules are resolved at compile time; extensions are chosen per SDK instance and shared as ordinary code.

Pass the `extensions` array **inline** so `sdk.ext` is typed. If you assign it to a variable first, add `as const`.

### `labels` (custom labels, API ≥ 64.0)

```typescript
import { createDataSDK } from "@salesforce/platform-sdk/data";
import { labels } from "@salesforce/platform-sdk/data/extensions";

const sdk = await createDataSDK({ extensions: [labels({ namespace: "MyApp" })] });

const greeting = (await sdk.ext.labels.get?.("greeting")) ?? "greeting"; // unresolved → undefined
const french = await sdk.ext.labels.get?.("greeting", { locale: "fr" });  // per-call override
const many = await sdk.ext.labels.getAll?.(["greeting", "farewell"]);      // Record<name, value>, unresolved names absent
```

`LabelsOptions` (in `labels(config)` as defaults and per call as overrides; each field resolves call → configured → built-in):

| Field | Default | Notes |
|---|---|---|
| `namespace` | server default `c` | `""` or omitted falls back |
| `locale` | logged-in user's locale | e.g. `fr`, `en-US` |
| `fallback` | `BASE_VALUE` | `LabelFallback` |

`type LabelFallback = "BASE_VALUE" | "USER_DEFAULT" | "NONE"`: org base value / user's language then base / no fallback (label absent).

API: `get?(name, options?) => Promise<string | undefined>`, `getAll?(names, options?) => Promise<Record<string, string>>`. Both are absent on surfaces without `graphql`, so call them with `?.`. `getAll` dedupes names, splits into batches of 100 (server limit) and fetches them concurrently. Fine for dozens to low hundreds; batch, cache or throttle yourself for thousands.

### Custom extension: `defineDataExtension`

```typescript
import { createDataSDK } from "@salesforce/platform-sdk/data";
import { defineDataExtension, type DataSDK } from "@salesforce/platform-sdk";

interface AccountApi {
  getName?(recordId: string): Promise<string | undefined>;
}

interface AccountNameResult {
  uiapi: { query: { Account: { edges: { node: { Name: { value: string } } }[] } } };
}

const accountExtension = defineDataExtension({
  name: "account",
  setup: (sdk: DataSDK): AccountApi => {
    // GraphQL isn't on every surface: omit the method instead of failing at call time
    const graphql = sdk.graphql;
    if (!graphql) return {};
    return {
      async getName(recordId) {
        const result = await graphql.query<AccountNameResult>({
          query: GET_ACCOUNT_NAME,
          variables: { recordId },
        });
        return result?.data?.uiapi.query.Account.edges[0]?.node.Name.value;
      },
    };
  },
});

const sdk = await createDataSDK({ extensions: [accountExtension] });
const name = await sdk.ext.account.getName?.("001xx000003DGb2AAG");
```

| Field | Type | Description |
|---|---|---|
| `name` | string | Key under `sdk.ext` (must be a literal; duplicates rejected at compile time) |
| `setup` | `(sdk: DataSDK) => Api \| Promise<Api>` | Runs at `createDataSDK()`; may be async (dynamic import, a query) |
| `minApiVersion` | string, optional | e.g. `"64.0"`. If the resolved API version is lower, `createDataSDK()` **rejects and attaches none of the extensions**. Skipped if the runtime supplies no version. Separate from runtime capability checks (`graphql`/`fetch` presence) |

Name collision → alias: `extensions: [labels({ namespace: "MyApp" }), { extension: partnerLabels, as: "partnerLabels" }]` → `sdk.ext.partnerLabels.get?.(...)`.

Uses: wrap repeated queries, a caching layer, an API client or telemetry behind one typed namespace, kept apart from SDK changes.

## App identity: `getCurrentApp()`

```typescript
import { getCurrentApp } from "@salesforce/platform-sdk";

const app = await getCurrentApp(); // never rejects; options?: CurrentAppOptions (surface override)
if (app.identity) {
  const targetIds = [app.identity.qualifiedName]; // ["MyNs__MyBundle"]
}
```

```typescript
interface CurrentApp { readonly identity?: AppIdentity } // undefined in local dev or when appName is missing
interface AppIdentity {
  namespace: string;      // "c" without a registered namespace
  appName: string;        // UI bundle developer name
  qualifiedName: string;  // namespace__appName
  bundleId?: string;      // UIBundle record id; undefined in local dev
}
```

Use it to scope calls to the app (e.g. CMS search) or to pass the app's addressable name. Read `bundleId` with a fallback (`app.identity?.bundleId ?? ""`). Call `getCurrentApp()` where you need it; don't cache it in a context/provider.

React hook pattern: resolve it in `useEffect` with a `cancelled` flag so an unmounted component doesn't set state, and fall back when `identity?.bundleId` is missing.

## View SDK (host UI)

The host is whatever embeds the bundle (a parent LWC via UI Embedding, an agent host, …).

```typescript
import { createViewSDK, getViewSDK, getViewSDKSync } from "@salesforce/platform-sdk";

const viewSDK = await createViewSDK();     // never rejects; empty SDK when there's no host
await viewSDK.displayToast?.({ message: "Operation completed successfully", level: "success" });

const shared = await getViewSDK();         // cached singleton; only the first call's options apply
const maybe = getViewSDKSync();            // instance or null if getViewSDK() hasn't finished
```

Every method is optional; always call with `?.`.

| Method | Signature / notes |
|---|---|
| `displayAlert` | `({ message, level? }) => Promise<void>`; blocking modal; `level`: `info` (default) / `success` / `warning` / `error` |
| `displayToast` | same options; non-blocking, auto-dismiss |
| `displayModal` | `({ componentReference: "ui://widget/[name].html", params? })` custom HTML from a UI resource |
| `navigateTo` | `(url) => Promise<void>`; full-page or iframe navigation depending on surface |
| `markDirtyState` | `(label?)`: unsaved changes; host can warn before navigation; labels track multiple regions |
| `clearDirtyState` | `(label?)`: pass the same label |
| `getUiState` | `() => { state: { props, styles }, subscribe(handler) => unsubscribe }`. `props` = host inputs (theme, locale, mode); `styles` = CSS custom properties/attributes mirrored onto the surface. Generic `<State extends UiState>` (type-only) |
| `getTheme` | `() => Theme \| null`. The table says it returns `light`/`dark`; the example reads `theme.mode` (see `sources.md`) |
| `resize` | `(width, height)`: CSS lengths or `"auto"` |
| `addEventListener` / `removeEventListener` / `dispatchEvent` | Optional `EventTarget`. With a host bridge, `dispatchEvent` reaches local listeners **and** the host; host pushes are re-dispatched on the SDK |

```typescript
form.addEventListener("input", () => viewSDK.markDirtyState?.("PrimaryForm"));
async function saveForm(data) {
  await api.save(data);
  await viewSDK.clearDirtyState?.("PrimaryForm");
}

const { state, subscribe } = viewSDK.getUiState?.() ?? {
  state: { props: {}, styles: {} },
  subscribe: () => () => {},
};
applyProps(state.props);
const unsubscribe = subscribe((next) => applyProps(next.props));

viewSDK.addEventListener?.("user-action", (e) => console.log((e as CustomEvent).detail));
viewSDK.dispatchEvent?.(new CustomEvent("user-action", { detail: { action: "click" } }));

await viewSDK.resize?.("800px", "600px");
```

Host-theme hook:

```typescript
import { useEffect, useState } from "react";
import { createViewSDK, type ThemeMode } from "@salesforce/platform-sdk";

function useHostTheme(): ThemeMode {
  const [mode, setMode] = useState<ThemeMode>("light");
  useEffect(() => {
    let cancelled = false;
    let unsubscribe: (() => void) | undefined;
    createViewSDK().then((viewSDK) => {
      if (cancelled) return;
      const initial = viewSDK.getTheme?.();
      if (initial) setMode(initial.mode);
      unsubscribe = viewSDK.getUiState?.()?.subscribe((next) => {
        const themeMode = next.props.theme;
        if (themeMode === "light" || themeMode === "dark") setMode(themeMode);
      });
    });
    return () => { cancelled = true; unsubscribe?.(); };
  }, []);
  return mode;
}
```

## i18n (API ≥ 68.0; context fetched over GraphQL only)

Format dates, numbers and currency by the user's **Salesforce** locale, not the browser's.

```typescript
import { createDataSDK } from "@salesforce/platform-sdk/data";
import { fetchI18nContext, createI18nFormatters } from "@salesforce/platform-sdk/i18n";

const dataSdk = await createDataSDK();
const ctx = await fetchI18nContext(dataSdk);  // cached for the page lifetime; rejects without GraphQL
const { formatDate, formatNumber, formatCurrency } = createI18nFormatters(ctx); // sync

formatDate(new Date());
formatDate(new Date(), { dateStyle: "full" });   // per-call Intl options merged last
formatNumber(1234567.89);
formatCurrency(1000);                            // org currency from ctx
formatCurrency(1000, { currency: "EUR" });       // throws if neither ctx nor options give a currency
```

```typescript
interface I18nContext {
  lang: string;     // translation language, e.g. "en"
  locale: string;   // BCP 47 formatting locale, e.g. "en-GB" (region decides date order, grouping)
  dir: string;      // "ltr" | "rtl"
  currency: string; // org currency, e.g. "USD" (may differ from the locale's region)
  timeZone: string; // e.g. "America/Los_Angeles"
}
```

Formatters use `ctx.locale` (not `lang`): `formatDate` uses locale + timeZone, `formatNumber` uses locale, `formatCurrency` uses locale + currency.

- `reloadI18nContext(dataSdk)`: clears the cache and re-queries after an in-session locale change. The cache is cleared first, so on failure it rejects and leaves the context empty. Handle the rejection.
- Labels with `{0}`/`{1}` placeholders: pre-format numbers/dates with the formatters and pass strings (raw values get `toString()`).
- `createSalesforceDetector(dataSdk)`: i18next language-detector, reports `ctx.lang`, only after `fetchI18nContext` has resolved.

### i18next backend: `SalesforceBackend`

```typescript
import { createDataSDK } from "@salesforce/platform-sdk/data";
import { SalesforceBackend } from "@salesforce/platform-sdk/i18n";
import i18next from "i18next";

const dataSDK = await createDataSDK();
await i18next.use(SalesforceBackend).init({
  defaultNS: "c", // org custom-label namespace
  backend: {
    dataSDK,
    labelManifest: ["c:Welcome_Text", "c:Save_Button"],
  },
  interpolation: { prefix: "{", suffix: "}" }, // Salesforce labels use {0}, {1}
});
```

`SalesforceBackendOptions`: `dataSDK` (required), `labelManifest?: string[]` (`"namespace:Key"`; unlisted labels aren't fetched), `labelFallback?: LabelFallback` (default `BASE_VALUE`). Entries are grouped by namespace, deduped and batched by 100. Unresolved labels are omitted, so i18next shows its key fallback. On orgs below API 68.0 labels don't resolve and the raw keys render. `platform-sdk` has no hard dependency on i18next.
