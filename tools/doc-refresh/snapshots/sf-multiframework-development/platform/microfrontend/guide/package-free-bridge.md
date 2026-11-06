# Build the Embedding Bridge Without a Salesforce Package

Embed an external web app in Salesforce and talk to the host without adding a `@salesforce/*` package to your app. An embedded app communicates with Salesforce over the `sf-embedding` protocol through a small piece of JavaScript called the bridge: it completes a one-time handshake, then exchanges JSON-RPC 2.0 messages with the host over a `MessagePort`. This guide shows how to build that bridge yourself, in plain JavaScript, and covers the message surface the deployed host implements today.

The `sf-embedding` protocol specification normatively defines the behavior described here. Where this guide and the specification disagree, the specification is authoritative.

:::note
**Scope.** This guide covers the surface the deployed `lightning-ui-embedding` host implements today: the handshake and version selection, the init lifecycle, host-driven UI state, custom events, resize, and error reporting. The specification defines a larger future surface, including a capability model, host-rendered UI (alert, toast, modal, prompt, and confirm dialogs), host navigation, and request cancellation, that the shipping host doesn't broker yet. Those aren't covered here. The shipping host doesn't gate methods by capability.
:::

:::note
This guide covers the guest side only: the bridge that runs inside your embedded app. It doesn't replace the host setup. On the Salesforce side, an admin or developer still renders the `lightning-ui-embedding` base component pointed at your app's URL and adds a CSP Trusted Site for your app's origin. For that path, see [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md).
:::

## When to Build a Bridge by Hand

Most apps use the Salesforce-provided guest SDK to talk to the host. Build the bridge yourself when you want full control over the protocol surface, want to avoid an added dependency, or want to integrate the protocol into an existing message layer. A hand-written, wire-level bridge is fully supported as long as it honors the message shapes described here.

## Prerequisites

- Your web app is hosted at an HTTPS URL that you control, on an origin that differs from your Salesforce org's origin.
- A Salesforce host renders the `lightning-ui-embedding` component pointed at your app, and the org trusts your app's origin for inline frames. See [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md).
- You're comfortable working with `window.postMessage`, `MessageChannel`, and JSON-RPC 2.0 message shapes.

## How the Protocol Works

Communication happens in two phases.

```text
Salesforce host (LWC)          Your app (React or any framework)
       |                                  |
       |  1. window.postMessage handshake |   (bootstrap only)
       |<---------- heartbeat ------------|
       |--------- MessagePort transfer -->|
       |                                  |
       |  2. JSON-RPC 2.0 over the port   |   (everything else)
       |<================================>|
```

1. **Handshake (`window.postMessage`).** The host loads your app in a cross-origin iframe and passes `hostMetaData` (which includes `hostAppOrigin` and `instanceId`) on the URL. Your app sends an `sf-embedding/ready` heartbeat, and the host replies by transferring a `MessagePort`.
2. **Session (JSON-RPC 2.0 over the port).** Every later message, whether a request, a response, or a notification, is standard JSON-RPC 2.0 framed over that port. `MessageChannel` delivers messages in order per port.

### Do You Need JSON-RPC?

A JSON-RPC library isn't required, but the JSON-RPC 2.0 message shape is required if you want to talk to the real Salesforce host. Keep two things separate.

- **The message shape is the host's contract.** The deployed `lightning-ui-embedding` host emits and parses JSON-RPC 2.0 on the port. Requests are `{ jsonrpc: "2.0", id, method, params }`, notifications drop the `id`, and responses carry the `id` plus a `result` or an `error`. The `id` is a monotonic, non-negative integer per side. A request can carry an optional `_meta.traceId`, which the host echoes on the reply. The host doesn't understand anything else on the port. That's a data format, not a dependency, so you can hand-build those objects, which is what the bridge in Step 2 does with no library.
- **The handshake is not JSON-RPC.** The heartbeat and bootstrap envelope are plain `window.postMessage` messages. JSON-RPC begins only after the `MessagePort` transfer.

## Step 1: Complete the Handshake

The handshake is Salesforce-specific and security-critical, so follow it exactly. Read `hostMetaData`, send the heartbeat, and then wait for the `MessagePort` inside an `sf-embedding.bootstrap` envelope. Validate the envelope with five checks before you trust it.

```javascript
// Runs at document start, before any bridge is created.
function bootstrap({ signal } = {}) {
  return new Promise((resolve, reject) => {
    if (window.parent === window) {
      // Loaded directly, not embedded. Stay silent so your app still works standalone.
      return reject(new Error("NOT_EMBEDDED"));
    }
    // hostAppOrigin pins where the heartbeat is sent and is the only trusted origin for this session.
    // instanceId binds the incoming envelope to this specific embed.
    const meta = JSON.parse(new URL(location.href).searchParams.get("hostMetaData") ?? "null");
    const hostAppOrigin = meta?.hostAppOrigin;
    const instanceId = meta?.instanceId;
    if (
      typeof hostAppOrigin !== "string" ||
      !hostAppOrigin ||
      typeof instanceId !== "string" ||
      !instanceId
    ) {
      return reject(new Error("BAD_HOST_METADATA")); // fail fast; don't half-initialize
    }

    let captured = false;
    function onMessage(event) {
      const d = event.data;
      // Five checks; all must pass before you trust the port:
      if (d?.type !== "sf-embedding.bootstrap" || d?.protocol !== "sf-embedding") return; // 1. type and protocol
      if (event.origin !== hostAppOrigin) return; // 2. only the host origin from hostMetaData
      if (event.source !== window.parent) return; // 3. only from the parent window
      if (event.ports.length !== 1) return; // 4. exactly one transferred port
      if (d.instanceId !== instanceId) return; // 5. bound to this embed

      if (captured) {
        // A second valid envelope means someone is racing the host. You can't tell which is real,
        // so fail closed: tell the host to shut this session down, and don't use the new port.
        parent.postMessage(
          { type: "sf-embedding/shutdown", reason: "DUPLICATE_PORT_TRANSFER" },
          hostAppOrigin,
        );
        return;
      }
      captured = true;
      const port = event.ports[0];
      port.start();
      resolve({ port, hostAppOrigin, instanceId });
      // Keep the listener registered so a later duplicate envelope still triggers the shutdown above.
    }

    window.addEventListener("message", onMessage);
    signal?.addEventListener("abort", () => reject(new Error("BOOTSTRAP_ABORTED")), { once: true });
    // Send the heartbeat only after the listener is registered, so you can't miss the reply.
    // protocolVersion here is how you select the protocol version; there is no separate handshake for it.
    parent.postMessage(
      { type: "sf-embedding/ready", instanceId, protocolVersion: "1.0.0" },
      hostAppOrigin,
    );
  });
}
```

:::important
There's no bootstrap timeout. Silence isn't failure. The iframe can legitimately sit on a login, multi-factor authentication (MFA), or consent screen before your app loads and sends its heartbeat.
:::

Run the handshake once, as early as possible, such as a module-load side effect or a mount effect on your top-level layout, and reuse the single session promise everywhere. If you bootstrap lazily on first feature use, any screen that doesn't touch the bridge on mount never handshakes. The failure is invisible because no error fires and the feature does nothing.

## Step 2: Build the Bridge

After the handshake, communication is plain JSON-RPC 2.0, so the bridge is small. It generates request IDs, correlates replies, dispatches inbound requests and notifications by method, and times out requests. Here's the whole bridge, hand-written with no dependencies.

```javascript
function createBridge(port) {
  let nextId = 1;
  const pending = new Map(); // id -> { resolve, reject }
  const handlers = new Map(); // method -> (params) => result | Promise

  // Don't JSON.stringify. MessagePort uses structured clone; pre-stringifying breaks it.
  port.onmessage = ({ data: msg }) => {
    if (msg.id != null && ("result" in msg || "error" in msg)) {
      // A reply to a request we sent.
      const p = pending.get(msg.id);
      if (!p) return;
      pending.delete(msg.id);
      msg.error ? p.reject(msg.error) : p.resolve(msg.result);
    } else if (msg.method) {
      // An inbound request (has id) or notification (no id) from the host.
      Promise.resolve(handlers.get(msg.method)?.(msg.params)).then((result) => {
        if (msg.id != null) port.postMessage({ jsonrpc: "2.0", id: msg.id, result });
      });
    }
  };

  return {
    // Fire-and-forget.
    notify: (method, params) => port.postMessage({ jsonrpc: "2.0", method, params }),
    // Request and response. All shipping requests are quick, so one default timeout is enough.
    request: (method, params, timeoutMs = 30_000) =>
      new Promise((resolve, reject) => {
        const id = nextId++;
        pending.set(id, { resolve, reject });
        if (timeoutMs)
          setTimeout(() => {
            if (pending.delete(id)) reject(new Error(`TIMEOUT ${method}`));
          }, timeoutMs);
        port.postMessage({ jsonrpc: "2.0", id, method, params });
      }),
    // Handle inbound host requests and notifications.
    on: (method, handler) => handlers.set(method, handler),
  };
}
```

:::important
Don't `JSON.stringify` payloads. `MessagePort.postMessage` runs the structured clone algorithm, which preserves `Date`, `Map`, `Set`, and typed arrays. Pass JSON-RPC objects to it directly, and read `event.data` directly rather than re-parsing a string. Every value you send must be structured-clone-safe.
:::

:::note
Prefer a maintained library? Any conformant JSON-RPC 2.0 library works, and the rest of this guide is identical. Whatever you use, pin the version, and confirm that it emits standard JSON-RPC 2.0, never auto-retries (which can duplicate a side effect), and never pre-stringifies payloads.
:::

## Step 3: Complete the Init Lifecycle and Subscribe to Host State

Right after the port is live, the host announces itself and you announce back. Then you subscribe to the host's rendering state. Register your inbound handlers before you announce, so a fast host can't get ahead of you.

- The host sends `ui/notifications/host-initialized`, the authoritative carrier of session identity (`instanceId` and `hostInfo`).
- You reply once with `ui/notifications/embedding-initialized` (your app's name and version).
- You subscribe to `ui/subscribe/ui-state` to receive the host's props and styles. The current snapshot arrives in the response, not as a separate notification.

```javascript
const { port } = await bootstrap();
const bridge = createBridge(port);

// Register inbound handlers before announcing, so a fast host can't get ahead of you.
bridge.on("ui/notifications/host-initialized", (p) => {
  /* p.instanceId, p.hostInfo */
});
bridge.on("ui/notifications/ui-state-changed", ({ current }) =>
  render(current.props, current.styles),
);
bridge.on("ui/events/dispatch", ({ eventType, detail }) => handleHostEvent(eventType, detail));

// Announce your app once.
bridge.notify("ui/notifications/embedding-initialized", {
  embeddingInfo: { name: "my-app", version: "1.0.0" },
});

// Subscribe to host-driven props and styles; the snapshot arrives in the response.
const { subscriptionId, current } = await bridge.request("ui/subscribe/ui-state", {});
render(current.props, current.styles);
```

:::note
There's at most one active UI-state subscription per session. A second `ui/subscribe/ui-state` while one is active rejects with `INVALID_PARAMS`. Snapshots are full replacements, never diffs, and the host batches a multi-property update in one JavaScript turn into a single `ui/notifications/ui-state-changed`.
:::

If you send a request before the init lifecycle finishes, the host rejects it with `NOT_INITIALIZED`. Wait for `ui/notifications/host-initialized`, and then send your requests.

## Use the Bridge

With the bridge in place, every protocol method is a request or a notification.

```javascript
// Request with a default 30-second timeout. Subscribe to host-driven state:
const { current } = await bridge.request("ui/subscribe/ui-state", {});

// Notification, fire-and-forget. Hint a new size:
bridge.notify("ui/notifications/resize", { height: 800 });

// Notification. Bubble a custom event onto the host <lightning-ui-embedding> element:
bridge.notify("ui/events/dispatch", { eventType: "orderselected", detail: { id: "O-123" } });

// Receive an event the host forwards to you (after ui/events/subscribe):
bridge.on("ui/events/dispatch", ({ eventType, detail }) => handleHostEvent(eventType, detail));
```

A few rules are worth internalizing.

- **Every request gets a response. Notifications never reply.** A request resolves with a `result` or rejects with an `error`. Only notifications are dropped silently, because they have no response path.
- **One default timeout is enough.** All shipping requests are quick, and the shipping host has no user-gated (indefinite) requests, so you don't need to extend or disable the timeout for any method.
- **Notifications are fire-and-forget.** `ui/notifications/resize` is a size hint; the host applies its own layout policy and can honor, clamp, or ignore it. There's no confirming response, so observe the outcome through `window.innerWidth` and `window.innerHeight` if you need to.
- **Dirty-state rides on the event channel.** There's no dedicated method for it. Dispatch `ui/events/dispatch` with `eventType: "trackdirtystate"` and `detail: { isDirty, instanceId, label }`. Use the `instanceId` from the handshake. Omit it and the host drops the signal. The host re-emits `trackdirtystate` as a DOM event that a page author can bind to.

## Protocol Messages

These are the messages a bridge uses over the port. None of them needs a Salesforce package, because you send and receive them all through the bridge. The handshake messages (the `sf-embedding/ready` heartbeat and the `sf-embedding.bootstrap` envelope) travel over `window.postMessage`, not the port. Every message in the table is JSON-RPC 2.0 over the port.

| Message                                  | Direction   | Kind         | Purpose                                                                      |
| ---------------------------------------- | ----------- | ------------ | ---------------------------------------------------------------------------- |
| `ui/notifications/host-initialized`      | host to app | notification | Host announces itself (`instanceId`, `hostInfo`)                             |
| `ui/notifications/embedding-initialized` | app to host | notification | Your app announces itself (name, version)                                    |
| `ui/subscribe/ui-state`                  | app to host | request      | Subscribe to host-driven props and styles; the response carries the snapshot |
| `ui/unsubscribe/ui-state`                | app to host | request      | Dispose the UI-state subscription                                            |
| `ui/notifications/ui-state-changed`      | host to app | notification | Full UI-state snapshot on every change                                       |
| `ui/events/subscribe`                    | app to host | request      | Subscribe to receive host-forwarded custom events                            |
| `ui/events/unsubscribe`                  | app to host | request      | Dispose the events subscription                                              |
| `ui/events/dispatch`                     | both        | notification | Custom event either way; dirty-state rides on this                           |
| `ui/notifications/resize`                | app to host | notification | Fire-and-forget size hint (width and height in CSS pixels)                   |
| `ui/notifications/error`                 | app to host | notification | Sanitized error report (no message or stack; capped at about 50 per session) |

:::note
This table is the full surface the deployed `lightning-ui-embedding` host implements today. The protocol specification defines a larger future surface, including a capability model, host-rendered UI (alert, toast, modal, prompt, and confirm dialogs), host navigation, and request cancellation, that the shipping host doesn't broker yet.
:::

## Error Responses

Every request gets a response. A failure comes back as a JSON-RPC error with a numeric `code`, an optional `message`, and optional `data` (`{ retryable?, details? }`). These are transport-level codes on the port, distinct from the component error codes reported on the `sf-embedding.component.error` DOM event. For those, see [UI Embedding Error Codes](https://developer.salesforce.com/docs/platform/microfrontend/references/microfrontend-error-codes/error-codes.md).

| Code   | Constant                    | Meaning and what to do                                                                                                                                  |
| ------ | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -32700 | `PARSE_ERROR`               | Malformed frame received. Fix the payload.                                                                                                              |
| -32600 | `INVALID_REQUEST`           | Not a valid JSON-RPC request object. Fix the envelope.                                                                                                  |
| -32601 | `METHOD_NOT_FOUND`          | Method unknown at the selected version. The feature isn't in this host version.                                                                         |
| -32602 | `INVALID_PARAMS`            | Params failed validation, such as a second `ui/subscribe/ui-state` or an unknown `subscriptionId`. Fix your params or subscription logic.               |
| -32603 | `INTERNAL_ERROR`            | Host-side failure handling a valid request. Retry if transient.                                                                                         |
| -32012 | `NOT_INITIALIZED`           | Request sent before the session finished initializing. Wait for the init lifecycle, then retry.                                                         |
| -32016 | `PORT_CLOSED`               | Session torn down; pending requests reject locally. Remount to reconnect.                                                                               |
| -32017 | `SERIALIZATION_FAILURE`     | A payload wasn't structured-clone-safe. Send clone-safe values.                                                                                         |
| -32020 | `PROTOCOL_VIOLATION`        | Contract broken, such as a duplicate lifecycle message. Fix ordering.                                                                                   |
| -32013 | `PROTOCOL_VERSION_MISMATCH` | Heartbeat version not supported by the host. Pin a supported version. Surfaces at the handshake as a component error DOM event, before any port exists. |
| -32018 | `REQUEST_TIMEOUT`           | Client-synthesized when a request outlives its timeout. Retry with backoff.                                                                             |

`METHOD_NOT_FOUND` and `INVALID_PARAMS` are distinct. `METHOD_NOT_FOUND` means the host doesn't know the method. `INVALID_PARAMS` means the method exists but your arguments are wrong. `REQUEST_TIMEOUT` is a client-side convention your bridge synthesizes, not a host error.

## Security Essentials

The bootstrap you hand-write is security-critical.

- **Serve your app from a different origin than the host.** The browser's Same-Origin Policy isolates it. In local development, different ports count as different origins.
- **Trust only `hostAppOrigin`.** Verify `event.origin === hostAppOrigin` on the envelope, and send the heartbeat to that exact origin, never `"*"`. Don't maintain your own list of accepted host origins.
- **Run all five envelope checks, and fail closed on a duplicate transfer.** A second valid envelope means you shut the session down and never use the second port. The worst outcome is a denied session, never a hijacked one.
- **Never let the port leak.** Keep the `MessagePort` in local or module scope. Don't put it on `window`, `globalThis`, or any shared registry.
- **You handle your own authentication.** The host gives you no credentials or data access, so authenticate to your own backend as usual.
- **Sanitize error reports.** Send only the method name, a category, and a path-only filename. Never send a message, a stack, or a reason.

## Protocol Versions

Your app declares the single version it speaks in the heartbeat (`protocolVersion: "1.0.0"`). The host accepts it by transferring the port. To refuse the session, the host doesn't transfer a port. Instead, it dispatches `sf-embedding.component.error` (code `PROTOCOL_VERSION_MISMATCH`) on its own element for the page to observe. The shipping host supports exactly 1.0.0. Pin to a version you've tested, and watch the protocol changelog.

## See Also

- [Get Started with UI Embedding](/docs/platform/microfrontend/guide/get-started.md)
- [Track Unsaved Changes in an Embedded App](/docs/platform/microfrontend/guide/track-unsaved-changes.md)
- [Resize an Embedded App to Fit Its Content](/docs/platform/microfrontend/guide/resize-embedded-app.md)
- [UI Embedding Error Codes](https://developer.salesforce.com/docs/platform/microfrontend/references/microfrontend-error-codes/error-codes.md)
