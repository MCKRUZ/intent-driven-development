# What happens when things change

_Because they will. Four things routinely happen mid-engagement; each has a route that leaves a
record. None of them is "start the phases over." The decisions these routes reach back into are
laid out in [the shape of an engagement](shape.md); the rules behind them are in the
[standard](../GOLD-STANDARD.md) (sections 5.3a and 9) and the [build loop](build-loop.md)
(sections 2 and 3a)._

---

## The one rule for every route

A signed decision may be revised. The revision has an owner, a reason, a clock and a visible blast
radius, and it rides the same loop as any other change. What the standard forbids is the _quiet_
version: code that no longer matches a decision nobody updated. Each route below is the recorded
alternative to that drift. The commands named under "in our toolchain" are the `claude-code-sdlc`
plugin's; they are the example mechanism, not the rule. Harbor Mutual, the standard's fictional
worked example, exercises every one of them in [the step-by-step walkthrough](with-the-plugin.md).

## 1 · A new need appears during build

This is the normal case, and the loop exists for it. Nothing enters the loop as a conversation; a
new need becomes a story and clears the definition of ready at the weekly intent triage like any
other.

| | |
|---|---|
| **The trigger** | Someone, on either side, wants something the baseline did not name. |
| **The route** | Weekly intent triage. The story is written precisely enough to be checked (every line passes the vague-line test), scope in and out are both stated, the silent product decisions go on the decision list for the product owner to answer, a risk tier is assigned, and the existing pattern the change should reuse is named. Then it rides the loop: Intent, Delegate, Discern, merged and deployed to dev. |
| **Who owns it** | The Pod Lead owns triage, the risk tier and the routing. The product owner answers the decision-list items on the agreed clock. The Orchestrator writes the spec. |
| **What is recorded** | The spec: one file, in the repo, travelling in the same pull request as the code. The decision-list answers, with the owner's name. |
| **What it costs** | The tier the Pod Lead assigns: LOW gets the grader and a light human look, MEDIUM the grader plus a non-author Checker, HIGH the full ladder with a security pass and a named signature. No phase gate re-runs; the merge gates are the gate. |
| **In our toolchain** | `/sdlc-spec` turns the triaged story into a spec, ready or bounced. The decision list is visible in `/sdlc-status`. |

## 2 · Something learned disproves the design

Design was decided at the design gate, and contact with a real implementation sometimes proves the
choice wrong. That happens on serious platform projects, not just sloppy ones, and pretending
otherwise just means the revision happens without a record.

| | |
|---|---|
| **The trigger** | A decision record rests on an assumption nobody has tested, and the evidence starts pointing the other way. Acceptance criteria written about an unknown are fiction, and the grader would grade them as if they weren't. |
| **The route** | A **spike** first: a bounded experiment, boxed in time or tokens and agreed at triage, run on a `spike/` branch that a required CI check refuses to merge. Its deliverable is a written finding (what was assumed, what was tested against which system, what was found, whether the assumption survived); the code is deleted. If the finding invalidates the decision, the revision goes through as a HIGH-risk change with a named signature. The old record is marked superseded, never edited, so the history of what was believed when survives. |
| **Who owns it** | The Architect opens the spike when a decision has no evidence behind it, or the Pod Lead opens it at triage when a story cannot be made ready. The Architect signs the revised record; the client's lead engineer co-signs it, as with every decision record. |
| **What is recorded** | The spike finding, committed. The superseded record, still in place. The HIGH-risk change with its `SIGNED-OFF-BY` line: a name and a sentence, because a bare name is the thumbs-up this rung exists to reject. |
| **What it costs** | The spike's box, then a HIGH change: tight agent permissions, the full checking ladder, a security review pass, a named sign-off. The design gate is not re-run; the revision is the gate. |
| **In our toolchain** | `/sdlc-spike "does the carrier API dedupe on our idempotency key?"` runs the bounded experiment. `/sdlc-revise ADR-007` carries the revision through as a HIGH-risk change. |

## 3 · A signed requirement changes

The baseline was signed at the requirements gate. When a requirement changes afterwards, the
change is made visible rather than absorbed.

| | |
|---|---|
| **The trigger** | The product owner, a regulator, or the market changes what the system has to do, after the baseline was signed. |
| **The route** | The requirement is revised in place with an owner, a reason and a two-business-day clock. The affected downstream artifacts (design records, specs, tests) are listed so the blast radius is visible. The requirements gate is re-run. When the discovery runs the other way, and a merged change has drifted from its requirement, the reverse runs: the merged work proposes the upstream edit and a person confirms it. |
| **Who owns it** | The product owner owns the requirement and the answer clock. The Pod Lead routes the edit and re-tiers whatever work it touches. A person, never an agent, confirms an upstream edit proposed from merged work. |
| **What is recorded** | A decision-log row with owner, reason and clock. The revised artifact, whose content history keeps every prior version. The list of what the change put at risk. The re-run gate report. |
| **What it costs** | The gate re-run, plus the tier of whatever downstream work the change forces: a changed public API contract or a schema migration is HIGH regardless of how small the wording change was. |
| **In our toolchain** | `/sdlc-revise FR-012` routes the edit to its owning discipline, opens the decision-log row, re-runs the phase's gate and lists what is at risk. `/sdlc-version list\|diff\|rollback FR-012` is the requirement's content history: what it said at each version, the diff between any two, and a roll-back when a revision went wrong. `/sdlc-refresh detect --spec specs/0016-duplicate-claim-merge.md` after a merge asks whether upstream drifted, and proposes the edit for a person to apply. `/sdlc-audit-artifacts` finds stale artifacts anywhere. |

## 4 · A gate fails

Gates tell you whether you may advance; a named human decides whether you do. A failed gate is
not an event; it is the gate doing its job.

| | |
|---|---|
| **The trigger** | The automated battery at a phase boundary (integrity, completeness, metrics, compliance, consistency, quality) reports something missing, or a merge gate on a pull request goes red. |
| **The route** | Nothing advances. The gate report says what is missing; the fix rides the loop; the gate runs again. A failed merge check goes back to the same Orchestrator, who drives the fix on the same branch, and every gate, including a fresh grader run, runs again before merge. The mechanical gates are never overridden. A quality-gate override requires written justification recorded with the phase state. A true emergency merge past a gate takes the Pod Lead and one other human, a `gate-exception` label, and a Retro+ agenda item. Two exceptions in a month means the gate or the specs are wrong; fix that, don't keep excepting. |
| **Who owns it** | The named human who would sign the gate. For an emergency merge, the Pod Lead plus one other named person. |
| **What is recorded** | The gate report. Any override, with a name, a reason and an expiry. The exception label on the pull request and the retro item that follows it. |
| **What it costs** | The time to fix what the report names, and no more. An override costs a name, a sentence and a retro; the standard is built so that it never costs less than that. |
| **In our toolchain** | `/sdlc-gate` runs the battery and opens the HTML report. `/sdlc-next` refuses to advance without the gate passed and a named human's sign-off. |

## 5 · Reopening a Phase 0 decision

The problem statement, the success metric, the product-owner mode and the tooling decision are the
four things signed at the very first gate, and every later signature stands on them. Reopening one
is the most expensive change in the engagement. Because billing milestones map to gates, it is also
a statement-of-work conversation, and it belongs at steering rather than in a pull request.

It does happen: a metric turns out to be unreadable where it was supposed to be read, a named
product owner leaves and proxy mode has to start, a client's AI procurement stalls. The route is
the same shape as every other reopening (an owner, a reason, a record, the gate re-run), with the
sponsor holding the pen and the affected downstream signatures listed before anyone agrees to it.
Nothing on this page makes it cheap; the point is that it is visible.

## Is this waterfall?

No. Waterfall phases the middle and checks a large batch of work at the end; this standard refuses
to phase the middle at all and checks every change, inside the loop, before it merges. The opening
and closing gates are ordered decisions with named owners, not calendar stages, and each of them
can be reopened through the routes above without starting anything over.
