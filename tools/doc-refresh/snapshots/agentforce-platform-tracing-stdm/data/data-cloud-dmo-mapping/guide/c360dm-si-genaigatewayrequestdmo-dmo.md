# Gen Ai Gateway Request DMO

Generative Request to the Gateway - Incoming request to the gateway to generate a generation.

:::note
This is a standard data model object (DMO), which is created in your org only after you map it. Until it's mapped, this DMO is visible on the data mapping screen but doesn't appear in the Data Model list or record view in the Data 360 app. This is expected behavior. To use this DMO, search for it on the data mapping screen and complete the mapping. After it's mapped, the DMO and its fields appear in the Data Model list.
:::

## Object Properties

**Object API Name:** `GenAiGatewayRequest_std__dlm`\
**Category:** Unassigned\
**Availability:** Available in 260 and later versions\
**Primary Key Field:** Id

## Fields

- [AiApplicationFeatureName](#aiapplicationfeaturename)
- [AiApplicationName](#aiapplicationname)
- [AiModelName](#aimodelname)
- [AiPlannerIdentifier](#aiplanneridentifier)
- [AiPromptTemplateName](#aiprompttemplatename)
- [AiPromptVersionName](#aipromptversionname)
- [AiProviderName](#aiprovidername)
- [BillToCloudIdentifier](#billtocloudidentifier)
- [BotVersionIdentifier](#botversionidentifier)
- [cdp_sys_record_currency](#cdp_sys_record_currency)
- [CompletionTokenCount](#completiontokencount)
- [CreatedById](#createdbyid)
- [CreatedDate](#createddate)
- [DataSourceId](#datasourceid)
- [DataSourceObjectId](#datasourceobjectid)
- [ExpectedGenerationCount](#expectedgenerationcount)
- [ExternalRecordId](#externalrecordid)
- [ExternalSourceId](#externalsourceid)
- [FeatureSessionIdentifier](#featuresessionidentifier)
- [FrequencyPenaltyNumber](#frequencypenaltynumber)
- [GenerationGroupIdentifier](#generationgroupidentifier)
- [GenerationResponseVarianceNumber](#generationresponsevariancenumber)
- [GenerationStoppingStringText](#generationstoppingstringtext)
- [Id](#id)
- [InternalOrganizationId](#internalorganizationid)
- [IsInputSafetyScoringEnabled](#isinputsafetyscoringenabled)
- [IsOutputSafetyScoringEnabled](#isoutputsafetyscoringenabled)
- [IsPiiMaskingEnabled](#ispiimaskingenabled)
- [KQ_Id](#kq_id)
- [MaskedPromptText](#maskedprompttext)
- [ModelParametersText](#modelparameterstext)
- [ParentAiGatewayRequestId](#parentaigatewayrequestid)
- [PresencePenaltyNumber](#presencepenaltynumber)
- [PromptText](#prompttext)
- [PromptTokenCount](#prompttokencount)
- [TotalTokenCount](#totaltokencount)

### AiApplicationFeatureName

- **Field API Name:** `AiApplicationFeatureName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the ai application feature name.

### AiApplicationName

- **Field API Name:** `AiApplicationName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the ai application name.

### AiModelName

- **Field API Name:** `AiModelName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the ai model name.

### AiPlannerIdentifier

- **Field API Name:** `AiPlannerIdentifier__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the ai planner identifier.

### AiPromptTemplateName

- **Field API Name:** `AiPromptTemplateName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the ai prompt template name.

### AiPromptVersionName

- **Field API Name:** `AiPromptVersionName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the ai prompt version name.

### AiProviderName

- **Field API Name:** `AiProviderName__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the ai provider name.

### BillToCloudIdentifier

- **Field API Name:** `BillToCloudIdentifier__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the bill to cloud identifier.

### BotVersionIdentifier

- **Field API Name:** `BotVersionIdentifier__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the bot version identifier.

### cdp_sys_record_currency

- **Field API Name:** `cdp_sys_record_currency__c`
- **Data Type:** TEXT
- **Description:** System-generated metadata field that stores a 3-letter ISO currency code.

### CompletionTokenCount

- **Field API Name:** `CompletionTokenCount__c`
- **Data Type:** DOUBLE
- **Description:** The number of completion tokens for this record.

### CreatedById

- **Field API Name:** `CreatedById__c`
- **Data Type:** TEXT
- **Description:** The user who created the record.

### CreatedDate

- **Field API Name:** `CreatedDate__c`
- **Data Type:** DATETIME
- **Description:** The date and time the record was originally created.

### DataSourceId

- **Field API Name:** `DataSourceId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### DataSourceObjectId

- **Field API Name:** `DataSourceObjectId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### ExpectedGenerationCount

- **Field API Name:** `ExpectedGenerationCount__c`
- **Data Type:** DOUBLE
- **Description:** The number of expected generations for this record.

### ExternalRecordId

- **Field API Name:** `ExternalRecordId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### ExternalSourceId

- **Field API Name:** `ExternalSourceId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### FeatureSessionIdentifier

- **Field API Name:** `FeatureSessionIdentifier__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the feature session identifier.

### FrequencyPenaltyNumber

- **Field API Name:** `FrequencyPenaltyNumber__c`
- **Data Type:** DOUBLE
- **Description:** Numeric value representing the frequency penalty number. Do not include currency symbols or commas.

### GenerationGroupIdentifier

- **Field API Name:** `GenerationGroupIdentifier__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the generation group identifier.

### GenerationResponseVarianceNumber

- **Field API Name:** `GenerationResponseVarianceNumber__c`
- **Data Type:** DOUBLE
- **Description:** Numeric value representing the generation response variance number. Do not include currency symbols or commas.

### GenerationStoppingStringText

- **Field API Name:** `GenerationStoppingStringText__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the generation stopping string text.

### Id

- **Field API Name:** `Id__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### InternalOrganizationId

- **Field API Name:** `InternalOrganizationId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### IsInputSafetyScoringEnabled

- **Field API Name:** `IsInputSafetyScoringEnabled__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the is input safety scoring enabled.

### IsOutputSafetyScoringEnabled

- **Field API Name:** `IsOutputSafetyScoringEnabled__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the is output safety scoring enabled.

### IsPiiMaskingEnabled

- **Field API Name:** `IsPiiMaskingEnabled__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the is pii masking enabled.

### KQ_Id

- **Field API Name:** `KQ_Id__c`
- **Data Type:** TEXT
- **Description:** Key Qualifier system field for Id

### MaskedPromptText

- **Field API Name:** `MaskedPromptText__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the masked prompt text.

### ModelParametersText

- **Field API Name:** `ModelParametersText__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the model parameters text.

### ParentAiGatewayRequestId

- **Field API Name:** `ParentAiGatewayRequestId__c`
- **Data Type:** TEXT
- **Description:** A unique, system-generated identifier for this record.

### PresencePenaltyNumber

- **Field API Name:** `PresencePenaltyNumber__c`
- **Data Type:** DOUBLE
- **Description:** Numeric value representing the presence penalty number. Do not include currency symbols or commas.

### PromptText

- **Field API Name:** `PromptText__c`
- **Data Type:** TEXT
- **Description:** Alphanumeric string representing the prompt text.

### PromptTokenCount

- **Field API Name:** `PromptTokenCount__c`
- **Data Type:** DOUBLE
- **Description:** The number of prompt tokens for this record.

### TotalTokenCount

- **Field API Name:** `TotalTokenCount__c`
- **Data Type:** DOUBLE
- **Description:** The number of total tokens for this record.
