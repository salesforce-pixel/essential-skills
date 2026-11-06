#!/usr/bin/env python3
"""
validate_hxl.py — static checks for Salesforce HXL widget bundles and the
custom Lightning types (CLTs) that render them.

Usage:
    python3 validate_hxl.py <path> [<path> ...] [--strict]

<path> can be an SFDX project root, a force-app dir, a uiWidgets/<name> dir,
a lightningTypes/<name> dir, or an .mcpServerDefinition-meta.xml file. The script
discovers every `uiWidgets/*`, `lightningTypes/*` and `mcpServerDefinitions/*` beneath
the given paths.

Static checks can't catch everything: also run a check-only deploy
(`sf project deploy validate`) before the real one.

Exit code: 0 = no FAIL, 1 = at least one FAIL (with --strict, WARN also fails).
Stdlib only.
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# ----------------------------------------------------------------------------
# Known vocab (Beta docs + sf-skills). Unknown components are WARN, not FAIL,
# because Dev Preview components exist and the palette evolves.
# ----------------------------------------------------------------------------
BETA_COMPONENTS = {
    "tile/widget", "tile/accordion", "tile/accordionItem", "tile/avatar", "tile/badge",
    "tile/button", "tile/callout", "tile/code", "tile/column", "tile/container",
    "tile/icon", "tile/image", "tile/link", "tile/list", "tile/listItem", "tile/markdown",
    "tile/progress", "tile/row", "tile/separator", "tile/spacer", "tile/spinner",
    "tile/table", "tile/text",
}
# Attribute names per component, from the official reference pages
# (developer.salesforce.com/docs/platform/hxl/references/hxl-reference-about/<name>.md),
# verified 2026-09-21. The deploy rejects unknown attributes ("additionalProperties is
# set to false"). Components absent from this map are not checked. "Required" in the
# docs is NOT enforced by deploy (rows/columns without gap/align deploy fine), so only
# names are checked here.
COMPONENT_ATTRS = {
    "tile/row": {"align", "gap", "isWrapped", "justify"},
    "tile/column": {"align", "gap", "width"},
    "tile/text": {"color", "isItalic", "isStrikethrough", "text", "variant", "weight"},
    "tile/badge": {"label", "variant"},
    "tile/callout": {"description", "iconAlt", "title", "variant"},
    "tile/icon": {"alt", "color", "name", "size"},
    "tile/progress": {"color", "label", "max", "shape", "size", "value"},
    "tile/container": {"borderless", "variant"},
    "tile/button": {"actions", "iconName", "label", "variant"},
    "tile/separator": {"orientation"},
    "tile/spacer": {"size"},
    "tile/link": {"href", "text", "underline", "variant"},
    "tile/list": {"marker"},
    "tile/image": {"alt", "size", "src"},
    "tile/avatar": {"alt", "iconName", "initials", "shape", "size", "src"},
    "tile/markdown": {"source"},
    "tile/table": {"appearance", "caption", "columns", "isStickyHeader", "pagination", "rows", "size", "sort"},
    "tile/accordionItem": {"iconAlt", "iconName", "isExpanded", "subtitle", "title"},
    "tile/code": {"code", "language"},
    "tile/spinner": {"label", "size"},
}
ATTR_HINTS = {
    ("tile/row", "wrap"): "isWrapped",
    ("tile/link", "url"): "href",
    ("tile/link", "label"): "text",
    ("tile/markdown", "text"): "source",
    ("tile/button", "icon"): "iconName",
}
PLAIN_REF_RE = re.compile(r"^\s*\$[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\s*$")
ACTIONS = {"action/openLink": "url", "action/sendMessage": "content"}
FUNCTIONS = {
    "IF", "CASE", "AND", "OR", "NOT", "ISNULL", "ISBLANK",
    "UPPER", "LOWER", "LEFT", "RIGHT", "MID", "LEN", "TRIM", "REVERSE", "SUBSTITUTE",
    "FIND", "LPAD", "RPAD", "TEXT", "VALUE", "CONTAINS", "BEGINS",
    "MOD", "MAX", "MIN", "ROUND", "ABS", "SQRT", "CEILING", "FLOOR", "MCEILING",
    "MFLOOR", "LOG", "EXP", "LN",
    "DATEVALUE", "DATETIMEVALUE", "TIMEVALUE", "DAY", "MONTH", "YEAR", "WEEKDAY",
    "ADDMONTHS", "TODAY", "NOW", "TIMENOW", "DATE", "HOUR", "MINUTE", "SECOND",
    "MILLISECOND",
    "NULLVALUE", "BLANKVALUE", "HTMLENCODE", "JSENCODE",
    "ISNUMBER", "REGEX",
}
PRIMITIVE_TYPES = {
    "lightning__textType", "lightning__multilineTextType", "lightning__richTextType",
    "lightning__urlType", "lightning__dateType", "lightning__timeType",
    "lightning__dateTimeType", "lightning__numberType", "lightning__integerType",
    "lightning__booleanType", "lightning__objectType", "lightning__listType",
    "lightning__markdownTextType",
}


class Report:
    def __init__(self):
        self.rows = []

    def add(self, scope, check, status, detail=""):
        self.rows.append((scope, check, status, detail))

    def ok(self, scope, check, detail=""):
        self.add(scope, check, "PASS", detail)

    def fail(self, scope, check, detail):
        self.add(scope, check, "FAIL", detail)

    def warn(self, scope, check, detail):
        self.add(scope, check, "WARN", detail)

    def print(self):
        cur = None
        for scope, check, status, detail in self.rows:
            if scope != cur:
                print(f"\n== {scope}")
                cur = scope
            line = f"  [{status}] {check}"
            if detail:
                line += f" — {detail}"
            print(line)
        n = {s: sum(1 for r in self.rows if r[2] == s) for s in ("PASS", "WARN", "FAIL")}
        print(f"\nSummary: {n['PASS']} pass, {n['WARN']} warn, {n['FAIL']} fail")
        return n


def load_json(path, rep, scope, check):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        rep.ok(scope, check)
        return data
    except FileNotFoundError:
        rep.fail(scope, check, f"missing {path.name}")
    except json.JSONDecodeError as e:
        rep.fail(scope, check, f"{path.name}: {e}")
    return None


# ----------------------------------------------------------------------------
# Expression parsing
# ----------------------------------------------------------------------------
def extract_expressions(s):
    """Return the inner text of every {!...} in s, honoring quotes/nesting."""
    out, i = [], 0
    while True:
        start = s.find("{!", i)
        if start < 0:
            return out
        j, depth, quote = start + 2, 1, None
        while j < len(s):
            c = s[j]
            if quote:
                if c == "\\":
                    j += 1
                elif c == quote:
                    quote = None
            elif c in ("'", '"'):
                quote = c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        out.append(s[start + 2:j])
        i = j + 1


def strip_strings(expr):
    return re.sub(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"", "''", expr)


REF_RE = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)((?:\.[A-Za-z_][A-Za-z0-9_]*)*)")
FUNC_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(")


def refs_and_funcs(expr):
    clean = strip_strings(expr)
    refs = [(m.group(1), [p for p in m.group(2).split(".") if p]) for m in REF_RE.finditer(clean)]
    funcs = [m.group(1) for m in FUNC_RE.finditer(clean)]
    return refs, funcs


def all_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from all_strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from all_strings(v)


# ----------------------------------------------------------------------------
# Widget bundle
# ----------------------------------------------------------------------------
def schema_attr_props(schema):
    try:
        return schema["properties"]["attributes"]["properties"]
    except (KeyError, TypeError):
        return None


def check_widget_schema(schema, rep, scope):
    if schema is None:
        return None
    errs = []
    if not isinstance(schema.get("title"), str):
        errs.append("root 'title' missing")
    if schema.get("type") != "object":
        errs.append("root 'type' must be \"object\"")
    attrs = (schema.get("properties") or {}).get("attributes")
    if not isinstance(attrs, dict):
        errs.append("missing properties.attributes")
    else:
        if attrs.get("lightning:type") != "lightning__objectType":
            errs.append("properties.attributes lightning:type must be lightning__objectType")
        if not isinstance(attrs.get("properties"), dict):
            errs.append("properties.attributes.properties map missing")
    if "unevaluatedProperties" in schema:
        rep.warn(scope, "schema-root-keys", "unevaluatedProperties belongs on CLTs, not widget schema")
    if errs:
        rep.fail(scope, "schema-root-keys", "; ".join(errs))
        return None
    rep.ok(scope, "schema-root-keys")

    props = attrs["properties"]
    leaf_errs = []
    for name, p in props.items():
        lt = p.get("lightning:type") if isinstance(p, dict) else None
        if not lt:
            leaf_errs.append(f"{name}: no lightning:type")
            continue
        if lt == "lightning__listType":
            items = p.get("items") or {}
            it = items.get("lightning:type")
            if not it:
                leaf_errs.append(f"{name}: list without items.lightning:type")
            elif it == "lightning__objectType" and not isinstance(items.get("properties"), dict):
                leaf_errs.append(f"{name}: object list needs items.properties")
        elif lt not in PRIMITIVE_TYPES and not lt.startswith("@apexClassType/"):
            rep.warn(scope, "schema-leaf-types", f"{name}: unusual lightning:type '{lt}'")
        if name == "outputValues":
            rep.warn(scope, "schema-flat", "widget schema contains 'outputValues' — keep widget schema flat; nesting belongs in the MCP wrapper renderer")
    if leaf_errs:
        rep.fail(scope, "schema-leaf-types", "; ".join(leaf_errs))
    else:
        rep.ok(scope, "schema-leaf-types", f"{len(props)} attributes")
    return props


def item_fields(prop):
    """Known fields of list items if declared inline; None = unknown (Apex type)."""
    items = (prop or {}).get("items") or {}
    if isinstance(items.get("properties"), dict):
        return items["properties"]
    return None


def check_composition(comp, props, rep, scope):
    if comp is None:
        return
    env_errs = []
    if comp.get("type") != "lightning__agentforceWidget":
        env_errs.append("type must be lightning__agentforceWidget")
    body = ((comp.get("contentBody") or {}).get("widgetBody"))
    if not isinstance(body, dict):
        env_errs.append("contentBody.widgetBody missing")
    elif body.get("definition") != "tile/widget":
        env_errs.append("widgetBody.definition must be tile/widget")
    extra = set(comp.keys()) - {"type", "contentBody"}
    if extra:
        env_errs.append(f"unexpected top-level keys {sorted(extra)}")
    if env_errs:
        rep.fail(scope, "body-envelope", "; ".join(env_errs))
        if not isinstance(body, dict):
            return
    else:
        rep.ok(scope, "body-envelope")

    problems = {"structure": [], "bindings": [], "funcs": [], "buttons": [], "meta": [], "attrs": []}
    stats = {"h1": 0, "primary": 0, "unknown": set(), "nodes": 0}
    attr_formulas = []  # non-plain expressions that reference $attrs (break in MCP channel)
    props = props or {}

    def walk(node, path, scope_vars):
        stats["nodes"] += 1
        if not isinstance(node, dict):
            problems["structure"].append(f"{path}: node is not an object")
            return
        if "type" in node:
            problems["structure"].append(f"{path}: node has a 'type' key")
        d = node.get("definition")
        if not isinstance(d, str) or not re.match(r"^[a-z]+/[A-Za-z]+$", d):
            problems["structure"].append(f"{path}: bad definition {d!r}")
            d = str(d)
        elif d not in BETA_COMPONENTS:
            stats["unknown"].add(d)
        if d == "tile/widget" and path != "widgetBody":
            problems["structure"].append(f"{path}: tile/widget only allowed as root")
        path = f"{path}>{d.split('/')[-1]}"

        attrs = node.get("attributes") or {}
        meta = node.get("meta") or {}
        new_vars = dict(scope_vars)

        # meta checks — forEach resolved in the PARENT scope
        if meta:
            unknown_meta = set(meta) - {"if", "forEach", "forItem", "forIndex"}
            if unknown_meta:
                problems["meta"].append(f"{path}: unknown meta keys {sorted(unknown_meta)}")
            if "forEach" in meta:
                fe = meta["forEach"]
                exprs = extract_expressions(fe) if isinstance(fe, str) else []
                if len(exprs) != 1 or fe.strip() != "{!" + exprs[0] + "}":
                    problems["meta"].append(f"{path}: forEach must be a single {{!...}} expression")
                item_var = meta.get("forItem", "$Item")
                if not str(item_var).startswith("$"):
                    problems["meta"].append(f"{path}: forItem '{item_var}' must start with $")
                if item_var in scope_vars:
                    problems["meta"].append(f"{path}: forItem '{item_var}' shadows an outer loop variable")
                # infer item fields
                fields = None
                if exprs:
                    refs, _ = refs_and_funcs(exprs[0])
                    if refs:
                        root, parts = refs[0]
                        if root == "attrs" and len(parts) == 1:
                            fields = item_fields(props.get(parts[0]))
                new_vars[item_var.lstrip("$")] = fields
                if "forIndex" in meta:
                    iv = meta["forIndex"]
                    if not str(iv).startswith("$"):
                        problems["meta"].append(f"{path}: forIndex '{iv}' must start with $")
                    new_vars[str(iv).lstrip("$")] = "INDEX"
            elif "forItem" in meta or "forIndex" in meta:
                problems["meta"].append(f"{path}: forItem/forIndex without forEach")
            if "if" in meta:
                v = meta["if"]
                if not (isinstance(v, str) and v.strip().startswith("{!") and v.strip().endswith("}")):
                    problems["meta"].append(f"{path}: meta.if must be a {{!...}} expression")

        # bindings: forEach expression uses parent scope; everything else uses new scope
        def check_expr(expr, vars_):
            refs, funcs = refs_and_funcs(expr)
            if any(r == "attrs" for r, _ in refs) and not PLAIN_REF_RE.match(strip_strings(expr)):
                attr_formulas.append(f"{path}: {{!{expr.strip()[:60]}}}")
            for root, parts in refs:
                if root == "attrs":
                    if not parts:
                        problems["bindings"].append(f"{path}: bare $attrs")
                    elif parts[0] not in props:
                        problems["bindings"].append(f"{path}: $attrs.{parts[0]} not in schema.json")
                elif root in vars_:
                    fields = vars_[root]
                    if isinstance(fields, dict) and parts and parts[0] not in fields:
                        problems["bindings"].append(f"{path}: ${root}.{parts[0]} not in list item properties")
                else:
                    problems["bindings"].append(f"{path}: ${root} is not $attrs or an in-scope loop variable")
            for f in funcs:
                if f not in FUNCTIONS:
                    problems["funcs"].append(f"{path}: unsupported function {f}()")

        for key, val in meta.items():
            if not isinstance(val, str):
                continue
            vars_ = scope_vars if key == "forEach" else new_vars
            for e in extract_expressions(val):
                check_expr(e, vars_)
        for s in all_strings(attrs):
            for e in extract_expressions(s):
                check_expr(e, new_vars)

        # attribute names against the official per-component lists
        allowed = COMPONENT_ATTRS.get(d)
        if allowed is not None and isinstance(attrs, dict):
            for a in attrs:
                if a not in allowed:
                    hint = ATTR_HINTS.get((d, a))
                    problems["attrs"].append(f"{path}: '{a}' not a {d} attribute" + (f" (use '{hint}')" if hint else ""))

        # component-specific checks
        if d == "tile/button":
            click = ((attrs.get("actions") or {}).get("click"))
            if not isinstance(click, list) or not click:
                problems["buttons"].append(f"{path}: no actions.click — renders disabled")
            else:
                for a in click:
                    ad = (a or {}).get("definition")
                    if ad not in ACTIONS:
                        problems["buttons"].append(f"{path}: action '{ad}' not openLink/sendMessage")
                    elif not ((a.get("attributes") or {}).get(ACTIONS[ad])):
                        problems["buttons"].append(f"{path}: {ad} missing '{ACTIONS[ad]}'")
            if attrs.get("variant") == "primary":
                stats["primary"] += 1
        if d == "tile/text" and attrs.get("variant") == "h1":
            stats["h1"] += 1
        if d == "tile/image" and not attrs.get("alt"):
            problems["structure"].append(f"{path}: tile/image without alt")

        kids = node.get("children") or []
        if not isinstance(kids, list):
            problems["structure"].append(f"{path}: children must be an array")
            return
        for idx, k in enumerate(kids):
            walk(k, f"{path}[{idx}]", new_vars)

    walk(body, "widgetBody", {})

    for key, name in (("structure", "tree-structure"), ("meta", "meta-directives"),
                      ("attrs", "component-attributes"),
                      ("bindings", "bindings-resolve"), ("funcs", "formulas-supported"),
                      ("buttons", "button-actions-present")):
        if problems[key]:
            rep.fail(scope, name, "; ".join(problems[key][:8]) + (" …" if len(problems[key]) > 8 else ""))
        else:
            rep.ok(scope, name)
    first = (body.get("children") or [{}])[0] if isinstance(body.get("children"), list) and body.get("children") else {}
    if len(body.get("children") or []) != 1 or (first or {}).get("definition") != "tile/column":
        rep.warn(scope, "root-column", "convention: tile/widget should have a single tile/column child")
    if stats["unknown"]:
        rep.warn(scope, "beta-components", f"not in Beta list (Dev Preview? verify): {sorted(stats['unknown'])}")
    if stats["h1"] > 1:
        rep.warn(scope, "style-h1", f"{stats['h1']} h1 texts; use one")
    if stats["primary"] > 1:
        rep.warn(scope, "style-primary", f"{stats['primary']} primary buttons; prefer one per group")
    bound = set()
    for s in all_strings(comp):
        for e in extract_expressions(s):
            for root, parts in refs_and_funcs(e)[0]:
                if root == "attrs" and parts:
                    bound.add(parts[0])
    unused = sorted(set(props) - bound)
    if unused:
        rep.warn(scope, "unused-attributes", f"declared but never bound: {unused} "
                 "(if already deployed, keep them: removing schema properties is a breaking change)")
    return attr_formulas


def check_meta_xml(path, name, rep, scope):
    try:
        root = ET.parse(path).getroot()
    except FileNotFoundError:
        rep.fail(scope, "metaxml-wellformed", f"missing {path.name}")
        return
    except ET.ParseError as e:
        rep.fail(scope, "metaxml-wellformed", str(e))
        return
    rep.ok(scope, "metaxml-wellformed")
    tag = root.tag.split("}")[-1]
    ns = root.tag[:root.tag.index("}") + 1] if root.tag.startswith("{") else ""

    def txt(t):
        el = root.find(ns + t)
        return (el.text or "").strip() if el is not None else ""
    errs = []
    if tag != "UiWidgetBundle":
        errs.append(f"root is <{tag}>")
    if txt("widgetType") != "JSON":
        errs.append("<widgetType>JSON</widgetType> required")
    if not txt("masterLabel"):
        errs.append("<masterLabel> empty/missing")
    if not txt("description"):
        errs.append("<description> empty/missing")
    if errs:
        rep.fail(scope, "metaxml-elements", "; ".join(errs))
    else:
        rep.ok(scope, "metaxml-elements")


def check_widget(wdir, rep):
    name = wdir.name
    scope = f"widget {name}"
    if wdir.parent.parent.name != "default" or wdir.parent.parent.parent.name != "main":
        rep.warn(scope, "bundle-location", f"expected .../main/default/uiWidgets/{name} (got {wdir})")
    comp_p = wdir / f"{name}.json"
    meta_p = wdir / f"{name}.uiwidget-meta.xml"
    schema_p = wdir / "schema.json"
    missing = [p.name for p in (comp_p, meta_p) if not p.exists()]
    if missing:
        rep.fail(scope, "files-present", f"missing {missing} (file stems must equal folder name)")
    else:
        rep.ok(scope, "files-present")
    props = None
    if schema_p.exists():
        schema = load_json(schema_p, rep, scope, "schema-parses")
        props = check_widget_schema(schema, rep, scope)
    else:
        rep.warn(scope, "schema-present", "no schema.json — widget can only show static content")
    comp = load_json(comp_p, rep, scope, "body-parses") if comp_p.exists() else None
    formulas = check_composition(comp, props or {}, rep, scope) or []
    if meta_p.exists():
        check_meta_xml(meta_p, name, rep, scope)
    WIDGET_ATTR_FORMULAS[name] = formulas
    return props


WIDGET_ATTR_FORMULAS = {}


# ----------------------------------------------------------------------------
# Lightning types
# ----------------------------------------------------------------------------
def check_clt(cdir, widgets, clts, rep):
    name = cdir.name
    scope = f"lightningType {name}"
    schema = load_json(cdir / "schema.json", rep, scope, "clt-schema-parses")
    if schema is None:
        return
    tags = schema.get("lightning:tags") or []
    is_mcp = "mcp" in tags
    root_type = schema.get("lightning:type", "")
    props = schema.get("properties") or {}

    for sub in ("lightningDesktopGenAi", "lightningMobileGenAi", "enhancedWebChat"):
        rp = cdir / sub / "renderer.json"
        if rp.exists():
            try:
                if "@widget/" in rp.read_text(encoding="utf-8"):
                    rep.fail(scope, "renderer-location", f"{sub}/renderer.json references a widget — must be at bundle root")
            except OSError:
                pass
    if (cdir / "editor.json").exists() and "@widget/" in (cdir / "editor.json").read_text(encoding="utf-8"):
        rep.fail(scope, "editor-widget", "editor.json can't reference widgets")

    if is_mcp:
        errs = []
        if schema.get("type") != "object":
            errs.append("type must be object")
        if root_type != "lightning__objectType":
            errs.append("lightning:type must be lightning__objectType")
        if schema.get("unevaluatedProperties") is not False:
            errs.append("unevaluatedProperties must be false")
        for pn, p in props.items():
            if isinstance(p, dict) and (p.get("type") == "object" and not p.get("lightning:type")):
                errs.append(f"{pn}: bare object — use @apexClassType/c__Outer$Inner")
            if isinstance(p, dict) and "items" in p:
                errs.append(f"{pn}: CLT-level items/listType not allowed; type to the Apex element class")
        if errs:
            rep.fail(scope, "mcp-clt-shape", "; ".join(errs))
        else:
            rep.ok(scope, "mcp-clt-shape")
        if "outputValues" in props:
            ov = (props["outputValues"] or {}).get("lightning:type", "")
            m = re.match(r"^([A-Za-z0-9]+)__(\w+)$", ov)
            missing = [k for k in ("actionName", "isSuccess") if k not in props]
            if missing:
                rep.fail(scope, "mcp-wrapper-props", f"missing {missing}")
            elif not m:
                rep.fail(scope, "clt-reference-integrity", f"outputValues lightning:type '{ov}' should be c__<payloadClt>")
            elif m.group(2) not in clts:
                rep.fail(scope, "clt-reference-integrity", f"payload CLT '{m.group(2)}' not found in project")
            else:
                rep.ok(scope, "clt-reference-integrity", f"outputValues → {m.group(2)}")
        elif (cdir / "renderer.json").exists():
            rep.fail(scope, "renderer-placement", "MCP payload CLT must not have renderer.json (put it on the wrapper)")
    else:
        if root_type.startswith("@apexClassType/"):
            rep.ok(scope, "apex-clt-type", root_type)
            cls = root_type.split("__", 1)[-1].split("$")[0]
            project = next((p for p in cdir.parents if (p / "sfdx-project.json").exists()), None)
            if project:
                found = list(project.rglob(f"classes/{cls}.cls"))
                if not found:
                    rep.warn(scope, "apex-class-local", f"{cls}.cls not in project (fine if already in org)")

    rp = cdir / "renderer.json"
    if not rp.exists():
        return
    renderer = load_json(rp, rep, scope, "renderer-parses")
    if renderer is None:
        return
    over = (((renderer.get("renderer") or {}).get("componentOverrides") or {}).get("$") or {})
    definition = over.get("definition", "")
    m = re.match(r"^@widget/([^/]+)/([A-Za-z0-9_]+)$", definition)
    if not m:
        rep.fail(scope, "renderer-wires-widget", f"definition '{definition}' is not @widget/c/<name>")
        return
    if m.group(1) != "c":
        rep.fail(scope, "renderer-wires-widget", "use the 'c' namespace for org widgets, even in namespaced orgs")
    wname = m.group(2)
    if wname not in widgets:
        rep.fail(scope, "renderer-wires-widget", f"widget '{wname}' not found under uiWidgets/")
        return
    wprops = widgets[wname] or {}
    amap = over.get("attributes") or {}
    errs, warns = [], []
    for k, v in amap.items():
        if k not in wprops:
            errs.append(f"key '{k}' not in widget schema")
        exprs = extract_expressions(v) if isinstance(v, str) else []
        if not exprs:
            continue
        refs, _ = refs_and_funcs(exprs[0])
        if not refs or refs[0][0] != "attrs" or not refs[0][1]:
            errs.append(f"{k}: value must reference $attrs.<path>")
            continue
        parts = refs[0][1]
        if is_mcp:
            if parts[0] != "outputValues":
                errs.append(f"{k}: MCP binding must go through $attrs.outputValues…")
            elif len(parts) < 2:
                errs.append(f"{k}: binding stops at outputValues")
            else:
                ov = (props.get("outputValues") or {}).get("lightning:type", "")
                payload = ov.split("__", 1)[-1] if "__" in ov else None
                pprops = clts.get(payload) if payload else None
                if pprops is not None and parts[1] not in pprops:
                    errs.append(f"{k}: '{parts[1]}' not a property of payload CLT {payload}")
        elif props and parts[0] not in props:
            errs.append(f"{k}: '{parts[0]}' not a property of this CLT")
    unmapped = sorted(set(wprops) - set(amap))
    if unmapped:
        warns.append(f"widget attributes not mapped: {unmapped}")
    if errs:
        rep.fail(scope, "renderer-wires-widget", "; ".join(errs))
    else:
        rep.ok(scope, "renderer-wires-widget", f"@widget/c/{wname}, {len(amap)} mappings" + (" (nested MCP)" if is_mcp else ""))
    for w in warns:
        rep.warn(scope, "renderer-coverage", w)
    if is_mcp:
        # Verified 2026-09-21 in Claude: the wrapper renderer rewrites plain {!$attrs.x}
        # bindings to $attrs.outputValues.<payload>.x but NOT $attrs refs inside formulas,
        # so any IF/BLANKVALUE/TEXT/comparison over $attrs fails when the tool runs.
        bad = WIDGET_ATTR_FORMULAS.get(wname) or []
        if bad:
            rep.fail(scope, "mcp-plain-bindings",
                     f"widget {wname} has {len(bad)} formula(s) over $attrs, which break in the MCP channel; "
                     "compute the value in Apex and bind it plainly: " + "; ".join(bad[:4]) + (" …" if len(bad) > 4 else ""))
        else:
            rep.ok(scope, "mcp-plain-bindings", f"widget {wname} uses only plain $attrs bindings")


# ----------------------------------------------------------------------------
# McpServerDefinition wiring
# ----------------------------------------------------------------------------
def check_mcp_server(path, clt_props, rep):
    scope = f"mcpServer {path.name.split('.')[0]}"
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        rep.fail(scope, "mcp-xml-wellformed", str(e))
        return
    ns = root.tag[:root.tag.index("}") + 1] if root.tag.startswith("{") else ""
    resources = {}
    for r in root.findall(ns + "resources"):
        name = (r.findtext(ns + "resourceName") or "").strip()
        resources[name] = (r.findtext(ns + "resourceUri") or "").strip()
    tools = root.findall(ns + "tools")
    errs, warns, linked = [], [], set()
    for t in tools:
        tname = (t.findtext(ns + "toolName") or "?").strip()
        ui = (t.findtext(ns + "uiResource") or "").strip()
        if ui:
            linked.add(ui)
            if ui not in resources:
                errs.append(f"tool {tname}: uiResource '{ui}' has no matching <resources><resourceName>")
    for name, uri in resources.items():
        m = re.match(r"^ui://widget/lightningType/([A-Za-z0-9]+)__(\w+)$", uri)
        if not m:
            errs.append(f"resource {name}: resourceUri '{uri}' is not ui://widget/lightningType/c__<wrapperClt>")
            continue
        clt = m.group(2)
        props = clt_props.get(clt)
        if props is None:
            warns.append(f"resource {name}: CLT '{clt}' not in project (fine if already deployed)")
        elif "outputValues" not in props:
            errs.append(f"resource {name}: '{clt}' is not the MCP wrapper CLT (no outputValues); point at the wrapper, not the payload or widget")
        if name not in linked:
            errs.append(f"resource {name}: no tool has <uiResource>{name}</uiResource>; the client will show plain text/table. "
                        "Editing or re-adding the tool in Setup wipes uiResource: re-add it and redeploy")
    if errs:
        rep.fail(scope, "mcp-ui-resource", "; ".join(errs))
    elif resources:
        rep.ok(scope, "mcp-ui-resource", f"{len(linked)} tool(s) linked to {sorted(resources)}")
    else:
        rep.warn(scope, "mcp-ui-resource", "no <resources>: tools on this server render as plain text")
    for w in warns:
        rep.warn(scope, "mcp-ui-resource", w)


# ----------------------------------------------------------------------------
def discover(paths):
    widgets, clts, servers = set(), set(), set()
    for p in paths:
        p = Path(p).resolve()
        if p.parent.name == "uiWidgets":
            widgets.add(p)
        elif p.parent.name == "lightningTypes":
            clts.add(p)
        elif p.name.endswith(".mcpServerDefinition-meta.xml"):
            servers.add(p)
        else:
            for d in p.rglob("mcpServerDefinitions"):
                if "node_modules" in d.parts or ".sfdx" in d.parts:
                    continue
                servers.update(d.glob("*.mcpServerDefinition-meta.xml"))
            for d in p.rglob("uiWidgets"):
                if "node_modules" in d.parts or ".sfdx" in d.parts:
                    continue
                widgets.update(x for x in d.iterdir() if x.is_dir())
            for d in p.rglob("lightningTypes"):
                if "node_modules" in d.parts or ".sfdx" in d.parts:
                    continue
                clts.update(x for x in d.iterdir() if x.is_dir())
    return sorted(widgets), sorted(clts), sorted(servers)


def main(argv):
    strict = "--strict" in argv
    paths = [a for a in argv if not a.startswith("--")] or ["."]
    wdirs, cdirs, servers = discover(paths)
    # widen: sibling folders for cross-refs
    for c in list(cdirs):
        proj_default = c.parent.parent
        extra_w = proj_default / "uiWidgets"
        if extra_w.is_dir():
            wdirs = sorted(set(wdirs) | {x for x in extra_w.iterdir() if x.is_dir()})
        cdirs = sorted(set(cdirs) | {x for x in c.parent.iterdir() if x.is_dir()})
    rep = Report()
    if not wdirs and not cdirs:
        print("No uiWidgets/ or lightningTypes/ folders found.")
        return 1
    widgets = {w.name: check_widget(w, rep) for w in wdirs}
    clt_props = {}
    for c in cdirs:
        try:
            clt_props[c.name] = (json.loads((c / "schema.json").read_text(encoding="utf-8")).get("properties") or {})
        except Exception:
            clt_props[c.name] = None
    for c in cdirs:
        check_clt(c, widgets, clt_props, rep)
    for s in servers:
        check_mcp_server(s, clt_props, rep)
    n = rep.print()
    return 1 if n["FAIL"] or (strict and n["WARN"]) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
