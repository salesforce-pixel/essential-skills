# Agentforce Conversation Client API (`lightning/accApi`)

Use the ACC API to programmatically manage the **native Agentforce side panel**
inside the Salesforce Lightning desktop interface. It's a headless LWC module
(`lightning/accApi`) that routes app-to-panel messages between custom LWC
components and the Agentforce panel.

Capabilities: open/close a panel, and execute utterances.

> This is a different integration from the ACC Web SDK. Use the API for control
> of the panel **inside Salesforce**; use the Web SDK to embed ACC into
> **external** apps.

## Prerequisites

- **Interface**: Salesforce **Lightning Experience desktop** only.
- **Compatibility**: default Lightning Experience panel only — Tableau, SentOS,
  and other interfaces are **not** supported (official docs). **Field finding
  (2026-10-26):** this is stricter than the platform. The Agentforce Coworker
  agent (`SearchAgent`, BotDefinition type `InternalCopilot`) opened in the native
  side panel with `open(botId)` and ran an utterance with `execute(utterance, botId)`
  from a Home page LWC. What is not supported is the *full* Coworker page
  (`/lightning/coworker`); for that, see "Agentforce Coworker" below.
- **API Version**: `lightning/accApi` requires **API version 59.0 or later**.
- **Feature access**: the org must have **Agentforce enabled**.

## Get started

```javascript
import { open, close, execute } from "lightning/accApi";
```

If you don't have a custom LWC yet, initialize one via the
[LWC Developer Guide](https://developer.salesforce.com/docs/platform/lwc/guide/get-started-introduction.md)
first.

### Component configuration (`meta.xml`)

Expose the component to record/home pages, then add it via Lightning App Builder:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>65.0</apiVersion>
    <isExposed>true</isExposed>
    <targets>
        <target>lightning__AppPage</target>
        <target>lightning__HomePage</target>
        <target>lightning__RecordPage</target>
    </targets>
</LightningComponentBundle>
```

## API reference

All panel methods are **asynchronous** and return `Promise<void>`.

### `open(botId?): Promise<void>`

Opens the Agentforce chat panel; resolves once opened. Optional `botId` opens a
specific agent; omit it to open with the last-used agent.

```javascript
import { open } from "lightning/accApi";

async handleOpenPanel() {
  const botId = "0Xx...";
  await open(botId);
}
```

### `close(): Promise<void>`

Hides the panel; resolves once closed. No parameters.

```javascript
import { close } from "lightning/accApi";

async handleClosePanel() {
  await close();
}
```

### `execute(utterance, botId): Promise<void>`

Sends a natural-language command to the agent as if the user typed it. Requires
a `botId` to target the specific agent. Multiple execute requests are queued and
run strictly in sequence.

```javascript
import { execute } from "lightning/accApi";

async askForSummary() {
  const utteranceString = "Summarize this Account";
  await execute(utteranceString, botId);
}
```

### Full component example

```javascript
import { LightningElement } from "lwc";
import { open, close, execute } from "lightning/accApi";

export default class CustomAgentforceLauncher extends LightningElement {
  async handleOpenChat() {
    await open();
  }

  async handleCloseChat() {
    await close();
  }

  async handleSendMessage() {
    const utterance = "What is my account balance?";
    await execute(utterance, botId);
  }
}
```

## Considerations

- **Queueing**: all requests are queued and executed strictly in sequence — the
  next runs only after the previous completes.
- **Executing actions**: only natural-language utterances are supported. You
  cannot execute an action directly by its name.
- **Finding the `botId`**: check the URL in Agent Builder (Salesforce Setup), or
  look it up at runtime so nothing org-specific is hardcoded (pattern below).
- **Name clashes**: `open` and `close` are generic names; alias them on import
  (`import { open as openAgentPanel, execute as askAgentPanel } from "lightning/accApi"`).
- **Errors**: wrap `open`/`execute` in `try/catch` and show a toast, so a missing
  agent or an unavailable panel doesn't fail silently.
- **Multiple panels**: pass `botId` to explicitly target an agent and prevent
  overlap when multiple agents are active in the same org.
- **No return data**: `execute` does not return the agent's textual response to
  your component.
- **Async**: `open`, `close`, and `execute` must be handled with standard
  Promise patterns.

## Look up the `botId` by agent API name (no hardcoded Ids)

Tested 2026-10-26. Cacheable Apex, user mode:

```apex
@AuraEnabled(cacheable=true)
public static Id getAgentId(String developerName) {
    if (String.isBlank(developerName)) {
        return null;
    }
    List<BotDefinition> agents = [
        SELECT Id FROM BotDefinition WHERE DeveloperName = :developerName WITH USER_MODE LIMIT 1
    ];
    return agents.isEmpty() ? null : agents[0].Id;
}
```

```javascript
import { LightningElement, api, wire } from "lwc";
import { ShowToastEvent } from "lightning/platformShowToastEvent";
import { open as openAgentPanel, execute as askAgentPanel } from "lightning/accApi";
import getAgentId from "@salesforce/apex/MyController.getAgentId";

export default class AskAgent extends LightningElement {
  @api agentName = "SearchAgent"; // expose as a design attribute
  agentId;

  @wire(getAgentId, { developerName: "$agentName" })
  wiredAgentId({ data }) {
    this.agentId = data || undefined;
  }

  async handleAsk() {
    if (!this.agentId) {
      this.dispatchEvent(new ShowToastEvent({ title: "Agent not found", variant: "warning" }));
      return;
    }
    try {
      await openAgentPanel(this.agentId);
      await askAgentPanel("What could derail my meeting with Carol Tezak?", this.agentId);
    } catch (error) {
      this.dispatchEvent(new ShowToastEvent({ title: "Agentforce panel not available", variant: "warning" }));
    }
  }
}
```

## Agentforce Coworker: side panel vs full experience

Coworker comes in two forms. Offering both (for example as a two-item menu) works well:

| Form | How to open it from an LWC | Notes |
|---|---|---|
| Coworker **agent** in the side panel | ACC API with the `SearchAgent` bot Id (above) | Stays on the current page. Agent chat only. |
| **Full** Coworker experience | `window.open('/lightning/coworker?c__term=' + encodeURIComponent(question))`, in a new tab or a popup docked right (`popup=yes,width=520,left=screen.availWidth-520`) | Coworker runs the question and opens it as a Lightning tab "Ask: <generated title>". Use a relative path so it works on any org domain. |

Gotchas (tested 2026-10-26):

- `c__term` is the question. `c__cid` opens an *existing* conversation by id; a question there (with or without a `uid`) fails with **"Chat cannot be loaded"**.
- Don't put `/lightning/coworker` in an iframe inside an LWC to fake a sidebar: it loads the whole Lightning UI inside the frame and crashes. Use the side panel (agent) or `window.open` (full experience).
