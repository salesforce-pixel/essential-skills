# AI Agent Moment Interaction DMO

## Object Properties

**Object API Name:** `ssot__AiAgentMomentInteraction__dlm`\
**Category:** Unassigned\
**Availability:** Available in 254 and later versions\
**Primary Key Field:** Id

## Relationships

- **AiAgentMomentId** has a FOREIGNKEY relationship with the [AI Agent Moment DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentmomentdmo-dmo.md) `Id` field.
- **AiAgentInteractionId** has a FOREIGNKEY relationship with the [AI Agent Interaction DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentinteractiondmo-dmo.md) `Id` field.

## Fields

- [AiAgentInteractionId](#aiagentinteractionid)
- [AiAgentMomentId](#aiagentmomentid)
- [cdp_sys_record_currency](#cdp_sys_record_currency)
- [DataSourceId](#datasourceid)
- [DataSourceObjectId](#datasourceobjectid)
- [ExternalSourceId](#externalsourceid)
- [Id](#id)
- [InternalOrganizationId](#internalorganizationid)
- [KQ_AiAgentInteractionId](#kq_aiagentinteractionid)
- [KQ_AiAgentMomentId](#kq_aiagentmomentid)
- [KQ_Id](#kq_id)
- [StartTimestamp](#starttimestamp)

### AiAgentInteractionId

- **Field API Name:** `ssot__AiAgentInteractionId__c`
- **Data Type:** TEXT
- **Description:** The ID of a specific AI agent interaction.

### AiAgentMomentId

- **Field API Name:** `ssot__AiAgentMomentId__c`
- **Data Type:** TEXT
- **Description:** The ID of a specific AI Agent Moment.

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

### ExternalSourceId

- **Field API Name:** `ssot__ExternalSourceId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### Id

- **Field API Name:** `ssot__Id__c`
- **Data Type:** TEXT
- **Description:** Required. A unique, system-generated identifier for the AiAgentMomentInteraction record. Maximum size is 15 characters.

### InternalOrganizationId

- **Field API Name:** `ssot__InternalOrganizationId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### KQ_AiAgentInteractionId

- **Field API Name:** `KQ_AiAgentInteractionId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentInteractionId

### KQ_AiAgentMomentId

- **Field API Name:** `KQ_AiAgentMomentId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentMomentId

### KQ_Id

- **Field API Name:** `KQ_Id__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for Id

### StartTimestamp

- **Field API Name:** `ssot__StartTimestamp__c`
- **Data Type:** DATETIME
- **Description:** The timestamp when the user-agent interaction began.
