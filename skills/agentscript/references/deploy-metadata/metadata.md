### Identify the Metadata for Your Agent

Before you list metadata in your `package.xml` manifest, identify your agent's stage. Different stages of an agent are represented by different metadata.

| Agent Stage         | Lifecycle                | Required Metadata                           |
| :------------------ | :----------------------- | :------------------------------------------ |
| Draft (uncommitted) | Save                     | `AiAuthoringBundle`                         |
| Committed           | Save → Commit → Activate | `AiAuthoringBundle` + `Bot` or `BotVersion` |
| Legacy              | Save → Activate          | `Bot` or `BotVersion`                       |

- **Draft (uncommitted) agent**: When you save a draft of an agent or agent version, Agentforce creates the agent's `AiAuthoringBundle`. A draft agent is editable until it's committed.
- **Committed agent**: When you commit an agent or agent version, Agentforce creates the `Bot` or `BotVersion`. A committed agent can't be changed; to change a committed agent, create a new version.
- **Legacy agent**: Legacy agents don't have a commit stage. You can edit and overwrite a published legacy agent or version. Legacy agents don't use `AiAuthoringBundle`.

For more details, see [Agent Metadata: A Shallow Dive](../agent-dx-metadata.md) and [Agentforce Metadata Types](/docs/ai/agentforce/references/agents-metadata-tooling/agents-metadata.html).

### Refresher: Agent and Legacy Agent Metadata

Draft, committed, and legacy agents are represented with different metadata.

- **Draft (uncommitted) agent version**: When you save a draft of an agent or agent version, Agentforce creates the agent's `AiAuthoringBundle`. To deploy a draft agent, deploy only the `AiAuthoringBundle`.

- **Committed agent version**: When you commit the agent or agent version, Agentforce creates the `Bot` or `BotVersion`. To deploy a committed agent or agent version, you must deploy `AiAuthoringBundle` **and** `Bot` or `BotVersion`.

- **Legacy Agent:** Legacy agents are represented with `Bot` or `BotVersion`. Legacy agents don't require `AiAuthoringBundle`.

#### Summary of Agent Metadata

| Agent Type                | AiAuthoringBundle | Bot or BotVersion |
| :------------------------ | :---------------- | :---------------- |
| Committed Agents          | yes               | yes               |
| Draft (uncommited) Agents | yes               | no                |
| Legacy Agents             | no                | yes               |

For more information on agent and legacy agent metadata, see [Agent Metadata: A Shallow Dive](../agent-dx-metadata.md) and [Agentforce Metadata Types](/docs/ai/agentforce/references/agents-metadata-tooling/agents-metadata.html).

### Refresher: Agent and Legacy Agent Lifecycle

To retrieve and deploy metadata for agents and legacy agents, you'll need to consider their lifecycles.

**Agents: Save, Commit, then Activate**

You can create and save multiple draft versions of an agent. Each agent version is editable until it's committed. After an agent or agent version is committed, you can't change it. To change a committed agent, you must create a new version. Committed agents are represented by additional metadata, as explained in [Refresher: Agent and Legacy Agent Metadata](#refresher-agent-and-legacy-agent-metadata).

**Legacy Agents: Save, then Activate**

Legacy agents don't have a commit stage. You can overwrite a published legacy agent or legacy agent version - just edit and save the agent or agent version.
