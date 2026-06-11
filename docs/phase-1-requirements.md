# Phase 1: Requirements

Deep-dive on the second phase of the Delivery Standard. What happens from the day after Phase 0
closes to the day the requirements baseline is signed: who is in the room, what gets made, what
runs on a schedule, and what has to be true before design starts.

**If you're starting here:**

| | |
|---|---|
| **The method** | Claude (the AI coding agent) drafts documents and writes most code. Humans own every decision and verify every result. |
| **The rhythm** | Numbered phases. Each ends with automated checks (the **gate**) plus a named human sign-off. Gates are the billing milestones. |
| **Where we are** | Phase 0 (discovery) established the problem, one measurable success metric, and the constraints. Phase 1 turns those into a requirements baseline. |
| **Our pod (4-6 people)** | Pod Lead · Setup Owner · Orchestrators · Quality Engineer. ([Team deep-dive](team.md)) |

**Words this page leans on** (every other term is explained where it first appears):

| Term | What it means |
|---|---|
| **A requirement** | What the system must do, with acceptance criteria — the checks that prove it. |
| **Acceptance criteria** | The testable checks that prove a requirement is met. Each must pass the vague-line test. |
| **The vague-line test** | "Could two people build different things from this line?" If yes, the line is a wish, not a requirement. |
| **NFR** | Non-functional requirement — a measurable quality target (speed, capacity, availability), always with a stated measurement basis (where the number will be read). |
| **Epic** | A large slice of work. |
| **Story** | A user-facing piece of an epic. |
| **P0** | The top priority tier. |
| **The PO** | The product owner — the client person who owns product decisions, on a 2-business-day answer clock. |
| **Proxy mode** | When the client can't field a product owner, our Pod Lead owns product calls and the client ratifies them on a clock; every proxy decision is logged. |
| **The decision list** | The running list of product decisions nobody has made yet ("you haven't decided X"), each needing a named human answer. |
| **Elicitation** | The structured working sessions where requirements are drawn out of the people who actually do the work. |
| **A feasibility spike** | A short, read-only investigation that answers one question about the client's systems (is this API still real?) before a requirement depends on it. |
| **Traceability** | Every requirement points backward to its source (a document or a named session) and forward to the outcome it serves. |

Phase 1 answers four questions, and nothing else:

1. **What must the system do?** (functional requirements with testable acceptance criteria)
2. **How well must it do it?** (non-functional requirements, each with a measurement basis)
3. **In what order does value ship?** (epics, sequenced against the outcome, priorities set by
   the product owner)
4. **What is explicitly out?** (scope boundaries written down before pressure arrives)

Everything that looks like architecture, technology selection, data modeling, or estimation is
deliberately out of scope — that work belongs to Phase 2 and beyond. A requirement says *what*
and *how well*, never *how*.

---

## 1. Who is involved

Phase 0 was two people and a corpus — the collected client documents. Phase 1 is where the pod
fills in and the product owner becomes the busiest person on the client side.

### Our side

| Person | Load | Workstream |
|---|---|---|
| **Pod Lead** | 80-100% | Runs the phase: elicitation sessions, requirement quality, the decision list, priority session facilitation, the handoff |
| **Orchestrators** | 30-50% | Arrive for real: structure elicitation notes into draft requirements, run read-only feasibility spikes against risks the handoff carried (a dated API inventory, an unverified integration), sanity-check that requirements are buildable |
| **Quality Engineer** | 30-40% | The testability conscience: every acceptance criterion through the vague-line test, every non-functional requirement checked for a real measurement basis, the traceability structure |
| **Setup Owner** | 30-50% | Enablement runs ahead: pipeline groundwork (early setup of the automated build-and-deploy machinery) and environment prep for Phase 3, plus answering feasibility questions the requirements raise |

### Client side

| Person | Needed for | How much |
|---|---|---|
| **Product Owner** | The whole phase: elicitation, the decision list (2-business-day clock), the priority session, sign-off | Their committed hours, fully spent — this is the phase the PO clause (the contract line that commits the product owner's hours and answer clock) was written for |
| **Domain experts** | Elicitation sessions, one per epic area | 60-90 min each |
| **Data owner** | The instrumentation epic (any metric that day 6 of Phase 0 showed can't be read yet) | One session |
| **Compliance / security** | Regulatory requirements become explicit, testable entries | One session if regulated |
| **Sponsor** | One checkpoint (a 30-minute mid-week read of the draft epic map and emerging scope-out, typically day 3) plus the phase review; the biweekly steering cadence (the recurring sponsor check-in) starts at the end of this phase | ~1.5 hours total |

**Proxy mode** (no client PO): the Pod Lead owns stories and priorities, every product decision
goes in the decision log, and the sponsor ratifies the log at the phase review. The phase runs
the same calendar; the decision-list clock binds the Pod Lead instead.

### Claude's role in Phase 1

Phase 1 is the drafting-heaviest phase of the engagement, and the rule from Phase 0 still
binds: **Claude drafts and interrogates; humans decide and own.** Concretely:

- **Decomposition drafting.** From the Phase 0 artifacts and the document corpus, Claude
  drafts the candidate epic map and candidate requirements — every one carrying a source
  trace (a document reference like DOC-003, or "elicitation session, day 2").
- **The decision list, continuously.** Every draft regenerates the list of decisions no human
  has made yet ("you haven't decided what happens when a duplicate arrives"). The list is the
  PO's work queue, on a visible 2-business-day clock.
- **Conflict and gap checks.** Claude cross-checks every requirement against the constitution
  (the short Phase 0 document fixing what must always be true — and never happen — for this
  engagement) and the constraints from Phase 0 ("REQ-014 implies storing claimant documents;
  constraint C-05 says PII — personally identifiable information — stays in the client tenant —
  reconcile") and flags requirements that trace to nothing.
- **Drafting the structure that makes review cheap.** Stable requirement IDs, acceptance
  criteria in checkable form, error behavior spelled out for the highest-priority items (what
  it accepts, what it returns, what it does on failure).

What Claude never does in Phase 1: set a priority, accept a criterion, or make a scope call.
Those are the product owner's, and in proxy mode they're logged, not just made.

---

## 2. Day one to the last day

The default calendar is **5 business days** — one week, assuming Phase 0 did its job (a signed
problem statement, a verified metric, resolved contradictions, a working PO arrangement). It
stretches to 8-10 days when the epic count is large, the domain is heavily regulated, or proxy
mode adds ratification latency. The week is front-loaded with conversation and back-loaded
with verification. Every "Claude drafts" and "the check runs" below has a concrete command
behind it — the worked example's closing section, "The tooling behind this phase," maps each
step to the command and agent that runs it.

**Day 1 — handoff intake and the elicitation plan.**
- The pod works the open questions Phase 0 carried forward: each has an owner and a due date
  of "this week" — the answers feed directly into requirements (an unsegmented claim
  population, an unverified regulatory nuance).
- Claude drafts the candidate epic map from the Phase 0 artifacts: 4-8 epics, each traced to
  one of the three outcomes, each with a one-paragraph intent. The Pod Lead corrects it and
  uses it to plan elicitation — one session per epic area, the right domain expert in each.
- If Phase 0 found the success metric couldn't be read end-to-end, the **instrumentation
  epic** goes on the map now, first, not as an afterthought.
- Orchestrators start the feasibility spikes the handoff flagged (read-only: verify the API
  inventory is current, confirm the integration surface actually exists as documented).

**Day 2 — elicitation.**
- Working sessions with domain experts and the PO, one per epic area, 60-90 minutes each, run
  by the Pod Lead. Humans in the room; Claude preps each session's question list from the
  corpus and the epic intent, and structures the notes afterward.
- The people interviewed are the ones who live the work — the same rule as Phase 0's
  interviews. The intake clerk knows the duplicate-claim workaround; the manager knows the
  org chart.
- By end of day, Claude has structured the notes into draft functional requirements with
  stable IDs, each traced to its session or document.

**Day 3 — the full draft and the decision list.**
- Claude produces the complete draft: functional requirements with acceptance criteria, plus
  non-functional requirements — and every NFR carries a **measurement basis**: the number, how
  it will be measured, and where ("p95 API response under 800ms, measured at the gateway, read
  from the monitoring dashboard" — p95 meaning 95% of requests come in at or under the number).
  An NFR without a measurement basis is an opinion. The numbers themselves come from humans —
  elicitation, the constraints, the client's own data; a target nobody on the client side
  stated goes on the decision list, not into the draft.
- The decision list regenerates against the full draft. The PO starts working it — the
  2-business-day clock is now the phase's critical path (the item everything else waits on),
  and the Pod Lead tracks it visibly.
- The Quality Engineer runs the testability pass: every acceptance criterion through the
  vague-line test (could two people build different things from this line?). Criteria that
  fail go back to the Pod Lead, not quietly into the pile.
- The sponsor checkpoint (30 minutes): the draft epic map and the emerging scope-out get a
  mid-week read, so nothing at the day-5 review is a surprise.

**Day 4 — priorities and stories.**
- The priority session, 90 minutes, PO driving: every requirement gets a priority the **PO
  assigns** — the pod advises on cost and risk, the PO owns the order. The hard rule: the
  top-priority tier has a budget. If everything is P0, nothing is. The Pod Lead sets the
  budget before the session — sized to what the pod can credibly deliver in the first stretch
  of Build — and announces it when the session opens; the PO ranks within it.
- Epics get sequenced against the outcome: which epic moves the success metric first.
- User stories are drafted under each epic, each carrying its stakeholder justification
  ("Dee's intake team needs X because Y") — no fabricated personas (made-up stand-in users);
  if nobody named the stakeholder, the story doesn't get one invented. A story carries three
  things: the epic it belongs to, the named stakeholder and why ("Dee's intake team needs X
  because Y"), and the requirements it bundles — nothing else; estimates and design stay out.
- For the top two priority tiers, error behavior is spelled out explicitly: what each
  operation accepts, what it returns, and what happens on each failure mode. This is where
  most confident-wrong builds get prevented.
- Feasibility spike results land: anything the spikes contradicted gets reconciled now
  (the integration that doesn't exist as documented becomes a requirement change or a risk).

**Day 5 — verification, review, and the gate.**
- The traceability check: every top-priority requirement traces backward to a source (a
  document, a named session) and forward to an outcome. Requirements that trace to nothing
  get challenged — they're usually someone's pet feature wearing a requirement costume.
- A structured adversarial review: fresh eyes (a review agent that didn't write the draft,
  plus the QE, the Quality Engineer) challenge the set from product, quality, and security
  angles — conflicting
  requirements, missing error paths, unstated assumptions, regulatory gaps.
- The automated gate check runs; placeholders and missing sections get fixed today.
- Claude drafts the Phase 2 handoff: summary, decisions made with rationale, the open
  questions (same numbered IDs, with owners), risks for design, and a recommended design
  starting point.
- The phase review: PO confirms the requirements say what they meant; the sponsor sees the
  scope-out list with their own eyes (this is the page that prevents the month-four "I
  assumed that was included" conversation). Sign-off recorded; the engagement advances. The
  **first biweekly steering** is scheduled — the cadence starts now and runs through the
  whole Build (the implementation stretch of the engagement).

### When the week stretches

- **The PO can't keep the 2-day clock** — escalate to the sponsor by name; the clock is in
  the SOW (the statement of work — the signed engagement contract). Don't silently absorb the
  latency by having the pod guess.
- **Elicitation keeps finding new epics** — the map grows past 8, which usually means the
  outcome is too broad; take it to the sponsor as a scope conversation, not a longer phase.
- **Proxy mode** — add 2-3 days for decision-log ratification; batch the log for one sponsor
  session rather than dripping it.

---

## 3. The artifacts

Everything Phase 1 produces, who owns it, and what "done" means. All of it lands in the
requirements artifacts folder of the delivery repo, committed, by the gate run.

> Worked example: [`phase-1-example.md`](phase-1-example.md) — Harbor Mutual's requirements
> week: the epic map, filled requirements with error behavior, the NFRs with measurement
> bases, the decision log, and the priority session where the P0 budget held.

| Artifact | Drafted by | Owned by | Done means |
|---|---|---|---|
| Functional requirements | Claude from elicitation + corpus | Pod Lead (content), PO (acceptance) | Every requirement: stable ID, testable acceptance criteria that pass the vague-line test, a PO-assigned priority, a source trace, an outcome trace |
| Non-functional requirements | Claude | Pod Lead + QE | Every NFR has a number, a measurement method, and a named place it will be read from — no "the system shall be fast" |
| Epic map | Claude (candidates) | PO | 4-8 epics, each traced to an outcome, sequenced by which moves the metric first; instrumentation epic included if the metric needs it |
| User stories | Claude (drafts) | PO | Stories under epics with real stakeholder justifications — no invented personas |
| Error behavior specs (top tiers) | Claude (drafts) | Pod Lead + QE | For every top-priority operation: what it accepts, what it returns, what it does on each failure |
| Decision list / decision log | Claude (generated) | PO (answers) or Pod Lead (proxy, ratified) | Empty, or every survivor is a numbered open question with an owner |
| Traceability matrix | Claude | QE | Requirement → source and requirement → outcome both populated for the top tiers |
| Feasibility spike notes | Orchestrators | Pod Lead | Each handoff risk verified or converted into a requirement change / design risk |
| Phase 2 handoff | Claude | Pod Lead | Summary, decisions with rationale, numbered open questions with owners, design risks, recommended starting point |
| Scope-out record | Pod Lead | Sponsor (has seen it) | The explicit not-in-v1 list, shown at the phase review |
| Narrative companion (optional) | Claude | Pod Lead (edits) | The requirements retold for stakeholders, human-edited before any client sees it |

What is deliberately **not** produced in Phase 1: architecture diagrams, technology choices,
data models, API designs, story-level estimates, and UI mockups. A requirement that names a
technology ("the system shall use a message queue") is design leaking upstream — rewrite it as
the behavior it wanted ("intake must accept submissions during downstream outages").

---

## 4. The cadences

| Rhythm | Who | What |
|---|---|---|
| **Daily 15-minute pod sync** | Whole pod | Elicitation findings, decision-list status, spike results. Still coordination, not ceremony. |
| **The decision-list clock** | PO + Pod Lead | Every open decision visible with its age; 2-business-day turnaround per the SOW; breaches escalate to the sponsor by name |
| **PO working sessions** | PO + Pod Lead | 2-3 across the week: elicitation (day 2), the priority session (day 4), sign-off (day 5) |
| **The anchor events** | Per the calendar | Elicitation day (2), priority session (4), gate and review (5). They move for people, never for polish. |
| **Biweekly steering begins** | Sponsor + Pod Lead | First one at the end of this phase; from here through Build it runs every two weeks with a live demo once there's software to show |

---

## 5. The exit gate

Phase 1 closes when all of these are true, verified at the phase review:

- [ ] The automated gate checks pass: artifacts exist, are complete, contain no placeholders
- [ ] Every top-priority requirement has testable acceptance criteria, a source trace, and an
      outcome trace
- [ ] Every non-functional requirement has a measurement basis (number, method, named source)
- [ ] Every top-tier operation has its error behavior spelled out
- [ ] Priorities were assigned by the product owner (or logged and ratified in proxy mode) —
      and the top tier respected its budget
- [ ] The decision list is empty, or every survivor is a numbered open question with an owner
      and a due date
- [ ] The scope-out record exists and the sponsor has seen it
- [ ] The Phase 2 handoff carries the open questions under their original IDs
- [ ] A named human (PO + sponsor side) approved the advance — gates report, humans decide

---

## 6. What goes wrong in Phase 1

- **Everything is P0.** Priority inflation is the default state of nature. The defense is a
  budget for the top tier, enforced in the priority session — the PO ranks within it, and the
  pod refuses to start a phase where the budget is blown.
- **Design wearing a requirements costume.** "Shall use a queue," "shall be built on
  microservices." Each one forecloses Phase 2 before it starts. Rewrite as the behavior that
  motivated it.
- **The corpus treated as requirements.** The RFP (request for proposal — the document the
  client issued to hire us) is evidence, not a requirements baseline.
  Requirements that only trace to the RFP and were never confirmed by a human in elicitation
  are candidates, not commitments — Phase 0's contradictions proved the corpus disagrees with
  itself.
- **The untestable criterion.** "Intuitive," "robust," "fast." The vague-line test exists for
  exactly this, and the QE's testability pass is the enforcement point, not the build loop
  (the per-feature implementation cycle later in the engagement) three weeks later.
- **NFR theater.** Non-functional requirements with no measurement basis are wishes. If
  nobody can say where the number will be read, the NFR isn't done.
- **Silent proxy drift.** In proxy mode, the pod starts making product calls without logging
  them — each one is a liability that surfaces at the worst time. The decision log is cheap;
  the month-six dispute is not.
- **Elicitation that only hears managers.** The people who live the process know where the
  bodies are buried (the shared inbox, the duplicate workaround). If every session attendee
  has "manager" in their title, the requirements describe the org chart's beliefs, not the
  work.
- **The decision-list stall.** The PO's clock slips, the pod fills the silence with guesses,
  and Phase 1 quietly becomes proxy mode without the rider (the contract clause that
  authorizes it). Escalate the clock breach instead — it's in the SOW precisely so this
  moment has teeth.

---

Next: [Phase 2: Design](phase-2-design.md) — how the requirements baseline becomes signed
architecture decisions, contracts, and the walking-skeleton definition (the thinnest
end-to-end slice of the system, built first to prove the architecture).
