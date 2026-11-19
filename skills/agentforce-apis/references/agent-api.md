# Agent API — full reference

Headless REST access to an Agentforce agent: start a session, exchange messages (sync or
streaming), pass variables, read citations, submit feedback, end the session.

Base URL: `https://api.salesforce.com/einstein/ai-agent/v1` (Government Cloud:
`https://api.gov.salesforce.com/einstein/ai-agent/v1`, same paths and bodies).

Not supported for agents of type **Agentforce (Default)**. You need Agentforce enabled and
at least one active agent.

## Contents

- [1. External Client App](#1-external-client-app)
- [2. Token](#2-token)
- [3. Agent ID](#3-agent-id)
- [4. Endpoints](#4-endpoints)
- [5. Start session](#5-start-session)
- [6. Send a message (sync)](#6-send-a-message-sync)
- [7. Send a message (streaming SSE)](#7-send-a-message-streaming-sse)
- [8. Citations](#8-citations)
- [Variables](#variables)
- [9. End session](#9-end-session)
- [10. Feedback](#10-feedback)
- [11. Considerations](#11-considerations)
- [12. Troubleshooting](#12-troubleshooting)

## 1. External Client App

Setup → External Client Apps Manager → New External Client App.

1. Name and contact email. **Enable OAuth**. Scopes:
   - Manage user data via APIs (`api`)
   - Perform requests at any time (`refresh_token`, `offline_access`)
   - Access chatbot services (`chatbot_api`)
   - Access the Salesforce API Platform (`sfap_api`)
2. Tick **Enable Client Credentials Flow** and **Issue JSON Web Token (JWT)-based access
   tokens for named users**.
3. Untick **Require secret for Web Server Flow**, **Require secret for Refresh Token Flow**
   and **Require PKCE extension for Supported Authorization Flows**.
4. Create. Then **Policy** tab → Edit → OAuth Flows and External Client App Enhancements →
   tick **Enable Client Credentials Flow** → set **Run As (Username)** to a user with at
   least API Only access → Save.
5. **Settings** tab → OAuth Settings → **Consumer Key and Secret** → copy both.

Any flow that yields a JWT-based access token works; client credentials is the simplest.

## 2. Token

```bash
curl https://{MY_DOMAIN_URL}/services/oauth2/token \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'grant_type=client_credentials' \
  --data-urlencode 'client_id={CONSUMER_KEY}' \
  --data-urlencode 'client_secret={CONSUMER_SECRET}'
```

`MY_DOMAIN_URL` = Setup → My Domain → **Current My Domain URL** (`*.my.salesforce.com`).
Not the `*.lightning.force.com` host in the browser.

Response (shortened): `access_token` (JWT), `token_format: "jwt"`,
`scope: "sfap_api chatbot_api api"`, `instance_url`, `api_instance_url:
"https://api.salesforce.com"`, `token_type: "Bearer"`. If `scope` lacks `chatbot_api` or
`sfap_api`, fix the app's scopes before going further.

## 3. Agent ID

| Builder | How to get the ID |
|---|---|
| New Agentforce Builder (Agentforce Studio, Canvas/Script view, Agent Script) | `SELECT Id, DeveloperName FROM BotDefinition WHERE DeveloperName = '<Agent_API_Name>'` — the `Id` (`0Xx…`) is the agent ID |
| Legacy Agentforce Builder (Setup → Agentforce Agents) | The 18-character id at the end of the Agent Overview URL, e.g. `…/lightning/setup/EinsteinCopilot/0XxSB000000IPCr0AO/edit` |

The `BotDefinition` query works for both, so prefer it in scripts:

```bash
sf data query -o <alias> --json \
  -q "SELECT Id, DeveloperName, MasterLabel FROM BotDefinition WHERE DeveloperName = '<Agent_API_Name>'"
```

## 4. Endpoints

| Call | Method + path | Notes |
|---|---|---|
| Start session | `POST /agents/{AGENT_ID}/sessions` | Returns `sessionId`, `_links`, greeting `messages` |
| Send message (sync) | `POST /sessions/{SESSION_ID}/messages` | `Accept: application/json` |
| Send message (stream) | `POST /sessions/{SESSION_ID}/messages/stream` | `Accept: text/event-stream` (SSE) |
| End session | `DELETE /sessions/{SESSION_ID}` | Header `x-session-end-reason: UserRequest` |
| Submit feedback | `POST /sessions/{SESSION_ID}/feedback` | HTTP 201 on success |

All calls: `Authorization: Bearer {ACCESS_TOKEN}`; bodies need
`Content-Type: application/json`.

## 5. Start session

```bash
curl -X POST https://api.salesforce.com/einstein/ai-agent/v1/agents/{AGENT_ID}/sessions \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer {ACCESS_TOKEN}' \
  --data '{
    "externalSessionKey": "{RANDOM_UUID}",
    "instanceConfig": { "endpoint": "https://{MY_DOMAIN_URL}" },
    "streamingCapabilities": { "chunkTypes": ["Text"] },
    "bypassUser": true
  }'
```

| Field | Meaning |
|---|---|
| `externalSessionKey` | A UUID you generate. Use it to find the conversation in the agent's event logs. |
| `instanceConfig.endpoint` | Your My Domain URL, with `https://`. Wrong value → `EngineConfigLookupException`. |
| `streamingCapabilities.chunkTypes` | `["Text"]` to receive `TextChunk` events on the stream endpoint. |
| `bypassUser` | `true`: run as the agent's assigned user. `false`: run as the token's user. With client credentials use `true`. |
| `variables` | Optional context and custom variables; see [Variables](#variables). |
| `surfaceConfig` | `{"surfaceType": "Custom"}` to use a custom connection; see `custom-connections.md`. |

Response:

```json
{
  "sessionId": "8e715939-a121-40ec-80e3-a8d1ac89da33",
  "_links": {
    "self": null,
    "messages": { "href": "https://api.salesforce.com/einstein/ai-agent/v1/sessions/8e71…/messages/stream" },
    "session":  { "href": "https://api.salesforce.com/einstein/ai-agent/v1/agents/0XxQZ0000000Ty50AE/sessions" },
    "end":      { "href": "https://api.salesforce.com/einstein/ai-agent/v1/sessions/8e71…" }
  },
  "messages": [
    { "type": "Inform", "id": "8e7c…", "feedbackId": "", "planId": "", "isContentSafe": true,
      "message": "Hi, I'm an AI service assistant. How can I help you?", "result": [], "citedReferences": [] }
  ]
}
```

## 6. Send a message (sync)

```bash
curl https://api.salesforce.com/einstein/ai-agent/v1/sessions/{SESSION_ID}/messages \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer {ACCESS_TOKEN}' \
  --data '{"message": {"sequenceId": 1, "type": "Text", "text": "Show me the cases for Lauren Bailey."}}'
```

`sequenceId` is a number you supply; increase it for every message in the session.

Response: `messages[]` of `Inform` objects with `id`, `feedbackId`, `planId`,
`isContentSafe`, `message` (the text), `result` (structured output, used by custom
connections), `citedReferences`, `metrics`; plus `_links`.

## 7. Send a message (streaming SSE)

Same body, path `…/messages/stream`, header `Accept: text/event-stream`. Each SSE `data:`
line is a JSON envelope `{timestamp, originEventId, traceId, offset, message}`:

| `message.type` | What to do |
|---|---|
| `ProgressIndicator` | Show a busy state; `indicatorType` (e.g. `ACTION`) and `message` ("Working on it"). |
| `TextChunk` | Append `message` to the visible reply (`formatType: "Text"`, `offset` orders chunks). |
| `ValidationFailureChunk` | The agent's response failed validation: **remove all chunks rendered so far** and show only the content that streams next. |
| `Inform` | The complete reply (same shape as a sync `Inform`, including `citedReferences`). Use it as the final text. |
| `EndOfTurn` | The turn is done; you may send the next message. |

Note: the docs' sample `Inform` stream event shows a `messages` array with `_links`, while
the other events carry a single `message`. Parse both shapes.

## 8. Citations

`Inform.citedReferences[]`: `type` (`link`), `value` (URL), `recordId`, `label`, and
optionally `inlineMetadata[]` with `claim` (the cited text) and `location` (character
offset in `message`). No `inlineMetadata` → show the sources under the reply; with it →
place an inline marker at `location`.

## Variables

Pass context and custom variables at session start (and editable ones on later
messages) in a `variables` array:

```json
{
  "externalSessionKey": "{RANDOM_UUID}",
  "instanceConfig": { "endpoint": "https://{MY_DOMAIN_URL}" },
  "streamingCapabilities": { "chunkTypes": ["Text"] },
  "bypassUser": true,
  "variables": [
    { "name": "$Context.EndUserLanguage", "type": "Text", "value": "en_US" },
    { "name": "team_descriptor", "type": "Text", "value": "The Greatest Team" },
    { "name": "troubleshootingSteps", "type": "Text", "value": "1. Check the username. 2. …" }
  ]
}
```

(The docs' copy of this sample is missing a comma between the 2nd and 3rd variable; the
version above is valid JSON.)

- Many variables are read-only and can only be set at **start session**. `$Context.*`
  variables are not editable after start, **except `$Context.EndUserLanguage`**. Only
  editable variables can change on a send-message call.
- Variables from custom fields drop `__c`: `Conversation_Key__c` → `$Context.Conversation_Key`.
- **Agentforce Builder**: the variable must have **Allow value to be set by API** ticked.
- **Metadata API**: `ConversationVariable` (in `BotVersion`, `BotTemplate`) and
  `ConversationContextVariable` (in `Bot`, `BotTemplate`).

| Field | Meaning |
|---|---|
| `dataType` | Text, Number, Boolean, Object, Date, DateTime, Currency, Id |
| `description` | Read by the planner |
| `developerName` | Starts with a letter; no spaces, no trailing `_`, no `__` |
| `includeInPrompt` | Sent to the model. `Id`, `EndUserId`, `EndUserLanguage` always show as included; don't change it for those |
| `label` | UI label |
| `visibility` | `ConversationVariable` only. `internal`: only action outputs can set it. `external`: action outputs **and** APIs such as the Agent API |

For Agent Script agents the same idea is a variable with `visibility: "External"`; see the
`agentscript` skill (`reference/ascript-ref-variables.md`).

## 9. End session

```bash
curl -X DELETE https://api.salesforce.com/einstein/ai-agent/v1/sessions/{SESSION_ID} \
  --header 'x-session-end-reason: UserRequest' \
  --header 'Authorization: Bearer {ACCESS_TOKEN}'
```

Returns `messages: [{"type": "SessionEnded", "reason": "ClientRequest", …}]`. Always end
sessions you start, including in error paths.

## 10. Feedback

```bash
curl https://api.salesforce.com/einstein/ai-agent/v1/sessions/{SESSION_ID}/feedback \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer {ACCESS_TOKEN}' \
  --data '{"feedbackId": "<feedbackId from the Inform>", "feedback": "GOOD", "text": "Email looks great"}'
```

HTTP 201 = received. Stored in Data 360 with Generative AI Audit and Feedback data.

## 11. Considerations

- **Not for "Agentforce (Default)" agents.**
- **Billing**: Agent API usage consumes generative AI credits (Help: *Generative AI Usage
  and Billing*).
- **Timeout**: 120 s per call; a timeout is returned as **HTTP 500**.
- **Concurrency**: one in-flight request per session (else HTTP 423).
- **Government Cloud**: `api.gov.salesforce.com` everywhere.
- **Access**: with `bypassUser: true` actions see what the agent user can see; with `false`
  they see what the token's user can see. Grant object, field and Apex class access to the
  right user.

## 12. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| 400, `{VALUE} is not a valid agent ID` | Wrong agent ID; re-query `BotDefinition` |
| 401 | Token problem: wrong key/secret, client credentials not enabled on the Policy tab, no Run As user, missing scopes |
| 404 | Wrong host or token; on Government Cloud you must call `api.gov.salesforce.com` |
| 423 Session Already Locked | Another request on this session is still running; wait for it |
| 500 `Unsupported Media Type` | Send `Content-Type: application/json` |
| 500 `EngineConfigLookupException` | `instanceConfig.endpoint` isn't your My Domain URL |
| 500 `HttpServerErrorException` | Wrong agent ID in the path |
| 500 after ~120 s | Timeout; make the turn faster |
| Reply flickers / garbled when streaming | You ignored `ValidationFailureChunk`; clear rendered chunks on it |
