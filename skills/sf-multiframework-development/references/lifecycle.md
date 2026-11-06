# Test, deploy, manage access, embed, package

Sources: `mfw-lifecycle`, `mfw-testing`, `mfw-deploy`, `mfw-manage`, `mfw-ui-embedding`, `mfw-packaging`.

Order: test → build + deploy → grant access → (optional) embed or package.

## Test (run from `<source>/uiBundles/<appName>/`)

**Unit tests**:

```bash
npm run test          # watch mode
npm run test -- run   # single pass (CI), React/Vitest
```

- React: Vitest + Testing Library + jsdom (`vitest.config.ts`, `vitest.setup.ts`). Put `MyComponent.test.tsx` next to the component.
- Angular: `ng test` over `*.spec.ts`.

**End-to-end (Playwright)**: `playwright.config.ts` + `e2e/app.spec.ts`. A local static server serves the compiled app, so **no org connection is needed**.

```bash
npm run build:e2e      # production build with paths rewritten for Playwright
npx playwright test    # React
npm run e2e            # Angular
```

Run both in CI before the deploy step.

## Build and deploy

Build first (`npm run build` = `vite build` for React or `ng build` for Angular) and confirm the `outputDir` from `ui-bundle.json` (default `dist`) exists. **Deploy the built assets, not only the source.**

Pre-deploy checklist:
- Clean build, `dist/` present.
- `ui-bundle.json` `apiVersion` matches the target org (or is omitted, so the org default is used).
- Org set up: Hyperforce, app domain, Edge Network (see `setup-and-project.md`).
- External app: DigitalExperience, DigitalExperienceConfig, Network and CustomSite metadata are in the project.

```shell
# one bundle
sf project deploy start --source-dir force-app/main/default/uiBundles/MyReactApp
# whole project, incl. CustomApplication / site metadata
sf project deploy start --source-dir force-app
```

Deploy the CustomApplication (internal) or site metadata (external) **together with** the bundle. Salesforce DX resolves the dependencies; no ordering or manifest is needed.

**Versioning**: `<version>` in `.uibundle-meta.xml` is a schema-version integer (starts at 1); `<isActive>true</isActive>` serves the bundle. To update the app, rebuild and redeploy; Salesforce stores the files and serves the active version.

CI/CD: commit the bundle (source format) and add the build as a pipeline step before deploy.

**Verify**:
- Internal: App Launcher (desktop or mobile). If it's missing: bundle `target` = `CustomApplication`, CustomApplication `uiBundle` points to it, the user has access.
- External: Digital Experiences app or the site URL.

## Manage and grant access

Setup → **App Manager**: Multi-Framework apps (internal and external) show **Multi-Framework** in the Type column (LWR/Aura sites show *Community*). Row menu → **View**.
- Internal app (a CustomApplication): App Details page, where only the label and description are editable. Everything else, including the `uiBundle` reference (`c__MyApp`), lives in metadata: edit the source and redeploy.
- External app: no App Details page; manage it through its site. Access is controlled by the site's guest and authenticated-user settings (visible to everyone by default).

**Internal access needs two separate things:**
1. **App visibility + API Enabled**: the generated `<AppName> Access` permission set grants both. Deploying it **doesn't assign it**:

   ```bash
   sf org assign permset --name MyApp_Access
   ```

   Or Setup → Permission Sets → `<AppName> Access` → Manage Assignments → Add Assignments. Or by profile: App Manager → edit the app → **User Profiles** step, and make sure those profiles have **API Enabled**.
2. **Data access**: object and field permissions for whatever the app reads and writes (same permission set, profile, or another permission set). Without it the user sees an **empty or partial UI, not an error**.

Opening: App Launcher → search → the app opens at its `salesforce.app` URL in a **new tab**. External apps open the site URL in a new tab.

Troubleshooting:
- **Not in the App Launcher**: check `target`/`uiBundle` wiring, the permission set or profile, deployed and `isActive` = true.
- **Opens but no data**: object/field-level access is missing.

## Embed as a microfrontend (Beta)

UI Embedding hosts the app in a sandboxed iframe through the `lightning-ui-embedding` base component, with a typed channel for styling, sizing and lifecycle signals (the View SDK, see `platform-sdk-extras.md`).

1. Deploy the bundle and grant access, open it from the App Launcher, and copy its full `*.salesforce.app` URL.
2. Write a thin LWC that renders `<lightning-ui-embedding>` with `src` set to that URL.
3. Add the LWC to a Lightning page or an Experience Cloud site page.

Wrapper details, error states and the View SDK are covered in the Microfrontend guide: <https://developer.salesforce.com/docs/platform/microfrontend/guide/get-started.md> and <https://developer.salesforce.com/docs/platform/microfrontend/guide/internal-ui-bundles.md>.

## Package (2GP), internal apps only

Unlocked packages: internal distribution, POCs, fast iteration. Managed packages: AppExchange or customer distribution. **External (B2B/B2C) apps can't be packaged.**

Requirements beyond normal 2GP setup (Dev Hub; namespace for managed):

```json
{
  "sourceApiVersion": "67.0",
  "namespace": "yourns",
  "packageDirectories": [{ "path": "force-app", "default": true }]
}
```

- `sourceApiVersion` ≥ `67.0`, top level. `namespace` is for managed packages only.
- The package directory contains the UIBundle and the CustomApplication that references it, plus optionally the generated Access permission set as a ready-made grant.
- Build before `sf package version create`:

  ```bash
  cd force-app/main/default/uiBundles/myapp
  npm install
  npm run build
  ```

- Don't iterate on UI through package versions (several minutes per round trip); use `npm run dev`.

**AppExchange security review (managed only)**:

1. Sourcemaps in `vite.config.ts`:

   ```typescript
   export default defineConfig(({ mode }) => {
     return {
       base: "./",
       plugins: [ /* tailwindcss(), react(), salesforce(), ... */ ],
       build: {
         outDir: resolve(__dirname, "dist"),
         assetsDir: "assets",
         sourcemap: true, // required for AppExchange submission
       },
     };
   });
   ```

   Every `dist/**/*.js` needs a co-located `.js.map` whose `sources[]` paths are **relative** (no `/Users/…`, `C:\…`).
2. Code Analyzer ≥ 5.16.0, run from the project root after `npm run build`:

   ```bash
   sf plugins install @salesforce/plugin-code-analyzer@latest
   sf plugins   # confirm code-analyzer 5.16.0+
   sf code-analyzer run \
     --rule-selector uibundle \
     --rule-selector Recommended \
     --output-file CodeAnalyzerReport.html
   ```

   `uibundle` runs the bundle integrity checks; `Recommended` runs the cross-engine baseline (ESLint, RetireJS, …). They add up without overlapping.

**Verify in the subscriber org**:

```bash
sf data query \
  --query "SELECT Id, DeveloperName, IsActive, ManageableState, NamespacePrefix FROM UIBundle" \
  --target-org my-subscriber --use-tooling-api
```

Managed: `ManageableState = installed`, `NamespacePrefix` = your namespace. Unlocked: `installedEditable`. Both: `IsActive = true`. Then open it from the App Launcher.

**An upgrade doesn't overwrite `IsActive`: activate the new version manually after upgrading.**
