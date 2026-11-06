# Use Third-Party JavaScript Libraries in Your Multi-Framework App

Multi-Framework apps run under a content security policy (CSP) that blocks third-party scripts loaded directly from external domains. For example, if you add a standard `<script src="https://...">` tag to your app, such as the snippet that an analytics service gives you, the browser blocks the external script. To use a third-party library, serve the library and all of its dependencies from Salesforce so that the policy treats them as first-party code.

If a library loads other files from an external domain at runtime, update the library to load those files from Salesforce instead. For example, if an analytics loader script requires jQuery, serve jQuery from Salesforce and update the loader to request jQuery from there.

:::note
Adding the library's domain to Trusted URLs in Setup or to the CSP settings in Experience Builder doesn't allowlist the script in a UIBundle.
:::

The options for serving a library from Salesforce depend on whether your app is an internal, employee-facing app or an external-facing app that runs on an Experience Cloud site.

| Option                    | Supported App Types                | Update Impact                                          |
| :------------------------ | :--------------------------------- | :----------------------------------------------------- |
| Bundle with app           | Internal- and external-facing apps | Requires rebuilding and redeploying the UIBundle       |
| Upload as static resource | External-facing apps               | Updates without rebuilding or redeploying the UIBundle |

## Bundle the Library with Your App

Add the library to your app's project so that your build tool includes it in the UIBundle and it loads from your app's own domain. If you're building an internal-facing app, you must use this approach to serve a third-pary library.

## Upload the Library as a Static Resource

For an external-facing app that runs on an Experience Cloud site, upload the library and each of its dependencies to your org as static resources.

To create a static resource, see [Static Resources](https://help.salesforce.com/s/articleView?id=platform.pages_static_resources.htm\&type=5) in Salesforce Help. To define one as metadata in a Salesforce DX project, see [StaticResource](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_staticresource.htm) in the Metadata API Developer Guide.

Load each static resource from its site URL.

```text
SITE_DOMAIN/SITE_PATH_PREFIX/sfsites/c/resource/RESOURCE_NAME
```

For example, for a site at `https://MyDomainName.my.site.com/shop/`, load a static resource named `gtagloader` like this.

```html
<script src="https://MyDomainName.my.site.com/shop/sfsites/c/resource/gtagloader"></script>
```
