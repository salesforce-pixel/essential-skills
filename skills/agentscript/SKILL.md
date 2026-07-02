---
name: agentscript
description: >-
  Authoritative Salesforce Agent Script (AgentScript) language reference — syntax,
  keywords, blocks, flow of control, model configuration, patterns, complete example
  agents, and agent metadata/package.xml deployment reference. TRIGGER when writing,
  editing, reviewing, or debugging Agent Script / .agent files; looking up Agent
  Script syntax (subagents/topics, start_agent, reasoning, instructions, variables,
  actions, tools, utils, transitions, conditionals, action chaining, multi-turn
  flows, model_config); or grounding generated Agent Script against correct syntax.
  Use ALONGSIDE the agentforce-adlc:developing-agentforce skill, which covers the
  ADLC workflow and CLI commands; this skill is the language grounding plus
  supporting metadata/deploy reference.
metadata:
  version: "1.1"
---

<!--
Changelog
1.1 — Synced against the 2026-06-17 AgentScriptDocs.zip release.
      • New references/ascript-model.md — model_config (per-agent/per-subagent
        model overrides, EinsteinHyperClassifier notes).
      • New references/deploy-metadata/ — package.xml manifests and agent
        metadata (AiAuthoringBundle/Bot/BotVersion) reference, folded in
        alongside developing-agentforce's ADLC/CLI coverage rather than
        excluded, since users of this skill hit deploy-shape questions too.
      • references/ascript-examples.md promoted to top level (was nested under
        references/examples/), matching the upstream doc site's structure;
        the three example scripts themselves stay under references/examples/.
      • Refreshed all agent-script/, patterns/, and reference/ pages with the
        latest prose; doc-site images re-stripped to the placeholder convention.
1.0 — Initial import from AgentScriptDocs.zip (2026-05-25 release).
-->

# Agent Script Reference

Authoritative documentation bundle for **Salesforce Agent Script** (the language for
building Agentforce agents in Agentforce Builder). Source: official Salesforce docs
(`AgentScriptDocs.zip`, last updated 2026-06-17), unzipped under `references/`.

Use this to ground any Agent Script you write or review against correct syntax and
established patterns — do not rely on memory for syntax. Open the specific reference
file relevant to the task rather than loading everything.

> **Terminology:** As of April 2026, agent **topics** are now called **subagents**
> (`subagent` block; `topic` is deprecated). Docs may mix both terms.

## How to use this skill

1. Identify what you're doing (look up syntax? follow a pattern? start from an example?).
2. Open the matching file(s) below — start narrow, widen only if needed.
3. For division of labor with the ADLC skill: use **developing-agentforce** for the
   workflow/CLI/deploy steps; use **this** skill for "what's the correct Agent Script
   syntax / pattern for X."

## Start here (overview)

- `references/agent-script.md` — What Agent Script is, why determinism + LLM reasoning, a full minimal example.
- `references/ascript-lang.md` — Language characteristics: comments, indentation, the `->` (logic) vs `|` (prompt) distinction.
- `references/ascript-blocks.md` — All block types: `system`, `config`, `language`, `variables`, `start_agent`, `subagent`, `connection`, `reasoning`.
- `references/ascript-flow.md` — Flow of control: how reasoning loops, transitions, and deterministic execution interleave.
- `references/ascript-model.md` — `model_config`: overriding the org-default model per agent/subagent/router, multiple-model agents, `EinsteinHyperClassifier`.
- `references/ascript-manage.md` — Managing/lifecycle of Agent Script agents.

## Reference — syntax & semantics (`references/reference/`)

- `ascript-reference.md` — **Master syntax table** (every symbol/keyword) + concept index. Best first stop for "what does X mean / how do I write X."
- `ascript-ref-actions.md` — Actions: `run`, `@actions.*`, `@outputs.*`, `with` inputs, `target:` (flow://...), action chaining.
- `ascript-ref-tools.md` — Tools (reasoning actions) the LLM may call; `available when`; referencing a subagent as a tool.
- `ascript-ref-utils.md` — Built-in utils: `@utils.escalate`, `@utils.setVariables`, `@utils.transition to`.
- `ascript-ref-variables.md` — Variables: `mutable`, `linked`, slot-fill `...`, scope, declaration syntax.
- `ascript-ref-instructions.md` — Reasoning instructions: prompt vs logic instructions, `{!expression}` resolution.
- `ascript-ref-expressions.md` — Conditional expressions (`if`/`else`) for execution paths and utterances.
- `ascript-ref-operators.md` — Comparison/logical/arithmetic operators (`==`, `!=`, `is None`, etc.).
- `ascript-ref-before-after-reasoning.md` — `before_reasoning` / `after_reasoning` blocks.

## Patterns — how to do common things (`references/patterns/`)

- `ascript-patterns.md` — Index/overview of patterns.
- `ascript-patterns-topic-selector.md` — `start_agent` routing/classification to the right subagent.
- `ascript-patterns-transitions.md` — Moving between subagents (deterministic vs LLM-driven).
- `ascript-patterns-action-chaining.md` — Running actions in a controlled sequence.
- `ascript-patterns-conditionals.md` — Branching logic patterns.
- `ascript-patterns-variables.md` / `ascript-patterns-var-list.md` — Working with variables and list variables.
- `ascript-patterns-fetch-data.md` — Fetching data via actions and storing results.
- `ascript-patterns-filtering.md` — Filtering data/results.
- `ascript-patterns-required-flow.md` — Enforcing required steps before proceeding.
- `ascript-patterns-multi-turn.md` — Multi-turn conversation handling.
- `ascript-patterns-resource-references.md` — Referencing resources (`@subagent`, `@actions`, `@variables`).
- `ascript-patterns-system-overrides.md` — Overriding system instructions per subagent.

## Examples — complete agents

- `references/ascript-examples.md` — Index of examples.
- `references/examples/ascript-examples-customer-support.md` — Full customer-support agent.
- `references/examples/ascript-examples-multi-turn.md` — Multi-turn conversation agent.
- `references/examples/ascript-example-rag-jargon.md` — RAG / knowledge-grounded agent (largest, most complete example).

## Deploy metadata — agent metadata & package.xml (`references/deploy-metadata/`)

Supporting reference for the metadata *shape* behind an Agent Script agent — not the
ADLC workflow itself (still `developing-agentforce`'s job).

- `agent-dx-deploy-metadata.md` — Retrieving/deploying agent metadata between orgs; draft vs. committed vs. legacy agent handling.
- `metadata.md` — `AiAuthoringBundle` vs. `Bot`/`BotVersion` by agent lifecycle stage.
- `package-singleagent.md` / `package-allagents.md` — `package.xml` manifest examples (one agent vs. all agents).
- `package-single-mismatch.md` — Handling a draft/committed version mismatch when deploying.
- `string-replace-example.md` — String-replace pattern for environment-specific values during deploy.

## Working notes

- When generating Agent Script, prefer copying structure from `examples/` and confirming
  each keyword against `reference/ascript-reference.md`.
- `.agent` files in a Salesforce DX project live under an `aiAuthoringBundle`; use the
  developing-agentforce skill + `sf agent` CLI for generate/preview/publish/test/deploy.
- These docs are a local snapshot (2026-06-17). If something looks newer in the org,
  trust the org and flag the discrepancy.
