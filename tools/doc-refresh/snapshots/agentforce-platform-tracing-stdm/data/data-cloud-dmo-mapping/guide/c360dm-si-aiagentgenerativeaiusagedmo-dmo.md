# Ai Agent Generative Ai Usage DMO

Captures granular AI usage analytics, including token consumption and LLM metadata for attributing consumption to specific agents and features.

:::note
This is a standard data model object (DMO), which is created in your org only after you map it. Until it's mapped, this DMO is visible on the data mapping screen but doesn't appear in the Data Model list or record view in the Data 360 app. This is expected behavior. To use this DMO, search for it on the data mapping screen and complete the mapping. After it's mapped, the DMO and its fields appear in the Data Model list.
:::

## Object Properties

**Object API Name:** `AiAgentGenerativeAiUsage_std__dlm`\
**Category:** Unassigned\
**Availability:** Available in 260 and later versions\
**Primary Key Field:** Id

## Fields

- [AgentDeveloperName](#agentdevelopername)
- [AgentIdentifier](#agentidentifier)
- [AgentTypeCode](#agenttypecode)
- [AiAgentInteractionId](#aiagentinteractionid)
- [AiAgentSessionId](#aiagentsessionid)
- [AiAgentToolIdentifier](#aiagenttoolidentifier)
- [AiAgentToolInvTargetCode](#aiagenttoolinvtargetcode)
- [AiAgentToolName](#aiagenttoolname)
- [cdp_sys_record_currency](#cdp_sys_record_currency)
- [DataSourceId](#datasourceid)
- [DataSourceObjectId](#datasourceobjectid)
- [FeatureDescriptorName](#featuredescriptorname)
- [GenAiGatewayFeatureName](#genaigatewayfeaturename)
- [GenAiGatewayModelName](#genaigatewaymodelname)
- [Id](#id)
- [InfraTenantIdentifier](#infratenantidentifier)
- [InternalOrganizationId](#internalorganizationid)
- [IsBillableIndicator](#isbillableindicator)
- [IsMeteredIndicator](#ismeteredindicator)
- [KQ_Id](#kq_id)
- [MeteringSkipReasonCode](#meteringskipreasoncode)
- [ModelClassType](#modelclasstype)
- [ModelProviderModelName](#modelprovidermodelname)
- [ModelProviderName](#modelprovidername)
- [PromptCompletionTokenCount](#promptcompletiontokencount)
- [PromptInputTokenCount](#promptinputtokencount)
- [PromptTemplateDeveloperName](#prompttemplatedevelopername)
- [PromptTemplateIdentifier](#prompttemplateidentifier)
- [PromptTotalTokenCount](#prompttotaltokencount)
- [RequestIdentifier](#requestidentifier)
- [TelemetryTraceIdentifier](#telemetrytraceidentifier)
- [TelemetryTraceSpanId](#telemetrytracespanid)
- [TierQualifierType](#tierqualifiertype)
- [Timestamp](#timestamp)
- [UnitTypeCode](#unittypecode)
- [UsageQuantity](#usagequantity)
- [UsageTypeCode](#usagetypecode)
- [UserContext](#usercontext)
- [UserId](#userid)

### AgentDeveloperName

- **Field API Name:** `AgentDeveloperName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the agent developer name.

### AgentIdentifier

- **Field API Name:** `AgentIdentifier__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the agent identifier.

### AgentTypeCode

- **Field API Name:** `AgentTypeCode__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the agent type code.

### AiAgentInteractionId

- **Field API Name:** `AiAgentInteractionId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### AiAgentSessionId

- **Field API Name:** `AiAgentSessionId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### AiAgentToolIdentifier

- **Field API Name:** `AiAgentToolIdentifier__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the ai agent tool identifier.

### AiAgentToolInvTargetCode

- **Field API Name:** `AiAgentToolInvTargetCode__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the ai agent tool inv target code.

### AiAgentToolName

- **Field API Name:** `AiAgentToolName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the ai agent tool name.

### cdp_sys_record_currency

- **Field API Name:** `cdp_sys_record_currency__c`
- **Data Type:** TEXT
- **Description:** System-generated metadata field that stores a 3-letter ISO currency code.

### DataSourceId

- **Field API Name:** `DataSourceId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### DataSourceObjectId

- **Field API Name:** `DataSourceObjectId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### FeatureDescriptorName

- **Field API Name:** `FeatureDescriptorName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the feature descriptor name.

### GenAiGatewayFeatureName

- **Field API Name:** `GenAiGatewayFeatureName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the gen ai gateway feature name.

### GenAiGatewayModelName

- **Field API Name:** `GenAiGatewayModelName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the gen ai gateway model name.

### Id

- **Field API Name:** `Id__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### InfraTenantIdentifier

- **Field API Name:** `InfraTenantIdentifier__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the infra tenant identifier.

### InternalOrganizationId

- **Field API Name:** `InternalOrganizationId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### IsBillableIndicator

- **Field API Name:** `IsBillableIndicator__c`
- **Data Type:** BOOLEAN
- **Description:** Indicates whether this record is billable indicator (true) or not (false).

### IsMeteredIndicator

- **Field API Name:** `IsMeteredIndicator__c`
- **Data Type:** BOOLEAN
- **Description:** Indicates whether this record is metered indicator (true) or not (false).

### KQ_Id

- **Field API Name:** `KQ_Id__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for Id

### MeteringSkipReasonCode

- **Field API Name:** `MeteringSkipReasonCode__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the metering skip reason code.

### ModelClassType

- **Field API Name:** `ModelClassType__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the model class type.

### ModelProviderModelName

- **Field API Name:** `ModelProviderModelName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the model provider model name.

### ModelProviderName

- **Field API Name:** `ModelProviderName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the model provider name.

### PromptCompletionTokenCount

- **Field API Name:** `PromptCompletionTokenCount__c`
- **Data Type:** DOUBLE
- **Description:** The number of prompt completion tokens for this record.

### PromptInputTokenCount

- **Field API Name:** `PromptInputTokenCount__c`
- **Data Type:** DOUBLE
- **Description:** The number of prompt input tokens for this record.

### PromptTemplateDeveloperName

- **Field API Name:** `PromptTemplateDeveloperName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the prompt template developer name.

### PromptTemplateIdentifier

- **Field API Name:** `PromptTemplateIdentifier__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the prompt template identifier.

### PromptTotalTokenCount

- **Field API Name:** `PromptTotalTokenCount__c`
- **Data Type:** DOUBLE
- **Description:** The number of prompt total tokens for this record.

### RequestIdentifier

- **Field API Name:** `RequestIdentifier__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the request identifier.

### TelemetryTraceIdentifier

- **Field API Name:** `TelemetryTraceIdentifier__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the telemetry trace identifier.

### TelemetryTraceSpanId

- **Field API Name:** `TelemetryTraceSpanId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### TierQualifierType

- **Field API Name:** `TierQualifierType__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the tier qualifier type.

### Timestamp

- **Field API Name:** `Timestamp__c`
- **Data Type:** DATETIME
- **Description:** The date and time of the timestamp.

### UnitTypeCode

- **Field API Name:** `UnitTypeCode__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the unit type code.

### UsageQuantity

- **Field API Name:** `UsageQuantity__c`
- **Data Type:** DOUBLE
- **Description:** The count or numerical value of the quantity for this record.

### UsageTypeCode

- **Field API Name:** `UsageTypeCode__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the usage type code.

### UserContext

- **Field API Name:** `UserContext__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the user context.

### UserId

- **Field API Name:** `UserId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.
