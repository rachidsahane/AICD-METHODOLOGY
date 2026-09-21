#!/usr/bin/env bash
#
# Build the AICD methodology PDF from the HTML source in src/.
#
# The HTML in src/ is the source of truth. This script is the only supported
# way to turn it into a PDF, so that the file attached to a release and the
# file a reader builds locally are the same document.
#
# Usage:
#   build/build.sh                 # build into dist/
#   OUT_DIR=/tmp/x build/build.sh  # build somewhere else
#
# Requirements:
#   python3, and the packages in build/requirements.txt
#   the fonts listed in build/fonts.md, installed system wide
#
# The script fails if any image the document references is missing, so a
# broken build is never published as a silently incomplete PDF.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="${REPO_ROOT}/src"
OUT_DIR="${OUT_DIR:-${REPO_ROOT}/dist}"

# WeasyPrint reaches Pango, cairo and friends through the dynamic loader. On
# macOS the Homebrew prefix is not on the default search path, so add it unless
# the caller already set one. On Linux this is a no-op.
if [ "$(uname -s)" = "Darwin" ] && [ -z "${DYLD_FALLBACK_LIBRARY_PATH:-}" ]; then
  for prefix in /opt/homebrew/lib /usr/local/lib; do
    if [ -d "$prefix" ]; then
      export DYLD_FALLBACK_LIBRARY_PATH="$prefix"
      break
    fi
  done
fi

# ---------------------------------------------------------------- the source
shopt -s nullglob
HTML_CANDIDATES=("${SRC_DIR}"/*.html)
shopt -u nullglob

if [ "${#HTML_CANDIDATES[@]}" -eq 0 ]; then
  echo "build: no HTML source found in ${SRC_DIR}" >&2
  exit 1
fi
if [ "${#HTML_CANDIDATES[@]}" -gt 1 ]; then
  echo "build: expected exactly one HTML source in ${SRC_DIR}, found ${#HTML_CANDIDATES[@]}:" >&2
  printf '  %s\n' "${HTML_CANDIDATES[@]}" >&2
  exit 1
fi
SRC_HTML="${HTML_CANDIDATES[0]}"

echo "build: source   ${SRC_HTML#"${REPO_ROOT}/"}"

# ------------------------------------------------- version, read from the HTML
VERSION="$(
  SRC_HTML="${SRC_HTML}" python3 - <<'PY'
import os
import re
import sys

with open(os.environ["SRC_HTML"], encoding="utf-8") as handle:
    html = handle.read()

# The cover states the version in prose; that statement is authoritative.
match = re.search(r"Version\s+(\d+\.\d+(?:\.\d+)?)\s*,", html)
if match is None:
    # Fall back to the running footer defined in the @page rule.
    match = re.search(r"\bv(\d+\.\d+(?:\.\d+)?)\s+working draft", html)
if match is None:
    sys.stderr.write("build: could not find a version statement in the HTML\n")
    raise SystemExit(1)

sys.stdout.write(match.group(1))
PY
)"

echo "build: version  ${VERSION}"

# --------------------------------------------- every referenced asset must exist
SRC_HTML="${SRC_HTML}" SRC_DIR="${SRC_DIR}" python3 - <<'PY'
import os
import re
import sys

src_dir = os.environ["SRC_DIR"]
with open(os.environ["SRC_HTML"], encoding="utf-8") as handle:
    html = handle.read()

refs = []
refs += re.findall(r"""<img\b[^>]*?\bsrc\s*=\s*["']([^"']+)["']""", html, re.IGNORECASE)
refs += re.findall(r"""url\(\s*["']?([^"')]+)["']?\s*\)""", html, re.IGNORECASE)

seen, local = set(), []
for ref in refs:
    ref = ref.strip()
    if not ref or ref in seen:
        continue
    seen.add(ref)
    lowered = ref.lower()
    if lowered.startswith(("http://", "https://", "data:", "//", "#", "mailto:")):
        continue
    local.append(ref)

missing = [ref for ref in local if not os.path.isfile(os.path.join(src_dir, ref))]

for ref in local:
    mark = "missing" if ref in missing else "ok"
    print("build: asset    %-24s %s" % (ref, mark))

if missing:
    sys.stderr.write(
        "build: %d referenced asset(s) missing from src/: %s\n"
        % (len(missing), ", ".join(missing))
    )
    raise SystemExit(1)

if not local:
    sys.stderr.write("build: no local assets referenced, which is unexpected\n")
    raise SystemExit(1)
PY

# ------------------------------------------------- anchors must be unambiguous
# A duplicate id does not fail the render, it silently sends every link to the
# first occurrence, so the contents can print a wrong page number and nothing
# complains. Check before spending time on the render.
python3 "${REPO_ROOT}/build/check_anchors.py" "${SRC_HTML}"

# ------------------------------------------------------------------- render
mkdir -p "${OUT_DIR}"
PDF="${OUT_DIR}/AICD-Methodology-v${VERSION}.pdf"

SRC_HTML="${SRC_HTML}" SRC_DIR="${SRC_DIR}" PDF="${PDF}" python3 - <<'PY'
import logging
import os
import sys

from weasyprint import HTML

# Print WeasyPrint's own warnings, such as unresolved references and missing
# resources, rather than discarding them. A missing font is not among them:
# fontconfig substitutes silently, which is why build/fonts.md insists the
# document fonts are installed before the build is trusted.
logger = logging.getLogger("weasyprint")
logger.addHandler(logging.StreamHandler(sys.stderr))
logger.setLevel(logging.WARNING)

src_html = os.environ["SRC_HTML"]
# base_url is the src/ directory, so the document's relative image paths
# resolve exactly as they do when the same file is served as a web page.
base_url = os.path.join(os.environ["SRC_DIR"], "")

HTML(filename=src_html, base_url=base_url).write_pdf(os.environ["PDF"])
PY

# ------------------------------------------------------------- page count
PAGES="$(
  PDF="${PDF}" python3 - <<'PY'
import os
import sys

from pypdf import PdfReader

sys.stdout.write(str(len(PdfReader(os.environ["PDF"]).pages)))
PY
)"

SIZE="$(wc -c < "${PDF}" | tr -d ' ')"

echo "build: output   ${PDF#"${REPO_ROOT}/"}"
echo "build: pages    ${PAGES}"
echo "build: bytes    ${SIZE}"
