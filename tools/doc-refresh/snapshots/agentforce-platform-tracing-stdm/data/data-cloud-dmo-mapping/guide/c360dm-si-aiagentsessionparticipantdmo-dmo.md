# AI Agent Session Participant DMO

## Object Properties

**Object API Name:** `ssot__AiAgentSessionParticipant__dlm`\
**Category:** Unassigned\
**Availability:** Available in 254 and later versions\
**Primary Key Field:** Id

## Relationships

- **IndividualId** has a FOREIGNKEY relationship with the [Individual DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-individualdmo-dmo.md) `Id` field.
- **AiAgentSessionId** has a FOREIGNKEY relationship with the [AI Agent Session DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentsessiondmo-dmo.md) `Id` field.
- **ParticipantUserId** has a FOREIGNKEY relationship with the [User DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-userdmo-dmo.md) `Id` field.
- **ConversationId** has a FOREIGNKEY relationship with the [Conversation DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-conversationdmo-dmo.md) `Id` field.

## Fields

- [AiAgentApiName](#aiagentapiname)
- [AiAgentSessionId](#aiagentsessionid)
- [AiAgentSessionParticipantRole](#aiagentsessionparticipantrole)
- [AiAgentTemplateApiName](#aiagenttemplateapiname)
- [AiAgentType](#aiagenttype)
- [AiAgentVersionApiName](#aiagentversionapiname)
- [cdp_sys_record_currency](#cdp_sys_record_currency)
- [ConversationId](#conversationid)
- [DataSourceId](#datasourceid)
- [DataSourceObjectId](#datasourceobjectid)
- [EndTimestamp](#endtimestamp)
- [ExternalSourceId](#externalsourceid)
- [Id](#id)
- [IndividualId](#individualid)
- [InternalOrganizationId](#internalorganizationid)
- [KQ_AiAgentSessionId](#kq_aiagentsessionid)
- [KQ_ConversationId](#kq_conversationid)
- [KQ_Id](#kq_id)
- [KQ_IndividualId](#kq_individualid)
- [KQ_ParticipantUserId](#kq_participantuserid)
- [ParticipantAttributeText](#participantattributetext)
- [ParticipantId](#participantid)
- [ParticipantObject](#participantobject)
- [ParticipantUserId](#participantuserid)
- [StartTimestamp](#starttimestamp)

### AiAgentApiName

- **Field API Name:** `ssot__AiAgentApiName__c`
- **Data Type:** TEXT
- **Description:** The API name of the AI agent. This field is populated only if the participant is an AI agent.

### AiAgentSessionId

- **Field API Name:** `ssot__AiAgentSessionId__c`
- **Data Type:** TEXT
- **Description:** The ID of the specific AI Agent Session this participant is involved in.

### AiAgentSessionParticipantRole

- **Field API Name:** `ssot__AiAgentSessionParticipantRole__c`
- **Data Type:** TEXT
- **Description:** The role of the participant within the session, for example, Owner or Observer.

### AiAgentTemplateApiName

- **Field API Name:** `ssot__AiAgentTemplateApiName__c`
- **Data Type:** TEXT
- **Description:** The template that was used to create the agent.

### AiAgentType

- **Field API Name:** `ssot__AiAgentType__c`
- **Data Type:** TEXT
- **Description:** The type of the AI Agent. Valid values include Employee, EinsteinSDR, and EinsteinServiceAgent.

### AiAgentVersionApiName

- **Field API Name:** `ssot__AiAgentVersionApiName__c`
- **Data Type:** TEXT
- **Description:** The API name of the AI agent version. This field is populated only if the participant is an AI agent.

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
- **Description:** The timestamp when the participant left or stopped interacting in the session.

### ExternalSourceId

- **Field API Name:** `ssot__ExternalSourceId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### Id

- **Field API Name:** `ssot__Id__c`
- **Data Type:** TEXT
- **Description:** Required. A unique, system-generated identifier for the AiAgentSessionParticipant record. Maximum size is 15 characters.

### IndividualId

- **Field API Name:** `ssot__IndividualId__c`
- **Data Type:** TEXT
- **Description:** The ID of an Individual record that represents the participant. This field is populated only if the type of the participant record's Data Model Object (DMO) is Individual.

### InternalOrganizationId

- **Field API Name:** `ssot__InternalOrganizationId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### KQ_AiAgentSessionId

- **Field API Name:** `KQ_AiAgentSessionId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentSessionId

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

### KQ_ParticipantUserId

- **Field API Name:** `KQ_ParticipantUserId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for ParticipantUserId

### ParticipantAttributeText

- **Field API Name:** `ssot__ParticipantAttributeText__c`
- **Data Type:** TEXT
- **Description:** JSON key-value pairs for additional metadata or attributes of the participant specific to this session.

### ParticipantId

- **Field API Name:** `ssot__ParticipantId__c`
- **Data Type:** TEXT
- **Description:** The ID of the record for the participant involved in the session.

### ParticipantObject

- **Field API Name:** `ssot__ParticipantObject__c`
- **Data Type:** TEXT
- **Description:** The name of the Data Model Object (DMO) the Participant record belongs to, for example, Individual.

### ParticipantUserId

- **Field API Name:** `ssot__ParticipantUserId__c`
- **Data Type:** TEXT
- **Description:** Reference to the User record that represents the participant. Populated only if the participant record's DMO type is User.

### StartTimestamp

- **Field API Name:** `ssot__StartTimestamp__c`
- **Data Type:** DATETIME
- **Description:** The timestamp when the participant joined the session.
