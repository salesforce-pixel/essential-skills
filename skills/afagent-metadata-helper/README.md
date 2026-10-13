# afagent-metadata-helper

A [Claude Code](https://claude.com/claude-code) **Agent Skill** for retrieving, deploying, and versioning **Agentforce agents** (Agent Script and legacy) as Salesforce metadata.

Agent metadata is easy to get subtly wrong. The type model changed in API v68, version names differ across four metadata types, and some CLI commands in the official docs don't behave as written. This skill puts together the official Agentforce DX guidance and behaviour verified against a real org, so Claude picks the right types, names, and commands the first time.

## What it covers

- **Picking the metadata model.** The v68 types (`AiAgentDefinition`, `AiAgentDefinitionVersion` + `--root-type-with-dependencies`) vs the v67-and-earlier types (`Bot`, `BotVersion`, `GenAiPlannerBundle`, `AiAuthoringBundle`, `GenAiPlugin`, `GenAiFunction`), based on the source/target org versions *and* the project's `sourceApiVersion`.
- **Version naming.** `Agent.vN` / `Agent_vN` / `Agent_N` / `Agent#N`, plus how to map an `AiAuthoringBundle` to its committed version via `<target>`.
- **Draft vs Commit.** Deploying the `AiAuthoringBundle` alone creates an editable **draft**. `sf agent publish` **commits** a permanent version, and it can't be undone. Includes how to check which versions are draft, committed, or active.
- **Moving an agent to another org.** A verified workaround for `sf project deploy start` not supporting `--root-type-with-dependencies`: retrieve in metadata format and deploy the CLI-generated `package.xml`. Covers production validation and agent-user replacement (it lives in two files).
- **Manifests.** Ready-to-use `package.xml` templates for v68 and v67, with an invalid snippet from the official docs fixed.
- **Troubleshooting.** `UNKNOWN_EXCEPTION` on `Agent:` / `Bot` dependency retrieves, *"not available in this api version"*, *"Can't edit an active bot version"*, outcome-based billing rejections, and more. Each entry says whether it was verified in an org or comes from the docs.

## Scope

| In scope | Out of scope |
|---|---|
| Retrieve / deploy / publish / activate planning for Agentforce agents | Writing or editing `.agent` Agent Script (use [`agentscript`](../agentscript) or `agentforce-adlc:agentforce-generate`) |
| Agent `package.xml` manifests (v68 and v67) | Agent testing (`agentforce-adlc:agentforce-test`) |
| Draft vs committed version workflows | Non-agent metadata deploys (use the standard retrieve/deploy skills) |

The skill plans and picks commands. Actual `sf project retrieve/deploy` and `sf agent publish` calls are routed through the Salesforce plugin skills (`platform-metadata-retrieve`, `platform-metadata-deploy`, `platform-deploy-validate`, `agentforce-adlc:agentforce-generate`) when they're installed.

## Install

This skill is pure Markdown, with no scripts and no runtime to provision. Installing it means copying the `afagent-metadata-helper/` folder into a Claude Code **skills directory**:

- **Personal** (available in every project): `~/.claude/skills/`
- **Per-project** (shared with your team via the project repo): `<your-project>/.claude/skills/`

### Option A: one-liner without cloning

```bash
mkdir -p ~/.claude/skills && \
curl -fsSL https://github.com/salesforce-pixel/essential-skills/archive/refs/heads/main.tar.gz \
  | tar -xz --strip-components=2 -C ~/.claude/skills \
      essential-skills-main/skills/afagent-metadata-helper
```

### Option B: clone and copy

```bash
# 1. Clone the skills repo
git clone https://github.com/salesforce-pixel/essential-skills.git
cd essential-skills

# 2. Ensure your skills directory exists
mkdir -p ~/.claude/skills

# 3. Copy this skill in (--delete keeps it identical to the repo on re-installs)
rsync -a --delete skills/afagent-metadata-helper ~/.claude/skills/
```

For a **per-project** install, swap the destination:

```bash
mkdir -p /path/to/your/project/.claude/skills
rsync -a --delete skills/afagent-metadata-helper /path/to/your/project/.claude/skills/
```

### After installing

Restart Claude Code (or start a new session) so it re-scans the skills directory. Claude then **auto-triggers** the skill when a request matches its description, for example:

- *"Retrieve the Quick_Agentforce_Service_Agent from my org"*
- *"Move this agent from my sandbox to production"*
- *"Deploy my agent change as a draft, don't publish it"*
- *"Why did my agent retrieve fail with UNKNOWN_EXCEPTION?"*

You can also invoke it explicitly: `/afagent-metadata-helper`.

### Updating

```bash
cd essential-skills && git pull
rsync -a --delete skills/afagent-metadata-helper ~/.claude/skills/
```

Check which version you have in `SKILL.md` → `metadata.version`, and the changelog comment just below the frontmatter.

## Files

```
afagent-metadata-helper/
├── SKILL.md                      # model selection, naming, draft vs commit, deploy workflow, troubleshooting
├── README.md
└── references/
    ├── v68-manifests.md          # AiAgentDefinition / AiAgentDefinitionVersion manifests + worked example
    └── v67-manifests.md          # Bot / BotVersion / GenAiPlannerBundle / AiAuthoringBundle manifests
```

## Requirements

- Salesforce CLI (`sf`) v2 with an authenticated org. Verified with `@salesforce/cli` 2.153.5 against an API 68.0 org.
- An Agentforce-enabled org (Einstein + Agentforce turned on, an Einstein Agent User for service agents).
- Recommended: the Salesforce Claude Code plugins (`salesforce-development`, `agentforce-adlc`) for the retrieve/deploy/publish skills this one routes to.

## License

MIT
