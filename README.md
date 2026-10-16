# essential-skills

A collection of [Claude Code](https://claude.com/claude-code) **Agent Skills** — reusable, self-contained capabilities you can drop into your local Claude Code setup. New skills get added here over time.

A *skill* is a folder containing a `SKILL.md` (instructions + metadata) and any supporting scripts or assets. Claude Code discovers skills placed under a `skills/` directory in your config and invokes them when a task matches their description.

## Available skills

| Skill | What it does |
|-------|--------------|
| [`afagent-metadata-helper`](skills/afagent-metadata-helper) | Retrieves, deploys, and versions **Agentforce agents** as metadata. Picks between the v68 types (`AiAgentDefinition` / `AiAgentDefinitionVersion`) and the v67-and-earlier types (`Bot`, `BotVersion`, `GenAiPlannerBundle`, `AiAuthoringBundle`), resolves version naming, builds `package.xml` manifests, and separates **draft** deploys from **publish** (which commits a permanent version). Includes verified workarounds for CLI/doc gaps and known retrieve/deploy errors. |
| [`agentscript`](skills/agentscript) | Authoritative Salesforce Agent Script (AgentScript) language reference — syntax, blocks, flow of control, model configuration, voice/modality configuration, patterns, complete example agents, and agent metadata/package.xml deployment reference (API v68 and v67-earlier). Grounds any `.agent` file you write or review against correct syntax instead of relying on memory. |
| [`crafting-demo-data`](skills/crafting-demo-data) | Populates and refreshes Salesforce **demo** orgs with realistic, story-coherent data. CREATE new narrative-coherent records (schema-first, dependency-ordered, idempotent via External ID + upsert) or REFRESH stale data in place (roll close dates forward, re-time activities). Org-safety check refuses to write to production; every created record is tagged for clean teardown. |
| [`fetching-salesforce-docs`](skills/fetching-salesforce-docs) | Reliably retrieves official Salesforce documentation (developer.salesforce.com, help.salesforce.com, architect/admin, Lightning Design System), including JS-heavy and shell-rendered pages, via a browser-rendered extractor. Self-provisions an isolated Python + Playwright runtime on first use. |

## Install as a Claude Code plugin (recommended)

This repo is also a Claude Code plugin marketplace. Installing the `essential-skills` plugin adds **all four skills** at once, works the same on macOS, Windows, and Linux, and can be updated later with one command — no zips, hidden folders, or copying.

Inside Claude Code, run:

```
/plugin marketplace add salesforce-pixel/essential-skills
/plugin install essential-skills@essential-skills
```

On Claude Code 2.1.275 or later this also works as one step:

```
/plugin install essential-skills --marketplace salesforce-pixel/essential-skills
```

Restart Claude Code and the skills are available. Plugin skills are namespaced, so the slash commands become e.g. `/essential-skills:agentscript`; they still trigger automatically when a request matches.

**Updating:** run `claude plugin marketplace update essential-skills` and then `claude plugin update essential-skills@essential-skills` from a terminal, then restart Claude Code.

> If you previously copied any of these skills into `~/.claude/skills/` by hand, delete those folders after installing the plugin so you don't end up with each skill twice.

## Installing a skill manually

If you'd rather copy skill folders yourself (or only want some of them), use the options below.

Skills live in your Claude Code skills directory:

- **Personal (all projects):** `~/.claude/skills/`
- **Per-project (shared via your repo):** `<your-project>/.claude/skills/`

Pick whichever scope you want, then copy the skill folder(s) into it. Each subfolder under `skills/` in this repo is one installable skill.

### Install all skills globally — one line

Drops every skill in this repo into your personal (`~/.claude/skills/`) directory, available in every project:

```bash
mkdir -p ~/.claude/skills && \
curl -fsSL https://github.com/salesforce-pixel/essential-skills/archive/refs/heads/main.tar.gz \
  | tar -xz --strip-components=2 -C ~/.claude/skills essential-skills-main/skills
```

### Install a single skill globally — one line

Same idea, scoped to one skill folder. Example: `agentscript`.

```bash
mkdir -p ~/.claude/skills && \
curl -fsSL https://github.com/salesforce-pixel/essential-skills/archive/refs/heads/main.tar.gz \
  | tar -xz --strip-components=2 -C ~/.claude/skills essential-skills-main/skills/agentscript
```

> Replace `agentscript` with any other skill folder name from the table above (e.g. `afagent-metadata-helper`, `crafting-demo-data`, `fetching-salesforce-docs`).

Both one-liners are safe to re-run any time to update: they never touch other skills already in `~/.claude/skills/`, and they overwrite every file the new version ships with the latest content from `main`. The one thing plain `tar` extraction *doesn't* do is delete files a newer version removed — if a skill's file layout changes, a stale leftover file could remain alongside the new one. For a guaranteed byte-for-byte clean overwrite, use the `rsync --delete` option below instead.

### Other install options

<details>
<summary>Clone and copy with <code>rsync</code> (recommended if you're already cloning the repo)</summary>

```bash
# 1. Clone this repo somewhere
git clone https://github.com/salesforce-pixel/essential-skills.git
cd essential-skills

# 2. Make sure your skills directory exists
mkdir -p ~/.claude/skills

# 3. Copy the skill you want (example: agentscript)
#    --delete keeps the destination identical to the repo (clean install/overwrite)
rsync -a --delete --exclude='__pycache__' \
  skills/agentscript \
  ~/.claude/skills/
```

For a **per-project** install, swap the destination:

```bash
mkdir -p /path/to/your/project/.claude/skills
rsync -a --delete --exclude='__pycache__' \
  skills/agentscript \
  /path/to/your/project/.claude/skills/
```

To install **all** skills this way, loop over the skill folders so `--delete` only cleans inside each skill and never touches other skills you already have in `~/.claude/skills/`:

```bash
for s in skills/*/; do
  rsync -a --delete --exclude='__pycache__' "${s%/}" ~/.claude/skills/
done
```

> ⚠️ Don't run `rsync -a --delete skills/ ~/.claude/skills/` — with the trailing slash, `--delete` makes the destination mirror this repo and **removes every other skill** you have installed.
</details>

<details>
<summary>Manual copy</summary>

Download or clone the repo, then drag the desired folder(s) from `skills/` into `~/.claude/skills/` (or your project's `.claude/skills/`). Delete any `scripts/__pycache__` afterward — it's just generated bytecode.
</details>

For a **per-project** install with the one-liners above, swap `-C ~/.claude/skills` for `-C /path/to/your/project/.claude/skills` (after `mkdir -p`-ing it).

## Overwriting / updating an existing skill

If you already have an older copy of a skill, overwrite it so you get the latest version. Re-running either one-liner from above does this cleanly — it always pulls the current `main` and overwrites the destination. If you cloned the repo instead, `git pull` then re-run the `rsync ... --delete` command for the skill(s) you have installed, which removes stale files the new version dropped:

```bash
cd essential-skills && git pull
rsync -a --delete --exclude='__pycache__' skills/agentscript ~/.claude/skills/
```

**How to tell which version you have:** open the skill's `SKILL.md` and check `metadata.version` in the YAML frontmatter (e.g. `version: "2.0"` under `metadata:`). After overwriting, restart Claude Code so it re-reads the skill directory.

## Activating a skill in Claude Code

Once installed, Claude Code auto-discovers the skill and triggers it when your request matches its description. You can also invoke it explicitly with a slash command, e.g. `/agentscript` (or `/essential-skills:agentscript` when installed as a plugin).

## Requirements

Requirements are per-skill — see each skill's own `README.md` / `SKILL.md`. As a general note, skills that ship Python scripts (like `fetching-salesforce-docs`) provision their own isolated runtime under `~/.claude/` on first run and need `python3` plus internet access for that one-time setup; they do **not** touch your system or project Python.

## Contributing a new skill

1. Create a new folder under `skills/<your-skill-name>/`.
2. Add a `SKILL.md` with YAML frontmatter (`name`, `description`, and a `metadata.version`).
3. Keep scripts and assets inside that folder so the skill stays self-contained and portable (no hardcoded absolute paths).
4. Add the skill to the **Available skills** table above.
5. Open a PR.

## License

[MIT](LICENSE).
