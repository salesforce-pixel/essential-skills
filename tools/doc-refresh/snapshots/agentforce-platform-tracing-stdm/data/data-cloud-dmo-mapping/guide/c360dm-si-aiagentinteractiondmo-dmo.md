# AI Agent Interaction DMO

## Object Properties

**Object API Name:** `ssot__AiAgentInteraction__dlm`\
**Category:** Unassigned\
**Availability:** Available in 254 and later versions\
**Primary Key Field:** Id

## Relationships

- **TelemetryTraceSpanId** has a FOREIGNKEY relationship with the [Telemetry Trace Span DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-telemetrytracespandmo-dmo.md) `Id` field.
- **IndividualId** has a FOREIGNKEY relationship with the [Individual DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-individualdmo-dmo.md) `Id` field.
- **AiAgentSessionId** has a FOREIGNKEY relationship with the [AI Agent Session DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentsessiondmo-dmo.md) `Id` field.
- **PrevInteractionId** has a FOREIGNKEY relationship with the [AI Agent Interaction DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentinteractiondmo-dmo.md) `Id` field.

## Fields

- [AiAgentInteractionType](#aiagentinteractiontype)
- [AiAgentSessionId](#aiagentsessionid)
- [AttributeText](#attributetext)
- [cdp_sys_record_currency](#cdp_sys_record_currency)
- [DataSourceId](#datasourceid)
- [DataSourceObjectId](#datasourceobjectid)
- [EndTimestamp](#endtimestamp)
- [ExternalSourceId](#externalsourceid)
- [Id](#id)
- [IndividualId](#individualid)
- [InternalOrganizationId](#internalorganizationid)
- [KQ_AiAgentSessionId](#kq_aiagentsessionid)
- [KQ_Id](#kq_id)
- [KQ_IndividualId](#kq_individualid)
- [KQ_PrevInteractionId](#kq_previnteractionid)
- [KQ_TelemetryTraceSpanId](#kq_telemetrytracespanid)
- [PrevInteractionId](#previnteractionid)
- [SessionOwnerId](#sessionownerid)
- [SessionOwnerObject](#sessionownerobject)
- [StartTimestamp](#starttimestamp)
- [TelemetryTraceId](#telemetrytraceid)
- [TelemetryTraceSpanId](#telemetrytracespanid)
- [TopicApiName](#topicapiname)

### AiAgentInteractionType

- **Field API Name:** `ssot__AiAgentInteractionType__c`
- **Data Type:** TEXT
- **Description:** The category of the interaction type, for example, Turn.

### AiAgentSessionId

- **Field API Name:** `ssot__AiAgentSessionId__c`
- **Data Type:** TEXT
- **Description:** The ID of the parent session this interaction occurs in.

### AttributeText

- **Field API Name:** `ssot__AttributeText__c`
- **Data Type:** TEXT
- **Description:** JSON key-value pairs that store additional metadata or contextual information specific to the interaction.

### cdp_sys_record_currency

- **Field API Name:** `ssot__cdp_sys_record_currency__c`
- **Data Type:** TEXT
- **Description:** System-generated metadata field that stores a 3-letter ISO currency code.

### DataSourceId

- **Field API Name:** `ssot__DataSourceId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### DataSourceObjectId

- **Field API Name:** `ssot__DataSourceObjectId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### EndTimestamp

- **Field API Name:** `ssot__EndTimestamp__c`
- **Data Type:** DATETIME
- **Description:** The timestamp when the interaction completed.

### ExternalSourceId

- **Field API Name:** `ssot__ExternalSourceId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### Id

- **Field API Name:** `ssot__Id__c`
- **Data Type:** TEXT
- **Description:** Required. A unique, system-generated identifier for the AiAgentInteraction record. Maximum size is 15 characters.

### IndividualId

- **Field API Name:** `ssot__IndividualId__c`
- **Data Type:** TEXT
- **Description:** The ID of an Individual record that represents the session owner participant. This field is populated only if the SessionOwnerObject is Individual.

### InternalOrganizationId

- **Field API Name:** `ssot__InternalOrganizationId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### KQ_AiAgentSessionId

- **Field API Name:** `KQ_AiAgentSessionId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentSessionId

### KQ_Id

- **Field API Name:** `KQ_Id__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for Id

### KQ_IndividualId

- **Field API Name:** `KQ_IndividualId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for IndividualId

### KQ_PrevInteractionId

- **Field API Name:** `KQ_PrevInteractionId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for PrevInteractionId

### KQ_TelemetryTraceSpanId

- **Field API Name:** `KQ_TelemetryTraceSpanId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for TelemetryTraceSpanId

### PrevInteractionId

- **Field API Name:** `ssot__PrevInteractionId__c`
- **Data Type:** TEXT
- **Description:** The ID of the previous interaction. The ID enables sequencing or chaining of interactions.

### SessionOwnerId

- **Field API Name:** `ssot__SessionOwnerId__c`
- **Data Type:** TEXT
- **Description:** The ID of the record for the participant who initiated (owned) the session.

### SessionOwnerObject

- **Field API Name:** `ssot__SessionOwnerObject__c`
- **Data Type:** TEXT
- **Description:** The name of the Data Model Object (DMO) the Session Owner record belongs to, for example, Individual.

### StartTimestamp

- **Field API Name:** `ssot__StartTimestamp__c`
- **Data Type:** DATETIME
- **Description:** The timestamp when the interaction began.

### TelemetryTraceId

- **Field API Name:** `ssot__TelemetryTraceId__c`
- **Data Type:** TEXT
- **Description:** An ID used for distributed tracing. The ID allows tracking of interactions across system components.

### TelemetryTraceSpanId

- **Field API Name:** `ssot__TelemetryTraceSpanId__c`
- **Data Type:** TEXT
- **Description:** The span ID for tracing this specific interaction within a larger distributed tracing context.

### TopicApiName

- **Field API Name:** `ssot__TopicApiName__c`
- **Data Type:** TEXT
- **Description:** The API name of the topic that was classified for the interaction.
