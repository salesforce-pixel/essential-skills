# Get Insights from Agentforce Session Tracing Data | Salesforce Help

Source: https://help.salesforce.com/s/articleView?id=ai.generative_ai_session_trace_use.htm&type=5

QUICKSTART YOUR EINSTEIN GENERATIVE AI SOLUTION
Get Insights from Agentforce Session Tracing Data

To analyze Agentforce session tracing data, you can use observability dashboards, run queries, and build Data 360 reports using the data model.

REQUIRED EDITIONS
Available in: Enterprise, Performance, and Unlimited Editions with an Einstein for Sales, Einstein for Platform, Einstein for Service, Einstein 1 Service, or Einstein GPT Service add-on. To purchase add-ons, contact your Salesforce account executive.
USER PERMISSIONS NEEDED
To view and access reports and dashboards Data Cloud User

To access any pre-built reports and dashboards, make sure that you have Data Cloud User permissions. See Create Data Cloud Users and Assign Permissions.

Observability Dashboards

Visualize session tracing data by using these out-of-the-box observability features:

Agent Analytics analyzes your AI agents’ performance within user and agent sessions. To get started, see Set Up Agent Analytics.
Agent Optimization allows you to inspect agent sessions from the initial user request to the agent’s resolution. To get started, see Set Up Agent Optimization.
Example Queries

To analyze Agentforce session tracing data, run queries on the applicable DMOs in the session tracing data model. See Query Data in Data 360.

NOTE The query examples use the default dataspace prefix ssot__. If your Salesforce org uses a custom dataspace, replace ssot with your dataspace's prefix (for example, std).
Example: Simple Query
SELECT *
FROM "ssot__AiAgentSession__dlm"
JOIN "ssot__AiAgentSessionParticipant__dlm" ON "ssot__AiAgentSession__dlm"."ssot__Id__c" = "ssot__AiAgentSessionParticipant__dlm"."ssot__AiAgentSessionId__c"
JOIN "ssot__AiAgentInteraction__dlm" ON "ssot__AiAgentSession__dlm"."ssot__Id__c" = "ssot__AiAgentInteraction__dlm"."ssot__AiAgentSessionId__c"
JOIN "ssot__AiAgentInteractionMessage__dlm" ON "ssot__AiAgentInteraction__dlm"."ssot__Id__c" = "ssot__AiAgentInteractionMessage__dlm"."ssot__AiAgentInteractionId__c"
JOIN "ssot__AiAgentInteractionStep__dlm" ON "ssot__AiAgentInteraction__dlm"."ssot__Id__c" = "ssot__AiAgentInteractionStep__dlm"."ssot__AiAgentInteractionId__c"
WHERE "ssot__AiAgentSession__dlm"."ssot__Id__c" = 'your_uuid'
LIMIT 10

where your_uuid is a user-specified UUID.

Example: Get Recent Sessions

This example query gets a list of recent sessions. You can change the internal days to see the session count data.

SELECT
ssot__Id__c,
ssot__StartTimestamp__c
FROM ssot__AiAgentSession__dlm s
WHERE s.ssot__StartTimestamp__c >= current_date - INTERVAL '7' DAY
ORDER BY s.ssot__StartTimestamp__c DESC;
NOTE Session counts in STDM and MessagingSession can differ because each system defines a session differently. STDM records a session for each agent invocation, while MessagingSession keeps persistent context for returning authenticated users.
Example: Get All Messages Within an Interaction

This example query gets all messages (user text or agent text) within a given interaction. It searches by interaction ID.

SELECT
ssot__AiAgentInteractionId__c AS InteractionId,
ssot__AiAgentInteractionMessageType__c, -- user or agent
ssot__AiAgentInteractionMsgContentType__c, -- e.g., text
ssot__ContentText__c,
ssot__AiAgentSessionParticipantId__c AS SenderParticipantId,
ssot__ParentMessageId__c -- if part of a thread
FROM "ssot__AiAgentInteractionMessage__dlm"
WHERE ssot__AiAgentInteractionId__c = '<given-interaction-id>' --'0199aac4-1047-70f3-8311-94d0d1678bb4'
ORDER BY ssot__MessageSentTimestamp__c ASC;
Example: Find Interaction Steps with Errors

This example query gets all interaction steps with errors.

SELECT
ssot__AiAgentInteractionId__c AS InteractionId,
ssot__Id__c AS StepId,
ssot__Name__c AS StepName,
ssot__InputValueText__c AS Input,
ssot__ErrorMessageText__c AS StepErrorMessage
FROM "ssot__AiAgentInteractionStep__dlm"
WHERE length(ssot__ErrorMessageText__c) > 0 AND ssot__ErrorMessageText__c != 'NOT_SET'
LIMIT 100;
Example: Integrate Feedback or Guardrails Metrics

The Session Trace data model includes reference fields for every LLM call the reasoning engine makes (generationRequestId, generationId, and gatewayResponseId). To incorporate feedback data or guardrails metrics in your analysis, join these fields when writing queries and building reports. Example:

SELECT *
FROM "ssot__AiAgentSession__dlm"
JOIN "ssot__AiAgentSessionParticipant__dlm" ON "ssot__AiAgentSession__dlm"."ssot__Id__c" = "ssot__AiAgentSessionParticipant__dlm"."ssot__AiAgentSessionId__c"
JOIN "ssot__AiAgentInteraction__dlm" ON "ssot__AiAgentSession__dlm"."ssot__Id__c" = "ssot__AiAgentInteraction__dlm"."ssot__AiAgentSessionId__c"
JOIN "ssot__AiAgentInteractionMessage__dlm" ON "ssot__AiAgentInteraction__dlm"."ssot__Id__c" = "ssot__AiAgentInteractionMessage__dlm"."ssot__AiAgentInteractionId__c"
JOIN "ssot__AiAgentInteractionStep__dlm" ON "ssot__AiAgentInteraction__dlm"."ssot__Id__c" = "ssot__AiAgentInteractionStep__dlm"."ssot__AiAgentInteractionId__c"
LIMIT 10
Example: Get Interactions from Session Tracing and Feedback Data

This example query gets a list of interactions from session tracing and feedback from Audit and Feedback data.

NOTE The GenAI*__dlm objects come from Audit and Feedback, so they don't use the ssot__ prefix.
SELECT
step.ssot__AiAgentInteractionId__c AS InteractionId,
step.ssot__Name__c AS StepName,
req.prompt__c AS InputPrompt,
gen.responseText__c AS LLMResponse,
fb.feedback__c AS Feedback
FROM ssot__AiAgentInteractionStep__dlm step
JOIN GenAIGatewayRequest__dlm req
ON step.ssot__GenAiGatewayRequestId__c = req.gatewayRequestId__c
JOIN GenAIGeneration__dlm gen
ON step.ssot__GenerationId__c = gen.generationId__c
LEFT JOIN GenAIFeedback__dlm fb
ON req.generationGroupId__c = fb.generationGroupId__c
LIMIT 100
Example: Get a Session’s Related Records in a Flat List

One agent session contains many records from related objects. Use this query to see all of a session’s records in a flattened list sorted by timestamp. Replace <your sessionID> with your session ID.

WITH
-- Keep session ID in temp table for easier reference
params AS (
SELECT '<your sessionID>' AS session_id
),
-- Retrieve the agent interactions and agent interaction messages to see each turn and input/output messages per turn
interactionsWithMessages AS (
SELECT
I.ssot__AiAgentInteractionType__c AS InteractionType,
I.ssot__StartTimestamp__c AS InteractionStartTime,
I.ssot__EndTimestamp__c AS InteractionEndTime,
I.ssot__TopicApiName__c AS TopicName,
M.ssot__MessageSentTimestamp__c AS MessageSentTime,
M.ssot__ContentText__c AS ContextText,
M.ssot__AiAgentInteractionMessageType__c AS InteractionMessageType
FROM ssot__AiAgentSession__dlm AS S
JOIN ssot__AiAgentInteraction__dlm AS I ON S.ssot__Id__c = I.ssot__AiAgentSessionId__c
JOIN ssot__AiAgentInteractionMessage__dlm AS M ON I.ssot__Id__c = M.ssot__AiAgentInteractionId__c
JOIN params AS p ON S.ssot__Id__c = p.session_id
),
-- Retrieve the agent interactions and agent interaction steps performed on each turn by the agent to generate its output
interactionsWithSteps AS (
SELECT
I.ssot__AiAgentInteractionType__c AS InteractionType,
I.ssot__StartTimestamp__c AS InteractionStartTime,
I.ssot__EndTimestamp__c AS InteractionEndTime,
I.ssot__TopicApiName__c AS TopicName,
St.ssot__AiAgentInteractionStepType__c AS InteractionStepType,
St.ssot__Name__c AS Name,
St.ssot__InputValueText__c AS InputValueText,
St.ssot__OutputValueText__c AS OutputValueText,
St.ssot__StartTimestamp__c AS InteractionStepStartTime,
St.ssot__PreStepVariableText__c AS PreStepVariableText,
St.ssot__PostStepVariableText__c AS PostStepVariableText
FROM ssot__AiAgentSession__dlm AS S
JOIN ssot__AiAgentInteraction__dlm AS I ON S.ssot__Id__c = I.ssot__AiAgentSessionId__c
JOIN ssot__AiAgentInteractionStep__dlm AS St ON I.ssot__Id__c = St.ssot__AiAgentInteractionId__c
JOIN params AS p ON S.ssot__Id__c = p.session_id
),
-- Join both data sets
interactionsWithMessagesAndSteps AS (
SELECT
*,
CAST(NULL AS VARCHAR) AS InteractionStepType,
CAST(NULL AS VARCHAR) AS Name,
CAST(NULL AS VARCHAR) AS InputValueText,
CAST(NULL AS VARCHAR) AS OutputValueText,
CAST(NULL AS VARCHAR) AS PreStepVariableText,
CAST(NULL AS VARCHAR) AS PostStepVariableText
FROM interactionsWithMessages
UNION ALL
SELECT
InteractionType,
InteractionStartTime,
InteractionEndTime,
TopicName,
-- Use InteractionStepStartTime as MessageSentTime to sort unified records
InteractionStepStartTime AS MessageSentTime,
CAST(NULL AS VARCHAR) AS ContextText,
CAST(NULL AS VARCHAR) AS InteractionMessageType,
InteractionStepType,
Name,
InputValueText,
OutputValueText,
PreStepVariableText,
PostStepVariableText
FROM interactionsWithSteps
)
-- Reorder fields and sort them by MessageSentTime
SELECT
TopicName, InteractionType, InteractionStartTime, InteractionEndTime,
MessageSentTime, InteractionMessageType, ContextText,
InteractionStepType, Name, InputValueText, OutputValueText, PreStepVariableText, PostStepVariableText
FROM interactionsWithMessagesAndSteps
ORDER BY MessageSentTime ASC

Example: List of Records for a Session

Example: Check for Duplicate Records
NOTE Data 360 streaming ingestion and Agentforce use at-least-once delivery semantics to prioritize data durability and avoid data loss during retry and recovery scenarios. In rare cases, this can result in the delivery of the same logical record more than once. Salesforce is working to reduce significantly the occurrence of duplicate records. For downstream systems that require strict uniqueness, however, be sure to apply an appropriate deduplication or upsert strategy.

These example queries show how to check whether messages from the same logical participant reuse its existing session participant record.

First, query the session participants using the session ID.

SELECT "ssot__Id__c", "ssot__ParticipantObject__c", "ssot__DataSourceObjectId__c"
FROM "ssot__AiAgentSessionParticipant__dlm"
WHERE "ssot__AiAgentSessionId__c" = '<YOUR_AGENT_SESSION_ID>'

Where YOUR_AGENT_SESSION_ID is the agent session ID.

Next, run this query.

SELECT "ssot__AiAgentSessionParticipantId__c", "ssot__ContentText__c"
FROM "ssot__AiAgentInteractionMessage__dlm"
WHERE "ssot__AiAgentSessionId__c" = '<YOUR_AGENT_SESSION_ID>'

Compare each message's ssot__AiAgentSessionParticipantId__c with the participant records' ssot__Id__c. Check whether messages from the same logical participant reuse its existing session participant record.

Here are the expected results:

Within a session involving one agent and one end user, each distinct logical participant should have a single AiAgentSessionParticipant record.
Subsequent AiAgentInteractionMessage records from that participant should reference the existing participant ID, without creating duplicate session participant records.
Your deduplication or upsert strategy should address instances in which duplicate records occur.
Build Data 360 Reports

To analyze Agentforce session trace data, build reports in Data 360 that pull relevant information from the applicable DMOs in the session tracing data model. You can use calculated insights to create metrics that can trigger alerts. To learn more, including required permissions, see Data 360 Reports and Dashboards.
