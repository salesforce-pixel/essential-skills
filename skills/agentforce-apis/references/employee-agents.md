# Agent API with Employee Agents — who the agent runs as

**Tested live on 2026-11-19** against an active Employee Agent (`BotDefinition.AgentType` =
`AgentforceEmployeeAgent`, `Type` = `InternalCopilot`, `BotUserId` = null), Agent API v1. The
official docs don't mention Employee Agents; everything here comes from that test unless it
says otherwise. Tested findings win over the docs. If a doc refresh disagrees, add a
"docs now say X — re-verify" note rather than overwriting them.

## Contents

- [Short answer](#short-answer)
- [Is it an Employee Agent?](#is-it-an-employee-agent)
- [Results](#results)
- [Shared user: client credentials](#shared-user-client-credentials)
- [Per user: web server flow with PKCE](#per-user-web-server-flow-with-pkce)
- [Choosing between them](#choosing-between-them)
- [Troubleshooting](#troubleshooting)
- [Not yet tested](#not-yet-tested)
- [Conflicting guidance](#conflicting-guidance)

## Short answer

- **No guest or anonymous access.** Every call needs a JWT-based token from an External
  Client App (ECA), and every such token belongs to a Salesforce user.
- **An Employee Agent always runs as the token's user.** It has no agent user, so
  `bypassUser: true` is rejected with HTTP 400. **Always send `bypassUser: false`.**
- **The OAuth flow decides who the agent runs as, not the ECA.** Client credentials → the
  ECA's Run As user. Web server flow → the person who signed in.
- **One ECA serves every user** and can support both flows at the same time. You don't need
  an ECA per user.

## Is it an Employee Agent?

```sql
SELECT Id, DeveloperName, Type, AgentType, BotUserId
FROM BotDefinition
WHERE DeveloperName = '<Agent_API_Name>'
```

`AgentType = AgentforceEmployeeAgent` / `Type = InternalCopilot` with `BotUserId` = null →
Employee Agent: use `bypassUser: false`. A service agent has a `BotUserId` (its agent
user), so `true` works there.

## Results

| Token | `bypassUser` | Result |
|---|---|---|
| None | `true` / `false` | **HTTP 404, empty body, no other headers** (from the `api.salesforce.com` gateway) |
| Classic session ID (`00D…!…`, e.g. from `sf org display`), not a JWT | `true` / `false` | **HTTP 404, empty body** |
| Client-credentials JWT (Run As user) | `true` | **HTTP 400** `AgentApiException`: `Bad Request: Invalid user ID provided on start session: ` (blank id: no agent user) |
| Client-credentials JWT (Run As user) | `false` | HTTP 200; start, 5 messages and end all succeeded |
| Web server flow + PKCE JWT (signed-in user) | `false` | HTTP 200; start, 5 messages and end all succeeded; refresh token issued |

All turns finished in 1.5–6.6 s, well inside the 120 s limit.

The gateway works out the org from the JWT (its `aud` claim lists `https://api.salesforce.com`
and the org's My Domain). With no token, or a non-JWT token, it can't route the call and
answers with a bare 404, not a 401. The request never reaches the org. So even a real
logged-in user's ordinary session ID is refused.

## Shared user: client credentials

ECA setup as in `agent-api.md` (client credentials on, Run As user on the Policy tab). The
token is issued for the Run As user: the JWT's `sub` is `uid:<Run As user Id>`, `scp` is
`sfap_api chatbot_api api`. Start the session with `"bypassUser": false`; the agent runs as
the Run As user for every caller. Callers don't need their own Salesforce users.

```bash
python3 scripts/agent_api_chat.py --agent-id 0Xx… --as-token-user "What can you help me with?"
```

This corrects an earlier line in this skill that said `bypassUser: false` "needs a
named-user token": a client-credentials token *is* a named-user token (for the Run As user),
and it works with `false`.

## Per user: web server flow with PKCE

The same ECA, with a **Callback URL** (e.g. `http://localhost:8080/callback` for a local
test; your app's real URL in production) and **Require secret for Web Server Flow** off.

1. Create a random PKCE **verifier** and its SHA-256 **challenge** (base64url, no padding),
   plus a random `state`.
2. Send the user's browser to the My Domain authorize endpoint:

   ```text
   https://<MY_DOMAIN>.my.salesforce.com/services/oauth2/authorize
     ?response_type=code
     &client_id=<CONSUMER_KEY>
     &redirect_uri=http://localhost:8080/callback
     &scope=api refresh_token sfap_api chatbot_api
     &code_challenge=<CHALLENGE>
     &code_challenge_method=S256
     &state=<STATE>
     &prompt=login
   ```

   `prompt=login` forces the login screen even if the browser already has a Salesforce
   session, so a different user can sign in.
3. The user signs in (Salesforce login or SSO) and clicks **Allow**. The browser is
   redirected to `…/callback?code=<CODE>&state=<STATE>`. Check `state` matches.
4. Swap the code for the user's token. No client secret is needed:

   ```bash
   curl -s https://<MY_DOMAIN>.my.salesforce.com/services/oauth2/token \
     --data-urlencode grant_type=authorization_code \
     --data-urlencode code="<CODE>" \
     --data-urlencode client_id="$SF_CLIENT_ID" \
     --data-urlencode redirect_uri=http://localhost:8080/callback \
     --data-urlencode code_verifier="$VERIFIER"
   ```

   Returns a JWT `access_token`, a `refresh_token` and
   `scope: "refresh_token sfap_api chatbot_api api"`.
5. Optional: confirm who the token belongs to with
   `GET https://<MY_DOMAIN>.my.salesforce.com/services/oauth2/userinfo` (`user_id`,
   `preferred_username`). It matches the JWT's `sub`.
6. Start the session with `"bypassUser": false`; send and end as usual.

PKCE protects the code swap, which suits browser and mobile apps that can't keep a secret.
Keep PKCE on for public clients and store each user's refresh token securely.

`scripts/agent_api_chat.py --login web` does steps 1–6 with a local callback listener:

```bash
export SF_MY_DOMAIN=<mydomain>.my.salesforce.com SF_CLIENT_ID=<consumer key>
python3 scripts/agent_api_chat.py --agent-id 0Xx… --login web "What can you help me with?"
```

## Choosing between them

| | Shared user (client credentials) | Per user (web server flow) |
|---|---|---|
| Agent runs as | The ECA's Run As user, for every caller | Each caller's own Salesforce user |
| Callers need a Salesforce user | No (only the Run As user) | Yes, active and with access to the agent |
| Login screen | None | Once per user; refresh token after that |
| Record and field access | The Run As user's, shared by everyone | Each caller's own |
| Audit trail | Every conversation logged as one user | Per person |
| Telling callers apart | Only through session `variables` your client sends | Built in |
| Secrets | Client secret on the server | None (PKCE) |
| Licensing | Employee Agents are licensed per user: confirm before putting many people behind one user | Normal |
| Fits | Back-office automation, one system acting as itself | Apps used by employees |

**Recommendation:** use the per-user model for Employee Agents unless there's a clear
reason, and licensing confirmation, for a shared user. If you do use a shared user, pass
the real caller's identity in session `variables`, give the Run As user only the access the
agent needs, and log the caller on the client side.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| 404, empty body, no headers | No token, or not a JWT (e.g. a CLI session ID). Get a token from an ECA flow |
| 400 `Invalid user ID provided on start session: ` | `bypassUser: true` on an agent with no agent user (Employee Agent). Send `false` |
| `redirect_uri_mismatch` at login | The `redirect_uri` in the request doesn't exactly match the ECA's Callback URL |
| Login never reaches the local callback | Listener bound to IPv4 only while the browser tried `localhost` over IPv6 (`::1`). Bind both |
| `CERTIFICATE_VERIFY_FAILED` in Python on macOS | python.org builds ship without a CA bundle: `export SSL_CERT_FILE=/etc/ssl/cert.pem`. Don't turn off certificate checks |

## Not yet tested

- Every test ran as a **System Administrator** (the Run As user, and the user who signed in).
  Not yet shown: a non-admin getting narrower access through the per-user flow, or a user
  without access to the agent being refused at session start (and with what error).
- The test agent was knowledge-only with no record-reading actions, so its answers couldn't
  show whose record access applied. Confirm with an action that reads records (e.g. "my open
  opportunities") and two users with different access.
- Other per-user flows on the same ECA: **JWT bearer** (backend signs a JWT naming the user;
  needs a certificate on the ECA and pre-approved users) and **token exchange** (swap an
  identity-provider token for the matching Salesforce user's token).
- Multi-turn memory looked weak (a "summarise our conversation" turn got a generic reply).
  That's agent behaviour, not the API, but don't assume conversation recall without testing.

## Conflicting guidance

- **`bypassUser` with client credentials.** The docs' get-started example pairs client
  credentials with `bypassUser: true`. That's right for **service agents**, which have an
  agent user, and fails for **Employee Agents** (HTTP 400 above; tested 2026-11-19).
  **Recommendation:** decide from the agent type. Employee Agent → `false`; service agent →
  `true` to run as the agent user, `false` to run as the token's user.
- Corroboration: the agentforce toolkit's preview lesson (Aug 2026) records the same
  `Invalid user ID provided on start session` error from `sf agent preview start --api-name`
  on a published Employee Agent, for the same reason (no agent user).
