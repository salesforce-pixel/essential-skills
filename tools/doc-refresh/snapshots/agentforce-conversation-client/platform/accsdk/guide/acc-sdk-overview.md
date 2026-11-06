# Agentforce Conversation Client Web SDK

Agentforce Conversation Client (ACC) Web SDK helps developers integrate Agentforce Employee Agent (AEA) conversational experiences into external web applications in a simple and flexible way. As a framework-agnostic SDK, it easily adapts to different frontend technologies. Built on the Lightning Out 2.0 platform as a Lightning Web Component Interface (LWCI), this SDK enables developers to quickly implement high-fidelity conversational interfaces that maintain the sophisticated rendering and interaction logic found in native Salesforce applications. It integrates your custom frontend with the Agentforce infrastructure, handling secure connections, real-time message state management, and the dynamic rendering of Lightning Types to deliver rich, interactive components.

### Prerequisites

#### Set Up Your Salesforce Org

Before integrating the Agentforce Conversation Client Web SDK into an external application, your Salesforce Administrator must configure the Salesforce org. To securely render the ACC UI outside of Salesforce, the ACC requires an authenticated session negotiated via an External Client App.

Review and complete these prerequisite configurations to ensure your external application can securely communicate with Salesforce.

- [Setup External Client Apps (ECA)](/docs/platform/accsdk/guide/acc-sdk-setup-auth-external.md): Configure an External Client App (ECA) to manage OAuth 2.0 authentication and generate the required client credentials.
- [Setup Trusted Domains](/docs/platform/accsdk/guide/acc-sdk-setup-trusted-domains.md): Update your Salesforce session settings to add your web application as a trusted domain for inline frames and ensure first-party cookie restrictions are disabled.
- [Generate the Access Token for Agentforce Conversation Client Web SDK](/docs/platform/accsdk/guide/acc-sdk-setup-token.md): Execute an OAuth flow from your backend server to negotiate a secure session token for the frontend client.
- [Get Your Employee Agent ID](/docs/platform/accsdk/guide/acc-sdk-get-acc-agent-id.md): Access the setup in your org and retrieve the unique 18-character `agentId` required to identify your agent in the ACC Web SDK.
