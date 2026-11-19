# Agent API Troubleshooting

Review these troubleshooting tips if you run into issues when calling the API.

## HTTP 400 Response: Bad Request

If you receive an HTTP 400 response, there's a problem with your request.

- **Message field in response contains "{VALUE} is not a valid agent ID"**. Verify that your agent ID is correct in your API request. See [Call the API](/docs/ai/agentforce/guide/agent-api-get-started.md#call-the-api).

## HTTP 401 Response: Unauthorized

If you recieve an HTTP 401 response, there's typically an authorization issue. Review [Get Started with Agent API](/docs/ai/agentforce/guide/agent-api-get-started.md).

## HTTP 404 Response: Not Found

If you receive an HTTP 404 response, verify that you're using the correct token and that you're using the correct endpoint. Review [Get Started with Agent API](/docs/ai/agentforce/guide/agent-api-get-started.md).
If your org is on Government Cloud, make sure you're calling `api.gov.salesforce.com` instead of `api.salesforce.com`.

## HTTP 423 Response: Session Already Locked Exception

If you receive an HTTP 423 response, verify that you don't have any requests in progress as the API only supports one request at a time. Review [Get Started with Agent API](/docs/ai/agentforce/guide/agent-api-get-started.md).

## HTTP 500 Response: Internal Server Error

If you receive an HTTP 500 response, verify that you've followed the setup instructions correctly.

- **Message field in response contains "Unsupported Media Type"**. Use the correct `Content-Type` value in the header: `Content-Type: application/json`.
- **Error field in response contains "EngineConfigLookupException"**. When specifying your domain in the [start session endpoint](/docs/ai/agentforce/guide/agent-api-examples.md#start-session), make sure that you're using the My Domain endpoint for your org. From Setup, search for **My Domain**. Copy the value shown in the **Current My Domain URL** field.
- **Error field in response contains "HttpServerErrorException"**. Verify that you are using the correct agent ID in the endpoint. See [Get the Agent ID for an Agent](/docs/ai/agentforce/guide/agent-api-agent-id.md) for instructions on obtaining your agent ID.
- For other issues, review [Get Started with Agent API](/docs/ai/agentforce/guide/agent-api-get-started.md).

## See Also

- [Get Started with Agent API](/docs/ai/agentforce/guide/agent-api-get-started.md)
- [Agent API Examples](/docs/ai/agentforce/guide/agent-api-examples.md)
- [Agent API Considerations](/docs/ai/agentforce/guide/agent-api-considerations.md)
- [Agent API Reference](/docs/ai/agentforce/references/agent-api?meta=summary)
