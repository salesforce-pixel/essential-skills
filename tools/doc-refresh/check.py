#!/usr/bin/env python3
"""Repo consistency checks run by the /refresh-skills routine before every push.

Checks every skills/<name>/SKILL.md:
  - frontmatter present, `name` == folder name, non-empty `description`
  - metadata.version present ("X.Y") and a Changelog comment block
  - every relative markdown link (*.md, optionally #anchor) in the skill resolves
  - no unconverted site-absolute /docs/... links in mirror skills
and that every skill in sources.json exists and every skill folder is in README.md.

Exit 1 with a list of problems, 0 if clean. Standard library only.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SKILLS = os.path.join(REPO, "skills")
REL_LINK = re.compile(r"\]\(((?!https?:|mailto:|#|/)[^)\s]+?\.md)(#[^)\s]*)?\)")
SITE_LINK = re.compile(r"\]\(/docs/[^)]*\)")
FENCE = re.compile(r"^\s*(```|~~~)")


def links_outside_fences(text):
    in_fence = False
    for n, line in enumerate(text.split("\n"), 1):
        if FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence:
            yield n, line


def main():
    problems = []
    with open(os.path.join(HERE, "sources.json"), encoding="utf-8") as f:
        sources = json.load(f)["skills"]
    with open(os.path.join(REPO, "README.md"), encoding="utf-8") as f:
        readme = f.read()

    for name in sorted(os.listdir(SKILLS)):
        sdir = os.path.join(SKILLS, name)
        if not os.path.isdir(sdir):
            continue
        p = os.path.join(sdir, "SKILL.md")
        if not os.path.exists(p):
            problems.append(f"{name}: missing SKILL.md")
            continue
        src = open(p, encoding="utf-8").read()
        m = re.match(r"---\n(.*?)\n---\n", src, re.S)
        if not m:
            problems.append(f"{name}: SKILL.md has no frontmatter")
            continue
        fm = m.group(1)
        nm = re.search(r"^name:\s*(\S+)", fm, re.M)
        if not nm or nm.group(1).strip("\"'") != name:
            problems.append(f"{name}: frontmatter name != folder name")
        if not re.search(r"^description:\s*\S", fm, re.M):
            problems.append(f"{name}: missing description")
        if not re.search(r'^\s+version:\s*"\d+\.\d+"', fm, re.M):
            problems.append(f'{name}: missing metadata.version "X.Y"')
        if not re.search(r"<!--\s*\nChangelog\n", src[m.end():m.end() + 400]):
            problems.append(f"{name}: no Changelog comment block right after frontmatter")
        if f"skills/{name}" not in readme:
            problems.append(f"{name}: not listed in README.md")

        mirror = sources.get(name, {}).get("kind") == "mirror"
        for root, _, files in os.walk(sdir):
            for fn in files:
                if not fn.endswith(".md"):
                    continue
                fp = os.path.join(root, fn)
                text = open(fp, encoding="utf-8").read()
                rel_fp = os.path.relpath(fp, REPO)
                for n, line in links_outside_fences(text):
                    for lm in REL_LINK.finditer(line):
                        target = os.path.normpath(os.path.join(root, lm.group(1)))
                        # ../<other-skill>/SKILL.md = cross-skill reference to a skill that
                        # may be installed from another library; not a broken link.
                        if not target.startswith(sdir + os.sep) and target.endswith("SKILL.md"):
                            continue
                        if not os.path.exists(target):
                            problems.append(f"{rel_fp}:{n}: broken link -> {lm.group(1)}")
                    if mirror and SITE_LINK.search(line):
                        problems.append(f"{rel_fp}:{n}: unconverted site-absolute /docs/ link")

    for name, cfg in sources.items():
        if not os.path.isdir(os.path.join(REPO, cfg["skill_dir"])):
            problems.append(f"sources.json: {name} -> {cfg['skill_dir']} does not exist")

    if problems:
        print("\n".join(problems))
        print(f"\n{len(problems)} problem(s)")
        sys.exit(1)
    print("check.py: all skills OK")


if __name__ == "__main__":
    main()
