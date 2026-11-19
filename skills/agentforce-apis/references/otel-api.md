# Agentforce Session Trace OTel API (beta)

One REST call returns a whole agent session as **OpenTelemetry (OTLP v1.0) `ResourceSpans`
JSON**: turns, messages, LLM calls, action executions, metric scores and feedback, already
joined. Feed it into Splunk, Datadog, New Relic or any OTLP collector without
transformation.

It reads from two Data 360 data models: **Agentforce Session Tracing** (the
`ssot__AiAgent*` DMOs) and **Generative AI Audit & Feedback**. It is additive: the STDM
DMOs and Agent Analytics stay the basis for Agentforce Studio analytics. For SQL across
many sessions use the `agentforce-platform-tracing-stdm` skill; use this API for one
session at a time (debugging, custom evals, third-party export).

## Beta limits

- **One session ID per request.** No bulk query.
- Only sessions whose **start time is within the last 72 hours** of the request.
- Connect REST API standard rate limits apply.
- **Data Cloud (Data 360) is required**: the API runs Data 360 SQL underneath. Data 360
  governance and dataspace rules apply to the calling user.
- No permissions beyond standard Agentforce access during the beta.

## Setup

1. Agentforce turned on.
2. Setup → **Einstein Generative AI** → **Einstein Audit, Analytics, and Monitoring
   Setup** → turn on **Agentforce Session Tracing** and **Audit and Feedback** if they
   aren't on.
3. Authenticate with OAuth 2.0 through an External Client App (same mechanism as the
   Agent API), or any REST client holding that app's token.

## Call

```bash
curl "https://{MY_DOMAIN_URL}/services/data/v66.0/einstein/audit/otel/{SESSION_ID}" \
  --header "Authorization: Bearer ${ACCESS_TOKEN}"
```

This is a Salesforce **instance** endpoint (`/services/data/…` on your My Domain), not
`api.salesforce.com` like the Agent API.

The response is a spans hierarchy: session → turns → messages, LLM calls and actions, with
metrics and feedback attached.

**Which session ID?** The docs only say "the session ID". In the STDM model that's
`ssot__AiAgentSession__dlm.ssot__Id__c`. Whether the Agent API's `sessionId` is the same
value isn't stated; if a call with it returns nothing, look up the session in the DMOs
(by time, agent, or your `externalSessionKey`) and use `ssot__Id__c`.

## Pull many sessions (beta workaround)

No bulk endpoint yet, so:

1. List session IDs for the window you want with Data 360 SQL (see
   `agentforce-platform-tracing-stdm`, e.g. sessions started in the last hour).
2. Call the OTel endpoint once per ID, respecting rate limits.
3. Send each payload to your OTLP endpoint or collector.

Native push or connector support is planned, not available.

## Collector example

An OTLP collector can poll the API, enrich the data and export it. The docs' example
(the `salesforce_otel` receiver is a placeholder: use a custom receiver or an HTTP
receiver with a poller):

```yaml
# otel-collector-config.yaml
receivers:
  salesforce_otel:
    endpoint: https://your-instance.salesforce.com
    auth:
      authenticator: oauth2client

processors:
  batch:
    timeout: 10s
  attributes:
    actions:
      - key: source
        value: salesforce
        action: insert

exporters:
  otlp/datadog:
    endpoint: https://api.datadoghq.com
    headers:
      DD-API-KEY: ${DD_API_KEY}

service:
  pipelines:
    traces:
      receivers: [salesforce_otel]
      processors: [batch, attributes]
      exporters: [otlp/datadog]
```

Keep API keys in environment variables or a secret store, as above, never in the file.
