# Response Format Examples for Custom Connections

Use these examples as starting points when you design `AiResponseFormat` entries for your own custom connection. To reference an `AiResponseFormat` from your `AiSurface` see, [Set Up a Custom Connection](/docs/ai/agentforce/guide/custom-connections-get-started.md).

For background on how the agent selects a response format and why client-side validation matters, see [Custom Connections](/docs/ai/agentforce/guide/custom-connections.md).

## Text Choices

Use this format when you want to present the user with a short list of text-only options, such as a menu or a disambiguation prompt.

```sfdocs-code {"lang":"xml", "title": "aiResponseFormats/AcmeChatChoices_{surfaceId}.aiResponseFormat"}
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

## Choices with Images

Use this format when the user is selecting from a collection of items where an image is essential to the decision—product listings, location cards, or avatar pickers.

```sfdocs-code {"lang":"xml", "title": "aiResponseFormats/AcmeChatChoicesWithImages_{surfaceId}.aiResponseFormat"}
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

## Time Picker

Use this format when you need the user to pick a specific time. The schema below follows [Slack Block Kit timepicker](https://docs.slack.dev/tools/node-slack-sdk/reference/types/interfaces/Timepicker/) syntax, which is a useful reference if your client already renders Block Kit components.

```sfdocs-code {"lang":"xml", "title": "aiResponseFormats/AcmeChatTimePicker_{surfaceId}.aiResponseFormat"}
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
      "properties": {
        "type": { "const": "mrkdwn" },
        "text": { "type": "string" }
      },
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

The time picker schema expects the agent to produce output in this format:

```sfdocs-code {"lang":"json", "title": "Example Agent Output"}
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "Section block with a timepicker"
  },
  "accessory": {
    "type": "timepicker",
    "initial_time": "13:37",
    "placeholder": {
      "type": "plain_text",
      "text": "Choose a time",
      "emoji": true
    },
    "action_id": "meeting_time_picker"
  }
}
```

## Tips for Designing Your Own Response Formats

- **Keep the set small.** We recommend fewer than 7 response formats per connection. Too many formats make it harder for the agent to reliably pick the right one.
- **Write the `description` for selection, not for humans.** The agent uses the `description` and `instructions` to decide whether a format applies. Spell out the exact conditions—number of items, presence of images, data shape—in natural language.
- **Generate the JSON schema with an LLM.** Provide your preferred LLM with the output structure your client expects and ask it to generate the corresponding JSON schema.

## See Also

- [Set Up a Custom Connection](/docs/ai/agentforce/guide/custom-connections-get-started.md)
- [Troubleshoot Custom Connections](/docs/ai/agentforce/guide/custom-connections-troubleshooting.md)
