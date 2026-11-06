# Generate an App from a Template

Salesforce Multi-Framework templates scaffold a fully configured project so you can focus on building features instead of configuring plumbing. The templates include the UIBundle metadata, runtime configuration, framework tooling, and the additional metadata your app needs to run on the Salesforce Platform. You generate an app with the Salesforce CLI, using the same `sf` commands you use for other Salesforce metadata.

## Choose a Template

Choose a template based on your framework and your app's audience. Internal templates target employees who sign in with Salesforce credentials, whereas external templates target customers, partners, or public users who reach your app through an Experience Cloud site.

An internal app and an external app use different project templates and platform configuration, and require some additional metadata types to integrate with the Salesforce Platform.

| Feature                | Internal Apps                                         | External Apps                                                                                               |
| ---------------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Audience**           | Employees with Salesforce logins                      | Customers, partners, or public users                                                                        |
| **Authentication**     | Salesforce credentials (SSO supported)                | Experience Cloud guest access or authenticated login                                                        |
| **Access point**       | App Launcher on desktop and the Salesforce mobile app | Digital Experiences app and Experience Cloud site URL                                                       |
| **Template**           | `reactinternalapp`, `angularinternalapp`              | `reactexternalapp`, `angularexternalapp`                                                                    |
| **Metadata Types**     | UIBundle + CustomApplication                          | UIBundle + Experience Cloud site metadata (DigitalExperience, DigitalExperienceConfig, Network, CustomSite) |
| **Pre-built features** | Agentforce Conversation Client, object search         | Navigation, authentication, object search                                                                   |

For more information, see [Project Structure and Metadata](/docs/platform/multiframework/guide/mfw-project-structure.md).

## Generate a New Project

To start a new app, you can generate a Salesforce DX project from an internal or external template. The internal and external app templates scaffold a full project, so you generate them with `sf template generate project`. The generated project includes the UIBundle and all of the additional metadata the app needs to run.

For example, for an internal React app, use:

```shell
sf template generate project --name MyReactApp --template reactinternalapp
cd MyReactApp
```

Or for an external Angular app, use:

```shell
sf template generate project --name MyAngularApp --template angularexternalapp
cd MyAngularApp
```

## Add a UI Bundle to an Existing Project

If you already have a Salesforce DX project and want to add an app to it, generate a UI bundle into the existing project rather than scaffolding a new one. Use a bundle-only template in this case, namaly `reactbasic` for React or `angularbasic` for Angular.

```shell
sf template generate ui-bundle --name MyApp --template reactbasic
```

The command adds the app under `force-app/main/default/uiBundles/`. You supply any additional metadata, such as CustomApplication or Experience Cloud site metadata, separately.

## Install Dependencies

A generated app manages its dependencies with npm. Install them from inside the app's UIBundle directory, not the project root.

```shell
cd force-app/main/default/uiBundles/MyReactApp
npm install
```

The install brings in standard framework tooling (Vite for React, the Angular CLI for Angular), so there's no custom toolchain to learn.

## Next Steps

After you generate and install your app:

- Run it locally and see live changes: [Preview and Run Your App Locally](/docs/platform/multiframework/guide/mfw-preview.md).
- Understand the generated files and metadata: [Project Structure and Metadata](/docs/platform/multiframework/guide/mfw-project-structure.md).
- Follow the end-to-end path from scaffold to deploy: [Quick Start: Build and Run Your First App](/docs/platform/multiframework/guide/mfw-quick-start.md).

## See Also

- *Salesforce CLI Command Reference*: [template generate ui-bundle](https://developer.salesforce.com/docs/platform/salesforce-cli-reference/guide/cli_reference_template_generate_ui-bundle.md)
- *Metadata API Developer Guide*: [UIBundle](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_uibundle.htm)
- [Multi-Framework recipes repo](https://github.com/trailheadapps/multiframework-recipes)
