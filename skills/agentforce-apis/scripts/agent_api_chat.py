#!/usr/bin/env python3
"""Talk to an Agentforce agent through the Agent API (standard library only).

Mints a client-credentials token, starts a session, sends one or more messages
(synchronous or SSE streaming), prints the replies, and always ends the session.

Credentials come from the environment, never from arguments or files:
  SF_MY_DOMAIN       My Domain host, e.g. acme.my.salesforce.com (no lightning.force.com)
  SF_CLIENT_ID       External Client App consumer key
  SF_CLIENT_SECRET   External Client App consumer secret
  SF_ACCESS_TOKEN    optional: use this token instead of minting one

Examples:
  agent_api_chat.py --agent-id 0Xx... "Where is my order?"
  agent_api_chat.py --agent-id 0Xx... --stream "Hi" "Order 1234"
  agent_api_chat.py --agent-id 0Xx...                    # interactive; empty line ends
  agent_api_chat.py --agent-id 0Xx... --var team_descriptor=Gold --custom-surface "Hi"
  agent_api_chat.py --agent-id 0Xx... --dry-run "Hi"     # print requests, send nothing

Exit codes: 0 ok, 1 API/HTTP error, 2 usage/config error.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

API_HOSTS = {"standard": "https://api.salesforce.com", "gov": "https://api.gov.salesforce.com"}
API_PATH = "/einstein/ai-agent/v1"
TIMEOUT = 130  # the Agent API itself times out at 120 s (returned as HTTP 500)


class ApiError(Exception):
    pass


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def base_url(host):
    host = host.strip().rstrip("/")
    return host if host.startswith(("https://", "http://")) else "https://" + host


def redact(headers):
    return {k: ("Bearer ***" if k == "Authorization" else v) for k, v in headers.items()}


def request(method, url, headers=None, body=None, form=None, dry_run=False, stream=False):
    headers = dict(headers or {})
    data = None
    if form is not None:
        data = urllib.parse.urlencode(form).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    if dry_run:
        shown = {k: ("***" if k == "client_secret" else v) for k, v in (form or {}).items()}
        print(f"--> {method} {url}", file=sys.stderr)
        print(f"    headers: {json.dumps(redact(headers))}", file=sys.stderr)
        if form is not None or body is not None:
            print(f"    body: {json.dumps(shown if form is not None else body)}", file=sys.stderr)
        return None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=TIMEOUT)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:2000]
        raise ApiError(f"HTTP {e.code} on {method} {url}: {detail or e.reason}{hint(e.code, detail)}")
    except urllib.error.URLError as e:
        raise ApiError(f"Cannot reach {url}: {e.reason}")
    if stream:
        return resp
    with resp:
        raw = resp.read().decode("utf-8", "replace")
    return json.loads(raw) if raw.strip() else {}


def hint(code, detail):
    d = detail or ""
    if code == 400 and "not a valid agent ID" in d:
        return "\n    hint: wrong agent ID; SELECT Id FROM BotDefinition WHERE DeveloperName = '<name>'"
    if code == 401:
        return "\n    hint: check consumer key/secret, client credentials + Run As user on the ECA Policy tab, and scopes"
    if code == 404:
        return "\n    hint: wrong host or token (Government Cloud needs --gov)"
    if code == 423:
        return "\n    hint: another request on this session is still running; the API allows one at a time"
    if "EngineConfigLookupException" in d:
        return "\n    hint: SF_MY_DOMAIN must be the Current My Domain URL (*.my.salesforce.com)"
    if "HttpServerErrorException" in d:
        return "\n    hint: check the agent ID in the path"
    if "Unsupported Media Type" in d:
        return "\n    hint: Content-Type must be application/json"
    if code == 500:
        return "\n    hint: a turn longer than 120 s is reported as HTTP 500"
    return ""


def mint_token(my_domain, dry_run):
    cid, secret = os.environ.get("SF_CLIENT_ID"), os.environ.get("SF_CLIENT_SECRET")
    if not (cid and secret):
        die("set SF_CLIENT_ID and SF_CLIENT_SECRET (or SF_ACCESS_TOKEN)")
    tok = request("POST", base_url(my_domain) + "/services/oauth2/token", form={
        "grant_type": "client_credentials", "client_id": cid, "client_secret": secret,
    }, dry_run=dry_run)
    if dry_run:
        return "DRY_RUN_TOKEN"
    scopes = set((tok.get("scope") or "").split())
    missing = {"chatbot_api", "sfap_api", "api"} - scopes
    if missing:
        print(f"warning: token lacks scopes {sorted(missing)}; add them to the External Client App",
              file=sys.stderr)
    return tok["access_token"]


def parse_var(spec):
    """NAME=VALUE or NAME:TYPE=VALUE (TYPE defaults to Text)."""
    if "=" not in spec:
        die(f"--var expects NAME=VALUE or NAME:TYPE=VALUE, got {spec!r}")
    key, value = spec.split("=", 1)
    name, _, vtype = key.partition(":")
    return {"name": name, "type": vtype or "Text", "value": value}


def inform_texts(payload):
    """Text of every Inform message in a sync response or an SSE Inform event."""
    msgs = payload.get("messages") or ([payload["message"]] if payload.get("message") else [])
    return [m for m in msgs if isinstance(m, dict) and m.get("type") == "Inform"]


def print_inform(m, as_json):
    if as_json:
        print(json.dumps(m, indent=2))
        return
    print(m.get("message", ""))
    for r in m.get("result") or []:
        print(f"  [result {r.get('type')}] {r.get('value')}")
    for c in m.get("citedReferences") or []:
        print(f"  [source] {c.get('value')}")


def iter_sse(resp):
    """Yield parsed JSON objects from an SSE response (data: lines, blank-line separated)."""
    buf = []
    with resp:
        for raw in resp:
            line = raw.decode("utf-8", "replace").rstrip("\r\n")
            if line.startswith("data:"):
                buf.append(line[5:].lstrip())
            elif line == "" and buf:
                chunk, buf = "\n".join(buf), []
                try:
                    yield json.loads(chunk)
                except json.JSONDecodeError:
                    print(f"warning: unparsable SSE data: {chunk[:200]}", file=sys.stderr)
        if buf:
            try:
                yield json.loads("\n".join(buf))
            except json.JSONDecodeError:
                pass


def send_stream(url, headers, body, as_json):
    resp = request("POST", url, {**headers, "Accept": "text/event-stream"}, body, stream=True)
    shown = []
    final = None
    for ev in iter_sse(resp):
        m = ev.get("message") or {}
        kind = m.get("type") or ("Inform" if inform_texts(ev) else None)
        if kind == "ProgressIndicator":
            print(f"… {m.get('message', '')}", file=sys.stderr)
        elif kind == "TextChunk":
            shown.append(m.get("message", ""))
            if not as_json:
                sys.stdout.write(m.get("message", ""))
                sys.stdout.flush()
        elif kind == "ValidationFailureChunk":
            # Docs: drop everything rendered so far, show only what streams next.
            shown = []
            if not as_json:
                sys.stdout.write("\n[response failed validation; discarding streamed text]\n")
        elif kind == "Inform":
            final = inform_texts(ev)
        elif kind == "EndOfTurn":
            break
    if as_json:
        for m in final or []:
            print_inform(m, True)
        return
    if shown:
        sys.stdout.write("\n")
    for m in final or []:
        # The Inform is the authoritative reply. If no chunks were shown, print its text;
        # otherwise print only what chunks don't carry (structured results, sources).
        if not shown:
            print_inform(m, False)
        elif m.get("result") or m.get("citedReferences"):
            print_inform({**m, "message": "[final reply has structured content]"}, False)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("messages", nargs="*", help="messages to send in order; none = interactive")
    p.add_argument("--agent-id", required=True, help="BotDefinition Id (0Xx...)")
    p.add_argument("--stream", action="store_true", help="use the SSE streaming endpoint")
    p.add_argument("--gov", action="store_true", help="Government Cloud (api.gov.salesforce.com)")
    p.add_argument("--api-base", help="override the Agent API host (testing)")
    p.add_argument("--as-token-user", action="store_true",
                   help="bypassUser=false: run as the token's user instead of the agent user")
    p.add_argument("--var", action="append", default=[], metavar="NAME[:TYPE]=VALUE",
                   help="agent variable to set at session start (repeatable)")
    p.add_argument("--custom-surface", action="store_true",
                   help='add surfaceConfig {"surfaceType": "Custom"} (custom connection)')
    p.add_argument("--session-key", help="externalSessionKey (default: random UUID)")
    p.add_argument("--json", action="store_true", help="print raw Inform messages as JSON")
    p.add_argument("--dry-run", action="store_true", help="print requests to stderr, send nothing")
    a = p.parse_args()
    sys.stdout.reconfigure(line_buffering=True)  # keep replies in order with stderr status lines

    my_domain = os.environ.get("SF_MY_DOMAIN")
    if not my_domain:
        die("set SF_MY_DOMAIN to your Current My Domain URL (*.my.salesforce.com)")
    if "lightning.force.com" in my_domain:
        die("SF_MY_DOMAIN must be the *.my.salesforce.com host, not lightning.force.com")
    if a.dry_run and not a.messages:
        a.messages = ["<message>"]

    api = base_url(a.api_base) if a.api_base else API_HOSTS["gov" if a.gov else "standard"]
    api += API_PATH
    try:
        token = os.environ.get("SF_ACCESS_TOKEN") or mint_token(my_domain, a.dry_run)
        auth = {"Authorization": f"Bearer {token}"}
        start = {
            "externalSessionKey": a.session_key or str(uuid.uuid4()),
            "instanceConfig": {"endpoint": base_url(my_domain)},
            "streamingCapabilities": {"chunkTypes": ["Text"]},
            "bypassUser": not a.as_token_user,
        }
        if a.var:
            start["variables"] = [parse_var(v) for v in a.var]
        if a.custom_surface:
            start["surfaceConfig"] = {"surfaceType": "Custom"}
        print(f"externalSessionKey: {start['externalSessionKey']}", file=sys.stderr)
        sess = request("POST", f"{api}/agents/{a.agent_id}/sessions",
                       {**auth, "Accept": "application/json"}, start, dry_run=a.dry_run)
        sid = sess["sessionId"] if sess else "DRY_RUN_SESSION"
        print(f"sessionId: {sid}", file=sys.stderr)
        for m in inform_texts(sess or {}):
            print_inform(m, a.json)
    except ApiError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    status = 0
    try:
        seq = 0
        queue = list(a.messages)
        while True:
            if queue:
                text = queue.pop(0)
            elif a.messages:
                break
            else:
                try:
                    text = input("> ").strip()
                except EOFError:
                    break
                if not text:
                    break
            seq += 1
            body = {"message": {"sequenceId": seq, "type": "Text", "text": text}}
            url = f"{api}/sessions/{sid}/messages"
            if a.dry_run:
                accept = "text/event-stream" if a.stream else "application/json"
                request("POST", url + ("/stream" if a.stream else ""),
                        {**auth, "Accept": accept}, body, dry_run=True)
            elif a.stream:
                send_stream(url + "/stream", auth, body, a.json)
            else:
                resp = request("POST", url, {**auth, "Accept": "application/json"}, body)
                for m in inform_texts(resp):
                    print_inform(m, a.json)
    except ApiError as e:
        print(f"error: {e}", file=sys.stderr)
        status = 1
    except KeyboardInterrupt:
        status = 130
    finally:
        try:
            request("DELETE", f"{api}/sessions/{sid}",
                    {**auth, "x-session-end-reason": "UserRequest"}, dry_run=a.dry_run)
            print("session ended", file=sys.stderr)
        except ApiError as e:
            print(f"warning: could not end session: {e}", file=sys.stderr)
    return status


if __name__ == "__main__":
    sys.exit(main())
