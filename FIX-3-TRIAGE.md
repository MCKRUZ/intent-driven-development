# Fix 3 — triage of the 42 unreceipted rituals

> **Status:** proposal, awaiting Matt's review. Nothing here is implemented.
> **Decision taken:** ships as a **major version** with a migration note, not behind a profile flag.
> A flag defaulting to off is Fix 3 shipped disabled, which is how the repetition dial ended up in limbo.

## What this is

`PLUGIN-SYNC.md`'s second finding: of 110 artifacts across the ten Example-tab ledgers, **65** are
machine artifacts, **3** are human receipts (all in Phase C), and **42** are human work that leaves
no trace. Fix 3 is applying Phase C's `close-gate-evidence.md` pattern to the other 42.

The instruction was "add an artifact spec and a registry entry for each." Reading all 42 against
what they actually are, **that would be wrong for 24 of them** — and adding 42 required files in one
release is a lot of new scaffolding for a standard that warns:

> Scaffolding that hedges model weakness should be expected to shrink; scaffolding that carries
> human accountability should not.

So they are triaged four ways.

## The four dispositions

| | Disposition | What it means | Count |
|---|---|---|---|
| **A** | **Required receipt** | A file, gate-checked, with a HITL gate that refuses to advance without it or a named waiver | **11** |
| **B** | **Optional receipt** | A file when the work happens, surfaced to the approver at sign-off via G7. Never blocks | **14** |
| **C** | **Verify, don't file** | It is a state of the world, not a document. Check the real thing; a markdown file asserting it is *weaker* | **6** |
| **D** | **No artifact** | Already recorded inside a parent artifact the gate checks, or the receipt would be ceremony | **6** |

Plus **one CI mechanism** (not an artifact) and **one already fixed** (`close-handoff.md`, done in the
defect sweep).

The 37 dispositions cover 39 of the ledger rows — A2 and A7 each absorb two rows, because the same
receipt serves two phases. 39 + 2 (the CI mechanism's two rows) + 1 (`close-handoff.md`) = **42**.

**The test for A vs B:** *in an incident review, would you need to know whether this happened?* If the
answer is "yes, and its absence would change the conclusion," it blocks. Otherwise it records.

---

## A — Required receipt, with a HITL gate (11)

These block the phase. Each is load-bearing, none can be performed by a command, and each is the
reason a client pays for a pod rather than a prompt.

| # | Artifact | Phase | Why it blocks | Today |
|---|---|---|---|---|
| A1 | `decision-list.md` | 1 | Every unmade product call, numbered, owned, on the 2-day clock. The Definition of Ready depends on it: a spec cannot be ready with an open decision for its story. Nothing writes it | nothing |
| A2 | `spikes/NNNN-*.md` | 1, 2, Build | Each risky assumption confirmed or falsified against the live system. The code is deleted; the finding is the deliverable. Covers both the Phase 1 feasibility spikes and the Phase 2 design spikes | `spikes/` optional; template ships; **no HITL gate** |
| A3 | `threat-model.md` | 2 | The guarded-path map Phase 3 wires its security gates from. Without it, which paths are guarded gets decided at wiring time, from memory | spec + Step 7 exist as **RECOMMENDED** |
| A4 | `nfr-proving-plan.md` | 2 | Per quality target: the verification method and the named place its number will be read. Phase 9 reads it back — a target with no proving plan is a wish | nothing |
| A5 | `walking-skeleton-spec.md` | 2 | The thin end-to-end slice Phase 3 must ship, sufficient to exercise every ADR's mechanism once. Phase 3 builds from it | **optional** in registry |
| A6 | `data-flow-brief.md` | 3 | What goes to the API, what does not, where keys live, who sees usage — in client security's hands, in writing. Contractual, not just technical | nothing |
| A7 | `cold-checkout-record.md` | 7 | The doc-defect log from a cold verifier following the README, and the client ops engineer walking the RUNBOOK through deploy → rollback → one failure. Phase 7's entire purpose is *prove a stranger can run this*; without the record, nothing distinguishes a phase that did it from one that did not | nothing |
| A8 | `rollback-rehearsal.md` | 8 | The timestamped deploy → roll back → redeploy timeline, run by the client's operators, with time-back-to-healthy. "A rollback that has never run is a wish" is already in the standard; this is the wish becoming a fact | nothing |
| A9 | `go-no-go-record.md` | 8 | Every named role asked and answered, the decision and rationale recorded with names. The most critical gate in the lifecycle currently produces an optional file nothing writes | **optional** in registry |
| A10 | `secrets-rotation-record.md` | 8 | Production secrets rotated to values the pod never held, signed by client security. The handoff made literal — and the single most audit-relevant fact at close | nothing |
| A11 | `drill-record.md` | 9 | Per critical alert: trigger, detection time, routing, responder, outcome. The one proof the pager works. An alert that has never fired is a configuration, not a control | **optional**; no step runs the drill |

**Six of the eleven already have partial machinery** (A2, A3, A5, A9, A11 exist as optional or
recommended; A3 has its spec). For those, Fix 3 is a promotion plus a HITL gate, not new authorship.

---

## B — Optional receipt, surfaced at sign-off (14)

Real work, worth recording, but its absence does not by itself mean the phase was done badly. These
become `optional` registry entries plus a G7 prose condition, so the approver **sees** them at
sign-off without the gate blocking.

| # | Artifact | Phase | Note |
|---|---|---|---|
| B1 | `po-decision-record.md` | 0 | SOW precondition with billing teeth. Commercial rather than technical; defensibly folded into `constitution.md` (Decision Authority), but a named file is cleaner |
| B2 | `tooling-record.md` | 0 | The other billing-teeth precondition — Anthropic access live under the client's account, or a signed fallback rider with a date |
| B3 | `workshop-brief.md` | 0 | Curated by a human, questions only. Today it is drafted, sent, and never committed |
| B4 | `scope-out-record.md` | 1 | The explicit not-in-v1 list the sponsor has seen, so nobody assumes a cut item into the build |
| B5 | `adversarial-review-record.md` | 1 | Fresh reviewers attacking the draft from product, quality and security angles; the catches recorded |
| B6 | `consistency-check-record.md` | 2 | Requirements traced against design both directions; orphans resolved or removed |
| B7 | `spec-audit-record.md` | 7 | Five to ten specs, weighted HIGH-risk, acceptance checks executed by hand against dev |
| B8 | `rollout-shape-decision.md` | 8 | Cutover / pilot / parallel, the in-flight-work answer, the fallback and its trigger — owned by the client, in writing, before the ceremony |
| B9 | `what-healthy-table.md` | 9 | Per failure scenario: healthy, degraded, who is woken, who is told in the morning. Currently folded into `monitoring-config.md` only if someone remembers |
| B10 | `fatigue-review-record.md` | 9 | Each proposed alert replayed over hypercare history; anything firing weekly without action raised or cut, with the count |
| B11 | `outcome-metric-first-read.md` | 9 | The headline number read honestly for the first time in production, caveats attached |
| B12 | `outcomes-dashboard-handover.md` | C | Already optional; needs the G7 condition so it is at least seen |
| B13 | `harvest-pr-notes.md` | C | Already optional. The PR itself lands in another repo the gate cannot see — the note is the only local trace |
| B14 | `retro-file` | C | Lives in the delivery-standard repo, outside `.sdlc/`. Record the link, not the file |

**B1 and B2 are the two I am least sure about** — see the open questions below.

---

## C — Verify, don't file (6)

These are states of the world. A markdown file asserting "branch protection is on" is *weaker* than
reading the setting, and it goes stale silently. Check the real thing.

| # | Item | How to verify instead |
|---|---|---|
| C1 | Branch protection | **Already done** — `/sdlc-doctor` reads the rulesets and reports whether any is enforcing |
| C2 | The security gates, fired | `gh` can confirm the workflow ran on a real PR. A probe PR touching a guarded path is the Phase 3 confirmation pass added in the defect sweep |
| C3 | The deployed walking skeleton | Running software. Verified against A5's definition by a human at the gate; a file claiming it is deployed proves nothing |
| C4 | The outcome metric, ticking | A measured property of the dashboard, read at the gate |
| C5 | The metrics line (per-merge data) | Telemetry, not a receipt. This is **IDD #12** (fleet observability), already open |
| C6 | The central provenance log | Same — **IDD #12**. A per-phase markdown file is the wrong shape for a continuous log |

---

## D — No artifact (6)

| # | Item | Why not |
|---|---|---|
| D1 | Error-behavior specs | Already written into `requirements.md`, which the gate checks. A separate file duplicates it and drifts |
| D2 | Traceability matrix | Same — inside `requirements.md` |
| D3 | User stories | Same — inside `epics.md` |
| D4 | Data model | Inside `design-doc.md`; `data-model.md` also exists as optional. Nothing missing |
| D5 | The non-author approval | GitHub records the approver, and branch protection enforces non-author. It is recorded — outside `.sdlc/`. Duplicating it into a file adds a second source that can disagree with the first |
| D6 | The "grader was read" receipt | The Checker's approval *is* the act. A receipt asserting they read the verdict is unfalsifiable ceremony — it records a claim, not a fact |

---

## The one CI mechanism (not an artifact)

**The `risk:high` named sign-off** (ledger rows 2 and 45). Today it is convention in a PR comment;
nothing templates it and nothing checks it. This is genuinely load-bearing — a name accepting the
risk, not a thumbs-up — but the right shape is **a required status check**, not a file:

- A PR-comment template the reviewer fills (`SIGNED-OFF-BY: <name> — <sentence>`)
- A `risk-signoff` CI job that fails when the `risk:high` label is present and no such comment exists
- Added to `branch-protection.json`'s required contexts

A markdown receipt would sit in `.sdlc/` describing a merge that already happened. The check has to
be at the merge.

---

## What this costs

| | Count | Work |
|---|---|---|
| New required artifacts | 6 | A1, A4, A6, A7, A8, A10 — authored from scratch |
| Promotions (already exist) | 5 | A2, A3, A5, A9, A11 — registry change + HITL gate |
| New optional artifacts | 11 | B1–B11 specs + registry entries |
| Registry-only | 3 | B12–B14 G7 conditions |
| CI mechanism | 1 | `risk-signoff` job + ruleset entry |
| Nothing to do | 12 | C1–C6, D1–D6 — documented as deliberate |

**Migration impact:** 11 newly-required artifacts. Any engagement past the relevant phase fails its
next `/sdlc-gate` until each is produced or explicitly waived. That is the whole reason this is a
major version.

---

## Open questions for Matt

1. **B1/B2 — the PO decision record and tooling record.** Both are SOW preconditions with billing
   teeth, which is an argument for **A**, not B. I put them in B because they are commercial
   artifacts that live in the contract, and duplicating them into `.sdlc/` risks the file and the
   SOW disagreeing. If you would rather the gate hold the engagement until they are recorded, they
   move to A and the required count goes to 13.

2. **A7 — one file or two?** The README cold-checkout and the RUNBOOK cold walk-through are two
   different rituals by two different people. One file keeps Phase 7 to a single new artifact; two
   files keep the receipts honest to who performed them. I lean **two**, but it makes Phase 7 the
   heaviest phase in the release.

3. **The waiver mechanism.** Every HITL gate needs an escape or it will be worked around. I propose
   a named waiver recorded *in the artifact itself* — the file exists, and says "waived by <name>,
   because <reason>." A missing file blocks; a waived one does not. That keeps the record honest
   about what was skipped, which is the same principle as the eval-bypass ledger.

4. **Sequencing.** 11 required artifacts is a large single release. An alternative is two: the six
   promotions first (they already exist, so the migration is smaller), then the five new ones. I
   lean **one release** — a half-migrated gate is worse than either end state — but it is your call.
