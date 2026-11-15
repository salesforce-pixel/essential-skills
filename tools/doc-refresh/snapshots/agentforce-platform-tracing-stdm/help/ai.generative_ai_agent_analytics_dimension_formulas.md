# Agentforce Observability Dimension Formulas | Salesforce Help

Source: https://help.salesforce.com/s/articleView?id=ai.generative_ai_agent_analytics_dimension_formulas.htm&type=5

QUICKSTART YOUR EINSTEIN GENERATIVE AI SOLUTION
Agentforce Observability Dimension Formulas

These formulas show how Agentforce Observability calculates dimensions in the Agentforce Analytics Foundations semantic data model. Use them to understand the fields available for reporting.

REQUIRED EDITIONS
REQUIRED EDITIONS
Agentforce Observability is available in Salesforce Enterprise, Performance, and Unlimited Editions with Salesforce Foundations or Agentforce 1 Edition.
Session Outcome and Status Fields
Dimension Formulas
LABEL CX DESCRIPTION FIELD NAME FORMULA
Abandon Status Indicates whether an LLM classified the session as abandoned, meaning the customer's request went unresolved. True if the session wasn't transferred, the latest Abandonment Score is true, and the latest Deflection Score is 3 or lower or unavailable. Abandonment_Status_clc
IF IFNULL({ FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX([Escalation_Status_clc]) }, FALSE) = FALSE AND { FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX(IF [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Source_Tag_Reference] = 'std_Abandonment_Score' AND [Is_Latest_Session_Scorer_clc] = TRUE THEN [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag2_Value] END) } = 'TRUE' AND IFNULL(INT({ FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX(IF [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Source_Tag_Reference] = 'std_Deflection_Score' AND [Is_Latest_Session_Scorer_clc] = TRUE THEN [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag2_Value] END) }), 0) <= 3 THEN TRUE ELSE FALSE END

Deflection Status Indicates whether an LLM classified the session as deflected, meaning the customer's main request was resolved. True if the session wasn't transferred and the latest Deflection Score is 4 (mostly resolved, with minor gaps) or 5 (fully resolved). Deflection_Status_clc
{ FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : IFNULL(MAX([Escalation_Status_clc]), FALSE) = FALSE AND INT(MAX(IF [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Source_Tag_Reference] = 'std_Deflection_Score' AND [Is_Latest_Session_Scorer_clc] = TRUE THEN [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag2_Value] END)) IN (4, 5) }

Engagement Status Indicates whether the session includes at least one engaged interaction. Engagement_Status_clc
{ FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX(
IF [Is_Interaction_Engaged_clc]
THEN TRUE
ELSE FALSE
END) }

Escalation Status Indicates whether a session was transferred to another agent at session end or after 24 hours without activity. Escalation_Status_clc
{ FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX(
IF
(
[AI_Agent_Interaction_Step].[Ai_Agent_Interaction_Step_Type]='SESSION_END'
OR
DATEDIFF('HOUR', { FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX([AI_Agent_Interaction].[End_Timestamp]) },NOW()) >= 24
)
AND
[AI_Agent_Interaction_Step].[Name]='CLOSED_TRANSFERRED'
THEN TRUE
ELSE FALSE
END )}

Is Session Ended Indicates whether a session has a SESSION_END event or has been inactive for at least 24 hours. Is_Session_Ended_clc
{ FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX(
IF [AI_Agent_Interaction].[Ai_Agent_Interaction_Type]='SESSION_END'
OR DATEDIFF('HOUR', { FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX(
[AI_Agent_Interaction].[End_Timestamp]) },
NOW()
) >= 24
THEN TRUE
ELSE FALSE
END
)
}

Session Ambiguous Indicates a session that is not escalated, has a low deflection score, and is not marked as abandoned. Is_Session_Ambiguous_clc
IF IFNULL({ FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX([Escalation_Status_clc]) }, FALSE) = FALSE AND IFNULL(INT({ FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX(IF [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Source_Tag_Reference] = 'std_Deflection_Score' AND [Is_Latest_Session_Scorer_clc] = TRUE THEN [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag2_Value] END) }), 0) <= 3 AND { FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX(IF [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Source_Tag_Reference] = 'std_Abandonment_Score' AND [Is_Latest_Session_Scorer_clc] = TRUE AND ([AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag2_Value] = 'FALSE' OR [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag2_Value] = 'Unsure') THEN TRUE ELSE FALSE END) } = TRUE THEN TRUE ELSE FALSE END

Session Outcome Classifies the session outcome as Escalated, Unengaged, Deflected, Abandoned, Not Resolved, Not Abandoned, or Not set. Session_Outcome_Base_clc
IF IFNULL({ FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX([Escalation_Status_clc]) }, FALSE) THEN 'Escalated' ELSEIF [Engagement_Status_clc] = FALSE THEN 'Unengaged' ELSEIF IFNULL({ FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX([Deflection_Status_clc]) }, FALSE) THEN 'Deflected' ELSEIF IFNULL([Abandonment_Status_clc], FALSE) THEN 'Abandoned' ELSEIF IFNULL([Is_Session_Ambiguous_clc], FALSE) THEN 'Not Resolved, Not Abandoned' ELSE 'Not set' END

Session Duration For an ended session, shows the seconds from the first turn start to the last turn end. Session_Duration_clc
{ FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX(
IF [Is_Session_Ended_clc]
THEN DATEDIFF( 'SECOND',
{ FIXED [AI_Agent_Session].[AI_Agent_Session_Id] :
MIN( IF [AI_Agent_Interaction].[Ai_Agent_Interaction_Type]='TURN'
THEN [AI_Agent_Interaction].[Start_Timestamp]
END
) },
{ FIXED [AI_Agent_Session].[AI_Agent_Session_Id] :
MAX(IF [AI_Agent_Interaction].[Ai_Agent_Interaction_Type]='TURN'
THEN [AI_Agent_Interaction].[End_Timestamp]
END
) }
)
END
) }

Is Sub Session Indicates whether the session continues from an earlier session. Is_Sub_Session_clc
IF NOT (ISNULL([AI_Agent_Session].[Previous_Session_Id]) OR [AI_Agent_Session].[Previous_Session_Id] = 'NOT_SET')
THEN TRUE
ELSE FALSE
END

Is Interaction Engaged Indicates whether the interaction includes one or more user messages. Is_Interaction_Engaged_clc
[Total_User_Messages_Per_Interaction_clc] > 0

Is Interaction With Errors Indicates whether any step in the interaction contains an error. Is_Interaction_With_Errors_clc
{ FIXED [AI_Agent_Interaction].[AI_Agent_Interaction_Id] : MAX([Is_Step_With_Error_clc]) }

Is Step With Error Indicates whether an interaction step contains a meaningful error message, excluding placeholder and no-error values. Is_Step_With_Error_clc
IF NOT ISNULL([AI_Agent_Interaction_Step].[Error_Message]) AND LEN(TRIM([AI_Agent_Interaction_Step].[Error_Message])) > 0 AND [AI_Agent_Interaction_Step].[Error_Message] != 'NOT_SET' AND [AI_Agent_Interaction_Step].[Error_Message] != 'None' AND NOT (CONTAINS([AI_Agent_Interaction_Step].[Error_Message], '"message":"None"') AND CONTAINS([AI_Agent_Interaction_Step].[Error_Message], '"source":"mgr.step.error"')) THEN TRUE ELSE FALSE END

Is User Indicates whether the participant is a user or messaging end user. Is_User_clc
IF
[AI_Agent_Session_Participant].[AI_Agent_Session_Participant_Role]='USER'
AND
[AI_Agent_Session_Participant].[Participant_Object] IN ('MessagingEndUser','User')
THEN TRUE
ELSE FALSE
END

Is User Turn Indicates whether the interaction is a turn from a user. Is_User_Turn_clc
IF [Is_User_clc] AND [AI_Agent_Interaction].[Ai_Agent_Interaction_Type] = 'TURN' THEN TRUE ELSE FALSE END
Scorer, Feedback, and Quality Fields
Dimension Formulas
LABEL CX DESCRIPTION FIELD NAME FORMULA
Agent Adherence Status Shows the Instruction Adherence evaluation category for generated interaction steps. Agent_Adherence_Status_clc
{ FIXED [AI_Agent_Interaction_Step].[AI_Agent_Interaction_Step_Id] : MAX(IF NOT ISNULL([AI_Agent_Interaction_Step].[Generation]) AND [AI_Agent_Interaction_Step].[Generation] != 'NOT_SET' AND [Ai_Content_Quality_Category].[Detector_Type] = 'InstructionAdherence' THEN [Ai_Content_Quality_Category].[Category] END) }

Task Resolution Status Shows the latest Task Resolution evaluation category for generated steps in the session. Task_Resolution_Status_clc
{ FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX(
IF NOT ISNULL([AI_Agent_Interaction_Step].[Generation])
AND [AI_Agent_Interaction_Step].[Generation] != 'NOT_SET'
AND [Ai_Content_Quality_Category].[Detector_Type] = 'TaskResolution'
AND [AI_Agent_Interaction_Step].[Start_Timestamp] =
{ FIXED [AI_Agent_Session].[AI_Agent_Session_Id] : MAX(
IF NOT ISNULL([AI_Agent_Interaction_Step].[Generation])
AND [AI_Agent_Interaction_Step].[Generation] != 'NOT_SET'
AND [Ai_Content_Quality_Category].[Detector_Type] = 'TaskResolution'
THEN [AI_Agent_Interaction_Step].[Start_Timestamp]
END
) }
THEN [Ai_Content_Quality_Category].[Category]
END
) }

Quality Score Shows the moment quality score as a whole number. Quality_Score_clc
INT([AI_Agent_Moment_Quality_Score_lv].[AI_Agent_Tag1_Value])

User Feedback Status Shows Positive or Negative based on the most recent feedback for the interaction, or N/A when no feedback exists. User_Feedback_Status_clc
IFNULL({ FIXED [AI_Agent_Interaction].[AI_Agent_Interaction_Id] : MAX(IF [Ai_Feedback].[Timestamp] = { FIXED [AI_Agent_Interaction].[AI_Agent_Interaction_Id] : MAX([Ai_Feedback].[Timestamp]) } THEN CASE [Ai_Feedback].[Feedback] WHEN 'GOOD' THEN 'Positive' WHEN 'BAD' THEN 'Negative' END END) }, 'N/A')

Is Intent Scorer Standard Indicates whether an intent scorer is a standard scorer. Is_Intent_Scorer_Standard_clc
IF
LEFT([AI_Agent_Tag_Definition].[Source_Tag_Reference], 4) = 'std_'
OR
[AI_Agent_Tag_Definition].[Developer_Name] = 'Quality_Score'
THEN TRUE
ELSE FALSE
END

Is Interaction Scorer Standard Indicates whether an interaction scorer is a standard scorer. Is_Interaction_Scorer_Standard_clc
IF
LEFT([AI_Agent_Interaction_Tag_Association_lv].[AI_Agent_Tag_Definition3_Source_Tag_Reference], 4) = 'std_'
THEN TRUE
ELSE FALSE
END

Is Session Scorer Standard Indicates whether a session scorer is a standard scorer. Is_Session_Scorer_Standard_clc
IF LEFT([AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Source_Tag_Reference], 4) = 'std_'
OR [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Source_Tag_Reference] = 'Quality_Score'
OR [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Source_Tag_Reference] = 'AIE_Request_Category'
THEN TRUE
ELSE FALSE
END

Is Latest Intent Scorer Indicates whether this is the most recently created scorer result for the moment and scorer. Is_Latest_Intent_Scorer_clc
[AI_Agent_Tag_Association].[Created_Date] =
{ FIXED [AI_Agent_Tag_Association].[AI_Agent_Moment_Id],
[AI_Agent_Tag_Definition].[Tag_Identifier] :
MAX([AI_Agent_Tag_Association].[Created_Date]) }

Is Latest Interaction Scorer Indicates whether this is the most recently created scorer result for the interaction and scorer. Is_Latest_Interaction_Scorer_clc
[AI_Agent_Interaction_Tag_Association_lv].[AI_Agent_Tag_Association4_Created_Date] =
{ FIXED [AI_Agent_Interaction_Tag_Association_lv].[AI_Agent_Tag_Association4_AI_Agent_Interaction],
[AI_Agent_Interaction_Tag_Association_lv].[AI_Agent_Tag_Definition3_Tag_Identifier] :
MAX([AI_Agent_Interaction_Tag_Association_lv].[AI_Agent_Tag_Association4_Created_Date]) }

Is Latest Session Scorer Indicates whether this is the most recently created scorer result for the session and scorer. Is_Latest_Session_Scorer_clc
[AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Association3_Created_Date] =
{ FIXED [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Association3_AI_Agent_Session_Id],
[AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Tag_Identifier] :
MAX([AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Association3_Created_Date]) }

Custom Scorer Semantic Type Classifies a custom scorer as a Measurement or Dimension based on its defined semantic type or data type. Custom_Scorer_Semantic_Type_clc
IF NOT ISNULL([AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Semantic_Type])
AND LEN(TRIM([AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Semantic_Type])) > 0
THEN [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Semantic_Type]
ELSEIF [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Data_Type] = 'Integer'
OR [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Data_Type] = 'Number'
THEN 'Measurement'
ELSE 'Dimension'
END

Custom Scorer Measures Shows the identifier for an active nonstandard scorer that can be used as a measure. Custom_Scorer_Measures_clc
IF [Custom_Scorer_Semantic_Type_clc] = 'Measurement'
AND [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition_Association3_Is_Active] = TRUE
AND [Is_Session_Scorer_Standard_clc] = FALSE
AND (
[AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Source_Type] = 'Predefined'
OR
[AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Source_Type] = 'OpenEnded'
)
THEN [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Tag_Identifier]
ELSE '--'
END

Custom Scorer Dimensions Shows the identifier for an active nonstandard scorer that can be used as a dimension. Custom_Scorer_Dimensions_clc
IF [Custom_Scorer_Semantic_Type_clc] = 'Dimension'
AND [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition_Association3_Is_Active] = TRUE
AND [Is_Session_Scorer_Standard_clc] = FALSE
AND (
[AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Source_Type] = 'Predefined'
OR
(
[AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Source_Type] = 'OpenEnded'
AND NOT ISNULL([AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag2_Value])
AND [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag2_Value] != 'NOT_SET'
)
)
THEN [AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag_Definition2_Tag_Identifier]
END

Custom Scorer Dimension Values Shows a custom scorer dimension together with its recorded value. Custom_Scorer_Dimension_Values_clc
IF NOT ISNULL([Custom_Scorer_Dimensions_clc]) THEN
[Custom_Scorer_Dimensions_clc]+" : "+[AI_Agent_Session_Tag_Association_lv].[AI_Agent_Tag2_Value]
ELSE
'--'
END
Message and Response Timing Fields
Dimension Formulas
LABEL CX DESCRIPTION FIELD NAME FORMULA
Agent Interaction Duration Shows the interaction duration in seconds, from start to end. Agent_Interaction_Latency_clc
DATEDIFF('SECOND', [AI_Agent_Interaction].[Start_Timestamp], [AI_Agent_Interaction].[End_Timestamp])

Moment Duration Shows the moment duration in seconds, from start to end. Moment_Duration_clc
DATEDIFF('SECOND', [AI_Agent_Moment].[Start_Timestamp], [AI_Agent_Moment].[End_Timestamp])

Agent Response Start Timestamp Shows when the agent starts responding in an interaction. Agent_Response_Timestamp_clc
{ FIXED [AI_Agent_Interaction].[AI_Agent_Interaction_Id] :
MAX(
IF NOT [Is_User_clc] THEN
IF [AI_Agent_Interaction_Message].[Message_Start_Timestamp]
<= [AI_Agent_Interaction_Message].[Message_Sent_Timestamp]
THEN [AI_Agent_Interaction_Message].[Message_Start_Timestamp]
ELSE [AI_Agent_Interaction_Message].[Message_Sent_Timestamp]
END
END
) }

Agent Response End Timestamp Shows when the agent finishes responding in an interaction. Agent_Response_End_Timestamp_clc
{ FIXED [AI_Agent_Interaction].[AI_Agent_Interaction_Id] :
MAX(
IF NOT [Is_User_clc] THEN
IF [AI_Agent_Interaction_Message].[Message_End_Timestamp]
>= [AI_Agent_Interaction_Message].[Message_Sent_Timestamp]
THEN [AI_Agent_Interaction_Message].[Message_End_Timestamp]
ELSE [AI_Agent_Interaction_Message].[Message_Sent_Timestamp]
END
END
) }

User Message End Timestamp Shows when the user message ends in an interaction. User_Turn_Timestamp_clc
{ FIXED [AI_Agent_Interaction].[AI_Agent_Interaction_Id] :
MAX(
IF [Is_User_clc] THEN
IF [AI_Agent_Interaction_Message].[Message_End_Timestamp]
>= [AI_Agent_Interaction_Message].[Message_Sent_Timestamp]
THEN [AI_Agent_Interaction_Message].[Message_End_Timestamp]
ELSE [AI_Agent_Interaction_Message].[Message_Sent_Timestamp]
END
END
) }

Agent Response Time in Seconds Shows agent response latency in seconds. Response_Time_Seconds_clc
[Time_To_First_Agent_Token_clc] / 1000

Is Agent Response Within 60s Indicates whether the agent begins responding within 60 seconds. Agent_Response_Within_60s_clc
IF [Response_Time_Seconds_clc] >= 0 AND [Response_Time_Seconds_clc] <= 60 THEN TRUE ELSE FALSE END

Agent Response Latency For eligible turns after July 10, 2026, shows milliseconds from the user message end until the agent starts responding. Time_To_First_Agent_Token_clc
IF [AI_Agent_Interaction].[Start_Timestamp] > #2026-07-10 00:00:00# AND [AI_Agent_Interaction].[Ai_Agent_Interaction_Type] = 'TURN' AND [Does_Interaction_Include_Only_Populated_Messages_clc] AND [Total_User_Messages_Per_Interaction_clc] = [Total_Agent_Messages_Per_Interaction_clc] THEN DATEDIFF('MILLISECONDS', [User_Turn_Timestamp_clc], [Agent_Response_Timestamp_clc]) END

Agent Response Completion Latency For eligible turns after July 10, 2026, shows milliseconds from the user message end until the agent finishes responding. Time_To_Last_Agent_Token_clc
IF [AI_Agent_Interaction].[Start_Timestamp] > #2026-07-10 00:00:00# AND [AI_Agent_Interaction].[Ai_Agent_Interaction_Type] = 'TURN' AND [Does_Interaction_Include_Only_Populated_Messages_clc] AND [Total_User_Messages_Per_Interaction_clc] = [Total_Agent_Messages_Per_Interaction_clc] THEN DATEDIFF('MILLISECONDS', [User_Turn_Timestamp_clc], [Agent_Response_End_Timestamp_clc]) END

Does Interaction Include Only Populated Messages Indicates whether every message in the interaction has content. Does_Interaction_Include_Only_Populated_Messages_clc
{ FIXED [AI_Agent_Interaction].[AI_Agent_Interaction_Id] : MIN(IF NOT ISNULL([AI_Agent_Interaction_Message].[Content]) AND [AI_Agent_Interaction_Message].[Content] <> '' THEN TRUE ELSE FALSE END) }

Total User Messages per Interaction Counts user messages in the interaction. Total_User_Messages_Per_Interaction_clc
{ FIXED [AI_Agent_Interaction].[AI_Agent_Interaction_Id] :
COUNTD(
IF [Is_User_clc]
THEN [AI_Agent_Interaction_Message].[AI_Agent_Interaction_Message_Id]
END
)
}

Total Agent Messages per Interaction Counts nonuser messages in the interaction. Total_Agent_Messages_Per_Interaction_clc
{ FIXED [AI_Agent_Interaction].[AI_Agent_Interaction_Id] :
COUNTD(
IF NOT [Is_User_clc]
THEN [AI_Agent_Interaction_Message].[AI_Agent_Interaction_Message_Id]
END
)
}
Agent, Action, and Connected Subagent Fields
Dimension Formulas
LABEL CX DESCRIPTION FIELD NAME FORMULA
Agent Label Shows the bot label when available; otherwise shows the agent API name. Agent_Label_clc
IF
NOT ISNULL({ FIXED [AI_Agent_Session_Participant].[AI_Agent_Session_Participant_Id] : MAX([Bot].[Label]) })
THEN
{ FIXED [AI_Agent_Session_Participant].[AI_Agent_Session_Participant_Id] : MAX([Bot].[Label]) }
ELSE
[AI_Agent_Session_Participant].[AI_Agent_Api_Name]
END

Subagent Label Shows the related subagent label when available; otherwise shows the topic API name. Subagent_Label_clc
IF
NOT ISNULL({ FIXED [AI_Agent_Interaction].[AI_Agent_Interaction_Id] : MAX([AI_Agent_Topic].[Master_Label]) })
THEN
{ FIXED [AI_Agent_Interaction].[AI_Agent_Interaction_Id] : MAX([AI_Agent_Topic].[Master_Label]) }
ELSE
[AI_Agent_Interaction].[Topic_API_Name]
END

Action Label For action steps, shows the action label when available; otherwise shows the step name. Tool_Label_clc
IF [AI_Agent_Interaction_Step].[Ai_Agent_Interaction_Step_Type] = 'ACTION_STEP'
THEN
IF NOT ISNULL({ FIXED [AI_Agent_Interaction_Step].[AI_Agent_Interaction_Step_Id] : MAX([AI_Agent_Action].[AI_Agent_Action_Id]) })
THEN { FIXED [AI_Agent_Interaction_Step].[AI_Agent_Interaction_Step_Id] : MAX([AI_Agent_Action].[Label3]) }
ELSE [AI_Agent_Interaction_Step].[Name]
END
END

Connected Subagent Name Shows the connected subagent name from the handoff step. Connected_Subagent_Name_clc
IF [AI_Agent_Interaction_Step].[Ai_Agent_Interaction_Step_Type] = 'RELATED_AGENT_STEP' THEN REGEXP_EXTRACT([AI_Agent_Interaction_Step].[Attribute], 'related_agent_name":"([^"]*)') END

Connected Subagent Api Name Shows the connected subagent API name from the handoff step. Connected_Subagent_Api_Name_clc
IF [AI_Agent_Interaction_Step].[Ai_Agent_Interaction_Step_Type] = 'RELATED_AGENT_STEP' THEN REGEXP_EXTRACT([AI_Agent_Interaction_Step].[Attribute], 'related_agent_api_name":"([^"]*)') END

Connected Subagent Session Id Shows the connected subagent session ID from the handoff step. Connected_Subagent_Session_Id_clc
IF [AI_Agent_Interaction_Step].[Ai_Agent_Interaction_Step_Type] = 'RELATED_AGENT_STEP' THEN REGEXP_EXTRACT([AI_Agent_Interaction_Step].[Attribute], 'related_agent_session_id":"([^"]*)') END

Connected Subagent Interaction Id Shows the connected subagent interaction ID from the handoff step. Connected_Subagent_Interaction_Id_clc
IF [AI_Agent_Interaction_Step].[Ai_Agent_Interaction_Step_Type] = 'RELATED_AGENT_STEP' THEN REGEXP_EXTRACT([AI_Agent_Interaction_Step].[Attribute], 'related_agent_interaction_id":"([^"]*)') END

Connected Subagent Orchestration Duration Shows handoff and orchestration time to the connected subagent, in milliseconds. Connected_Subagent_Orchestration_Duration_ms_clc
IF [AI_Agent_Interaction_Step].[Ai_Agent_Interaction_Step_Type] = 'RELATED_AGENT_STEP' THEN INT(REGEXP_EXTRACT([AI_Agent_Interaction_Step].[Attribute], '"orchestration_latency_ms":(\d+)')) END

Connected Subagent Execution Duration Shows connected-subagent execution time, in milliseconds. Connected_Subagent_Execution_Duration_ms_clc
IF [AI_Agent_Interaction_Step].[Ai_Agent_Interaction_Step_Type] = 'RELATED_AGENT_STEP' THEN INT(REGEXP_EXTRACT([AI_Agent_Interaction_Step].[Attribute], '"sub_agent_execution_latency_ms":(\d+)')) END
