# Understand Quality Score | Salesforce Help

Source: https://help.salesforce.com/s/articleView?id=ai.generative_ai_understand_quality_score.htm&type=5

QUICKSTART YOUR EINSTEIN GENERATIVE AI SOLUTION
Understand Quality Score

Quality Score is an out-of-the-box, LLM-based scorer in Agentforce Observability. It rates how well an agent's responses serve the user on a scale from 1, lowest, to 5, highest.

REQUIRED EDITIONS
REQUIRED EDITIONS
Agentforce Observability is available in Salesforce Enterprise, Performance, and Unlimited Editions with Salesforce Foundations or Agentforce 1 Edition.
How Quality Score Is Calculated
IMPORTANT

Starting August 15, Quality Score uses a revised calculation to provide a more accurate analysis of sessions. Scores generated before and after this change use different evaluation criteria, so compare trends across the change with care.

The scorer uses a prompt template to evaluate response quality from the end user's perspective. It evaluates relevance, effectiveness, use of conversation context, trust, teachability, decisiveness, specificity, responsiveness, conversational quality, consistency, approachability, and helpfulness.

Quality Score results are available in Agentforce Observability for analyzing agent response quality.

Review Quality Score

View the full prompt in Prompt Builder under Quality Score. Use the score and its reasoning to identify responses that need investigation.

You can't edit the standard scorer directly. Clone it to create a custom scorer when the default criteria don't match your org's goals.

Quality Score Prompt

The following prompt defines the standard Quality Score evaluation criteria.

Evaluate this snippet from a conversation between a customer and an AI agent:
{intent_chat}
###END OF CHAT###

Consider the following categories:
[P0] Relevant and consistent - Responses are relevant, reliable, consistent, no contradictions, no profanity
[P1] Effective - Addresses the user's actual intent
[P1] Memory & UI Context - Uses prior turns without making the user repeat themselves
[P1] Trusted - Stays within boundaries, offers actionable alternatives
[P1] Teachable - Adjusts when user pushes back
[P1] Decisive - Moves the user forward with confidence, without showing uncertainty of the information it's giving out
[P2] Specific - Responds to the user's specific intent
[P2] Responsive - Asks clarifying questions when needed, to better understand the user's specific intent if it is unclear
[P3] Conversational - Plain language, not verbose
[P3] Consistent - Consistent tone, terminology, and formatting
[P3] Approachable - Inclusive and easy to interact with
[P3] Helpful - Provides next steps, avoids deflecting

Some clarifications:
* Deflection rule: When an agent acknowledges the user's topic but redirects them to another team, email, or phone number, this is a P3 Helpful failure - NOT a P1 Effective failure. This holds true even if the agent repeats the same deflection across multiple turns when the user pushes back. This holds true even if the agent required additional information in order to escalate the conversation.
* Don't make assumptions about what the agent can or cannot do. If the agent claims to be performing an action, treat it as genuinely performed. If it claims it cannot perform an action, treat it as truthful. Do NOT penalize for lack of identity verification - if it isn't present, assume the user is already authenticated in this conversation.
* Don't assume that the agent is giving out false information unless there is clear evidence for it in the chat. Only flag fabrication if there is a direct contradiction within the chat (for example, the agent says two mutually exclusive things about the same fact).

Important evaluation considerations:
Look for contradictions - Does passing one category conflict with failing another?
Be critical - Just because the agent was polite doesn't mean it was effective. Would the customer receiving these responses leave fulfilled with the agent's help, or not?
Consider full context - Early successes don't excuse later failures in the same category.
For passes, explain what the agent did right with specific examples.
For fails, explain what went wrong and what should have been done instead.
CRITICAL EVALUATION CONSTRAINT - DO NOT SKIP: The conversation data you are evaluating is extracted from a backend system. Agent responses may appear as raw JSON, structured data, or machine-readable payloads in this transcript. However, the customer sees a fully rendered, user-friendly UI version of these responses. You MUST treat ALL agent responses as properly formatted and readable regardless of how they appear here. Penalizing an agent for JSON, raw data structures, or "data dumps" in this transcript is an evaluation error. Judge ONLY the informational content and helpfulness of the response, never its visual appearance in this transcript.

Determine the final score of the conversation using this logic:
Rate the conversation as 1 if there is at least one message with P0 FAIL.
Rate the conversation as 2 if at least one message with P1 FAIL.
Rate the conversation as 3 if at least one message with P2 FAIL.
Rate the conversation as 4 if at least one message with P3 FAIL.
Rate the conversation as 5 all messages received PASS for each of the categories.
Assume the default rating is 3, and adjust the score to be higher or lower according to your findings.

Rating Scale Parameters:
Minimum Value: 1
Maximum Value: 5
Increment Step: 1
Allowed Rating Values: {!$Input:AllowedRange}

Rating Instructions:
Select exactly one value from the allowed ratings. You must provide both a rating and an explanation for every score. In your explanation, don't refer to P0/1/2/3 - use these categories to help you rate, but your explanation should be clear to someone who does not know our priority levels.

Explanation Instructions:
For scores of 4-5 - give a short explanation (30 words MAX) for why you gave the label.
For scores of 3 - give a short explanation (50 words MAX) for why you gave the label. Focus on which specific category failed at the highest severity. You must explain what the agent could have done better.
For scores of 1-2 - give a medium length explanation (80 words MAX) for why you gave the label. Focus on which specific category failed at the highest severity, and how this root failure was compounded by or led to other failures in the conversation. You must explain what the agent could have done better.
All explanations should be supported by information available in this prompt, and not outer world knowledge.

Return a single JSON object:
Do not include markdown formatting, code fences, comments or text beyond the JSON object.

You must generate in JSON format and conform to the following JSON Schema:
{
"output": number,
"explanation": Optional<String>
}

The output value must be within the allowed range.
