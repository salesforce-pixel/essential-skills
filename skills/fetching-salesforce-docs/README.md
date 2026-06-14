# fetching-salesforce-docs

## What it is

`fetching-salesforce-docs` is a **prompt-only skill**.

It gives a practical retrieval playbook for official Salesforce-owned docs on the public web, especially when:
- `developer.salesforce.com` pages are JS-heavy
- legacy `developer.salesforce.com/docs/atlas.*` guides don't render headless (AngularJS DocsApp)
- `help.salesforce.com` pages return shell content
- `architect.salesforce.com` / `admin.salesforce.com` pages need browser-rendered extraction
- `lightningdesignsystem.com` pages contain official SLDS guidance
- Salesforce-owned product docs are involved: MuleSoft (`*.mulesoft.com`), Tableau (`*.tableau.com`), Slack (`*.slack.com`, `*.slack.dev`), Heroku (`*.heroku.com`)
- the real answer is on a child page, not the guide homepage

## What it is not

This skill does not include:
- local corpus workflows
- indexing
- benchmark workflows
- any required helper CLI dependency
- PDF fallback guidance

## Use it for

- official Salesforce docs lookup
- hard-to-fetch Help articles
- Apex / API / LWC / Agentforce documentation grounding
- deciding when to follow child links from broad official guide pages
- rejecting weak results such as shells, landing pages, and third-party summaries

## Optional utility

A tiny wrapper is available for official Salesforce doc URLs:

```bash
python3 skills/fetching-salesforce-docs/scripts/extract_salesforce_doc.py \
  --url "https://help.salesforce.com/s/articleView?id=service.miaw_security.htm&type=5" \
  --pretty
```

Behavior:
- automatically routes by URL:
  - `help.salesforce.com` → the dedicated Help extractor
  - `developer.salesforce.com/docs/atlas.*` (legacy AngularJS guides) → the JSON content API the DocsApp itself uses, since these don't render headless
  - all other supported hosts → the browser-rendered extractor
- supports Salesforce-owned doc hosts: `developer.salesforce.com`, `help.salesforce.com`, `architect.salesforce.com`, `admin.salesforce.com`, `lightningdesignsystem.com`, plus Salesforce-owned product docs (`*.mulesoft.com`, `*.tableau.com`, `*.slack.com`, `*.slack.dev`, `*.heroku.com`)
- retries once automatically on a transient miss (e.g. a cold-load reCAPTCHA or late render), preferring stealth when available
- returns JSON with an `ok` flag — trust it; failed/empty/shell extractions come back `ok:false` (often with an `error`) rather than as a false-positive success
- supports optional best-effort stealth mode via `--stealth`

Dependencies for the helper scripts live in:
- `skills/fetching-salesforce-docs/requirements.txt`

The scripts run inside an isolated runtime under `~/.claude/.fetching-salesforce-docs-runtime` (a dedicated venv plus a Playwright Chromium browser), kept separate from system/project Python. No manual install is required: on first use the scripts **auto-provision** this runtime (create venv → install the packages from `requirements.txt` → `playwright install chromium`) and then re-exec themselves inside it. The first run takes a minute or two and logs progress to stderr; later runs are instant. To provision explicitly (or for offline/locked-down machines) run `scripts/setup_runtime.sh`. Set `SF_DOCS_RUNTIME_NO_PROVISION=1` to disable auto-provisioning.

The underlying Help extractor is also available directly at:

```bash
python3 skills/fetching-salesforce-docs/scripts/extract_help_salesforce.py \
  --url "https://help.salesforce.com/s/articleView?id=service.miaw_security.htm&type=5" \
  --pretty
```

## Key idea

Keep retrieval:
- **official-source-first**
- **HTML-only**
- **targeted**
- **child-link aware**
- **strict about exact concept matching**
