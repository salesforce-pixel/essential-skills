# Project Structure and Metadata

A Multi-Framework app lives in your Salesforce DX project as a UIBundle. The UIBundle represents your app's UI and works with several other metadata types to define the app on the platform. In your project, its source code, build configuration, and metadata definition are stored together in a self-contained folder. When you deploy it, this metadata creates a UIBundle record that establishes the app's identity on the Salesforce Platform and declares which containers can host it.

This topic describes the files and metadata that make up an app, whichever framework you use.

## UIBundle Files

The Salesforce DX project structure includes a `force-app/main/default` folder that contains a `uiBundles` folder. Application metadata and content live together in this `uiBundles` directory. Each application subdirectory is a complete, self-contained unit with its own metadata definition (`.uibundle-meta.xml`), runtime configuration (`ui-bundle.json`), source code, and compiled assets.

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

Each app includes framework build files that connect your app to the platform:

- `vite.config.ts` for React apps
- `angular.json` and its `esbuild/` and `middleware/` folders for Angular apps

:::note
The UIBundle metadata type can contain up to 2,500 files.
:::

For more information, see [Salesforce DX Project Structure and Source Format](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_source_file_format.htm).

## The .uibundle-meta.xml File

The `.uibundle-meta.xml` file, located in the `force-app/main/default/uiBundles/{app_name}` folder, defines the metadata for the app's UI.

The `target` property in this file declares which kind of Salesforce container can use this UIBundle for its UI. It doesn't surface anything on its own. Instead, a CustomApplication or a site references the UIBundle, and that container is what appears in the Salesforce UI.

- `CustomApplication` lets a CustomApplication, which is an internal, employee-facing app, use the UIBundle. This is the default target if you don't specify a value. The CustomApplication appears in the App Launcher and opens in Salesforce, rendering its UI from the UIBundle.
- `Experience` lets an Experience Cloud site use the UIBundle. The site appears in the Digital Experiences app and in the App Launcher, where selecting it opens the site URL in a new tab, and renders its UI from the UIBundle.

:::important
In both cases, additional metadata types are required to integrate your app with the Salesforce Platform and make it available in the UI. For example, to make an internal app available in the App Launcher, you also need a CustomApplication metadata type that references the UIBundle. See [Internal and External App Files](#internal-and-external-app-files).
:::

Here's an example of the UI bundle metadata that's deployed with an internal user app.

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

The `isActive` flag controls whether the deployed bundle is served, and `version` is a schema-version integer that starts at 1.

## The ui-bundle.json File

The `ui-bundle.json` file, located in the `force-app/main/default/uiBundles/{app_name}` folder, is the app's runtime configuration file. The file can include these properties.

| Property                       | Type    | Description                                                                                                                                                                                                                                                                                            |
| ------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `outputDir`                    | string  | Required. The relative path to the directory that contains built application assets. The default value is "`dist`" for bundled apps.                                                                                                                                                                   |
| `apiVersion`                   | string  | The Salesforce API version. Uses the format "`vXX.X`"; for example, "`v66.0`". Be sure to use the same API version as the Salesforce org where you're deploying your app. Defaults to the current org version.                                                                                         |
| `routing`                      | string  | Block containing custom URL handling. If omitted, standard file-based serving is used.                                                                                                                                                                                                                 |
| `routing.fileBasedRouting`     | boolean | When `true`, URLs are automatically mapped to the folder structure in `outputDir`. Defaults to `true`.                                                                                                                                                                                                 |
| `routing.trailingSlash`        | string  | Controls how the platform handles trailing slashes in URLs. Valid values are: <br>• `never`: Removes the slash (for example, redirects "/page/" to "/page"). <br>• `always`: Adds a slash (for example, redirects "/page" to "/page/"). <br>• `auto`: No change.                                       |
| `routing.fallback`             | string  | Specifies the file to serve when a request doesn't match any static asset or explicit rule. Set to `index.html` to allow client-side routing for single-page apps (SPAs).                                                                                                                              |
| `routing.rewrites`             | array   | An array of rewrite rules that serve a different file without changing the browser URL.                                                                                                                                                                                                                |
| `routing.rewrites.route`       | string  | Required for `rewrites`. The source URL pattern. Supports named parameters (`:id`) and wildcards (`*`).                                                                                                                                                                                                |
| `routing.rewrites.target`      | string  | Required for `rewrites`. The internal file path to serve.                                                                                                                                                                                                                                              |
| `routing.redirects`            | array   | An array of redirect rules that return an HTTP redirect response to the client. Rules are evaluated in order.                                                                                                                                                                                          |
| `routing.redirects.route`      | string  | Required for `redirects`. The source URL pattern. Supports named parameters (`:id`) and wildcards (`*`).                                                                                                                                                                                               |
| `routing.redirects.target`     | string  | Required for `redirects`. The destination URL.                                                                                                                                                                                                                                                         |
| `routing.redirects.statusCode` | string  | Required for `redirects`. The HTTP status for the redirect: <br>• **301**: Moved permanently (cacheable) <br>• **302**: Found (temporary, not cached) <br>• **307**: Temporary redirect (preserves request method, not cached) <br>• **308**: Permanent redirect (preserves request method, cacheable) |

This example shows all possible configuration options for a `ui-bundle.json` file.

```json
{
  "outputDir": "dist",
  "apiVersion": "v66.0",
  "routing": {
    "fileBasedRouting": true,
    "trailingSlash": "never",
    "fallback": "index.html",
    "rewrites": [
      {
        "route": "/products/:id",
        "target": "/product-detail.html"
      },
      {
        "route": "/legacy/*",
        "target": "/app.html"
      }
    ],
    "redirects": [
      {
        "route": "/old-home",
        "target": "/",
        "statusCode": 301
      },
      {
        "route": "/promo",
        "target": "/sale",
        "statusCode": 302
      }
    ]
  }
}
```

This example shows a typical configuration file for a single-page app, which ensures that the app works correctly when a user refreshes the page on a sub-route (for example, `/dashboard`).

```json
{
  "outputDir": "dist",
  "routing": {
    "trailingSlash": "never",
    "fallback": "index.html"
  }
}
```

## Internal and External App Files

When you create an app, you choose an internal or an external template, which provides the necessary UIBundle project structure along with the related metadata that differs by use case. The template names differ by framework—for example, `reactinternalapp` and `reactexternalapp` for React, or `angularinternalapp` and `angularexternalapp` for Angular. For the full list of templates and the generate commands, see [Generate an App from a Template](/docs/platform/multiframework/guide/mfw-generate-app.md).

### Internal App Files

Use an internal template to create internal-facing apps for employees signing in with their Salesforce credentials.

Projects based on an internal template also require the CustomApplication metadata. This type defines and configures a Salesforce app, and connects your app to the App Launcher. The `force-app/main/default/applications` folder contains the `.app-meta.xml` file, which includes a field called `uiBundle`. This field contains the fully qualified name of the UIBundle that represents your app, such as `c__myapp`.

When a CustomApplication references the UIBundle through its `uiBundle` field, and the UIBundle's `target` is set to `CustomApplication` in [the `.uibundle-meta.xml` file](#the-uibundle-metaxml-file), the CustomApplication appears in the App Launcher and renders its UI from the UIBundle.

```shell
my-sfdx-project/
└── force-app/main/default/
    ├── uiBundles/
    │   └── myinternalapp/
    │       ├── myinternalapp.uibundle-meta.xml  # target: CustomApplication
    │       ├── ui-bundle.json
    │       └── src/
    └── applications/
        └── MyInternalApp.app-meta.xml           # CustomApplication metadata
```

:::note
Similar to a standard Salesforce app, you can control user access to the app using profiles and permission sets. The internal templates also generate an `<AppName> Access` permission set that grants app visibility and the API Enabled permission. For more information, see [Manage Your App and Grant User Access](/docs/platform/multiframework/guide/mfw-manage.md).
:::

### External App Files

Use an external template to create external-facing apps for business-to-business (B2B) and business-to-consumer (B2C) use cases, such as partners or customers signing in from outside your org. The template provides a prebuilt shell that includes an Experience Cloud site with several pages, navigation, and authentication.

Projects based on an external template also require several additional metadata types to support the Experience Cloud site. The files are contained in these folders in `force-app/main/default`:

- `digitalExperienceConfigs`: The DigitalExperienceConfig metadata type represents the configuration details for your org's workspaces, such as the site label, site URL path prefix, and workspace type.
- `digitalExperiences`: The DigitalExperience metadata type represents a collection of related content items that form the site when combined with data from the DigitalExperienceConfig metadata type.
- `networks`: The Network metadata type represents an Experience Cloud site.
- `sites`: The CustomSite metadata type represents a Salesforce site.

Unlike a standard LWR site, the `digitalExperiences` folder contains only the `sfdc_cms_site` folder. In the `content.json` file in the folder:

- The `appContainer` property is set to `true` to indicate that the site is used in a Multi-Framework app.
- The `appSpace` property refers to the related app. Make sure that the value uses the format `NamespacePrefix__DeveloperName` (for example, `MyNamespace__MyWebApp` or `c__MyWebApp` for orgs without a registered namespace).

```shell
my-sfdx-project/
└── force-app/main/default/
    ├── uiBundles/
    │   └── myexternalapp/
    │       ├── myexternalapp.uibundle-meta.xml  # target: Experience
    │       ├── ui-bundle.json
    │       └── src/
    ├── digitalExperienceConfigs/                # Site configuration
    ├── digitalExperiences/                      # Site content
    ├── networks/                                # Experience Cloud site
    └── sites/                                   # CustomSite metadata
```

:::note
You can't edit a Multi-Framework app's Experience Cloud site in Experience Builder.
:::

## See Also

- [Generate an App from a Template](/docs/platform/multiframework/guide/mfw-generate-app.md)
- [Manage Your App and Grant User Access](/docs/platform/multiframework/guide/mfw-manage.md)
- *Metadata API Developer Guide*: [UIBundle](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_uibundle.htm)
- [Salesforce DX Project Structure and Source Format](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_source_file_format.htm)
