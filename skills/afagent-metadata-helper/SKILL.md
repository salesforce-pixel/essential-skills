---
name: afagent-metadata-helper
description: >-
  Retrieve and deploy Agentforce agents (Agent Script and legacy) as metadata —
  choosing between the v68 types (AiAgentDefinition, AiAgentDefinitionVersion +
  --root-type-with-dependencies) and the v67-and-earlier types (Bot, BotVersion,
  GenAiPlannerBundle, AiAuthoringBundle, GenAiPlugin, GenAiFunction), building the
  right package.xml, resolving agent version naming (Agent.vN / Agent_vN / Agent_N /
  Agent#N), mapping AiAuthoringBundle versions to committed BotVersions, and
  working around known retrieve failures. TRIGGER when the user wants to retrieve,
  pull, download, move, migrate, promote, or deploy an Agentforce agent or agent
  version between orgs; asks which metadata types represent an agent; builds a
  package.xml for an agent; asks why an agent retrieve returned nothing or failed
  with UNKNOWN_EXCEPTION; or needs to find which retrieved bundle is the active
  version; deploys an agent change as a draft vs publishing/committing a new
  version; or asks why a version became Committed. DO NOT TRIGGER when writing or editing .agent Agent Script content (use
  agentscript / agentforce-adlc:agentforce-generate), testing agents
  (agentforce-adlc:agentforce-test), or retrieving/deploying non-agent metadata
  (use salesforce-development:platform-metadata-retrieve / platform-metadata-deploy
  directly).
metadata:
  version: "1.1"
---

<!--
Changelog
1.1 — Deploy findings (2026-10-13): deploy has no --root-type-with-dependencies
      (metadata-format staging workaround); active versions can't be redeployed;
      OutcomeBased billing/template rejection in a production target; botUser in
      two files; AiAgentDefinitionVersion <status>. Draft vs Commit: `sf agent
      publish` commits permanently (v4); deploying AiAuthoringBundle alone makes
      a draft (_5, no <target>). sourceApiVersion 68 makes the one-liner work.
1.0 — Initial version. Built from the Agentforce DX "Use Metadata to Move an Agent"
      docs (v68 and v67-and-earlier) plus behaviour observed retrieving
      Quick_Agentforce_Service_Agent from an org on API 68.0 with
      @salesforce/cli 2.152.14 / 2.153.5 (2026-10-13).
-->

# afagent-metadata-helper

Moves Agentforce agents between a Salesforce org and a local SFDX project as
metadata. It decides **which metadata model to use** (v68 vs v67-and-earlier),
builds the **manifest**, picks the **right version names**, and hands the
actual CLI call to the owning skill.

## Tool Routing (important)

This skill plans; it does not run raw CLI on its own.

| Step | Run through |
|---|---|
| `sf project retrieve start ...` | `salesforce-development:platform-metadata-retrieve` skill (invoke it first, then run the command) |
| `sf project deploy start ...` | `salesforce-development:platform-metadata-deploy` (or `platform-deploy-validate` for a production dry-run first) |
| Writing `package.xml` | Write tool, using the templates in `references/` |
| Reading `.agent` content | `agentscript` skill if you need language help |

A PreToolUse hook in Salesforce projects blocks raw `sf project retrieve/deploy`
calls that weren't made through those skills.

Always pass `--json`. Retrieve output reports `status: 0` even when the retrieve
**failed**. Check `result.status` (`Succeeded` / `Failed`), `result.errorMessage`
and each `result.files[].state` / `.error`.

## Step 1 — Pick the metadata model

```bash
sf org display --target-org <alias> --json      # result.apiVersion
grep sourceApiVersion sfdx-project.json
```

| Source org | Target org (deploy only) | Use |
|---|---|---|
| ≥ 68.0 | ≥ 68.0 (or retrieve only) | **v68 model** (Step 2A) |
| ≥ 68.0 | ≤ 67.0 | **v67 model** (Step 2B). Docs: keep using the old types until *both* orgs are on v68 |
| ≤ 67.0 | any | **v67 model** (Step 2B) |

The project's `sourceApiVersion` (66.0 in older projects) controls which model a
plain `--metadata` retrieve uses, **not** the org's version. Under 66.0 you get
Bot / GenAiPlannerBundle / AiAuthoringBundle even from a v68 org.

## Step 2A — v68 model (AiAgentDefinition)

**Either route works, but the one-liner needs `sourceApiVersion` ≥ 68.0 in `sfdx-project.json`.**

| Route | Project 66.0 | Project 68.0 |
|---|---|---|
| One-liner: `--metadata 'AiAgentDefinitionVersion:<Agent>#N' --root-type-with-dependencies AiAgentDefinitionVersion` | ❌ *"Entity type 'AiAgentDefinitionVersion' is not available in this api version"*, **even with `--api-version 68.0`** | ✅ verified |
| Manifest with `<version>68.0</version>` + same flag | ✅ verified | ✅ |

The one-liner brings back the `AiAgentDefinition`, the `AiAuthoringBundle`
and dependent flows automatically (same result as the manifest, observed
2026-10-13). So `--metadata 'AiAgentDefinitionVersion:<Agent>#N'` alone is enough
for a retrieve. Use a manifest for deploys and multi-agent sets.

Raising `sourceApiVersion` changes the default model for **every** plain
`--metadata`/`--source-dir` call in the project. Agents then come back as
AiAgentDefinition types, not Bot/GenAiPlannerBundle. If the project must
also deploy to a v67 org, keep 66/67 and use the manifest route instead.

| Type | Member syntax | Notes |
|---|---|---|
| `AiAgentDefinition` | `<Agent>` | Top-level agent. Must exist in target or ship in the same deploy |
| `AiAgentDefinitionVersion` | `<Agent>#3`, `<Agent>#*` (all versions), `*` (all agents) | At least one version is required when deploying `AiAgentDefinition` |
| `AiAuthoringBundle` | `<Agent>_N` (what the CLI writes in a generated `package.xml`) | **Required for Agent Script agents** |
| other (CustomObject, CustomField, Data 360 …) | explicit names | You must list these yourself |

Flows, Apex classes and prompt templates the agent uses are **not** listed. Pass
`--root-type-with-dependencies AiAgentDefinitionVersion` on the retrieve so the
correct versions come along automatically.

**`sf project deploy start` has no `--root-type-with-dependencies` flag**
(checked in CLI 2.153.5 / plugin-deploy-retrieve 4.2.2; only retrieve has it).
The docs' deploy command fails on this CLI. Verified workaround: retrieve in
**metadata format** into a staging folder outside the package dirs. The
CLI-generated `package.xml` then already lists every dependency. Deploy that
folder with `--metadata-dir`:

```bash
# 1. Retrieve agent + dependencies as a deployable mdapi package
sf project retrieve start --metadata 'AiAgentDefinitionVersion:<Agent>#N' \
  --root-type-with-dependencies AiAgentDefinitionVersion \
  --target-org <src> --target-metadata-dir deploy-staging --unzip --json
#    → deploy-staging/unpackaged/unpackaged/package.xml (+ aiAgents/, aiAgentDefinitionVersions/,
#      aiAuthoringBundles/<Agent>_N/, flows/, and a *.dependencies-meta.json the CLI adds)

# 2. Check the target org type (production → validate; otherwise dry-run)
~/.claude/plugins/cache/salesforce/salesforce-development/<ver>/scripts/sf-deploy-gate bucket <tgt>   # platform-deploy-validate runs this

# 3a. Non-production
sf project deploy start --dry-run --metadata-dir deploy-staging/unpackaged/unpackaged --target-org <tgt> --json
sf project deploy start          --metadata-dir deploy-staging/unpackaged/unpackaged --target-org <tgt> --json
# 3b. Production: validate (RunLocalTests) → platform-quick-deploy with the job id
sf project deploy validate --metadata-dir deploy-staging/unpackaged/unpackaged --target-org <tgt> --test-level RunLocalTests --json
```

Staging outside `force-app` also keeps legacy `BotVersion` files there out of
the package, which the deploy rules forbid mixing with the same version.

What comes back (observed, single version `#3`):
```
aiAgents/<Agent>.aiAgentDefinition-meta.xml          ← includes <botUser>
aiAgentDefinitionVersions/<Agent>#3/                 ← meta + agentScript/ + agentGraph/ + localActions/
aiAuthoringBundles/<Agent>_3/                        ← bundle renamed with the _N suffix
flows/<dependent flow>.flow-meta.xml                 ← pulled in by dependencies
```

Deploy rules:
- A version can't be deployed in the same package as its matching legacy `BotVersion` (docs).
- **An active version can't be redeployed** over itself. Observed: *"Can't edit an active bot version"* on `<Agent>#N`, even with identical content. To change a live agent, create a new version. Deploys are atomic, so this failure blocks the whole package.
- **Billing mode must be allowed in the target.** Observed in a production org: `billingMode` `OutcomeBased` → *"To enable outcome-based billing, specify a template. Outcome-based billing is supported for Help agents only"*. Valid values: `ActionBased`, `OutcomeBased`. Changing it changes how the agent is billed, so ask the user and don't switch it silently.
- When the version fails, two follow-on errors appear: *"AiAgentDefinition … cannot be created without at least one AiAgentDefinitionVersion"* and, on the bundle, *"no BotVersion named <Agent>.vN found"*. Fix the version error. The other two clear with it.
- After deploying, keep source and target versions in sync. If you create a version in the target, create the matching one in the source, or future deploys are blocked (docs).
- A full successful cross-org deploy hasn't been observed yet. The checks above all come from validations and dry-runs.

Templates: `references/v68-manifests.md`.

## Step 2B — v67-and-earlier model (Bot / BotVersion / bundles)

### What represents an agent

| Agent state | Metadata | Editable |
|---|---|---|
| Draft (saved, not committed) | `AiAuthoringBundle` only | Yes |
| Committed | `AiAuthoringBundle` + `Bot` + `BotVersion` (+ `GenAiPlannerBundle`) | No. Create a new version |
| Legacy (pre-Agent Script) | `Bot` + `BotVersion` | Inactive versions only |

### Version naming (non-obvious)

| Type | Version N of agent `MyAgent` | Example |
|---|---|---|
| `Bot` | `MyAgent` (no version) | `Quick_Agentforce_Service_Agent` |
| `BotVersion` | `MyAgent.vN` | `Quick_Agentforce_Service_Agent.v3` |
| `GenAiPlannerBundle` | `MyAgent_vN` | `Quick_Agentforce_Service_Agent_v3` |
| `AiAuthoringBundle` | `MyAgent_N` (saved-version number) | `Quick_Agentforce_Service_Agent_2` |

**Don't infer versions from bundle folder names. Read the bundle's `<target>`.**
- `aiAuthoringBundles/<name>/<name>.bundle-meta.xml` → `<target>MyAgent.v7</target>` names the BotVersion / GenAiPlannerBundle it maps to.
- Saved versions outnumber committed ones when drafts were saved but not committed (e.g., bundle `_9` → `v7`).
- **Under API 66, one bundle comes back unsuffixed** (`MyAgent`, not `MyAgent_N`). Observed: `Quick_Agentforce_Service_Agent` targeted `.v3`, while `_1` → `.v1` and `_2` → `.v2`. In that org v3 was both the newest and the active version, so it's not established whether "unsuffixed" means newest or active. Read `<target>`. Under API 68, every bundle comes back suffixed (`_1` … `_N`). The same v3 bundle came back as `_3`, with byte-identical `.agent` content.
- A bundle **with** `<target>` is a committed version's source. A bundle **without** `<target>` is a draft.
- `BotVersion` XML → `<conversationDefinitionPlanners><genAiPlannerName>` gives the planner bundle name.
- Active version: neither `Bot` nor `BotVersion` XML has an active/status field (checked). In the v68 model, `AiAgentDefinitionVersion` XML has `<status>Active</status>`, so retrieve that to check. Otherwise confirm in Setup / Agent Builder.

### Retrieval recipes (v67 model)

| Goal | Command (`--metadata` …) | Result (observed) |
|---|---|---|
| The agent's Agent Script source, all saved versions | `'AiAuthoringBundle:<Agent>*'` (prefix wildcard, quoted) | ✅ `<Agent>`, `<Agent>_1`, `<Agent>_2` … only that agent |
| One bundle | `AiAuthoringBundle:<Agent>` (or `<Agent>_N`), **in its own call** | ✅ |
| Bot + all versions | `'BotVersion:<Agent>.*'` | ✅ Bot + v1, v2, v3 |
| Bot only | `Bot:<Agent>` | ⚠ Bot + only one BotVersion (v3, the newest and active one there), not all versions |
| Planner for version N | `GenAiPlannerBundle:<Agent>_vN` (exact name) | ✅ includes agentScript/, agentGraph/, localActions/ schemas |
| Planner by wildcard | `'GenAiPlannerBundle:<Agent>*'` | ⚠ returned nothing (in a combined call) |
| Everything in one shot | `Agent:<Agent>` | ❌ UNKNOWN_EXCEPTION (see Troubleshooting) |
| Bot + dependencies | `Bot:<Agent> --root-type-with-dependencies Bot` | ❌ same UNKNOWN_EXCEPTION |

For deploys, use a manifest (`references/v67-manifests.md`) and list
GenAiPlugin, GenAiFunction, Apex, Flow and GenAiPromptTemplate explicitly.

**Tip: finding dependency names.** If the source org is on v68, run the v68
dependency retrieve (Step 2A) into a throwaway `--output-dir` and read off the
Flow/Apex/prompt-template names. That's how
`Quick_Agentforce_Service_Agent_Outbound_Messaging_Flow` was found. None of the
v67-model retrieves surfaced it.

Deploy rules (from the docs; deploy **not exercised** here):
- Deploy the **full agent** (all-agents / Bot-level manifest) to an org before deploying a single `BotVersion` into it.
- **Don't wildcard** `ApexClass`, `Flow` or `GenAiPromptTemplate` in real orgs. Name the ones the agent uses, or the deploy can time out.

## Changing an agent in the same org: Draft vs Commit (verified)

Committed or active versions can't be redeployed (*"Can't edit an active bot
version"*). Changes go into a **new version**, made one of two ways. **Ask the
user which one they want before running anything:**

| Want | Command | Result in org | Reversible? |
|---|---|---|---|
| **Draft** (test/iterate, nothing committed) | `sf project deploy start --metadata AiAuthoringBundle:<Agent> --target-org <org> --json` | New saved version, e.g. `<Agent>_5`, **no `<target>`**. Editable in Agent Builder. No `AiAgentDefinitionVersion` created | Yes. Keep editing and redeploying |
| **Committed** version | `sf agent publish authoring-bundle --api-name <Agent> --target-org <org> --json` | Deploys the bundle **and commits** `#N+1` (`AiAgentDefinitionVersion` + a bundle `<Agent>_N` with `<target><Agent>.vN</target>`). Created **Inactive** | **No.** It can't be turned back into a draft. Deletion is unverified |
| Go live | `sf agent activate --api-name <Agent> --version <N> --target-org <org> --json` | Switches the active version | Re-activate the old version |

**"Publish" means "commit".** `sf agent publish` doesn't just upload. It
commits a permanent version in one step, even though the result shows only
"Inactive". Never use it when the user only asked to "deploy" or "test".

Verified sequence (2026-10-13, `partnerBootcamp2026`): v3 active →
`publish` created committed **#4** (Inactive) → deploying the bundle alone
created draft **`_5`** (no target), with committed versions still #1–#4.

```bash
# Draft workflow (default for testing)
#   edit force-app/main/default/aiAuthoringBundles/<Agent>/<Agent>.agent
sf agent validate authoring-bundle --api-name <Agent> --target-org <org> --json   # server compile check
sf project deploy start --dry-run --metadata AiAuthoringBundle:<Agent> --target-org <org> --json
sf project deploy start          --metadata AiAuthoringBundle:<Agent> --target-org <org> --json
#   preview/test the draft (agentforce-adlc:agentforce-test / sf agent preview)
#   then, only when the user explicitly approves: publish → activate
```

How to check version state (v68 model):
```bash
sf project retrieve start --metadata 'AiAuthoringBundle:<Agent>*' --output-dir tmp_check --json
#   each bundle-meta.xml: <target><Agent>.vN</target> = committed as vN; no <target> = draft
sf project retrieve start --metadata 'AiAgentDefinitionVersion:<Agent>#*' --output-dir tmp_check --json
#   each version XML: <status>Active|Inactive</status>. Only committed versions appear here
```

Side effects and gotchas:
- **Local bundle name ≠ org bundle name.** Deploying the unsuffixed local `aiAuthoringBundles/<Agent>/` creates the *next* numbered bundle in the org (`<Agent>_5`). Under `sourceApiVersion` 68.0, a retrieve returns only suffixed bundles (`_1` … `_5`).
- **Publish rewrites the local project.** It retrieves `aiAgents/`, `aiAgentDefinitionVersions/<Agent>#N/`, the dependent flows, and rewrites `<Agent>.bundle-meta.xml` with **no `<target>`** (ready for the next draft). Pass `--skip-retrieve` to prevent this.
- **Hooks.** Raw `sf agent publish` (even `--help`) is blocked unless it goes through `agentforce-adlc:agentforce-generate`. Bundle deploys go through `platform-metadata-deploy`. List command flags with `sf commands --json`.
- **Billing/template.** `config.agent_template` (e.g. `"QuickASA__QuickASA"`, from a managed package) and `config.billing.mode` in the `.agent` drive `billingMode`. A target org without that package can reject `OutcomeBased` billing.

## Step 3 — Before deploying (both models)

1. **Agent user.** Retrieved metadata carries the source org's agent username in **two places**: `<botUser>` in `AiAgentDefinition` (or `Bot`), **and** `default_agent_user:` in the bundle's `.agent` file. Replace both, or neither. Check that the target has that user first. Einstein Agent users are those with Profile `Einstein Agent User`. For **draft** agents, use SFDX [string replacement](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_ws_string_replace.htm) in `sfdx-project.json` to swap it for the target org's user. Committed agents can't be edited, so assign the user on a new version in the target after deploying.
2. **Don't hand-edit other retrieved agent metadata.** The docs warn that deploying edited metadata can corrupt the org. Make Agent Script changes in the `.agent` file of an `AiAuthoringBundle`, never in the planner's `agentScript/` copy.
3. Agent user permissions: give the agent user access to every object/field its actions touch.
4. Production: validate first (`platform-deploy-validate`), then `platform-quick-deploy`.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `result.status: Failed`, `UNKNOWN_EXCEPTION … ErrorId …` on `Agent:<Agent>` or `Bot:<Agent> --root-type-with-dependencies Bot` | Server-side failure resolving Bot dependencies. Observed on an API 68 org with CLI 2.152.14 **and** 2.153.5. Retrieve the parts separately (recipes above) or use the v68 manifest route. Re-test after CLI or org upgrades |
| Combined call (`Bot:X` + `'GenAiPlannerBundle:X*'` + `AiAuthoringBundle:X`) "Succeeded" but returned only Bot/BotVersion | Observed once; the same `AiAuthoringBundle:X` alone succeeded. Retrieve `AiAuthoringBundle` in its own call and use exact `GenAiPlannerBundle` names |
| `Entity type 'AiAgentDefinitionVersion' is not available in this api version` | Project `sourceApiVersion` < 68 and `--metadata` was used (`--api-version 68.0` does not help). Raise `sourceApiVersion` to 68.0 (verified fix), or use a `<version>68.0</version>` manifest |
| `'AiAuthoringBundle:*'` pulled in many unrelated agents | Use a prefix: `'AiAuthoringBundle:<Agent>*'`. Delete stray folders you just created |
| Unsure which bundle is the live agent | Read each `bundle-meta.xml` `<target>` and match it to the active BotVersion |
| Deploy blocked after editing in the target org | Source and target agent versions diverged. Recreate the matching version in the source |
| Single `BotVersion` deploy fails on a fresh org | Deploy the full agent first |
| `Nonexistent flag: --root-type-with-dependencies` (or flag missing) on deploy | Deploy doesn't support it. Use the metadata-format staging workflow in Step 2A |
| `Can't edit an active bot version` | Target already has that version active. Create a new version, or deploy to an org without it |
| `To enable outcome-based billing, specify a template…` | Target won't accept `billingMode` `OutcomeBased` for this agent. Ask the user before switching to `ActionBased` |
| User wanted a draft but the version shows **Committed** in Agent Builder | `sf agent publish` was used, and it commits. It can't be reverted. Deploy the `AiAuthoringBundle` alone to start a new draft on top |
| Hook blocks `sf agent publish --help` | Use `sf commands --json` to read flags, and run publish via `agentforce-adlc:agentforce-generate` |

## Output

Report: which model was used and why (org/project API versions); each retrieved
component with its version mapping (bundle → `<target>` → planner); anything
skipped or failed with its `errorMessage`/ErrorId; and any stray files cleaned up.

## Sources

- [Use Metadata to Move an Agent to a New Org (v68)](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-dx-deploy-metadata.md)
- [Define Agent Metadata (v67 and Earlier)](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-dx-api-v67-earlier.md)
- [Manifest Defining All Agents (v67)](https://developer.salesforce.com/docs/ai/agentforce/guide/package-allagents67.md) · [Single Agent Version (v67)](https://developer.salesforce.com/docs/ai/agentforce/guide/package-singleagent67.md) · [Different Bot/AiAuthoringBundle Versions (v67)](https://developer.salesforce.com/docs/ai/agentforce/guide/package-single-mismatch67.md)
- [AiAuthoringBundle metadata type](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_aiauthoringbundle.htm)

The `.md` doc URLs return raw markdown with `curl -sL`.

## Reference File Index

| File | When to read |
|---|---|
| `references/v68-manifests.md` | Building a v68 manifest (all versions / specific versions / all agents) |
| `references/v67-manifests.md` | Building a v67 manifest (all agents / single version / mismatched bundle vs BotVersion) |
