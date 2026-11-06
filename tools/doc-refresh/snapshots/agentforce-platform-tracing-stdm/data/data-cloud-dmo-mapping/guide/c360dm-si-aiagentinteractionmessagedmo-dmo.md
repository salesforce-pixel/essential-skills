# AI Agent Interaction Message DMO

## Object Properties

**Object API Name:** `ssot__AiAgentInteractionMessage__dlm`\
**Category:** Unassigned\
**Availability:** Available in 254 and later versions\
**Primary Key Field:** Id

## Relationships

- **AiAgentSessionParticipantId** has a FOREIGNKEY relationship with the [AI Agent Session Participant DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentsessionparticipantdmo-dmo.md) `Id` field.
- **AiAgentSessionId** has a FOREIGNKEY relationship with the [AI Agent Session DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentsessiondmo-dmo.md) `Id` field.
- **AiAgentInteractionId** has a FOREIGNKEY relationship with the [AI Agent Interaction DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentinteractiondmo-dmo.md) `Id` field.
- **IndividualId** has a FOREIGNKEY relationship with the [Individual DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-individualdmo-dmo.md) `Id` field.
- **ParentMessageId** has a FOREIGNKEY relationship with the [AI Agent Interaction Message DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentinteractionmessagedmo-dmo.md) `Id` field.
- **ParticipantUserId** has a FOREIGNKEY relationship with the [User DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-userdmo-dmo.md) `Id` field.
- **ConversationId** has a FOREIGNKEY relationship with the [Conversation DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-conversationdmo-dmo.md) `Id` field.

## Fields

- [AiAgentInteractionId](#aiagentinteractionid)
- [AiAgentInteractionMessageType](#aiagentinteractionmessagetype)
- [AiAgentInteractionMsgContentType](#aiagentinteractionmsgcontenttype)
- [AiAgentSessionId](#aiagentsessionid)
- [AiAgentSessionParticipantId](#aiagentsessionparticipantid)
- [AttributeText](#attributetext)
- [cdp_sys_record_currency](#cdp_sys_record_currency)
- [ContentText](#contenttext)
- [ConversationId](#conversationid)
- [DataSourceId](#datasourceid)
- [DataSourceObjectId](#datasourceobjectid)
- [ExternalSourceId](#externalsourceid)
- [Id](#id)
- [IndividualId](#individualid)
- [InternalOrganizationId](#internalorganizationid)
- [KQ_AiAgentInteractionId](#kq_aiagentinteractionid)
- [KQ_AiAgentSessionId](#kq_aiagentsessionid)
- [KQ_AiAgentSessionParticipantId](#kq_aiagentsessionparticipantid)
- [KQ_ConversationId](#kq_conversationid)
- [KQ_Id](#kq_id)
- [KQ_IndividualId](#kq_individualid)
- [KQ_ParentMessageId](#kq_parentmessageid)
- [KQ_ParticipantUserId](#kq_participantuserid)
- [MessageEndTimestamp](#messageendtimestamp)
- [MessageSentTimestamp](#messagesenttimestamp)
- [MessageStartTimestamp](#messagestarttimestamp)
- [Modality](#modality)
- [ParentMessageId](#parentmessageid)
- [ParticipantUserId](#participantuserid)
- [SessionOwnerId](#sessionownerid)
- [SessionOwnerObject](#sessionownerobject)

### AiAgentInteractionId

- **Field API Name:** `ssot__AiAgentInteractionId__c`
- **Data Type:** TEXT
- **Description:** The ID of the interaction this message belongs to.

### AiAgentInteractionMessageType

- **Field API Name:** `ssot__AiAgentInteractionMessageType__c`
- **Data Type:** TEXT
- **Description:** The type of the message, for example, Input or Output.

### AiAgentInteractionMsgContentType

- **Field API Name:** `ssot__AiAgentInteractionMsgContentType__c`
- **Data Type:** TEXT
- **Description:** A description of the format or type of the message content. Possible values include text/plain, application/json, and audio/wav.

### AiAgentSessionId

- **Field API Name:** `ssot__AiAgentSessionId__c`
- **Data Type:** TEXT
- **Description:** The ID of the session this message belongs to.

### AiAgentSessionParticipantId

- **Field API Name:** `ssot__AiAgentSessionParticipantId__c`
- **Data Type:** TEXT
- **Description:** The ID of the participant who sent the message.

### AttributeText

- **Field API Name:** `ssot__AttributeText__c`
- **Data Type:** TEXT
- **Description:** JSON key-value pairs storing per-word transcription attributes including confidence scores and timestamps for the message.

### cdp_sys_record_currency

- **Field API Name:** `ssot__cdp_sys_record_currency__c`
- **Data Type:** TEXT
- **Description:** System-generated metadata field that stores a 3-letter ISO currency code.

### ContentText

- **Field API Name:** `ssot__ContentText__c`
- **Data Type:** TEXT
- **Description:** Direct textual content if the message is text-based.

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

### ExternalSourceId

- **Field API Name:** `ssot__ExternalSourceId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### Id

- **Field API Name:** `ssot__Id__c`
- **Data Type:** TEXT
- **Description:** Required. A unique, system-generated identifier for the AiAgentInteractionMessage record. Maximum size is 15 characters.

### IndividualId

- **Field API Name:** `ssot__IndividualId__c`
- **Data Type:** TEXT
- **Description:** The ID of an Individual record that represents the session owner participant. This field is populated only if the SessionOwnerObject is Individual.

### InternalOrganizationId

- **Field API Name:** `ssot__InternalOrganizationId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### KQ_AiAgentInteractionId

- **Field API Name:** `KQ_AiAgentInteractionId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentInteractionId

### KQ_AiAgentSessionId

- **Field API Name:** `KQ_AiAgentSessionId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentSessionId

### KQ_AiAgentSessionParticipantId

- **Field API Name:** `KQ_AiAgentSessionParticipantId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentSessionParticipantId

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

### KQ_ParentMessageId

- **Field API Name:** `KQ_ParentMessageId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for ParentMessageId

### KQ_ParticipantUserId

- **Field API Name:** `KQ_ParticipantUserId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for ParticipantUserId

### MessageEndTimestamp

- **Field API Name:** `ssot__MessageEndTimestamp__c`
- **Data Type:** DATETIME
- **Description:** The exact time the message was ended.

### MessageSentTimestamp

- **Field API Name:** `ssot__MessageSentTimestamp__c`
- **Data Type:** DATETIME
- **Description:** The exact time the message was sent.

### MessageStartTimestamp

- **Field API Name:** `ssot__MessageStartTimestamp__c`
- **Data Type:** DATETIME
- **Description:** The exact time the message was started.

### Modality

- **Field API Name:** `ssot__Modality__c`
- **Data Type:** TEXT
- **Description:** The message is in voice or text mode.

### ParentMessageId

- **Field API Name:** `ssot__ParentMessageId__c`
- **Data Type:** TEXT
- **Description:** The ID of another message if this message is a reply or continuation.

### ParticipantUserId

- **Field API Name:** `ssot__ParticipantUserId__c`
- **Data Type:** TEXT
- **Description:** Reference to the User record that represents the participant. Populated only if the participant record's DMO type is User.

### SessionOwnerId

- **Field API Name:** `ssot__SessionOwnerId__c`
- **Data Type:** TEXT
- **Description:** The ID of the record of the participant who initiated the session.

### SessionOwnerObject

- **Field API Name:** `ssot__SessionOwnerObject__c`
- **Data Type:** TEXT
- **Description:** The name of the Data Model Object (DMO) the Session Owner record belongs to, for example, Individual.
