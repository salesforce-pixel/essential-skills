# Export Agentforce Session Tracing Data (Beta)

Extract a single, unified JSON view of a full agent session trace with the Agentforce Session Trace OTel API. Import the output into your favorite observability tool or OpenTelemetry Protocol (OTLP) collector for further investigation.

## About the Agentforce Session Trace OTel API

This REST API extracts unified trace, metric and log data from two sources:

- [Agentforce Session Tracing data model](https://help.salesforce.com/s/articleView?id=ai.generative_ai_session_trace_data_model.htm)
- [Generative AI Audit & Feedback data model](https://help.salesforce.com/s/articleView?id=ai.generative_ai_feedback_data_model.htm)

The JSON output includes every step of an Agentforce agent interaction: turns, messages, LLM calls, actions, metric scores, and feedback. The output format conforms with the [OpenTelemetry (OTLP) specification](https://opentelemetry.io/docs/specs/otlp/), which is an open standard for sharing telemetry data with observability platforms and OTLP collectors.

## Beta Release Limitations and Considerations

The beta release of the Agentforce Session Trace OTel API has these limitations and considerations:

- Only single-session queries are supported (one session ID per API request). Bulk query support is not yet available.

- Salesforce Connect API standard rate limits apply (see [Connect REST API Limits](https://developer.salesforce.com/docs/atlas.en-us.chatterapi.meta/chatterapi/intro_rate_limits.htm?d=afx)).

- The API returns data for sessions that started (StartTimestamp) within the previous 72 hours of the API request.

## Get Started

### Prerequisites

- Agentforce must be turned on in your Salesforce org.

### Step 1: Turn On Data Collection

1. From Setup, in the Quick Find box, enter **Einstein Generative AI**, and then select **Einstein Audit, Analytics, and Monitoring Setup**.
2. Turn on any of the following features that aren’t turned on:

- Agentforce Session Tracing (see [Set Up Agentforce Session Tracing](https://help.salesforce.com/s/articleView?id=ai.generative_ai_session_trace_setup.htm\&type=5))
- Audit and Feedback (see [Set Up Einstein Generative AI Audit and Feedback](https://help.salesforce.com/s/articleView?id=ai.generative_ai_feedback_enable.htm\&type=5))

### Step 2: Authenticate

Authenticate using OAuth 2.0 using an [external client app (ECA)](https://help.salesforce.com/s/articleView?id=xcloud.external_client_apps.htm\&type=5). Alternatively, you can authenticate using your favorite REST client (using the auth token from the external client app).

### Step 3: Submit a REST API Query

Run the Agentforce Session Trace OTel API against the REST endpoint, passing in the session ID for the session you want to retrieve.

`GET /services/data/v66.0/einstein/audit/otel/{session-id}`

Here’s a high-level view of the response showing the spans hierarchy.

![OTel API Response](https://a.sfdcstatic.com/developer-website/sfdocs/genai/media/otel-api/otel-api-response.png)

### Step 4: Export the Output to Your Observability Platform

Most modern observability platforms (such as Splunk, Datadog, and New Relic) support OpenTelemetry Protocol (OTLP) ingestion. Because the API already returns OpenTelemetry-formatted data, you can feed it directly into the observability platform or into any [OpenTelemetry Protocol (OTLP) collector](https://opentelemetry.io/docs/collector/).

## Share Telemetry Data Using an OTLP Collector

You can use an OTLP collector to poll the Agentforce Session Trace OTel API, transform and enrich the data, and export it to an observability platform. Here is an example config for an OTLP collector.

```yaml
# otel-collector-config.yaml
receivers:
  # Custom receiver or use http receiver with poller
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

## Frequently Asked Questions (Beta)

1. **What does the Agentforce Session Trace OTel API return?**\
   A full session trace in OTel ResourceSpans format. The output includes all turns, messages, LLM calls, action executions, metric scores, and feedback signals. All data is pre-joined. No Data Cloud SQL is required.

2. **Do I need Data Cloud enabled?**\
   Yes, for the Beta release. Agentforce Session Tracing data is stored in Data 360. The API queries the data using Data 360 SQL. The long-term Unified Planner native OTel path is designed to reduce this dependency, but it is not available in this beta release.

3. **Does the API enforce data governance and dataspace access?**\
   Yes. The underlying Data 360 query service enforces dataspace and governance rules based on the user context making the API call. The API uses the user context to query only what is allowed.

4. **Does this API replace the existing STDM DMOs and Agent Analytics?**\
   No. The OTel JSON API is additive. It’s designed for pro-code and API-based use cases like debugging, custom evals, and third-party export. The normalized STDM DMOs remain the foundation for Agentforce Studio analytics and observability

5. **What are the Beta limitations?**

   - Only single-session queries are supported (one session ID per API request). Bulk query support is not yet available.
   - Salesforce Connect API standard rate limits apply (see [Connect REST API Limits](https://developer.salesforce.com/docs/atlas.en-us.chatterapi.meta/chatterapi/intro_rate_limits.htm?d=afx)).

6. **How does authentication work?**\
   OAuth 2.0 using an [external client app (ECA)](https://help.salesforce.com/s/articleView?id=xcloud.external_client_apps.htm\&type=5). This is the same mechanism as the Agent Builder API. For Beta, no additional permissions beyond standard Agentforce access are required.

7. **Can I send this data to my other observability platform (such as Datadog, Splunk, or New Relic)?**\
   In the beta release, pull data via the API and pipe it to any OTLP-compatible endpoint. The OTel format means that no transformation is needed.

   **Example**: Call the API in automated to pull multiple traces one by one.

   Get me all the sessions that happened in one hour.

   - Call query service to get a session list.
   - Use that list to query the API.\
     Native push/connector support is planned.

8. **Which OpenTelemetry Specification is used for this API?**\
   This trace uses [OTLP (OpenTelemetry Protocol) v1.0](https://opentelemetry.io/docs/specs/otlp/).
