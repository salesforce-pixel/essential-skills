# AI Agent Tag Association DMO

## Object Properties

**Object API Name:** `ssot__AiAgentTagAssociation__dlm`\
**Category:** Unassigned\
**Availability:** Available in 254 and later versions\
**Primary Key Field:** Id

## Relationships

- **AiAgentSessionId** has a FOREIGNKEY relationship with the [AI Agent Session DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentsessiondmo-dmo.md) `Id` field.
- **AiAgentMomentId** has a FOREIGNKEY relationship with the [AI Agent Moment DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentmomentdmo-dmo.md) `Id` field.
- **AiAgentTagId** has a FOREIGNKEY relationship with the [AI Agent Tag DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagenttagdmo-dmo.md) `Id` field.
- **AiAgentTagDefinitionAssociationId** has a FOREIGNKEY relationship with the [AI Agent Tag Definition Association DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagenttagdefinitionassociationdmo-dmo.md) `Id` field.
- **AiAgentInteractionId** has a FOREIGNKEY relationship with the [AI Agent Interaction DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentinteractiondmo-dmo.md) `Id` field.

## Fields

- [AiAgentInteractionId](#aiagentinteractionid)
- [AiAgentMomentId](#aiagentmomentid)
- [AiAgentSessionId](#aiagentsessionid)
- [AiAgentSessionStartTimestamp](#aiagentsessionstarttimestamp)
- [AiAgentTagDefinitionAssociationId](#aiagenttagdefinitionassociationid)
- [AiAgentTagId](#aiagenttagid)
- [AssociationReasonText](#associationreasontext)
- [AttributeText](#attributetext)
- [cdp_sys_record_currency](#cdp_sys_record_currency)
- [CreatedByUserId](#createdbyuserid)
- [CreatedDate](#createddate)
- [DataSourceId](#datasourceid)
- [DataSourceObjectId](#datasourceobjectid)
- [ExternalSourceId](#externalsourceid)
- [Id](#id)
- [InternalOrganizationId](#internalorganizationid)
- [IsPassed](#ispassed)
- [KQ_AiAgentInteractionId](#kq_aiagentinteractionid)
- [KQ_AiAgentMomentId](#kq_aiagentmomentid)
- [KQ_AiAgentSessionId](#kq_aiagentsessionid)
- [KQ_AiAgentTagDefinitionAssociationId](#kq_aiagenttagdefinitionassociationid)
- [KQ_AiAgentTagId](#kq_aiagenttagid)
- [KQ_Id](#kq_id)
- [OutcomeType](#outcometype)
- [SourceType](#sourcetype)
- [ValueText](#valuetext)

### AiAgentInteractionId

- **Field API Name:** `ssot__AiAgentInteractionId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### AiAgentMomentId

- **Field API Name:** `ssot__AiAgentMomentId__c`
- **Data Type:** TEXT
- **Description:** The reference ID of an associated AI Agent Moment.

### AiAgentSessionId

- **Field API Name:** `ssot__AiAgentSessionId__c`
- **Data Type:** TEXT
- **Description:** The reference ID of an associated AI Agent Session.

### AiAgentSessionStartTimestamp

- **Field API Name:** `ssot__AiAgentSessionStartTimestamp__c`
- **Data Type:** DATETIME
- **Description:** The timestamp when the originating AI agent session started.

### AiAgentTagDefinitionAssociationId

- **Field API Name:** `ssot__AiAgentTagDefinitionAssociationId__c`
- **Data Type:** TEXT
- **Description:** The reference ID of an associated AI Agent Tag Defintion Assocation.

### AiAgentTagId

- **Field API Name:** `ssot__AiAgentTagId__c`
- **Data Type:** TEXT
- **Description:** The reference ID of an associated AI Agent Tag.

### AssociationReasonText

- **Field API Name:** `ssot__AssociationReasonText__c`
- **Data Type:** TEXT
- **Description:** The reason a moment or session received a specific tag.

### AttributeText

- **Field API Name:** `ssot__AttributeText__c`
- **Data Type:** TEXT
- **Description:** JSON key-value pairs storing additional metadata or contextual information specific to the tag association.

### cdp_sys_record_currency

- **Field API Name:** `ssot__cdp_sys_record_currency__c`
- **Data Type:** TEXT
- **Description:** System-generated metadata field that stores a 3-letter ISO currency code.

### CreatedByUserId

- **Field API Name:** `ssot__CreatedByUserId__c`
- **Data Type:** TEXT
- **Description:** The ID of the user who created the record.

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
- **Description:** Required. A unique, system-generated identifier for the AiAgentTagAssociation record. Maximum size is 15 characters.

### InternalOrganizationId

- **Field API Name:** `ssot__InternalOrganizationId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### IsPassed

- **Field API Name:** `ssot__IsPassed__c`
- **Data Type:** BOOLEAN
- **Description:** Indicates whether this record is passed (true) or not (false).

### KQ_AiAgentInteractionId

- **Field API Name:** `KQ_AiAgentInteractionId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentInteractionId

### KQ_AiAgentMomentId

- **Field API Name:** `KQ_AiAgentMomentId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentMomentId

### KQ_AiAgentSessionId

- **Field API Name:** `KQ_AiAgentSessionId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentSessionId

### KQ_AiAgentTagDefinitionAssociationId

- **Field API Name:** `KQ_AiAgentTagDefinitionAssociationId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentTagDefinitionAssociationId

### KQ_AiAgentTagId

- **Field API Name:** `KQ_AiAgentTagId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentTagId

### KQ_Id

- **Field API Name:** `KQ_Id__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for Id

### OutcomeType

- **Field API Name:** `ssot__OutcomeType__c`
- **Data Type:** TEXT
- **Description:** Indicates the tag association verdict: pass, fail, or not applicable.

### SourceType

- **Field API Name:** `ssot__SourceType__c`
- **Data Type:** TEXT
- **Description:** The source of the tag association, indicating whether it was generated by the Annotation UI, API, PromptTemplate, or a Formula.

### ValueText

- **Field API Name:** `ssot__ValueText__c`
- **Data Type:** TEXT
- **Description:** The value of the tag association.
