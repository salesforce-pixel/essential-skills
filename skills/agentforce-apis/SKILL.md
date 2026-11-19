---
name: agentforce-apis
description: >-
  Call and connect Agentforce agents from outside Salesforce: the headless Agent API
  (REST on api.salesforce.com — External Client App + client-credentials token, agent ID
  lookup, start session, sync and SSE streaming messages, agent variables, citations,
  feedback, end session, errors), Enhanced Chat v2 for service agents (inline vs floating
  display mode, targetElement, disableInlineAutoLaunch, setSessionContext context events),
  custom connections (AiSurface + AiResponseFormat metadata, plannerSurfaces in
  GenAiPlannerBundle, surfaceConfig, parsing SURFACE_ACTION__ results into native UI), and
  the Agentforce Session Trace OTel API (beta) that exports one session as OTLP JSON.
  TRIGGER when the user calls /einstein/ai-agent/v1, builds a headless or custom chat
  client, Slack/Teams/mobile/IVR bridge or backend integration for an agent; asks about
  bypassUser, externalSessionKey, sequenceId, streamingCapabilities, chatbot_api /
  sfap_api scopes, TextChunk / Inform / EndOfTurn / ValidationFailureChunk events, HTTP
  423 or EngineConfigLookupException; embeds Enhanced Chat v2 inline; writes AiSurface or
  AiResponseFormat files; or exports a session trace to Datadog, Splunk, New Relic or an
  OTLP collector. DO NOT TRIGGER for embedding the Employee Agent UI in a web app or
  driving the Lightning side panel (use agentforce-conversation-client), Custom Lightning
  Type renderers (use clt-agentforce-actions), SQL over the ssot__AiAgent* DMOs (use
  agentforce-platform-tracing-stdm), writing .agent files (use agentscript), or
  retrieving/deploying agent metadata in general (use afagent-metadata-helper).
metadata:
  version: "1.0"
---

<!--
Changelog
1.0 — New skill (2026-11-19), curated from the Agentforce Developer Guide pages on the
      Agent API, Enhanced Chat v2, custom connections and the Session Trace OTel API
      (doc sources tracked by tools/doc-refresh). Adds scripts/agent_api_chat.py.
-->

# Agentforce APIs — Agent API, Enhanced Chat v2, custom connections, OTel export

Four ways to work with an agent from outside the Salesforce UI. Pick one before you
write code; they share auth (an External Client App) but little else.

| Goal | Use | Read |
|---|---|---|
| Talk to an agent from your own backend, bot bridge, test harness or app (no Salesforce UI) | **Agent API** (REST, `api.salesforce.com/einstein/ai-agent/v1`) | `references/agent-api.md` |
| Put a **service agent** on a website with Salesforce's chat widget, inline in the page or floating | **Enhanced Chat v2** (Embedded Service deployment snippet) | `references/enhanced-chat-v2.md` |
| Your own chat client that renders agent replies as **native components** (carousels, pickers, forms) | **Custom connection** (`AiSurface` + `AiResponseFormat`) on top of the Agent API | `references/custom-connections.md` |
| Pull one session's full trace (turns, LLM calls, actions, scores, feedback) into an observability tool | **Session Trace OTel API (beta)** | `references/otel-api.md` |

Not here: the **Employee Agent** UI in an external app or the Lightning side panel →
`agentforce-conversation-client`. Custom cards in Enhanced Chat v2 → `clt-agentforce-actions`.
Querying many sessions with SQL → `agentforce-platform-tracing-stdm`.

## Agent API in five calls

```text
1. POST https://{MY_DOMAIN}/services/oauth2/token           grant_type=client_credentials → access_token (JWT)
2. agent ID                                                  BotDefinition.Id (0Xx…), see below
3. POST https://api.salesforce.com/einstein/ai-agent/v1/agents/{AGENT_ID}/sessions        → sessionId + greeting
4. POST …/v1/sessions/{SESSION_ID}/messages                 sync, one JSON reply
   POST …/v1/sessions/{SESSION_ID}/messages/stream          SSE: ProgressIndicator, TextChunk, Inform, EndOfTurn
5. DELETE …/v1/sessions/{SESSION_ID}   header x-session-end-reason: UserRequest
```

Start-session body (minimum that works with client credentials):

```json
{
  "externalSessionKey": "<random UUID — your trace key>",
  "instanceConfig": { "endpoint": "https://<MyDomain>.my.salesforce.com" },
  "streamingCapabilities": { "chunkTypes": ["Text"] },
  "bypassUser": true
}
```

Message body: `{"message": {"sequenceId": 1, "type": "Text", "text": "…"}}`, with
`sequenceId` going up by one per message in the session.

`scripts/agent_api_chat.py` does the whole loop (token → session → sync or streaming turns
→ end) with the standard library only. Credentials come from environment variables, never
arguments or files. `--dry-run` prints the requests without sending anything.

```bash
export SF_MY_DOMAIN=<mydomain>.my.salesforce.com SF_CLIENT_ID=… SF_CLIENT_SECRET=…
python3 scripts/agent_api_chat.py --agent-id 0Xx… --stream "Where is my order?"
python3 scripts/agent_api_chat.py --agent-id 0Xx…            # interactive; empty line ends
```

## Rules that prevent most failures

1. **The agent must not be "Agentforce (Default)"**, and it must be active.
2. **External Client App**: scopes `api`, `refresh_token offline_access`, `chatbot_api`,
   `sfap_api`; enable Client Credentials Flow **and** "Issue JWT-based access tokens for
   named users"; on the Policy tab enable client credentials again and set **Run As** to a
   user with at least API Only access. Untick the three "Require secret / PKCE" boxes.
3. **Two different hosts.** The token call and `instanceConfig.endpoint` use your **My
   Domain** URL (`*.my.salesforce.com`, not `*.lightning.force.com`). Every Agent API call
   goes to `api.salesforce.com`, or `api.gov.salesforce.com` on Government Cloud. The wrong
   My Domain gives `EngineConfigLookupException` (HTTP 500); the wrong API host gives 404.
4. **Agent ID.** New Agentforce Builder / Agent Script agents:
   `SELECT Id FROM BotDefinition WHERE DeveloperName = '<Agent_API_Name>'`. Legacy builder:
   the 18-character `0Xx…` id at the end of the agent's Setup URL. A bad id gives HTTP 400
   "… is not a valid agent ID" or a 500 `HttpServerErrorException`.
5. **`bypassUser`.** `true` runs as the agent's assigned user (what you want with client
   credentials); `false` runs as the token's user and needs a named-user token. It decides
   whose record and field access the actions get.
6. **One request at a time per session.** A second call while one is in flight returns
   **HTTP 423** (session locked). Serialise turns; don't retry in parallel.
7. **120-second timeout**, reported as **HTTP 500**. Keep slow actions out of a single turn.
8. **Streaming**: send `Accept: text/event-stream`. Concatenate `TextChunk.message`; treat
   the `Inform` as the authoritative full reply; stop at `EndOfTurn`. On a
   `ValidationFailureChunk`, **discard every chunk already shown** and render only what
   streams afterwards.
9. **Variables**: send them in `variables[]` (`name`, `type`, `value`) at session start.
   `$Context.*` variables are read-only after start except `$Context.EndUserLanguage`; drop
   the `__c` suffix (`Conversation_Key__c` → `$Context.Conversation_Key`). A custom variable
   must allow API writes (Builder: "Allow value to be set by API"; metadata:
   `visibility` External). Details: `references/agent-api.md#variables`.
10. **Usage is billed** as generative AI consumption (Flex Credits). Load tests cost money.

## Custom connection checklist (details in `references/custom-connections.md`)

- Metadata API **66.0+**. Deploy `AiResponseFormat` files before the `AiSurface` that
  lists them, then add `<plannerSurfaces>` (surface name + `surfaceType` `Custom`) to the
  agent's `GenAiPlannerBundle`.
- Start sessions with `"surfaceConfig": {"surfaceType": "Custom"}`; without it you get
  plain text.
- A formatted turn has `messages[].result[0]`: `type` = `SURFACE_ACTION__<FormatName>`
  (without the `_{surfaceId}` suffix), `value` = a **JSON string**. Parse it, validate it
  against your schema, and fall back to `message` text when `result` is empty or invalid.
  The platform doesn't enforce the schema and picks at most one format per turn.
- Keep fewer than 7 formats per connection; write each `description` as selection rules.

## Enhanced Chat v2 inline (details in `references/enhanced-chat-v2.md`)

```javascript
embeddedservice_bootstrap.settings.displayMode = 'inline';
embeddedservice_bootstrap.settings.targetElement = document.querySelector('.chat-container');
embeddedservice_bootstrap.settings.headerEnabled = false;          // optional
embeddedservice_bootstrap.settings.disableInlineAutoLaunch = true; // optional; then call launchChat()
```

Set these after pasting the deployment's Code Snippet and before it initialises. Set
`displayMode` and `targetElement` together; the console warns if only one is set.

## OTel export (details in `references/otel-api.md`)

`GET https://{MY_DOMAIN}/services/data/v66.0/einstein/audit/otel/{session-id}` → OTLP v1.0
`ResourceSpans` JSON for one session. Beta: one session per call, sessions that started in
the **last 72 hours**, Connect API rate limits, needs Session Tracing + Audit and Feedback
turned on (data lives in Data 360).

## Before you call an org

- Confirm the target org with the user. Never write consumer secrets or tokens into files,
  commits or logs; read them from the environment or a secret store.
- Read back what you deployed (`AiSurface`, `AiResponseFormat`, the planner bundle) before
  blaming the client.
- To see what the agent actually did in an API session, query the trace DMOs
  (`agentforce-platform-tracing-stdm`) or pull it with the OTel API. `externalSessionKey`
  is the key you chose to find it again.

## Source documentation

Agentforce Developer Guide (`developer.salesforce.com/docs/ai/agentforce/guide/`):
`agent-api-get-started`, `agent-api-agent-id`, `agent-api-lifecycle`, `agent-api-examples`,
`agent-api-variables`, `agent-api-considerations`, `agent-api-troubleshooting`,
`get-started-enhanced-chat`, `enhanced-chat-inline-mode`, `custom-connections`,
`custom-connections-get-started`, `custom-connections-response-formats`,
`custom-connections-troubleshooting`, `otel-api`. API reference:
<https://developer.salesforce.com/docs/ai/agentforce/references/agent-api?meta=summary>.
Postman collection:
<https://www.postman.com/salesforce-developers/salesforce-developers/collection/gwv9bjy/agent-api>.
