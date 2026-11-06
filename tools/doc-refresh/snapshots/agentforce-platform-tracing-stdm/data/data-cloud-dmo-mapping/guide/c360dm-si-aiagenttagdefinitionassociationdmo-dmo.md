# AI Agent Tag Definition Association DMO

## Object Properties

**Object API Name:** `ssot__AiAgentTagDefinitionAssociation__dlm`\
**Category:** Unassigned\
**Availability:** Available in 254 and later versions\
**Primary Key Field:** Id

## Relationships

- **AiAgentTagDefinitionId** has a FOREIGNKEY relationship with the [AI Agent Tag Definition DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagenttagdefinitiondmo-dmo.md) `Id` field.

## Fields

- [AiAgentApiName](#aiagentapiname)
- [AiAgentTagDefinitionId](#aiagenttagdefinitionid)
- [AiPromptTemplateId](#aiprompttemplateid)
- [cdp_sys_record_currency](#cdp_sys_record_currency)
- [CreatedDate](#createddate)
- [DataSourceId](#datasourceid)
- [DataSourceObjectId](#datasourceobjectid)
- [ExternalSourceId](#externalsourceid)
- [Id](#id)
- [InputScope](#inputscope)
- [InternalOrganizationId](#internalorganizationid)
- [IsActive](#isactive)
- [KQ_AiAgentTagDefinitionId](#kq_aiagenttagdefinitionid)
- [KQ_Id](#kq_id)

### AiAgentApiName

- **Field API Name:** `ssot__AiAgentApiName__c`
- **Data Type:** TEXT
- **Description:** The API Name of the AI Agent.

### AiAgentTagDefinitionId

- **Field API Name:** `ssot__AiAgentTagDefinitionId__c`
- **Data Type:** TEXT
- **Description:** The reference ID of an associated AI Agent Tag Definition.

### AiPromptTemplateId

- **Field API Name:** `ssot__AiPromptTemplateId__c`
- **Data Type:** TEXT
- **Description:** The reference ID of an associated AI Prompt Template.

### cdp_sys_record_currency

- **Field API Name:** `ssot__cdp_sys_record_currency__c`
- **Data Type:** TEXT
- **Description:** System-generated metadata field that stores a 3-letter ISO currency code.

### CreatedDate

- **Field API Name:** `ssot__CreatedDate__c`
- **Data Type:** DATETIME
- **Description:** The date and time when the record was created.

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
- **Description:** Required. A unique, system-generated identifier for the AiAgentTagDefinitionAssociation record. Maximum size is 255 characters.

### InputScope

- **Field API Name:** `ssot__InputScope__c`
- **Data Type:** TEXT
- **Description:** Specifies where this tag is applied, such as sessions, moments, or interactions.

### InternalOrganizationId

- **Field API Name:** `ssot__InternalOrganizationId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### IsActive

- **Field API Name:** `ssot__IsActive__c`
- **Data Type:** BOOLEAN
- **Description:** Indicates whether this record is active (true) or not (false).

### KQ_AiAgentTagDefinitionId

- **Field API Name:** `KQ_AiAgentTagDefinitionId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentTagDefinitionId

### KQ_Id

- **Field API Name:** `KQ_Id__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for Id
