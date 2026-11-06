---
name: agentforce-platform-tracing-stdm
description: Build and run Data 360 SQL over the Agentforce Session Trace Data Model (STDM) — the ssot__AiAgent* DMOs (Session, SessionParticipant, Interaction, InteractionMessage, InteractionStep) plus the Agent Analytics tag/moment DMOs — to monitor and debug any Agentforce agent. TRIGGER when the user asks to list or count agent sessions, read a conversation transcript, trace what an agent did in a turn (topic routing, actions, LLM calls, guardrails), find failing or slow steps, check action inputs/outputs, measure latency, review deflection/abandonment scores or request categories, link a MessagingSession to its agent session, measure an agent's LLM token usage (per version, model or prompt), count an agent's metered Agentforce actions or turn them into Flex Credits, or write any SQL against ssot__AiAgent*__dlm, GenAIGatewayRequest__dlm or AiAgentGenerativeAiUsage__dll. DO NOT TRIGGER for enabling or configuring session tracing itself (EventSettings / AgentforcePlatformTracingSettings metadata), for writing Agent Script (.agent) files, for website search-index SQL (hybrid_search / vector_search — use building-data360-semantic-queries), or for plain SOQL on CRM objects.
metadata:
  version: "1.0"
---

<!--
Changelog
1.0 — Imported into essential-skills (2026-11-06) from the personal
      ~/.claude/skills copy. Doc sources tracked by tools/doc-refresh.
-->

# Agentforce session tracing (STDM) SQL

Agentforce session tracing streams every agent session into Data 360 within minutes. One row tree per session:

```
ssot__AiAgentSession__dlm (1 per session, Id = UUID like 01a158d3-…)
 ├─< ssot__AiAgentSessionParticipant__dlm   (USER / AGENT rows — one set PER TURN, see gotcha 4)
 ├─< ssot__AiAgentInteraction__dlm          (TURN = one user request + agent reply; SESSION_END)
 │    ├─< ssot__AiAgentInteractionMessage__dlm   (Input / Output text; also carries AiAgentSessionId)
 │    └─< ssot__AiAgentInteractionStep__dlm      (router, guardrail, LLM, action, variable steps)
 ├─< ssot__AiAgentMoment__dlm               (Agent Analytics: request/response summaries)
 └─< ssot__AiAgentTagAssociation__dlm       (Agent Analytics: scores) → AiAgentTag → AiAgentTagDefinition
```

Join keys: child `ssot__AiAgentSessionId__c` / `ssot__AiAgentInteractionId__c` → parent `ssot__Id__c`. Message → participant via `ssot__AiAgentSessionParticipantId__c`. Full verified field lists: `references/dmo-fields.md`. A real 3-turn trace of an Agent Script service agent, with every step: `references/example-trace.md`.

Sources: Salesforce Help "About Agentforce Session Tracing", "Data Model for Agentforce Session Tracing", "Get Insights from Agent Session Tracing Data" (ai.generative_ai_session_trace_*). **Real orgs differ from those articles in several places; trust this skill and the DMO metadata (`d360_dmo_get`) over the Help field tables.** Everything below was verified against a live sandbox in October 2026; the token and metering parts (gotcha 9, R11, R12) in November 2026. Re-check with `d360_dmo_get` (DMOs) or `d360_dlo_get` (DLOs) if a field is missing in another org.

## How to run the SQL

1. **Data 360 MCP server (preferred), if one is configured** (Salesforce-hosted, `https://api.salesforce.com/platform/mcp/v1/d/<my-domain>/<sandbox|production>/data/data360`; often named `data360` in `.mcp.json`). Runs as the logged-in user (OAuth).
   - Tool `mcp__<server>__execute` (e.g. `mcp__data360__execute`), `toolName: "d360_query_sql"`, `paramsJson: {"input":{"sql":"<SQL>"},"dataspace":"default"}`.
   - If tools show only `authenticate`, start the OAuth flow and give the user the link.
   - Field metadata: `toolName: "d360_dmo_get"`, `paramsJson: {"dataModelObjectName":"ssot__AiAgentSession__dlm"}`.
   - Results over the first chunk: `d360_query_sql_rows` with the returned `queryId`.
2. **Fallback: anonymous Apex** (runs as the `sf` CLI user): `sfsqlquery.SqlStatement.create(sql, 'default')`, via the `platform-apex-anonymous-run` skill.

Always `SUBSTR(text, 1, N)` long text columns (`ssot__InputValueText__c` on LLM steps is 10–17k chars) and `LIMIT` exploratory queries.

## Gotchas (verified in a sandbox, October–November 2026)

1. **Use the `ssot__` DMO names.** The Help "Simple Query" example (`AiAgentSession__dlm`, `id__c`) doesn't work here. Use `ssot__AiAgentSession__dlm`, `ssot__Id__c`.
2. **Real field names differ from the Help table.** Type fields carry the value directly and have no `Id` suffix: `ssot__AiAgentChannelType__c`, `ssot__AiAgentInteractionType__c`, `ssot__AiAgentInteractionStepType__c`, `ssot__AiAgentInteractionMessageType__c`, `ssot__AiAgentInteractionMsgContentType__c`, `ssot__AiAgentSessionParticipantRole__c`, `ssot__AiAgentType__c`. The messaging link is `ssot__RelatedMessagingSessionId__c` (voice: `ssot__RelatedVoiceCallId__c`).
3. **Some fields have no `ssot__` prefix:** `SubType__c` (Step), `Modality__c`, `MessageStartTimestamp__c`, `MessageEndTimestamp__c` (Message). Step has **no** `TopicApiName` field here; use the interaction's.
4. **Participant rows repeat per turn.** A 4-turn session has 4 USER and 4 AGENT rows, each with its own `ssot__Id__c`. Never join Participant straight into a session-level count. Reduce it first:
   ```sql
   WITH agent_sessions AS (
     SELECT DISTINCT ssot__AiAgentSessionId__c AS sid, ssot__AiAgentVersionApiName__c AS ver
     FROM ssot__AiAgentSessionParticipant__dlm
     WHERE ssot__AiAgentApiName__c = '<Agent_API_Name>' AND ssot__AiAgentSessionParticipantRole__c = 'AGENT')
   ```
   The session row itself has no agent name; this CTE is how you filter by agent.
5. **`'NOT_SET'` is the null sentinel, even in ids.** It shows up as a value in version, topic, error text, subtype, `ssot__AiAgentSessionEndType__c` (always `NOT_SET`) and `ssot__RelatedMessagingSessionId__c` (Builder sessions).
   - Some agents (seen on a standard `SearchAgent`) write **`ssot__Id__c = 'NOT_SET'` on interactions**, and 215 messages point at that id. Joining Message→Interaction on id alone fans them out across every such session.
   - Join messages with `m.ssot__AiAgentInteractionId__c = i.ssot__Id__c AND m.ssot__AiAgentSessionId__c = i.ssot__AiAgentSessionId__c`, or filter by session first.
   - Real values test: `col IS NOT NULL AND col <> 'NOT_SET' AND LENGTH(col) > 0` (`SubType__c` has both NULL and `NOT_SET`).
6. **Session end:** `ssot__AiAgentSession__dlm.ssot__EndTimestamp__c` is always NULL (deprecated), and `ssot__AiAgentSessionEndType__c` is always `NOT_SET`.
   - Use `MAX(interaction.ssot__EndTimestamp__c)` for the end time.
   - Sessions that closed have a `SESSION_END` interaction and a `SESSION_END` step. **The step's `ssot__Name__c` is the end reason:** `CLOSED_USER_REQUEST` or `EXPIRED`.
7. **Turn counting:** the welcome message is its own `TURN` interaction with topic `NOT_SET` and only an Output message. Count user turns as interactions that have an `Input` message, or as `TURN`s with topic `<> 'NOT_SET'`.
8. **Topic names carry the planner id:** `<Topic>_16j…` (e.g. `GeneralFAQ_16jXX0000000001`). Match with `LIKE 'GeneralFAQ%'`. Step `ssot__Name__c` holds the plain name (`GeneralFAQ`).
9. **Token counts live in the LLM gateway DMO, not in the trace.** Step payloads and `GenAIGatewayResponse__dlm` have no token counts. `GenAIGatewayRequest__dlm` has one row per LLM call: `promptTokens__c`, `completionTokens__c`, `totalTokens__c`, `model__c`, `promptTemplateDevName__c`, `feature__c`, `plannerId__c`, `botVersionId__c`, `sessionId__c`, `timestamp__c`. Recipe R11.
   - **Its id and name values are stored with literal double quotes** (`"16jXX0000000002"`). Strip them with `REPLACE(col, '"', '')` before joining.
   - Joins (verified November 2026, all rows matched):
     - `REPLACE(g.plannerId__c,'"','')` = AGENT participant `ssot__ParticipantId__c` (`16j…`, or `PlannerPreview-…` for Builder preview). This is how you filter by agent.
     - `REPLACE(g.sessionId__c,'"','')` = `ssot__AiAgentSession__dlm.ssot__Id__c` (741 of 741 agent rows).
     - `REPLACE(g.gatewayRequestId__c,'"','')` = step `ssot__GenAiGatewayRequestId__c` (460 of 460 `LLM_STEP`s).
   - **Agent rows only exist from a start date.** In the verified org they begin 2026-10-21 06:21 UTC; until then the DMO held only Conversation Explorer (`CopilotUtteranceAnalysis`) rows, and agent sessions before that date have no token counts. Check `MIN(timestamp__c)` against the agent's first session before quoting a total.
   - Rows with no planner id can't be tied to one agent: `feature__c` `agentforce-standard-evals` (Agent Analytics scoring), `nextGenAuthoring` (the Builder authoring assistant), and Conversation Explorer.
   - Read what the model saw and said from `LLM_STEP` Input/Output text; the gateway `prompt__c` isn't needed for that.
10. **Freshness:** data arrives "within minutes", not instantly. A finished session was queryable within the hour; a Builder preview turn had its Input message after 8 minutes but no steps or Output yet.
11. **Use `STRPOS`, not `LIKE`, to search JSON payloads.** `LIKE '%"__action_execution_status__":"success"%'` matched **no** rows even though the text is there; `STRPOS(col, '…') > 0` works. Plain-word `LIKE '%success%'` is fine.
12. **There are two action-output formats.**
    - Agent Script agents write compact JSON `{"actionName":…,"actionResponse":{"__action_execution_status__":"success",…}}`.
    - Older planner agents (e.g. `GeneralCRM_…` actions) write pretty-printed JSON with `"historyEntryType" : "ACTION_SUCCESS_RESPONSE"` or `"ACTION_ERROR_RESPONSE"`.
    - Their action names look like `<Topic>_<plannerId>.<Action>_<id>`.
13. **Row counts differ from MessagingSession.** STDM makes one session per agent invocation (`ssot__RelatedMessagingSessionId__c` = `MessagingSession.Id`, `0Mw…`).
14. **Model per LLM call:** `LLM_STEP` `ssot__InputValueText__c` holds `"gen_ai.request.model":"<model>"`: the org default (e.g. `llmgateway__GPT41`), or the full `sfdc_ai__…` name when `model_config` overrides it (e.g. `sfdc_ai__DefaultBedrockAnthropicClaude55Sonnet`). Extract it with `SUBSTR(text, STRPOS(text, 'gen_ai.request.model') + 23, 60)` to compare models. Builder preview sessions are version `v0`, with topic `<Topic>_PlannerPreview-…`.

## Value vocabularies (seen in the verified org; others may add values)

| Field | Values |
|---|---|
| Session `ssot__AiAgentChannelType__c` | `SCRT2 - EmbeddedMessaging` (website chat), `Builder` (Agentforce Builder preview), `LightningDesktopCopilot`, `MIDAS`, `Field Service Mobile`, `LEX/LDS` |
| Participant role / `ParticipantObject__c` | `AGENT` → `GenAiPlannerDefinition` (`ParticipantId` = `16j…`); `USER` → `MessagingEndUser` (`0PA…`) or `User` (`005…`, Builder/internal) |
| Participant `ssot__AiAgentType__c` | `EinsteinServiceAgent`, `AgentforceEmployeeAgent`, `Setup`, `ServicePlanner` |
| Participant `ssot__AiAgentVersionApiName__c` | `v1`, `v2`, `v0` (preview/older), `NOT_SET` |
| Interaction type | `TURN`, `SESSION_END` |
| Message type / content type / modality | `Input`, `Output` / `text/plain`, `application/json` / `text`, `NOT_SET` |
| Step type | `LLM_STEP`, `ACTION_STEP`, `TOPIC_STEP`, `CLASSIFIER_STEP`, `TRUST_GUARDRAILS_STEP`, `VARIABLE_UPDATE_STEP`, `SESSION_END`, `PLATFORM_ACTION_STEP` |
| Step `SubType__c` (ACTION_STEP) | `generatePromptResponse`, `standardInvocableAction` |
| Gateway `feature__c` | `plannerservice` (published versions outside Builder; website chat in the verified org), `Agentforce Builder Preview` (drafts, and published versions tested in Builder), `agentforce-standard-evals`, `nextGenAuthoring`, `Agentforce Conversation Explorer` |
| Gateway `promptTemplateDevName__c` (quoted) | `Atlas__AgentGraphReasoningPrompt` (router and subagent LLM calls), `Atlas__GroundednessValidationPrompt` (post-check), `Atlas__StructuredOutputPrompt`, `Atlas__ProgressIndicatorLocalizationPrompt`, `Atlas__DynamicProgressIndicatorPrompt` |
| Gateway `model__c` | provider model names, e.g. `gpt-6-sol`, `gpt-4.1-2025-04-14`; the router is `EinsteinHyperClassifier` |
| Metering `unitTypeCode__c` / `usageTypeCode__c` | `ACTION` / `Agentforce_CustomAction`, `Agentforce_StandardAction`; `INTERACTION` / NULL; `PROMPT` / `EmbeddedAI_BasicPrompts`, `EmbeddedAI_StandardPrompts`, `EmbeddedAI_AdvancedPrompts` |
| Metering `meteringSkipReasonCode__c` | `NOT_SKIPPED` (metered), `INTERACTION`, `NON_BILLABLE_STANDARD_ACTION`, `AGENTFORCE_USAGE_WITH_FLEX_CREDITS` |
| Metering `featureDescriptorName__c` | `CopilotForDigitalChannels` (messaging channel), `plannerservice` (Builder preview), `EmployeeAssistant` (agent prompt rows), `AgentforceCoworker`, an id (`aLU…`) for a Builder session on a published version |

The Help examples `UserInputStep`, `LLMExecutionStep`, `FunctionStep` and the roles `Owner`/`Observer` didn't occur there.

## What one turn looks like (Agent Script agent)

The steps run in this order:
- `VARIABLE_UPDATE_STEP __state_update_action__`
- `CLASSIFIER_STEP pre_orchestration.guardrail` (~80 ms)
- `TOPIC_STEP agent_router` (~100 ms)
- `LLM_STEP <Topic>`: plans, picks the action and its inputs (~0.6 s)
- `ACTION_STEP <action>`: the action itself (Apex, Flow, prompt template…); usually the slowest step when it calls an LLM, e.g. a prompt-template action took ~5 s on average
- `LLM_STEP <Topic>`: writes the reply (~1–1.7 s)
- `TRUST_GUARDRAILS_STEP InstructionAdherence` and `LLM_STEP Atlas__GroundednessValidationPrompt`: post-checks, ~1–2 s, run after the reply is ready.

Step payloads (JSON text):

| Step | `ssot__InputValueText__c` | `ssot__OutputValueText__c` |
|---|---|---|
| `TOPIC_STEP agent_router` | `classifier.input` (user text), `af.router_classifier.choices` | `af.router_classifier.selected_target` |
| `LLM_STEP <Topic>` | the full resolved prompt (system + topic instructions + history) | the model's tool call or reply |
| `ACTION_STEP` | `{"actionName":…,"actionInput":{…the action's inputs…}}` | `{"actionName":…,"actionResponse":{"__action_execution_status__":"success",…the action's outputs…}}` |
| `TRUST_GUARDRAILS_STEP` | `mgr.llm.request_id` | `mgr.sensitive.step.result`: `InstructionAdherence: value=HIGH…; TaskResolution: value=FULLY_RESOLVED…` |

`ssot__AttributeText__c` on steps holds `internalTraceId` / `internalSpanId`, plus `progress_indicators` for actions.

## Recipes

Replace `<Agent_API_Name>` (the agent's API name, e.g. `My_Service_Agent`; list them with R9) and the ids with your own values. Every recipe below ran successfully against a live org.

### R1. Recent sessions for an agent, with turns and duration
```sql
WITH agent_sessions AS (
  SELECT DISTINCT ssot__AiAgentSessionId__c AS sid, ssot__AiAgentVersionApiName__c AS ver
  FROM ssot__AiAgentSessionParticipant__dlm
  WHERE ssot__AiAgentApiName__c = '<Agent_API_Name>' AND ssot__AiAgentSessionParticipantRole__c = 'AGENT')
SELECT s.ssot__Id__c AS session_id, a.ver, s.ssot__AiAgentChannelType__c AS channel,
       s.ssot__StartTimestamp__c AS started, s.ssot__RelatedMessagingSessionId__c AS messaging_session,
       COUNT(DISTINCT CASE WHEN i.ssot__AiAgentInteractionType__c = 'TURN'
                            AND i.ssot__TopicApiName__c <> 'NOT_SET' THEN i.ssot__Id__c END) AS user_turns,
       MAX(i.ssot__EndTimestamp__c) AS last_activity,
       MAX(CASE WHEN i.ssot__AiAgentInteractionType__c = 'SESSION_END' THEN 1 ELSE 0 END) AS ended
FROM ssot__AiAgentSession__dlm s
JOIN agent_sessions a ON a.sid = s.ssot__Id__c
LEFT JOIN ssot__AiAgentInteraction__dlm i ON i.ssot__AiAgentSessionId__c = s.ssot__Id__c
WHERE s.ssot__StartTimestamp__c >= current_date - INTERVAL '7' DAY
GROUP BY 1,2,3,4,5
ORDER BY started DESC
LIMIT 25
```

### R2. Transcript of one session
```sql
SELECT m.ssot__MessageSentTimestamp__c AS sent, i.ssot__TopicApiName__c AS topic,
       m.ssot__AiAgentInteractionMessageType__c AS dir, SUBSTR(m.ssot__ContentText__c, 1, 500) AS content
FROM ssot__AiAgentInteractionMessage__dlm m
JOIN ssot__AiAgentInteraction__dlm i
  ON i.ssot__Id__c = m.ssot__AiAgentInteractionId__c
 AND i.ssot__AiAgentSessionId__c = m.ssot__AiAgentSessionId__c
WHERE m.ssot__AiAgentSessionId__c = '<session-id>'
ORDER BY m.ssot__MessageSentTimestamp__c
```

### R3. Step trace of one session (what happened, how long each step took)
```sql
SELECT i.ssot__StartTimestamp__c AS turn_start, st.ssot__StartTimestamp__c AS step_start,
       st.ssot__AiAgentInteractionStepType__c AS step_type, st.ssot__Name__c AS name, st.SubType__c AS subtype,
       CAST(EXTRACT(EPOCH FROM (st.ssot__EndTimestamp__c - st.ssot__StartTimestamp__c)) * 1000 AS BIGINT) AS ms,
       SUBSTR(st.ssot__ErrorMessageText__c, 1, 200) AS err,
       SUBSTR(st.ssot__InputValueText__c, 1, 300) AS input_head,
       SUBSTR(st.ssot__OutputValueText__c, 1, 300) AS output_head
FROM ssot__AiAgentInteraction__dlm i
JOIN ssot__AiAgentInteractionStep__dlm st ON st.ssot__AiAgentInteractionId__c = i.ssot__Id__c
WHERE i.ssot__AiAgentSessionId__c = '<session-id>'
ORDER BY st.ssot__StartTimestamp__c
```
Leave out `input_head`/`output_head` for a compact view. Pull the full `ssot__InputValueText__c` of one `LLM_STEP` to see the exact prompt.

### R4. Failing steps for an agent
```sql
WITH agent_sessions AS (
  SELECT DISTINCT ssot__AiAgentSessionId__c AS sid FROM ssot__AiAgentSessionParticipant__dlm
  WHERE ssot__AiAgentApiName__c = '<Agent_API_Name>' AND ssot__AiAgentSessionParticipantRole__c = 'AGENT')
SELECT st.ssot__AiAgentInteractionStepType__c AS step_type, st.ssot__Name__c AS name,
       SUBSTR(st.ssot__ErrorMessageText__c, 1, 200) AS err, COUNT(*) AS n,
       MAX(st.ssot__StartTimestamp__c) AS last_seen, MIN(i.ssot__AiAgentSessionId__c) AS example_session
FROM ssot__AiAgentInteractionStep__dlm st
JOIN ssot__AiAgentInteraction__dlm i ON i.ssot__Id__c = st.ssot__AiAgentInteractionId__c
JOIN agent_sessions a ON a.sid = i.ssot__AiAgentSessionId__c
WHERE st.ssot__ErrorMessageText__c IS NOT NULL AND st.ssot__ErrorMessageText__c <> 'NOT_SET'
  AND LENGTH(st.ssot__ErrorMessageText__c) > 0
GROUP BY 1,2,3 ORDER BY n DESC LIMIT 50
```
Errors don't only appear in `ErrorMessageText`. Also check action outputs whose `__action_execution_status__` isn't `success` (R5), and replies that say "couldn't find" (R7).

### R5. Action calls: inputs, status, latency
```sql
WITH agent_sessions AS (
  SELECT DISTINCT ssot__AiAgentSessionId__c AS sid FROM ssot__AiAgentSessionParticipant__dlm
  WHERE ssot__AiAgentApiName__c = '<Agent_API_Name>' AND ssot__AiAgentSessionParticipantRole__c = 'AGENT')
SELECT st.ssot__StartTimestamp__c AS at, st.ssot__Name__c AS action, st.SubType__c AS kind,
       CAST(EXTRACT(EPOCH FROM (st.ssot__EndTimestamp__c - st.ssot__StartTimestamp__c)) * 1000 AS BIGINT) AS ms,
       SUBSTR(st.ssot__InputValueText__c, 1, 400) AS input,
       CASE WHEN STRPOS(st.ssot__OutputValueText__c, '"__action_execution_status__":"success"') > 0
              OR STRPOS(st.ssot__OutputValueText__c, 'ACTION_SUCCESS_RESPONSE') > 0 THEN 'success'
            WHEN STRPOS(st.ssot__OutputValueText__c, 'ACTION_ERROR_RESPONSE') > 0 THEN 'error'
            ELSE 'CHECK' END AS status,
       SUBSTR(st.ssot__OutputValueText__c, 1, 400) AS output_head,
       i.ssot__AiAgentSessionId__c AS session_id
FROM ssot__AiAgentInteractionStep__dlm st
JOIN ssot__AiAgentInteraction__dlm i ON i.ssot__Id__c = st.ssot__AiAgentInteractionId__c
JOIN agent_sessions a ON a.sid = i.ssot__AiAgentSessionId__c
WHERE st.ssot__AiAgentInteractionStepType__c = 'ACTION_STEP'
ORDER BY at DESC LIMIT 50
```
`input` shows the exact values the LLM filled in for the action's inputs. Use it to check how the agent rewrote or translated the user's question before calling the action.

### R6. Latency per step name (monitoring)
```sql
WITH agent_sessions AS (
  SELECT DISTINCT ssot__AiAgentSessionId__c AS sid FROM ssot__AiAgentSessionParticipant__dlm
  WHERE ssot__AiAgentApiName__c = '<Agent_API_Name>' AND ssot__AiAgentSessionParticipantRole__c = 'AGENT'),
d AS (
  SELECT st.ssot__AiAgentInteractionStepType__c AS step_type, st.ssot__Name__c AS name,
         EXTRACT(EPOCH FROM (st.ssot__EndTimestamp__c - st.ssot__StartTimestamp__c)) * 1000 AS ms
  FROM ssot__AiAgentInteractionStep__dlm st
  JOIN ssot__AiAgentInteraction__dlm i ON i.ssot__Id__c = st.ssot__AiAgentInteractionId__c
  JOIN agent_sessions a ON a.sid = i.ssot__AiAgentSessionId__c
  WHERE st.ssot__StartTimestamp__c >= current_date - INTERVAL '30' DAY)
SELECT step_type, name, COUNT(*) AS n, CAST(AVG(ms) AS BIGINT) AS avg_ms,
       CAST(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY ms) AS BIGINT) AS p95_ms, CAST(MAX(ms) AS BIGINT) AS max_ms
FROM d GROUP BY 1,2 ORDER BY avg_ms DESC
```
For end-to-end turn latency, use `MAX(Output message sent) - interaction StartTimestamp` per interaction.

### R7. Replies that didn't answer ("couldn't find")
```sql
WITH agent_sessions AS (
  SELECT DISTINCT ssot__AiAgentSessionId__c AS sid FROM ssot__AiAgentSessionParticipant__dlm
  WHERE ssot__AiAgentApiName__c = '<Agent_API_Name>' AND ssot__AiAgentSessionParticipantRole__c = 'AGENT')
SELECT q.ssot__AiAgentSessionId__c AS session_id, q.ssot__MessageSentTimestamp__c AS asked,
       SUBSTR(q.ssot__ContentText__c, 1, 200) AS question, SUBSTR(r.ssot__ContentText__c, 1, 300) AS reply
FROM ssot__AiAgentInteractionMessage__dlm q
JOIN ssot__AiAgentInteractionMessage__dlm r
  ON r.ssot__AiAgentInteractionId__c = q.ssot__AiAgentInteractionId__c
 AND r.ssot__AiAgentSessionId__c = q.ssot__AiAgentSessionId__c
 AND r.ssot__AiAgentInteractionMessageType__c = 'Output'
JOIN agent_sessions a ON a.sid = q.ssot__AiAgentSessionId__c
WHERE q.ssot__AiAgentInteractionMessageType__c = 'Input'
  AND (LOWER(r.ssot__ContentText__c) LIKE '%couldn''t find%' OR LOWER(r.ssot__ContentText__c) LIKE '%could not find%'
       OR LOWER(r.ssot__ContentText__c) LIKE '%not listed%' OR LOWER(r.ssot__ContentText__c) LIKE '%not available%')
ORDER BY asked DESC LIMIT 50
```
Change the phrases to match the agent's fallback wording. This is the fastest way to find knowledge or retrieval gaps.

### R8. Agent Analytics scores (deflection, abandonment, request category)
```sql
SELECT d.ssot__DeveloperName__c AS tag_def, d.ssot__Name__c AS metric, t.ssot__Value__c AS value,
       COUNT(DISTINCT a.ssot__AiAgentSessionId__c) AS sessions
FROM ssot__AiAgentTagAssociation__dlm a
JOIN ssot__AiAgentTag__dlm t ON t.ssot__Id__c = a.ssot__AiAgentTagId__c
JOIN ssot__AiAgentTagDefinition__dlm d ON d.ssot__Id__c = t.ssot__AiAgentTagDefinitionId__c
WHERE d.ssot__DeveloperName__c LIKE '%<Agent_API_Name>%'
GROUP BY 1,2,3 ORDER BY 1,3
```
- Tag definitions are `std_Deflection_Score_<Agent>_V<n>` (Number 0–5, 5 = fully resolved), `std_Abandonment_Score_<Agent>_V<n>` (`TRUE`/`FALSE`), and `AIE_Request_Category_<Agent>` (clustered topic label).
- `a.ssot__AssociationReasonText__c` holds the LLM judge's explanation.
- Per-session request and response summaries are in `ssot__AiAgentMoment__dlm` (`ssot__RequestSummaryText__c`, `ssot__ResponseSummaryText__c`, `ssot__AiAgentApiName__c`).
- `ssot__AiAgentMomentInteraction__dlm` maps moments to interactions.
- These come from Agent Analytics/Optimization batch jobs, so they lag behind the raw trace by hours.
- `AiAgentTag` isn't SOQL-queryable; use the DMO.

### R9. Volume by agent, channel and day
```sql
WITH agent_sessions AS (
  SELECT DISTINCT ssot__AiAgentSessionId__c AS sid, ssot__AiAgentApiName__c AS agent
  FROM ssot__AiAgentSessionParticipant__dlm WHERE ssot__AiAgentSessionParticipantRole__c = 'AGENT')
SELECT CAST(s.ssot__StartTimestamp__c AS DATE) AS day, a.agent, s.ssot__AiAgentChannelType__c AS channel,
       COUNT(DISTINCT s.ssot__Id__c) AS sessions
FROM ssot__AiAgentSession__dlm s JOIN agent_sessions a ON a.sid = s.ssot__Id__c
WHERE s.ssot__StartTimestamp__c >= current_date - INTERVAL '30' DAY
GROUP BY 1,2,3 ORDER BY 1 DESC, 4 DESC
```

### R10. Speed benchmark: reply time and where it goes
Turn reply time is first `Output` minus first `Input` message. Post-checks run after the reply, so the visitor doesn't wait on them.

Reference point (a sandbox Agent Script service agent with one retrieval + prompt-template action, 58 turns): reply avg 5.9 s, p95 11.2 s; the action alone avg 5.4 s. Save your own agent's numbers as a baseline before changing it.

Caveats:
- With under ~200 turns, p95 rests on 2–3 replies. Treat it as a rough signal.
- Sandbox timings aren't production timings.
- To exclude incident days, add `AND CAST(i.ssot__StartTimestamp__c AS DATE) NOT IN (DATE '…')` in `turns`.
```sql
WITH params AS (SELECT '<Agent_API_Name>' AS agent, 30 AS days_back),
agent_sessions AS (
  SELECT DISTINCT p.ssot__AiAgentSessionId__c AS sid, p.ssot__AiAgentVersionApiName__c AS ver
  FROM ssot__AiAgentSessionParticipant__dlm p JOIN params ON p.ssot__AiAgentApiName__c = params.agent
  WHERE p.ssot__AiAgentSessionParticipantRole__c = 'AGENT'),
turns AS (
  SELECT i.ssot__Id__c AS iid, i.ssot__AiAgentSessionId__c AS sid, j.ver
  FROM ssot__AiAgentInteraction__dlm i
  JOIN agent_sessions j ON j.sid = i.ssot__AiAgentSessionId__c
  CROSS JOIN params
  WHERE i.ssot__AiAgentInteractionType__c = 'TURN' AND i.ssot__TopicApiName__c <> 'NOT_SET' AND i.ssot__Id__c <> 'NOT_SET'
    AND i.ssot__StartTimestamp__c >= current_date - params.days_back * INTERVAL '1' DAY),
msgs AS (
  SELECT t.iid,
         MIN(CASE WHEN m.ssot__AiAgentInteractionMessageType__c = 'Input'  THEN m.ssot__MessageSentTimestamp__c END) AS asked_at,
         MIN(CASE WHEN m.ssot__AiAgentInteractionMessageType__c = 'Output' THEN m.ssot__MessageSentTimestamp__c END) AS answered_at
  FROM turns t JOIN ssot__AiAgentInteractionMessage__dlm m
    ON m.ssot__AiAgentInteractionId__c = t.iid AND m.ssot__AiAgentSessionId__c = t.sid
  GROUP BY t.iid),
steps AS (
  SELECT t.iid, st.ssot__AiAgentInteractionStepType__c AS step_type, st.ssot__Name__c AS name,
         st.ssot__StartTimestamp__c AS st_start, st.ssot__EndTimestamp__c AS st_end,
         EXTRACT(EPOCH FROM (st.ssot__EndTimestamp__c - st.ssot__StartTimestamp__c)) * 1000 AS ms
  FROM turns t JOIN ssot__AiAgentInteractionStep__dlm st ON st.ssot__AiAgentInteractionId__c = t.iid),
per_turn AS (
  SELECT t.iid,
         EXTRACT(EPOCH FROM (m.answered_at - m.asked_at)) * 1000 AS reply_ms,
         SUM(CASE WHEN s.step_type IN ('CLASSIFIER_STEP','TOPIC_STEP') THEN s.ms ELSE 0 END) AS routing_ms,
         SUM(CASE WHEN s.step_type = 'LLM_STEP' AND STRPOS(s.name, 'Atlas__') = 0 THEN s.ms ELSE 0 END) AS agent_llm_ms,
         SUM(CASE WHEN s.step_type = 'ACTION_STEP' THEN s.ms ELSE 0 END) AS action_ms,
         EXTRACT(EPOCH FROM (MAX(CASE WHEN s.step_type = 'TRUST_GUARDRAILS_STEP' OR STRPOS(s.name, 'Atlas__') = 1 THEN s.st_end END)
                           - MIN(CASE WHEN s.step_type = 'TRUST_GUARDRAILS_STEP' OR STRPOS(s.name, 'Atlas__') = 1 THEN s.st_start END))) * 1000 AS post_check_ms,
         SUM(CASE WHEN s.step_type = 'ACTION_STEP' THEN 1 ELSE 0 END) AS action_calls
  FROM turns t JOIN msgs m ON m.iid = t.iid LEFT JOIN steps s ON s.iid = t.iid
  WHERE m.asked_at IS NOT NULL AND m.answered_at IS NOT NULL
  GROUP BY t.iid, m.asked_at, m.answered_at),
metrics AS (
  SELECT '1. Reply time (visitor waits)' AS metric, reply_ms AS ms FROM per_turn
  UNION ALL SELECT '2. Routing (guardrail + router)', routing_ms FROM per_turn
  UNION ALL SELECT '3. Agent LLM calls (plan + answer)', agent_llm_ms FROM per_turn
  UNION ALL SELECT '4. Actions', action_ms FROM per_turn WHERE action_calls > 0
  UNION ALL SELECT '5. Post-checks (after reply, not waited on)', post_check_ms FROM per_turn WHERE post_check_ms IS NOT NULL)
SELECT metric, COUNT(*) AS turns, ROUND(AVG(ms)) AS avg_ms,
       ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY ms)) AS p50_ms,
       ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY ms)) AS p90_ms,
       ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY ms)) AS p95_ms,
       ROUND(MIN(ms)) AS min_ms, ROUND(MAX(ms)) AS max_ms
FROM metrics GROUP BY metric ORDER BY metric
```

**Daily trend** (compare days or versions before and after a change):
```sql
WITH agent_sessions AS (
  SELECT DISTINCT ssot__AiAgentSessionId__c AS sid, ssot__AiAgentVersionApiName__c AS ver
  FROM ssot__AiAgentSessionParticipant__dlm
  WHERE ssot__AiAgentApiName__c = '<Agent_API_Name>' AND ssot__AiAgentSessionParticipantRole__c = 'AGENT'),
per_turn AS (
  SELECT CAST(i.ssot__StartTimestamp__c AS DATE) AS day, j.ver,
         EXTRACT(EPOCH FROM (MIN(CASE WHEN m.ssot__AiAgentInteractionMessageType__c = 'Output' THEN m.ssot__MessageSentTimestamp__c END)
                           - MIN(CASE WHEN m.ssot__AiAgentInteractionMessageType__c = 'Input'  THEN m.ssot__MessageSentTimestamp__c END))) * 1000 AS reply_ms
  FROM ssot__AiAgentInteraction__dlm i
  JOIN agent_sessions j ON j.sid = i.ssot__AiAgentSessionId__c
  JOIN ssot__AiAgentInteractionMessage__dlm m
    ON m.ssot__AiAgentInteractionId__c = i.ssot__Id__c AND m.ssot__AiAgentSessionId__c = i.ssot__AiAgentSessionId__c
  WHERE i.ssot__AiAgentInteractionType__c = 'TURN' AND i.ssot__TopicApiName__c <> 'NOT_SET' AND i.ssot__Id__c <> 'NOT_SET'
    AND i.ssot__StartTimestamp__c >= current_date - INTERVAL '30' DAY
  GROUP BY i.ssot__Id__c, CAST(i.ssot__StartTimestamp__c AS DATE), j.ver)
SELECT day, ver, COUNT(*) AS turns, ROUND(AVG(reply_ms)) AS avg_ms,
       ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY reply_ms)) AS p50_ms,
       ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY reply_ms)) AS p95_ms,
       ROUND(MAX(reply_ms)) AS max_ms,
       SUM(CASE WHEN reply_ms > 10000 THEN 1 ELSE 0 END) AS turns_over_10s
FROM per_turn WHERE reply_ms IS NOT NULL
GROUP BY day, ver ORDER BY day DESC
```

## Tokens, metered actions and Flex Credits (verified November 2026)

Two sources, both in data space `default`, both joinable to STDM:

| Source | What it holds | Join |
|---|---|---|
| `GenAIGatewayRequest__dlm` (DMO) | One row per LLM call, with token counts, model and prompt name. Includes Builder preview | Gotcha 9 (strip the quotes) |
| `AiAgentGenerativeAiUsage__dll` (a **DLO**; query it by that name) | Agentforce metering: one row per action, turn or prompt, with `isMeteredIndicator__c`, `isBillableIndicator__c`, `meteringSkipReasonCode__c`, `usageQuantity__c`, `promptInputTokenCount__c` / `promptCompletionTokenCount__c` / `promptTotalTokenCount__c` | `u.aiAgentSessionId__c` = `ssot__AiAgentSession__dlm.ssot__Id__c` (285 of 285 rows matched). `ACTION` and `INTERACTION` rows carry `agentDeveloperName__c` and `aiAgentToolName__c`; `PROMPT` rows have no agent name, so filter them by session |

What the metering showed for an Agent Script service agent with one custom Apex action:

- **Each action call is one metered `ACTION` row:** `usageTypeCode__c = Agentforce_CustomAction`, `isMeteredIndicator__c = true`, `NOT_SKIPPED`, `usageQuantity__c = 1`, `aiAgentToolName__c` = the action name. Builder preview action calls are metered too.
- **Turns are `INTERACTION` rows and aren't metered** (skip reason `INTERACTION`).
- **The agent's LLM prompts aren't metered separately:** `PROMPT` rows with skip reason `AGENTFORCE_USAGE_WITH_FLEX_CREDITS` and `isMeteredIndicator__c = false`. Tokens are reported, not charged on their own.
- **Builder preview prompts have no `PROMPT` rows.** That agent's metering prompt tokens (5,661,152) equalled its gateway tokens minus the Builder preview rows exactly. Use the gateway (R11) for full token counts.
- **Filter on `isMeteredIndicator__c`, not `isBillableIndicator__c`.** Billable is `true` on some unmetered rows (messaging-channel `INTERACTION` rows, agent `PROMPT` rows).
- Salesforce's own agents (Setup, Flow) log `Agentforce_StandardAction` rows with skip reason `NON_BILLABLE_STANDARD_ACTION`. Coworker prompts (`AgentforceCoworker`, `EmbeddedAI_BasicPrompts`) are metered.
- **STDM `ACTION_STEP` count = metered action count.** Over the same period: 164 = 164, and none of 31 sessions differed. So for sessions before the metering rows start, count `ACTION_STEP`s instead (R12, second query).
- Metering rows start at the same time as the gateway's agent rows (2026-10-21 06:22 UTC in the verified org).

**Data 360 consumption is not in these sources.** The metering DLO has no row for Data 360 work an action triggers, such as a `hybrid_search` query run from Apex.
- The Digital Wallet DLOs exist (`TenantBillingUsageEvent__dll`, `TenantEnrichedUsageEvent__dll`, `TenantHourlyEntitlementConsumption__dll`, `TenantDailyEntitlementConsumption__dll`, `TenantUsageTypeMultiplier__dll`, `TenantEntitlementTransaction__dll`).
- In the verified sandbox they belonged to no data space (`d360_dlo_get` → `"dataSpaceInfo":[]`), so SQL returns "table does not exist", and the usage-event DLOs had 0 records.
- Read Data 360 consumption in Setup → Digital Wallet instead.
- Each query's result `status` includes `rowsProcessed` (one retriever `hybrid_search` query returning 8 passages processed 15,912 rows).

### R11. LLM tokens for an agent, per version, model and prompt
```sql
WITH agent AS (
  SELECT DISTINCT ssot__ParticipantId__c AS pid, ssot__AiAgentVersionApiName__c AS ver
  FROM ssot__AiAgentSessionParticipant__dlm
  WHERE ssot__AiAgentApiName__c = '<Agent_API_Name>' AND ssot__AiAgentSessionParticipantRole__c = 'AGENT')
SELECT a.ver, g.feature__c AS feature, g.model__c AS model,
       REPLACE(g.promptTemplateDevName__c, '"', '') AS prompt,
       COUNT(*) AS llm_calls, SUM(g.promptTokens__c) AS input_tokens,
       SUM(g.completionTokens__c) AS output_tokens, SUM(g.totalTokens__c) AS total_tokens,
       MIN(g.timestamp__c) AS first_call, MAX(g.timestamp__c) AS last_call
FROM GenAIGatewayRequest__dlm g
JOIN agent a ON a.pid = REPLACE(g.plannerId__c, '"', '')
GROUP BY 1,2,3,4 ORDER BY total_tokens DESC
```
- Builder preview rows come back as version `v0` (planner id `PlannerPreview-…`).
- Compare `first_call` with the agent's first session (R1/R9). Earlier sessions have no token counts.
- Input tokens dominate: 99.5% of one agent's 6.2 million tokens. Each `LLM_STEP` input is the full resolved prompt, with instructions, action results and the conversation so far.
- The `Atlas__GroundednessValidationPrompt` post-check is counted too. It was a third of one agent's tokens.

### R12. Metered actions and Flex Credits for an agent
Set `credits_per_action` to the contract rate. The rates the user supplied in November 2026 were 20 Flex Credits per action in production and 16 in a sandbox.
```sql
WITH params AS (SELECT '<Agent_API_Name>' AS agent, 20 AS credits_per_action)
SELECT u.featureDescriptorName__c AS feature, u.aiAgentToolName__c AS action, u.usageTypeCode__c AS usage_type,
       COUNT(*) AS metered_actions, SUM(u.usageQuantity__c) AS qty,
       SUM(u.usageQuantity__c) * MAX(params.credits_per_action) AS flex_credits,
       MIN(u.timestamp__c) AS first_ts, MAX(u.timestamp__c) AS last_ts
FROM AiAgentGenerativeAiUsage__dll u CROSS JOIN params
WHERE u.agentDeveloperName__c = params.agent AND u.unitTypeCode__c = 'ACTION' AND u.isMeteredIndicator__c = true
GROUP BY 1,2,3 ORDER BY metered_actions DESC
```
Action calls from before the metering rows start, from STDM. Multiply by the same rate; this applies to custom actions, because standard actions can be non-billable.
```sql
WITH params AS (SELECT '<Agent_API_Name>' AS agent),
agent_sessions AS (
  SELECT DISTINCT p.ssot__AiAgentSessionId__c AS sid FROM ssot__AiAgentSessionParticipant__dlm p
  JOIN params ON p.ssot__AiAgentApiName__c = params.agent WHERE p.ssot__AiAgentSessionParticipantRole__c = 'AGENT'),
first_meter AS (
  SELECT MIN(u.timestamp__c) AS ts FROM AiAgentGenerativeAiUsage__dll u
  JOIN params ON u.agentDeveloperName__c = params.agent WHERE u.unitTypeCode__c = 'ACTION')
SELECT s.ssot__AiAgentChannelType__c AS channel, st.ssot__Name__c AS action, COUNT(*) AS actions_before_meter,
       MIN(st.ssot__StartTimestamp__c) AS first_ts, MAX(st.ssot__StartTimestamp__c) AS last_ts
FROM ssot__AiAgentInteractionStep__dlm st
JOIN ssot__AiAgentInteraction__dlm i ON i.ssot__Id__c = st.ssot__AiAgentInteractionId__c
JOIN agent_sessions a ON a.sid = i.ssot__AiAgentSessionId__c
JOIN ssot__AiAgentSession__dlm s ON s.ssot__Id__c = a.sid
CROSS JOIN first_meter f
WHERE st.ssot__AiAgentInteractionStepType__c = 'ACTION_STEP' AND (f.ts IS NULL OR st.ssot__StartTimestamp__c < f.ts)
GROUP BY 1,2 ORDER BY 3 DESC
```

## Bridging to CRM records (SOQL)

| STDM value | CRM object |
|---|---|
| Session `ssot__RelatedMessagingSessionId__c` (`0Mw…`) | `MessagingSession.Id` |
| USER participant `ssot__ParticipantId__c` (`0PA…`) | `MessagingEndUser.Id`, which leads to `ContactId` (if the routing flow or pre-chat sets it) |
| AGENT participant `ssot__ParticipantId__c` (`16j…`) | `GenAiPlannerDefinition.Id` (the published agent) |
| Step `ssot__Name__c` on ACTION_STEP | action name in the `.agent` file or the agent's action list |

To go from a chat someone reports to its trace, find the `MessagingSession` Id in Salesforce, then run `WHERE s.ssot__RelatedMessagingSessionId__c = '0Mw…'`.

## Syntax that works in Data 360 SQL

- Timestamp literal `TIMESTAMP '2026-10-20 10:21:40.032+00:00'`.
- Relative dates `current_date - INTERVAL '7' DAY`.
- Durations `EXTRACT(EPOCH FROM (end - start)) * 1000`.
- `SUBSTR`, `LENGTH`, `LOWER`, `LIKE`, CTEs, `UNION ALL`, scalar subqueries, `COUNT(DISTINCT …)`, `PERCENTILE_CONT … WITHIN GROUP`.
- Escape `'` inside strings as `''`.
- Prefer the DMOs (`…__dlm`) over the raw DLOs.
- If expected rows are missing, check the data stream's Problem Records.
