# Ai Agent Session Log DMO

Captures log events emitted during AI agent sessions, including informational, warning, error, and fatal entries with causal chaining for multi-agent error tracing.

:::note
This is a standard data model object (DMO), which is created in your org only after you map it. Until it's mapped, this DMO is visible on the data mapping screen but doesn't appear in the Data Model list or record view in the Data 360 app. This is expected behavior. To use this DMO, search for it on the data mapping screen and complete the mapping. After it's mapped, the DMO and its fields appear in the Data Model list.
:::

## Object Properties

**Object API Name:** `AiAgentSessionLog_std__dlm`\
**Category:** Unassigned\
**Availability:** Available in 264 and later versions\
**Primary Key Field:** Id

## Relationships

- **AiAgentSessionId** has a FOREIGNKEY relationship with the [AI Agent Session DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentsessiondmo-dmo.md) `Id` field.
- **AiAgentInteractionId** has a FOREIGNKEY relationship with the [AI Agent Interaction DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentinteractiondmo-dmo.md) `Id` field.
- **AiAgentInteractionStepId** has a FOREIGNKEY relationship with the [AI Agent Interaction Step DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentinteractionstepdmo-dmo.md) `Id` field.
- **TelemetryTraceSpanId** has a FOREIGNKEY relationship with the [Telemetry Trace Span DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-telemetrytracespandmo-dmo.md) `Id` field.
- **CauseLogId** has a FOREIGNKEY relationship with the [Ai Agent Session Log DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentsessionlogdmo-dmo.md) `Id` field.
- **RootCauseLogId** has a FOREIGNKEY relationship with the [Ai Agent Session Log DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentsessionlogdmo-dmo.md) `Id` field.

## Fields

- [AiAgentInteractionId](#aiagentinteractionid)
- [AiAgentInteractionStepId](#aiagentinteractionstepid)
- [AiAgentSessionId](#aiagentsessionid)
- [Category](#category)
- [CauseLogId](#causelogid)
- [cdp_sys_record_currency](#cdp_sys_record_currency)
- [Code](#code)
- [DataSourceId](#datasourceid)
- [DataSourceObjectId](#datasourceobjectid)
- [Description](#description)
- [DetailedDescription](#detaileddescription)
- [ExternalSourceId](#externalsourceid)
- [Id](#id)
- [InternalOrganizationId](#internalorganizationid)
- [KQ_AiAgentInteractionId](#kq_aiagentinteractionid)
- [KQ_AiAgentInteractionStepId](#kq_aiagentinteractionstepid)
- [KQ_AiAgentSessionId](#kq_aiagentsessionid)
- [KQ_CauseLogId](#kq_causelogid)
- [KQ_Id](#kq_id)
- [KQ_RootCauseLogId](#kq_rootcauselogid)
- [KQ_TelemetryTraceSpanId](#kq_telemetrytracespanid)
- [LogDateTime](#logdatetime)
- [LogLevelType](#logleveltype)
- [RootCauseLogId](#rootcauselogid)
- [TelemetryTrace](#telemetrytrace)
- [TelemetryTraceSpanId](#telemetrytracespanid)

### AiAgentInteractionId

- **Field API Name:** `AiAgentInteractionId__c`
- **Data Type:** TEXT
- **Description:** Foreign key to AiAgentInteraction. Nullable.

### AiAgentInteractionStepId

- **Field API Name:** `AiAgentInteractionStepId__c`
- **Data Type:** TEXT
- **Description:** Foreign key to AiAgentInteractionStep. Nullable.

### AiAgentSessionId

- **Field API Name:** `AiAgentSessionId__c`
- **Data Type:** TEXT
- **Description:** Required. Foreign key to AiAgentSession.

### Category

- **Field API Name:** `Category__c`
- **Data Type:** TEXT
- **Description:** Required. Contextual domain of the log entry. Examples: Tool, LLM, Retrieval, Guardrail, Auth, HTTP, Delegation, Platform, Lifecycle, Performance.

### CauseLogId

- **Field API Name:** `CauseLogId__c`
- **Data Type:** TEXT
- **Description:** Self-FK. Immediate wrapped/underlying cause. Can reference a log entry in a different session. Populated only when LogLevel is ERROR or FATAL.

### cdp_sys_record_currency

- **Field API Name:** `cdp_sys_record_currency__c`
- **Data Type:** TEXT
- **Description:** System-generated metadata field that stores a 3-letter ISO currency code.

### Code

- **Field API Name:** `Code__c`
- **Data Type:** TEXT
- **Description:** Required. Structured code for the event. For errors: user-facing error code. For non-errors: event type identifier (examples: TOOL_INVOCATION_START, LLM_RESPONSE_RECEIVED).

### DataSourceId

- **Field API Name:** `DataSourceId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### DataSourceObjectId

- **Field API Name:** `DataSourceObjectId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### Description

- **Field API Name:** `Description__c`
- **Data Type:** TEXT
- **Description:** Short, human-readable summary of the issue. Nullable.

### DetailedDescription

- **Field API Name:** `DetailedDescription__c`
- **Data Type:** TEXT
- **Description:** Required. Structured JSON payload / diagnostics. Schema varies by Category and LogLevelType.

### ExternalSourceId

- **Field API Name:** `ExternalSourceId__c`
- **Data Type:** TEXT
- **Description:** Organization identifier used for dataspace filtering.

### Id

- **Field API Name:** `Id__c`
- **Data Type:** TEXT
- **Description:** Required. Primary Key.

### InternalOrganizationId

- **Field API Name:** `InternalOrganizationId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### KQ_AiAgentInteractionId

- **Field API Name:** `KQ_AiAgentInteractionId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentInteractionId

### KQ_AiAgentInteractionStepId

- **Field API Name:** `KQ_AiAgentInteractionStepId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentInteractionStepId

### KQ_AiAgentSessionId

- **Field API Name:** `KQ_AiAgentSessionId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentSessionId

### KQ_CauseLogId

- **Field API Name:** `KQ_CauseLogId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for CauseLogId

### KQ_Id

- **Field API Name:** `KQ_Id__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for Id

### KQ_RootCauseLogId

- **Field API Name:** `KQ_RootCauseLogId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for RootCauseLogId

### KQ_TelemetryTraceSpanId

- **Field API Name:** `KQ_TelemetryTraceSpanId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for TelemetryTraceSpanId

### LogDateTime

- **Field API Name:** `LogDateTime__c`
- **Data Type:** DATETIME
- **Description:** Required. Timestamp of the log event.

### LogLevelType

- **Field API Name:** `LogLevelType__c`
- **Data Type:** TEXT
- **Description:** Required. Log level. Values: DEBUG | INFO | WARNING | ERROR | FATAL (Severity).

### RootCauseLogId

- **Field API Name:** `RootCauseLogId__c`
- **Data Type:** TEXT
- **Description:** Self-FK. Deepest known cause (denormalized). Can reference a log entry in a different session. Populated only when LogLevel is ERROR or FATAL.

### TelemetryTrace

- **Field API Name:** `TelemetryTrace__c`
- **Data Type:** TEXT
- **Description:** Shared identifier used for implicit joins on TraceId among DMOs (AiAgentInteraction, TelemetryTraceSpan, AiAgentSessionLog). Nullable.

### TelemetryTraceSpanId

- **Field API Name:** `TelemetryTraceSpanId__c`
- **Data Type:** TEXT
- **Description:** Foreign key to TelemetryTraceSpan. Nullable.
