# Contributing

AICD is a methodology, not a library, so most useful contributions are not code. What helps most, in order: reports of applying it on a real product, defects in the document, and proposals to extend it.

The methodology's own rule applies to itself. The core is closed to modification and the methodology is open to extension, so a change to the founding principles, the five layers or the separation of duties is not a pull request. It is evidence from a real project, sent to the author. Everything else has a path below.

## Ask a question

Open a [Discussion](https://github.com/rachidsahane/AICD-METHODOLOGY/discussions). Questions about what a section means, whether the methodology covers a situation, or how to start are all in scope, and the answer usually belongs in public where the next person can find it.

Please do not open an issue for a question. Issues here are for defects in the document.

## Report an experience applying AICD

Open a [Discussion](https://github.com/rachidsahane/AICD-METHODOLOGY/discussions). This is the most valuable thing you can contribute, because the methodology is revised from what real applications teach, and it currently rests on a small number of them.

What makes a report useful:

- What you ran, on what kind of product, and for how long.
- Which parts you actually followed and which you skipped or changed.
- What broke, in enough detail that someone else would recognise it.
- What the methodology told you to do that turned out to be wrong, or impossible, or unnecessary.

Negative results are more useful than positive ones. A section that did not survive contact with a real product is exactly what the next version needs to know.

## Propose a change to the methodology

Extensions go through the AICD Change Proposal process, which the methodology defines in its own section 29. Read [proposals/README.md](proposals/README.md) first: it records what may change and by which procedure, so you can tell whether what you have in mind needs a proposal at all. A parameter change or a tooling choice does not.

If it does need one, copy [proposals/TEMPLATE.md](proposals/TEMPLATE.md), fill every field, and open a pull request adding it to `proposals/`. A proposal with an unfilled field is not reviewable. [ACP-0001](proposals/ACP-0001-single-operator-profile.md) is a worked example of an accepted one.

If you are not sure yet, raise it in a Discussion before writing the proposal.

## Fix a typo, a broken link or a rendering defect

Open a pull request. These need no discussion first.

The document is a single self-contained HTML file, `src/aicd.html`, with its CSS inline. Edit it directly. Two rules:

- Keep the change to what you are fixing. The methodology's wording is the author's.
- Do not hand-edit section ids or contents links. They are checked, and the check runs on every pull request.

If the defect is in how the document renders rather than in its text, describe what you see and on what, because the PDF and the web page come from the same file and a fix has to work in both.

## Build the PDF

The HTML in `src/` is the source of truth. The PDF is a build artifact of it, so it is never edited directly.

Install the fonts first, system wide. They matter more than usual: WeasyPrint substitutes silently, so a missing font is not an error, it is a different page count and different line breaks. [build/fonts.md](build/fonts.md) lists every family, where it comes from, and the exact install command for Debian, Ubuntu and macOS.

Then:

```sh
python3 -m pip install -r build/requirements.txt
build/build.sh
```

The build checks the document's anchors and every image it references, and fails before rendering if anything is missing, so an incomplete PDF is never produced. It writes two files:

- `dist/AICD-Methodology-v0.3.pdf`, the versioned name a release attaches.
- `dist/AICD-Methodology.pdf`, the stable name the README and the site link to.

The reference build of v0.3 is **76 pages**. A different number almost always means a missing font; check that before anything else.

To refresh the copy committed at the repository root:

```sh
cp dist/AICD-Methodology.pdf AICD-Methodology.pdf
```

### The images

`src/cover_bg.jpg` and `src/portrait_circle.png` are the author's own cover artwork and photograph. They are committed source, not build output. Do not regenerate them, and do not replace them in a pull request.

`assets/social-preview.png`, the 1280x640 card link previews show, is generated from whichever cover is in `src/`, so it stays in step with the document:

```sh
python3 build/generate_assets.py
```

That needs Pillow and NumPy in addition to the pinned build dependencies, and it writes only the social card.

The script also carries generated stand-ins for the cover and the portrait, behind `--placeholders`, for a checkout where the artwork is missing. That flag **overwrites the author's artwork with a generated background and a monogram**, so it is not something to run casually.

## Checks

Two checks run on every pull request, and both are worth running locally before you open one:

```sh
python3 build/check_anchors.py   # every section id matches its number, no duplicates, no ambiguous links
python3 build/check_links.py     # every relative link in the Markdown resolves
```

`build/check_anchors.py` exists because this document shipped with `id="s31"` used twice. A duplicate id does not fail a render: it silently sends every link to the first occurrence, so the contents printed the wrong page number for a whole section and nothing complained.

## What is not accepted

- Changes to the methodology's wording that are not fixing a defect.
- Changes to the founding principles, the five layers or the separation of duties. See the top of this file.
- Rewriting the PDF by hand. It is generated.
- Reformatting, restyling or reorganising the document.
