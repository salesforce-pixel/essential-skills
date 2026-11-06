# Setup, templates, project structure, agentic tools, preview

Sources: `multiframework-overview`, `mfw-setup`, `mfw-quick-start`, `mfw-generate-app`, `mfw-project-structure`, `mfw-agentic-tools`, `mfw-preview` (see `sources.md`).

## Platform concepts

- **UIBundle** is the metadata type your app becomes: a self-contained unit with the app's source, config and routing rules. It's stored and versioned in Salesforce, managed with Salesforce DX, and deployed as metadata (in pipelines too). It lives in `force-app/main/default/uiBundles/<app>/`.
- **Internal apps** (B2E): employees sign in with Salesforce credentials and open the app from the App Launcher (desktop or Salesforce mobile app). Access through permission sets or profiles.
- **External apps** (B2C customers, B2B partners): served through an Experience Cloud site, so visitors don't need a Salesforce login. The app also shows in the App Launcher for Salesforce users; selecting it opens the site URL in a new tab.
- **Salesforce app domain**: internal apps run on their own origin under `*.salesforce.app` (served from `.my.salesforce.app`). The same-origin policy keeps the app and its third-party dependencies away from the Lightning DOM, browser storage and Salesforce session cookies. Users still get SSO through a scoped session that can call the supported platform APIs.
- **Security**: data requests go through the User Interface API, which enforces OLS, FLS, sharing and validation rules on the server for every query and mutation. Don't reimplement access control in the frontend.

### Multi-Framework vs LWC

| | LWC | Multi-Framework |
|---|---|---|
| Use for | Integrated, reusable, composable components in Lightning Experience, Experience Builder sites, mobile | Self-contained SPAs or highly customised experiences with Salesforce as host and data source |
| Integration | Native: data binding, LDS, Apex | Through Data SDK / GraphQL / UI API |
| Performance | Optimised for the Salesforce UI | Depends heavily on API design and data retrieval strategy |
| Component reuse | Across LWC projects and Lightning Experience | Inside the app; embedding in Lightning needs Microfrontend support (UI Embedding, Beta) |

### Development approaches

- **Agentforce Vibes**: org-aware (metadata, objects, Apex), stays inside the Salesforce Trust Boundary. Scaffolds, adds data, CMS content and features from natural language.
- **Builder Central (Beta)**: low-code, natural-language app builder in Setup; produces React apps.
- **Your own tooling** (Claude Code, Cursor, …): it's a standard Salesforce DX project with an npm build.

Features you can add: Salesforce data (Data SDK), Salesforce CMS content, object search, authentication (Salesforce credentials internally; Experience Cloud guest/authenticated externally), Agentforce Conversation Client, embedding as a microfrontend (Beta).

## Org setup

**Editions**: Enterprise, Performance, Unlimited, Developer, Partner Developer — **Hyperforce only**. Not on Alibaba Cloud or Government Cloud.

Checklist:
1. **Hyperforce check**: Setup → Company Information → Organization Detail. An instance name with a three-letter prefix plus a number (e.g. `abc123`) means Hyperforce.
2. Latest **Salesforce CLI** and **Salesforce Extension Pack** (brings current skills and Live Preview).
3. **External apps only**: Digital Experiences enabled; licences: Customer Community or Customer Community Plus (B2C), Partner Community and Channel Account (B2B).
4. **Salesforce app domain** (internal apps; needs *Customize Application*):
   - Setup → Quick Find `Salesforce Multi-Framework` → **Salesforce Multi-Framework Apps**. If an **Enable Domain** button shows, click it and confirm; otherwise it's already on (most orgs have it on).
   - Setup → **My Domain** → Routing and Policies: enable **Salesforce Edge Network** if it isn't (required for the app domain).

Limitations: packaging is unsupported for external apps; developer orgs support only the `c` namespace.

Optional:
- **Content Read-Only / Content Write MCP servers** (Salesforce-hosted) let Agentforce Vibes search, retrieve, create and publish Salesforce CMS content (images, documents, brands) for the app.
- **Agentforce Conversation Client**: see `styling-libraries-acc.md` for the org setup (Employee Agent, cookie policy, Trusted Domains for Inline Frames).

## Templates

| | Internal | External |
|---|---|---|
| Audience | Employees with Salesforce logins | Customers, partners, public users |
| Auth | Salesforce credentials (SSO) | Experience Cloud guest or authenticated login |
| Access point | App Launcher (desktop + mobile app) | Digital Experiences app and site URL |
| Project templates | `reactinternalapp`, `angularinternalapp` | `reactexternalapp`, `angularexternalapp` |
| Metadata | UIBundle + CustomApplication | UIBundle + DigitalExperience, DigitalExperienceConfig, Network, CustomSite |
| Prebuilt features | Agentforce Conversation Client, object search | Navigation, authentication, object search |

Bundle-only templates (add an app to an existing project): `reactbasic`, `angularbasic`.

```shell
# New project (full scaffold incl. related metadata)
sf template generate project --name MyReactApp --template reactinternalapp
sf template generate project --name MyAngularApp --template angularexternalapp

# Add a UI bundle to an existing DX project
sf template generate ui-bundle --name MyApp --template reactbasic
```

`ui-bundle` adds the app under `force-app/main/default/uiBundles/`. You then supply CustomApplication or Experience Cloud site metadata yourself.

Install dependencies **inside the bundle directory, not the project root**:

```shell
cd force-app/main/default/uiBundles/MyReactApp
npm install
```

Tooling is standard: Vite for React, Angular CLI for Angular.

## Quick start (React, internal)

```shell
sf template generate project --name MyFirstApp --template reactinternalapp
cd MyFirstApp
cd force-app/main/default/uiBundles/MyFirstApp
npm install
npm run dev                     # http://localhost:5173, hot reload on save under src/
npm run build
sf project deploy start --target-org MyOrg
sf org assign permset --name MyFirstApp_Access
```

Then App Launcher → search **MyFirstApp**. To run the dev server against live org data, authenticate an org and set it as default before `npm run dev`. If the template didn't generate a permission set, grant access to the CustomApplication in Setup (Permission Sets or profile).

## Project structure

```shell
my-sfdx-project
└── force-app/
    └── main/
        └── default/
              └── uiBundles/
                    └── myapp/
                        ├── myapp.uibundle-meta.xml    # Salesforce metadata
                        ├── ui-bundle.json             # Runtime configuration
                        ├── package.json               # Application dependencies
                        ├── src/                       # Application source code
                        │   ├── components/            # UI components
                        │   ├── pages/                 # Application pages
                        │   ├── assets/                # Images, fonts, icons
                        │   └── styles/                # Global styles
                        └── dist/                      # Build output (generated)
├── sfdx-project.json                                  # SFDX project configuration
└── package.json                                       # Root workspace configuration
```

Framework build files: `vite.config.ts` (React); `angular.json` plus `esbuild/` and `middleware/` folders (Angular). Generated projects also have `AGENT.md` at the root and a generated `schema.graphql` (don't edit it).

**Limit: a UIBundle can contain up to 2,500 files.**

### `<app>.uibundle-meta.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<UIBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <masterLabel>myapp</masterLabel>
    <description>A Salesforce UI Bundle.</description>
    <isActive>true</isActive>
    <version>1</version>
    <target>CustomApplication</target>
</UIBundle>
```

- `target` declares which container may use the bundle; it surfaces nothing by itself.
  - `CustomApplication` (default): an internal CustomApplication references the bundle and appears in the App Launcher.
  - `Experience`: an Experience Cloud site uses the bundle.
- `isActive`: whether the deployed bundle is served.
- `version`: schema-version integer, starts at 1.

### `ui-bundle.json` (runtime config)

| Property | Type | Description |
|---|---|---|
| `outputDir` | string | **Required.** Relative path to built assets. Default `dist`. |
| `apiVersion` | string | Format `vXX.X`, e.g. `v66.0`. Match the target org. Defaults to the org's current version. |
| `routing` | object | Custom URL handling. Omitted → standard file-based serving. |
| `routing.fileBasedRouting` | boolean | Map URLs to the folder structure in `outputDir`. Default `true`. |
| `routing.trailingSlash` | string | `never` (strip, `/page/`→`/page`), `always` (add), `auto` (no change). |
| `routing.fallback` | string | File served when nothing else matches. `index.html` enables SPA client-side routing. |
| `routing.rewrites[]` | array | `{route, target}`: serve another file without changing the URL. `route` supports `:id` params and `*` wildcards. |
| `routing.redirects[]` | array | `{route, target, statusCode}`, evaluated in order. Status: `301` permanent (cacheable), `302` temporary (not cached), `307` temporary, keeps method, `308` permanent, keeps method. |

Every option:

```json
{
  "outputDir": "dist",
  "apiVersion": "v66.0",
  "routing": {
    "fileBasedRouting": true,
    "trailingSlash": "never",
    "fallback": "index.html",
    "rewrites": [
      { "route": "/products/:id", "target": "/product-detail.html" },
      { "route": "/legacy/*", "target": "/app.html" }
    ],
    "redirects": [
      { "route": "/old-home", "target": "/", "statusCode": 301 },
      { "route": "/promo", "target": "/sale", "statusCode": 302 }
    ]
  }
}
```

Typical SPA (refresh on `/dashboard` keeps working):

```json
{
  "outputDir": "dist",
  "routing": {
    "trailingSlash": "never",
    "fallback": "index.html"
  }
}
```

### Internal app files

```shell
force-app/main/default/
├── uiBundles/
│   └── myinternalapp/
│       ├── myinternalapp.uibundle-meta.xml  # target: CustomApplication
│       ├── ui-bundle.json
│       └── src/
└── applications/
    └── MyInternalApp.app-meta.xml           # CustomApplication metadata
```

The `.app-meta.xml` has a `uiBundle` field with the bundle's fully qualified name, e.g. `c__myapp`. CustomApplication `uiBundle` reference + bundle `target` = `CustomApplication` → the app shows in the App Launcher. Internal templates also generate an `<AppName> Access` permission set (app visibility + API Enabled).

### External app files

```shell
force-app/main/default/
├── uiBundles/
│   └── myexternalapp/
│       ├── myexternalapp.uibundle-meta.xml  # target: Experience
│       ├── ui-bundle.json
│       └── src/
├── digitalExperienceConfigs/                # Site configuration (label, URL path prefix, workspace type)
├── digitalExperiences/                      # Site content
├── networks/                                # Experience Cloud site (Network)
└── sites/                                   # CustomSite
```

- Unlike an LWR site, `digitalExperiences` holds only the `sfdc_cms_site` folder. Its `content.json` has:
  - `appContainer: true` (the site hosts a Multi-Framework app)
  - `appSpace`: the related app as `NamespacePrefix__DeveloperName` (e.g. `MyNamespace__MyWebApp`, or `c__MyWebApp` without a namespace).
- **You can't edit a Multi-Framework app's site in Experience Builder.**

## Agentic coding tools

Three pieces: the project's agent context, the Salesforce skills library, and the Salesforce DX MCP server.

**`AGENT.md`** (generated at project root, nothing to configure) tells the tool to:
- run build, lint and dev commands from `<source>/uiBundles/<appName>/`, not the root;
- access Salesforce data through the Data SDK, never `fetch`/`axios` directly;
- leave generated files such as `schema.graphql` alone;
- check for a relevant skill first (skills are the authoritative guidance).

**Skills library**: Agentforce Vibes has it built in. Other tools:

```bash
npx skills add forcedotcom/sf-skills
```

It covers generating a project, building the frontend, accessing data, internal/external apps, deploying, localising, file upload and ACC. It changes often (skills may be renamed or removed), so install it rather than relying on fixed names.

**MCP server** (Salesforce DX MCP; authorises an org already connected with the CLI, so log in first):

```json
{
  "mcpServers": {
    "salesforce": {
      "command": "npx",
      "args": ["-y", "@salesforce/mcp", "--orgs", "DEFAULT_TARGET_ORG", "--toolsets", "orgs,metadata,data"]
    }
  }
}
```

Toolsets: `orgs` (authorise/open/manage orgs), `metadata` (deploy/retrieve incl. UIBundle), `data` (SOQL).

**Standard agent workflow**:
1. Work from the bundle directory with the project's npm scripts (build, lint, dev).
2. `npm run graphql:schema` (fetch the org's GraphQL schema), then `npm run graphql:codegen` (typed operations → `src/api/graphql-operations-types.ts`).
3. Access data through the Data SDK.
4. Deploy the UIBundle and its metadata to the org.

## Preview and run locally

**Dev server** (React and Angular):

```bash
npm run dev                       # http://localhost:5173, auto-reload
SF_UIBUNDLE_PORT=4200 npm run dev # other port
npx ng serve                      # Angular alternative
```

**Live Preview in VS Code** (renders in a VS Code tab with your authorised org's data):

```bash
sf plugins install @salesforce/plugin-ui-bundle-dev
```

Then Command Palette → **SFDX: Open in Live Preview** (or right-click a `.js/.jsx/.ts/.tsx` file → same command) → pick the app.

| | Dev server | Live Preview |
|---|---|---|
| Renders in | Browser at `localhost:5173` | VS Code tab |
| Data | Local/mocked data plus any org connection your code makes | Your authorised org |
| Best for | Fast UI iteration, framework dev-server features | Real org data while building |

If the app embeds ACC, add the local origin (e.g. `http://localhost:5173`) to **Trusted Domains for Inline Frames**.
