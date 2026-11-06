# Package Your App for Distribution

You can distribute a Multi-Framework app as a second-generation package (2GP), which wraps your UIBundle and its related metadata into a single, versioned artifact that you install into a subscriber org, upgrade in place, and uninstall.

## What You Can Package

Both package types support internal, employee-facing (B2E) apps built with React or Angular. Packaging is unsupported for external-facing (B2B and B2C) apps.

Choose a package type based on how you distribute the app.

- Use unlocked packages for internal distribution, proofs of concept, and rapid iteration.
- Use managed packages for listing on AppExchange or customer distribution.

For a full comparison of the two types, including namespaces, component editability, and AppExchange eligibility, see [Second-Generation Managed Packages](https://developer.salesforce.com/docs/platform/pkg2-dev/guide/sfdx-dev-dev2gp.md) and [Unlocked Packages](https://developer.salesforce.com/docs/platform/pkg2-dev/guide/sfdx-dev-unlocked-pkg-intro.md) in the packaging guide.

## Prepare Your UIBundle for Packaging

Beyond the standard packaging setup (a Dev Hub with second-generation packaging enabled, and a registered namespace for a managed package), packaging a UIBundle has a few specific requirements.

### Set the Source API Version

Set `sourceApiVersion` to `67.0` or later as a top-level property in `sfdx-project.json`, alongside `packageDirectories`.

```json
{
  "sourceApiVersion": "67.0",
  "packageDirectories": [{ "path": "force-app", "default": true }]
}
```

For a managed package, also set the top-level `namespace` property to your registered namespace.

### Include the App's Metadata

Make sure that your package directory contains your UIBundle and its related metadata. For an internal app, include the CustomApplication type that references the UIBundle. To give subscribers a ready-made access grant, you can also include the permission set that the template generates with your app.

### Build the Bundle

Build your UIBundle so the packaged assets are current before you create a package version.

```bash
cd force-app/main/default/uiBundles/myapp
npm install
npm run build
```

:::note
Use the local dev server (`npm run dev`) as your inner development loop while you build the app. A full build, version create, and install round trip takes several minutes, so don't use `sf package version create` to iterate on UI changes. See [Preview and Run Your App Locally](/docs/platform/multiframework/guide/mfw-preview.md).
:::

## Prepare a Managed Package for AppExchange Submission

Before you submit a Multi-Framework app as a managed package to AppExchange for a security review, complete these two prerequisites. Unlocked packages don't go through AppExchange Security Review and therefore don't require these steps.

### Enable Sourcemap Emission

To verify that the compiled JavaScript in `dist/` traces back to your source code, the Salesforce Code Analyzer reads the sourcemaps that your build tool emits. Sourcemaps are required for the analyzer to run its UIBundle checks.

In your `vite.config.ts`, set `sourcemap` to `true` in the `build` block:

```typescript
export default defineConfig(({ mode }) => {
  return {
    base: "./",
    plugins: [
      // tailwindcss(), react(), salesforce(), ...
    ],
    build: {
      outDir: resolve(__dirname, "dist"),
      assetsDir: "assets",
      sourcemap: true, // ← must be true for AppExchange submission
    },
    // resolve: { ... },
    // test: { ... },
  };
});
```

Verify that every `.js` file under `dist/` has a co-located `.js.map`, and that the `sources[]` array inside each map uses relative paths. Don't include absolute paths, such as `/Users/…` or `C:\…`.

### Run the Code Analyzer Scan

Before submitting, run the Salesforce Code Analyzer with the `uibundle` selector to scan your compiled bundle.

First, make sure that the plugin is version 5.16.0 or later:

```bash
sf plugins install @salesforce/plugin-code-analyzer@latest
sf plugins   # confirm code-analyzer 5.16.0 or later
```

Then, from your project root after you've run `npm run build`, run the scan:

```bash
sf code-analyzer run \
  --rule-selector uibundle \
  --rule-selector Recommended \
  --output-file CodeAnalyzerReport.html
```

The `uibundle` selector runs UIBundle integrity checks, and `Recommended` runs the standard cross-engine baseline (ESLint, RetireJS, and others). The two selectors compose additively with no overlap.

## Verify the Packaged UIBundle

After you install the package in a subscriber org, query it through the Tooling API to confirm that the UIBundle component is present.

```bash
sf data query \
  --query "SELECT Id, DeveloperName, IsActive, ManageableState, NamespacePrefix FROM UIBundle" \
  --target-org my-subscriber --use-tooling-api
```

- For a managed package, `ManageableState` is `installed`, meaning it's locked, and `NamespacePrefix` is your namespace.
- For an unlocked package, `ManageableState` is `installedEditable`.
- In both cases, `IsActive` is `true`.

Then, to confirm that the app renders, open the app from the App Launcher in the subscriber's org.

:::note
Because an upgrade doesn't overwrite the UIBundle's `IsActive` value, you must activate the new version manually after you upgrade it.
:::

## See Also

- *Second-Generation Managed Packaging Developer Guide*: [UI Bundle](https://developer.salesforce.com/docs/platform/pkg2-dev/guide/packaging-packageable-components.md#ui-bundle)
- *Metadata API Developer Guide*: [UIBundle](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_uibundle.htm)
- *Salesforce CLI Command Reference*: [package Commands](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_package_commands_unified.htm)
- [Project Structure and Metadata](/docs/platform/multiframework/guide/mfw-project-structure.md)
- [Deploy and Publish a UIBundle](/docs/platform/multiframework/guide/mfw-deploy.md)
