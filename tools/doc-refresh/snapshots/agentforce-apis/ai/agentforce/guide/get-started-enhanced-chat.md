# Get Started With Enhanced Chat v2

Enhanced Chat v2 is a new customer interface for Enhanced Web Chat on Service Cloud. Both Enhanced Chat versions allow you to connect and deploy Service agents to external chat channels.

The UI of Enhanced Chat v2 can be customized with custom Lightning Types. See [Introduction to Lightning Types](/docs/ai/agentforce/guide/lightning-types-get-started.md).

:::note
Enhanced Chat v2 is different from Enhanced Web Chat. For more information, see [What’s Enhanced Chat v2?](https://help.salesforce.com/s/articleView?id=service.enhanced_chat_v2\_intro.htm\&type=5).
:::

## Context Events

Enhanced Chat v2 offers a unique way to pass context events. `utilAPI` in Enhanced Web Chat now has a new `setSessionContext` method that can be used in Enhanced Chat v2 deployments. See [the enhanced chat developer guide](https://developer.salesforce.com/docs/service/messaging-web/guide/context-events.md) and [the enhanced chat reference](https://developer.salesforce.com/docs/service/messaging-web/references/m4w-reference/utilAPI.md#setsessioncontext) in Service Cloud.

## Inline Mode

You can embed the Enhanced Chat v2 client directly within a specific element on your web page. Learn how to enable and configure inline mode in [Inline Mode in Enhanced Chat v2](/docs/ai/agentforce/guide/enhanced-chat-inline-mode.md).

## Custom Lightning Types

You can use custom lightning types to personalize the appearance of your chat deployment. To send a message on behalf of the user or pass context events from your Lightning Web Component (LWC), see [Custom Lightning Type APIs for Enhanced Chat v2](https://developer.salesforce.com/docs/service/messaging-web/guide/custom-lighting-type-apis.md).

## See Also

- *Salesforce Help*: [Connect a Service Agent to Enhanced Chat v2](https://help.salesforce.com/s/articleView?id=ai.service_agent_deploy_enhanced_chat_v2.htm)
