# AICD: Artificial Intelligence Centered Development

A software development methodology for teams whose code is written by AI agents.

Every methodology of the last forty years was built around one scarce resource: the time of skilled humans writing code. Waterfall planned that time, Scrum sliced it into sprints and estimated it in story points, and standups, retrospectives and velocity charts all exist to coordinate something expensive and slow to hire. That scarcity is going away. When producing code stops being the bottleneck, the difficulty moves somewhere else: to specifying precisely what should exist, to verifying that what was built is correct, and to deciding the architecture, the stack and what is worth building at all.

AICD is designed around those three bottlenecks instead of the old one. It reproduces a complete development team with AI agents that build, test, operate and document the software, and it places a small group of experienced engineers above them, who specify, verify, decide and supervise. Those engineers read code fluently and are hired for exactly that, but they do not write production code or test code. The specification is the source of truth, every change enters through git, and nothing ships without a human who understands the system approving it on evidence.

**[Read it online](https://rachidsahane.github.io/AICD-METHODOLOGY/)**  ·  **[Download the PDF](AICD-Methodology.pdf)**

Version 0.3, working draft, September 2026. 76 pages.

## What's inside

- **[Part I: Understanding AICD](https://rachidsahane.github.io/AICD-METHODOLOGY/#part1)** Why the methodology exists, what it is, and what it asks of the humans who use it. No technical background required.
- **[Part II: The architecture of AICD](https://rachidsahane.github.io/AICD-METHODOLOGY/#part2)** The structural core: the five layers, the agent team and how its roles are separated, and the memory that gives every agent knowledge of the whole project.
- **[Part III: How work flows](https://rachidsahane.github.io/AICD-METHODOLOGY/#part3)** How a need becomes a specification, a ticket, a branch, a verified pull request, a deployment and an observed behavior.
- **[Part IV: People and organization](https://rachidsahane.github.io/AICD-METHODOLOGY/#part4)** Who the humans are, what they own, how they are hired, and how they stay capable of disagreeing with the machines they direct.
- **[Part V: Governance, economics, resilience](https://rachidsahane.github.io/AICD-METHODOLOGY/#part5)** What it costs to run, how to know whether it is working, and what can go wrong.
- **[Part VI: Applying AICD](https://rachidsahane.github.io/AICD-METHODOLOGY/#part6)** How a product enters the methodology, either born inside it or migrated into it from a codebase that already exists.
- **[Part VII: Deep dives](https://rachidsahane.github.io/AICD-METHODOLOGY/#part7)** The memory service, running several products with one team, the security model of the agent fleet, the fleet dashboard, how the methodology evolves, and how its thresholds are calibrated.
- **[Part VIII: Extensions and profiles](https://rachidsahane.github.io/AICD-METHODOLOGY/#part8)** Profiles for mobile clients, for working without live telemetry, for regulated domains and for a single operator, plus what the first real application taught.
- **[Appendices](https://rachidsahane.github.io/AICD-METHODOLOGY/#appx)** Templates, glossary, document history.

## Start here

- **Founder or product lead.** Read [Part I](https://rachidsahane.github.io/AICD-METHODOLOGY/#part1), then [Economics and metrics](https://rachidsahane.github.io/AICD-METHODOLOGY/#s21) and [Failure modes and safeguards](https://rachidsahane.github.io/AICD-METHODOLOGY/#s22). That is what it is, what it costs, and how it breaks.
- **Engineer starting a new product.** Read [Part I](https://rachidsahane.github.io/AICD-METHODOLOGY/#part1) and [Part II](https://rachidsahane.github.io/AICD-METHODOLOGY/#part2), then work through [Starting a new product under AICD](https://rachidsahane.github.io/AICD-METHODOLOGY/#s23), which runs from gate G0 to gate G7.
- **Engineer migrating a product that already exists**, whether it was built with agents or entirely by hand. Read [Part I](https://rachidsahane.github.io/AICD-METHODOLOGY/#part1), then [Migrating an existing product into AICD](https://rachidsahane.github.io/AICD-METHODOLOGY/#s24), phases M0 to M5, and [Lessons from the first application](https://rachidsahane.github.io/AICD-METHODOLOGY/#s39) before you touch anything.
- **You only want the rules.** [Founding principles](https://rachidsahane.github.io/AICD-METHODOLOGY/#s3) is eight of them on one page. Then [Autonomy tiers and the permission model](https://rachidsahane.github.io/AICD-METHODOLOGY/#s17) and [Git and release workflow](https://rachidsahane.github.io/AICD-METHODOLOGY/#s13) for what an agent is allowed to do.
- **Working alone.** [Profile: the single operator](https://rachidsahane.github.io/AICD-METHODOLOGY/#s38) is the only accepted substitute for the second human that tier 2 changes require.

## Learned the hard way

Four findings from the first migration of a live product into AICD, each recorded in [Lessons from the first application](https://rachidsahane.github.io/AICD-METHODOLOGY/#s39) with the failure that earned it.

- **A ticket asked for the deletion of a directory described as a dead legacy backend.** The agent's first gate, prove which component serves production, showed the directory owned the live database's migration history and built two of five production images. Destructive tickets now state a belief and its source, never a conclusion, and proof precedes action. [Read it](https://rachidsahane.github.io/AICD-METHODOLOGY/#s39)
- **A rollback point was named in the backlog as if it existed. It did not.** Every precondition a ticket names is now verified to exist at approval time, not at execution time. [Read it](https://rachidsahane.github.io/AICD-METHODOLOGY/#s39)
- **Two CI workflows sat intact behind a manual trigger and a build target had no recipe, while every document cited them as gates.** A newly written citation checker returned failure on clean and dirty trees alike and looked like it was working. "Present but reporting nothing" is now a named defect class, and a gate is installed only after it has been seen to fail on a planted defect. [Read it](https://rachidsahane.github.io/AICD-METHODOLOGY/#s39)
- **Four drafting agents produced eleven fabricated section references, one of which would have removed a required check.** References are now checked mechanically: the section index is machine-readable, a checker validates every reference, and the drafting-error rate is a calibration metric. [Read it](https://rachidsahane.github.io/AICD-METHODOLOGY/#s39)

The pattern across all eight findings is worth stating once, and the document states it: none of the failures were the agents' inventions. Every one was a human belief written into an artifact as a fact, or a control that existed on paper. The gates caught them because the gates demanded proof rather than agreement.

## Discuss

Questions, disagreements and reports of applying AICD on a real product are all welcome in [GitHub Discussions](https://github.com/rachidsahane/AICD-METHODOLOGY/discussions). If you have run part of this on something real, what broke is more useful than what worked.

## Evolving the methodology

AICD is open to extension and closed to modification. The core, meaning the founding principles, the five-layer architecture and the separation of duties, is not revised to suit a project, a tool or a new model release; only the author changes it, and such a change increments the major version. An addition to the methodology itself, a new agent role, a new ticket category, a new test family, a new document type or a compliance overlay, is proposed as an AICD Change Proposal, reviewed by every seat, and adopted with a minor version increment. [proposals/README.md](proposals/README.md) has what a proposal must contain and how one is reviewed.

## How to cite

APA:

> Ngatcha Sahane, R. A. (2026). *AICD: Artificial Intelligence Centered Development* (Version 0.3) [Methodology document]. https://github.com/rachidsahane/AICD-METHODOLOGY

BibTeX:

```bibtex
@manual{sahane2026aicd,
  title   = {AICD: Artificial Intelligence Centered Development},
  author  = {Ngatcha Sahane, Rachid Alim},
  year    = {2026},
  version = {0.3},
  url     = {https://github.com/rachidsahane/AICD-METHODOLOGY}
}
```

[CITATION.cff](CITATION.cff) carries the same values in machine-readable form.

## License

AICD © 2026 by Alim Sahane is licensed under CC BY 4.0. To view a copy of this license, visit https://creativecommons.org/licenses/by/4.0/

Photographs and the author's likeness are excluded from this license and remain all rights reserved. The name AICD is subject to the trademark policy in [TRADEMARK.md](TRADEMARK.md).

The full license text is in [LICENSE](LICENSE). SPDX identifier: `CC-BY-4.0`.

## Author

Ngatcha Sahane Rachid Alim, writing as Alim Sahane.

- GitHub: https://github.com/rachidsahane
- LinkedIn: https://www.linkedin.com/in/alim-sahane/
- Email: rachidsahane007@gmail.com

Contributions, including how to build the PDF yourself, are covered in [CONTRIBUTING.md](CONTRIBUTING.md).
