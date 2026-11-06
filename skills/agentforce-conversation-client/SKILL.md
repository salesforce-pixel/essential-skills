---
name: agentforce-conversation-client
description: >-
  Integrate Agentforce Conversation Client (ACC) — Salesforce's Employee Agent
  conversation UI — into apps. Use when embedding an Agentforce/Employee Agent
  chat experience into an EXTERNAL web app (React, Vue, plain JS, or any
  framework) via the @salesforce/agentforce-conversation-client Web SDK, OR when
  controlling the native Agentforce side panel from a custom Lightning Web
  Component inside Salesforce via the lightning/accApi module, including opening
  Agentforce Coworker (SearchAgent in the side panel, or the full
  /lightning/coworker page with a pre-filled question) from a button. Covers External
  Client App (ECA) OAuth setup, trusted domains, access token + frontdoor URL
  generation, getting the Employee Agent ID, embedAgentforceClient()
  initialization, rendering modes (floating/inline), style tokens, custom
  images, and the open/close/execute panel API.
metadata:
  version: "1.0"
---

<!--
Changelog
1.0 — Imported into essential-skills (2026-11-06) from the personal
      ~/.claude/skills copy. Doc sources tracked by tools/doc-refresh.
-->

# Agentforce Conversation Client (ACC)

Agentforce Conversation Client (ACC) is Salesforce's unified UI framework for
building Agentforce **Employee Agent (AEA)** conversation experiences. It
handles real-time token-by-token streaming, dynamic rendering of Lightning Types
(rich interactive components), brand styling, and secure connection logic — so
you don't build a conversational interface from scratch.

## Pick the right integration path

There are **two distinct ways** to use ACC. Identify which one the task needs
before writing any code — they share almost nothing.

| If the goal is… | Use | Read |
|---|---|---|
| Embed an Employee Agent chat into an **external** web app hosted **outside** Salesforce (React, Vue, Angular, plain JS…) | **ACC Web SDK** (`@salesforce/agentforce-conversation-client`) | `references/web-sdk-setup.md` then `references/web-sdk-integrate.md` |
| Programmatically **open/close** or **send utterances** to the **native Agentforce side panel** from a custom LWC **inside** Salesforce Lightning | **ACC API** (`lightning/accApi`) | `references/acc-api.md` |

**Do NOT use the ACC Web SDK** for purely headless agent integrations (SMS,
WhatsApp, custom native mobile). ACC provides UI; headless channels don't need it.

## ACC Web SDK — high-level workflow

Embedding into an external app is a two-part job. The Salesforce **org setup is
an admin prerequisite** and must be done before the frontend code will work.

1. **Org setup (admin, one-time)** — see `references/web-sdk-setup.md`:
   - Create an **External Client App (ECA)** for OAuth 2.0 auth.
   - Add the app's domain as a **Trusted Domain for Inline Frames** (iframe type
     "Lightning Out") and ensure first-party cookie restrictions are disabled.
   - Copy the **Consumer Key** (`client_id`) and **Consumer Secret**
     (`client_secret`).
   - Get the **18-character Employee Agent ID** (`agentId`).
2. **Auth flow (backend)** — see `references/web-sdk-setup.md`:
   - Exchange client credentials for an `access_token`.
   - Use the token to generate a short-lived **frontdoor URL**
     (`/services/oauth2/singleaccess`). This becomes the `frontdoorUrl` you pass
     to the SDK. **Do this server-side** — never hardcode tokens/frontdoor URLs
     in client code.
3. **Frontend integration** — see `references/web-sdk-integrate.md`:
   - `npm install @salesforce/agentforce-conversation-client`
   - Call `embedAgentforceClient({ container, frontdoorUrl, agentforceClientConfig })`.
   - `agentId` is **required in every configuration**.

### Minimal Web SDK example

```javascript
import { embedAgentforceClient } from "@salesforce/agentforce-conversation-client";

const { loApp } = await embedAgentforceClient({
  container: "#agentforce-container",
  frontdoorUrl: "<YOUR_FRONT_DOOR_URL>", // generated server-side, short-lived
  agentforceClientConfig: {
    agentId: "<18_CHAR_EMPLOYEE_AGENT_ID>", // required
    renderingConfig: {
      mode: "floating", // or "inline"
      agentLabel: "My Agent",
      styleTokens: {
        headerBlockBackground: "#0176d3",
        headerBlockTextColor: "#ffffff",
      },
    },
  },
});
```

## ACC API — high-level workflow

Inside Salesforce Lightning Experience (desktop only), a custom LWC can drive the
native side panel:

```javascript
import { open, close, execute } from "lightning/accApi";

await open(botId);                 // botId optional; opens last-used agent if omitted
await execute("Summarize this Account", botId);
await close();
```

Requires API version 59.0+, Agentforce enabled, and Lightning Experience desktop.
See `references/acc-api.md` for the full signatures, considerations (queueing, no
return data), `meta.xml` targets, a runtime `botId` lookup by agent API name, and
how to open **Agentforce Coworker** (the `SearchAgent` agent opens in the side panel
despite the docs; the full Coworker page opens via `/lightning/coworker?c__term=…`,
never `c__cid`, and never in an iframe).

## Key guardrails

- **Security**: Generate tokens and frontdoor URLs on your backend. Never
  hardcode OAuth tokens or frontdoor URLs in client-side code — they can be
  scraped from the browser. Pass credentials to the browser only when strictly
  necessary.
- **Frontdoor URLs are short-lived** — regenerate a new one to refresh the
  session.
- **`agentId` is required** in every Web SDK configuration.
- **Style tokens & config props change frequently** — verify current token names
  and properties against the
  [@salesforce/agentforce-conversation-client npm package](https://www.npmjs.com/package/@salesforce/agentforce-conversation-client)
  rather than hardcoding an outdated list.
- **Custom images** must be publicly accessible from Salesforce (e.g. uploaded to
  Salesforce CMS and made public) so the SDK can load them at runtime.
- ACC UI renders inside an **iframe** — external CSS cannot style its interior;
  use `styleTokens` instead.

## Source documentation

Official guide: https://developer.salesforce.com/docs/platform/accsdk/guide/acc-developer-guide.md
