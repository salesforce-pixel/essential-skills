# Custom connections — structured replies for your own chat client

A custom connection links an **external web client** to an agent through the **Agent API**.
You declare which structured response formats your client can render; the agent returns
JSON matching one of those schemas so you can render carousels, cards, forms, pickers or
any other component of your design system. Reasoning, subagent selection and action
execution stay in Agentforce.

Use one when you host the chat yourself and want native components. If an out-of-the-box
channel such as Enhanced Chat v2 is enough, use that instead (`enhanced-chat-v2.md`).

## Contents

- [How the agent picks a format](#how-the-agent-picks-a-format)
- [Prerequisites](#prerequisites)
- [Metadata layout](#metadata-layout)
- [package.xml](#packagexml)
- [AiSurface](#aisurface)
- [AiResponseFormat](#airesponseformat)
- [Attach it to the agent](#attach-it-to-the-agent)
- [Deploy](#deploy)
- [Use it from the Agent API](#use-it-from-the-agent-api)
- [Parse the response](#parse-the-response)
- [Example formats](#example-formats)
- [Design tips](#design-tips)
- [Troubleshooting](#troubleshooting)
- [Open questions](#open-questions)

## How the agent picks a format

1. Topic and action instructions for the turn run first.
2. The agent reads the `description` and `instructions` of every **enabled**
   `AiResponseFormat` (plus the `AiSurface` instructions) and picks **at most one** format
   for the turn.
3. If none fits, or producing the structured output fails, it returns a normal Agent API
   reply with plain text. **No log tells you why a format wasn't chosen.**

`sortOrder` on instructions sets the order they're sent to the LLM (lower first). It
influences priority but doesn't enforce it. Selection and schema conformance are
**nondeterministic**: the agent can pick the wrong format or return JSON that doesn't match
the schema. Your client must handle valid structured output, invalid structured output and
plain text.

## Prerequisites

- A client that already starts Agent API sessions and gets plain-text replies
  (`agent-api.md`), and an External Client App.
- **Metadata API 66.0+** to retrieve and deploy.
- If plain text is all your client needs, skip the metadata and just send `surfaceConfig`
  (below).

## Metadata layout

| Type | Purpose |
|---|---|
| `AiSurface` | The connection: surface-level instructions and the list of response formats. |
| `AiResponseFormat` | One structured output format: a JSON schema plus selection instructions. |
| `GenAiPlannerBundle` | The agent; a `plannerSurfaces` entry associates it with the connection. |

```
unpackaged/
├── package.xml
├── aiResponseFormats/
│   ├── AcmeChatChoices_{surfaceId}.aiResponseFormat
│   ├── AcmeChatChoicesWithImages_{surfaceId}.aiResponseFormat
│   └── AcmeChatTimePicker_{surfaceId}.aiResponseFormat
├── aiSurfaces/
│   └── AcmeChatClient_{surfaceId}.aiSurface
└── genAiPlannerBundles/
    └── {YourPlannerBundle}/
        └── {YourPlannerBundle}.genAiPlannerBundle
```

`{surfaceId}` is a unique alphanumeric suffix shared by the surface and its formats. Pick
your own (e.g. `MyCustomSurface_01`) or keep the one a metadata export generated.

## package.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types><members>*</members><name>AiSurface</name></types>
    <types><members>*</members><name>AiResponseFormat</name></types>
    <!-- Optional: only to retrieve/deploy the agents that use the connection -->
    <types><members>*</members><name>GenAiPlannerBundle</name></types>
    <version>66.0</version>
</Package>
```

## AiSurface

```xml
<?xml version="1.0" encoding="UTF-8"?>
<AiSurface xmlns="http://soap.sforce.com/2006/04/metadata">
    <description>Custom AcmeChatClient surface.</description>
    <instructions>
        <instruction>Always reply with a brief, friendly, clear response under 160 characters.</instruction>
        <sortOrder>1</sortOrder>
    </instructions>
    <instructions>
        <instruction>Do not use response formats where the response contains more than 10 choices.</instruction>
        <sortOrder>2</sortOrder>
    </instructions>
    <instructions>
        <instruction>Do not use any of the AcmeChat* type formatting where the response contains only a single, text-only choice without images or URLs.</instruction>
        <sortOrder>3</sortOrder>
    </instructions>
    <masterLabel>AcmeChatClient</masterLabel>
    <responseFormats>
        <enabled>true</enabled>
        <responseFormat>AcmeChatChoices_{surfaceId}</responseFormat>
    </responseFormats>
    <responseFormats>
        <enabled>true</enabled>
        <responseFormat>AcmeChatChoicesWithImages_{surfaceId}</responseFormat>
    </responseFormats>
    <responseFormats>
        <enabled>true</enabled>
        <responseFormat>AcmeChatTimePicker_{surfaceId}</responseFormat>
    </responseFormats>
    <surfaceType>Custom</surfaceType>
</AiSurface>
```

| Field | Type | Meaning |
|---|---|---|
| `description` | String | Description of the connection |
| `instructions` | `instructions[]` | General guidance for the whole connection (tone, length, when not to format). Each has `instruction` (String) + `sortOrder` (Integer) |
| `masterLabel` | String | Display label |
| `responseFormats` | list | Each has `enabled` (Boolean) + `responseFormat` (developer name of an `AiResponseFormat`) |
| `surfaceType` | String | `Custom` for custom connections. Other values: `Messaging`, `Telephony`, `NextGenChat` |

Surface instructions set general behaviour; response-format instructions decide selection.

## AiResponseFormat

| Field | Type | Meaning |
|---|---|---|
| `description` | String | Tells the agent **when** to select this format; the agent evaluates it |
| `input` | String | JSON schema of the formatted response. Not strictly enforced: validate on the client |
| `instructions` | `instructions[]` | Detailed use-case conditions for this format (`instruction` + `sortOrder`) |
| `invocationTarget` | String | Optional reference to an invocable action |
| `invocationTargetType` | String | `apex`, `flow` or `standardInvocableAction` |
| `masterLabel` | String | Display label |

Create one per output type your client renders. Examples are [below](#example-formats).

## Attach it to the agent

Add to the agent's `GenAiPlannerBundle`:

```xml
<plannerSurfaces>
    <callRecordingAllowed>false</callRecordingAllowed>
    <surface>AcmeChatClient_{surfaceId}</surface>
    <surfaceType>Custom</surfaceType>
</plannerSurfaces>
```

The `surfaceType` here must equal the one on the `AiSurface`. To find and retrieve the
right planner bundle (and its version naming), use the `afagent-metadata-helper` skill.

## Deploy

```bash
sf project deploy start --manifest unpackaged/package.xml -o <alias>
```

- Deploying in steps: **`AiResponseFormat` first, then `AiSurface`**, then the planner
  bundle; the surface references the formats.
- To update a connection or format, redeploy with the same developer name; it replaces the
  previous definition.
- Sandboxes and scratch orgs work for testing.

## Use it from the Agent API

Add to the start-session body:

```json
"surfaceConfig": { "surfaceType": "Custom" }
```

If the agent can't resolve a connection or format, you get a standard plain-text reply.

## Parse the response

```json
{
  "messages": [
    {
      "id": "cb19c42e-2d70-4b19-89a7-69cf7aadc92e",
      "type": "Inform",
      "message": "Text response reformatted in the format SURFACE_ACTION__RegistrationForm",
      "result": [
        {
          "property": "",
          "type": "SURFACE_ACTION__RegistrationForm",
          "value": "{\"title\":\"registrationForm\",\"message\":\"To register your vehicle, please provide the plate number and the two-letter state name.\"}"
        }
      ],
      "isContentSafe": true,
      "feedbackId": "bd13…",
      "planId": "bd13…"
    }
  ]
}
```

1. `result` present and non-empty → a format was applied.
2. `result[0].type` = `SURFACE_ACTION__` + the `AiResponseFormat` developer name **without**
   the `_{surfaceId}` suffix. Map it to a renderer.
3. `JSON.parse(result[0].value)` — it's an escaped JSON **string**, not an object.
4. Validate it against the format's schema; if parsing or validation fails, or `result` is
   empty, render `message` as plain text.

```javascript
function renderTurn(msg, renderers, renderText) {
  const r = msg.result && msg.result[0];
  if (r && typeof r.type === 'string' && r.type.startsWith('SURFACE_ACTION__')) {
    const name = r.type.slice('SURFACE_ACTION__'.length);
    try {
      const data = JSON.parse(r.value);
      const render = renderers[name];
      if (render && render.validate(data)) return render(data);
    } catch (e) { /* fall through to text */ }
  }
  return renderText(msg.message);
}
```

## Example formats

### Text choices (2–7 options)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<AiResponseFormat xmlns="http://soap.sforce.com/2006/04/metadata">
    <description>A response action for AcmeChatClient. Use this to prompt the user to select one of many available text choices when the number of choices is GREATER THAN 1 and LESSER THAN 8.</description>
    <input>{"type":"object","properties":{"message":{"type":"string","description":"Placeholder for message input"},"choices":{"type":"array","items":{"type":"string"}}},"required":["message","choices"]}</input>
    <instructions>
        <instruction>Always use AcmeChatChoices when showing choice text responses with GREATER THAN 1 choice and LESS THAN 8 choices to the user.</instruction>
        <sortOrder>1</sortOrder>
    </instructions>
    <masterLabel>Acme Chat Choice Response</masterLabel>
</AiResponseFormat>
```

### Choices with images (product listings, locations, avatars)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<AiResponseFormat xmlns="http://soap.sforce.com/2006/04/metadata">
    <description>A response action for AcmeChatClient. Use this to prompt the user to select one of many choices with accompanying images, such as product listings.</description>
    <input>{"type":"object","properties":{"message":{"type":"string","description":"Placeholder for message input"},"choices":{"type":"array","items":{"type":"object","properties":{"title":{"type":"string"},"imageUrl":{"type":"string"},"actionText":{"type":"string"}},"required":["title","imageUrl","actionText"]}}},"required":["message","choices"]}</input>
    <instructions>
        <instruction>Always use AcmeChatChoicesWithImages when showing choices with images with GREATER THAN 1 choice and LESS THAN 8 choices to the user.</instruction>
        <sortOrder>2</sortOrder>
    </instructions>
    <masterLabel>Acme Chat Choice With Images</masterLabel>
</AiResponseFormat>
```

### Time picker (Slack Block Kit `timepicker` shape)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<AiResponseFormat xmlns="http://soap.sforce.com/2006/04/metadata">
    <description>A response action for AcmeChatClient. Use this to prompt the user to select a time using a time picker component.</description>
    <input>
{
  "type": "object",
  "properties": {
    "type": { "const": "section" },
    "text": {
      "type": "object",
      "properties": { "type": { "const": "mrkdwn" }, "text": { "type": "string" } },
      "required": ["type", "text"],
      "additionalProperties": false
    },
    "accessory": {
      "type": "object",
      "properties": {
        "type": { "const": "timepicker" },
        "initial_time": { "type": "string", "pattern": "^(?:[01]\\d|2[0-3]):[0-5]\\d$" },
        "placeholder": {
          "type": "object",
          "properties": {
            "type": { "const": "plain_text" },
            "text": { "type": "string" },
            "emoji": { "type": "boolean" }
          },
          "required": ["type", "text", "emoji"],
          "additionalProperties": false
        },
        "action_id": { "type": "string" }
      },
      "required": ["type", "initial_time", "placeholder", "action_id"],
      "additionalProperties": false
    }
  },
  "required": ["type", "text", "accessory"],
  "additionalProperties": false
}
    </input>
    <instructions>
        <instruction>Use AcmeChatTimePicker when you need the user to select a specific time. The response must conform to Slack Block Kit timepicker syntax.</instruction>
        <sortOrder>3</sortOrder>
    </instructions>
    <masterLabel>Acme Chat Time Picker</masterLabel>
</AiResponseFormat>
```

Expected output: `{"type":"section","text":{"type":"mrkdwn","text":"…"},"accessory":{"type":"timepicker","initial_time":"13:37","placeholder":{"type":"plain_text","text":"Choose a time","emoji":true},"action_id":"meeting_time_picker"}}`.

## Design tips

- **Fewer than 7 formats per connection.** More makes selection unreliable.
- **Write `description` for the selector, not for people.** State exact conditions: item
  counts, whether images exist, data shape. Make conditions mutually exclusive across
  formats (e.g. "text-only, 2–7 items" vs "with images, 2–7 items").
- **Generate the JSON schema with an LLM** from the structure your client expects, then
  check it's valid JSON. Escape it properly inside `<input>`.
- Put "when not to format" rules on the `AiSurface` (single choice, more than N items).

## Troubleshooting

| Issue | Fix |
|---|---|
| Invalid JSON schema | `input` must be valid, properly escaped JSON |
| Missing references | Every format listed in `AiSurface` must be a deployed `AiResponseFormat` |
| Deployment errors | Deploy `AiResponseFormat` before `AiSurface` |
| Surface type mismatch | `surfaceType` in `AiSurface` must match the `plannerSurfaces` entry |
| Replies never formatted | The start-session body lacks `"surfaceConfig": {"surfaceType": "Custom"}`; or the formats' descriptions don't match the turn (no logs; tighten wording) |

## Open questions

Not covered by the docs; check in your org before relying on them.

- **Agent Script agents.** The docs attach the surface through `GenAiPlannerBundle`. For
  agents built in the new Builder, that bundle is compiled when you publish, so a
  hand-added `plannerSurfaces` entry may not survive the next publish. Retrieve the
  planner bundle after each publish and check the entry is still there.
- **Several custom surfaces on one agent.** `surfaceConfig` only names `surfaceType`, not
  which surface, so which `Custom` surface is used when a bundle lists more than one isn't
  documented. Keep one `Custom` surface per agent.
