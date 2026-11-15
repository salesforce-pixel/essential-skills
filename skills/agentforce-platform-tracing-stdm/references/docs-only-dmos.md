# Docs-only DMOs (from Salesforce Help; not yet verified in an org)

Unlike `dmo-fields.md`, nothing here was checked with `d360_dmo_get`. The STDM Help tables turned out to be wrong in several places (see SKILL gotchas 1–3), so **run `d360_dmo_get` / `SELECT * … LIMIT 5` before writing a query against these**, then move the confirmed fields to `dmo-fields.md`.

In the `default` data space, standard fields carry the `ssot__` prefix; in a custom data space, use that space's prefix (e.g. `std__`). The `GenAI*__dlm` objects are legacy custom DMOs with **no** prefix.

## Audit and Feedback (Help: "Data Model for Generative AI Audit and Feedback")

Each DLO maps to a legacy custom DMO and a standard DMO. Salesforce adds future schema changes only to the **standard** DMOs.

| DLO / legacy custom DMO | Standard DMO (label) | Holds |
|---|---|---|
| `GenAIGatewayRequest` | Ai Gateway Request | One row per LLM call: prompt, model, tokens, `generationGroupId__c` (verified fields in `dmo-fields.md`) |
| `GenAIGatewayResponse` | Ai Gateway Response | Response metadata |
| `GenAIGeneration` | Ai Response Generation (`GenAiResponseGeneration`) | `generationId__c`, `generationResponseId__c`, `responseText__c` (demasked), `maskedResponseText__c`, `responseParameters__c`, `feature__c`, `cloud__c`, `timestamp__c` |
| `GenAIFeedback` | Ai Feedback (`GenAiFeedback`) | `feedbackId__c`, `feedback__c` (`GOOD`/`BAD`/NULL; NULL when only verbatim text was given), `action__c` (`accept`, `reject`, `generation-edit`, `thumbs-up`, `thumbs-down`, `regeneration`), `source__c` (`HUMAN`/`SYSTEM`/`NOT_PROVIDED`), `generationGroupId__c`, `generationId__c`, `userId__c`, `appType__c`, `feature__c`, `timestamp__c` |
| `GenAIFeedbackDetail` | Ai Feedback Additional Info | Free-text and flags such as `Inaccurate-True`, `Incomplete-True` |
| `GenAIContentQuality` | Ai Content Quality | Trust Layer evaluation parent rows |
| `GenAIContentCategory` | Ai Content Quality Category (`GenAiContentQualityCategory`) | `detectorType__c` (`PII`, `TOXICITY`, `PROMPT_DEFENSE`, `InstructionAdherence`, `TaskResolution`), `category__c` (e.g. `Email`, `Hate`, `HIGH`, `FULLY_RESOLVED`), `value__c` (count / likelihood / explanation text), `parent__c` (→ ContentQuality or Generation), `timestamp__c` |
| `GenAIAppGeneration` | Ai Response App Generation | App edits to a generated text (`generationUpdate__c`) |
| `GenAIGatewayRequestTag` | Ai Gateway Request Tag | Tags on requests |
| `GenAIGtwyRequestMetadata` | Ai Gateway Req Additional Info | |
| `GenAIGtwyRequestLLM` | Ai Gateway Request Model Diagnostic | |
| `GenAIGtwyObjRecord` / `GenAIGtwyObjRecCitation` | Ai Gateway Request Object Record / … Citation | Grounding records and citations (e.g. a Knowledge article) used in a prompt |

Join chain from the trace:
- step `ssot__GenAiGatewayRequestId__c` → request `gatewayRequestId__c`
- step `ssot__GenerationId__c` → generation `generationId__c`
- request `generationGroupId__c` → feedback `generationGroupId__c`

## Knowledge/RAG quality (Help: "Data Model for Knowledge/RAG Quality Data and Metrics")

| Object | Kind | Key fields |
|---|---|---|
| `AIRetrieverRequest` | DLO | `Id`, `QueryText`, `RetrieverApiName`, `FeatureText` (`DocumentRetrieval`, `KnowledgeSearch`), `RequestTimestamp`, `SessionId` (agent session), `TraceId`, `SpanId`, `RequestReferenceId` (calling agent/prompt/Apex), `SourceAssetApiName`, `SourceAssetTypeName`, `SourceAssetVersion` |
| `AIRetrieverResponse` | DLO | `Id`, `AiRetrieverRequestId` (→ request), `ResultText` (JSON: chunk, `SourceRecordId`…), `SortIndexNumber` (chunk rank), `SourceRecordId`, `ResponseTimestamp` |
| `AIRetrieverQualityMetric` | DMO | `Id__c`, `AiRetrieverRequestId__c`, `AiGatewayRequestId__c`, `AiResponseGenerationId__c`, `RetrieverApiName__c`, `UserUtteranceText__c`, `AgentGeneratedResponseText__c`, `AnswerRelevancyScoreNumber__c`, `ContextPrecisionScoreNumber__c`, `FaithfulnessRelevancyScoreNumber__c`, `RetrievedContextIdListText__c` (top-K), `SourceDocumentIdListText__c`, `RetrieverTraceId__c`, `RetrieverTraceSpanId__c` (→ Telemetry Trace Span), `MetricCreatedTimestamp__c`, `LastProcessedReqTimestamp__c` |

## Agent Platform Tracing (Help: "Agent Platform Tracing")

| Object | Fields |
|---|---|
| `ObservabilitySpans__dll` (DLO) | `traceId__c`, `spanId__c`, `parentSpanId__c`, `serviceName__c`, `operationName__c`, `spanKind__c`, `startDateTime__c`, `endDateTime__c`, `durationNanos__c`, `statusCode__c`, `attributes__c`, `organizationId__c` |
| `ssot__TelemetryTraceSpan__dlm` (DMO) | `ssot__Id__c` (span), `ssot__TelemetryTrace__c`, `ssot__TelemetryParentSpanId__c`, `ssot__ServiceName__c`, `ssot__OperationName__c`, `ssot__SpanKind__c`, `ssot__StartDateTime__c`, `ssot__EndDateTime__c`, `ssot__DurationNumber__c` (ns), `ssot__StatusCode__c`, `ssot__TelemetrySpanAttributeText__c`, `ssot__TelemetrySpanEventText__c`, `KQ_Id__c`, `KQ_TelemetryParentSpanId__c` |

The Help's data-type column for the DMO is misaligned (e.g. it lists `StatusCode` as DateTime). Check with `d360_dmo_get`.

## Agentforce Observability semantic model (Help: "Agentforce Observability Data Model")

The semantic model **Agentforce Analytics Foundations** groups entities as follows.
- **Session and identity:** AI Agent Session, Session Participant, Session Log, Bot, Bot Version, Session Participant Extended.
- **Interactions:** AI Agent Interaction, Interaction Step, Interaction Message, AI Agent Topic, AI Agent Action, AI Retriever Quality Metric.
- **Moments and evaluations:** AI Agent Moment, Moment Interaction, Tag, Tag Definition, Tag Definition Association, Tag Association, plus the logical views Moment Tag Association, Moment Quality Score, Session Tag Association and Interaction Tag Association.
- **Quality and feedback:** AI Response Generation, AI Content Quality Category, Categorized Content Quality, AI Feedback, AI Feedback Additional Info, Gen AI Gateway Request Object Record (+ Content).
- **Voice:** Voice Call (mapped only with Service Cloud Voice or Native Voice). When mapped, it has Created Date, Disconnect Reason, Id and Quality Score.

Calculated fields end in `_clc`. Examples: `Unique_Sessions_clc`, `Engaged_Sessions_clc`, `Deflection_Rate_clc`, `Abandonment_Rate_clc`, `Escalation_Rate_clc`, `Success_Rate_clc`, `Error_Rate_clc`, `Agent_Response_Rate_clc` (turn completion within 60 s), `Average_Session_Duration_clc`, `Time_To_First_Agent_Token_P50/P90/P95/P99_clc`, `Time_To_Last_Agent_Token_P*_clc`, `Quality_Score_clc`, `User_Feedback_Status_clc`, `Agent_Adherence_Status_clc`, `Task_Resolution_Status_clc`. SKILL.md (R8) shows how the main ones are defined. The full formulas are in the Help pages "Agentforce Observability Measure Formulas" and "… Dimension Formulas" (snapshots in `tools/doc-refresh/snapshots/agentforce-platform-tracing-stdm/help/`).
