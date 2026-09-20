# ACP-0001: The single operator profile

## Metadata

- **ACP number:** 0001
- **Title:** The single operator profile
- **Author:** Alim Sahane, author of the methodology
- **Status:** `accepted`
- **Target version:** 0.3
- **Date:** 2026-09

## The problem observed on a real project

Tier 2 requires CI green, lead agent approval, two humans, a written rollback plan, and at least one human who reads the diff itself. It covers authentication and authorization, payments, data schema and migrations, infrastructure, secrets, external contracts, and anything covered by an ADR. A person running AICD alone meets every part of that except one: there is no second human. Without a profile the solo operator either abandons tier 2 work, or merges it with the second reviewer quietly missing and nothing saying so. The second outcome is what this proposal prevents.

Section 29 asks for evidence from the metrics of section 21. The document records no metric values for the first application; it records eight findings in section 39, each paired with the failure that earned it. Those that bear on an operator without a second reviewer:

- A ticket instructed deleting a directory described as a dead legacy backend. It owned the live database's migration history and built two of five production images. The repository also ran an undocumented dual-runtime architecture in which a service described as retired owned the schema.
- A rollback point was named in the backlog as if it existed. It did not.
- Two CI workflows sat intact behind a manual trigger and a build target had no recipe, while every document cited them as gates; a citation checker looked like it was working while returning failure on clean and dirty trees alike.
- Four drafting agents produced eleven fabricated section references, one of which would have removed a required check.
- Two migration chains wrote to one database with no down-migration and no snapshot, and had already produced one incident repaired by hand.

Section 39 states the pattern once: every one was a human belief written into an artifact as a fact, or a control that existed on paper. The ordinary defense is a second person to doubt the belief or notice the gate that never fired. A solo operator has to reproduce that effect by other means.

## The proposed extension

A profile recording the only accepted substitute for the second human, so that a solo operator runs the methodology with a documented, expiring exception rather than a silent gap. All of the following are required together for every tier 2 change:

1. Independent review by a different model than the coder, with a hard veto rather than an advisory opinion, working through the adversarial checklist.
2. The operator's own full diff read, in a separate session from the one in which the plan was approved, at least several hours later.
3. Rollback rehearsed on staging for that specific change before merge, and for changes with data migrations, a snapshot taken immediately before the migration with a rehearsed restore.
4. Migrations backward compatible with the previous tag, behind a flag where the change is behavioral.
5. Limited rollout where the product supports it, with the operations agent authorized to halt.

The exception is recorded as an ADR with status accepted and an expiry condition: the day a second seat is filled. Until then, the operator merges every tier 1 and tier 2 change personally, and no agent merges above tier 0.

## Which founding principle it serves

Principle 5, nothing ships without human verification: a human who understands the system design approves every behavioral change, on the test plan, the coverage evidence and the agent's report. The profile keeps that approval intact where only one human exists, and reinforces it with substitute 2, which puts the full diff read at a remove in time from the approval of the plan. It also serves principle 7, every producing agent is separated from the agent that judges it: substitute 1 keeps the reviewer on a different model from the coder and gives it a veto rather than an opinion.

## Demonstration that it violates no founding principle

Principles 1, 2, 4 and 8 are untouched: the operator writes no production code or tests, the specification stays the source of truth because the profile adds merge conditions and not a source of behavior, no technology is selected, and substitute 1 names no vendor and no model. Principle 3 is strengthened, since every change above tier 0 passes through the operator's own hand on the repository. Principle 5 is strengthened by substitute 2, principle 6 by substitute 5, and principle 7 by substitute 1.

The profile grants no agent anything it did not have. The merge policy of section 13 already confines agent merges to tier 0; the profile restates that, and adds that the operator merges every tier 1 and tier 2 change personally. The confirmation section 29 asks of the reliability and governance seat, that no permission changes without a corresponding control, therefore has nothing to object to. The document records that one person may hold more than one seat early on, and records no separate adoption procedure for a proposal reviewed by an operator holding every seat.

## Compensation structure replaced, and the evidence

None. The profile replaces no compensation structure and removes none.

Section 5 distinguishes control structures, which keep humans accountable for what runs in production however capable the models become, from compensation structures, which exist because today's agents sometimes loop, drift or share blind spots. The two humans of tier 2 are a control structure, and section 27 lists them as the safeguard against an insider abusing a seat. A compensation structure is removed only after evidence, on a real project, that the limitation it compensated for is gone; no such evidence is claimed here, and none is recorded in the document.

The profile adds rather than removes: a conjunction that applies only where the second seat is empty, and an expiry that retires it the day that seat is filled.

## Parameters introduced, and their calibration

The profile introduces no new numeric parameter. It introduces a required conjunction and an expiry condition. The conjunction is that the five substitutes are not a menu: four of five is not the profile, and a tier 2 change that cannot satisfy all five does not merge. The expiry condition is the day a second seat is filled, recorded in an ADR with status accepted.

Calibration is open. Section 40 lists this profile among the items still to validate on real products, in these terms: whether its five substitutes hold up over months, and what the second seat changes when it arrives. The document records no calibration procedure for it in section 30, no threshold, and no measured rate. The one interval it names, that the diff read happens in a separate session at least several hours later, is qualitative, and this proposal does not turn it into a number.

## Status

`accepted`, on the evidence above. Adopted in version 0.3, September 2026, as section 38 of the methodology document, under the extension procedure of section 29, where an adopted extension increments the minor version.
