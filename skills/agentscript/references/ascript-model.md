# Configure Models in Agent Script

By default, Agentforce uses the [org-level model selected in Setup](https://help.salesforce.com/s/articleView?id=ai.agent_setup_select_model_provider.htm\&type=5) for all agents and subagents. To use a different model, or to change model behavior, use `model_config` parameters. To specify a model other than the default, set `model`. To configure how the model behaves, set `max_tokens`, `temperature`, and `top_p`.

| Parameter     | What It Does                                                                                                                                                | Typical Value                                   |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `model`       | Specifies the model to use for the agent or subagent.                                                                                                       | `model://sfdc_ai__DefaultVertexAIGemini35Flash` |
| `temperature` | Controls how random responses are. Lower values give more focused, repeatable answers; higher values give more varied ones.                                 | `0` to `1`                                      |
| `max_tokens`  | Caps the length of the model's response, in tokens.                                                                                                         | For example, `500` or `2000`                    |
| `top_p`       | Nucleus sampling. The model picks from the most likely tokens until their combined probability reaches this value. Lower values make responses less random. | `0` to `1`                                      |

## Example: Override the Org-Level Default Model and Configure Temperature and Max Tokens

This example uses `model_config` to override the org-level default model for the agent, set the temperature for more varied answers, and limit responses to 2,000 tokens. You can use a `model_config` block to configure a subagent's model.

```sfdocs-code {"lang":"agentscript", "title": "Agent-Level Model Configuration"}
system:
    instructions: "You are an AI agent."
    messages:
        welcome: "Hi, I'm an AI service assistant. How can I help you?"
        error: "Sorry, it looks like something has gone wrong."
model_config:
    model: "model://sfdc_ai__DefaultBedrockAnthropicClaude45Haiku"
    params:
        temperature: 0.7
        max_tokens: 2000
```

## Supported Models

Specify any [supported model](https://developer.salesforce.com/docs/ai/agentforce/guide/supported-models.md). To test your model selections, use different models in different versions of your agent.

:::important
- We recommend that you use GPT 4.1 (`sfdc_ai__DefaultGPT41`), Claude Haiku 4.5 (`sfdc_ai__DefaultBedrockAnthropicClaude45Haiku`), or Gemini 3.5 Flash (`sfdc_ai__DefaultVertexAIGemini35Flash`) because we've thoroughly tested these models with agents.
- Thoroughly test your agent with your chosen model or models before deploying. Some supported models aren't suitable for your agent or its tools.
:::

## Multiple Models in an Agent

An agent can use different models for different subagents. A subagent-level model overrides the agent-level model, and an agent-level model overrides the org-level default.

### Example: Org, Agent, and Subagent Have Different Models

Suppose that your org, agent, and subagent specify these models:

- Your org uses the Salesforce default model.
- The MyTestAgent agent specifies Claude Haiku 4.5.
- The HandleReservation subagent specifies Gemini 3.1 Pro.

In this example, Agentforce uses Gemini 3.1 Pro for the HandleReservation subagent. For all other subagents in MyTestAgent, Agentforce uses Claude Haiku 4.5. For other agents in the same org, Agentforce uses the Salesforce default model.

## EinsteinHyperClassifier Model

Some agent templates, such as Agentforce Service agent, use the Salesforce-owned [EinsteinHyperClassifier](#einsteinhyperclassifier-model) model for subagent classification in the Agent Router. You can keep that model, or specify a different model in your Agent Router.

```sfdocs-code {"lang":"agentscript", "title": "Agent Router-Level Model Configuration"}
start_agent agent_router:
    description: "Welcome the user and determine the appropriate subagent based on user input"
    model_config:
        model: "model://sfdc_ai__DefaultGPT41"
```

Compared to other LLMs, Salesforce's EinsteinHyperClassifier offers these advantages for subagent classification:

- Faster subagent classification
- Higher classification accuracy, especially for specialized classification constraints and negative instructions

The EinsteinHyperClassifier model has these limitations:

- **Can't** use `before_reasoning` or `after_reasoning`
- **Can** use **only** the `@utils.transition` tool. It can't use other [tools](reference/ascript-ref-tools.md)

## Related Topics

- [Agent Script Reference](reference/ascript-reference.md)
- [Agent Script Blocks](ascript-blocks.md)
