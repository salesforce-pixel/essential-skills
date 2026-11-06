# Deploy and Publish a UIBundle

After you build and preview your app, deploy it to your Salesforce org as metadata and publish a version so that users can access it. Because your app is a UIBundle—a Salesforce metadata type—you deploy it with the same Salesforce DX workflows and CLI commands that you use for any other source, and you can include it in your deployment pipeline.

This topic applies to both React and Angular apps. Build your production assets with your framework's build command first (for example, `npm run build`, which runs `vite build` for React or `ng build` for Angular), and then deploy the resulting UIBundle.

## Before You Deploy

Confirm that:

- Your app builds cleanly. Run your framework's build command from the UI bundle directory before you deploy, and verify that it produces the output directory named in `ui-bundle.json` (`dist` by default). Deploy the built assets, not just your source.
- The `apiVersion` in `ui-bundle.json` matches the API version of the target org. If you omit `apiVersion`, the app defaults to the org's current version.
- Your target org is configured for Multi-Framework development. See [Set Up Your Org for Multi-Framework App Development](/docs/platform/multiframework/guide/mfw-setup.md).
- For an external app, the Experience Cloud site metadata (DigitalExperience, DigitalExperienceConfig, Network, CustomSite) is present in your project. See [Project Structure and Metadata](/docs/platform/multiframework/guide/mfw-project-structure.md).

## Deploy the UIBundle

Deploy your app the same way you deploy any other metadata, with `sf project deploy start`.

To deploy a single UIBundle to your default org:

```shell
sf project deploy start --source-dir force-app/main/default/uiBundles/MyReactApp
```

To deploy the whole project, including the CustomApplication or Experience Cloud site metadata that the app depends on:

```shell
sf project deploy start --source-dir force-app
```

An internal app also needs its CustomApplication metadata, and an external app needs its site metadata, to appear in the UI. Deploy those types together with the UIBundle—for example, by deploying the whole `force-app` directory—so the app resolves correctly. Salesforce DX resolves the dependencies, so no special metadata-type order or manifest is required. See [Internal and External App Files](/docs/platform/multiframework/guide/mfw-project-structure.md#internal-and-external-app-files).

## Versioning and Publication Lifecycle

Each UIBundle carries a `version` in its `.uibundle-meta.xml` file and an `isActive` flag.

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

- **`version`**: A positive integer that identifies the schema version of the UIBundle definition. New apps start at `1`.
- **`isActive`**: Controls whether the deployed UIBundle is served to users. Set it to `true` to serve the app.

To update a deployed app, rebuild your production assets and redeploy the UIBundle. Salesforce stores your app's files and serves the active version, so you manage the publication lifecycle on the platform rather than on an external web server.

## Verify the Deployed App

After deployment:

- **Internal app**: Open the app from the App Launcher on desktop or in the Salesforce mobile app. If the app doesn't appear, confirm that the UIBundle `target` is `CustomApplication`, that the CustomApplication metadata references the UIBundle, and that users have access. See [Manage Your App and Grant User Access](/docs/platform/multiframework/guide/mfw-manage.md).
- **External app**: Open the site from the Digital Experiences app or the Experience Cloud site URL.

## Include Your App in a Deployment Pipeline

Because the UIBundle is source-format metadata in your Salesforce DX project, you can commit it to version control and deploy it through your existing CI/CD pipeline alongside your other metadata. Build the production assets as a pipeline step before the deploy, and treat the UIBundle like any other component in your package.

## See Also

- *Salesforce CLI Command Reference*: [project deploy start](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_project_commands_unified.htm)
- *Metadata API Developer Guide*: [UIBundle](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_uibundle.htm)
- [Multi-Framework recipes repo](https://github.com/trailheadapps/multiframework-recipes)
