# Custom Connections

Custom connections connect an external web client to an Agentforce agent through the [Agent API](/docs/ai/agentforce/guide/agent-api.md). You define a metadata-based connection that tells the agent which structured response formats your client supports, and the agent returns JSON that conforms to those schemas so your client can render native UI components like carousels, cards, forms, or pickers.

## When to Use a Custom Connection

Consider building a custom connection when you want to:

- Host a chat experience in your own infrastructure, outside of Salesforce-managed surfaces.
- Render agent responses as native UI components in your client—carousels, cards, forms, pickers, or any other component your design system supports.
- Keep full control of the client-side experience while still using Agentforce for reasoning, subagent selection, and action execution.

:::note
If an out-of-the-box channel like [Enhanced Chat v2](/docs/ai/agentforce/guide/get-started-enhanced-chat.md) meets your needs, use that instead. Custom connections are for teams that need to build a channel from the ground up.
:::

## How It Works

A custom connection is defined through two metadata types that you deploy to your org:

- **`AiSurface`** defines the connection itself, including surface-level instructions and the set of response formats available to the agent.
- **`AiResponseFormat`** defines a single structured output format using a JSON schema. The agent uses the format's description and instructions to decide when to apply it, then maps its response into the schema so your client can render the output as a specific UI component.

You associate the connection with an agent by adding a `plannerSurfaces` entry to the agent's `GenAiPlannerBundle`. Your client then starts agent sessions through the [Agent API](/docs/ai/agentforce/guide/agent-api.md), passing `surfaceConfig` in the session initialization request to tell the agent to use your custom connection.

### Response Format Selection

When the agent generates a response, it uses this process to decide whether to apply a response format:

1. **Topic and action instructions run first.** The agent processes the topic and action instructions associated with the current conversation turn before evaluating response formats.
2. **Response format selection.** The agent evaluates the `description` and `instructions` on each enabled `AiResponseFormat` and selects at most one format per turn—the one it judges to best fit the current response. The `instructions` on the `AiSurface` provide additional high-level guidance (for example, "don't use formatting for single text-only choices").
3. **Fallback.** If no response format is selected—or if the agent encounters an error while producing structured output, the agent returns a standard Agent API response with unformatted text. There are no visible logs that provide information on why a response format was not selected.

The `sortOrder` value on each `instructions` entry controls the order in which those instructions are fed to the LLM. Lower values are sent first. Ordering influences but does not enforce priority because selection is nondeterministic.

:::warning
All instructions on response formats are nondeterministic. The agent uses natural language instructions when choosing which schema to apply, but there is no strict enforcement. The agent may select the wrong format or produce output that doesn't perfectly conform to the JSON schema defined in the `input` field. Build your client-side parsing to handle both well-formed structured responses and plain-text fallback responses.
:::

## Resources

- [Set Up a Custom Connection](/docs/ai/agentforce/guide/custom-connections-get-started.md)
- [Response Format Examples for Custom Connections](/docs/ai/agentforce/guide/custom-connections-response-formats.md)
- [Troubleshoot Custom Connections](/docs/ai/agentforce/guide/custom-connections-troubleshooting.md)
- [Agent API Developer Guide](/docs/ai/agentforce/guide/agent-api.md)
