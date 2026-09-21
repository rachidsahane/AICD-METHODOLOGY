#!/usr/bin/env python3
"""Check that the document's anchors are sound.

Three things must hold, and each has broken at least once in this document's
history:

1. No id is used twice. A duplicate id silently steals every link to it,
   and the renderer resolves both to the first occurrence, so a contents
   entry can print the wrong page number without anything failing.
2. Every numbered section heading carries the id matching its own number,
   so section 23 is at id "s23". When the two drift apart, a reference
   written from the printed numbering points somewhere else.
3. Every internal href resolves to exactly one id.

Usage:
    python3 build/check_anchors.py [path/to/document.html]

With no argument it checks the single HTML file in src/. Exits 0 when the
document is sound and 1 when it is not, printing every problem it found.
"""

import argparse
import collections
import os
import re
import sys

HEADING_RE = re.compile(
    r"<h1\b([^>]*)>\s*<span class=\"num\">([^<]+)</span>([^<]*)</h1>",
    re.IGNORECASE,
)
ID_ATTR_RE = re.compile(r"\bid=\"([^\"]+)\"")
ANY_ID_RE = re.compile(r"\sid=\"([^\"]+)\"")
HREF_RE = re.compile(r"href=\"#([^\"]+)\"")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def default_source():
    """The single HTML document in src/."""
    src_dir = os.path.join(REPO_ROOT, "src")
    candidates = sorted(
        os.path.join(src_dir, name)
        for name in os.listdir(src_dir)
        if name.lower().endswith(".html")
    )
    if len(candidates) != 1:
        sys.stderr.write(
            "check_anchors: expected exactly one HTML file in src/, found %d\n"
            % len(candidates)
        )
        raise SystemExit(1)
    return candidates[0]


def check(path):
    """Return a list of problem strings. Empty means the document is sound."""
    with open(path, encoding="utf-8") as handle:
        html = handle.read()

    problems = []

    ids = ANY_ID_RE.findall(html)
    counts = collections.Counter(ids)

    for name, n in sorted(counts.items()):
        if n > 1:
            problems.append("duplicate id: %s is defined %d times" % (name, n))

    headings = []
    for match in HEADING_RE.finditer(html):
        attrs, number, title = match.group(1), match.group(2).strip(), match.group(3).strip()
        id_match = ID_ATTR_RE.search(attrs)
        headings.append((id_match.group(1) if id_match else None, number, title))

    numbered = [h for h in headings if h[1].isdigit()]
    for anchor, number, title in numbered:
        expected = "s%s" % number
        if anchor is None:
            problems.append(
                "section %s (%s) has no id, expected id=\"%s\"" % (number, title, expected)
            )
        elif anchor != expected:
            problems.append(
                "section %s (%s) has id=\"%s\", expected id=\"%s\""
                % (number, title, anchor, expected)
            )

    seen_numbers = [int(h[1]) for h in numbered]
    for number, n in sorted(collections.Counter(seen_numbers).items()):
        if n > 1:
            problems.append("section number %d appears on %d headings" % (number, n))

    if seen_numbers:
        missing = [n for n in range(1, max(seen_numbers) + 1) if n not in seen_numbers]
        for number in missing:
            problems.append("no heading is numbered %d, so id s%d has nothing to point at" % (number, number))

    for href in sorted(set(HREF_RE.findall(html))):
        n = counts.get(href, 0)
        if n == 0:
            problems.append("href #%s points at an id that does not exist" % href)
        elif n > 1:
            problems.append("href #%s resolves to %d ids, so the link is ambiguous" % (href, n))

    if not problems:
        print(
            "check_anchors: ok, %d ids, %d numbered sections, %d internal links"
            % (len(counts), len(numbered), len(set(HREF_RE.findall(html))))
        )
    return problems


def main():
    parser = argparse.ArgumentParser(description="Check the document's anchors.")
    parser.add_argument(
        "path",
        nargs="?",
        help="HTML file to check (default: the single HTML file in src/)",
    )
    args = parser.parse_args()
    path = args.path or default_source()

    problems = check(path)
    if problems:
        sys.stderr.write(
            "check_anchors: %s\ncheck_anchors: %d problem(s)\n"
            % (os.path.relpath(path, REPO_ROOT), len(problems))
        )
        for problem in problems:
            sys.stderr.write("  %s\n" % problem)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
