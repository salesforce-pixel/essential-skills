# ACC Web SDK — Salesforce Org Setup & Authentication

These are **admin prerequisites**. Complete all of them before the frontend
integration in `web-sdk-integrate.md` will function. ACC uses Lightning Out 2.0
to embed the LWC-based client into external apps that run outside the Salesforce
domain, so those apps need a secure OAuth-based way to authenticate.

## 1. Set Up an External Client App (ECA)

External Client Apps are the new generation of connected apps; they provide SSO
and use OAuth 2.0 to authorize external apps.

1. Salesforce **Setup** → Quick Find → **External Client App Manager**.
2. Click **New External Client App**.
3. Enter basic info:
   - **Name** (shown in the manager) and **API Name** (auto-derived).
   - **Contact email**.
   - **Distribution state**: choose **Local** for your own org; **Packaged** for
     packaging/distribution.
4. Click **Enable OAuth** to configure the OAuth policy.
5. App settings:
   - **Callback URL** — the URL in your app that accepts the auth returned from
     Salesforce, e.g. `https://<3p-domain>/callback.html`.
   - **OAuth Scopes** — select at minimum:
     - Manage user data via APIs (`api`)
     - Manage user data via Web browsers (`web`)
     - Access Lightning applications (`lightning`)
     - Add others as needed.
6. **Flow Enablement** — pick the flow for your app:
   - **Authorization Code and Credentials Flow** — specify whether user
     credentials are required in the POST body.
   - **Client Credentials Flow** — only works with the `api`, `lightning`, or
     `web` scopes.
7. **Security** — select **Require secret for Refresh Token** plus any others.
8. Click **Create**.
9. On the **Settings** tab, click **Consumer Key and Secret** to copy/save:
   - Consumer Key → `client_id`
   - Consumer Secret → `client_secret`

### Additional JWT Bearer Flow settings (only if using JWT Bearer)

After creating the ECA:

1. Setup → **External Client App Manager** → select your ECA → **Edit**.
2. **OAuth Policies** → set **Permitted Users** to
   *Admin approved users are pre authorized*.
3. **App Policies** → add the custom permission set to **Selected Permission Sets**.
4. Save and close.

Reference: [Set Up Authentication for Lightning Out 2.0](https://help.salesforce.com/s/articleView?id=platform.lightning_out_auth.htm&type=5)

## 2. Set Up Trusted Domains

Requires Salesforce Admin permissions.

1. Setup → Quick Find → **Session Settings**.
2. Scroll to **Trusted Domains for Inline Frames** → **Add Domain**.
3. Enter the domain of the web app where you embed ACC. Accepted formats:
   `example.com`, `https://example.com`, `*.example.com`.
4. Select **Lightning Out** as the iFrame type and **Save**.

Also ensure first-party cookie restrictions are disabled per the org's session
settings.

## 3. Generate the Access Token

Exchange client credentials for an access token. `<your-salesforce-org>` is your
org's My Domain / instance host; `client_id`/`client_secret` are the ECA consumer
values from step 1.

```bash
curl --location 'https://<your-salesforce-org>/services/oauth2/token' \
  --data-urlencode 'grant_type=client_credentials' \
  --data-urlencode 'client_id=<client_id>' \
  --data-urlencode 'client_secret=<client_secret>'
```

> **Docs conflict, not verified in an org.** The ACC guide shows the client
> credentials flow above. The Lightning Out 2.0 auth article (which ACC is built
> on) says the client credentials flow **isn't supported**: the flow has no user
> context, so Salesforce removes the `web` scope from its token. Lightning Out 2.0
> supports flows that give a web-scoped token with user context: the **web server
> (authorization code) flow** and the **JWT bearer flow** (for JWT bearer, also
> add the `refresh_token` scope to the ECA). If `singleaccess` returns
> `Invalid_Scope` for a client-credentials token, switch to one of those flows.

## 4. Generate a Frontdoor URL (the SDK's `authCredential`)

Frontdoor URLs bridge an existing session into a UI session without re-entering
credentials. Use the generated frontdoor URL as the `frontdoorUrl` value when
initializing the SDK.

> Frontdoor URLs are **short-lived**. To refresh the session, generate a new one.

```javascript
const getFrontdoorUrl = async (accessToken, instanceUrl) => {
  try {
    const frontdoorEndpoint = `${instanceUrl}/services/oauth2/singleaccess`;
    const myHeaders = new Headers();
    myHeaders.append("accept", "application/json");
    myHeaders.append("authorization", `Bearer ${accessToken}`);
    myHeaders.append("content-type", "application/x-www-form-urlencoded");

    const response = await fetch(frontdoorEndpoint, {
      method: "POST",
      headers: myHeaders,
      body: new URLSearchParams(),
    });
    if (!response.ok) {
      return { error: `Salesforce API responded with ${response.status}`, statusCode: response.status };
    }
    const responseData = await response.json();
    return { frontdoorUrl: responseData.frontdoor_uri };
  } catch (error) {
    console.error("Error in getFrontdoorUrl:", error);
    return { error: error.message || "Failed to generate frontdoor URL" };
  }
};
```

Reference: [Generate a frontdoor URL to Bridge into UI Sessions](https://help.salesforce.com/s/articleView?id=xcloud.frontdoor_singleaccess.htm&type=5)

### UI Bridge (`singleaccess`) rules

From the UI Bridge help article:

- **Lifetime**: the `frontdoor_uri` is valid for **up to 1 minute** and is
  **single-use**. Repeat requests in that window return the same URL and don't
  extend it. Generate it just before calling `embedAgentforceClient()`, not at
  page build time or in a cache.
- **Host**: call your **My Domain** (or Experience Cloud site) URL. Hosts such as
  `login.salesforce.com` and `test.salesforce.com` return `No_Access`.
- **Token**: the token must have the `web` or `full` scope, and it must come from
  the same org you call (otherwise `Wrong_Org`). For POST, send it in the
  `Authorization: Bearer` header (as above) or as an `access_token` body parameter.
- **User**: the user behind the token **can't have the API Only User
  permission** (otherwise `Bad_OAuth_Token`).
- **No `redirect_uri`** is needed for embedding.

| Error | Meaning / fix |
|---|---|
| `Bad_OAuth_Token` | Token invalid or expired (get a new one), or the user has API Only User |
| `Missing_OAuth_Token` | No token in the header or body |
| `Invalid_Scope` | Token lacks the `web` or `full` scope: fix the ECA scopes or the OAuth flow (see the note in step 3) |
| `Invalid_Param` | `redirect_uri` isn't a relative path |
| `No_Access` | Sent to `login.`/`test.salesforce.com`: use My Domain |
| `Wrong_Org` | Token issued by a different org than the host |

### Authentication management (security)

- **Don't hardcode** OAuth tokens or frontdoor URLs in client-side code.
- Pass credentials to the browser **only when strictly necessary** — they can be
  scraped by malicious actors. Run the token + frontdoor generation on your
  backend.

## 5. Get Your Employee Agent ID (`agentId`)

1. Setup → Quick Find → **Agentforce Agents** → select **Agentforce Employee Agent**.
2. Locate the Employee Agent you want to embed.
3. Open the Agent record and copy its **18-character** Salesforce record ID from
   the URL. Provide this as `agentId` during SDK initialization.
