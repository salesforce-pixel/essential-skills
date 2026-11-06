# Data SDK Extensions

A Data SDK extension adds a self-contained, named API that gives the SDK instance extra capabilities. Use an extension that comes with the SDK, such as for retrieving a custom label from your org. Or create an extension to package your own reusable code.

- To read custom labels with the `labels` extension, see [Get Custom Labels](/docs/platform/multiframework/guide/data-sdk-extension-label.md).
- To package your own reusable data logic behind a typed API, see [Create a Data SDK Extension](/docs/platform/multiframework/guide/data-sdk-extension-custom.md).

Extensions play a role similar to `@salesforce/*` scoped modules in Lightning Web Components (LWC), but they work differently.

- A scoped module is an import that the LWC compiler resolves when it builds your component, so its capability is fixed into the component at build time.
- A Data SDK extension is an opt-in capability that you add when your app runs; you pass it to `createDataSDK()`, and its API becomes available on the SDK instance as `sdk.ext.<name>`.

Because you add extensions when you create the SDK, you choose which ones each SDK instance includes. You can also package and share your own extensions as regular code, without depending on a special module that the compiler has to recognize.

## See Also

- [Work with Data SDK](/docs/platform/multiframework/guide/data-sdk-intro.md)
