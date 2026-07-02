# agentscript

A [Claude Code](https://claude.com/claude-code) **Agent Skill** that bundles the official Salesforce **Agent Script** developer documentation as a local, always-available reference — so agent scripts get grounded against real syntax instead of memory.

## What it is

`agentscript` is a documentation-bundle skill (prompt-only reference, no scripts). It ships the official Agent Script docs (language reference, blocks, flow of control, model configuration, patterns, complete example agents, and agent metadata/`package.xml` deployment reference) under `references/`, sourced from Salesforce's `AgentScriptDocs.zip` releases.

Use it alongside the `agentforce-adlc:developing-agentforce` skill, which covers the ADLC workflow and CLI commands — `agentscript` is the language grounding plus supporting metadata/deploy reference.

## Use it for

- Writing, editing, reviewing, or debugging Agent Script / `.agent` files
- Looking up exact syntax: `subagent`/topic blocks, `start_agent`, reasoning, variables, actions, tools, utils, transitions, conditionals, action chaining, multi-turn flows, `model_config`
- Grounding generated Agent Script against correct syntax before shipping it
- Looking up the metadata shape (`AiAuthoringBundle`, `Bot`/`BotVersion`) and `package.xml` manifests behind an agent, when you need the *shape* rather than the full deploy workflow

## Files

```
agentscript/
├── SKILL.md
├── README.md
└── references/
    ├── agent-script.md                  # What Agent Script is, minimal example
    ├── ascript-lang.md                  # Language characteristics
    ├── ascript-blocks.md                # All block types
    ├── ascript-flow.md                  # Flow of control
    ├── ascript-model.md                 # model_config: per-agent/subagent model overrides
    ├── ascript-manage.md                # Managing/lifecycle of agents
    ├── ascript-examples.md              # Index of example agents
    ├── ascript-download-documentation.md
    ├── examples/                        # Complete example agent scripts
    ├── patterns/                        # Common Agent Script patterns
    ├── reference/                       # Master syntax & keyword reference
    └── deploy-metadata/                 # Agent metadata & package.xml reference
```

## Install

This skill is pure Markdown — no scripts, no runtime to provision. Installing it means copying the `agentscript/` folder into a Claude Code **skills directory**:

- **Personal** (available in every project): `~/.claude/skills/`
- **Per-project** (shared with your team via the project repo): `<your-project>/.claude/skills/`

### Option A — clone and copy (recommended)

```bash
# 1. Clone the skills repo
git clone https://github.com/salesforce-pixel/essential-skills.git
cd essential-skills

# 2. Ensure your skills directory exists
mkdir -p ~/.claude/skills

# 3. Copy this skill in (--delete keeps it identical to the repo on re-installs)
rsync -a --delete skills/agentscript ~/.claude/skills/
```

For a **per-project** install, swap the destination:

```bash
mkdir -p /path/to/your/project/.claude/skills
rsync -a --delete skills/agentscript /path/to/your/project/.claude/skills/
```

### Option B — one-liner without cloning

```bash
mkdir -p ~/.claude/skills && \
curl -fsSL https://github.com/salesforce-pixel/essential-skills/archive/refs/heads/main.tar.gz \
  | tar -xz --strip-components=2 -C ~/.claude/skills \
      essential-skills-main/skills/agentscript
```

### After installing

Restart Claude Code (or start a new session) so it re-scans the skills directory. Claude then **auto-triggers** the skill when a request matches its description (e.g. *"write an Agent Script topic that transitions to another subagent"*, *"what's the syntax for model_config"*). You can also invoke it explicitly: `/agentscript`.

### Updating

```bash
cd essential-skills && git pull
rsync -a --delete skills/agentscript ~/.claude/skills/
```
Check the version you have in `SKILL.md` → `metadata.version` (and the changelog comment just below the frontmatter).

## Requirements

None — this skill is a documentation bundle only.

## License
MIT
