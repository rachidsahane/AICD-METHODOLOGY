# AICD: Artificial Intelligence Centered Development

AICD is a software development methodology for teams whose code is written by AI agents. It starts from one observation: when producing code stops being scarce, the difficulty moves to three places, specifying precisely what should exist, verifying that what was built is correct, and deciding on architecture, stack and priorities. AICD reproduces a complete development team with AI agents that build, test, operate and document the software, and places a small group of experienced engineers above them as specifiers, verifiers, decision makers and monitors. Those engineers read code fluently but never write production code or test code, because the specification stays the source of truth and every change enters through git.

## Current version and status

Version 0.3, working draft, September 2026.

- Latest release: https://github.com/rachidsahane/AICD-METHODOLOGY/releases/latest
- PDF asset of the v0.3 release: https://github.com/rachidsahane/AICD-METHODOLOGY/releases/download/v0.3/AICD-Methodology-v0.3.pdf

Neither the release nor its PDF asset exists yet. Both appear only once the author creates the `v0.3` tag and publishes the release, which is a manual step described in [PUBLISHING.md](PUBLISHING.md).

## Read it

- Site: https://rachidsahane.github.io/AICD-METHODOLOGY/
- PDF: https://github.com/rachidsahane/AICD-METHODOLOGY/releases/download/v0.3/AICD-Methodology-v0.3.pdf
- HTML source: https://github.com/rachidsahane/AICD-METHODOLOGY/blob/main/src/AICD_Methodology_v0.3.html

The site is served by GitHub Pages and responds only after the author enables Pages for this repository, per [PUBLISHING.md](PUBLISHING.md). Until the v0.3 release is published, the PDF link returns a 404 and the document can be read from the HTML source or built locally.

## How to cite

APA:

> Ngatcha Sahane, R. A. (2026). *AICD: Artificial Intelligence Centered Development* (Version 0.3) [Methodology document]. https://github.com/rachidsahane/AICD-METHODOLOGY. DOI: <<NEEDS: Zenodo DOI after first archived release>>

BibTeX:

```bibtex
@manual{sahane2026aicd,
  title   = {AICD: Artificial Intelligence Centered Development},
  author  = {Ngatcha Sahane, Rachid Alim},
  year    = {2026},
  version = {0.3},
  url     = {https://github.com/rachidsahane/AICD-METHODOLOGY},
  doi     = {<<NEEDS: Zenodo DOI after first archived release>>}
}
```

## Contributing and evolving the methodology

AICD is open to extension and closed to modification. The core, meaning the founding principles, the five-layer architecture and the separation of duties, is not revised to suit a project, a tool or a new model release; only the author changes it, and such a change increments the major version. Everything that depends on the current state of tooling is an extension point and is recorded as an organizational decision, while an addition to the methodology itself, a new agent role, a new ticket category, a new test family, a new document type or a compliance overlay, is proposed as an AICD Change Proposal, reviewed by every seat, and adopted with a minor version increment. Read [proposals/README.md](proposals/README.md) for what a proposal must contain and how one is reviewed.

## Building the PDF

Install the fonts the document uses first, system wide, as listed in [build/fonts.md](build/fonts.md). The build substitutes silently otherwise and the pagination changes. Then:

```sh
python3 -m pip install -r build/requirements.txt
build/build.sh
```

The output is `dist/AICD-Methodology-v0.3.pdf`, and the script prints the page count, which is 76 pages for v0.3. The build checks every image the document references and fails before rendering if any of them is missing from `src/`, so an incomplete PDF is never produced. The two generated images, `src/cover_bg.jpg` and `src/portrait_circle.png`, are committed to the repository and can be regenerated deterministically with `build/generate_assets.py`, which needs Pillow and NumPy in addition to the pinned build dependencies.

## License

AICD © 2026 by Alim Sahane is licensed under CC BY 4.0. To view a copy of this license, visit https://creativecommons.org/licenses/by/4.0/

Photographs and the author's likeness are excluded from this license and remain all rights reserved. The name AICD is subject to the trademark policy in [TRADEMARK.md](TRADEMARK.md).

The full license text is in [LICENSE](LICENSE). SPDX identifier: `CC-BY-4.0`.

## Author

Ngatcha Sahane Rachid Alim, writing as Alim Sahane.

- GitHub: https://github.com/rachidsahane
- LinkedIn: https://www.linkedin.com/in/alim-sahane/
- Email: rachidsahane007@gmail.com
