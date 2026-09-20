# AICD Change Proposals

An AICD Change Proposal (ACP) is the document that proposes an extension to the methodology and records the decision made about it. It exists because AICD is open to extension and closed to modification: the core is fixed, and an extension to it is adopted only through a reviewed, recorded proposal. The process is defined by the methodology itself, in section 29, "Evolving the methodology: the extension process", of [the AICD document](https://github.com/rachidsahane/AICD-METHODOLOGY/blob/main/src/AICD_Methodology_v0.3.html); this file is the working procedure for this repository.

## What may change, and how

| Category | Examples | Procedure |
| --- | --- | --- |
| Parameters | Budget multiples, review cadence, coverage and mutation thresholds, autonomy step durations | Decided by the owning seat, recorded in organizational knowledge, no proposal required. Re-measured after any model change. |
| Tooling | Which models run which roles, observability platform, ticket system, memory service implementation | Recorded as an organizational ADR by the owning seat. |
| Extensions | A new agent role, a new ticket category, a new test family, a new document type, a compliance overlay | Requires an AICD Change Proposal, reviewed by all seats, adopted with a version increment. |
| Core | The founding principles, the five layers, separation of duties, the tier structure, the migration rule | Not changed by a team. A team that believes the core is wrong documents the evidence from a real project and proposes it to the methodology's author as a candidate for a new major version. |

Only the Extensions row needs an ACP. A parameter change or a tooling change is recorded where the table says and goes no further. A core change is not a proposal a team adopts; it is evidence sent to the author.

## Review and adoption

A proposal is adopted when every seat has reviewed it and the reliability and governance seat has confirmed it changes no permission without a corresponding control.

## Versioning

Parameter and tooling changes do not change the version. An adopted extension increments the minor version. A core change, which only the author makes, increments the major version. Every product records which version of AICD it runs, and a product is migrated to a new minor version by adopting the extension; there is nothing else to do, because extensions never invalidate what a product already does.

## How to submit a proposal

1. Copy [TEMPLATE.md](TEMPLATE.md) to a new file in this directory, named `ACP-NNNN-short-title.md`. `NNNN` is the next free four-digit number, zero padded. `short-title` is lowercase words joined by hyphens.
2. Fill every field. A proposal with an unfilled field is not reviewable and will be sent back rather than reviewed.
3. Open a pull request against this repository that adds the file. Set the status to `proposed`.
4. The review happens in the pull request. Every seat reviews, and the reliability and governance seat states in writing whether the proposal changes a permission without a corresponding control.
5. The author of the methodology, Alim Sahane, merges an adopted proposal. Merging is what records the adoption: the status becomes `accepted`, the target version becomes the version that ships it, and the index below gains an entry.

A rejected or superseded proposal stays in this directory with its status updated, so that the reasoning survives.

## Index

| Number | Title | Status |
| --- | --- | --- |
| [ACP-0001](ACP-0001-single-operator-profile.md) | The single operator profile | Accepted in v0.3 |
