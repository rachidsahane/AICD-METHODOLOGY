# Fonts

The PDF is rendered by WeasyPrint from `src/AICD_Methodology_v0.3.html`. Every typeface
the document uses is named in the inline CSS of that file. Nothing is embedded in the
HTML and nothing is downloaded at build time, so the fonts have to be installed on the
machine that runs `build/build.sh`.

This matters more than it usually does, because WeasyPrint substitutes silently. A
missing family is not an error. Fontconfig hands back whatever it considers the closest
match, the build succeeds, and the file that comes out has different metrics: different
line breaks, different table widths, different page breaks and a different page count.
The reference build of v0.3 is 76 pages. If a build reports a different number, look at
the fonts before anything else.

## The families the document names

| Family | What it sets in this document | License | Where it comes from |
| --- | --- | --- | --- |
| Carlito | Body text (`html, body`), the summary block on the cover (`.cover .sub`), and the running footer and page number in the `@page` rules | SIL Open Font License 1.1 | Google, metric compatible with Calibri. Packaged by Debian and Ubuntu as `fonts-crosextra-carlito` |
| Caladea | The cover line "Artificial Intelligence Centered Development" (`.cover .full`), the cover byline (`.cover .author .by`) and the colophon title (`.colophon h1.doctitle`). It also sets the cover acronym and the author name in practice, see the note on GFS Baskerville below | SIL Open Font License 1.1 | Google, metric compatible with Cambria. Packaged by Debian and Ubuntu as `fonts-crosextra-caladea` |
| DejaVu Sans Condensed | Every heading, `h1` to `h4`, plus table header cells, part labels, box titles, the numbered principle badges and the bold lead-in line of each principle, the flow chips, layer names, the colophon and author page labels, the first column of the contact table, and the part rows of the table of contents | Bitstream Vera Fonts Copyright, a permissive free license, with public domain additions | The DejaVu project. Debian and Ubuntu package `fonts-dejavu-extra` |
| DejaVu Sans | Fallback only: second in the body stack after Carlito, second in the heading stack after DejaVu Sans Condensed | the same DejaVu license | `fonts-dejavu-core` |
| DejaVu Sans Mono | Inline code and `.mono` spans | the same DejaVu license | `fonts-dejavu-mono` on Debian 13 and Ubuntu 24.04 and later, `fonts-dejavu-core` on older releases. The `fonts-dejavu` metapackage pulls in whichever applies |
| GFS Baskerville | Named first in `.cover .acronym` and `.authorpage h1.name`, and named as a fallback in three further rules, but never used for any glyph in this document. See below | SIL Open Font License | CTAN, https://ctan.org/pkg/gfsbaskerville . Not required |
| `sans-serif`, `serif`, `monospace` | The generic last resort at the end of each stack | not applicable | Resolved by fontconfig to the system defaults |

Carlito and Caladea are the two faces that carry the reading text and the display text.
DejaVu Sans Condensed is the heading face of the whole document, so it is the one whose
absence changes the most pages. Install all of them.

## GFS Baskerville is named but is not used

Two rules list GFS Baskerville first: `.cover .acronym`, which sets the word AICD on the
cover, and `.authorpage h1.name`, which sets the author name. Both set Latin text, and
GFS Baskerville has no Latin letters to set it with.

The face was downloaded from CTAN and measured. `GFSBaskerville.otf` maps 366 codepoints.
Only 4 of them fall in the range U+0041 to U+007A, and none of the Latin letters this
document actually sets are among them. It is a Greek face. Both rules therefore fall
through to the next family in the stack, Caladea, which is the face the cover acronym and
the author name really render in. Installing GFS Baskerville does not change the output.

To repeat the measurement, read the character map of the OTF with fontTools:

```bash
python3 -m pip install fonttools
python3 - <<'PY'
from fontTools.ttLib import TTFont

cmap = TTFont("GFSBaskerville.otf").getBestCmap()
latin = [cp for cp in cmap if 0x41 <= cp <= 0x7A]
print("codepoints mapped:", len(cmap))
print("in U+0041..U+007A:", len(latin), sorted(hex(cp) for cp in latin))
for word in ("AICD", "Ngatcha Sahane Rachid Alim"):
    missing = sorted({ch for ch in word if ch != " " and ord(ch) not in cmap})
    print(word, "missing:", missing)
PY
```

Anyone who wants the font anyway can get it from https://ctan.org/pkg/gfsbaskerville ,
where the Greek Font Society releases it under the SIL Open Font License. It is not in
the install commands below and the build does not look for it.

One related trap on macOS: the system ships a font called Baskerville. That is a
different face, and the CSS asks for "GFS Baskerville", so it is never matched. Nothing
needs to be done about it.

## Debian and Ubuntu

```bash
sudo apt-get install -y fonts-crosextra-carlito fonts-crosextra-caladea fonts-dejavu fonts-dejavu-core fonts-dejavu-extra
sudo fc-cache -f
```

This is the same command `.github/workflows/release.yml` runs before building the release
PDF. On a fresh machine or a container image, run `sudo apt-get update` first.

Why those five names:

- `fonts-dejavu-extra` is the package that ships `DejaVuSansCondensed.ttf`, in
  `/usr/share/fonts/truetype/dejavu/`. Since it carries the heading face, leaving it out
  reflows every heading in the document without any visible error.
- `fonts-dejavu-core` ships `DejaVuSans.ttf`, the fallback in the body and heading stacks.
- `fonts-dejavu` is the metapackage for core, mono and extra. It is named explicitly
  because the monospace faces moved out of `fonts-dejavu-core` into their own
  `fonts-dejavu-mono` package in Debian 13 and Ubuntu 24.04. The metapackage pulls in the
  right one on both old and new releases, so the code font resolves either way.
- `fonts-crosextra-carlito` and `fonts-crosextra-caladea` install into
  `/usr/share/fonts/truetype/crosextra/`, four styles each: regular, bold, italic and bold
  italic. On Ubuntu these two are in the universe component, which is enabled on the
  GitHub hosted runners.

`fc-cache -f` rebuilds the fontconfig cache. The apt hooks normally do this already, but
in a container layer or a CI step that installs and builds in the same shell it is worth
being explicit.

## macOS

```bash
brew install --cask font-carlito font-caladea font-dejavu
```

These are the casks used for the reference build. They install into `~/Library/Fonts`,
and the DejaVu cask includes the condensed and monospace faces, so no fourth cask is
needed. GFS Baskerville has no Homebrew cask, and as explained above it is not needed.

WeasyPrint on macOS also needs Pango, which Homebrew provides as a formula rather than a
cask:

```bash
brew install pango
```

WeasyPrint reaches Pango through the dynamic loader, and the Homebrew prefix is not on the
default search path. `build/build.sh` handles this: when it runs on macOS and the caller
has not set `DYLD_FALLBACK_LIBRARY_PATH`, it sets it to `/opt/homebrew/lib`, or to
`/usr/local/lib` on an Intel machine where that is the Homebrew prefix. If you have set
that variable yourself, the script leaves it alone, and Pango has to be reachable through
the value you set.

## How to check

Ask fontconfig for each family by name. Every command should print at least one line:

```bash
fc-list "Carlito" family
fc-list "Caladea" family
fc-list "DejaVu Sans" family
fc-list "DejaVu Sans Condensed" family
fc-list "DejaVu Sans Mono" family
```

The condensed query prints `DejaVu Sans,DejaVu Sans Condensed`, because those files
declare both names. That is the expected answer, not a partial match. Empty output from
any of the five means the family is missing and the build will substitute something else.

All five at once:

```bash
for family in Carlito Caladea "DejaVu Sans" "DejaVu Sans Condensed" "DejaVu Sans Mono"; do
  printf '%-22s %s\n' "$family" "$(fc-list "$family" file | head -n 1 || true)"
done
```

Use `fc-list` for this, not `fc-match`. `fc-match` always answers with something: on a
machine without the font, `fc-match "GFS Baskerville"` happily replies
`DejaVuSans.ttf: "DejaVu Sans" "Book"`. That is the substitution behaviour this file is
about, which makes `fc-match` useful for demonstrating the problem and useless for
detecting it.

Finally, the build itself reports. `build/build.sh` attaches a handler to the WeasyPrint
logger at warning level and sends it to stderr, so font substitutions and unresolved
references are printed rather than swallowed. A correct build prints only its own
`build:` lines. The page count is the second to last of them, `build: pages    76`,
followed by `build: bytes` with the size of the finished file.
