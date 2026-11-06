# Rendering Widgets in Claude / ChatGPT / Slackbot (MCP)

HXL widgets follow the **MCP Apps** standard, so any MCP Apps–compatible client can render them. You need a **custom** Salesforce hosted MCP server (the standard ones can't carry your widget resource).

## Flow

```
Apex @InvocableMethod ─► MCP tool (Setup) ─► McpServerDefinition: <tools><uiResource> → <resources> ui://widget/lightningType/c__<wrapperCLT>
                                                                   │
                                           wrapper CLT renderer.json ─► @widget/c/<widget>
```

## 1. Apex invocable action
- `global` class, `@InvocableMethod`, output shaped to the payload CLT. Template: `templates/apex/AccountHealthService.cls`.
- Include display-ready fields (labels, variants/colors, fallback text, booleans). The widget can't compute them with formulas in this channel (see `composition.md`).
- Deploy it **before** the admin creates the MCP tool. Setup can only list Apex actions that already exist in the org.
- `sf project deploy start --metadata ApexClass:AccountHealthService --target-org <alias>`
- Confirm the output: `POST /services/data/v67.0/actions/custom/apex/<Class>` with `{"inputs":[{...}]}` (see SKILL.md Step 4).

## 2. Custom MCP server
1. Setup → Quick Find `MCP` → **API Catalog → MCP Servers** → **Add MCP Server** → Create. Note the server URL, e.g. `https://api.salesforce.com/platform/mcp/v1/custom/<ServerApiName>`.
2. **Add Server Assets → Add Tools** → *Apex actions* → pick the action → **+ Add Tool** → Save.
3. Setup can't add HXL resources yet. Retrieve the metadata:
   ```bash
   sf project retrieve start --metadata McpServerDefinition:<ServerApiName> --target-org <alias>
   ```
   → `force-app/main/default/mcpServerDefinitions/<ServerApiName>.mcpServerDefinition-meta.xml`
4. Edit the retrieved file — **merge into it; never author it from scratch**:
   - Add a `<resources>` element **alongside** `<tools>` with `<resourceName>`, `<resourceUri>`, `<resourceTitle>`, `<description>`.
   - `<resourceUri>` = `ui://widget/lightningType/c__<wrapperCltApiName>` (the **wrapper** CLT, e.g. `c__accountHealthResult`).
   - Inside the tool's `<tools>` element add `<uiResource>` whose value **exactly equals** `<resourceName>`.

   Verified-working layout (deployed and round-tripped 2026-09-21). Children are in alphabetical order: `<resources>` before `<tools>`, and `<uiResource>` last inside `<tools>`:
   ```xml
   <McpServerDefinition xmlns="http://soap.sforce.com/2006/04/metadata">
       <description>…</description>
       <masterLabel>…</masterLabel>
       <resources>
           <description>Renders account health as an HXL widget</description>
           <resourceName>accountHealthCard</resourceName>
           <resourceTitle>Account Health Card</resourceTitle>
           <resourceUri>ui://widget/lightningType/c__accountHealthResult</resourceUri>
       </resources>
       <tools>
           <apiDefinition>…retrieved, unchanged…</apiDefinition>
           <descriptionOverride>…</descriptionOverride>
           <destructive>false</destructive>
           <idempotent>true</idempotent>      <!-- true for read-only lookups -->
           <openWorld>false</openWorld>
           <readOnly>true</readOnly>          <!-- true for read-only lookups -->
           <returnDirect>false</returnDirect>
           <toolName>…retrieved, unchanged…</toolName>
           <toolTitle>…</toolTitle>
           <uiResource>accountHealthCard</uiResource>
       </tools>
   </McpServerDefinition>
   ```
   Setup creates tools with `readOnly`/`idempotent` = false. For a pure lookup, set both to true so clients don't treat it as a write.
5. Back up the retrieved file, run `validate_hxl.py` (checks `mcp-ui-resource`), then deploy it back and activate:
   ```bash
   sf project deploy start --metadata McpServerDefinition:<ServerApiName> --target-org <alias>
   ```
   Setup → MCP server detail → **Activate**. Re-retrieve into a scratch dir (`--target-metadata-dir <dir> --unzip`) and diff it against your file to confirm `<uiResource>` stuck.

> ⚠️ **Setup wipes `<uiResource>`.** Setup has no field for the UI resource. Editing, removing or re-adding the tool in Setup → MCP Servers rewrites the tool without `<uiResource>` and resets `readOnly`/`idempotent`. `<resources>` survives, so the server looks fine, but the client now shows a plain markdown table built from the raw output. Tell the admin not to touch the tool after wiring. If they do: retrieve, diff, re-add `<uiResource>`, redeploy, reconnect the client.

## 3. Org setup (one-time per org)
- **External Client App** for OAuth — note the **consumer key (client ID)**.
- OAuth scopes needed by hosted MCP servers.
- Enable **PKCE** and **JWT-based access tokens**.
- For images in widgets: add image domains as **Trusted URLs** (CSP is provisioned for the MCP server automatically).
Details: Hosted MCP Servers guide → Set Up Your Org.

## 4. Connect the client
| Client | How |
|---|---|
| Claude (Desktop / claude.ai) | Add custom connector with the MCP server URL + ECA client ID (Hosted MCP guide → Configure Claude) |
| ChatGPT | Same inputs (Hosted MCP guide → Configure ChatGPT) |
| Slackbot | Auth Type **Manual OAuth**, URL = server URL, Client ID = ECA consumer key. Not Block Kit. |
| Testing | MCPJam (mcpjam.com) for inspecting MCP Apps resources |

## 5. Test
Prompt that clearly triggers the tool, e.g. *"How healthy is the Equinor account?"*.

**How to read the result:**

| Client shows | Meaning |
|---|---|
| The card (badges, bars, buttons), under a header like `<Server> <toolName>` | Working |
| A markdown table/prose with the right data | Tool ran, but no UI resource is attached. `<uiResource>` is missing (usually wiped by Setup), or the client cached the tool list from before it was added |
| "Connector crashed while formatting" + a quoted `{!...}` expression | Formula over `$attrs` in the widget: switch to plain bindings. If the quoted expression is one you already removed, it's a **stale cache**. Retrieve the org's widget to prove the fix is deployed, then reconnect |

**Caching.** Clients (Claude web confirmed) cache the tool list and the UI resource per connection. After any change to the widget, the CLTs or the server definition, **disconnect and reconnect the connector, then start a new chat**. Waiting or retrying in the same chat keeps the old version.

## Don'ts
- Don't call the MCP tool to "discover" its shape; describe the action via REST instead.
- Don't point `resourceUri` at the payload CLT or at the widget name.
- Vibe-coding the MCP server itself isn't supported by Agentforce Vibes; this step is manual metadata work.
