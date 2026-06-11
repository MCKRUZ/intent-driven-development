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
| **Q-NN** | An open question with a named owner. |
| **D-NN** | A product decision. |
| **E-NN** | An epic — a large slice of work. |
| **REQ-NN** | A requirement — what the system must do, with acceptance criteria, the checks that prove it. |
| **NFR-NN** | A non-functional requirement — a measurable quality target (speed, capacity, availability). |
| **C-NN** | A constraint from Phase 0. |
| **CON-NN** | A contradiction resolved in Phase 0. |
| **P0** | The top priority tier. |

## 1. How the five days played out

> **Reading the Tooling lines.** **You run it** — a slash command you type (e.g. `/sdlc-gate`,
> `/sdlc-coach`). **It triggers** — an agent or script that command runs under the hood, always
> shown after a `→`. **No plugin command** — a human meeting, client-system work, or an
> exploratory spike; nothing the plugin drives. Drafting and decomposition run through
> `/sdlc-coach`, which fills the phase templates and spawns the `requirements-analyst` agent
> for the heavy decomposition.

**Day 1 (Mon 3/16) — handoff intake and the elicitation plan.**
**Tooling —** `/sdlc-coach` → spawns the `requirements-analyst` agent to draft the candidate
epic map.
- The two open questions from Phase 0 come due, and both answers land by end of day:
  - **Q-13** (Luis): the 15-business-day acknowledgment clock applies to every channel — and
    one of the two regulated states requires a *written* acknowledgment; a portal confirmation
    screen alone does not count. This becomes a requirement, not a footnote.
  - **Q-14** (Priti): the segmentation query says **61%** of property claims are single
    dwelling, no injury, under $25k. The fast-path is a real lever, not a hope.
- The **`requirements-analyst`** agent drafts the candidate epic map from the constitution
  (the short Phase 0 document fixing what must always be true for this engagement),
  constraints, and locked intake catalog (the DOC-NN document index) — six epics, each traced
  to an outcome. Maya corrects
  one boundary (the draft had merged the email channel into the queue epic; Dee's day-5
  interview from Phase 0 says email is its own beast).
- Elicitation sessions — the working interviews that draw requirements out of the people who
  do the work — get scheduled: one per epic area, the right person in each room.
- Jonah starts the feasibility spike (a short, read-only check that answers one question
  against the live systems) the handoff demanded: is the 2023-dated API inventory
  (DOC-007) still true? Sara spikes whether the shared FNOL inbox can be read programmatically.

**Day 2 (Tue 3/17) — elicitation.**
**Tooling —** No plugin command. The elicitation sessions are human conversations; Claude preps
questions and structures notes alongside.
- Five sessions, 60-90 minutes each, Maya facilitating, Claude prepping question lists and
  structuring notes afterward:
  - Queue and assignment — with Dee and two intake clerks (not just Dee: the clerks reveal the
    duplicate-FNOL workaround nobody documented — the same loss reported by phone and portal
    gets two claim numbers today).
  - Coverage verification — with Gail and Marcus: what an adjuster actually needs to know
    before they can decide, and what "yesterday's data" does to a Friday-afternoon claim.
  - Fast-path — with Luis and Marcus: what makes a claim genuinely simple, and what the
    adjuster must still see.
  - Acknowledgments — with compliance: the written-acknowledgment rule from Q-13, bounce and
    returned-mail handling.
  - Instrumentation — with Priti: automating the read of S1 (the secondary success metric
    from Phase 0: the share of claims acknowledged within the regulatory window, today a
    manual quarterly calculation), plus fast-path sub-metrics.
- By evening, Claude has structured the notes into 31 candidate functional requirements, each
  with a stable ID and a source trace.

**Day 3 (Wed 3/18) — the full draft and the decision list.**
**Tooling —** `/sdlc-coach` → the `requirements-analyst` agent produces the requirements and
NFRs; the decision list is written to the open-questions file as it goes.
- The complete draft lands (the `requirements-analyst` agent decomposing, in-session drafting
  against the `templates/phases/01-requirements/` templates): 31 functional requirements and
  7 NFRs, every NFR with a measurement basis (the number, how it's measured, and where it will
  be read). One NFR exposes a gap nobody had named: storm season. Priti's data shows
  catastrophe events spike intake to roughly 10x normal daily volume for a week. The sizing
  constraint from Phase 0 (40k/yr) said nothing about peaks.
- The decision list — the running list of product decisions nobody has answered yet —
  regenerates and persists to the open-questions file (so it survives sessions and audits):
  9 open decisions for Luis. The two that matter most:
  - **D-07:** what happens when a duplicate FNOL arrives for the same policy and loss date?
    Luis, same day: flag and merge into one claim, never silently reject — a rejected
    duplicate is a policyholder who thinks they filed and didn't.
  - **D-09:** does the fast-path *decide* or *recommend*? Luis takes the full two days on
    this one, then rules: v1 recommends; an adjuster confirms with one click. Reason:
    regulatory caution until the model of "simple" is proven against a year of data.
- Nadia runs the testability pass: 5 of 31 acceptance criteria — the testable checks that
  prove a requirement is met — fail the vague-line test ("could two people build different
  things from this line?"): lines like "promptly" and "clearly visible" go back to Maya for
  sharpening the same day.

**Day 4 (Thu 3/19) — priorities and stories.**
**Tooling —** The priority session is the PO's room (no plugin command); separately, `/sdlc-coach`
→ drafts the stories and the P0 error specs.
- The priority session, Luis driving, 90 minutes. The P0 budget — a hard cap on how many
  requirements may sit in the top tier — is set at 12; the room has 19
  candidates. Luis cuts seven — including, painfully, the adjuster dashboard ("we survive
  with the current screens one more quarter"). The budget held.
- Epics get sequenced by what moves the metric: queue first (everything depends on it), then
  coverage verification (kills the built-in batch-window day — the day every claim loses
  waiting for the nightly sync), then fast-path (the 61% lever), then acknowledgments,
  channels hardening, instrumentation running throughout.
- Stories — the user-facing pieces of each epic — drafted with real stakeholders: Dee's intake
  team, Gail's adjusters, the compliance officer by name. No invented personas (made-up
  stand-in users).
- Error behavior specs written for all 12 P0 requirements — what each operation accepts,
  returns, and does on failure (the duplicate-merge rule from D-07 becomes three explicit
  failure-path behaviors).
- The spike results land and one of them changes the requirements:
  - Jonah: DOC-007 is stale in the good direction — PolicyOne now exposes a read-only
    *nightly snapshot replica* (a queryable copy of its data, refreshed each night) that the
    2023 inventory didn't list. Same-business-day
    verification can read the replica directly instead of queuing batch requests. New
    open question for Dan: security approval for replica access (becomes Q-15).
  - Sara: the shared FNOL inbox is readable programmatically through the client's standard
    mail API; parsing is feasible; the twice-daily manual triage can become minutes.

**Day 5 (Fri 3/20) — verification, review, and the gate.**
**Tooling —** `/sdlc-review --adversarial` → `multi-reviewer` agent · `/sdlc-gate` →
`check_gates.py` · `/sdlc-phase-report` → `generate_phase_report.py` · `/sdlc-next` →
`advance_phase.py` (after the human sign-off).
- The traceability check (every requirement must point back to a source and forward to an
  outcome) passes after one casualty: a candidate requirement for SMS notifications traced to
  nothing — no document, no session, no stakeholder. It came from the boilerplate appendix of
  the RFP (request for proposal — the document Harbor issued to hire the pod). Cut, recorded
  in scope-out (the explicit not-in-v1 list).
- **`/sdlc-review --adversarial`** spawns the `multi-reviewer` agent — fresh reviewers that
  didn't write the draft — against the full
  requirements set; its findings plus Nadia's pass produce two real catches:
  - The acknowledgment requirement had no failure path for bounced email against the
    written-acknowledgment rule — REQ-022 (bounce-to-postal fallback) is added.
  - A conflict: fast-path recommendation (D-09) could let a claim sit unconfirmed past the
    regulatory clock — resolved by adding the clock to the fast-path queue's escalation rule.
- **`/sdlc-gate`** passes clean. Claude drafts the Phase 2 handoff: the design risks (batch
  window strategy, replica access, storm-surge sizing), open questions Q-15 and Q-16, and a
  recommended design starting point (the queue's data model, because the auto-proof constraint
  C-03 — the data model must not preclude a future move into auto claims — lives or dies
  there). **`/sdlc-phase-report`** renders the review packet.
- The phase review: Luis confirms the requirements say what he meant; Karen sees the
  scope-out list (auto claims, SMS, fraud scoring, payment changes — all explicitly out).
  Sign-off recorded; **`/sdlc-next`** re-verifies the gates and advances the engagement state
  to Phase 2. **The first biweekly steering is booked for Thursday 3/26.** Billing milestone 2.

## 2. What to notice

- **Q-14 paid for itself.** The 61% figure turned the fast-path from an assumption into the
  engagement's biggest lever, and it was a Phase 0 open question with an owner and a date —
  not a guess someone built on.
- **The P0 budget survived contact.** 19 candidates, 12 slots, and the PO — not the pod — did
  the cutting. The dashboard cut hurt; that's what a real priority decision feels like.
- **D-09 is what the PO clause buys.** "Recommend vs decide" is exactly the kind of decision
  that, unanswered, an agent resolves silently at 2 a.m. in week 7. Here it got a named human,
  a deadline, and a recorded rationale.
- **The spike beat the document.** DOC-007 was wrong in a useful direction; only running the
  check against the live system found the replica. The 2024 vendor never did this.
- **The review earned its slot.** Two findings (bounce handling, the fast-path/regulatory
  conflict) that the authors couldn't see because they shared the draft's blind spots.

---

## 3. Artifact: the epic map

*Drafted day 1 by the `requirements-analyst` agent, corrected by Maya, sequenced by Luis on
day 4.*

| ID | Epic | Outcome it serves | Sequence rationale |
|----|------|-------------------|--------------------|
| E-01 | Unified intake queue and assignment | Software | First — everything else lands in it; the auto-proof data model decision lives here |
| E-02 | Channel adapters (portal direct, email parsing, phone form) | Software / Business | Second — kills manual re-keying and the no-SLA inbox (Q-11) |
| E-03 | Coverage verification against PolicyOne | Business (the metric) | Third — removes the built-in batch-window day from every claim |
| E-04 | Fast-path triage for simple claims | Business (the metric) | Fourth — the 61% lever (Q-14); recommend-then-confirm per D-09 |
| E-05 | Acknowledgments and notifications | Business / Regulatory | Fifth — the 15-business-day clock (C-04), written-acknowledgment rule (Q-13) |
| E-06 | Metric instrumentation | All three | Runs alongside from the start — automates the S1 read, adds fast-path sub-metrics |

## 4. Artifact: requirements (excerpt)

*31 functional requirements drafted day 3; 12 P0 after the day-4 priority session. A
representative slice:*

| ID | Requirement | Pri | Epic | Source | Acceptance criteria (excerpt) |
|----|-------------|-----|------|--------|-------------------------------|
| REQ-001 | Every FNOL, from any channel, appears in the unified queue within 5 minutes of receipt | P0 | E-01 | DOC-003; Dee session 3/17 | A claim submitted via portal at 14:00 is visible in the queue with status "new" by 14:05; same for phone-entered and parsed-email FNOL |
| REQ-004 | Duplicate FNOL (same policy + loss date) is flagged and merged, never rejected | P0 | E-01 | Intake clerks session 3/17; D-07 | Second submission attaches to the existing claim with both sources recorded; submitter receives the existing claim number; no second claim number is ever issued |
| REQ-009 | Email FNOL is parsed into a queue entry within 15 minutes of arrival | P0 | E-02 | Q-11; Dee session | An email with attachments arriving 9:00 produces a queue entry with extracted fields and attachments linked by 9:15; parse failures route to a human triage view, never a dead letter (a failed message that silently goes nowhere) |
| REQ-014 | Coverage status for a new claim is available the same business day | P0 | E-03 | CON-01 resolution; Gail/Marcus session | FNOL received before 16:00 shows verified coverage status by 17:00 the same day, with the data's as-of timestamp displayed |
| REQ-019 | Fast-path-eligible claims are auto-identified and routed with a recommended decision | P0 | E-04 | Q-14; D-09 | A single-dwelling, no-injury, sub-$25k claim is tagged fast-path at intake and carries a recommendation the adjuster confirms or overrides with one action; override reasons are recorded |
| REQ-021 | Acknowledgment is dispatched within 3 business days of FNOL, in the form each state requires | P0 | E-05 | C-04; Q-13; compliance session | For the written-acknowledgment state: a letter or compliant email is generated and dispatch-logged; the portal confirmation screen alone never satisfies the requirement |
| REQ-022 | Bounced or failed acknowledgments fall back to postal dispatch and alert the intake team | P0 | E-05 | Day-5 adversarial review | An email bounce within the regulatory window triggers postal generation and a queue alert; the regulatory clock display reflects the remaining margin |
| REQ-027 | The acknowledgment-compliance figure (S1) is computed continuously and readable on demand | P1 | E-06 | Success criteria S1; Priti session | The figure matches the manual quarterly calculation within 0.5 points on the validation sample |

### One requirement in full: REQ-014, error behavior

*Every P0 requirement carries this structure. REQ-014's, abridged:*

- **Accepts:** a claim with a policy number that exists in the nightly snapshot.
- **Returns:** coverage status (verified / not-covered / needs-review) plus the as-of
  timestamp of the underlying data.
- **On policy not found:** status "needs-review" with reason code; never silently "verified";
  claim flagged for adjuster attention within the same business day.
- **On replica unavailable:** status falls back to "pending verification"; the queue entry
  shows the degradation; intake is never blocked (a claim is always accepted — verification
  degrades, intake does not).
- **On stale data (snapshot older than 36h):** status carries a staleness warning; claims in
  the written-acknowledgment state escalate rather than auto-proceed.

## 5. Artifact: non-functional requirements

*Seven NFRs, each with a measurement basis. The ones that shaped design:*

| ID | Requirement | Measurement basis |
|----|-------------|-------------------|
| NFR-01 | Queue ingestion p95 (the time 95% of intakes beat) under 5 seconds per FNOL | Measured at the API gateway; read from the application monitoring dashboard |
| NFR-02 | Sized for 40,000 claims/yr steady state **and a 10x storm surge** (≈1,600/day for 7 consecutive days) | Priti's 2024 catastrophe-event data; load test at surge profile before go-live |
| NFR-03 | 99.5% availability during business hours (7:00-19:00 local, Mon-Sat) | Uptime monitor on the intake endpoints; monthly figure on the ops dashboard |
| NFR-05 | No PII (personally identifiable information) in model context outside the approved tenant path (C-05) | Verified by the security review checklist per change touching claim data |
| NFR-07 | Every queue action is audit-logged with actor and timestamp | Audit log completeness check in the test suite; sampled quarterly by compliance |

NFR-02 is the one day 3 surfaced: the Phase 0 sizing constraint (C-09) was annual volume only.
Storm surge becomes design-driving, and confirming the exact surge profile against 2024
catastrophe data is **Q-16** (Priti, due in design week).

## 6. Artifact: the decision log (excerpt)

*Nine decisions surfaced; all nine answered inside the phase. The two that mattered:*

| ID | Decision | Answer | Who | Days open |
|----|----------|--------|-----|-----------|
| D-07 | Duplicate FNOL for the same policy + loss date: reject, queue separately, or merge? | Flag and merge; never reject; submitter gets the existing claim number | Luis | 0 (same day) |
| D-09 | Does fast-path decide or recommend? | v1 recommends, adjuster confirms with one click; revisit after a year of override data | Luis | 2 (used the full clock) |

## 7. Artifact: scope-out record

*Shown to Karen at the phase review, in writing:*

- Auto claims (the data model must not preclude them — C-03 — but nothing ships for them in v1)
- SMS notifications (the RFP boilerplate requirement that traced to nothing — cut on day 5)
- Fraud scoring and ML-based triage (fast-path uses explicit rules, not a model)
- Payment disbursement changes (intake through decision only; payment flows untouched)
- The adjuster dashboard rebuild (cut in the priority session; current screens survive v1)

## 8. Artifact: the Phase 2 handoff (summary)

- **Design risks carried forward:** the batch-window strategy now has a candidate answer (the
  snapshot replica) that needs security approval; storm-surge sizing needs the 2024 data; the
  auto-proof constraint (C-03) concentrates in the queue's claim data model — start design
  there.
- **Open questions:**

| ID | Question | Owner | Due |
|----|----------|-------|-----|
| Q-15 | Will security approve direct read access to the PolicyOne nightly snapshot replica, and under what controls? | Dan Kowalski | Design week, day 2 |
| Q-16 | What exactly does a storm surge look like in the 2024 catastrophe data (peak day, duration, channel mix)? | Priti Shah | Design week, day 2 |

- **Recommended design starting point:** the claim data model and queue, because three
  constraints converge on it (auto-proof, duplicate-merge, audit logging) and every epic
  depends on it.

---

## 9. The tooling behind this phase

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
