# Download Agent Script Documentation

Download the Agent Script documentation as Markdown files so your coding agents can reference correct syntax and patterns without web lookups. Use the files as grounding context for agentic coding tools, or search them locally. This download is updated weekly on Thursday evenings (PST), so download regularly to get the latest updates.


## Download and Set Up

1. Download the documentation bundle: [AgentScriptDocs.zip](https://resources.docs.salesforce.com/rel1/doc/en-us/static/misc/AgentScriptDocs.zip).
2. Unzip the file into your project workspace or the context source used by your coding agent.

## What's Included

The bundle contains Markdown files organized into these categories:

| Folder       | Contents                                                                                         |
| :----------- | :----------------------------------------------------------------------------------------------- |
| `root`       | Language overview, agent script blocks, model config, flow of control, managing your agent       |
| `reference/` | Syntax, keywords, and semantics for Agent Script features                                        |
| `patterns/`  | Solutions for common tasks like multi-turn conversations, action chaining, and conditional logic |
| `examples/`  | Complete agent implementations you can use as starting points                                    |

## Use with Coding Agents

Point your coding agent's context to the unzipped folder. For example, in a `CLAUDE.md` or similar context file:

```markdown
Reference the Agent Script documentation in ./docs/agent-script/ for syntax and patterns.
```

Your agent can then look up syntax in the reference files and follow established patterns when generating Agent Script code.

## See the Agentforce Development Skill

If you prefer a pre-packaged skill, use the [Agentforce Development Skill](https://github.com/forcedotcom/afv-library/tree/main/skills/developing-agentforce) to build, modify, debug, and deploy Agentforce agents with Agent Script. The Agentforce Development skill is part of the [Agentforce Vibes Library](https://github.com/forcedotcom/afv-library).
