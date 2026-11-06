# Ai Agent Session Attachment DMO

Stores metadata and file paths for attachments linked to AI Agent Sessions.

:::note
This is a standard data model object (DMO), which is created in your org only after you map it. Until it's mapped, this DMO is visible on the data mapping screen but doesn't appear in the Data Model list or record view in the Data 360 app. This is expected behavior. To use this DMO, search for it on the data mapping screen and complete the mapping. After it's mapped, the DMO and its fields appear in the Data Model list.
:::

## Object Properties

**Object API Name:** `AiAgentSessionAttachment_std__dlm`\
**Category:** Unassigned\
**Availability:** Available in 260 and later versions\
**Primary Key Field:** Id

## Relationships

- **AiAgentSessionId** has a FOREIGNKEY relationship with the [AI Agent Session DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentsessiondmo-dmo.md) `Id` field.

## Fields

- [AiAgentSessionId](#aiagentsessionid)
- [cdp_sys_record_currency](#cdp_sys_record_currency)
- [ContentDocumentVersionId](#contentdocumentversionid)
- [CreatedTimestamp](#createdtimestamp)
- [DataSourceId](#datasourceid)
- [DataSourceObjectId](#datasourceobjectid)
- [ExternalSourceId](#externalsourceid)
- [FilePathName](#filepathname)
- [FileType](#filetype)
- [Id](#id)
- [InternalOrganizationId](#internalorganizationid)
- [KQ_AiAgentSessionId](#kq_aiagentsessionid)
- [KQ_Id](#kq_id)
- [SourceName](#sourcename)

### AiAgentSessionId

- **Field API Name:** `AiAgentSessionId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### cdp_sys_record_currency

- **Field API Name:** `cdp_sys_record_currency__c`
- **Data Type:** TEXT
- **Description:** System-generated metadata field that stores a 3-letter ISO currency code.

### ContentDocumentVersionId

- **Field API Name:** `ContentDocumentVersionId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### CreatedTimestamp

- **Field API Name:** `CreatedTimestamp__c`
- **Data Type:** DATETIME
- **Description:** The date and time of the created timestamp.

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
- **Description:** A unique, system-generated identifier for this record.

### FilePathName

- **Field API Name:** `FilePathName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the file path name.

### FileType

- **Field API Name:** `FileType__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the file type.

### Id

- **Field API Name:** `Id__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### InternalOrganizationId

- **Field API Name:** `InternalOrganizationId__c`
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

### SourceName

- **Field API Name:** `SourceName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the source name.
