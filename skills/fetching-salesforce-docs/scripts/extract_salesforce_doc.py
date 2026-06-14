#!/usr/bin/env python3
"""
Tiny wrapper for Salesforce documentation extraction.

Behavior:
- If the URL is on help.salesforce.com, automatically route to the dedicated
  Help extractor with shadow DOM heuristics.
- Otherwise, use a lightweight browser-rendered extractor for official
  Salesforce-owned documentation sites such as developer.salesforce.com,
  architect.salesforce.com, admin.salesforce.com, lightningdesignsystem.com,
  and other supported official documentation hosts.

Examples:
  python3 skills/fetching-salesforce-docs/scripts/extract_salesforce_doc.py \
    --url "https://help.salesforce.com/s/articleView?id=service.miaw_security.htm&type=5" \
    --pretty

  python3 skills/fetching-salesforce-docs/scripts/extract_salesforce_doc.py \
    --url "https://developer.salesforce.com/docs/platform/lwc/guide/use-message-channel-intro.html" \
    --pretty

  python3 skills/fetching-salesforce-docs/scripts/extract_salesforce_doc.py \
    --url "https://architect.salesforce.com/well-architected/overview" \
    --stealth --pretty
"""

from __future__ import annotations

import argparse
import html
import json
import re
from typing import Any, Dict, Optional
from urllib.parse import urljoin, urlparse

from runtime_bootstrap import maybe_reexec_in_sf_docs_runtime

maybe_reexec_in_sf_docs_runtime(__file__)

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

try:
    from playwright_stealth import Stealth
except ImportError:
    Stealth = None

try:
    from playwright_stealth import stealth_sync
except ImportError:
    stealth_sync = None

from extract_help_salesforce import extract as extract_help_salesforce


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

STRONG_SHELL_TOKENS = [
    "loading",
    "sorry to interrupt",
    "css error",
    "enable javascript",
    "we looked high and low",
    "couldn't find that page",
    "404 error",
]

WEAK_SHELL_TOKENS = [
    "sign in",
    "cookie preferences",
]

# A page whose body is dominated by the OneTrust cookie-consent overlay is a
# failed extraction, not content. These banners are short (~700 chars) and
# contain none of the STRONG_SHELL_TOKENS, so without this they slip through as
# a false-positive success. Real doc pages that merely mention cookies are far
# longer, so we only treat these as a shell below a generous length threshold.
CONSENT_SHELL_TOKENS = [
    "we use cookies on our website",
    "accept all cookies",
    "cookie consent manager",
    "do not accept",
]
CONSENT_SHELL_MAX_LEN = 1500

# A page with this much extracted text is a real article, not a loading/error
# shell — shells (spinners, soft-404s, cookie banners) are inherently short.
# This guards against shell tokens incidentally appearing inside long content.
SUBSTANTIAL_CONTENT_LEN = 1500

# Salesforce-owned documentation domains. Includes Salesforce core plus the
# Salesforce-owned product families (MuleSoft, Tableau, Slack, Heroku). Bare
# apex domains go in the EXACT set; subdomains are matched via the suffixes.
OFFICIAL_DOC_EXACT_HOSTS = {
    "salesforce.com",
    "lightningdesignsystem.com",
    "mulesoft.com",
    "tableau.com",
    "slack.com",
    "slack.dev",
    "heroku.com",
}

OFFICIAL_DOC_SUFFIXES = (
    ".salesforce.com",
    ".lightningdesignsystem.com",
    ".mulesoft.com",
    ".tableau.com",
    ".slack.com",
    ".slack.dev",
    ".heroku.com",
)


def normalize_text(text: str) -> str:
    text = text.replace("\u00a0", " ").replace("\r", "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def _has_token(haystack: str, tokens) -> bool:
    # Word-boundary match so e.g. "loading" does not match inside "downloading".
    return any(re.search(r"\b" + re.escape(token) + r"\b", haystack) for token in tokens)


def looks_like_shell(title: str, text: str) -> bool:
    stripped = len(text.strip())
    # Substantial content is a real article, never a shell — even if a shell-ish
    # word happens to appear somewhere in it.
    if stripped >= SUBSTANTIAL_CONTENT_LEN:
        return False
    haystack = f"{title}\n{text}".lower()
    if _has_token(haystack, STRONG_SHELL_TOKENS):
        return True
    if _has_token(haystack, CONSENT_SHELL_TOKENS) and stripped < CONSENT_SHELL_MAX_LEN:
        return True
    if _has_token(haystack, WEAK_SHELL_TOKENS):
        return stripped < 600
    return False


def apply_stealth(page) -> bool:
    if stealth_sync is not None:
        try:
            stealth_sync(page)
            return True
        except Exception:
            pass
    if Stealth is not None:
        try:
            Stealth().apply_stealth_sync(page)
            return True
        except Exception:
            return False
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract official Salesforce documentation from a URL")
    parser.add_argument("--url", required=True, help="Official Salesforce doc URL")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout in seconds (default: 60)")
    parser.add_argument("--stealth", action="store_true", help="Best-effort stealth mode for bot-sensitive pages")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    return parser.parse_args()


def is_official_salesforce_host(host: str) -> bool:
    host = (host or "").lower()
    return host in OFFICIAL_DOC_EXACT_HOSTS or any(host.endswith(suffix) for suffix in OFFICIAL_DOC_SUFFIXES)


def route_kind(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if host.endswith("help.salesforce.com"):
        return "help"
    # Legacy "atlas" docs (e.g. atlas.en-us.sfdx_dev.meta) are an AngularJS
    # single-page app (DocsApp) that injects the article via XHR and does not
    # hydrate in headless Chromium. Route them to the JSON content API the app
    # itself calls instead of trying to render them.
    if host.endswith("developer.salesforce.com") and "/docs/atlas." in parsed.path:
        return "atlas"
    if is_official_salesforce_host(host):
        return "official"
    raise SystemExit(f"Unsupported host for fetching-salesforce-docs extractor: {host or url}")


def extract_official_salesforce_doc(url: str, timeout_seconds: int, use_stealth: bool = False) -> Dict[str, Any]:
    timeout_ms = timeout_seconds * 1000
    host = (urlparse(url).hostname or "").lower()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=USER_AGENT, viewport={"width": 1440, "height": 1400})
        stealth_used = apply_stealth(page) if use_stealth else False

        try:
            response = page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
            http_status = response.status if response else None
            page.wait_for_timeout(1500)
            try:
                page.wait_for_function(
                    r"""
                    () => {
                      const el = document.querySelector('main, article, [role="main"]');
                      const text = (el?.innerText || el?.textContent || '').trim();
                      return text.length > 200;
                    }
                    """,
                    timeout=min(timeout_ms, 15000),
                )
            except PlaywrightTimeoutError:
                pass
            try:
                page.wait_for_load_state("networkidle", timeout=min(timeout_ms, 15000))
            except PlaywrightTimeoutError:
                pass
            page.wait_for_timeout(500)

            payload = page.evaluate(
                r"""
                () => {
                  function normalize(text) {
                    return String(text || '')
                      .replace(/\u00a0/g, ' ')
                      .replace(/\r/g, '')
                      .replace(/\n{3,}/g, '\n\n')
                      .trim();
                  }

                  function isVisible(el) {
                    if (!el || !el.getBoundingClientRect) return false;
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    return rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none';
                  }

                  function allRoots() {
                    const roots = [document];
                    const queue = [document];
                    while (queue.length) {
                      const current = queue.shift();
                      if (!current || !current.querySelectorAll) continue;
                      const elements = current.querySelectorAll('*');
                      for (const el of elements) {
                        if (el.shadowRoot) {
                          roots.push(el.shadowRoot);
                          queue.push(el.shadowRoot);
                        }
                      }
                    }
                    return roots;
                  }

                  function deepQueryAll(selector) {
                    const results = [];
                    const seen = new Set();
                    for (const root of allRoots()) {
                      if (!root.querySelectorAll) continue;
                      for (const el of root.querySelectorAll(selector)) {
                        if (!seen.has(el)) {
                          seen.add(el);
                          results.push(el);
                        }
                      }
                    }
                    return results;
                  }

                  function collectLinks(scope) {
                    const urls = new Set();
                    const nodes = scope && scope.querySelectorAll ? scope.querySelectorAll('a[href]') : [];
                    for (const a of nodes) {
                      const href = a.href || a.getAttribute('href') || '';
                      if (!href) continue;
                      if (href.startsWith('javascript:') || href.startsWith('mailto:')) continue;
                      urls.add(href);
                    }
                    return Array.from(urls);
                  }

                  const title = document.title || normalize(document.querySelector('title')?.innerText || 'Untitled');
                  const childLinks = new Set();
                  for (const root of allRoots()) {
                    for (const link of collectLinks(root)) childLinks.add(link);
                  }

                  const selectorConfigs = [
                    { selector: 'article', strategy: 'article', base: 260 },
                    { selector: 'main', strategy: 'main', base: 220 },
                    { selector: '[role="main"]', strategy: 'role-main', base: 220 },
                    { selector: '.slds-text-longform', strategy: 'longform', base: 200 },
                    { selector: '.markdown-content', strategy: 'markdown-content', base: 190 },
                    { selector: '.content-body', strategy: 'content-body', base: 180 },
                    { selector: '.article-body', strategy: 'article-body', base: 180 },
                    { selector: '.article-content', strategy: 'article-content', base: 180 },
                    { selector: '.post-content', strategy: 'post-content', base: 170 },
                    { selector: '.main-content', strategy: 'main-content', base: 170 },
                    { selector: '.tds-content', strategy: 'tds-content', base: 165 },
                    { selector: '.siteforceContentArea .content', strategy: 'siteforce-content', base: 160 },
                    { selector: 'doc-content-layout', strategy: 'legacy-doc-layout', base: 150 },
                    { selector: 'doc-xml-content', strategy: 'legacy-doc-xml', base: 145 },
                    { selector: 'doc-amf-reference .markdown-content', strategy: 'legacy-amf-markdown', base: 150 },
                    { selector: 'main .content, article .content', strategy: 'nested-content', base: 140 },
                  ];

                  const candidates = [];
                  for (const cfg of selectorConfigs) {
                    const nodes = deepQueryAll(cfg.selector);
                    for (const node of nodes) {
                      if (!isVisible(node)) continue;
                      const text = normalize(node.innerText || node.textContent || '');
                      if (text.length < 200) continue;
                      let score = cfg.base + Math.min(text.length, 5000) / 30;
                      const lowered = text.toLowerCase();
                      if (lowered.includes(title.toLowerCase())) score += 50;
                      if (lowered.includes('table of contents')) score -= 80;
                      if (lowered.includes('cookie preferences')) score -= 120;
                      if (lowered.includes('sign in')) score -= 120;
                      candidates.push({
                        strategy: cfg.strategy,
                        selector: cfg.selector,
                        score,
                        text,
                        links: collectLinks(node).slice(0, 200),
                      });
                    }
                  }

                  const bodyText = normalize(document.body?.innerText || '');
                  if (bodyText.length >= 200) {
                    candidates.push({
                      strategy: 'body',
                      selector: 'body',
                      score: Math.min(bodyText.length, 5000) / 50,
                      text: bodyText,
                      links: Array.from(childLinks).slice(0, 200),
                    });
                  }

                  candidates.sort((a, b) => b.score - a.score);
                  const best = candidates[0] || null;

                  return {
                    url: window.location.href,
                    title,
                    strategy: best ? best.strategy : 'none',
                    selector: best ? best.selector : null,
                    text: best ? best.text : '',
                    contentLinks: best ? best.links : [],
                    childLinks: Array.from(childLinks).slice(0, 200),
                    candidateCount: candidates.length,
                  };
                }
                """
            )

            text = normalize_text(payload.get("text", ""))
            likely_shell = looks_like_shell(payload.get("title", ""), text)
            ok = bool(text) and len(text) >= 300 and not likely_shell

            return {
                "ok": ok,
                "url": payload.get("url", url),
                "httpStatus": http_status,
                "title": payload.get("title") or "Untitled",
                "host": host,
                "hostKind": "official-salesforce",
                "strategy": payload.get("strategy"),
                "selector": payload.get("selector"),
                "likelyShell": likely_shell,
                "stealthRequested": use_stealth,
                "stealthAvailable": stealth_sync is not None or Stealth is not None,
                "stealthUsed": stealth_used,
                "text": text,
                "contentLinks": payload.get("contentLinks", []),
                "childLinks": payload.get("childLinks", []),
                "candidateCount": payload.get("candidateCount", 0),
            }
        finally:
            page.close()
            browser.close()


_BLOCK_TAG_RE = re.compile(
    r"</(?:p|div|li|ul|ol|tr|table|h[1-6]|section|article|pre|br|blockquote)\s*>",
    re.IGNORECASE,
)
_SELF_CLOSE_BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
_SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
_HREF_RE = re.compile(r'href\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)


def html_to_text(content_html: str) -> str:
    text = _SCRIPT_STYLE_RE.sub(" ", content_html or "")
    text = _SELF_CLOSE_BR_RE.sub("\n", text)
    text = _BLOCK_TAG_RE.sub("\n", text)
    text = _TAG_RE.sub(" ", text)
    text = html.unescape(text)
    return normalize_text(text)


def extract_atlas_links(content_html: str, base_url: str) -> list:
    urls = []
    seen = set()
    for raw in _HREF_RE.findall(content_html or ""):
        if not raw or raw.startswith(("javascript:", "mailto:", "#")):
            continue
        resolved = urljoin(base_url, raw)
        if resolved not in seen:
            seen.add(resolved)
            urls.append(resolved)
    return urls


def parse_atlas_url(url: str) -> Dict[str, Optional[str]]:
    """Pull the atlas document id and the .htm content id out of an atlas URL."""
    parts = [seg for seg in urlparse(url).path.split("/") if seg]
    atlas_id = next((seg for seg in parts if seg.startswith("atlas.")), None)
    content_id = parts[-1] if parts and parts[-1].endswith(".htm") else None
    return {"atlas_id": atlas_id, "content_id": content_id}


def extract_atlas_doc(url: str, timeout_seconds: int) -> Dict[str, Any]:
    """Fetch a legacy atlas doc via the JSON content API the DocsApp SPA uses.

    Flow: get_document/<atlas_id> -> descriptor (deliverable, locale, version)
    then get_document_content/<deliverable>/<content_id>/<locale>/<doc_version>.
    The content id MUST keep its '.htm' suffix or the endpoint returns HTTP 200
    with an empty body.
    """
    timeout_ms = timeout_seconds * 1000
    host = (urlparse(url).hostname or "").lower()
    parsed = parse_atlas_url(url)
    atlas_id = parsed["atlas_id"]
    content_id = parsed["content_id"]

    if not atlas_id:
        raise SystemExit(f"Could not parse atlas document id from URL: {url}")

    docs_base = "https://developer.salesforce.com/docs/"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/plain, */*",
        "Referer": url,
    }

    def _atlas_error(status, message):
        return {
            "ok": False,
            "url": url,
            "httpStatus": status,
            "title": "Untitled",
            "host": host,
            "hostKind": "atlas",
            "strategy": "atlas-json-api",
            "selector": None,
            "likelyShell": False,
            "stealthRequested": False,
            "stealthAvailable": stealth_sync is not None or Stealth is not None,
            "stealthUsed": False,
            "text": "",
            "contentLinks": [],
            "childLinks": [],
            "candidateCount": 0,
            "atlasDocId": atlas_id,
            "atlasContentId": content_id,
            "atlasContentUrl": None,
            "error": message,
        }

    with sync_playwright() as p:
        req = p.request.new_context(extra_http_headers=headers)
        try:
            # The descriptor endpoint, like the content endpoint, occasionally
            # returns an empty / non-JSON body on a transient miss. Retry before
            # giving up, and fail cleanly (ok:false) rather than crashing.
            descriptor = None
            descriptor_status = None
            for _ in range(3):
                descriptor_resp = req.get(docs_base + "get_document/" + atlas_id, timeout=timeout_ms)
                descriptor_status = descriptor_resp.status
                body = descriptor_resp.text()
                if body.strip():
                    try:
                        descriptor = json.loads(body)
                        break
                    except json.JSONDecodeError:
                        descriptor = None
            if descriptor is None:
                return _atlas_error(
                    descriptor_status,
                    f"Atlas descriptor endpoint returned an empty or non-JSON body "
                    f"(HTTP {descriptor_status}) for get_document/{atlas_id}. Likely a "
                    f"transient miss; retry, or verify the atlas document id.",
                )

            deliverable = descriptor.get("deliverable")
            locale = descriptor.get("locale") or "en-us"
            version = descriptor.get("version") or {}
            doc_version = version.get("doc_version") if isinstance(version, dict) else version

            content_html = ""
            title = None
            content_status = None
            content_url = None
            section_requested = bool(content_id and deliverable and doc_version)
            section_empty = False

            if section_requested:
                content_url = (
                    f"{docs_base}get_document_content/{deliverable}/{content_id}/{locale}/{doc_version}"
                )
                # The endpoint occasionally returns HTTP 200 with an empty body
                # for a transient miss; retry a couple times before giving up.
                # A persistently empty body means the content id is invalid or
                # renamed (the .htm in the URL no longer maps to a document).
                for _ in range(3):
                    content_resp = req.get(content_url, timeout=timeout_ms)
                    content_status = content_resp.status
                    body = content_resp.text()
                    if body.strip():
                        try:
                            payload = json.loads(body)
                            content_html = payload.get("content", "") or ""
                            title = payload.get("title")
                        except json.JSONDecodeError:
                            content_html = body
                        break
                section_empty = not content_html.strip()

            # Use the descriptor's own content ONLY for a genuine landing-page
            # request (no specific .htm section). We must NOT substitute the
            # landing page when a specific section was requested but came back
            # empty — that would report the wrong page as a success.
            if not section_requested and not content_html.strip():
                content_html = descriptor.get("content", "") or ""
                title = title or descriptor.get("title")

            if section_empty:
                doc_title = descriptor.get("doc_title") or descriptor.get("title") or "Untitled"
                return {
                    "ok": False,
                    "url": url,
                    "httpStatus": content_status,
                    "title": doc_title,
                    "host": host,
                    "hostKind": "atlas",
                    "strategy": "atlas-json-api",
                    "selector": None,
                    "likelyShell": False,
                    "stealthRequested": False,
                    "stealthAvailable": stealth_sync is not None or Stealth is not None,
                    "stealthUsed": False,
                    "text": "",
                    "contentLinks": [],
                    "childLinks": [],
                    "candidateCount": 0,
                    "atlasDocId": atlas_id,
                    "atlasContentId": content_id,
                    "atlasContentUrl": content_url,
                    "error": (
                        f"Atlas content endpoint returned an empty body (HTTP {content_status}) "
                        f"for content id '{content_id}'. The page may have been renamed or removed; "
                        f"verify the URL or browse the document at get_document/{atlas_id}."
                    ),
                }

            title = title or descriptor.get("doc_title") or "Untitled"
            text = html_to_text(content_html)
            links = extract_atlas_links(content_html, url)
            likely_shell = looks_like_shell(title, text)
            ok = bool(text) and len(text) >= 300 and not likely_shell

            return {
                "ok": ok,
                "url": url,
                "httpStatus": content_status if content_status is not None else descriptor_resp.status,
                "title": title,
                "host": host,
                "hostKind": "atlas",
                "strategy": "atlas-json-api",
                "selector": None,
                "likelyShell": likely_shell,
                "stealthRequested": False,
                "stealthAvailable": stealth_sync is not None or Stealth is not None,
                "stealthUsed": False,
                "text": text,
                "contentLinks": links[:200],
                "childLinks": links[:200],
                "candidateCount": 1 if text else 0,
                "atlasDocId": atlas_id,
                "atlasContentId": content_id,
                "atlasContentUrl": content_url,
            }
        finally:
            req.dispose()


def _is_transient_miss(result: Dict[str, Any]) -> bool:
    """A failed extraction that looks like a bot-check / render timing miss
    rather than a genuine empty page — worth one retry."""
    if result.get("ok"):
        return False
    return (
        result.get("strategy") in (None, "none")
        or not (result.get("text") or "").strip()
        or result.get("likelyShell")
    )


def extract_official_salesforce_doc_with_retry(
    url: str, timeout_seconds: int, use_stealth: bool = False
) -> Dict[str, Any]:
    """Run the browser extractor, retrying once on a transient miss.

    Modern /docs/platform/ pages occasionally trip reCAPTCHA or render late on a
    cold headless load, returning no content. A single retry (preferring stealth
    when available) clears it. The better of the two attempts is returned.
    """
    result = extract_official_salesforce_doc(url, timeout_seconds, use_stealth=use_stealth)
    if not _is_transient_miss(result):
        return result

    retry_stealth = True if (stealth_sync is not None or Stealth is not None) else use_stealth
    retry = extract_official_salesforce_doc(url, timeout_seconds, use_stealth=retry_stealth)
    winner = retry if (retry.get("ok") or len(retry.get("text", "")) >= len(result.get("text", ""))) else result
    winner["retriedAfterTransientMiss"] = True
    winner["firstAttemptStrategy"] = result.get("strategy")
    return winner


def main() -> int:
    args = parse_args()
    kind = route_kind(args.url)

    if kind == "help":
        result = extract_help_salesforce(args.url, args.timeout, use_stealth=args.stealth)
        result["routedVia"] = "extract_help_salesforce"
        result.setdefault("hostKind", "help")
    elif kind == "atlas":
        result = extract_atlas_doc(args.url, args.timeout)
        result["routedVia"] = "atlas_json_content_api"
    else:
        result = extract_official_salesforce_doc_with_retry(args.url, args.timeout, use_stealth=args.stealth)
        result["routedVia"] = "generic_official_salesforce_extractor"

    dump = json.dumps(result, indent=2 if args.pretty else None)
    print(dump)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
