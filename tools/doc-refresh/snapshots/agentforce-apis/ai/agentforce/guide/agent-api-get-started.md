# Get Started with the Agent API

Bring the power of generative AI to your business with Agentforce. Build intelligent, trusted, and customizable AI agents and empower your users to get more done with Salesforce. Use the Agent API to communicate with AI agents directly from a REST API. Start sessions, send messages to the AI agent, receive messages, and end sessions using the API.

:::note
Agent API isn’t supported for agents of type “Agentforce (Default)”.
:::

To access the Agent API, you must set up an external client app that supports the client credential flow. These instructions show you how to get your environment set up for use with the API and demonstrate how to make your first call to the API.

![API Flow](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/api-onboarding-steps-simpler.svg)

## Prerequisites

You must have Agentforce enabled with at least one agent activated. See [Set Up Your Agent](https://help.salesforce.com/s/articleView?id=ai.copilot_setup.htm) in Salesforce Help.

## Create a Salesforce App

To use the Agent API, you must create an [external client app (ECA)](https://help.salesforce.com/s/articleView?id=xcloud.external_client_apps.htm). To learn how to create an ECA, see [Create an External Client App](https://help.salesforce.com/s/articleView?id=xcloud.create_a_local_external_client_app.htm) in Salesforce Help.

These instructions help you create a basic app with the client credentials flow, although you can use any flow that provides a [JWT-based access token](https://help.salesforce.com/s/articleView?id=xcloud.jwt_access_tokens.htm).

1. From Setup, in the Quick Find box, enter `External Client App`, and then select **External Client Apps Manager**.

2. Select **New External Client App**.

3. Specify a name and contact email.

4. Select **Enable OAuth** and use these OAuth scopes.

   - **Manage user data via APIs (api)**
   - **Perform requests at any time (refresh_token, offline_access)**
   - **Access chatbot services (chatbot_api)**
   - **Access the Salesforce API Platform (sfap_api)**

   ![OAuth settings scope](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/oauth-settings-agent-api.png)

5. Select these additional OAuth settings.

   - **Enable Client Credentials Flow:** Allows your app to exchange its client credentials for an access token.
   - **Issue JWT Web Token (JWT)-based access tokens for named users:** Allows your app to issue tokens for named users.

   ![OAuth settings checkboxes](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/oauth-settings-2b.png)

6. Deselect:

   - **Require secret for Web Server Flow**
   - **Require secret for Refresh Token Flow**
   - **Require Proof Key for Code Exchange (PKCE) extension for Support Authorization Flows**

7. Create the app.

8. From your app settings, click the **Policy** tab.

9. Click **Edit**.

10. From the **OAuth Flows and External Client App Enhancements** section, check **Enable Client Credentials Flow**.

11. Set the **Run As (Username)** field to the email address of a user that has at least [API Only access](https://help.salesforce.com/s/articleView?id=platform.integration_user.htm).

12. Save the changes.

## Obtain Credentials

To create a token, you need the consumer key and consumer secret from your external client app.

1. From your app settings, click the **Settings** tab.
2. Expand the **OAuth Settings** section.
3. Click the **Consumer Key and Secret** button, and copy your key and secret. You need these values to mint this token.

## Create a Token

All calls to the Agent API require a token. Create a token by using the consumer key, consumer secret, and your domain name.

```sfdocs-code {"lang":"bash", "title": "Create a Token"}
curl https://{MY_DOMAIN_URL}/services/oauth2/token \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=client_credentials' \
--data-urlencode 'client_id={CONSUMER_KEY}' \
--data-urlencode 'client_secret={CONSUMER_SECRET}'
```

- `MY_DOMAIN_URL`: You can get the domain from Setup. Search for **My Domain**. Copy the value shown in the **Current My Domain URL** field.
- `CONSUMER_KEY`, `CONSUMER_SECRET`: You can get the consumer key and secret by following the instructions in [Obtain Credentials](#obtain-credentials).

The previous command returns a JSON payload similar to this response.

```sfdocs-code {"lang":"json", "title": "Sample Token Response"}
{
  "access_token": "eyJ0bmsiOiJjb3JlL3Byb2QvM…(shortened)",
  "signature": "HBb7Zf4aaOUlI1V…(shortened)",
  "token_format": "jwt",
  "scope": "sfap_api chatbot_api api",
  "instance_url": "https://sample-org-eaa32a127e4a6b.my.salesforce.com",
  "id": "https://login.salesforce.com/id/00DW…Wpg5MAC/005W…nF9IAI",
  "token_type": "Bearer",
  "issued_at": "1736530186928",
  "api_instance_url": "https://api.salesforce.com"
}
```

Copy the access token specified in the `access_token` property. This token is required when making requests to the API.

## Call the API

After you set up your app and created a token, you're ready to call the API. Before making the call, gather this information.

- `AGENT_ID`: The ID of the agent that you want to interact with. The method for obtaining this ID depends on which builder you used to create your agent. See [Get the Agent ID for an Agent](/docs/ai/agentforce/guide/agent-api-agent-id.md) for detailed instructions.
- `ACCESS_TOKEN`: The token that you created in [Create a Token](#create-a-token).
- `RANDOM_UUID`: A random UUID value that you provide to represent the session key. You can use this parameter to trace the conversation in your agent's event logs.
- `MY_DOMAIN_URL`: From Setup, search for **My Domain**. Copy the value shown in the **Current My Domain URL** field.

:::important
Be sure to use the right URLs for your org.

- Use your **My Domain** URL (for example, `some_domain.my.salesforce.com`) and not simply the domain name displayed in your browser (`some_domain.lightning.force.com`).
- If your org is on Government Cloud, replace `api.salesforce.com` with `api.gov.salesforce.com` in all Agent API endpoints.
:::

This curl command creates a new agent session with the Agent API.

```sfdocs-code {"lang":"bash", "title": "Create a Session"}
curl --location -X POST https://api.salesforce.com/einstein/ai-agent/v1/agents/{AGENT_ID}/sessions \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {ACCESS_TOKEN}' \
--data '{
 "externalSessionKey": "{RANDOM_UUID}",
 "instanceConfig": {
   "endpoint": "https://{MY_DOMAIN_URL}"
 },
 "streamingCapabilities": {
   "chunkTypes": ["Text"]
 },
 "bypassUser": true
}'
```

:::note
The `bypassUser` parameter indicates whether to use the agent-assigned user instead of the logged in user. If set to `true`, the API uses the user associated with the agent. If set to `false`, the API uses the user associated with the token. For this client credentials flow scenario, we set the value to `true`. However, you may need to change this value depending on your use case.
:::

When this call succeeds, you receive a response with a session ID and additional info. Use the session ID to continue the conversation with the agent.

```sfdocs-code {"lang":"json", "title": "Sample Response"}
{
  "sessionId": "8e715939-a121-40ec-80e3-a8d1ac89da33",
  "_links": {
    "self": null,
    "messages": {
      "href": "https://api.salesforce.com/einstein/ai-agent/v1/sessions/8e715939-a121-40ec-80e3-a8d1ac89da33/messages/stream"
    },
    "session": {
      "href": "https://api.salesforce.com/einstein/ai-agent/v1/agents/0XxQZ0000000Ty50AE/sessions"
    },
    "end": {
      "href": "https://api.salesforce.com/einstein/ai-agent/v1/sessions/8e715939-a121-40ec-80e3-a8d1ac89da33"
    }
  },
  "messages": [
    {
      "type": "Inform",
      "id": "8e7cafae-0eb5-44b1-9195-21f1cd6e1f4b",
      "feedbackId": "",
      "planId": "",
      "isContentSafe": true,
      "message": "Hi, I'm an AI service assistant. How can I help you?",
      "result": [],
      "citedReferences": []
    }
  ]
}
```

Congratulations, you’ve successfully started using the Agent API! To continue using the API, see [Agent API Examples](/docs/ai/agentforce/guide/agent-api-examples.md) and the [Agent API Postman Collection](https://www.postman.com/salesforce-developers/salesforce-developers/collection/gwv9bjy/agent-api).

## See Also

- [Get the Agent ID for an Agent](/docs/ai/agentforce/guide/agent-api-agent-id.md)
- [Agent API Session Lifecycle](/docs/ai/agentforce/guide/agent-api-lifecycle.md)
- [Agent API Examples](/docs/ai/agentforce/guide/agent-api-examples.md)
- [Agent API Postman Collection](https://www.postman.com/salesforce-developers/salesforce-developers/collection/gwv9bjy/agent-api)
- [Agent API Considerations](/docs/ai/agentforce/guide/agent-api-considerations.md)
- [Agent API Troubleshooting](/docs/ai/agentforce/guide/agent-api-troubleshooting.md)
- [Agent API Reference](/docs/ai/agentforce/references/agent-api?meta=summary)
