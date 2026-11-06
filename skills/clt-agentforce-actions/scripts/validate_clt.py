#!/usr/bin/env python3
"""Static checks for Custom Lightning Type bundles (lightningTypes/<type>/...).

Usage:
  python3 -I validate_clt.py <dir> [<dir> ...]

<dir> can be a DX project, a package dir (force-app), a `lightningTypes` folder, or a
single type folder. LWCs and Apex classes are looked up in sibling `lwc/` and `classes/`
folders next to each `lightningTypes/` folder. When they aren't there, the check
reports a WARN and the cross-file checks are skipped.

Prints PASS / WARN / FAIL lines. Exit code 1 if any FAIL. Standard library only.
Rules come from the Lightning Types docs and forcedotcom/sf-skills; see
references/sources.md for where they disagree. A check-only deploy is still the
final word (`sf project deploy start --dry-run ...`).
"""

import json
import os
import re
import sys

CHANNELS = {"lightningDesktopGenAi", "enhancedWebChat", "lightningMobileGenAi", "experienceBuilder"}
GENAI_CHANNELS = CHANNELS - {"experienceBuilder"}
STANDARD_TYPES = {
    "lightning__booleanType", "lightning__dateType", "lightning__dateTimeType",
    "lightning__dateTimeStringType", "lightning__integerType", "lightning__multilineTextType",
    "lightning__numberType", "lightning__objectType", "lightning__richTextType",
    "lightning__textType", "lightning__timeType", "lightning__urlType", "lightning__listType",
    "lightning__recordInfoType",
}
APEX_KEYS = {"title", "description", "lightning:type"}
ATTR_RE = re.compile(r"\{!\$attrs\.([A-Za-z_][\w]*)")

results = []


def log(level, where, msg):
    results.append((level, where, msg))


def load_json(path, where):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        hint = " (JSON has no comments: remove // lines copied from docs)" if "//" in open(path, encoding="utf-8").read() else ""
        log("FAIL", where, f"invalid JSON: {e}{hint}")
    except OSError as e:
        log("FAIL", where, f"can't read: {e}")
    return None


def find_type_dirs(path):
    path = os.path.abspath(path)
    if os.path.isfile(os.path.join(path, "schema.json")):
        return [path]
    out = []
    for root, dirs, _ in os.walk(path):
        dirs[:] = [d for d in dirs if d not in {"node_modules", ".git", ".sfdx", ".sf"}]
        if os.path.basename(root) == "lightningTypes":
            out += [os.path.join(root, d) for d in sorted(dirs)]
            dirs[:] = []
    return out


def lwc_meta(type_dir, name):
    base = os.path.dirname(os.path.dirname(type_dir))  # .../default
    p = os.path.join(base, "lwc", name, f"{name}.js-meta.xml")
    return p if os.path.exists(p) else None


def apex_file(type_dir, cls):
    base = os.path.dirname(os.path.dirname(type_dir))
    p = os.path.join(base, "classes", f"{cls}.cls")
    return p if os.path.exists(p) else None


def check_schema(tdir, name):
    where = f"{name}/schema.json"
    p = os.path.join(tdir, "schema.json")
    if not os.path.exists(p):
        log("FAIL", name, "missing schema.json")
        return None, None
    s = load_json(p, where)
    if not isinstance(s, dict):
        return None, None
    fails_before = sum(1 for r in results if r[0] == "FAIL")
    ok = True
    if "$schema" in s:
        log("FAIL", where, 'remove "$schema" (CLT validator rejects it)'); ok = False
    if not s.get("title"):
        log("FAIL", where, "missing required title"); ok = False
    lt = s.get("lightning:type")
    if not lt:
        log("FAIL", where, "missing required lightning:type"); return s, None

    if lt.startswith("@apexClassType/"):
        kind = "apex"
        extra = set(s) - APEX_KEYS
        if extra:
            log("FAIL", where, f"Apex-based schema allows only title/description/lightning:type; remove {sorted(extra)}"); ok = False
        m = re.match(r"@apexClassType/([A-Za-z0-9]+)__([A-Za-z_]\w*)(\$\w+)?$", lt)
        if not m:
            log("FAIL", where, f"malformed Apex reference {lt!r} (expected @apexClassType/c__ClassName)"); ok = False
        else:
            ns, cls, inner = m.groups()
            if inner:
                log("WARN", where, f"inner class {cls}{inner}: docs require top-level classes (works in some orgs; risky in namespaced orgs/packages)")
            af = apex_file(tdir, cls) if ns == "c" else None
            if ns == "c" and not af:
                log("WARN", where, f"classes/{cls}.cls not found next to lightningTypes; Apex checks skipped")
            elif af:
                check_apex(af, cls, where)
    elif lt == "lightning__objectType":
        kind = "object"
        props = s.get("properties")
        if not isinstance(props, dict) or not props:
            log("FAIL", where, "object-based schema needs a non-empty properties block"); ok = False
            props = {}
        if s.get("type") != "object" or s.get("unevaluatedProperties") is not False:
            log("WARN", where, 'sf-skills requires root "type": "object" and "unevaluatedProperties": false (docs examples omit them); add if deploy rejects the schema')
        if s.get("unevaluatedProperties") is True:
            log("FAIL", where, "unevaluatedProperties must be false"); ok = False
        if "examples" in s and s.get("unevaluatedProperties") is False:
            log("FAIL", where, '"examples" not allowed with unevaluatedProperties: false'); ok = False
        for r in s.get("required", []) or []:
            if r not in props:
                log("FAIL", where, f"required lists unknown property {r!r}"); ok = False
        for pn, pv in props.items():
            check_property(pv, f"{where}#{pn}", root_level=True)
    else:
        kind = "other"
        log("WARN", where, f"root lightning:type {lt!r} is neither @apexClassType/... nor lightning__objectType")
    if ok and sum(1 for r in results if r[0] == "FAIL") == fails_before:
        log("PASS", where, f"{kind}-based schema")
    return s, kind


def check_property(pv, where, root_level):
    if not isinstance(pv, dict):
        log("FAIL", where, "property definition must be an object"); return
    lt = pv.get("lightning:type")
    if "items" in pv:
        log("WARN", where, '"items" is often rejected by the CLT metaschema; prefer removing it')
    if lt == "lightning__objectType":
        log("FAIL", where, "properties must not use lightning__objectType; reference a CLT (c__Type) or an Apex class type")
    if pv.get("type") == "array" and not root_level and lt == "lightning__listType":
        log("FAIL", where, 'nested arrays: use "type": "array" only, no lightning__listType')
    if lt and not (lt in STANDARD_TYPES or re.match(r"^[A-Za-z0-9]+__\w+$", lt) or lt.startswith("@apexClassType/")):
        log("FAIL", where, f"unknown lightning:type {lt!r} (check spelling, e.g. lightning__richTextType)")
    elif lt and lt.startswith("lightning__") and lt not in STANDARD_TYPES:
        log("FAIL", where, f"unknown standard type {lt!r}")
    for k, v in (pv.get("properties") or {}).items():
        check_property(v, f"{where}.{k}", root_level=False)


def check_apex(path, cls, where):
    src = open(path, encoding="utf-8").read()
    code = re.sub(r"//[^\n]*|/\*.*?\*/", "", src, flags=re.S)
    if not re.search(rf"\bglobal\s+(?:(?:with|without|inherited)\s+sharing\s+)?(?:virtual\s+|abstract\s+)?class\s+{cls}\b", code, re.I):
        log("WARN", where, f"{cls}.cls: class should be global (public can fail in namespaced orgs/packages)")
    if not re.search(r"@JsonAccess\s*\(", code, re.I):
        log("WARN", where, f"{cls}.cls: add @JsonAccess(serializable='always' deserializable='always')")
    if not re.search(r"@AuraEnabled", code, re.I):
        log("WARN", where, f"{cls}.cls: no @AuraEnabled fields; schema projection exposes only @AuraEnabled members")


def walk_overrides(cfg):
    """Yield (path, key, override) for every componentOverrides entry."""
    for top in ("editor", "renderer"):
        if isinstance(cfg.get(top), dict):
            for k, v in (cfg[top].get("componentOverrides") or {}).items():
                yield top, k, v
    coll = cfg.get("collection")
    if isinstance(coll, dict):
        for top in ("editor", "renderer"):
            if isinstance(coll.get(top), dict):
                for k, v in (coll[top].get("componentOverrides") or {}).items():
                    yield f"collection.{top}", k, v


def check_layout(node, where):
    if isinstance(node, dict):
        if node.get("definition") == "lightning/propertyLayout":
            extra = set((node.get("attributes") or {})) - {"property"}
            if extra:
                log("FAIL", where, f"lightning/propertyLayout accepts only 'property'; remove {sorted(extra)}")
        for c in node.get("children", []) or []:
            check_layout(c, where)


def check_ui_file(tdir, name, rel, role, channel, schema, kind):
    where = f"{name}/{rel}"
    cfg = load_json(os.path.join(tdir, rel), where)
    if not isinstance(cfg, dict):
        return
    allowed_top = {"editor", "collection"} if role == "editor" else {"renderer", "collection"}
    bad = set(cfg) - allowed_top
    if bad:
        log("FAIL", where, f"unexpected top-level keys {sorted(bad)} (allowed: {sorted(allowed_top)})")
    for top in ("editor", "renderer"):
        for container in (cfg.get(top), (cfg.get("collection") or {}).get(top)):
            if isinstance(container, dict):
                for legacy in ("propertyRenderers", "view"):
                    if legacy in container:
                        log("FAIL", where, f"legacy key {legacy!r}: use componentOverrides / layout")
                if "layout" in container:
                    check_layout(container["layout"], where)
    props = set((schema or {}).get("properties", {}) or {})
    fails_before = sum(1 for r in results if r[0] == "FAIL")
    n = 0
    for path, key, ov in walk_overrides(cfg):
        n += 1
        w = f"{where} {path}.componentOverrides[{key!r}]"
        if not isinstance(ov, dict) or not ov.get("definition"):
            log("FAIL", w, "override needs a definition"); continue
        d = ov["definition"]
        if key != "$" and kind == "object" and key not in props:
            log("FAIL", w, f"property override {key!r} not in schema properties")
        attrs = ov.get("attributes") or {}
        if attrs and kind == "apex" and key == "$" and not d.startswith("@widget/"):
            log("WARN", w, "attributes on an Apex-based type: sf-skills reports unevaluatedProperties rejection; prefer reading @api value (see references/sources.md #1)")
        if kind == "object":
            for ak, av in attrs.items():
                for ref in ATTR_RE.findall(str(av)):
                    if ref not in props:
                        log("FAIL", w, f"attribute {ak!r} maps $attrs.{ref}, which isn't a schema property")
        if d.startswith("@widget/"):
            log("FAIL", w, "widget definitions belong in a root-level renderer.json, not a channel folder (see hxl-widget-builder)")
            continue
        m = re.match(r"^([A-Za-z0-9]+)/([A-Za-z][\w]*)$", d)
        if not m:
            log("FAIL", w, f"malformed definition {d!r} (expected c/componentName)"); continue
        ns, comp = m.groups()
        if ns != "c":
            if ns not in {"es_property_editors", "lightning"}:
                log("WARN", w, f"namespace {ns!r}: use 'c' for components in this org/package, the package namespace only for installed packages")
            continue
        meta = lwc_meta(tdir, comp)
        if not meta:
            log("WARN", w, f"lwc/{comp} not found next to lightningTypes; target check skipped")
            continue
        xml = open(meta, encoding="utf-8").read()
        if channel == "experienceBuilder" or (kind == "object" and key != "$"):
            need = "lightning__PropertyEditor"
        else:
            need = "lightning__AgentforceInput" if role == "editor" else "lightning__AgentforceOutput"
        if f"<target>{need}</target>" not in xml:
            log("FAIL", w, f"lwc/{comp}/{comp}.js-meta.xml must include <target>{need}</target>")
        if not re.search(r"<isExposed>\s*true\s*</isExposed>", xml):
            log("FAIL", w, f"lwc/{comp}: isExposed must be true")
        js = os.path.join(os.path.dirname(meta), f"{comp}.js")
        if os.path.exists(js):
            jsrc = open(js, encoding="utf-8").read()
            if role == "editor" and "valuechange" not in jsrc:
                log("WARN", w, f"lwc/{comp}: editors must dispatch a 'valuechange' CustomEvent with detail.value")
            if not attrs and not re.search(r"@api\s+(get\s+)?value\b", jsrc):
                log("WARN", w, f"lwc/{comp}: no @api value; without attributes mapping the data arrives in value")
    if n == 0:
        log("FAIL", where, "no componentOverrides found")
    elif sum(1 for r in results if r[0] == "FAIL") == fails_before:
        log("PASS", where, f"{n} override(s)")


def check_type(tdir):
    name = os.path.basename(tdir)
    if not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", name):
        log("FAIL", name, "type folder name must be alphanumeric/underscore, starting with a letter")
    schema, kind = check_schema(tdir, name)
    for entry in sorted(os.listdir(tdir)):
        full = os.path.join(tdir, entry)
        if entry == "schema.json" or entry.startswith("."):
            continue
        if os.path.isfile(full):
            if entry == "renderer.json":
                cfg = load_json(full, f"{name}/renderer.json") or {}
                defs = [ov.get("definition", "") for _, _, ov in walk_overrides(cfg) if isinstance(ov, dict)]
                if defs and all(d.startswith("@widget/") for d in defs):
                    log("PASS", f"{name}/renderer.json", "root-level widget renderer (validate with hxl-widget-builder)")
                else:
                    log("FAIL", f"{name}/renderer.json", "root-level renderer.json is only for @widget/ renderers; move LWC overrides into a channel folder")
            elif entry == "editor.json":
                log("FAIL", f"{name}/editor.json", "editor.json must be inside a channel folder")
            elif not entry.endswith("-meta.xml"):
                log("WARN", f"{name}/{entry}", "unexpected file in type folder")
            continue
        if entry not in CHANNELS:
            log("FAIL", f"{name}/{entry}", f"unknown channel folder; use one of {sorted(CHANNELS)}")
            continue
        if kind == "apex" and entry == "experienceBuilder":
            log("FAIL", f"{name}/{entry}", "Apex-based types aren't supported in Experience Builder")
        if kind == "object" and entry in GENAI_CHANNELS:
            log("WARN", f"{name}/{entry}", "agent-action channels are documented for Apex-based types")
        files = set(os.listdir(full))
        for fn in sorted(files - {"editor.json", "renderer.json"}):
            log("WARN", f"{name}/{entry}/{fn}", "unexpected file (expected editor.json / renderer.json)")
        if "renderer.json" in files and entry == "experienceBuilder":
            log("FAIL", f"{name}/{entry}/renderer.json", "renderer.json isn't supported in experienceBuilder")
        for fn, role in (("editor.json", "editor"), ("renderer.json", "renderer")):
            if fn in files:
                check_ui_file(tdir, name, f"{entry}/{fn}", role, entry, schema, kind)


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    types = []
    for a in argv:
        if not os.path.isdir(a):
            print(f"FAIL  {a}: not a directory")
            return 1
        types += find_type_dirs(a)
    if not types:
        print("FAIL  no lightningTypes/<type>/ folders found")
        return 1
    for t in types:
        check_type(t)
    for level, where, msg in results:
        print(f"{level:<5} {where}: {msg}")
    fails = sum(1 for r in results if r[0] == "FAIL")
    warns = sum(1 for r in results if r[0] == "WARN")
    print(f"\n{len(types)} type(s), {fails} FAIL, {warns} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
