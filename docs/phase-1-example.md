# Phase 1 Worked Example: Harbor Mutual

The continuation of [the Phase 0 example](phase-0-example.md), companion to
[the Phase 1 deep-dive](phase-1-requirements.md). Phase 0 closed Friday 2026-03-13 with a
signed outcome statement, a verified 11.4-day baseline, and two open questions. This is the
week that follows.

The pod fills in for Phase 1: Maya Chen (Pod Lead) and Rob Feld (Setup Owner) are joined by
**Jonah Kim** and **Sara Whitfield** (Orchestrator/Checkers) and **Nadia Brooks** (Quality
Engineer). On the Harbor side, Luis Ortega's 6 hours per week start getting spent.

**The story so far (you can start here):**

| | |
|---|---|
| **The client** | Harbor Mutual — a fictional regional insurer. They hired a five-person consulting pod to rebuild how property-insurance claims get reported and decided. |
| **The problem** | A claim takes a median of **11.4 days** from FNOL (first notice of loss — the policyholder reporting the damage) to a coverage decision. Customers who wait renew less. |
| **The target** | Median **5 days or less**. |
| **The hard facts** | Harbor's claims and policy data live in **PolicyOne**, an aging core system that syncs data downstream only once per night (the "nightly batch"). Product decisions belong to **Luis Ortega**, Harbor's product owner, on a 2-business-day answer clock. |
| **Where we are** | Phase 0 (discovery) closed last Friday: signed problem statement, 8 client documents cataloged (DOC-001..008), and two open questions — **Q-13** (do state claim-acknowledgment rules differ per intake channel?) and **Q-14** (what share of claims is simple enough to fast-track?). |
| **Our pod** | Maya Chen (Pod Lead) · Rob Feld (Setup Owner) · Jonah Kim, Sara Whitfield (Orchestrator/Checkers) · Nadia Brooks (Quality Engineer). |
| **Harbor's cast** | Karen Voss (VP Claims Operations — sponsor) · Luis Ortega (product owner) · Priti Shah (data and reporting lead) · Dan Kowalski (IT security) · Dee Alvarez (intake supervisor) · Gail Tran, Marcus Webb (senior adjusters). |

**The IDs you'll see on this page:**

| ID | What it means |
|---|---|
| **DOC-NN** | A client document cataloged in Phase 0. |
| **C-NN** | A constraint from Phase 0. |
| **CON-NN** | A contradiction resolved in Phase 0. |
| **Q-NN** | An open question with a named owner. |
| **D-NN** | A product decision. |
| **REQ-NN** | A requirement — what the system must do, with acceptance criteria, the checks that prove it. |
| **NFR-NN** | A non-functional requirement — a measurable quality target (speed, capacity, availability). |
| **E-NN** | An epic — a large slice of work. |
| **AQ-NN** | An architectural question Design must answer — each becomes an ADR in Phase 2. |
| **P0** | The top priority tier. |

## What Phase 1 received

Before a single requirement is written, five files arrive and two questions are still open.

Harbor Mutual — a fictional regional insurer — hired a five-person pod to rebuild how
property-insurance claims get reported and decided. A claim takes a median of **11.4 days** from
FNOL (first notice of loss) to a coverage decision; the target is **5 days or less**. Phase 0
closed Friday 2026-03-13 with a signed problem, a verified baseline, and two open questions.
Requirements does not start from a blank page — it starts from these five files, on disk, in
Harbor's own repository.

**Inherited from Phase 0** — the signed problem baseline; the plugin's Step 0 reads
`phase1-handoff.md`: `phase1-handoff.md`, `constitution.md`, `problem-statement.md`,
`success-criteria.md`, `constraints.md`.

**The number, and the two unknowns that come due this week.** The whole engagement turns on one
number, and Phase 1's requirements are what have to move it. Two questions Phase 0 could not
close came forward — and their answers shape the requirements, so they are due Monday.

**11.4 → ≤ 5.0** — days from claim to decision today → the target the requirements must actually
move.

- **Q-13** (Luis) — do state claim-acknowledgment rules differ per intake channel?
- **Q-14** (Priti) — what share of claims is simple enough to fast-track?

**Where the week is headed.** Phase 1 turns the signed problem into a list of exactly what the
system must do, written so precisely that two people could not build two different things from it.
Everything this week is either a behavior the system must have, a number it must hit, or a
decision a named human still owes.

**Luis Ortega is the one to watch.** Harbor's product owner spends his first real hours here: he
assigns every priority, answers every product decision on a two-business-day clock, and does the
cutting when the top tier is over budget. The pod advises; Luis owns.

> **Carried in from Phase 0, still open on Monday:** Q-13 — per-channel acknowledgment rules?
> (Luis) · Q-14 — how many claims are simple enough to fast-track? (Priti)

**The cast.**

| Side | Person | Role |
|------|--------|------|
| Pod | Maya Chen | Pod Lead — runs elicitation, owns requirement quality and the handoff |
| Pod | Rob Feld | Setup Owner — enablement runs ahead; answers feasibility questions |
| Pod | Jonah Kim | Orchestrator / Checker — runs the feasibility spikes |
| Pod | Sara Whitfield | Orchestrator / Checker — runs the feasibility spikes |
| Pod | Nadia Brooks | Quality Engineer — the testability conscience; owns traceability |
| Harbor | Karen Voss | VP Claims Operations — sponsor; sees the scope-out list, approves the advance |
| Harbor | Luis Ortega | Product owner — assigns priorities, answers decisions on a 2-day clock |
| Harbor | Priti Shah | Data & reporting — the storm data, the instrumentation, Q-14 |
| Harbor | Dan Kowalski | IT security — the replica-access question (Q-15) the requirements raise |
| Harbor | Domain experts | Gail Tran, Marcus Webb (adjusters), Dee Alvarez (intake), compliance |

**The ID codes, decoded.** Every artifact in this engagement carries a stable identifier, so a
requirement written in week two can still be traced in month nine. You'll see these throughout:

| Prefix | Means | Born in | Example here |
|--------|-------|---------|--------------|
| `DOC-NNN` | A client document taken in at intake | Phase 0 | DOC-003 FNOL channels · DOC-007 the stale 2023 API inventory |
| `C-NN` | A constraint — a hard limit the requirements must honor | Phase 0 | C-03 auto-proof · C-04 15-day clock · C-05 PII-in-tenant |
| `CON-NN` | A Phase 0 contradiction, resolved | Phase 0 | CON-01 real-time vs nightly batch |
| `Q-NN` | An open question with an owner and a due date | any | Q-13, Q-14 due this week; Q-15, Q-16 born here |
| `D-NN` | A product decision the PO owes us | Phase 0/1 | D-07 duplicate merge · D-09 fast-path recommends |
| `REQ-NNN` | A functional requirement | Phase 1 | REQ-014 same-business-day coverage |
| `NFR-NN` | A non-functional requirement — a quality target | Phase 1 | NFR-02 the 10x storm surge |
| `E-NN` | An epic — a slice of the work, traced to an outcome | Phase 1 | E-01…E-06 |
| `AQ-NN` | An architectural question Design must answer | Phase 1 handoff | The four that become Phase 2's ADR-001–004 |

The last row is the thread out of this phase. Phase 1's handoff records the `AQ-NN` — the
architectural questions the requirements raise but must not answer. Phase 2's very first step
reads exactly those out of `phase2-handoff.md` and turns each into a signed ADR. An `AQ` with no
ADR at the end of design week is a gate failure.

## The procedure, step by step

Phase 1 is eight numbered steps in `claude-code-sdlc` and five working days in this standard —
the same week seen twice. Below they're braided: what the tool runs, what the humans do that the
tool cannot, and the file each day leaves behind. This is the drafting-heaviest week of the
engagement, and also the one where the most human work leaves no receipt. **Step through it.**

The state markers used throughout:

- `▪` a command does it — and writes the file
- `▸` a person does it — and it is recorded
- `⚠` a person does it — and nothing records it

### Day 1 — Mon 3/16 · plugin Step 0 opens

**Confirm the scope, then draw the map of the work.**

**Tooling —** `/sdlc-next → Step 0 HITL gate` · `/sdlc-coach → requirements-analyst` ·
*human decision*
**Artifacts out —** ▸ *Q-13 & Q-14 answered — decisions, not yet on disk* · ▸ *candidate epic map
(draft)*

Before any requirement is written, the plugin stops for a human. Claude reads `phase1-handoff.md`
and confirms scope: are Phase 0's open questions answered, is the prioritization clear, is
anything expected that Discovery missed? Only then does drafting begin. The pod's own day-1 craft
— which no command performs — is drawing the candidate epic map and planning one elicitation
session per slice.

> **At Harbor:** **Q-13** (Luis): the 15-day acknowledgment clock applies to every channel, and
> one regulated state requires a *written* acknowledgment — a portal screen alone does not count.
> **Q-14** (Priti): the segmentation query says **61%** of claims are single-dwelling, no-injury,
> under $25k. The `requirements-analyst` agent drafts the six-epic map; Maya corrects one boundary
> (email is its own beast, not part of the queue epic). Jonah and Sara start the feasibility
> spikes.

### Day 2 — Tue 3/17 · elicitation · no command runs

**Draw the requirements out of the people who do the work.**

**Tooling —** *none — human elicitation sessions; Claude preps question lists and structures the
notes after*
**Artifacts out —** ▸ *31 candidate requirements, each source-traced (draft)*

The requirements come from humans in rooms, not from the tool. Five working sessions, 60 to 90
minutes each, one per epic area, the right person in every room — and crucially not just the
managers. By evening Claude has structured the notes into candidate functional requirements, each
carrying a source trace back to the document or session it came from.

> **At Harbor:** Sessions: queue/assignment (Dee **plus two intake clerks**), coverage (Gail,
> Marcus), fast-path (Luis, Marcus), acknowledgments (compliance), instrumentation (Priti). The
> clerks — not their supervisor — reveal the **duplicate-FNOL workaround**: the same loss reported
> by phone and portal gets two claim numbers today. That one finding becomes REQ-004 and D-07.
> Talk only to managers and it never surfaces.

### Day 3 — Wed 3/18 · plugin Steps 1–2

**The full draft — and what it exposes.**

**Tooling —** `/sdlc-coach → requirements-analyst`
**Artifacts out —** under `.sdlc/artifacts/01-requirements/`: `requirements.md` ·
`non-functional-requirements.md` · ⚠ *the decision list — regenerated in the session; no file
holds it*

Now the tool writes. Step 1 turns the notes into functional requirements — "the system shall…",
each with a priority, a source trace, and (for the top tiers) an explicit error specification:
what it accepts, what it returns, what it does on each failure. Step 2 writes the non-functional
requirements, every number carrying a measurement basis. The decision list regenerates and the
testability pass runs.

> ⚠ **The gap:** The standard's decision list is the PO's work queue — every unmade product call,
> visible, on a two-business-day clock. In `claude-code-sdlc` Phase 1, **no file holds it.** The
> plugin's Step 0 asks the human about open questions once, in conversation; nothing writes them
> down, ages them, or checks at the gate that they were answered. The clock the SOW bills against
> has no artifact behind it.

> **At Harbor:** 31 functional requirements and 7 NFRs land. **NFR-02 exposes the storm-surge gap**
> nobody had named — Phase 0 sized annual volume only. The decision list regenerates to nine open
> items for Luis; D-07 is answered same day, D-09 takes the full two days. Nadia's testability pass
> sends **5 of 31** acceptance criteria back for being untestable. A 30-minute sponsor checkpoint
> keeps the day-5 review free of surprises.

### Day 4 — Thu 3/19 · plugin Step 3 · the priority session

**The product owner does the cutting.**

**Tooling —** `/sdlc-coach → stories + P0 error specs` · *the priority session — the PO's room; no
command sets an order*
**Artifacts out —** `epics.md` · ⚠ *the P0 budget & the cut list — a decision, no file* · ⚠
*feasibility spike findings — no command writes them*

Step 3 writes the epics — user stories in "as a / I want / so that" form with Given/When/Then
acceptance criteria — into `epics.md`. But the day's real work is human and has no command: the
priority session, where the PO ranks within a hard top-tier budget the pod announced, and cuts
whatever doesn't fit. Feasibility spike results land and get reconciled.

> ⚠ **The gap:** The word "spike" appears in no file in `claude-code-sdlc`'s Phase 1. Nothing
> prompts a feasibility check against the live system, and nothing records what it found. At Harbor
> the spikes were the most valuable hour of the week — and they leave no receipt.

> **At Harbor:** The 90-minute priority session: a **12-slot** budget, **19** candidates, Luis cuts
> **7** — including, painfully, the adjuster-dashboard rebuild. Epics get sequenced by what moves
> the metric. Error behavior is written for all 12 P0 requirements. The spikes land: DOC-007 (the
> 2023 API inventory) is stale in a useful direction — PolicyOne now exposes a read-only **nightly
> snapshot replica** (becomes **Q-15**), and the FNOL inbox is readable programmatically.

### Day 5 — Fri 3/20 · plugin Steps 4–7 · the gate

**Break it, check it, sign it.**

**Tooling —** `/sdlc-review --adversarial → multi-reviewer` ·
`/visual-explainer → .sdlc/reports/phase01-visual.html` · `/sdlc-gate → check_gates.py` ·
`/sdlc-next → advance_phase.py`
**Artifacts out —** `phase2-handoff.md` · `phase01-visual.html` · `phase01-report.html` · ⚠ *the
adversarial-review record* · ⚠ *the traceability check* · ⚠ *the scope-out record* · ▸ *the PO's +
sponsor's sign-off — billing milestone 2*

Fresh reviewers that did not write the draft attack the set from product, quality, and security
angles. The traceability check runs. Then the tool writes the handoff, renders the stakeholder
report, and the gate runs and stops for a human. `advance_phase.py` will not move the engagement
forward without a named sign-off.

> ⚠ **The gap:** `check_gates.py` verifies that four files exist, are non-empty, and contain no
> placeholder text: `requirements.md`, `non-functional-requirements.md`, `epics.md`,
> `phase2-handoff.md`. It never reads the nine-bullet exit checklist this standard specifies —
> priorities assigned by the PO, the scope-out seen by the sponsor, error specs for every top-tier
> operation, traceability traced both ways. That list lives in `phase-registry.yaml`, and no code
> opens it. *The human gate is real. What it asks is not.*

> **At Harbor:** The traceability check cuts the untraced SMS requirement (it traced only to RFP
> boilerplate). The `multi-reviewer` pass plus Nadia produce two catches: **REQ-022**
> (bounce-to-postal fallback for a bounced acknowledgment) and the fast-path/regulatory-clock
> conflict. The gate passes clean; Claude drafts the Phase 2 handoff. Luis confirms the requirements
> say what he meant; Karen sees the scope-out list. Sign-off; the engagement advances. First
> biweekly steering booked for Thursday 3/26.

## What Phase 1 produced

The requirements phase's whole output, named. Blue (`▪`) rows are written by a command and checked
by the gate. **Amber (`⚠`) rows are the method's human work** — required by this standard,
produced by no tool, and today leaving no file of their own behind. Those are the rows to argue
about.

State markers:

- `▪` a command does it — and writes the file
- `▸` a person does it — and it is recorded
- `⚠` a person does it — and nothing records it

| Artifact | What it actually is | Written by | Signed by | Lives at | Feeds |
|----------|---------------------|------------|-----------|----------|-------|
| ▪ `requirements.md` | The functional requirements: each a "shall", with a priority, a source trace, testable acceptance criteria, the error spec for the top tiers, and the traceability matrix — all in one file | `/sdlc-coach` → `requirements-analyst` | Pod Lead; PO accepts | `.sdlc/artifacts/01-requirements/` | Phase 2 spec synthesis |
| ▪ `non-functional-requirements.md` | The quality targets — speed, capacity, uptime — each with a number, a test method, and a measurement basis naming where the number is read | `/sdlc-coach` → `requirements-analyst` | Pod Lead + QE | `.sdlc/artifacts/01-requirements/` | Phase 2 design drivers (the AQ-NN) |
| ▪ `epics.md` | Epics *and* the user stories under them — "as a / I want / so that" with Given/When/Then acceptance criteria, each linked to a requirement ID | `/sdlc-coach` → `requirements-analyst` | PO | `.sdlc/artifacts/01-requirements/` | Phase 3 spec backlog |
| ▪ `phase2-handoff.md` | Requirements summary, the architectural implications the NFRs raise (the AQ-NN), decisions with rationale, open questions under their original IDs, risks, recommended starting point | `/sdlc-coach` drafts; Pod Lead completes | Pod Lead | `.sdlc/artifacts/01-requirements/` | Phase 2 Step 0, directly |
| ▪ `phase01-visual.html` | The requirements retold as a stakeholder-facing visual — the standard's "narrative companion", rendered | `/visual-explainer` | — | `.sdlc/reports/` | The stakeholder review |
| ▪ `phase01-report.html` | The gate result and artifact inventory, self-contained. This is the document a sponsor actually reads before signing | `generate_phase_report.py` | — | `.sdlc/reports/` | The manual sign-off gate |
| ⚠ error-behavior specs | For every top-tier operation: what it accepts, what it returns, what it does on each failure mode | Plugin Step 1 — but *into* `requirements.md`, not its own file | Pod Lead + QE | folded into requirements.md | Phase 2 contract error semantics |
| ⚠ traceability matrix | Every top-tier requirement traced to a source and forward to an outcome, both directions | Plugin Step 1 — but *into* `requirements.md`, not its own file | QE | folded into requirements.md | The exit gate |
| ⚠ user stories | The stakeholder justification under each requirement — real people, no invented personas | Plugin Step 3 — but *into* `epics.md`, not their own file | PO | folded into epics.md | Phase 3 specs |
| ⚠ the decision list / log | Every unmade product call, numbered, owned, aged on the 2-business-day clock — empty or fully-owned at the gate | **PO answers; nothing writes it** | PO | no path — nothing writes it | The exit gate; Phase 2 open questions |
| ⚠ feasibility spike notes | Each handoff risk verified against the live system, or converted into a requirement change — the spike code deleted, the finding kept | **Orchestrators, on a throwaway branch** | Pod Lead | no path — nothing writes it | Phase 2 design risks |
| ⚠ scope-out record | The explicit not-in-v1 list, shown to the sponsor at the review so no one assumes a cut item into the build | **Pod Lead** | Sponsor has seen it | no path — nothing writes it | Phase 2 scope inputs |
| ⚠ adversarial review record | Fresh reviewers who did not write the draft, attacking it from product, quality, and security angles; the catches recorded | **`multi-reviewer` + QE** | Pod Lead | no path — nothing writes it | The fixes it forces (REQ-022, the clock conflict) |

> ⚠ **The gap — read the amber rows again:** Seven of the thirteen things Phase 1 is supposed to
> produce have no home of their own. Three are *folded* into a bigger file — error specs and
> traceability into `requirements.md`, stories into `epics.md` — so they exist but can't be checked
> or cited on their own. Four leave **no receipt at all**: the decision list the SOW clock bills
> against, the spike that found Harbor's snapshot replica, the scope-out list the sponsor signs off,
> and the adversarial review that caught REQ-022. **Human work is not the problem. Human work
> without a receipt is.**

Deliberately **not** produced in Phase 1: architecture diagrams, technology choices, data models,
API designs, story-level estimates, UI mockups. A requirement that names a technology ("the system
shall use a message queue") is design leaking upstream — rewrite it as the behavior it wanted, and
let Phase 2 choose the how.

## Four questions — and deliberately nothing else

An exhibit from `epics.md` — the four answers, and the epics they produced.

Phase 1's four answers at Harbor became six epics, each traced to an outcome and sequenced by
which moves the metric first. The map was drafted day 1 by the `requirements-analyst` agent into
`epics.md`, corrected by Maya, and sequenced by Luis on day 4.

| ID | Epic | Outcome it serves | Sequence rationale |
|----|------|-------------------|--------------------|
| E-01 | Unified intake queue and assignment | Software | First — everything else lands in it; the auto-proof data model decision lives here |
| E-02 | Channel adapters (portal direct, email parsing, phone form) | Software / Business | Second — kills manual re-keying and the no-SLA inbox (Q-11) |
| E-03 | Coverage verification against PolicyOne | Business (the metric) | Third — removes the built-in batch-window day from every claim |
| E-04 | Fast-path triage for simple claims | Business (the metric) | Fourth — the 61% lever (Q-14); recommend-then-confirm per D-09 |
| E-05 | Acknowledgments and notifications | Business / Regulatory | Fifth — the 15-business-day clock (C-04), written-acknowledgment rule (Q-13) |
| E-06 | Metric instrumentation | All three | Runs alongside from the start — automates the S1 read, adds fast-path sub-metrics |

> ⚠ **The gap — deliberately out of v1:** Auto claims, SMS notifications, fraud scoring,
> payment-disbursement changes, and the adjuster dashboard rebuild — all named explicitly, so
> nobody assumes them into the build.

## The vague-line test: could two people build two different things?

An exhibit from `requirements.md` — day 3's testability pass, and one error spec whole.

On day 3, Nadia Brooks ran the testability pass over all 31 acceptance criteria. Five failed the
vague-line test — lines like "promptly" and "clearly visible" — and went back to Maya for
sharpening the same day, not quietly into the pile. An AI handed "respond promptly" picks a number
for you, and it will not be the one you would have picked.

> **REQ-001, original acceptance criterion (a line that failed):** "The new claim appears in the
> queue promptly and is clearly visible."

> **REQ-001, after the testability pass (the same line, sharpened):** "A claim submitted via portal
> at 14:00 is visible in the queue with status 'new' by 14:05; same for phone-entered and
> parsed-email FNOL."

A representative slice of the 31 functional requirements — 12 of them P0 after the day-4 priority
session:

| ID | Requirement | Pri | Epic | Source | Acceptance criteria (excerpt) |
|----|-------------|-----|------|--------|-------------------------------|
| REQ-001 | Every FNOL, from any channel, appears in the unified queue within 5 minutes of receipt | P0 | E-01 | DOC-003; Dee session 3/17 | A claim submitted via portal at 14:00 is visible with status "new" by 14:05; same for phone-entered and parsed-email FNOL |
| REQ-004 | Duplicate FNOL (same policy + loss date) is flagged and merged, never rejected | P0 | E-01 | Intake clerks session 3/17; D-07 | Second submission attaches to the existing claim with both sources recorded; submitter receives the existing claim number; no second claim number is ever issued |
| REQ-009 | Email FNOL is parsed into a queue entry within 15 minutes of arrival | P0 | E-02 | Q-11; Dee session | An email with attachments arriving 9:00 produces a queue entry with extracted fields and attachments linked by 9:15; parse failures route to a human triage view, never a dead letter |
| REQ-014 | Coverage status for a new claim is available the same business day | P0 | E-03 | CON-01 resolution; Gail/Marcus session | FNOL received before 16:00 shows verified coverage status by 17:00 the same day, with the data's as-of timestamp displayed |
| REQ-019 | Fast-path-eligible claims are auto-identified and routed with a recommended decision | P0 | E-04 | Q-14; D-09 | A single-dwelling, no-injury, sub-$25k claim is tagged fast-path at intake and carries a recommendation the adjuster confirms or overrides with one action; override reasons are recorded |
| REQ-021 | Acknowledgment is dispatched within 3 business days of FNOL, in the form each state requires | P0 | E-05 | C-04; Q-13; compliance session | For the written-acknowledgment state: a letter or compliant email is generated and dispatch-logged; the portal confirmation screen alone never satisfies the requirement |
| REQ-022 | Bounced or failed acknowledgments fall back to postal dispatch and alert the intake team | P0 | E-05 | Day-5 adversarial review | An email bounce within the regulatory window triggers postal generation and a queue alert; the regulatory clock display reflects the remaining margin |
| REQ-027 | The acknowledgment-compliance figure (S1) is computed continuously and readable on demand | P1 | E-06 | Success criteria S1; Priti session | The figure matches the manual quarterly calculation within 0.5 points on the validation sample |

### One requirement in full: REQ-014, error behavior

Every P0 requirement carries an error-behavior structure — the specs the plugin folds into
`requirements.md`. REQ-014's, abridged:

- **Accepts:** a claim with a policy number that exists in the nightly snapshot.
- **Returns:** coverage status (verified / not-covered / needs-review) plus the as-of timestamp of
  the underlying data.
- **On policy not found:** status "needs-review" with reason code; never silently "verified"; claim
  flagged for adjuster attention within the same business day.
- **On replica unavailable:** status falls back to "pending verification"; the queue entry shows the
  degradation; intake is never blocked.
- **On stale data (snapshot older than 36h):** status carries a staleness warning; claims in the
  written-acknowledgment state escalate rather than auto-proceed.

## "Fast" is an opinion — until you say where the number is read

An exhibit from `non-functional-requirements.md` — seven targets, each with a measurement basis.

Writing the quality targets surfaced a gap nobody had named: **storm season**. The Phase 0 sizing
constraint (**C-09**) was annual volume only — it said nothing about peaks. NFR-02 made the surge
design-driving.

> **Priti's 2024 catastrophe-event data (the gap it exposed):** "A catastrophe event spikes intake
> to roughly 10x normal daily volume — about 1,600 claims a day — for a week straight."

> **NFR-02, sized and load-tested for the surge:** "Sized for 40,000 claims/yr steady state and a
> 10x storm surge (≈1,600/day for 7 consecutive days); load-tested at the surge profile before
> go-live."

Confirming the exact surge profile against 2024 catastrophe data became **Q-16**, carried into
design week.

| ID | Requirement | Measurement basis |
|----|-------------|-------------------|
| NFR-01 | Queue ingestion p95 (the time 95% of intakes beat) under 5 seconds per FNOL | Measured at the API gateway; read from the application monitoring dashboard |
| NFR-02 | Sized for 40,000 claims/yr steady state **and a 10x storm surge** (≈1,600/day for 7 consecutive days) | Priti's 2024 catastrophe-event data; load test at surge profile before go-live |
| NFR-03 | 99.5% availability during business hours (7:00–19:00 local, Mon–Sat) | Uptime monitor on the intake endpoints; monthly figure on the ops dashboard |
| NFR-05 | No PII in model context outside the approved tenant path (C-05) | Verified by the security review checklist per change touching claim data |
| NFR-07 | Every queue action is audit-logged with actor and timestamp | Audit log completeness check in the test suite; sampled quarterly by compliance |

## If everything is top priority, nothing is

Day 4 — the priority session · Day 5 — the decisions and the scope-out.

The priority session, Luis driving, 90 minutes. The P0 budget — a hard cap on how many
requirements may sit in the top tier — was set at **12**; the room had **19** candidates. Luis cut
seven. The budget held. None of this — the cap, the cut, the reasons — is written to any plugin
file; it survives only in the priorities column and the scope-out list.

The pod set the budget before the session and announced it when the room opened; Luis ranked
within it. Epics got sequenced by what moves the metric: queue first (everything depends on it),
then coverage verification (kills the batch-window day), then fast-path (the 61% lever), then
acknowledgments, with instrumentation running throughout. Stories were drafted with real
stakeholders — Dee's intake team, Gail's adjusters, the compliance officer by name.

> **The cut:** Seven requirements cut to fit the 12-slot budget — including the **adjuster
> dashboard rebuild**. "We survive with the current screens one more quarter."

**The decision log — nine surfaced, the two that mattered.** All nine decisions surfaced this
phase were answered inside it. The two with teeth:

| ID | Decision | Answer | Who | Days |
|----|----------|--------|-----|------|
| D-07 | Duplicate FNOL (same policy + loss date): reject, queue separately, or merge? | Flag and merge; never reject; submitter gets the existing claim number | Luis | 0 |
| D-09 | Does the fast-path decide, or recommend? | v1 recommends; an adjuster confirms with one click; revisit after a year of override data | Luis | 2 |

Day 5's traceability check claimed one casualty — a candidate SMS-notification requirement that
traced to nothing but RFP boilerplate, confirmed by no human. It was cut and recorded in the
scope-out list Karen saw at the review:

- Auto claims (the data model must not preclude them — C-03 — but nothing ships for them in v1)
- SMS notifications (the RFP boilerplate requirement that traced to nothing — cut on day 5)
- Fraud scoring and ML-based triage (fast-path uses explicit rules, not a model)
- Payment disbursement changes (intake through decision only; payment flows untouched)
- The adjuster dashboard rebuild (cut in the priority session; current screens survive v1)

> ⚠ **The gap — two catches the authors couldn't see:** The day-5 adversarial review — reviewers
> who wrote none of the draft — found a missing failure path (a bounced acknowledgment against a
> written-acknowledgment state rule → REQ-022, bounce-to-postal) and a hidden conflict (a
> "recommend" fast-path could let a claim sit past the regulatory clock → the clock added to the
> fast-path escalation rule). Both were caught here, for the price of an afternoon, instead of in
> the build.

## What Phase 2 receives

A phase ends by handing the next one a package, not a feeling. Everything below crosses the
boundary into Design: the signed requirements, the quality targets, the epics — and, carried in
`phase2-handoff.md`, the questions the requirements *raise* but must not answer, because answering
them is Design's job.

**Crosses into Phase 2:** `phase2-handoff.md` · `requirements.md` ·
`non-functional-requirements.md` · `epics.md` · ⚠ the decision log → open questions Q-15, Q-16 · ⚠
the scope-out record.

### The architectural questions Design must answer

This is the thread that ties the two phases together, and the one place a name in this handoff
reaches directly into the next phase's first command. The requirements raise four questions they
deliberately do not answer — each recorded as an `AQ-NN` in `phase2-handoff.md`, under its "What
Design Must Address" section. Phase 2's **Step 0** reads *exactly these* out of the handoff and
turns each into a signed ADR before it may write anything else.

| AQ | The question the requirements raise | Raised by | Becomes |
|----|-------------------------------------|-----------|---------|
| AQ-01 | Where does a coverage check get its answer, given the once-a-night PolicyOne sync? | REQ-014 (same-day) vs C-02/CON-01 (nightly batch) | ADR-001 |
| AQ-02 | What shape is the claim store, so duplicate-merge and auto-proof are both honored? | REQ-004/D-07, C-03, NFR-07 | ADR-002 |
| AQ-03 | How does intake absorb a 10x storm surge without dropping claims? | NFR-02 | ADR-003 |
| AQ-04 | How is a free-text email FNOL turned into a structured queue entry? | REQ-009 | ADR-004 |

An `AQ` that reaches the end of design week with no ADR is a gate failure. That is how Phase 1's
homework becomes Phase 2's output — and until this page said so, no companion page named the
connection.

### The open questions, carried under their original IDs

| ID | Question | Owner | Due |
|----|----------|-------|-----|
| Q-15 | Will security approve direct read access to the PolicyOne nightly snapshot replica, and under what controls? | Dan Kowalski | Design week, day 2 |
| Q-16 | What exactly does a storm surge look like in the 2024 catastrophe data (peak day, duration, channel mix)? | Priti Shah | Design week, day 2 |

> **Recommended design starting point:** the claim data model and queue — three constraints
> converge on it (auto-proof C-03, duplicate-merge D-07, audit logging) and every epic depends on
> it.

## The tooling behind this phase

The abstract Phase 1 page describes this work generically. What actually ran, on the
**claude-code-sdlc** plugin:

| What got produced | How |
|---|---|
| Epic map, requirement decomposition, validation | The `requirements-analyst` agent over the Phase 0 artifacts and the locked intake catalog (DOC-NNN traceability comes from the catalog) |
| Requirements, NFRs, stories, error specs | Drafted in-session against the `templates/phases/01-requirements/` templates, following `/sdlc` phase guidance; structured error specs per the P0/P1 rule |
| Decision list (D-01..D-09) | Generated continuously in-session; persisted to the open-questions file for audit trail |
| Testability + traceability checks | Nadia's vague-line pass; cross-artifact reference checks inside `/sdlc-gate` |
| Adversarial review (day 5) | `/sdlc-review --adversarial` spawning the `multi-reviewer` agent; report written as a phase artifact |
| Gate check, review packet, advance | `/sdlc-gate`, `/sdlc-phase-report`, `/sdlc-next` (after Luis + Karen sign-off) |
| Mid-week visibility | `/sdlc-status` at the daily pod sync |

---

Next: [the Phase 2 worked example](phase-2-example.md) — Q-15 and Q-16 land, four ADRs
(architecture decision records) get signed, and a spike finds the replica's refresh window.
