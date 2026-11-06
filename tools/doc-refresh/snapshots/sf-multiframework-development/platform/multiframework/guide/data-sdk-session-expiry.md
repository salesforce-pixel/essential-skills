# Handle an Expired Session

When a user's Salesforce session expires, Data SDK requests fail with an HTTP 401 response. To recover, register an `onStatus` callback for 401 that reloads the page. When the page loads, Salesforce checks the session. If the session is gone, Salesforce shows the login page, and after the user logs in, returns them to the same page in your app.

```typescript
import { createDataSDK } from "@salesforce/platform-sdk/data";

let reloading = false;

function reloadOnce(): void {
  // On a local development server, reloading doesn't fix a 401.
  if (import.meta.env.DEV) return;

  // Several requests can fail at the same time. Reload only for the first one.
  if (reloading) return;
  reloading = true;

  // Save anything that you want to restore after the reload, such as a form draft.

  // Salesforce checks the session when the page loads. If the session is gone,
  // the user logs in and comes back to this page.
  window.location.reload();
}

const dataSdk = await createDataSDK({
  webapp: { onStatus: { 401: reloadOnce } },
});
```

Each `createDataSDK()` call has its own `onStatus` callbacks. Pass `reloadOnce` to every `createDataSDK()` call in your app, and keep it and the `reloading` flag in one shared module. An SDK instance created without the callback doesn't react to a 401.

The callback doesn't reload the page during local development. `import.meta.env.DEV` is the development flag in Vite. If your app uses a different build tool, use that tool's development flag.

Register the callback for 401 only. A 403 response means that the user doesn't have access, and reloading the page doesn't fix it.

## How the Callback Works

The `webapp.onStatus` option is supported on the `WebApp` and `Micro-Frontend` surfaces. See [Data SDK Support](/docs/platform/multiframework/guide/data-sdk-intro.md#data-sdk-support).

- **When it runs.** The SDK calls the callback when a request gets a response with that status.
- **How often.** The SDK calls the callback once for each request that gets the status. If several requests fail at the same time, the callback runs once for each of them.
- **Arguments.** The callback receives no arguments. It can be synchronous or asynchronous.
- **Result.** The SDK waits for the callback to finish, then completes the request with the original response. The SDK ignores the callback's return value. If the callback throws an error, `fetch()` rejects with that error, while `query()` and `mutate()` return it in `errors`.
- **No retry.** The SDK doesn't send the request again after the callback runs, and it doesn't start a login. After a reload, your app loads its data again.

## Which Requests Call the Callback

| Request                                                  | Calls `onStatus[401]` | What your code receives                        |
| :------------------------------------------------------- | :-------------------: | :--------------------------------------------- |
| `fetch()` that gets a 401                                |           ✅           | The 401 `Response`. The promise doesn't reject |
| `graphql.query()` that sends a request and gets a 401    |           ✅           | A result with `errors`                         |
| `graphql.query()` that's answered from the GraphQL cache |           ❌           | The cached data                                |
| `graphql.mutate()` that gets a 401                       |           ✅           | A result with no `data` and no `errors`        |
| Any GraphQL request that gets HTTP 200 with `errors`     |           ❌           | A result with `errors`                         |

A query answered from the cache doesn't send a request, so it doesn't call the callback. The next query that sends a request does. See [Cache Control](/docs/platform/multiframework/guide/data-sdk-cache-control.md).

A mutation that gets a 401 returns a result with neither `data` nor `errors`. Treat that result as a failure, not a success.

## Considerations

- **A 401 doesn't always mean that the session expired.** A request to an endpoint that your app can't access from its domain also gets a 401, and reloading the page doesn't fix it. With the `reloadOnce` callback, the page reloads each time your app calls that endpoint. If one feature keeps reloading the page while the rest of your app works, check that its endpoint is supported. See [Access Salesforce APIs](/docs/platform/multiframework/guide/data-sdk-connect.md).
- **Save state before the reload.** A reload discards the state of the page. In the callback, before you call `window.location.reload()`, save anything that you want to restore after the user returns, such as a form draft in `sessionStorage`. Restore it when your app loads. A mutation that was in progress during the reload might or might not have been applied, so make writes safe to repeat.
- **Unsaved-changes prompts.** If your app asks the user to confirm before leaving the page, and the user stays, the `reloading` flag stays set. The app then ignores later 401 responses until the page loads again.
- **Hash routes.** The URL fragment (the part after `#`) might not persist through the login page. Use path-based routes so that the user returns to the same view.
- **Local development.** On a local development server, the dev server refreshes your org login for you. If a 401 still reaches your app, your Salesforce CLI login expired, and reloading the page doesn't fix it. The `reloadOnce` callback skips the reload during local development, so the request fails with the 401. Log in again with `sf org login web`. See [Preview and Run Your App Locally](/docs/platform/multiframework/guide/mfw-preview.md).
