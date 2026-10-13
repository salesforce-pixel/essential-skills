---
name: agentscript
description: >-
  Authoritative Salesforce Agent Script (AgentScript) language reference — syntax,
  keywords, blocks, flow of control, model configuration, patterns, complete example
  agents, and agent metadata/package.xml deployment reference. TRIGGER when writing,
  editing, reviewing, or debugging Agent Script / .agent files; looking up Agent
  Script syntax (subagents/topics, start_agent, reasoning, instructions, variables,
  actions, tools, utils, transitions, conditionals, action chaining, multi-turn
  flows, ask for (Beta), system and list variables, model_config, the runtime and
  file_upload config sub-blocks, and voice / modality configuration incl. the
  voice model catalog); or grounding generated Agent Script against correct syntax.
  Use ALONGSIDE the agentforce-adlc:developing-agentforce skill, which covers the
  ADLC workflow and CLI commands; this skill is the language grounding plus
  supporting metadata/deploy reference.
metadata:
  version: "2.0"
---

<!--
Changelog
2.0 — Full replace from the 2026-09-17 AgentScriptDocs.zip release (no diffing;
      the whole references/ tree was swapped for the new bundle, then images
      re-stripped to the placeholder convention and cross-folder links re-pointed
      for the flattened layout: agent-script/* → references/, agent-examples/ →
      references/examples/). Supersedes all 1.x notes below, incl. the 1.3
      dangling-link note (system variables now have their own page).
      • New: ascript-voice.md + ascript-voice-catalog*.md (5 files) — TTS voice
        models and persona IDs for `modality voice`.
      • New reference pages: ascript-ref-ask-for.md (Beta), ascript-ref-variables-
        system.md, ascript-ref-variables-list.md.
      • New examples: ascript-lead-gather.md, headless-example-org-build.md.
      • deploy-metadata: agent metadata changed in API v68. Old metadata.md and
        package-*.md replaced by agent-dx-api-v67-earlier.md and package-*67.md;
        agent-dx-deploy-metadata.md now covers v68.
1.3 — Page-level sync of 15 doc pages against the LIVE doc site (2026-08-24):
      ascript-blocks, ascript-model, ascript-flow, and all 12 patterns pages.
      This was NOT a full AgentScriptDocs.zip re-sync — every other file in the
      bundle still reflects the 2026-07-30 zip.
      • 14 of the 15 verified content-identical with upstream. The only deltas
        were doc-site serving artifacts (escaped "\&" in help.salesforce URLs,
        markdown table column padding, blank-line placement inside :::important),
        so those files were deliberately left untouched rather than churned.
      • references/ascript-blocks.md substantially expanded (+~135 lines):
        - New `runtime` config sub-block — `streaming`, `thought_chunks`,
          `citation`, `groundedness`, `reset_to_initial_node`.
        - New `file_upload` config sub-block — `mode` (auto / managed /
          disabled / error) plus `message`. `managed` is the mode that pairs
          with slice syntax on `@system_variables.uploaded_files`.
        - New top-level `modality voice:` block — `voice_id`, `outbound_speed`,
          `outbound_style_exaggeration`, `inbound_filler_words_detection`,
          `inbound_keywords`, `pronunciation_dict`, `outbound_filler_sentences`,
          and `additional_configs` (`speak_up_config`, `endpointing_config`,
          `beepboop_config`). Voice requires a deterministic locale — a
          `language` block with `adaptive: True` is ignored on voice channels.
        - Heading + anchor rename: "Connected_Subagent Blocks (Beta)" →
          "Connected Subagent Block (Beta)" (`#connected-subagent-block-beta`).
          No other file linked the old anchor.
      • v1.2's model_config correctness fix is RETIRED: upstream now ships the
        `model:` key correctly in all three examples, and local already matched.
        No local-vs-upstream divergence remains in ascript-model.md.
      • KNOWN DANGLING LINK: ascript-blocks.md now links to
        `reference/ascript-ref-variables.md#system_variablescurrent_modality`,
        but the local variables reference (still 2026-07-30) documents neither
        `@system_variables.current_modality` nor `@system_variables.uploaded_files`.
        Sync ascript-ref-variables.md to close this.
1.2 — Synced against the 2026-07-30 AgentScriptDocs.zip release.
      • New references/examples/apex-examples-custom-action.md — building a
        custom Apex retriever action and wiring it into an agent as a tool.
      • New references/examples/agent-examples.md — the examples hub/index
        (Apex + Agent Script examples), placed under references/examples/.
      • Terminology: "regular variable" renamed to "custom variable"
        (ascript-ref-variables.md, reference/ascript-reference.md, var-list).
      • `id` variable type deprecated → use `string`; conditionals now support
        `else if` (ascript-ref-expressions.md); new top-level `access` block and
        `visibility` variable property; `before_reasoning`/`after_reasoning`
        unavailable on EinsteinHyperClassifier; draft-vs-committed editability
        clarified in deploy-metadata/agent-dx-deploy-metadata.md.
      • Correctness fix: upstream ascript-model.md shipped 3 model_config
        examples missing the `model:` key (`model://…"` instead of
        `model: "model://…"`). Corrected to valid syntax here since this skill
        grounds *correct* syntax; worth reporting upstream via the doc-page feedback.
      • Image/media links re-stripped to the placeholder convention; example
        cross-links re-pointed for the flattened references/ layout.
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
(`AgentScriptDocs.zip`, last updated 2026-09-17), unzipped under `references/`.

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
- `references/ascript-blocks.md` — All block types: `system`, `config` (incl. the
  `runtime` and `file_upload` sub-blocks), `access`, `language`, `modality voice`,
  `variables`, `start_agent`, `subagent`, `connected_subagent` (Beta), `connection`,
  `reasoning`.
- `references/ascript-flow.md` — Flow of control: how reasoning loops, transitions, and deterministic execution interleave.
- `references/ascript-model.md` — `model_config`: overriding the org-default model per agent/subagent/router, multiple-model agents, `EinsteinHyperClassifier`.
- `references/ascript-manage.md` — Managing/lifecycle of Agent Script agents.
- `references/ascript-voice.md` — Configuring TTS voice models for voice agents (`modality voice`), per-language defaults.
- `references/ascript-voice-catalog.md` — Voice catalog index; per-model persona/Voice ID lists in `ascript-voice-catalog-v3-conversational.md`, `-flash-2.md`, `-flash-2-5.md`, `-kotoba.md`.

## Reference — syntax & semantics (`references/reference/`)

- `ascript-reference.md` — **Master syntax table** (every symbol/keyword) + concept index. Best first stop for "what does X mean / how do I write X."
- `ascript-ref-actions.md` — Actions: `run`, `@actions.*`, `@outputs.*`, `with` inputs, `target:` (flow://...), action chaining.
- `ascript-ref-tools.md` — Tools (reasoning actions) the LLM may call; `available when`; referencing a subagent as a tool.
- `ascript-ref-utils.md` — Built-in utils: `@utils.escalate`, `@utils.setVariables`, `@utils.transition to`.
- `ascript-ref-variables.md` — Variables: `mutable`, `linked`, slot-fill `...`, scope, declaration syntax.
- `ascript-ref-variables-system.md` — Read-only `@system_variables.*` (e.g. `current_modality`, `uploaded_files`).
- `ascript-ref-variables-list.md` — List variables: declaring, initializing, and working with lists.
- `ascript-ref-ask-for.md` — `ask for` (Beta): collect structured customer input one field at a time into variables.
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

- `references/ascript-examples.md` — Index of Agent Script examples (top-level).
- `references/examples/agent-examples.md` — Examples hub: Apex examples + Agent Script examples.
- `references/examples/apex-examples-custom-action.md` — Custom Apex retriever action (Apex class + wiring it into an agent as a tool).
- `references/examples/ascript-examples-customer-support.md` — Full customer-support agent.
- `references/examples/ascript-examples-multi-turn.md` — Multi-turn conversation agent.
- `references/examples/ascript-example-rag-jargon.md` — RAG / knowledge-grounded agent (largest, most complete example).
- `references/examples/ascript-lead-gather.md` — Collect customer info across turns, then create a record.
- `references/examples/headless-example-org-build.md` — End-to-end: use a coding agent + Salesforce skills to build an org and agent (Palonia Resort demo).

## Deploy metadata — agent metadata & package.xml (`references/deploy-metadata/`)

Supporting reference for the metadata *shape* behind an Agent Script agent — not the
ADLC workflow itself (still `developing-agentforce`'s job).

- `agent-dx-deploy-metadata.md` — Moving an agent between orgs via metadata (API v68+; both orgs must be on v68).
- `agent-dx-api-v67-earlier.md` — Agent metadata for API v67 and earlier: `AiAuthoringBundle` vs. `Bot`/`BotVersion`, draft vs. committed.
- `package-singleagent67.md` / `package-allagents67.md` — `package.xml` manifest examples, v67 and earlier (one agent vs. all agents).
- `package-single-mismatch67.md` — Draft/committed (Bot vs. AiAuthoringBundle) version mismatch, v67 and earlier.
- `string-replace-example.md` — String-replace pattern for environment-specific values during deploy.

## Working notes

- When generating Agent Script, prefer copying structure from `examples/` and confirming
  each keyword against `reference/ascript-reference.md`.
- `.agent` files in a Salesforce DX project live under an `aiAuthoringBundle`; use the
  developing-agentforce skill + `sf agent` CLI for generate/preview/publish/test/deploy.
- These docs are a local snapshot of the 2026-09-17 `AgentScriptDocs.zip`. If
  something looks newer in the org, trust the org and flag the discrepancy.
