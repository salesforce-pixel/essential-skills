# Agentforce Conversation Client API

Use the Agentforce Conversation Client (ACC) API to programmatically manage the state of the native Agentforce side panel within the Salesforce Lightning desktop interface.
The ACC API is implemented as a headless LWC module (`lightning/accApi`) that acts as a router of app-to-panel messages. It enables communication between custom LWC components and Agentforce panel.

With the ACC API, interact with your agent inside Salesforce application programmatically to:

- Open and close a panel
- Execute utterances
- Reset the panel

### Prerequisites

Before implementing the API, ensure your environment meets the following requirements:

- **Interface**: This feature is supported exclusively in the Salesforce Lightning Experience desktop environment.
- **Compatibility**: This feature is for the default Lightning Experience panel only; other interfaces like Tableau or SentOS are not supported.
- **API Version**: The lightning/accApi module requires API version 59.0 or later.
- **Feature Access**: Your Salesforce org must have Agentforce enabled.

### When to Use the ACC API

Use this API for programmatic control to open, close, or send a text utterance to the native Agentforce side panel from a custom LWC. You can also reset the panel to clear the conversation history and start a new conversation.

### Get Started with the ACC API

To interact with the panel, import the methods from the lightning/accApi module into your custom Lightning web component JavaScript file.

```javascript
import { open, close, execute, reset } from "lightning/accApi";
```

:::note
If you do not yet have a custom LWC, please refer to the standard [Salesforce Lightning Web Components Developer Guide](https://developer.salesforce.com/docs/platform/lwc/guide/get-started-introduction.md) to initialize your project and create your component first.
:::

### Component Configuration

To make your custom component available on record and home pages, add targets to the component's `meta.xml` file:

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

After adding the targets and deploying your component, you can use the Lightning App Builder to include the component on a record or home page. See [Create and Configure Lightning Experience Record Pages](https://help.salesforce.com/s/articleView?id=platform.lightning_app_builder_customize_lex_pages.htm).

### ACC API Reference & Examples

Communicate directly with the panel from your custom LWC components.

All Panel API methods are asynchronous and return a void promise (`Promise<void>`).

#### Open the Panel

- **Signature**: `export function open(botId?: string): Promise<void>;`

  **Description**: This function opens the Agentforce chat panel and resolves once the panel is successfully opened. It accepts an optional `botId` to open the panel with a specific agent; if a `botId` string isn't provided, the panel opens using the last used agent.

  **Example: Open with a Specific Agent**

  JavaScript

  ```javascript
  import { open } from 'lightning/accApi';

  async handleOpenPanel() {
      // Define the botId as a string
      const botId = '0Xx...';

      // Open the panel with a specific agent
      await open(botId);
  }
  ```

#### Close the Panel

- **Signature**: `export function close(): Promise<void>;`

  **Description**: This function hides the Agentforce chat panel and resolves once it is successfully closed. This method requires no parameters.

  **Example: Close the Panel**

  JavaScript

  ```javascript
  import { close } from 'lightning/accApi';

  async handleClosePanel() {
      // Close the panel
      await close();
  }
  ```

#### Execute an Utterance

The `execute` method programmatically sends a command to the agent as if the user had typed it into the panel. This method executes the utterance for the provided `botID`.

- **Signature**: `export function execute(utterance: string, botId: string): Promise<void>;`

  **Description**: Provide a natural language string directly to the `execute` method. This method requires a `botId` parameter to execute the utterance for the specific agent. If multiple execute requests are made, they are queued and executed strictly in sequence.

  **Example: Execute a Natural Language Utterance**

  JavaScript

  ```javascript
  import { execute } from 'lightning/accApi';

  async askForSummary() {
      // Define the utterance as a string
      const utteranceString = 'Summarize this Account';

      // Execute the natural language utterance
      await
  }
  ```

#### Reset the Panel

The `reset` method programmatically clears the conversation history and starts a new conversation in the default Agentforce panel.

- **Signature**: `export function reset(): Promise<void>;`

  **Description**: This function resets the Agentforce panel and resolves once it is successfully reset. This method requires no parameters.

**Example: Reset the Panel**

JavaScript

```javascript
import { reset } from 'lightning/accApi';

async handleResetPanel() {
    // Reset the panel to clear the conversation history
    await reset();
}
```

### Functional Example & UI Behavior

This example showcases a custom Lightning Web Component (LWC), CustomAgentforceLauncher, that demonstrates the core programmatic control features of the Agentforce Conversation Client API. This component uses methods imported from the `lightning/accApi` module to manage the native Agentforce side panel. The component includes four asynchronous methods:

- **`handleOpenChat()`**: Calls the `open()` method to display the Agentforce chat panel.
- **`handleCloseChat()`**: Calls the `close()` method to hide the Agentforce chat panel.
- **`handleSendMessage()`**: Calls the `execute(utterance, botId)` method to programmatically send a natural language utterance, "What is my account balance?", to the agent.
- **`handleResetChat()`**: Calls the `reset()` method to clear the conversation history and start a new conversation.

This functional snippet illustrates how custom host applications can communicate directly with the panel to manage its state (open/close/reset) and invoke actions on the agent (execute utterance).

**Example**

JavaScript

```javascript
import { LightningElement } from "lwc";
import { open, close, execute, reset } from "lightning/accApi";

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

  async handleResetChat() {
    await reset();
  }
}
```

### ACC API Considerations

Review these limitations and best practices when building with the ACC API:

- **Queueing Behavior**: All requests that are made would be queued and executed strictly in sequence. The platform ensures that the next query is only executed after the previous one has completed.
- **Executing Actions**: Currently, only natural language utterances are supported. You cannot execute an action directly by passing its name.
- **Finding the Bot ID**: Retrieve the `botId` for your agents by checking the URL within the Agent Builder in Salesforce Setup.
- **Multiple Panels**: Use the `botId` to explicitly target a specific agent to prevent behavior overlap if multiple agents are active in the same org.
- **No Return Data**: The `execute` method does not return the agent's textual response to your component.
- **Asynchronous Methods**: `open`, `close`, `execute`, and `reset` are asynchronous and must be handled using standard JavaScript Promise patterns.
