# STDM DMO fields (verified in a sandbox, October 2026)

Taken from `d360_dmo_get` and `SELECT *`, not from the Help article. All DMOs are category `ENGAGEMENT`, data space `default`.

Every DMO also has these system columns, not repeated below: `ssot__DataSourceId__c`, `ssot__DataSourceObjectId__c`, `ssot__InternalOrganizationId__c` (the 18-char org id), `ssot__ExternalSourceId__c`, and `KQ_*__c` key-qualifier columns. Ignore them in queries.

**Bold** = primary key. ⚠ = differs from the Help article.

## ssot__AiAgentSession__dlm

| Field | Type | Notes |
|---|---|---|
| **`ssot__Id__c`** | Text | UUID, e.g. `01a158d3-3609-7c4e-807a-e8e45c42255d` |
| `ssot__StartTimestamp__c` | DateTime | Session start (the welcome message time) |
| `ssot__EndTimestamp__c` | DateTime | ⚠ always NULL (deprecated) |
| `ssot__AiAgentChannelType__c` | Text | ⚠ value, not an id: `SCRT2 - EmbeddedMessaging`, `Builder`, `LightningDesktopCopilot`, `MIDAS`, `Field Service Mobile`, `LEX/LDS` |
| `ssot__AiAgentSessionEndType__c` | Text | ⚠ always `NOT_SET` (deprecated) |
| `ssot__RelatedMessagingSessionId__c` | Text | ⚠ (Help: `MessagingSessionId`). `MessagingSession.Id` `0Mw…`, or `NOT_SET` |
| `ssot__RelatedVoiceCallId__c` | Text | `VoiceCall.Id` |
| `ssot__PreviousSessionId__c` | Text | reserved |
| `ssot__SessionOwnerId__c`, `ssot__SessionOwnerObject__c`, `ssot__IndividualId__c` | Text | reserved |
| `ssot__VariableText__c` | Text | reserved |

No agent name on the session: get it from Participant (role `AGENT`).

## ssot__AiAgentSessionParticipant__dlm — 1,188 rows

⚠ One USER row and one AGENT row **per turn**, each with a distinct `ssot__Id__c`. Use `SELECT DISTINCT` when you only need one per session.

| Field | Type | Notes |
|---|---|---|
| **`ssot__Id__c`** | Text | |
| `ssot__AiAgentSessionId__c` | Text | → Session |
| `ssot__AiAgentSessionParticipantRole__c` | Text | ⚠ `AGENT` / `USER` (Help: Owner/Observer) |
| `ssot__ParticipantObject__c` | Text | `GenAiPlannerDefinition` (agent), `MessagingEndUser`, `User` |
| `ssot__ParticipantId__c` | Text | `16j…` planner / `0PA…` messaging end user / `005…` user |
| `ssot__AiAgentApiName__c` | Text | e.g. `My_Service_Agent`, `SearchAgent`. Filled on USER rows too |
| `ssot__AiAgentVersionApiName__c` | Text | `v1`, `v2`, `v0`, `NOT_SET` |
| `ssot__AiAgentType__c` | Text | ⚠ value: `EinsteinServiceAgent`, `AgentforceEmployeeAgent`, `Setup`, `ServicePlanner` |
| `ssot__AiAgentTemplateApiName__c` | Text | |
| `ssot__StartTimestamp__c` / `ssot__EndTimestamp__c` | DateTime | End is filled on ~half the rows |
| `ssot__ParticipantAttributeText__c` | Text | reserved |
| `ssot__IndividualId__c` | Text | reserved |

## ssot__AiAgentInteraction__dlm — 410 rows / 377 distinct ids

| Field | Type | Notes |
|---|---|---|
| **`ssot__Id__c`** | Text | ⚠ `NOT_SET` on 34 SearchAgent rows. Never join on id alone |
| `ssot__AiAgentSessionId__c` | Text | → Session |
| `ssot__AiAgentInteractionType__c` | Text | ⚠ value: `TURN`, `SESSION_END` |
| `ssot__TopicApiName__c` | Text | `GeneralFAQ_16jXX0000000001` (topic + planner id); `NOT_SET` on the welcome turn |
| `ssot__StartTimestamp__c` / `ssot__EndTimestamp__c` | DateTime | Always filled |
| `ssot__PrevInteractionId__c` | Text | Chaining; order by `StartTimestamp` instead |
| `ssot__TelemetryTraceId__c`, `ssot__TelemetryTraceSpanId__c` | Text | Distributed-trace ids |
| `ssot__AttributeText__c` | Text | JSON |
| `ssot__SessionOwnerId__c`, `ssot__SessionOwnerObject__c`, `ssot__IndividualId__c` | Text | reserved |

## ssot__AiAgentInteractionMessage__dlm — 789 rows

| Field | Type | Notes |
|---|---|---|
| **`ssot__Id__c`** | Text | |
| `ssot__AiAgentInteractionId__c` | Text | → Interaction (may be `NOT_SET`, see above) |
| `ssot__AiAgentSessionId__c` | Text | → Session (always use it in the join too) |
| `ssot__AiAgentSessionParticipantId__c` | Text | → Participant (sender) |
| `ssot__AiAgentInteractionMessageType__c` | Text | ⚠ value: `Input` (user), `Output` (agent) |
| `ssot__AiAgentInteractionMsgContentType__c` | Text | `text/plain`, `application/json` |
| `ssot__ContentText__c` | Text | Message text (`NA` if not text) |
| `ssot__MessageSentTimestamp__c` | DateTime | Order transcripts by this |
| `MessageStartTimestamp__c`, `MessageEndTimestamp__c` | DateTime | ⚠ no `ssot__` prefix |
| `Modality__c` | Text | ⚠ no prefix (Help: `MessageModalityId`): `text`, `NOT_SET` |
| `ssot__ParentMessageId__c` | Text | Threading |
| `ssot__SessionOwnerId__c`, `ssot__SessionOwnerObject__c`, `ssot__IndividualId__c` | Text | reserved |

## ssot__AiAgentInteractionStep__dlm — 1,702 rows

| Field | Type | Notes |
|---|---|---|
| **`ssot__Id__c`** | Text | |
| `ssot__AiAgentInteractionId__c` | Text | → Interaction |
| `ssot__AiAgentInteractionStepType__c` | Text | ⚠ value: `LLM_STEP`, `ACTION_STEP`, `TOPIC_STEP`, `CLASSIFIER_STEP`, `TRUST_GUARDRAILS_STEP`, `VARIABLE_UPDATE_STEP`, `SESSION_END`, `PLATFORM_ACTION_STEP` |
| `ssot__Name__c` | Text | Topic name for LLM_STEP, action name for ACTION_STEP, `agent_router`, `pre_orchestration.guardrail`, `InstructionAdherence`, `Atlas__GroundednessValidationPrompt`, `__state_update_action__`; for SESSION_END: `CLOSED_USER_REQUEST` / `EXPIRED` |
| `SubType__c` | Text | ⚠ no prefix. `generatePromptResponse`, `standardInvocableAction`, `NOT_SET`, NULL |
| `ssot__StartTimestamp__c` / `ssot__EndTimestamp__c` | DateTime | Duration = end − start |
| `ssot__InputValueText__c` / `ssot__OutputValueText__c` | Text | JSON payloads; LLM_STEP input = the full resolved prompt (10–17k chars) |
| `ssot__PreStepVariableText__c` / `ssot__PostStepVariableText__c` | Text | Variable state (often `NOT_SET`) |
| `ssot__ErrorMessageText__c` | Text | `NOT_SET` when there's no error |
| `ssot__AttributeText__c` | Text | `internalTraceId`, `internalSpanId`, `progress_indicators` |
| `ssot__GenerationId__c`, `ssot__GenAiGatewayRequestId__c`, `ssot__GenAiGatewayResponseId__c` | Text | Filled on LLM and guardrail steps. `ssot__GenAiGatewayRequestId__c` = `REPLACE(GenAIGatewayRequest__dlm.gatewayRequestId__c,'"','')` (verified Nov 2026; gateway rows exist only from a start date, see SKILL gotcha 9) |
| `ssot__PrevStepId__c` | Text | reserved |
| `ssot__TelemetryTraceSpanId__c` | Text | |
| ⚠ (no `TopicApiName`) | | The Help lists it; it isn't in this org. Use the interaction's |

## Agent Analytics / Optimization DMOs

### ssot__AiAgentMoment__dlm — 41 rows
`ssot__Id__c`, `ssot__AiAgentSessionId__c`, `ssot__AiAgentApiName__c`, `ssot__AiAgentVersionApiName__c`, `ssot__StartTimestamp__c`, `ssot__EndTimestamp__c`, `ssot__RequestSummaryText__c` (what the user wanted), `ssot__ResponseSummaryText__c` (what the agent did). One moment = one user intent in a session; a session can have several.

### ssot__AiAgentMomentInteraction__dlm — 77 rows
`ssot__Id__c`, `ssot__AiAgentMomentId__c`, `ssot__AiAgentInteractionId__c`, `ssot__StartTimestamp__c`. Maps moments to interactions.

### ssot__AiAgentTagAssociation__dlm — 46 rows
`ssot__Id__c`, `ssot__AiAgentSessionId__c`, `ssot__AiAgentMomentId__c`, `ssot__AiAgentTagId__c` (→ Tag), `ssot__AiAgentTagDefinitionAssociationId__c`, `ValueText__c`, `ssot__AssociationReasonText__c` (the LLM judge's explanation), `SourceType__c` (`PROMPT_TEMPLATE`), `OutcomeType__c`, `CreatedByUserId__c`, `AiAgentSessionStartTimestamp__c`, `AttributeText__c`, `ssot__CreatedDate__c`.

### ssot__AiAgentTag__dlm
`ssot__Id__c`, `ssot__AiAgentTagDefinitionId__c` (→ TagDefinition), `ssot__Value__c` (e.g. `0`–`5`, `TRUE`/`FALSE`, a category label), `ssot__Description__c`, `ssot__IsActive__c`, `ssot__CreatedDate__c`.

### ssot__AiAgentTagDefinition__dlm
`ssot__Id__c`, `ssot__DeveloperName__c` (`std_Deflection_Score_<Agent>_V1`, `std_Abandonment_Score_<Agent>_V1`, `AIE_Request_Category_<Agent>`, `Quality_Score`), `ssot__Name__c` (label), `ssot__Description__c`, `ssot__DataType__c` (`Text`/`Number`/`Integer`), `ssot__SourceType__c` (`Predefined`/`Generated`), `SemanticType__c`, `LightningTypeApiName__c`, `ssot__CreatedDate__c`.

### ssot__AiAgentTagDefinitionAssociation__dlm
`ssot__Id__c`, `ssot__AiAgentTagDefinitionId__c`, `ssot__AiAgentApiName__c`, `ssot__AiPromptTemplateId__c`, `InputScope__c`, `ssot__CreatedDate__c`. Says which tag definitions apply to which agent.

## Token and metering objects (verified November 2026)

⚠ Both store some values differently from STDM; read the notes before joining.

### GenAIGatewayRequest__dlm: one row per LLM call

Category `ENGAGEMENT`, created as Custom. ⚠ Id and name values are stored **with literal double quotes** (`"16jXX0000000002"`, `"Atlas__AgentGraphReasoningPrompt"`); use `REPLACE(col,'"','')`.

| Field | Type | Notes |
|---|---|---|
| **`gatewayRequestId__c`** | Text | = step `ssot__GenAiGatewayRequestId__c` (quotes stripped) |
| `plannerId__c` | Text | = AGENT participant `ssot__ParticipantId__c` (`16j…` / `PlannerPreview-…`); NULL for evals and authoring rows |
| `sessionId__c` | Text | = `ssot__AiAgentSession__dlm.ssot__Id__c` |
| `botVersionId__c` | Text | `0X9…` for published versions, `v0` for Builder preview drafts |
| `feature__c`, `appType__c` | Text | e.g. `plannerservice` / `EinsteinGPT`; see SKILL vocabularies |
| `model__c` | Text | Provider model name (`gpt-6-sol`, `gpt-4.1-2025-04-14`, `EinsteinHyperClassifier`) |
| `promptTemplateDevName__c` | Text | `Atlas__…` system prompt names |
| `promptTokens__c`, `completionTokens__c`, `totalTokens__c` | Number | Token counts |
| `timestamp__c` | DateTime | |
| Also | | `prompt__c`, `maskedPrompt__c`, `temperature__c`, `userId__c`, `generationGroupId__c`, `promptTemplateVersionNo__c`, safety and PII flags |

`GenAIGatewayResponse__dlm` has only `generationRequestId__c`, `generationResponseId__c`, `parameters__c`, `timestamp__c`, `orgId__c`, `cloud__c`: **no token counts**.

### AiAgentGenerativeAiUsage__dll: Agentforce metering (a DLO, data space `default`)

| Field | Type | Notes |
|---|---|---|
| **`id__c`** | Text | |
| `aiAgentSessionId__c` | Text | = `ssot__AiAgentSession__dlm.ssot__Id__c` (plain, no quotes) |
| `aiAgentInteractionId__c` | Text | |
| `agentDeveloperName__c` | Text | Agent API name on `ACTION` / `INTERACTION` rows; NULL on `PROMPT` rows |
| `agentIdentifier__c`, `agentTypeCode__c` | Text | |
| `unitTypeCode__c` | Text | `ACTION`, `INTERACTION`, `PROMPT` |
| `usageTypeCode__c` | Text | `Agentforce_CustomAction`, `Agentforce_StandardAction`, `EmbeddedAI_*Prompts`, NULL on interactions |
| `aiAgentToolName__c` | Text | Action name; `execute` on interactions |
| `isMeteredIndicator__c` | Bool | `true` = metered. Filter on this |
| `isBillableIndicator__c` | Bool | ⚠ also `true` on some unmetered rows |
| `meteringSkipReasonCode__c` | Text | `NOT_SKIPPED`, `INTERACTION`, `NON_BILLABLE_STANDARD_ACTION`, `AGENTFORCE_USAGE_WITH_FLEX_CREDITS` |
| `usageQuantity__c` | Number | `1` per action |
| `promptInputTokenCount__c`, `promptCompletionTokenCount__c`, `promptTotalTokenCount__c` | Number | On `PROMPT` rows; 0 on actions |
| `featureDescriptorName__c`, `genAiGatewayFeatureName__c`, `genAiGatewayModelName__c`, `modelProviderName__c`, `modelProviderModelName__c`, `modelClassType__c` | Text | |
| `promptTemplateDeveloperName__c`, `promptTemplateIdentifier__c` | Text | |
| `requestIdentifier__c`, `telemetryTraceIdentifier__c`, `telemetryTraceSpanId__c` | Text | |
| `timestamp__c` | DateTime | |

### Digital Wallet DLOs (Data 360 consumption)

`TenantBillingUsageEvent__dll`, `TenantEnrichedUsageEvent__dll`, `TenantHourlyEntitlementConsumption__dll`, `TenantDailyEntitlementConsumption__dll`, `TenantUsageTypeMultiplier__dll` (68 rows), `TenantEntitlementTransaction__dll` (15 rows).
- ⚠ In the verified sandbox they had no data space (`d360_dlo_get` → `"dataSpaceInfo":[]`), and SQL returned "table does not exist" with or without `dataspace`.
- The usage-event DLOs had 0 records.

## Other related DMOs in the org (not needed for normal tracing)

- `GenAiGatewayRequest_std__dlm` (`Id__c`, `AiModelName__c`, `AiPromptTemplateName__c`, `PromptText__c`, `PromptTokenCount__c`, `CompletionTokenCount__c`, `TotalTokenCount__c`, `CreatedDate__c`): not re-checked in November 2026.
- `GenAIGeneration__dlm` / `GenAiResponseGeneration_std__dlm`, `GenAIFeedback__dlm` (0 rows in October 2026), `GenAIContentQuality__dlm`.

Also present but unexplored: `AiAgentSessionLog_std__dlm`, `AiAgentTagAssocLog_std__dlm`, `AiAgentGenerativeAiUsage_std__dlm` (the DMO counterpart of the metering DLO above; not queried), `AiAgentMessageAttachment_std__dlm`, `AiAgentSessionAttachment_std__dlm`.

Finding DLO names: `d360_dlo_list` returns 20 objects per call whatever `limit` says; page with `offset`.
