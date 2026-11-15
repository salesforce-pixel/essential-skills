# Agent Platform Tracing | Salesforce Help

Source: https://help.salesforce.com/s/articleView?id=ai.generative_ai_platform_trace.htm&type=5

QUICKSTART YOUR EINSTEIN GENERATIVE AI SOLUTION
Agent Platform Tracing

This tracing capability provides comprehensive visibility into the actions and performance of Agentforce Agents, capturing crucial telemetry data across various services. By leveraging Data 360, users can unify this trace data with session information to create detailed reports. These reports are invaluable for monitoring Key Performance Indicators (KPIs), identifying performance bottlenecks, and quickly pinpointing the root cause of issues, ultimately enhancing the reliability and efficiency of Agent implementations.

REQUIRED EDITIONS
NOTE Agent Platform Tracing does not support Government Cloud.
Available in: Lightning Experience
Available in: Enterprise, Performance, Unlimited, and Developer Editions with Foundations, or Agentforce 1 or Einstein 1 Editions
Set Up Agent Platform Tracing

To generate Data 360 reports for Session and Platform Traces, users must first enable Data 360 and Platform Tracing.

From Setup, in the Quick Find box, enter Einstein Generative AI, and then select Einstein Generative AI.
From Einstein Generative AI, click Einstein Audit, Analytics, and Monitoring Setup.
Confirm that Agentforce Session Tracing is turned on. See Set Up Agentforce Session Tracing.
Scroll to the Agent Platform Tracing toggle and turn it on.

Your data model is provisioned in just a few minutes. Data collection then starts immediately and recurs at five-minute intervals. Note that turning data collection increases your org’s credit consumption rate.

Suspending data collection keeps your data so that you can resume later. Any reports show a gap between the time you turn it off and turn it back on.

Data 360 Reports for Service Rep Sessions and Platform Traces

To gain insights into KPIs and trends, create a single Data 360 report that integrates both Agent Session traces and End-to-End Platform traces. This report can be run for near real-time data, allows for grouping, filtering, and summarizing records, and can be shared with others.

Agent Tracing includes spans from the following services:

Apex
Flows
Prompt Builder
Invocable Actions
Planner
AI Gateway
LLM Gateway
DC Query Federator

Generate a Data 360 Report

Create reports on specific Data Model Objects (DMOs), such as Telemetry Trace Span and AI Agent Interaction, to analyze and learn from unified data.

Navigate to the Reports tab in Salesforce and click New Report. The Report Types page is displayed.
In the search bar, type the name of the Data Model Object (DMO) you want to report on. In this case, you would select Telemetry Trace Span or AI Agent Interaction.
Create a new field relationship within the relevant data model objects. In this instance, you could select Telemetry Trace Span -Telemetry Trace → ManyToOne → AI Agent Interaction - Telemetry Trace.

In Data 360, relationships between DMOs are established by defining a connection from a "Source DMO" to a "Target DMO" using key fields. The most frequent type of relationship is Many-to-One, where multiple records from the Source DMO correspond to a single record in the Target DMO. Refer to Data Model Object Relationships for more information.

Within the DMO's detail page, there is a Relationships tab. This tab provides a visual and structured view of all the relationships that exist for this DMO. Verify the new DMO relationships through the Relationships tab.

Telemetry Trace Span Example

AI Agent Interaction Example

Create a custom report type.
Click New Custom Report in Setup underneath New Custom Report. Fill out the fields to create a new custom report type. In this case, you would create a Session & Platform Traces report type.
Go to the Data Cloud App and select the Reports tab.
Create a Data 360 Report. Click New Report and select the desired report type (i.e. Session Traces and Platform Traces).
Click Start Report.

Once the report is initiated, you should be able to visualize correlated platform telemetry trace spans logged as part of each Agent Session.

NOTE Data 360 reports display a maximum of 2,000 rows in run mode. You can export up to 50,000 rows. For more information, see Data 360 Reports and Dashboards and Data Cloud Reports and Dashboards: Limits and Limitations.
Data Model for Agent Platform Tracing

Enabling these features automatically generates a Data 360 data stream, a Data Lake Object (DLO), and a Data Model Object (DMO). This data is created within the data space specified in Auditing & Monitoring.

Observability Spans Data Stream

The Observability Spans Data Stream is automatically created to capture the trace data:

LABEL API SCHEMA ID
cdp_sys_PartitionDate cdp_sys_PartitionDate__c DateTime
Internal Organization InternalOrganization__c Text
Data Source Object DataSourceObject__c Text
Data Source DataSource__c Text
attributes attributes__c Text
durationNanos durationNanos__c Number
endDateTime endDateTime__c DateTime
operationName operationName__c Text
organizationId organizationId__c Text
parentSpanId parentSpanId__c Text
serviceName serviceName__c Text
spanId spanId__c Text
spanKind spanKind__c Text
startDateTime startDateTime__c DateTime
statusCode statusCode__c Text
traceId traceId__c Text
Observability Spans Data Lake Object

A new DLO called ObservabilitySpans is created with the following fields:

LABEL API SCHEMA DATA TYPE
attributes attributes__c Text
cdp_sys_PartitionDate cdp_sys_PartitionDate__c DateTime
cdp_sys_SourceVersion cdp_sys_SourceVersion__c Text
Data Source DataSource__c Text
Data Source Object DataSourceObject__c Text
durationNanos durationNanos__c Number
endDateTime endDateTime__c DateTime
Internal Organization InternalOrganization__c Text
KQ_parentSpanId KQ_parentSpanId__c Text
KQ_spanId KQ_spanId__c Text
operationName operationName__c Text
organizationId organizationId__c Text
parentSpanId parentSpanId__c Text
serviceName serviceName__c Text
spanId spanId__c Text
startDateTime startDateTime__c DateTime
statusCode statusCode__c Text
traceId traceId__c Text
Telemetry Trace Span Data Model Object

A new DMO called Telemetry Trace Span is created with the following fields:

LABEL API SCHEMA DATA TYPE DESCRIPTION
Data Source ssot__DataSourceId__c Text A unique reference ID for the record source.
Data Source Object ssot__DataSourceObjectId__c Text Unique ID for the origin object, like a cloud storage file or connector entity.
Duration Number ssot__DurationNumber__c Text Total duration of the span in nano seconds.
End Date Time ssot__EndDateTime__c Number Span end time.
Internal Organization ssot__InternalOrganizationId__c DateTime Identifier for the internal organization or department that owns the data.
Key Qualifier Telemetry Parent Span KQ_TelemetryParentSpanId__c Text Fully Qualified Trace Parent Span ID
Key Qualifier Telemetry Trace Span Id KQ_Id__c Text Fully Qualified Trace Span ID
Operation Name ssot__OperationName__c Text Name of the operation performed on the external service.
Service Name ssot__ServiceName__c Text Service identifier.
Start Date Time ssot__StartDateTime__c Text Span start time.
Status Code ssot__StatusCode__c DateTime The execution result of a span.
Telemetry Parent Span ssot__TelemetryParentSpanId__c Text Unique identifier for a parent span, used to track nested sub-operations.
Telemetry Span Attributes ssot__TelemetrySpanAttributeText__c Text Key-value metadata providing operational context for a Span.
Telemetry Span Events ssot__TelemetrySpanEventText__c Text Logs a singular, meaningful event during a Span's duration.
Telemetry Traces ssot__TelemetryTrace__c Text Unique identifier used to track a complete request across all related spans.
Telemetry Trace Span Id ssot__Id__c Text A unique ID for an individual span, representing a single unit of work.
SOQL Examples

DLO SOQL

SELECT attributes__c, cdp_sys_PartitionDate__c, cdp_sys_SourceVersion__c, DataSource__c, DataSourceObject__c,
durationNanos__c, endDateTime__c, InternalOrganization__c, KQ_parentSpanId__c, KQ_spanId__c
FROM ObservabilitySpans__dll LIMIT 100

DMO SOQL

SELECT ssot__DataSourceId__c, ssot__DataSourceObjectId__c, ssot__DurationNumber__c, ssot__EndDateTime__c,
ssot__InternalOrganizationId__c, KQ_TelemetryParentSpanId__c, KQ_Id__c, ssot__OperationName__c, ssot__ServiceName__c,
ssot__SpanKind__c FROM ssot__TelemetryTraceSpan__dlm LIMIT 100
Trace Example
Trace ID: a744ad5ccf0f61c2

run.interaction [Atlas Reasoning Engine] [ROOT]
(spanId: 9dcc09221a05d4cf)
│
├── run.action.AnswerQuestionsWithKnowledge_179gL0000019Ah7 [Atlas Reasoning Engine]
│ (spanId: 90a3808ba7a67fe8)
│ │
│ └── run.invokeActions.STREAM_KNOWLEDGE_SEARCH [InvocableAction]
│ (spanId: 95499b41725eb82a)
│ │
│ └── run.einstein_gpt__answerWithKnowledge.1 [PromptTemplate]
│ (spanId: a9a8b8f2e1fd35cb)
│ 📋 Attributes:
│ • prompt_template.execution.api.version: 66.0
│ • prompt_template.execution.step: 66.0
│ • prompt_template.api.name: einstein_gpt__answerWithKnowledge
│ • prompt_template.api.version: 1
│ │
│ └── run.invokeActions.EINSTEIN_RETRIEVER_GET_RESULTS [InvocableAction]
│ (spanId: 82559a5dedaff638)
│ │
│ ├── run.step.einstein_gpt__answerWithKnowledge [PromptTemplate]
│ │ (spanId: 934afceaac15c6d4)
│ │ 📋 Attributes:
│ │ • prompt_template.step.start_time: 1774049705404
│ │ • prompt_template.step.end_time: 1774049705430
│ │ • prompt_template.step: resolve_template
│ │ │
│ │ └── run.step.einstein_gpt__answerWithKnowledge [PromptTemplate]
│ │ (spanId: b93e831b1c492cf9)
│ │ 📋 Attributes:
│ │ • prompt_template.step.start_time: 1774049705447
│ │ • prompt_template.step.end_time: 1774049705449
│ │ • prompt_template.step: mask_template
│ │ │
│ │ └── run.step.einstein_gpt__answerWithKnowledge [PromptTemplate]
│ │ (spanId: 8380c9b813f64afa)
│ │ 📋 Attributes:
│ │ • prompt_template.step.start_time: 1774049705500
│ │ • prompt_template.step.end_time: 1774049705502
│ │ • prompt_template.step: generation
│ │
│ └── run.retriever.File_ADL_File_ADL_1Cx_Xl7d6d114de [Einstein AI Gateway]
│ (spanId: a0f6b9721e1049a3)
│ 📋 Attributes:
│ • retriever.numberofresults: 10
│ • retriever.isadvancedmode: False
│ • retriever.retrievername: File_ADL_File_ADL_1Cx_Xl7d6d114de
│ │
│ └── run.hybridsearch.ADL_File_ADL_index__dlm [Data Cloud]
│ (spanId: 86aa7512858c1aa9)
│
├── run.topic.GeneralFAQ_16jgL000001ATzR [Atlas Reasoning Engine]
│ (spanId: a3709c000d5d6a2e)
│ │
│ ├── run.llmstep [Atlas Reasoning Engine]
│ │ (spanId: 9829763b4362466f)
│ │
│ ├── run.llmstep [Atlas Reasoning Engine]
│ │ (spanId: 9a29b1009ea0f4c6)
│ │
│ └── run.llmstep [Atlas Reasoning Engine]
│ (spanId: bf63506e4fccff9f)
│
└── run.llmstep [Atlas Reasoning Engine]
(spanId: 9f31edde2c62d1dc)
Summary:
- 15 total spans in this trace
- 5 spans with attributes (marked with 📋)
- 10 spans without attributes
- All spans share trace ID: a744ad5ccf0f61c2
