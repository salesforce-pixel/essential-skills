# Agent API Considerations

Review these considerations before you use the Agent API.

## Supported Agent Types

The Agent API isn’t supported for agents of type “Agentforce (Default)”.

## Usage and Billing

Agent API usage impacts credit consumption as described in the following Salesforce help topic: [Generative AI Usage and Billing](https://help.salesforce.com/s/articleView?id=ai.generative_ai_usage.htm).

## API Timeout

The Agent API has a 120-second timeout. When a call times out, you receive an HTTP 500 response.

## Government Cloud

If your org is on Government Cloud, use `api.gov.salesforce.com` as the base endpoint for all Agent API requests instead of `api.salesforce.com`. The path and request format are otherwise identical to the standard endpoint. For example, to start a session, use `https://api.gov.salesforce.com/einstein/ai-agent/v1/agents/{AGENT_ID}/sessions`.

## See Also

- [Get Started with Agent API](/docs/ai/agentforce/guide/agent-api-get-started.md)
- [Agent API Examples](/docs/ai/agentforce/guide/agent-api-examples.md)
- [Agent API Troubleshooting](/docs/ai/agentforce/guide/agent-api-troubleshooting.md)
- [Agent API Reference](/docs/ai/agentforce/references/agent-api?meta=summary)
