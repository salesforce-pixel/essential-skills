# Access Data and Platform Capabilities

While Agentforce Vibes automatically generates code for data access, it's helpful to understand how you can write your own code to access Salesforce data and related platform capabilities from your web app.

Use the Data SDK for data access with these benefits:

- **Abstraction and consistency:** Data SDK abstracts environment-specific APIs, so you call a simple method and the SDK handles the implementation details for the specific host environment, for example, Lightning Experience or an Experience Builder site.
- **Capability detection:** Data SDK includes integrated capability detection to identify the runtime environment, infer its capabilities, and determine the concrete way to implement those capabilities. Given the built-in detection, component authors can code safely across deployment scenarios.
- **Modern developer experience:** Data SDK provides full TypeScript definitions to offer IntelliSense and autocomplete functionality, compile-time type safety, and uses Promises for structured error handling (try/catch blocks) instead of loosely-typed events.

Learn how you can access and update Salesforce data using the Data SDK.

- [Work with the Data SDK](/docs/platform/multiframework/guide/data-sdk-intro.md)
- [Access Salesforce APIs](/docs/platform/multiframework/guide/data-sdk-connect.md)
- [GraphQL Query Parameters](/docs/platform/multiframework/guide/data-sdk-query.md)
- [GraphQL Mutate Parameters](/docs/platform/multiframework/guide/data-sdk-mutate.md)
- [GraphQL Queries](/docs/platform/multiframework/guide/data-sdk-graphql.md)
- [GraphQL Mutations](/docs/platform/multiframework/guide/data-sdk-graphql-mutation.md)
- [Error Handling](/docs/platform/multiframework/guide/data-sdk-graphql-error.md)
- [Cache Control](/docs/platform/multiframework/guide/data-sdk-cache-control.md)
- [Per-Request Headers](/docs/platform/multiframework/guide/data-sdk-request-headers.md)
- [Data SDK Extensions](/docs/platform/multiframework/guide/data-sdk-extension.md)

Explore platform capabilities for your web app.

- [Get App Identity](/docs/platform/multiframework/guide/data-sdk-identity.md)
- [Manage the Host UI](/docs/platform/multiframework/guide/data-sdk-view.md)
- [Localize Your App](/docs/platform/multiframework/guide/data-sdk-i18n.md)

Find out more about the agent skills you can use to speed up data access implementation in your web app.

- [Use Skills for Data Access](/docs/platform/multiframework/guide/data-sdk-skills.md)
