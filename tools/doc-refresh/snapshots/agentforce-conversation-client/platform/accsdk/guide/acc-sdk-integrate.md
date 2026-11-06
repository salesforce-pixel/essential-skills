## Integrate the Agentforce Conversation Client Web SDK

To embed the Agentforce Conversation Client into an external application, follow these steps to install, initialize, and configure the conversational interface.

### 1. Install the Package

In your frontend project directory, run this command to install the core package using npm.

```bash
npm install @salesforce/agentforce-conversation-client
```

### 2. Initialize the Client

Use the `embedAgentforceClient()` function to inject the ACC interface into a designated DOM container. To route the conversation to a specific Employee Agent and apply a custom label to the conversational interface, add the `agentId` and `agentLabel` to your configuration.

```javascript
import { embedAgentforceClient } from "@salesforce/agentforce-conversation-client";

const initializeClient = async () => {
  const { loApp } = await embedAgentforceClient({
    container: "#agentforce-container",
    // IMPORTANT: Provide your authenticated frontdoor URL
    frontdoorUrl: "<YOUR_FRONT_DOOR_URL>",
    agentforceClientConfig: {
      // IMPORTANT: Provide Employee Agent Id
      agentId: "ADD EMPLOYEE AGENT ID HERE",
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

### 3. Configure Rendering Modes

Configure how the interface displays within your page layout by using the `renderingConfig` property. Dimensions accept both pixels (numbers) and CSS strings.

#### Floating

Renders a persistent ACC UI widget overlay pinned to the bottom right corner of the viewport. On mobile viewports (<640px), the floating mode ACC UI expands to full screen when maximized.

```javascript
import { embedAgentforceClient } from "@salesforce/agentforce-conversation-client";

const initializeClient = async () => {
  const { loApp } = await embedAgentforceClient({
    container: "#agentforce-container",
    frontdoorUrl: "<YOUR_FRONT_DOOR_URL>",
    agentforceClientConfig: {
      // IMPORTANT: agentId is required in all configurations
      agentId: "ADD EMPLOYEE AGENT ID HERE",
      renderingConfig: {
        mode: "floating",
      },
    },
  });
};
initializeClient();
```

#### Inline

Renders the ACC UI inside the specified parent container.

```javascript
import { embedAgentforceClient } from "@salesforce/agentforce-conversation-client";

const initializeClient = async () => {
  const { loApp } = await embedAgentforceClient({
    container: "#agentforce-container",
    frontdoorUrl: "<YOUR_FRONT_DOOR_URL>",
    agentforceClientConfig: {
      agentId: "ADD EMPLOYEE AGENT ID HERE",
      renderingConfig: {
        mode: "inline",
        width: "420px",
        height: "600px",
      },
    },
  });
};
initializeClient();
```

#### Header visibility (`headerEnabled`)

In inline mode, the header is hidden by default. Set `headerEnabled: true` to show it. In floating mode, the header is always visible regardless of this setting.

```javascript
import { embedAgentforceClient } from "@salesforce/agentforce-conversation-client";

const initializeClient = async () => {
  const { loApp } = await embedAgentforceClient({
    container: "#agentforce-container",
    frontdoorUrl: "<YOUR_FRONT_DOOR_URL>",
    agentforceClientConfig: {
      agentId: "ADD EMPLOYEE AGENT ID HERE",
      renderingConfig: {
        mode: "inline",
        headerEnabled: true,
      },
    },
  });
};
initializeClient();
```

#### Show Agentforce header icon (`showHeaderIcon`)

By default, the header icon is shown. Set `showHeaderIcon: false` to hide the Agentforce icon

```javascript
import { embedAgentforceClient } from "@salesforce/agentforce-conversation-client";

const initializeClient = async () => {
  const { loApp } = await embedAgentforceClient({
    container: "#agentforce-container",
    frontdoorUrl: "<YOUR_FRONT_DOOR_URL>",
    agentforceClientConfig: {
      agentId: "ADD EMPLOYEE AGENT ID HERE",
      renderingConfig: {
        showHeaderIcon: false,
      },
    },
  });
};
initializeClient();
```

#### See Also

[Customize UI Style Tokens](/docs/platform/accsdk/guide/acc-sdk-customize-tokens.md)
