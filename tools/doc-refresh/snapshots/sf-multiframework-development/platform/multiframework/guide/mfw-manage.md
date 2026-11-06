# Manage Your App and Grant User Access

After you deploy a Multi-Framework app, you manage it in Setup from App Manager, the same place you manage any Lightning app. Both internal and external apps appear there, listed as Multi-Framework in the Type column. How you grant users access depends on the app. An internal app opens in Salesforce, and you control who can see it in the App Launcher with a permission set or profile, the same as any custom app. An external app runs on an Experience Cloud site and is visible to everyone by default, like any site, so you control access through the site's guest and authenticated-user settings. An external app also appears in the App Launcher, but selecting it opens the site's URL in a new tab.

:::note
The access steps in this topic are for internal apps, which users open from the App Launcher. You still manage external apps in App Manager, but users reach them through an Experience Cloud site, so you control access with the site's guest and authenticated-user settings instead.
:::

## Manage Your App in Setup

Both internal and external Multi-Framework apps appear in App Manager, listed as Multi-Framework in the Type column. Standard Experience Cloud sites built with LWR or Aura appear as the Community type instead, so the Multi-Framework type identifies your Multi-Framework apps.

1. From Setup, in the Quick Find box, enter `App Manager`, and then select **App Manager**.
2. Find your app in the list, and then select **View** from the row menu.

Whether an app has editable details depends on how it's hosted:

- An internal app is registered as a CustomApplication and has an App Details page. From it, you can edit the app's label and description. Other settings are defined in your app's metadata.
- An external app that runs on an Experience Cloud site doesn't have an App Details page. You manage it through its site instead.

The app connects to your frontend code through the `uiBundle` reference in its metadata, which points to your UIBundle by its fully qualified name, such as `c__MyApp`.

:::note
Structural details like the `uiBundle` reference are defined in your app's metadata. To change them, edit the metadata in your Salesforce DX project and redeploy rather than editing in Setup, so that your source stays the source of truth. See [Deploy and Publish a UIBundle](/docs/platform/multiframework/guide/mfw-deploy.md).
:::

## Grant Users Access to Your App

Access to a Multi-Framework app works the same way as access to any Lightning app: a user can open the app when a permission set or profile makes the app visible to them. Because your app reads and writes Salesforce data through the platform API, users also need the **API Enabled** permission.

Granting access takes two things that are easy to confuse: making the app *visible* to a user, and giving that user access to the *data* the app reads and writes. The generated permission set covers app visibility and API access. Object- and field-level data access can come from the same permission set or from the user's profile or another permission set. A user who can open the app but has no access to its objects sees an empty or partial UI, not an error.

:::note
Deploying a permission set doesn't assign it. When you deploy your project, the `<AppName> Access` permission set is created in the org, but no user has it until you assign it. Assign the permission set after you deploy.
:::

The internal app templates generate a permission set that grants both app visibility and API Enabled, so assigning it is the fastest way to grant access.

### Assign the Generated Permission Set

The internal templates include a permission set named **`<AppName> Access`** (for example, **MyApp Access**). It sets the app to visible and enables the API Enabled user permission.

Assign it to a user with the Salesforce CLI:

```bash
sf org assign permset --name MyApp_Access
```

Or assign it from Setup:

1. From Setup, in the Quick Find box, enter `Permission Sets`, and then select **Permission Sets**.
2. Select the **`<AppName> Access`** permission set.
3. Select **Manage Assignments**, and then **Add Assignments**.
4. Select the users, and then select **Assign**.

### Grant Access Through a Profile

If you manage access with profiles instead of permission sets, make the app visible to a profile:

1. From Setup, open **App Manager**, and edit your app.
2. On the **User Profiles** step, select the profiles that can access the app, and then save.

Confirm that those profiles also have the **API Enabled** permission so the app can load data.

## Open the App from the App Launcher

After a user has access, they open an internal app from the App Launcher.

1. Select the App Launcher (the grid icon) in the navigation bar, on desktop or in the Salesforce mobile app.
2. Search for the app by name.
3. Select the app. It opens at its `salesforce.app` domain URL in a new browser tab.

External apps also appear in the App Launcher. Because they run on an Experience Cloud site, selecting one opens the site's URL in a new browser tab instead of opening in Salesforce.

If an internal app doesn't appear, confirm that:

- The UIBundle's `target` is `CustomApplication`, and the CustomApplication's `uiBundle` field references the UIBundle.
- The user has the **`<AppName> Access`** permission set or a profile that makes the app visible.
- The UIBundle is deployed and its `isActive` flag is `true`.

If the app opens but its data doesn't load, the user has app visibility but not access to the app's data. Confirm that the user has object- and field-level access to the objects the app reads and writes, through their profile or a permission set.

## See Also

- [Deploy and Publish a UIBundle](/docs/platform/multiframework/guide/mfw-deploy.md)
- [Quick Start: Build and Run Your First App](/docs/platform/multiframework/guide/mfw-quick-start.md)
- *Salesforce Help*: [Permission Sets](https://help.salesforce.com/s/articleView?id=sf.perm_sets_overview.htm\&type=5)
- *Salesforce CLI Command Reference*: [org assign permset](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_org_commands_unified.htm)
