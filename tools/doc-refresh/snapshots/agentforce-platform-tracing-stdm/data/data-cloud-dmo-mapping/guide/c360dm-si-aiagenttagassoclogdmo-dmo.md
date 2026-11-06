# Ai Agent Tag Assoc Log DMO

Captures logs for AI agent tag association scoring.

:::note
This is a standard data model object (DMO), which is created in your org only after you map it. Until it's mapped, this DMO is visible on the data mapping screen but doesn't appear in the Data Model list or record view in the Data 360 app. This is expected behavior. To use this DMO, search for it on the data mapping screen and complete the mapping. After it's mapped, the DMO and its fields appear in the Data Model list.
:::

## Object Properties

**Object API Name:** `AiAgentTagAssocLog_std__dlm`\
**Category:** Unassigned\
**Availability:** Available in 262 and later versions\
**Primary Key Field:** Id

## Relationships

- **AiAgentSessionId** has a FOREIGNKEY relationship with the [AI Agent Session DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentsessiondmo-dmo.md) `Id` field.
- **AiAgentInteractionId** has a FOREIGNKEY relationship with the [AI Agent Interaction DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentinteractiondmo-dmo.md) `Id` field.
- **AiAgentMomentId** has a FOREIGNKEY relationship with the [AI Agent Moment DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentmomentdmo-dmo.md) `Id` field.
- **AiAgentTagDefinitionId** has a FOREIGNKEY relationship with the [AI Agent Tag Definition DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagenttagdefinitiondmo-dmo.md) `Id` field.
- **AiAgentTagId** has a FOREIGNKEY relationship with the [AI Agent Tag DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagenttagdmo-dmo.md) `Id` field.

## Fields

- [AiAgentApiName](#aiagentapiname)
- [AiAgentInteractionId](#aiagentinteractionid)
- [AiAgentMomentId](#aiagentmomentid)
- [AiAgentSessionId](#aiagentsessionid)
- [AiAgentSessionStartTimestamp](#aiagentsessionstarttimestamp)
- [AiAgentTagDefinitionId](#aiagenttagdefinitionid)
- [AiAgentTagId](#aiagenttagid)
- [Category](#category)
- [cdp_sys_record_currency](#cdp_sys_record_currency)
- [Code](#code)
- [DataSourceId](#datasourceid)
- [DataSourceObjectId](#datasourceobjectid)
- [ExternalSourceId](#externalsourceid)
- [Id](#id)
- [InternalOrganizationId](#internalorganizationid)
- [LogDateTime](#logdatetime)
- [LogLevel](#loglevel)
- [Message](#message)

### AiAgentApiName

- **Field API Name:** `AiAgentApiName__c`
- **Data Type:** TEXT
- **Description:** The API name of the agent associated with this log entry.

### AiAgentInteractionId

- **Field API Name:** `AiAgentInteractionId__c`
- **Data Type:** TEXT
- **Description:** The reference ID of an associated AI Agent Interaction.

### AiAgentMomentId

- **Field API Name:** `AiAgentMomentId__c`
- **Data Type:** TEXT
- **Description:** The reference ID of an associated AI Agent Moment.

### AiAgentSessionId

- **Field API Name:** `AiAgentSessionId__c`
- **Data Type:** TEXT
- **Description:** The reference ID of an associated AI Agent Session.

### AiAgentSessionStartTimestamp

- **Field API Name:** `AiAgentSessionStartTimestamp__c`
- **Data Type:** DATETIME
- **Description:** The timestamp when the originating AI agent session started.

### AiAgentTagDefinitionId

- **Field API Name:** `AiAgentTagDefinitionId__c`
- **Data Type:** TEXT
- **Description:** The reference ID of an associated AI Agent Tag Definition.

### AiAgentTagId

- **Field API Name:** `AiAgentTagId__c`
- **Data Type:** TEXT
- **Description:** The reference ID of an associated AI Agent Tag.

### Category

- **Field API Name:** `Category__c`
- **Data Type:** TEXT
- **Description:** The error category for grouping related errors.

### cdp_sys_record_currency

- **Field API Name:** `cdp_sys_record_currency__c`
- **Data Type:** TEXT
- **Description:** System-generated metadata field that stores a 3-letter ISO currency code.

### Code

- **Field API Name:** `Code__c`
- **Data Type:** TEXT
- **Description:** The error code identifier for this log entry.

### DataSourceId

- **Field API Name:** `DataSourceId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### DataSourceObjectId

- **Field API Name:** `DataSourceObjectId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### ExternalSourceId

- **Field API Name:** `ExternalSourceId__c`
- **Data Type:** TEXT
- **Description:** Organization identifier used for dataspace filtering.

### Id

- **Field API Name:** `Id__c`
- **Data Type:** TEXT
- **Description:** The primary key identifier for the AiAgentTagAssocLog record.

### InternalOrganizationId

- **Field API Name:** `InternalOrganizationId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### LogDateTime

- **Field API Name:** `LogDateTime__c`
- **Data Type:** DATETIME
- **Description:** The timestamp when this log entry was generated.

### LogLevel

- **Field API Name:** `LogLevel__c`
- **Data Type:** TEXT
- **Description:** The severity level of the log entry.

### Message

- **Field API Name:** `Message__c`
- **Data Type:** TEXT
- **Description:** A human-readable description of the error.
