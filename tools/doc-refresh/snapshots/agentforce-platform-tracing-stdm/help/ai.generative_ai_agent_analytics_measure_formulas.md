# Agentforce Observability Measure Formulas | Salesforce Help

Source: https://help.salesforce.com/s/articleView?id=ai.generative_ai_agent_analytics_measure_formulas.htm&type=5

QUICKSTART YOUR EINSTEIN GENERATIVE AI SOLUTION
Agentforce Observability Measure Formulas

These formulas show how Agentforce Observability calculates measures in the Agentforce Analytics Foundations semantic data model. Use them to understand the metrics available for reporting.

REQUIRED EDITIONS
REQUIRED EDITIONS
Agentforce Observability is available in Salesforce Enterprise, Performance, and Unlimited Editions with Salesforce Foundations or Agentforce 1 Edition.
Session and Interaction Metrics
Measure Formulas
LABEL CX DESCRIPTION FIELD NAME FORMULA
Abandon Rate The percentage of engaged sessions with an Abandon Status of true. A session is engaged when the customer sent at least one message. Calculated as Abandoned Sessions divided by Engaged Sessions. Abandonment_Rate_clc
[Abandoned_Sessions_clc]/[Engaged_Sessions_clc]

Abandoned Sessions The number of unique sessions with an Abandon Status of true. A session is abandoned when it wasn't transferred, the latest Abandonment Score is true, and the latest Deflection Score is 3 or lower or unavailable. Abandoned_Sessions_clc
COUNTD(IF [Abandonment_Status_clc] THEN [AI_Agent_Session].[AI_Agent_Session_Id] END)

Deflected Sessions The number of unique sessions with a Deflection Status of true. A session is deflected when it wasn't transferred and the latest Deflection Score is 4 or 5, meaning the customer's main request was mostly or fully resolved. Deflected_Sessions_clc
COUNTD(IF [Deflection_Status_clc] THEN [AI_Agent_Session].[AI_Agent_Session_Id] END)

Deflection Rate The percentage of engaged sessions with a Deflection Status of true. A session is engaged when the customer sent at least one message. Calculated as Deflected Sessions divided by Engaged Sessions. Deflection_Rate_clc
[Deflected_Sessions_clc]/[Engaged_Sessions_clc]

Engaged Sessions Counts sessions that include an engaged interaction. Engaged_Sessions_clc
COUNTD( IF [Engagement_Status_clc] THEN [AI_Agent_Interaction].[AI_Agent_Session] END )

Engagement Rate Shows the share of all sessions that include an engaged interaction. Engagement_Rate_clc
[Engaged_Sessions_clc]/[Unique_Sessions_clc]

Escalated Sessions Counts sessions that are marked as escalated. Escalated_Sessions_clc
COUNTD(IF [Escalation_Status_clc] THEN [AI_Agent_Session].[AI_Agent_Session_Id] END)

Escalation Rate Shows the share of engaged sessions that are escalated. Escalation_Rate_clc
[Escalated_Sessions_clc]/[Engaged_Sessions_clc]

Success Rate Shows the share of turn interactions that include an action step without an error. Success_Rate_clc
COUNTD(
IF [AI_Agent_Interaction_Step].[Ai_Agent_Interaction_Step_Type] = 'ACTION_STEP'
AND [Is_Step_With_Error_clc] = FALSE
THEN [AI_Agent_Interaction].[AI_Agent_Interaction_Id]
END
) / [Unique_Interactions_clc]

Unique Interactions Counts unique turn interactions. Unique_Interactions_clc
COUNTD(IF [AI_Agent_Interaction].[Ai_Agent_Interaction_Type] = 'TURN' THEN [AI_Agent_Interaction].[AI_Agent_Interaction_Id] END)

Unique Moments Counts unique agent moments. Unique_Moments_clc
COUNTD([AI_Agent_Moment].[AI_Agent_Moment_Id])

Unique Sessions Counts unique agent sessions. Unique_Sessions_clc
COUNTD([AI_Agent_Session].[AI_Agent_Session_Id])

Unique Users Counts unique user participants, including messaging end users and users. Unique_Users_clc
COUNTD(
IF
[AI_Agent_Session_Participant_Extended_lv].[AI_Agent_Session_Participant_Ext_AI_Agent_Session_Participant_Role] = 'USER'
AND
[AI_Agent_Session_Participant_Extended_lv].[AI_Agent_Session_Participant_Ext_Participant_Object] IN ('MessagingEndUser', 'User')
THEN
[AI_Agent_Session_Participant_Extended_lv].[AI_Agent_Session_Participant_Ext_Participant]
END
)

Average Interactions Per Session Shows the average number of turn interactions in sessions that have ended. Average_Interactions_Per_Session_clc
AVG(IF [Is_Session_Ended_clc] THEN
{FIXED[AI_Agent_Session].[AI_Agent_Session_Id]:[Unique_Interactions_clc]}
END)

Average User Interactions Shows the average number of turn interactions for each user participant. Average_User_Interactions_clc
AVG(
IF [Is_User_clc]
THEN
{ FIXED [AI_Agent_Session_Participant].[Participant] : [Unique_Interactions_clc] }
END
)

Average Moment Duration Shows the average duration of agent moments, in seconds. Average_Moment_Duration_clc
AVG([Moment_Duration_clc])

Average Session Duration Shows the average duration of sessions, in seconds. Average_Session_Duration_clc
AVG([Session_Duration_clc])

Average Agent Interaction Duration Shows the average duration of turn interactions, in seconds. Average_Agent_Interaction_Latency_clc
AVG(IF [AI_Agent_Interaction].[Ai_Agent_Interaction_Type] = 'TURN' THEN [Agent_Interaction_Latency_clc] END)

Agent to User Message Ratio Compares the number of agent messages with the number of user messages. Agent_User_Message_Ratio_clc
[Total_Agent_Messages_clc]
/
[Total_User_Messages_clc]

Total Agent Messages Counts messages sent by the agent. Total_Agent_Messages_clc
COUNTD(
IF [AI_Agent_Session_Participant].[AI_Agent_Session_Participant_Role] = "AGENT"
THEN [AI_Agent_Interaction_Message].[AI_Agent_Interaction_Message_Id]
ELSE NULL
END
)

Total Agent Triggered Actions Counts action steps triggered by the agent. Total_Agent_Triggered_Actions_clc
COUNTD(
IF [AI_Agent_Interaction_Step].[Ai_Agent_Interaction_Step_Type] = "ACTION_STEP"
THEN [AI_Agent_Interaction_Step].[AI_Agent_Interaction_Step_Id]
ELSE NULL
END
)

Total User Messages Counts messages sent by users. Total_User_Messages_clc
COUNTD(
IF [Is_User_clc]
THEN [AI_Agent_Interaction_Message].[AI_Agent_Interaction_Message_Id]
ELSE NULL
END
)

Unique Tags Counts unique agent tags. Unique_Tags_clc
COUNTD([AI_Agent_Tag].[AI_Agent_Tag_Id])

Interaction Error Rate Shows the share of turn interactions that contain an error step. Error_Rate_clc
COUNTD(IF [Is_Step_With_Error_clc] THEN [AI_Agent_Interaction].[AI_Agent_Interaction_Id] END) / [Unique_Interactions_clc]

Total Errors Counts interaction steps identified as errors. Total_Errors_clc
COUNTD(IF [Is_Step_With_Error_clc] THEN [AI_Agent_Interaction_Step].[AI_Agent_Interaction_Step_Id] END)

Interruption Rate Shows the share of turn interactions where a user interruption has a recorded value. Interruption_Rate_clc
COUNTD(
IF [AI_Agent_Interaction_Step].[Ai_Agent_Interaction_Step_Type] = 'INTERRUPT_STEP'
AND NOT ISNULL([AI_Agent_Interaction_Step].[Output_Value])
AND LEN(TRIM([AI_Agent_Interaction_Step].[Output_Value])) > 0
AND [AI_Agent_Interaction_Step].[Output_Value] != 'NOT_SET'
THEN [AI_Agent_Interaction_Step].[AI_Agent_Interaction]
END
)
/
[Unique_Interactions_clc]

Total User Interruptions Counts user interruption steps with a recorded value. Total_User_Interruptions_clc
COUNTD(
IF [AI_Agent_Interaction_Step].[Ai_Agent_Interaction_Step_Type] = 'INTERRUPT_STEP'
AND NOT ISNULL([AI_Agent_Interaction_Step].[Output_Value])
AND LEN(TRIM([AI_Agent_Interaction_Step].[Output_Value])) > 0
AND [AI_Agent_Interaction_Step].[Output_Value] != 'NOT_SET'
THEN [AI_Agent_Interaction_Step].[AI_Agent_Interaction_Step_Id]
END
)
Response and Voice Metrics
Measure Formulas
LABEL CX DESCRIPTION FIELD NAME FORMULA
Turn Completion Rate Shows the share of user turns that receive an agent response within 60 seconds. Agent_Response_Rate_clc
[User_Turns_With_Response_clc] / [Total_User_Turns_clc]

Total User Turns Counts user turns. Total_User_Turns_clc
COUNTD(IF [Is_User_Turn_clc] THEN [AI_Agent_Interaction].[AI_Agent_Interaction_Id] END)

User Turns With Response Counts user turns that receive an agent response within 60 seconds. User_Turns_With_Response_clc
COUNTD(IF [Agent_Response_Within_60s_clc] THEN [AI_Agent_Interaction].[AI_Agent_Interaction_Id] END)

Average Agent Response Latency Shows the average time until the agent starts responding after a user message ends. Average_Agent_Response_Latency_clc
AVG([Time_To_First_Agent_Token_clc])

Average Agent Response Completion Latency Shows the average time until the agent finishes responding after a user message ends. Average_Agent_Response_Duration_clc
AVG([Time_To_Last_Agent_Token_clc])

Agent Response Latency (P50) Shows the midpoint response latency: half of responses start sooner and half start later. Time_To_First_Agent_Token_P50_clc
PERCENTILE([Time_To_First_Agent_Token_clc], 0.5)

Agent Response Latency (P90) Shows the response latency that 90% of responses meet or improve on. Time_To_First_Agent_Token_P90_clc
PERCENTILE([Time_To_First_Agent_Token_clc], 0.9)

Agent Response Latency (P95) Shows the response latency that 95% of responses meet or improve on. Time_To_First_Agent_Token_P95_clc
PERCENTILE([Time_To_First_Agent_Token_clc], 0.95)

Agent Response Latency (P99) Shows the response latency that 99% of responses meet or improve on. Time_To_First_Agent_Token_P99_clc
PERCENTILE([Time_To_First_Agent_Token_clc], 0.99)

Agent Response Completion Latency (P50) Shows the midpoint completion latency: half of responses finish sooner and half finish later. Time_To_Last_Agent_Token_P50_clc
PERCENTILE([Time_To_Last_Agent_Token_clc], 0.5)

Agent Response Completion Latency (P90) Shows the completion latency that 90% of responses meet or improve on. Time_To_Last_Agent_Token_P90_clc
PERCENTILE([Time_To_Last_Agent_Token_clc], 0.9)

Agent Response Completion Latency (P95) Shows the completion latency that 95% of responses meet or improve on. Time_To_Last_Agent_Token_P95_clc
PERCENTILE([Time_To_Last_Agent_Token_clc], 0.95)

Agent Response Completion Latency (P99) Shows the completion latency that 99% of responses meet or improve on. Time_To_Last_Agent_Token_P99_clc
PERCENTILE([Time_To_Last_Agent_Token_clc], 0.99)

Total Agent Talk Duration Shows total agent speaking time for voice sessions with complete message timestamps. Total_Agent_Talk_Duration_clc
SUM(
IF NOT ISNULL([AI_Agent_Session].[Related_Voice_Call])
AND [AI_Agent_Session].[Related_Voice_Call] != 'NOT_SET'
AND [AI_Agent_Interaction_Message].[AI_Agent_Interaction_Message_Type] = 'Output'
AND NOT ISNULL([AI_Agent_Interaction_Message].[Message_Start_Timestamp])
AND YEAR([AI_Agent_Interaction_Message].[Message_Start_Timestamp]) > 1970
AND NOT ISNULL([AI_Agent_Interaction_Message].[Message_End_Timestamp])
AND YEAR([AI_Agent_Interaction_Message].[Message_End_Timestamp]) > 1970
THEN DATEDIFF('MILLISECONDS', [AI_Agent_Interaction_Message].[Message_Start_Timestamp], [AI_Agent_Interaction_Message].[Message_End_Timestamp]) / 1000.0
END
)

Total User Talk Duration Shows total user speaking time for voice sessions with complete message timestamps. Total_User_Talk_Duration_clc
SUM(
IF NOT ISNULL([AI_Agent_Session].[Related_Voice_Call])
AND [AI_Agent_Session].[Related_Voice_Call] != 'NOT_SET'
AND [AI_Agent_Interaction_Message].[AI_Agent_Interaction_Message_Type] = 'Input'
AND NOT ISNULL([AI_Agent_Interaction_Message].[Message_Start_Timestamp])
AND YEAR([AI_Agent_Interaction_Message].[Message_Start_Timestamp]) > 1970
AND NOT ISNULL([AI_Agent_Interaction_Message].[Message_End_Timestamp])
AND YEAR([AI_Agent_Interaction_Message].[Message_End_Timestamp]) > 1970
THEN DATEDIFF('MILLISECONDS', [AI_Agent_Interaction_Message].[Message_Start_Timestamp], [AI_Agent_Interaction_Message].[Message_End_Timestamp]) / 1000.0
END
)

Agent Talk Ratio Shows the proportion of voice-session talk time used by the agent. Agent_Talk_Ratio_clc
[Total_Agent_Talk_Duration_clc]
/
([Total_Agent_Talk_Duration_clc] + [Total_User_Talk_Duration_clc])
Feedback, Trust Layer, and Scorer Metrics
Measure Formulas
LABEL CX DESCRIPTION FIELD NAME FORMULA
Positive User Feedback Counts interactions whose latest user feedback is positive. Positive_User_Feedback_clc
COUNTD(IF [User_Feedback_Status_clc] = 'Positive' THEN [AI_Agent_Interaction].[AI_Agent_Interaction_Id] END)

Negative User Feedback Counts interactions whose latest user feedback is negative. Negative_User_Feedback_clc
COUNTD(IF [User_Feedback_Status_clc] = 'Negative' THEN [AI_Agent_Interaction].[AI_Agent_Interaction_Id] END)

Average Answer Faithfulness Score Shows the average faithfulness score for interactions with telemetry data. Average_Answer_Faithfulness_Score_clc
AVG(IF NOT ISNULL([AI_Agent_Interaction].[Telemetry_Trace]) AND [AI_Agent_Interaction].[Telemetry_Trace] != 'NOT_SET' THEN [AI_Retriever_Quality_Metric].[Faithfulness_Relevancy_Score] END)

Average Answer Relevance Score Shows the average answer relevance score for interactions with telemetry data. Average_Answer_Relevance_Score_clc
AVG(IF NOT ISNULL([AI_Agent_Interaction].[Telemetry_Trace]) AND [AI_Agent_Interaction].[Telemetry_Trace] != 'NOT_SET' THEN [AI_Retriever_Quality_Metric].[Answer_Relevancy_Score] END)

Average Context Relevance Score Shows the average context precision score for interactions with telemetry data. Average_Context_Relevance_Score_clc
AVG(IF NOT ISNULL([AI_Agent_Interaction].[Telemetry_Trace]) AND [AI_Agent_Interaction].[Telemetry_Trace] != 'NOT_SET' THEN [AI_Retriever_Quality_Metric].[Context_Precision_Score] END)

Average Agent Toxicity Score Shows the average toxicity score for generated agent output. Average_Agent_Toxicity_Score_clc
AVG(IF [AI_Agent_Interaction_Step].[Generation] != 'NOT_SET' AND [Categorized_Content_Quality_View_lv].[Ai_Content_Quality_Category2_Detector_Type] = 'TOXICITY' AND [Categorized_Content_Quality_View_lv].[Ai_Content_Quality_Content_Type] = 'OUTPUT' THEN FLOAT([Categorized_Content_Quality_View_lv].[Ai_Content_Quality_Category2_Value]) END)

Average Quality Score Shows the average quality score. Average_Quality_Score_clc
AVG([Quality_Score_clc])

Quality Score Reasoning Shows the reason associated with the moment quality score. Quality_Score_Reasoning_clc
[AI_Agent_Moment_Quality_Score_lv].[AI_Agent_Tag_Association2_Association_Reason]

High Adherence Response Rate Shows the share of evaluated interaction steps with a High instruction-adherence rating. High_Adherence_Response_Rate_clc
COUNTD(IF [Agent_Adherence_Status_clc] = 'High' THEN [AI_Agent_Interaction_Step].[AI_Agent_Interaction_Step_Id] END)
/
COUNTD(IF NOT ISNULL([Agent_Adherence_Status_clc]) THEN [AI_Agent_Interaction_Step].[AI_Agent_Interaction_Step_Id] END)

Task Resolution Rate Shows the share of evaluated sessions that are fully resolved. Task_Resolution_Rate_clc
COUNTD(IF [Task_Resolution_Status_clc] = 'FULLY_RESOLVED' THEN [AI_Agent_Session].[AI_Agent_Session_Id] END)
/ COUNTD(IF NOT ISNULL([Task_Resolution_Status_clc]) THEN [AI_Agent_Session].[AI_Agent_Session_Id] END)

Intent Scorer Aggregation Shows the average latest score for the intent scorer selected by the Intent Scorer API Name parameter. Intent_Scorer_Aggregation_clc
AVG(
IF [AI_Agent_Tag_Definition].[Tag_Identifier] = [Parameters].[Intent_Scorer_Api_Name_prm]
AND [Is_Latest_Intent_Scorer_clc] = TRUE
THEN FLOAT([AI_Agent_Tag].[Value])
END
)

Interaction Scorer Aggregation Shows the average latest score for the interaction scorer selected by the Interaction Scorer API Name parameter. Interaction_Scorer_Aggregation_clc
AVG(
IF [AI_Agent_Interaction_Tag_Association_lv].[AI_Agent_Tag_Definition3_Tag_Identifier] = [Parameters].[Interaction_Scorer_Api_Name_prm]
AND [Is_Latest_Interaction_Scorer_clc] = TRUE
THEN FLOAT([AI_Agent_Interaction_Tag_Association_lv].[AI_Agent_Tag3_Value])
END
)

Session Scorer Aggregation Shows the average latest score for the session scorer selected by the Session Scorer API Name parameter. Session_Scorer_Aggregation_clc
AVG(
IF [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Tag_Identifier] = [Parameters].[Session_Scorer_Api_Name_prm]
AND [Is_Latest_Session_Scorer_clc] = TRUE
THEN
FLOAT(
IF
NOT ISNULL([AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Association3_Value]) AND [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Association3_Value] != 'NOT_SET'
THEN [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Association3_Value]
ELSE [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag2_Value]
END
)
END
)

Stickiness Rate Compares average daily active users with average monthly active users. Stickiness_Ratio_clc
(AVG(IF [Is_User_clc] THEN {FIXED DATE([AI_Agent_Session].[Start_Timestamp]): [Unique_Users_clc]} END)) / (AVG({FIXED UPPER(LEFT(DATENAME("Month", [AI_Agent_Session].[Start_Timestamp]),3)) + " " + STR(YEAR([AI_Agent_Session].[Start_Timestamp])): [Unique_Users_clc]}))
Usage and Connected Subagent Metrics
Measure Formulas
LABEL CX DESCRIPTION FIELD NAME FORMULA
Total Flex Credits The total number of Flex Credits consumed by the agent. Only orgs with Digital Wallet enabled are included. Total_Flex_Credits_clc
SUM(
IF 1=1 THEN
{ FIXED [Tenant_Consumption_Insights].[ID] : MAX(
IF [Tenant_Consumption_Insights].[Card_Definition_Developer_Name] = 'FlexCredits'
THEN [Tenant_Consumption_Insights].[Units_Consumed]
ELSE 0
END
) }
ELSE 0 END
)

Average Connected Subagent Orchestration Duration Shows the average time to delegate work to a connected subagent, in milliseconds. Average_Connected_Subagent_Orchestration_Duration_clc
AVG([Connected_Subagent_Orchestration_Duration_ms_clc])

Average Connected Subagent Execution Duration Shows the average connected-subagent execution time, in milliseconds. Average_Connected_Subagent_Execution_Duration_clc
AVG([Connected_Subagent_Execution_Duration_ms_clc])

Total Connected Subagent Orchestration Duration Shows total time spent delegating work to connected subagents, in milliseconds. Total_Connected_Subagent_Orchestration_Duration_clc
SUM([Connected_Subagent_Orchestration_Duration_ms_clc])

Total Connected Subagent Execution Duration Shows total connected-subagent execution time, in milliseconds. Total_Connected_Subagent_Execution_Duration_clc
SUM([Connected_Subagent_Execution_Duration_ms_clc])
