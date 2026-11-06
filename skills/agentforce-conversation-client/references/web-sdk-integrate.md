# ACC Web SDK — Integrate into an External App

Prerequisite: complete `web-sdk-setup.md` (ECA, trusted domain, frontdoor URL,
`agentId`).

## 1. Install

```bash
npm install @salesforce/agentforce-conversation-client
```

## 2. Initialize

Use `embedAgentforceClient()` to inject the ACC interface into a DOM container.
`agentId` is **required in every configuration**. `agentLabel` sets a custom
label on the conversational interface.

```javascript
import { embedAgentforceClient } from "@salesforce/agentforce-conversation-client";

const initializeClient = async () => {
  const { loApp } = await embedAgentforceClient({
    container: "#agentforce-container",
    // Provide your authenticated frontdoor URL (generated server-side)
    frontdoorUrl: "<YOUR_FRONT_DOOR_URL>",
    agentforceClientConfig: {
      agentId: "ADD EMPLOYEE AGENT ID HERE", // required
      renderingConfig: {
        agentLabel: "My Agent",
        styleTokens: {
          headerBlockBackground: "#7B2CBF",
          headerBlockTextColor: "#ffffff",
        },
      },
    },
  });
};
initializeClient();
```

## 3. Rendering Modes (`renderingConfig`)

Dimensions accept both pixels (numbers) and CSS strings.

### `mode: "floating"`

Persistent widget overlay pinned to the bottom-right of the viewport. On mobile
viewports (< 640px), it expands to full screen when maximized. This is the
default Floating Action Button (FAB) entry-point experience.

```javascript
renderingConfig: {
  mode: "floating",
}
```

### `mode: "inline"`

Renders the ACC UI inside the specified parent container.

```javascript
renderingConfig: {
  mode: "inline",
  width: "420px",
  height: "600px",
}
```

### `headerEnabled`

In **inline** mode the header is **hidden by default** — set
`headerEnabled: true` to show it. In **floating** mode the header is always
visible regardless of this setting.

```javascript
renderingConfig: {
  mode: "inline",
  headerEnabled: true,
}
```

### `showHeaderIcon`

The Agentforce header icon is shown by default. Set `showHeaderIcon: false` to
hide it.

```javascript
renderingConfig: {
  showHeaderIcon: false,
}
```

## 4. Customize UI Style Tokens

The ACC UI renders inside an **iframe**, so CSS outside the iframe cannot style
its interior. Use the `styleTokens` object inside `agentforceClientConfig`.
Tokens are passed as **strings** (CSS color values, pixel values, and other CSS
properties are all strings).

```javascript
agentforceClientConfig: {
  agentId: "ADD EMPLOYEE AGENT ID HERE", // required
  renderingConfig: {
    styleTokens: {
      headerBlockBackground: "#0176d3",
      headerBlockTextColor: "#ffffff",
    },
  },
}
```

> **Supported style tokens change frequently.** For current token names/values
> (headers, message bodies, input areas), check the
> [@salesforce/agentforce-conversation-client npm package](https://www.npmjs.com/package/@salesforce/agentforce-conversation-client).
> Don't ship hardcoded styling specs to production without verifying against the
> latest release.

## 5. Customize Images

For extra branding, the SDK can substitute custom images for these visual
elements:

- **Floating button icon** — the FAB in floating mode (bottom-right of viewport).
- **Header image** — displayed at the top of the conversation panel.
- **Agent avatar** — shown alongside agent messages in the conversation thread.

> **Important:** custom images must be available from Salesforce and **publicly
> accessible** at runtime (e.g. uploaded to Salesforce CMS and made public).

Configuration properties change frequently — for the complete, current property
reference use the npm package linked above.
