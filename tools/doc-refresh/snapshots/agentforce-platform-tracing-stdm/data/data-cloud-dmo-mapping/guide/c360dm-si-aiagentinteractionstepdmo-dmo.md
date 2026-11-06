# AI Agent Interaction Step DMO

## Object Properties

**Object API Name:** `ssot__AiAgentInteractionStep__dlm`\
**Category:** Unassigned\
**Availability:** Available in 254 and later versions\
**Primary Key Field:** Id

## Relationships

- **TelemetryTraceSpanId** has a FOREIGNKEY relationship with the [Telemetry Trace Span DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-telemetrytracespandmo-dmo.md) `Id` field.
- **AiAgentInteractionId** has a FOREIGNKEY relationship with the [AI Agent Interaction DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentinteractiondmo-dmo.md) `Id` field.
- **PrevStepId** has a FOREIGNKEY relationship with the [AI Agent Interaction Step DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentinteractionstepdmo-dmo.md) `Id` field.
- **ParticipantIndividualId** has a FOREIGNKEY relationship with the [Individual DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-individualdmo-dmo.md) `Id` field.
- **ParticipantUserId** has a FOREIGNKEY relationship with the [User DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-userdmo-dmo.md) `Id` field.
- **ConversationId** has a FOREIGNKEY relationship with the [Conversation DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-conversationdmo-dmo.md) `Id` field.
- **SessionId** has a FOREIGNKEY relationship with the [AI Agent Session DMO](/docs/data/data-cloud-dmo-mapping/guide/c360dm-si-aiagentsessiondmo-dmo.md) `Id` field.

## Fields

- [AiAgentInteractionId](#aiagentinteractionid)
- [AiAgentInteractionStepType](#aiagentinteractionsteptype)
- [AttributeText](#attributetext)
- [cdp_sys_record_currency](#cdp_sys_record_currency)
- [ConversationId](#conversationid)
- [DataSourceId](#datasourceid)
- [DataSourceObjectId](#datasourceobjectid)
- [EndTimestamp](#endtimestamp)
- [ErrorMessageText](#errormessagetext)
- [ExternalSourceId](#externalsourceid)
- [GenAiGatewayRequestId](#genaigatewayrequestid)
- [GenAiGatewayResponseId](#genaigatewayresponseid)
- [GenerationId](#generationid)
- [Id](#id)
- [InputValueText](#inputvaluetext)
- [InternalOrganizationId](#internalorganizationid)
- [KQ_AiAgentInteractionId](#kq_aiagentinteractionid)
- [KQ_ConversationId](#kq_conversationid)
- [KQ_Id](#kq_id)
- [KQ_ParticipantIndividualId](#kq_participantindividualid)
- [KQ_ParticipantUserId](#kq_participantuserid)
- [KQ_PrevStepId](#kq_prevstepid)
- [KQ_SessionId](#kq_sessionid)
- [KQ_TelemetryTraceSpanId](#kq_telemetrytracespanid)
- [Name](#name)
- [OutputValueText](#outputvaluetext)
- [ParticipantIndividualId](#participantindividualid)
- [ParticipantUserId](#participantuserid)
- [PostStepVariableText](#poststepvariabletext)
- [PreStepVariableText](#prestepvariabletext)
- [PrevStepId](#prevstepid)
- [SessionId](#sessionid)
- [StartTimestamp](#starttimestamp)
- [SubType](#subtype)
- [TelemetryTraceSpanId](#telemetrytracespanid)
- [TopicApiName](#topicapiname)

### AiAgentInteractionId

- **Field API Name:** `ssot__AiAgentInteractionId__c`
- **Data Type:** TEXT
- **Description:** The ID of the interaction this step belongs to.

### AiAgentInteractionStepType

- **Field API Name:** `ssot__AiAgentInteractionStepType__c`
- **Data Type:** TEXT
- **Description:** The category of the step type. Possible values include UserInputStep, LLMExecutionStep, and FunctionStep.

### AttributeText

- **Field API Name:** `ssot__AttributeText__c`
- **Data Type:** TEXT
- **Description:** JSON key-value pairs that store additional metadata or properties of the step.

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
- **Description:** The timestamp when execution of the step completed.

### ErrorMessageText

- **Field API Name:** `ssot__ErrorMessageText__c`
- **Data Type:** TEXT
- **Description:** Error details for the step if step execution encountered issues or exceptions.

### ExternalSourceId

- **Field API Name:** `ssot__ExternalSourceId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### GenAiGatewayRequestId

- **Field API Name:** `ssot__GenAiGatewayRequestId__c`
- **Data Type:** TEXT
- **Description:** The ID of a GenAiGatewayRequest record if the step involved making an LLM generation request.

### GenAiGatewayResponseId

- **Field API Name:** `ssot__GenAiGatewayResponseId__c`
- **Data Type:** TEXT
- **Description:** The ID of a GenAiGatewayResponse record if the step involved making an LLM generation request.

### GenerationId

- **Field API Name:** `ssot__GenerationId__c`
- **Data Type:** TEXT
- **Description:** The ID of a GenAiGeneration record if the step involved making an LLM generation request.

### Id

- **Field API Name:** `ssot__Id__c`
- **Data Type:** TEXT
- **Description:** Required. A unique, system-generated identifier for the AiAgentInteractionStep record. Maximum size is 15 characters.

### InputValueText

- **Field API Name:** `ssot__InputValueText__c`
- **Data Type:** TEXT
- **Description:** The input data provided to the step.

### InternalOrganizationId

- **Field API Name:** `ssot__InternalOrganizationId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### KQ_AiAgentInteractionId

- **Field API Name:** `KQ_AiAgentInteractionId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for AiAgentInteractionId

### KQ_ConversationId

- **Field API Name:** `KQ_ConversationId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for ConversationId

### KQ_Id

- **Field API Name:** `KQ_Id__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for Id

### KQ_ParticipantIndividualId

- **Field API Name:** `KQ_ParticipantIndividualId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for ParticipantIndividualId

### KQ_ParticipantUserId

- **Field API Name:** `KQ_ParticipantUserId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for ParticipantUserId

### KQ_PrevStepId

- **Field API Name:** `KQ_PrevStepId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for PrevStepId

### KQ_SessionId

- **Field API Name:** `KQ_SessionId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for SessionId

### KQ_TelemetryTraceSpanId

- **Field API Name:** `KQ_TelemetryTraceSpanId__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for TelemetryTraceSpanId

### Name

- **Field API Name:** `ssot__Name__c`
- **Data Type:** TEXT
- **Description:** The name of the step performed by the AI Agent. For example, if the step type is an action, Name is the Action Name.

### OutputValueText

- **Field API Name:** `ssot__OutputValueText__c`
- **Data Type:** TEXT
- **Description:** The output data of the step's execution.

### ParticipantIndividualId

- **Field API Name:** `ssot__ParticipantIndividualId__c`
- **Data Type:** TEXT
- **Description:** Reference to the Individual record that represents the participant. Populated only if the participant record's DMO type is Individual.

### ParticipantUserId

- **Field API Name:** `ssot__ParticipantUserId__c`
- **Data Type:** TEXT
- **Description:** Reference to the User record that represents the participant. Populated only if the participant record's DMO type is User.

### PostStepVariableText

- **Field API Name:** `ssot__PostStepVariableText__c`
- **Data Type:** TEXT
- **Description:** The state of relavant variables after step execution finishes.

### PreStepVariableText

- **Field API Name:** `ssot__PreStepVariableText__c`
- **Data Type:** TEXT
- **Description:** The state of relevant variables before step execution begins.

### PrevStepId

- **Field API Name:** `ssot__PrevStepId__c`
- **Data Type:** TEXT
- **Description:** The ID of the previous step. The ID enables sequencing or chaining of steps.

### SessionId

- **Field API Name:** `ssot__SessionId__c`
- **Data Type:** TEXT
- **Description:** Reference to the specific AiAgentSession in which this step is involved.

### StartTimestamp

- **Field API Name:** `ssot__StartTimestamp__c`
- **Data Type:** DATETIME
- **Description:** The timestamp when execution of the the step started.

### SubType

- **Field API Name:** `ssot__SubType__c`
- **Data Type:** TEXT
- **Description:** The subtype of the step that provides additional classification within the step type.

### TelemetryTraceSpanId

- **Field API Name:** `ssot__TelemetryTraceSpanId__c`
- **Data Type:** TEXT
- **Description:** The ID used for distributed tracing to place the step within a broader tracing context.

### TopicApiName

- **Field API Name:** `ssot__TopicApiName__c`
- **Data Type:** TEXT
- **Description:** Developer name of a subagent or (in multi-agent solutions) a connected subagent, at the AiAgentInteractionStep level. Defaults to NOT_SET in some scenarios, such as when the agent router in an orchestrator agent coordinates multiple subagents within a single interaction.
