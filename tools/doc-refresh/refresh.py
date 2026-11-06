#!/usr/bin/env python3
"""Copy-replace refresh of skills from the live Salesforce doc site.

Driven by tools/doc-refresh/sources.json. Two kinds of skill:

mirror  — the skill's reference pages ARE the docs (e.g. agentscript).
          Pages = every guide page in the product llms.txt whose slug matches
          `discover`, plus `pinned` slugs. Each is fetched as markdown, converted
          (site-absolute links -> relative paths in the skill's folder layout,
          out-of-bundle links -> full URLs, images -> placeholder) and written
          over the local file. All-or-nothing: if any fetch fails, nothing is
          written for that skill. --bump bumps metadata.version + changelog.

curated — SKILL.md is hand-written from the docs. The raw source pages are
          copy-replaced into tools/doc-refresh/snapshots/<skill>/ (never into
          the skill). `git diff` on the snapshots is what a human / Claude
          reviews to decide whether the skill needs editing. The script never
          edits a curated skill. Per-page failures keep the old snapshot.

No content diffing anywhere — files are overwritten and git shows changes.

Standard library only (help.salesforce.com and atlas pages are fetched via the
repo's fetching-salesforce-docs extractor, which provisions its own runtime).

Usage:
  python3 tools/doc-refresh/refresh.py [--skill NAME ...] [--dry-run] [--bump]
                                       [--summary out.md] [--json out.json]
"""

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))
CONFIG_PATH = os.path.join(HERE, "sources.json")
SNAPSHOT_ROOT = os.path.join(HERE, "snapshots")
EXTRACTOR = os.path.join(REPO_ROOT, "skills", "fetching-salesforce-docs", "scripts", "extract_salesforce_doc.py")
USER_AGENT = "essential-skills-doc-refresh/1.1 (+https://github.com/salesforce-pixel/essential-skills)"
SITE = "https://developer.salesforce.com"

FENCE_RE = re.compile(r"^\s*(```|~~~)")
LINKED_IMAGE_RE = re.compile(r"\[!\[([^\]]*)\]\([^)]*\)\]\(([^)]*)\)")
STANDALONE_IMAGE_RE = re.compile(r"^(\s*)!\[[^\]]*\]\([^)]*\)\s*$")
INLINE_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
SITE_LINK_RE = re.compile(r"\]\((/docs/[^)\s#]*)(#[^)\s]*)?\)")
INDEX_LINK_RE = re.compile(r"\((https://developer\.salesforce\.com/docs/([^)\s]+)\.md)\)")

# python.org builds on macOS ship without a CA bundle; fall back to the system one
# (inherited by the extractor subprocess too). No-op if already set or elsewhere.
if sys.platform == "darwin" and not os.environ.get("SSL_CERT_FILE") and os.path.exists("/etc/ssl/cert.pem"):
    os.environ["SSL_CERT_FILE"] = "/etc/ssl/cert.pem"


class FetchError(Exception):
    pass


# ---------------------------------------------------------------- fetching

def fetch_markdown(url, attempts=3):
    last = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as resp:
                ctype = resp.headers.get("Content-Type", "")
                body = resp.read().decode("utf-8")
            if "html" in ctype or body.lstrip().startswith("<"):
                raise FetchError(f"got HTML, not markdown ({ctype})")
            if not body.strip():
                raise FetchError("empty body")
            return body
        except (urllib.error.URLError, FetchError, TimeoutError) as e:
            last = e
            if isinstance(e, urllib.error.HTTPError) and e.code == 404:
                break
            time.sleep(2 * (i + 1))
    raise FetchError(f"{url}: {last}")


def fetch_rendered(url, attempts=2):
    """Non-markdown pages (help.salesforce.com, atlas) via the docs extractor -> plain text."""
    last = None
    for _ in range(attempts):
        proc = subprocess.run([sys.executable, EXTRACTOR, "--url", url],
                              capture_output=True, text=True, timeout=300)
        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError:
            last = f"extractor exit {proc.returncode}: {proc.stderr.strip()[-300:]}"
            continue
        if data.get("ok") and data.get("text", "").strip():
            return f"# {data.get('title') or 'Untitled'}\n\nSource: {url}\n\n{data['text'].strip()}\n"
        last = data.get("error") or "extractor returned ok=false / empty text"
    raise FetchError(f"{url}: {last}")


def fetch_any(url):
    return fetch_markdown(url) if urllib.parse.urlparse(url).path.endswith(".md") else fetch_rendered(url)


def index_urls(index_url, match):
    index = fetch_markdown(index_url)
    pat = re.compile(match)
    urls = sorted({m.group(1) for m in INDEX_LINK_RE.finditer(index) if pat.search(m.group(2))})
    if not urls:
        raise FetchError(f"{index_url}: 0 pages match {match!r} — index format changed?")
    return urls


def fetch_all(urls, workers=6):
    """Return ({url: text}, {url: error})."""
    ok, bad = {}, {}
    with cf.ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(fetch_any, u): u for u in urls}
        for f in cf.as_completed(futs):
            u = futs[f]
            try:
                ok[u] = f.result()
            except Exception as e:  # noqa: BLE001 - report every failure, keep going
                bad[u] = str(e)
    return ok, bad


def write_if_changed(path, text, dry_run):
    old = None
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = f.read()
    if old == text:
        return "unchanged"
    if not dry_run:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    return "new" if old is None else "changed"


# ---------------------------------------------------------------- mirror skills

def page_dir(slug, cfg):
    for rule in cfg["layout"]:
        if re.search(rule["match"], slug):
            return rule["dir"]
    return ""


def convert(slug, text, slugs, cfg):
    here = page_dir(slug, cfg)
    guide = cfg["guide_path"]

    def fix_link(m):
        path, frag = m.group(1), m.group(2) or ""
        if path.startswith(guide) and path.endswith(".md"):
            target = path[len(guide):-3]
            if target in slugs:
                rel = os.path.relpath(os.path.join(page_dir(target, cfg), target + ".md"), here or ".")
                return f"]({rel}{frag})"
        return f"]({cfg['site_root']}{path}{frag})"

    out, in_fence = [], False
    for line in text.split("\n"):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if not in_fence:
            line = LINKED_IMAGE_RE.sub(r"[\1](\2)", line)
            m = STANDALONE_IMAGE_RE.match(line)
            if m:
                line = m.group(1) + cfg["image_placeholder"]
            else:
                line = INLINE_IMAGE_RE.sub("*[Image removed]*", line)
            line = SITE_LINK_RE.sub(fix_link, line)
        out.append(line)
    text = "\n".join(out)
    return text if text.endswith("\n") else text + "\n"


def bump_skill_md(path, today, changed, new, orphans):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    m = re.search(r'^(\s*version:\s*")(\d+)\.(\d+)(")', src, re.M)
    if not m:
        raise SystemExit(f"{path}: no metadata.version found")
    old_v = f"{m.group(2)}.{m.group(3)}"
    new_v = f"{m.group(2)}.{int(m.group(3)) + 1}"
    src = src[: m.start()] + f"{m.group(1)}{new_v}{m.group(4)}" + src[m.end():]

    lines = [f"{new_v} — Automated copy-replace refresh from the live doc site ({today})."]
    lines.append(f"      • {len(changed)} page(s) changed" + (f", {len(new)} new" if new else "") + ".")
    if changed:
        lines.append("      • Changed: " + ", ".join(sorted(changed)) + ".")
    if new:
        lines.append("      • New (add to the SKILL.md index): " + ", ".join(sorted(new)) + ".")
    if orphans:
        lines.append("      • No longer upstream (kept, review): " + ", ".join(sorted(orphans)) + ".")
    entry = "\n".join(lines) + "\n"
    src, n = re.subn(r"(<!--\s*\nChangelog\n)", lambda mm: mm.group(1) + entry, src, count=1)
    if n == 0:
        raise SystemExit(f"{path}: no 'Changelog' comment block found")

    src = re.sub(r"(live doc site on )\d{4}-\d{2}-\d{2}", rf"\g<1>{today}", src)
    src = re.sub(r"(live site )\d{4}-\d{2}-\d{2}", rf"\g<1>{today}", src)
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    return old_v, new_v


def refresh_mirror(name, cfg, dry_run, bump, today):
    skill_dir = os.path.join(REPO_ROOT, cfg["skill_dir"])
    dest = os.path.join(skill_dir, cfg["dest"])
    prefix = cfg["site_root"] + cfg["guide_path"]
    discovered = {u[len(prefix):-3] for u in index_urls(cfg["index"], ".") if u.startswith(prefix)}
    discovered = {s for s in discovered if re.match(cfg["discover"], s)}
    if not discovered:
        raise FetchError(f"{cfg['index']}: discovered 0 pages for {name}")
    slugs = discovered | set(cfg.get("pinned", []))

    raw, bad = fetch_all([prefix + s + ".md" for s in sorted(slugs)])
    if bad:  # all-or-nothing for mirrors
        raise FetchError("; ".join(f"{u}: {e}" for u, e in sorted(bad.items())))

    status = {"changed": [], "new": [], "unchanged": []}
    for slug in sorted(slugs):
        text = convert(slug, raw[prefix + slug + ".md"], slugs, cfg)
        path = os.path.join(dest, page_dir(slug, cfg), slug + ".md")
        status[write_if_changed(path, text, dry_run)].append(slug)

    managed = {os.path.normpath(os.path.join(dest, page_dir(s, cfg), s + ".md")) for s in slugs}
    orphans = sorted(os.path.relpath(os.path.join(r, f), dest)
                     for r, _, fs in os.walk(dest) for f in fs
                     if f.endswith(".md") and os.path.normpath(os.path.join(r, f)) not in managed)

    version = None
    if bump and not dry_run and (status["changed"] or status["new"]):
        version = bump_skill_md(os.path.join(skill_dir, "SKILL.md"), today, status["changed"], status["new"], orphans)

    return {"skill": name, "kind": "mirror", "pages": len(slugs),
            "detail": f"{len(discovered)} from llms.txt, {len(cfg.get('pinned', []))} pinned",
            "changed": status["changed"], "new": status["new"], "unchanged": len(status["unchanged"]),
            "removed": orphans, "failed": {}, "version": version}


# ---------------------------------------------------------------- curated skills

def snapshot_rel(url):
    """Stable, readable snapshot path for a source URL."""
    u = urllib.parse.urlparse(url)
    if u.netloc == "help.salesforce.com":
        art = urllib.parse.parse_qs(u.query).get("id", ["unknown"])[0]
        return os.path.join("help", re.sub(r"\.htm$", "", art) + ".md")
    path = u.path[len("/docs/"):] if u.path.startswith("/docs/") else u.path.lstrip("/")
    if not path.endswith(".md"):
        path = re.sub(r"\.html?$", "", path) + ".md"
    return path


def refresh_curated(name, cfg, dry_run, today):
    snap_dir = os.path.join(SNAPSHOT_ROOT, name)
    urls, index_errors = set(), {}
    for src in cfg["sources"]:
        if "index" in src:
            try:
                urls.update(index_urls(src["index"], src.get("match", ".")))
            except FetchError as e:
                index_errors[src["index"]] = str(e)
        urls.update(src.get("urls", []))

    got, bad = fetch_all(sorted(urls))
    bad.update(index_errors)

    status = {"changed": [], "new": [], "unchanged": []}
    for url in sorted(got):
        rel = snapshot_rel(url)
        status[write_if_changed(os.path.join(snap_dir, rel), got[url], dry_run)].append(rel)

    # Snapshots for URLs no longer in the source set are removed (they aren't
    # shipped, and the deletion in git is the signal that a page went away).
    # If an index failed to load, skip this so a transient outage can't wipe it.
    keep = {snapshot_rel(u) for u in urls}
    removed = []
    if not index_errors and os.path.isdir(snap_dir):
        for r, _, fs in os.walk(snap_dir):
            for f in fs:
                rel = os.path.relpath(os.path.join(r, f), snap_dir)
                if rel not in keep:
                    removed.append(rel)
                    if not dry_run:
                        os.remove(os.path.join(r, f))
    return {"skill": name, "kind": "curated", "pages": len(urls), "detail": f"snapshots in tools/doc-refresh/snapshots/{name}/",
            "changed": status["changed"], "new": status["new"], "unchanged": len(status["unchanged"]),
            "removed": sorted(removed), "failed": bad, "version": None}


# ---------------------------------------------------------------- reporting

def summary_md(results, errors, today):
    def ticks(xs):
        return ", ".join(f"`{x}`" for x in xs)
    out = [f"## Doc refresh — {today}", ""]
    for r in results:
        head = f"### `{r['skill']}` ({r['kind']})"
        if r["version"]:
            head += f" — {r['version'][0]} → {r['version'][1]}"
        out += [head, f"{r['pages']} pages ({r['detail']}): {len(r['changed'])} changed, "
                      f"{len(r['new'])} new, {len(r['removed'])} removed, {r['unchanged']} unchanged, "
                      f"{len(r['failed'])} failed."]
        if r["changed"]:
            out.append(f"- **Changed:** {ticks(r['changed'])}")
        if r["new"]:
            out.append(f"- **New:** {ticks(r['new'])}")
        if r["removed"]:
            out.append(f"- **Removed upstream:** {ticks(r['removed'])}")
        for u, e in sorted(r["failed"].items()):
            out.append(f"- **Fetch failed** (old snapshot kept): {u} — {e}")
        out.append("")
    for name, err in errors:
        out += [f"### `{name}` — FAILED, nothing written", "", "```", err, "```", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skill", action="append", help="skill name from sources.json (default: all)")
    ap.add_argument("--dry-run", action="store_true", help="fetch and report, write nothing")
    ap.add_argument("--bump", action="store_true", help="mirror skills: bump version + changelog when files change")
    ap.add_argument("--summary", help="write a markdown summary to this path")
    ap.add_argument("--json", help="write the machine-readable result to this path")
    args = ap.parse_args()

    with open(CONFIG_PATH, encoding="utf-8") as f:
        config = json.load(f)["skills"]
    names = args.skill or list(config)
    unknown = [n for n in names if n not in config]
    if unknown:
        raise SystemExit(f"unknown skill(s): {', '.join(unknown)}")
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()

    results, errors = [], []
    for name in names:
        cfg = config[name]
        print(f"[doc-refresh] {name} ({cfg['kind']})", file=sys.stderr)
        try:
            if cfg["kind"] == "mirror":
                results.append(refresh_mirror(name, cfg, args.dry_run, args.bump, today))
            else:
                results.append(refresh_curated(name, cfg, args.dry_run, today))
        except FetchError as e:
            errors.append((name, str(e)))

    payload = {"date": today, "results": results, "errors": [{"skill": n, "error": e} for n, e in errors]}
    for out in (args.summary, args.json):
        if out:
            os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    if args.summary:
        with open(args.summary, "w", encoding="utf-8") as f:
            f.write(summary_md(results, errors, today))
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    print(summary_md(results, errors, today))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
