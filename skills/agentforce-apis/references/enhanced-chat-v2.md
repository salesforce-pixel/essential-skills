# Enhanced Chat v2 — service agents on a website

Enhanced Chat v2 (ECv2) is the newer customer interface for Enhanced Web Chat on Service
Cloud. Both versions connect and deploy **service agents** to external chat channels.
ECv2 is **not** the same as Enhanced Web Chat (v1); see Help: *What's Enhanced Chat v2?*
(`service.enhanced_chat_v2_intro`). Connecting a service agent to it: Help *Connect a
Service Agent to Enhanced Chat v2* (`ai.service_agent_deploy_enhanced_chat_v2`).

## What ECv2 adds

| Feature | How |
|---|---|
| **Context events** | `utilAPI.setSessionContext` (new in Enhanced Web Chat, usable in ECv2 deployments). Messaging for Web guide: `service/messaging-web/guide/context-events`, reference `m4w-reference/utilAPI#setsessioncontext`. |
| **Inline mode** | Render the chat inside a `<div>` of your page instead of a floating button. Below. |
| **Custom Lightning Types** | Custom input/output UI for agent actions; channel folder `enhancedWebChat`. Use the `clt-agentforce-actions` skill. To send a message for the user or pass context events from your LWC: Messaging for Web guide `custom-lighting-type-apis`. |

## Display modes

- **Floating** (default): the chat opens from a Floating Action Button at the bottom right.
- **Inline**: the client renders inside a target element and fills it completely. The
  header can be turned off. Inline is **ECv2 only**.

## Enable inline mode

1. Setup → **Embedded Service Deployments** → your deployment → **Code Snippet**.
2. Paste the snippet into the page that hosts the chat.
3. Before the snippet initialises, set:

```javascript
embeddedservice_bootstrap.settings.displayMode = 'inline';
embeddedservice_bootstrap.settings.targetElement = document.querySelector('.chat-container');
embeddedservice_bootstrap.settings.headerEnabled = false;          // optional: hide the header
embeddedservice_bootstrap.settings.disableInlineAutoLaunch = true; // optional: don't open on load
```

- By default inline mode **launches automatically** so the element has content on page load.
- With `disableInlineAutoLaunch = true`, open it from your own control by calling the
  `launchChat` API (Messaging for Web guide `launch-chat`).
- Other settings: Messaging for Web `m4w-reference/settingsAPI`. Full API setup: *Get
  Started with APIs for Enhanced Chat* (`service/messaging-web/guide/api-overview`).

## Console warnings ECv2 checks for

| Warning | Fix |
|---|---|
| `displayMode is set to "inline" but targetElement is using the default (document.body). This will embed the chat into the entire page body` | Set `targetElement` to your container. |
| `targetElement is set to a custom element but displayMode is not set to "inline". In floating mode, the chat button will float within the specified container` | Either set `displayMode = 'inline'`, or remove `targetElement` to float in the default place. |

## Field notes (from the agentforce toolkit, not the official docs)

These come from live service-agent builds (Aug–Oct 2026). Re-check them if they're more
than a few months old.

- **Custom cards need the right connection settings.** For CLT cards to render in ECv2,
  the agent had `connection customer_web_client:` with `adaptive_response_allowed: False`.
  Without it, sessions reported `__supports_result_display__ = false` and the card came out
  flattened as text, or as a literal `show_command` (Aug 2026).
- **Republish the Embedded Service deployment** after every agent, action or renderer
  change, allow up to about 10 minutes for the cache, and test in a private window with a
  new conversation (Aug–Oct 2026).
- **Builder and CLI preview don't render service-agent cards reliably**; check the payload
  in preview and the card in the real widget (Oct 2026).
- A metadata-deployed messaging Flow can land as Draft even though the source says
  `Active`; read back Flow and channel status after deploying. Create a new Embedded
  Service deployment in Setup before retrieving it, because Setup creates its Experience
  network and site (Oct 2026).
