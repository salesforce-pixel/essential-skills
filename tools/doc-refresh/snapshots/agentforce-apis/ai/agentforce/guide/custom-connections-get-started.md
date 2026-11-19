# Set Up a Custom Connection

This guide walks through setting up a custom connection named `AcmeChatClient` end to end. For the concepts behind custom connections and how the agent chooses a response format, see [Custom Connections](/docs/ai/agentforce/guide/custom-connections.md).

## Prerequisites

Before you begin, ensure your org meets these requirements.

- **Agent API connectivity**: Your client application must be integrated with the Agent API and able to start sessions and receive responses. Follow the [Get Started with Agent API](/docs/ai/agentforce/guide/agent-api-get-started.md) instructions to set this up. Verify that you can initiate a session and receive basic text responses from your agent through your client before proceeding.
- **External Client App (ECA)**: Ensure that you have an [External Client App](https://help.salesforce.com/s/articleView?id=xcloud.external_client_apps.htm) to allow secure connection to the Agent API.
- **Metadata API version**: Version 66.0 or later is required for retrieval and deployment.

:::note
If your client only needs standard, unstructured text responses, skip the metadata setup and jump straight to [Use a Custom Connection](#use-a-custom-connection).
:::

## Metadata Overview

Setting up a custom connection involves creating and deploying three metadata types.

| Metadata Type        | Purpose                                                                                             |
| :------------------- | :-------------------------------------------------------------------------------------------------- |
| `AiSurface`          | Defines the connection configuration, including instructions and references to response formats.    |
| `AiResponseFormat`   | Defines a response format with a JSON input schema that the agent uses to structure its output.     |
| `GenAiPlannerBundle` | References the surface through `plannerSurfaces` entries to associate the connection with an agent. |

For the `GenAiPlannerBundle` metadata type reference, see [GenAiPlannerBundle](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_genaiplannerbundle.htm) in the Metadata API Developer Guide. For more information on agent metadata, see [Agentforce Metadata Types](/docs/ai/agentforce/references/agents-metadata-tooling/agents-metadatav67.md). Field references for `AiSurface` and `AiResponseFormat` are included inline below.

## Set Up the Custom Connection

### Directory Structure

Organize your metadata files using this structure.

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

The `{surfaceId}` suffix is a unique identifier that distinguishes your custom connection and its associated response formats. You can either choose your own unique alphanumeric string (for example, `MyCustomSurface_01`) or use the `surfaceId` generated during a metadata export.

### Step 1: Configure package.xml

The `package.xml` file declares the metadata types to deploy. See [Retrieve and Deploy Agent Metadata](/docs/ai/agentforce/guide/agent-dx-deploy-metadata.md).

```sfdocs-code {"lang":"xml", "title": "package.xml"}
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>*</members>
        <name>AiSurface</name>
    </types>
    <types>
        <members>*</members>
        <name>AiResponseFormat</name>
    </types>
    <!-- GenAiPlannerBundle is optional. Include it only if you also want to
         retrieve or deploy the agents using the connections. -->
    <types>
        <members>*</members>
        <name>GenAiPlannerBundle</name>
    </types>
    <version>66.0</version>
</Package>
```

### Step 2: Create the AiSurface

The `AiSurface` metadata type defines the custom connection and references the response formats available to it. The agent selects the most appropriate response format for each response. When no response format is appropriate, the agent returns an unformatted response.

Use `instructions` on the `AiSurface` to give the agent high-level guidance that applies to the whole connection—for example, tone, length limits, or conditions for when to skip formatting entirely. Each entry has an `instruction` string and a `sortOrder` integer. `sortOrder` controls the order in which instructions are sent to the LLM (lower values first), which influences but does not enforce priority.

```sfdocs-code {"lang":"xml", "title": "aiSurfaces/AcmeChatClient_{surfaceId}.aiSurface"}
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

#### AiSurface Reference

| Field             | Type                 | Description                                                                                                                                                                                                      |
| :---------------- | :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `description`     | String               | A description of the custom connection.                                                                                                                                                                          |
| `instructions`    | `instructions[]`     | Ordered instructions that guide the agent generally on how to behave for a connection. Each entry contains an `instruction` (String) and a `sortOrder` (Integer) that controls evaluation order.                 |
| `masterLabel`     | String               | The display label for the connection.                                                                                                                                                                            |
| `responseFormats` | `AiResponseFormat[]` | References to `AiResponseFormat` entities associated with this connection. Each entry contains an `enabled` (Boolean) flag and a `responseFormat` (String) that references the response format's developer name. |
| `surfaceType`     | String               | The type of connection. Set to `Custom` for custom connections. Other valid values are `Messaging`, `Telephony`, and `NextGenChat`.                                                                              |

The schema for `instructions` is the same on `AiSurface` and `AiResponseFormat`, but the instructions apply at different levels. Use `instructions` on `AiSurface` to give the agent general guidance about the connection. Use `instructions` on `AiResponseFormat` to describe detailed use-case conditions for when to apply a specific response format.

| Field         | Type    | Description                                                                                          |
| :------------ | :------ | :--------------------------------------------------------------------------------------------------- |
| `instruction` | String  | Natural language directions that the agent uses to reason between response formats and JSON schemas. |
| `sortOrder`   | Integer | The order in which the instructions are evaluated.                                                   |

### Step 3: Create AiResponseFormat Definitions

Each `AiResponseFormat` defines a structured output schema that the agent uses to format responses for your client. Create one `AiResponseFormat` for each output type your client supports.

The `instructions` on an `AiResponseFormat` describe detailed use-case situations that help the agent decide when to apply this specific format—for example, "Use this response format if there is a collection of between 2 and 5 choices for the user to select and each choice includes an associated image." Surface-level instructions set general behavior; response-format instructions determine selection.

For examples and authoring guidance, see [Response Format Examples for Custom Connections](/docs/ai/agentforce/guide/custom-connections-response-formats.md).

#### AiResponseFormat Reference

| Field                  | Type             | Description                                                                                                                                                                                                                     |
| :--------------------- | :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `description`          | String           | A description that tells the agent when to select this response format. The agent evaluates this field to decide whether the format is appropriate for the current response.                                                    |
| `input`                | String           | A JSON schema that defines the expected structure of the formatted response. The agent attempts to map its output to this schema, but the platform does not enforce strict adherence. Your client should validate the response. |
| `instructions`         | `instructions[]` | Ordered instructions that provide guidance to the agent for a single response format. Each entry contains an `instruction` (String) and a `sortOrder` (Integer).                                                                |
| `invocationTarget`     | String           | A reference to an invocable action. Relates to `invocationTargetType`.                                                                                                                                                          |
| `invocationTargetType` | String           | The type of the invocable action referenced by `invocationTarget`. Valid values are `apex`, `flow`, and `standardInvocableAction`.                                                                                              |
| `masterLabel`          | String           | The display label for the response format.                                                                                                                                                                                      |

### Step 4: Add the Connection to a GenAiPlannerBundle

In your `GenAiPlannerBundle` file, add a `plannerSurfaces` entry to associate the custom connection with your agent.

```sfdocs-code {"lang":"xml", "title": "GenAiPlannerBundle"}
<?xml version="1.0" encoding="UTF-8"?>
<GenAiPlannerBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <description>Your agent description</description>

    <!-- Other configurations: topics, actions, etc. -->

    <plannerSurfaces>
        <callRecordingAllowed>false</callRecordingAllowed>
        <surface>AcmeChatClient_{surfaceId}</surface>
        <surfaceType>Custom</surfaceType>
    </plannerSurfaces>
</GenAiPlannerBundle>
```

### Step 5: Deploy

Deploy the metadata using the Salesforce CLI. Navigate to the parent directory containing `unpackaged/` and run:

```sfdocs-code {"lang":"bash", "title": "Deploy"}
sf project deploy start --manifest unpackaged/package.xml
```

You can also deploy using your preferred Metadata API tool. If deploying incrementally, deploy `AiResponseFormat` entities before `AiSurface` entities, because the surface references the response formats.

To update an existing connection or response format, redeploy the metadata with the same developer name. The updated definition replaces the previous one.

## Use a Custom Connection

After deploying your custom connection metadata, update your Agent API session initialization call to use it.

Add the following to the body of your Agent API `/sessions` call:

```sfdocs-code {"lang":"json", "title": "Session Request Body"}
"surfaceConfig": {
  "surfaceType": "Custom"
}
```

This tells the agent to use your custom connection for the session. If the agent can't resolve a specific connection or response format, it returns a standard Agent API response with unformatted text.

## Parse the Response

When the agent applies a response format to a turn, the Agent API response includes a `result` array on the message. Each entry identifies which `AiResponseFormat` was applied and carries the structured output as a JSON string in the `value` field. A `SURFACE_ACTION__` prefix is automatically appended to `type` at runtime.

```sfdocs-code {"lang":"json", "title": "Example Agent API Response"}
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
      "feedbackId": "bd13a942-97fc-4e9a-bc6b-c3bb62ebcae2",
      "planId": "bd13a942-97fc-4e9a-bc6b-c3bb62ebcae2"
    }
  ]
}
```

:::note
When determining parser logic, the returned JSON string must be properly escaped.
:::

To render the response:

1. Check whether the message includes a `result` array. If it does, a response format was applied.
2. Read `result[0].type` to identify which format was selected. The value is prefixed with `SURFACE_ACTION__` followed by the `AiResponseFormat` developer name (without the `_{surfaceId}` suffix).
3. Parse `result[0].value` as JSON. The parsed object conforms to the `input` schema you defined on the `AiResponseFormat`.
4. If no `result` array is present, fall back to rendering the `message` field as plain text.

Because the platform does not validate the agent's structured output against the `input` schema, always validate `result[0].value` client-side before handing it to a renderer.

## Testing

You can deploy and test custom connections in sandbox and scratch orgs.

After deployment, test the connection by starting a session from your client through the Agent API and verifying that the agent returns responses using the structured formats you defined.

## See Also

- [Custom Connections](/docs/ai/agentforce/guide/custom-connections.md)
- [Response Format Examples for Custom Connections](/docs/ai/agentforce/guide/custom-connections-response-formats.md)
- [Troubleshoot Custom Connections](/docs/ai/agentforce/guide/custom-connections-troubleshooting.md)
- [Agent API Developer Guide](/docs/ai/agentforce/guide/agent-api.md)
