#!/usr/bin/env python3
"""Check that every relative link in the repository's Markdown resolves.

Only links that stay inside the repository are checked. External URLs are
left alone, because a network check would make the result depend on someone
else's uptime. In-page fragments are left alone too; the document's own
anchors are the job of build/check_anchors.py.

Usage:
    python3 build/check_links.py

Exits 0 when every relative link resolves and 1 when one does not, naming
the file, the line and the target.
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "dist", "__pycache__", ".venv", "venv", "node_modules"}
EXTERNAL = ("http://", "https://", "mailto:", "tel:", "//")

# [text](target) and [text](target "title"), the inline form.
LINK_RE = re.compile(r"\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")


def markdown_files():
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            if name.lower().endswith(".md"):
                yield os.path.join(dirpath, name)


def main():
    problems = []
    checked = 0

    for path in markdown_files():
        rel_doc = os.path.relpath(path, REPO_ROOT)
        with open(path, encoding="utf-8") as handle:
            for lineno, line in enumerate(handle, 1):
                for match in LINK_RE.finditer(line):
                    target = match.group(1).strip()
                    if not target or target.startswith("#") or target.startswith(EXTERNAL):
                        continue
                    target = target.split("#", 1)[0]
                    if not target:
                        continue
                    checked += 1
                    resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
                    if not os.path.exists(resolved):
                        problems.append(
                            "%s:%d points at %s, which does not exist" % (rel_doc, lineno, target)
                        )

    if problems:
        sys.stderr.write("check_links: %d broken relative link(s)\n" % len(problems))
        for problem in problems:
            sys.stderr.write("  %s\n" % problem)
        return 1

    print("check_links: ok, %d relative links resolve" % checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())
