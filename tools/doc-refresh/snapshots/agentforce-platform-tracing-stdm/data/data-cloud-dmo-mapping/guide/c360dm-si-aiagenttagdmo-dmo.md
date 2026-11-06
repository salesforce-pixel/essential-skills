# AI Agent Tag DMO

## Object Properties

**Object API Name:** `ssot__AiAgentTag__dlm`\
**Category:** Unassigned\
**Availability:** Available in 254 and later versions\
**Primary Key Field:** Id

## Relationships

- **AiAgentTagDefinitionId** has a FOREIGNKEY relationship with the [AI Agent Tag Definition DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagenttagdefinitiondmo-dmo.md) `Id` field.

## Fields

- [AiAgentTagDefinitionId](#aiagenttagdefinitionid)
- [cdp_sys_record_currency](#cdp_sys_record_currency)
- [CreatedDate](#createddate)
- [DataSourceId](#datasourceid)
- [DataSourceObjectId](#datasourceobjectid)
- [Description](#description)
- [ExternalSourceId](#externalsourceid)
- [Id](#id)
- [InternalOrganizationId](#internalorganizationid)
- [IsActive](#isactive)
- [IsFallback](#isfallback)
- [KQ_AiAgentTagDefinitionId](#kq_aiagenttagdefinitionid)
- [KQ_Id](#kq_id)
- [OrderNumber](#ordernumber)
- [Value](#value)

### AiAgentTagDefinitionId

- **Field API Name:** `ssot__AiAgentTagDefinitionId__c`
- **Data Type:** TEXT
- **Description:** The reference ID of an associated AI Agent Tag Definition.

### cdp_sys_record_currency

- **Field API Name:** `ssot__cdp_sys_record_currency__c`
- **Data Type:** TEXT
- **Description:** System-generated metadata field that stores a 3-letter ISO currency code.

### CreatedDate

- **Field API Name:** `ssot__CreatedDate__c`
- **Data Type:** DATETIME
- **Description:** The date when the record for the AI Agent Tag was created.

### DataSourceId

- **Field API Name:** `ssot__DataSourceId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### DataSourceObjectId

- **Field API Name:** `ssot__DataSourceObjectId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### Description

- **Field API Name:** `ssot__Description__c`
- **Data Type:** TEXT
- **Description:** Additional information about the AI Agent Tag.

### ExternalSourceId

- **Field API Name:** `ssot__ExternalSourceId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### Id

- **Field API Name:** `ssot__Id__c`
- **Data Type:** TEXT
- **Description:** Required. A unique, system-generated identifier for the AiAgentTag record. Maximum size is 15 characters.

### InternalOrganizationId

- **Field API Name:** `ssot__InternalOrganizationId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### IsActive

- **Field API Name:** `ssot__IsActive__c`
- **Data Type:** BOOLEAN
- **Description:** Whether the tag is currently active (true) or not (false).

### IsFallback

- **Field API Name:** `ssot__IsFallback__c`
- **Data Type:** BOOLEAN
- **Description:** Indicates whether this record is fallback (true) or not (false).

### KQ_AiAgentTagDefinitionId

- **Field API Name:** `KQ_AiAgentTagDefinitionId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentTagDefinitionId

### KQ_Id

- **Field API Name:** `KQ_Id__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for Id

### OrderNumber

- **Field API Name:** `ssot__OrderNumber__c`
- **Data Type:** DOUBLE
- **Description:** Numeric value representing the order number. Do not include currency symbols or commas.

### Value

- **Field API Name:** `ssot__Value__c`
- **Data Type:** TEXT
- **Description:** The value assigned to the AI Agent Tag.
