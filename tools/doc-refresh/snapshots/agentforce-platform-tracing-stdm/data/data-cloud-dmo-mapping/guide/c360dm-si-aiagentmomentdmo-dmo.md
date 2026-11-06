# AI Agent Moment DMO

## Object Properties

**Object API Name:** `ssot__AiAgentMoment__dlm`\
**Category:** Unassigned\
**Availability:** Available in 254 and later versions\
**Primary Key Field:** Id

## Relationships

- **AiAgentSessionId** has a FOREIGNKEY relationship with the [AI Agent Session DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentsessiondmo-dmo.md) `Id` field.

## Fields

- [AiAgentApiName](#aiagentapiname)
- [AiAgentSessionId](#aiagentsessionid)
- [AiAgentVersionApiName](#aiagentversionapiname)
- [cdp_sys_record_currency](#cdp_sys_record_currency)
- [DataSourceId](#datasourceid)
- [DataSourceObjectId](#datasourceobjectid)
- [EndTimestamp](#endtimestamp)
- [ExternalSourceId](#externalsourceid)
- [Id](#id)
- [InternalOrganizationId](#internalorganizationid)
- [KQ_AiAgentSessionId](#kq_aiagentsessionid)
- [KQ_Id](#kq_id)
- [RequestSummaryText](#requestsummarytext)
- [ResponseSummaryText](#responsesummarytext)
- [StartTimestamp](#starttimestamp)

### AiAgentApiName

- **Field API Name:** `ssot__AiAgentApiName__c`
- **Data Type:** TEXT
- **Description:** The API Name of the AI agent.

### AiAgentSessionId

- **Field API Name:** `ssot__AiAgentSessionId__c`
- **Data Type:** TEXT
- **Description:** The ID for a specific AiAgentSession. An AiAgentSession ID can be asociated with one or more individual moments.

### AiAgentVersionApiName

- **Field API Name:** `ssot__AiAgentVersionApiName__c`
- **Data Type:** TEXT
- **Description:** The API Name of the AI agent version.

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
- **Description:** The timestamp when the AI Agent Moment ended.

### ExternalSourceId

- **Field API Name:** `ssot__ExternalSourceId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### Id

- **Field API Name:** `ssot__Id__c`
- **Data Type:** TEXT
- **Description:** Required. A unique, system-generated identifier for the AiAgentMoment record. Maximum size is 15 characters.

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

### RequestSummaryText

- **Field API Name:** `ssot__RequestSummaryText__c`
- **Data Type:** TEXT
- **Description:** A summary of the main points the user provided during a specific AI Agent Moment. The text highlights key requests and information shared.

### ResponseSummaryText

- **Field API Name:** `ssot__ResponseSummaryText__c`
- **Data Type:** TEXT
- **Description:** A summary of the AI agent's responses during a specific moment. The text captures key information provided and actions performed.

### StartTimestamp

- **Field API Name:** `ssot__StartTimestamp__c`
- **Data Type:** DATETIME
- **Description:** The timestamp when a specific AI Agent Moment within a session began.
