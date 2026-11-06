# UI Embedding Error Codes

When you embed a web app with the UI Embedding host component, the host reports failures by dispatching a single DOM event, `sf-embedding.component.error`, on its own element. Listen for that event to detect and handle every error the host surfaces to your page.

Each error event carries this detail shape:

```json
{
  "instanceId": "string",
  "phase": "configuration | bootstrap",
  "code": "STRING_CODE",
  "message": "Human-readable description of the failure.",
  "retryable": false
}
```

- `phase` groups the failure by the stage at which it occurred: `configuration` (a setup or attribute problem) or `bootstrap` (the handshake with the embedded document).
- `code` is a stable string identifier for the specific error. Match on `code` in your handler.
- `retryable` indicates whether a fresh attempt (for example, remounting the component) is plausibly worthwhile. When `retryable` is `false`, fix the underlying problem first.

:::note
The `sf-embedding.component.error` event is the only channel through which the host surfaces errors to your page. Errors that the host records for internal diagnostics only aren't delivered through this event and aren't listed here.
:::

## Error Codes

Match on the `code` value in your `sf-embedding.component.error` handler.

| Code                        | Phase         | Retryable |
| --------------------------- | ------------- | --------- |
| `ALLOW_SCRIPTS_STRIPPED`    | configuration | No        |
| `BLOCKED_SANDBOX_TOKEN`     | configuration | No        |
| `MISSING_SRC`               | configuration | No        |
| `INVALID_SRC`               | configuration | No        |
| `SAME_ORIGIN_SRC`           | configuration | No        |
| `SESSION_BINDING_MUTATED`   | configuration | No        |
| `WRONG_ORIGIN`              | bootstrap     | No        |
| `PROTOCOL_VERSION_MISMATCH` | bootstrap     | No        |
| `INSTANCE_ID_MISMATCH`      | bootstrap     | No        |
| `DUPLICATE`                 | bootstrap     | No        |
| `WRONG_TYPE`                | bootstrap     | No        |
| `DUPLICATE_PORT_TRANSFER`   | configuration | No        |
| `HEARTBEAT_TIMEOUT`         | bootstrap     | Yes       |
| `TRANSFER_FAILED`           | bootstrap     | No        |
| `EMBEDDING_SHUTDOWN`        | configuration | No        |

Most of these codes report a setup or attribute problem that you fix in your own configuration. A few of them, such as `HEARTBEAT_TIMEOUT`, `TRANSFER_FAILED`, and `EMBEDDING_SHUTDOWN`, report a runtime or lifecycle condition in the embedded app or the frame rather than a mistake in your setup. They're documented here so you can recognize and handle them, but they don't always call for a configuration change.

## Configuration Errors

These errors occur before the handshake, when the host validates the attributes you set on the component.

### ALLOW_SCRIPTS_STRIPPED

**Message:** `iframe sandbox MUST include 'allow-scripts'; embedding cannot run without it.`

The resolved `sandbox` attribute for the embedding frame doesn't include the `allow-scripts` token. The embedded app can't run its scripts without it, so the embedding can't start.

To resolve:

1. Review the `sandbox` and `removeSandboxTokens` values you set on the component.
2. Make sure that the resolved sandbox keeps `allow-scripts`.
3. Remove `allow-scripts` from `removeSandboxTokens` if you added it there.

### BLOCKED_SANDBOX_TOKEN

**Message:** `iframe sandbox MUST NOT include 'allow-top-navigation'; poses phishing risk.` or `iframe sandbox MUST NOT include 'allow-popups-to-escape-sandbox'; poses security risk.`

The resolved sandbox includes a token that UI Embedding blocks for security reasons: `allow-top-navigation` or `allow-popups-to-escape-sandbox`.

To resolve:

1. Remove `allow-top-navigation` and `allow-popups-to-escape-sandbox` from the `sandbox` value.
2. Reload the component.

### MISSING_SRC

**Message:** `iframe src MUST be provided; the embedding cannot start without a src.`

No `src` value was set on the component. The embedding can't start without a source URL.

To resolve:

1. Set the `src` attribute to the URL of the app that you want to embed.

### INVALID_SRC

**Message:** `iframe src MUST be a parseable URL.` On the `src`-mutation path, the same code carries an appended detail: `iframe src MUST be a parseable URL. Error: {details}`.

The `src` value isn't a URL that the host can parse.

To resolve:

1. Set `src` to a complete, absolute URL, such as `https://app.example.com/widget`.
2. Confirm that the value has no leading spaces or unresolved template placeholders.

### SAME_ORIGIN_SRC

**Message:** `iframe src origin MUST differ from the host document origin.`

The `src` origin is the same as the host page's origin. UI Embedding requires the embedded app to load from a different origin.

To resolve:

1. Host the embedded app on an origin that differs from the host page.
2. Update `src` to point to that origin.

### SESSION_BINDING_MUTATED

**Message:** `'{property}' is session-binding; remount the component to change it.`

The `src`, `sandbox`, or `removeSandboxTokens` attribute was changed after the component mounted. These attributes are read once at mount and can't change during the life of an instance.

To resolve:

1. Unmount and remount the component to apply a new `src`, `sandbox`, or `removeSandboxTokens` value.

### DUPLICATE_PORT_TRANSFER

**Message:** `embedding signalled shutdown.`

The host detected a duplicate bootstrap envelope from the iframe bridge and shut the session down. This code is distinct from `DUPLICATE`, which reports a duplicate handshake heartbeat. `DUPLICATE_PORT_TRANSFER` arrives as the `code` on the `sf-embedding.component.error` event (see the note under EMBEDDING_SHUTDOWN).

To resolve:

1. Confirm that the embedded app completes the bootstrap handshake only once per load.
2. Remount the component to start a new session.

## Bootstrap Errors

These errors occur during the handshake between the host and the embedded document.

### WRONG_ORIGIN

**Message:** `heartbeat origin '{origin}' does not match the expected iframe src origin '{expected}'`

The handshake message arrived from an origin that doesn't match the origin of the `src` URL.

To resolve:

1. Confirm that the embedded app sends its handshake from the same origin as its `src` URL.
2. Check for redirects that move the app to a different origin before it sends the handshake.

### PROTOCOL_VERSION_MISMATCH

**Message:** `declared version '{version}' is not supported by host`

The embedded app declared a protocol version that the host doesn't support.

To resolve:

1. Update the embedded app to use a protocol version that the host supports.

### INSTANCE_ID_MISMATCH

**Message:** `heartbeat instanceId does not match the host-minted session instanceId`

The instance identifier in the handshake doesn't match the identifier the host assigned for the session. This mismatch usually means the app echoed a stale or hard-coded identifier instead of the one the host passed in.

To resolve:

1. Confirm that the embedded app reads the host-provided instance identifier and returns the same value in its handshake.
2. Remove any hard-coded or cached instance identifier from the app.

### DUPLICATE

**Message:** `heartbeat received after port1 was already transferred`

The host received a handshake after it already completed the handshake and transferred the message port for the session.

To resolve:

1. Confirm that the embedded app sends the handshake only once per load.

### WRONG_TYPE

**Message:** `heartbeat rejected: WRONG_TYPE`

The host received a handshake message during bootstrap, but the message wasn't a `sf-embedding/ready` heartbeat. The message was missing, wasn't an object, or carried a different type value.

To resolve:

1. Confirm that the embedded app sends a well-formed `sf-embedding/ready` message as its handshake.
2. Check that no other code on the page posts messages to the host while it waits for the handshake.

### HEARTBEAT_TIMEOUT

**Message:** `Embedded document did not send sf-embedding/ready heartbeat within {n}ms`

The embedded document didn't send its `sf-embedding/ready` handshake within the advisory deadline. This deadline is advisory: the host reports the timeout but doesn't tear down the component, so a late handshake can still succeed.

To resolve:

1. Confirm that the embedded app sends the `sf-embedding/ready` message during load.
2. Check that the app loads and runs without errors at the URL in `src`.
3. To adjust or disable the deadline, set `heartbeatTimeoutMs`. A positive number sets the deadline in milliseconds, and `Infinity` disables it.
4. Because this error is retryable, remount the component to try again after you fix the underlying delay.

### TRANSFER_FAILED

**Message:** `<iframe> port transfer threw. Error: {details}`

The host tried to transfer the message port to the embedded frame, but the transfer failed. This failure usually means the frame was removed or navigated away before the handshake finished.

To resolve:

1. Confirm that the embedded frame stays in the page during load.
2. Check for code that removes or reloads the frame before the handshake completes.

## Lifecycle Errors

### EMBEDDING_SHUTDOWN

**Message:** `embedding signalled shutdown.`

- **Phase:** configuration

The embedded app signaled that it shut down. The host closes the session in response.

`EMBEDDING_SHUTDOWN` isn't a fixed code. The host dispatches the app-supplied `reason`, or `EMBEDDING_SHUTDOWN` when the app omits one. So this exact code appears only when the app shuts down without a reason. Otherwise, an app-defined string arrives as the `code` on the same event (for example, `DUPLICATE_PORT_TRANSFER`). Don't match only on `code === "EMBEDDING_SHUTDOWN"` to detect a shutdown.

To resolve:

1. Check the embedded app's logic to understand why it shut down.
2. Remount the component to start a new session.

## See Also

- [Get Started with UI Embedding](https://developer.salesforce.com/docs/platform/microfrontend/guide/get-started.md)
- [Migrate from the Developer Preview API](https://developer.salesforce.com/docs/platform/microfrontend/guide/migrate-from-dev-preview.md)
