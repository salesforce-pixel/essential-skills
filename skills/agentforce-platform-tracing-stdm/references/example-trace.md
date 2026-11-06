# Example: one website-chat session of an Agent Script service agent, fully traced

A real session, with company and product names replaced by placeholders (`Acme`, `Acme_Website_FAQ`) and ids shortened. Agent `My_Service_Agent` v1 (one FAQ topic, one prompt-template action grounded by an Apex retriever), channel `SCRT2 - EmbeddedMessaging`, MessagingSession `0Mw…`. Produced with recipes R2 and R3 from SKILL.md.

## Transcript (R2)

| Sent (UTC) | Topic | Dir | Content (start) |
|---|---|---|---|
| 10:20:00.528 | NOT_SET | Output | Hi, I'm your Acme assistant. How can I help you? |
| 10:20:25.755 | GeneralFAQ_16j… | Input | I'm looking into full factory solutions for my production plant. |
| 10:20:34.528 | GeneralFAQ_16j… | Output | Acme offers complete solutions for food processing… |
| 10:21:40.032 | GeneralFAQ_16j… | Input | What is the price range for a slicing machine' |
| 10:21:45.433 | GeneralFAQ_16j… | Output | The Acme website does not list pricing… |
| 10:22:10.331 | GeneralFAQ_16j… | Input | can you help me connect with a specialist? |
| 10:22:15.146 | GeneralFAQ_16j… | Output | You can connect with an Acme specialist by using the "Contact a specialist" option… |

The session has 4 `TURN` interactions: 1 welcome turn and 3 user turns. There's no `SESSION_END` yet: the visitor never closed the chat.

## Steps of turn 1 (R3), 10:20:25.755

| Step start | Type | Name | Subtype | ms | in/out chars |
|---|---|---|---|---|---|
| 25.750 | VARIABLE_UPDATE_STEP | `__state_update_action__` | | 0 | 7/7 |
| 25.768 | CLASSIFIER_STEP | `pre_orchestration.guardrail` | | 91 | 1862/65 |
| 25.870 | VARIABLE_UPDATE_STEP | `__state_update_action__` | | 0 | 7/7 |
| 25.877 | TOPIC_STEP | `agent_router` | | 75 | 730/98 |
| 25.973 | LLM_STEP | `GeneralFAQ` (plans + picks the action) | | 663 | 10537/565 |
| 26.643 | ACTION_STEP | `Acme_Website_FAQ` | generatePromptResponse | **6856** | 204/1943 |
| 34.154 | LLM_STEP | `GeneralFAQ` (writes the reply) | | 1684 | 12791/1965 |
| 35.844 | TRUST_GUARDRAILS_STEP | `InstructionAdherence` | | 1413 | 112/339 |
| 35.847 | LLM_STEP | `Atlas__GroundednessValidationPrompt` | | 1108 | 112/402 |

The visitor waited 8.8 s (25.755 → reply at 34.528). 78% of that was the action: the Apex retriever's `hybrid_search` plus the prompt-template LLM call. The two post-checks finish after the reply has been sent.

Turns 2 and 3 have the same shape, with actions taking 4,231 ms and 3,532 ms.

## Payload samples (turn 2)

TOPIC_STEP `agent_router`:
- input: `{"af.request_id":"854092e4…","classifier.input":"What is the price range for a slicing machine'","af.topic_names_or_ids":"agent_router,GeneralFAQ","af.router_classifier.choices":"[{\"target\":\"GeneralFAQ\",\"description\":\"Questions about Acme, its products, solutions…`
- output: `{"mgr.output.payload_type":"classifier_event","af.router_classifier.selected_target":"GeneralFAQ"}`

ACTION_STEP `Acme_Website_FAQ`. The LLM rewrote the question into a standalone English question:
- input: `{"actionName":"Acme_Website_FAQ","actionInput":{"outputLanguage":"en_US","Input:Question":"What is the price range for a slicing machine for food processing?","isPreviewOnly":false}}`
- output: `{"actionName":"Acme_Website_FAQ","actionResponse":{"__action_execution_status__":"success","generationId":"8ffdcb41-…","promptResponse":"Pricing or a price range for slicing machines is not listed on the Acme website…`
- attributes: `{"internalTraceId":"24cea9ec…","internalSpanId":"54de54d4…","progress_indicators":[{"message":"Looking for information"}]}`

TRUST_GUARDRAILS_STEP `InstructionAdherence`:
- output: `{"gen_ai.response.id":"chatcmpl-…","mgr.sensitive.step.result":"InstructionAdherence: value=HIGH, explanation=This response adheres to the assigned instructions.; TaskResolution: value=FULLY_RESOLVED, explanation=User task was correctly identified and fully resolved","mgr.output.payload_type":"graph_complete"}`

## Latency baseline for this agent (R6, last 30 days, 48 action calls)

| Step | n | avg ms | p95 ms | max ms |
|---|---|---|---|---|
| ACTION_STEP `Acme_Website_FAQ` | 48 | 5,380 | 9,515 | 13,470 |
| TRUST_GUARDRAILS_STEP `InstructionAdherence` | 57 | 1,660 | 3,028 | 4,126 |
| LLM_STEP `GeneralFAQ` | 101 | 1,114 | 2,633 | 3,281 |
| LLM_STEP `off_topic` | 4 | 993 | 1,430 | 1,501 |
| LLM_STEP `Atlas__GroundednessValidationPrompt` | 57 | 918 | 1,394 | 1,964 |
| CLASSIFIER_STEP `pre_orchestration.guardrail` | 58 | 122 | 153 | 614 |
| TOPIC_STEP `agent_router` | 57 | 118 | 160 | 811 |

Session ends: 14 `CLOSED_USER_REQUEST`, 3 `EXPIRED`. All 48 action calls returned `success`, and no step had an error.
