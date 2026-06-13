# crafting-demo-data

A [Claude Code](https://claude.com/claude-code) **Agent Skill** that helps Solution Engineers populate and maintain Salesforce **demo** orgs with realistic, story-coherent data — and keep it fresh.

It reads the object schema first (so records don't bounce off required fields, picklists, or validation rules), builds a dependency-ordered plan, previews it, then drives the `sf data` CLI to create or refresh records — tagging everything it creates so it can be cleanly removed later.

## Two modes

- **CREATE** — generate new, narrative-coherent demo records (dependency-ordered, schema-valid, tagged for teardown).
- **REFRESH** — update *existing* stale demo data in place: roll past close dates forward, re-time old activities, re-randomize values. No new rows, no broken relationships.

## What makes it more than a record generator

- **Schema-first** — required/createable fields, picklists, record types, **and validation rules** read before any value is generated.
- **Dependency ordering** — parents before children, via `sf data import tree` reference IDs or staged bulk loads.
- **Coherence** — dates relative to "today", consistent geography/currency, dashboard-believable distributions.
- **Refresh-in-place** — fix a stale demo org without re-seeding it.
- **Demo-safe teardown** — every created record is tagged; one command removes exactly what was made.
- **Org guardrails** — refuses to silently write to production.

## Scope

| In scope | Out of scope |
|---|---|
| Demo/POC data CREATE + REFRESH via `sf data` | Apex `TestDataFactory` / unit-test fixtures (use `handling-sf-data`) |
| Schema discovery, dependency ordering, teardown | Creating objects/fields (use `generating-custom-object` / `-field`) |
| Industry scenario templates | Production data migration |

## Install

This skill is pure Markdown — no scripts, no runtime to provision. Installing it means copying the `crafting-demo-data/` folder into a Claude Code **skills directory**:

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
rsync -a --delete skills/crafting-demo-data ~/.claude/skills/
```

For a **per-project** install, swap the destination:

```bash
mkdir -p /path/to/your/project/.claude/skills
rsync -a --delete skills/crafting-demo-data /path/to/your/project/.claude/skills/
```

### Option B — one-liner without cloning

```bash
mkdir -p ~/.claude/skills && \
curl -fsSL https://github.com/salesforce-pixel/essential-skills/archive/refs/heads/main.tar.gz \
  | tar -xz --strip-components=2 -C ~/.claude/skills \
      essential-skills-main/skills/crafting-demo-data
```

### After installing

Restart Claude Code (or start a new session) so it re-scans the skills directory. Claude then **auto-triggers** the skill when a request matches its description (e.g. *"freshen up the stale opportunities"*, *"create some demo accounts with contacts and opps"*). You can also invoke it explicitly: `/crafting-demo-data`.

### Updating

```bash
cd essential-skills && git pull
rsync -a --delete skills/crafting-demo-data ~/.claude/skills/
```
Check the version you have in `SKILL.md` → `metadata.version` (and the changelog comment just below the frontmatter).

## Files
```
crafting-demo-data/
├── SKILL.md
├── README.md
└── references/
    ├── schema-discovery.md        # describe + validation rules + dependency graph
    ├── generating-data.md         # CREATE: coherence rules + mechanism recipes
    ├── refreshing-stale-data.md   # REFRESH: in-place update playbook
    ├── teardown-and-safety.md     # org-type check + tagged teardown
    └── scenario-templates.md      # industry/vertical demo stories
```

## Requirements
- Salesforce CLI (`sf`) with an authenticated org
- `jq` (for parsing describe output)

## License
MIT
