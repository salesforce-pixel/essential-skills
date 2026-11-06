# AI Agent Session DMO

## Object Properties

**Object API Name:** `ssot__AiAgentSession__dlm`\
**Category:** Unassigned\
**Availability:** Available in 254 and later versions\
**Primary Key Field:** Id

## Relationships

- **IndividualId** has a FOREIGNKEY relationship with the [Individual DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-individualdmo-dmo.md) `Id` field.
- **RelatedVoiceCallId** has a FOREIGNKEY relationship with the [Voice Call DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-voicecalldmo-dmo.md) `Id` field.
- **PreviousSessionId** has a FOREIGNKEY relationship with the [AI Agent Session DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentsessiondmo-dmo.md) `Id` field.
- **OwnerUserId** has a FOREIGNKEY relationship with the [User DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-userdmo-dmo.md) `Id` field.
- **ConversationId** has a FOREIGNKEY relationship with the [Conversation DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-conversationdmo-dmo.md) `Id` field.

## Fields

- [AiAgentChannelType](#aiagentchanneltype)
- [AiAgentSessionEndType](#aiagentsessionendtype)
- [cdp_sys_record_currency](#cdp_sys_record_currency)
- [ConversationId](#conversationid)
- [DataSourceId](#datasourceid)
- [DataSourceObjectId](#datasourceobjectid)
- [EndTimestamp](#endtimestamp)
- [ExternalSourceId](#externalsourceid)
- [Id](#id)
- [IndividualId](#individualid)
- [InternalOrganizationId](#internalorganizationid)
- [KQ_ConversationId](#kq_conversationid)
- [KQ_Id](#kq_id)
- [KQ_IndividualId](#kq_individualid)
- [KQ_OwnerUserId](#kq_owneruserid)
- [KQ_PreviousSessionId](#kq_previoussessionid)
- [KQ_RelatedVoiceCallId](#kq_relatedvoicecallid)
- [OwnerUserId](#owneruserid)
- [PreviousSessionId](#previoussessionid)
- [RelatedMessagingSessionId](#relatedmessagingsessionid)
- [RelatedVoiceCallId](#relatedvoicecallid)
- [SessionOwnerId](#sessionownerid)
- [SessionOwnerObject](#sessionownerobject)
- [StartTimestamp](#starttimestamp)
- [VariableText](#variabletext)

### AiAgentChannelType

- **Field API Name:** `ssot__AiAgentChannelType__c`
- **Data Type:** TEXT
- **Description:** The type of the communication channel through which the session was initiated.

### AiAgentSessionEndType

- **Field API Name:** `ssot__AiAgentSessionEndType__c`
- **Data Type:** TEXT
- **Description:** The reason the session ended. Possible values are resolved, escalated, deflected, and other.

### cdp_sys_record_currency

- **Field API Name:** `ssot__cdp_sys_record_currency__c`
- **Data Type:** TEXT
- **Description:** System-generated metadata field that stores a 3-letter ISO currency code.

### ConversationId

- **Field API Name:** `ssot__ConversationId__c`
- **Data Type:** TEXT
- **Description:** Optional foreign-key relationship with the Conversation Entity.

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
- **Description:** The timestamp when the session concluded or timed out.

### ExternalSourceId

- **Field API Name:** `ssot__ExternalSourceId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### Id

- **Field API Name:** `ssot__Id__c`
- **Data Type:** TEXT
- **Description:** Required. A unique, system-generated identifier for the AiAgentSession record. Maximum size is 15 characters.

### IndividualId

- **Field API Name:** `ssot__IndividualId__c`
- **Data Type:** TEXT
- **Description:** The ID of the Individual record for the session owner participant. This field is populated only if the type of the Session Owner Object is Individual.

### InternalOrganizationId

- **Field API Name:** `ssot__InternalOrganizationId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### KQ_ConversationId

- **Field API Name:** `KQ_ConversationId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for ConversationId

### KQ_Id

- **Field API Name:** `KQ_Id__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for Id

### KQ_IndividualId

- **Field API Name:** `KQ_IndividualId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for IndividualId

### KQ_OwnerUserId

- **Field API Name:** `KQ_OwnerUserId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for OwnerUserId

### KQ_PreviousSessionId

- **Field API Name:** `KQ_PreviousSessionId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for PreviousSessionId

### KQ_RelatedVoiceCallId

- **Field API Name:** `KQ_RelatedVoiceCallId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for RelatedVoiceCallId

### OwnerUserId

- **Field API Name:** `ssot__OwnerUserId__c`
- **Data Type:** TEXT
- **Description:** Reference to the User record that represents the participant. Populated only if the participant record's DMO type is User.

### PreviousSessionId

- **Field API Name:** `ssot__PreviousSessionId__c`
- **Data Type:** TEXT
- **Description:** The ID of the previous AI agent session in a multi-agent scenario.

### RelatedMessagingSessionId

- **Field API Name:** `ssot__RelatedMessagingSessionId__c`
- **Data Type:** TEXT
- **Description:** An ID that links the AI agent session to the messaging session from which it was initiated.

### RelatedVoiceCallId

- **Field API Name:** `ssot__RelatedVoiceCallId__c`
- **Data Type:** TEXT
- **Description:** An ID that links the session to the voice call from which it was initiated.

### SessionOwnerId

- **Field API Name:** `ssot__SessionOwnerId__c`
- **Data Type:** TEXT
- **Description:** The ID of the record of the participant who initiated the session.

### SessionOwnerObject

- **Field API Name:** `ssot__SessionOwnerObject__c`
- **Data Type:** TEXT
- **Description:** The name of the Data Model Object (DMO) the Session Owner record belongs to, for example, Individual.

### StartTimestamp

- **Field API Name:** `ssot__StartTimestamp__c`
- **Data Type:** DATETIME
- **Description:** The timestamp when the session was initiated.

### VariableText

- **Field API Name:** `ssot__VariableText__c`
- **Data Type:** TEXT
- **Description:** JSON key-value pairs for contextual session data used by agents during interactions.
