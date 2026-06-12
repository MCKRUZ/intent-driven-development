# Phase 2: Design

Deep-dive on the third phase of the Delivery Standard. What happens between the requirements
baseline and the foundation build: who decides the shape of the system, how options become
signed decisions, and what has to be true before anyone provisions an environment.

> **What closes Phase 2** (full checklist in §5): every ADR records 2-3 genuinely considered
> options and carries both signatures, every external integration was spiked against the live
> system, contracts carry error and degradation semantics, the threat review is done with each
> threat mitigated or assigned to a build-time gate, and the walking-skeleton definition exists.
> The failure mode to watch (§6): the single-option ADR — documentation of a reflex, not a decision.

**If you're starting here:**

| | |
|---|---|
| **The method** | Claude (the AI coding agent) drafts documents and writes most code. Humans own every decision and verify every result. |
| **The rhythm** | Numbered phases. Each ends with automated checks (the **gate**) plus a named human sign-off. Gates are the billing milestones. |
| **Where we are** | Phase 0 fixed the problem and constraints. Phase 1 produced a signed requirements baseline. Phase 2 decides the architecture. |
| **Our pod (4-6 people)** | Pod Lead · Setup Owner · Orchestrators · Quality Engineer. ([Team deep-dive](team.md)) |

**Words this page leans on** (every other term is explained where it first appears):

| Term | What it means |
|---|---|
| **ADR** | Architecture decision record: one hard-to-undo choice written down — the options considered, the decision, and its consequences — signed by a named human on each side (a signature is the person's name and date recorded in the ADR file itself). |
| **NFR** | Non-functional requirement — a measurable quality target (speed, capacity, availability), with a stated measurement basis. |
| **Spike** | Small throwaway code written to test a risky assumption against reality before the design depends on it; the findings are kept, the code is deleted. |
| **Contract** | Exactly how a piece of the system behaves at its boundary, failures included — what callers may rely on. |
| **Walking skeleton** | The thinnest end-to-end slice of the system, built first to prove the architecture works in practice, not on paper. |
| **A spec** | One feature, described in one file in the repo (`specs/NNNN-name.md`): the goal, what is in and out of scope, testable acceptance checks, and a risk tier. |
| **Risk tier** | HIGH / MEDIUM / LOW, assigned per spec. Sets how tightly an agent is bounded and how much review a change gets. |
| **The constitution** | The short Phase 0 document fixing what must always be true (and what must never happen) for this engagement; later phases may not silently contradict it. |
| **Threat model** | A structured walk of the design's data flows asking "where could this be attacked or leak," producing mitigations and build-time security gates. |

Phase 2 answers four questions, and nothing else:

1. **What is the shape of the system?** (components, boundaries, data flow, deployment view)
2. **What are the contracts?** (API contracts, the data model, integration interfaces — with
   error semantics, meaning how each operation behaves when things fail, not just the happy
   paths)
3. **Which decisions are hard to undo, and what did we choose?** (architecture decision
   records, each with real options and consequences, each signed)
4. **How will the design be proven?** (the verification approach per NFR, and what the
   Phase 3 walking skeleton must demonstrate)

Production code, the full backlog of build specs, environment provisioning, and pixel-level UI
design are out of scope — they belong to Phase 3 and the Build (the continuous per-spec build
loop that follows the gated phases). Design spikes (small,
throwaway code to test a risky assumption) are explicitly *in* scope; they're how design
claims get verified against reality instead of against documents.

---

## 1. Who is involved

Phase 2 is the Setup Owner's phase the way Phase 1 was the product owner's. The decisions made
this week are the expensive-to-undo ones, which is why every one of them gets a record and two
signatures.

### Our side

| Person | Load | Workstream |
|---|---|---|
| **Setup Owner** | 80-100% | Design authority: drives the option evaluation, owns the design document, signs every ADR, owns the integration strategy |
| **Orchestrators** | 50-70% | Design spikes (throwaway code against the riskiest assumptions), drafting API contracts and the data model under the Setup Owner's direction |
| **Pod Lead** | 40-50% | Keeps design traced to requirements, routes product-relevant trade-offs to the PO (the client's product owner), runs the steering, owns the handoff |
| **Quality Engineer** | 30-40% | Designs how the design will be proven: the verification approach per NFR, the test strategy skeleton, what the walking skeleton must demonstrate |

### Client side

| Person | Needed for | How much |
|---|---|---|
| **Lead engineer / architect counterpart** | The option sessions; co-signs every ADR — they own this system after handoff, so they choose with us, not after us | 3-5 hours across the week |
| **Security** | The threat review session; data-flow approval; any open access questions from Phase 1 | 1-2 hours |
| **Product Owner** | Product-facing trade-offs only (behavior under degradation, what users see when things fail) | ~1 hour; the decision-list clock (Phase 1's 2-business-day turnaround on product decisions) still applies |
| **Ops / DBA** | Integration access realities, operational constraints the documents don't show | As the spikes demand |
| **Sponsor** | The steering (the design narrative, not the diagrams) | 45 min |

If the client cannot name an engineering counterpart, that's a finding, not an inconvenience —
it predicts the handoff failing, and it goes to the sponsor at steering.

### Claude's role in Phase 2

This phase has the second-strictest human rule in the standard, after Phase 0's: **Claude
presents options; humans choose.** Concretely:

- **Option research and framing.** For each architecture-level decision, Claude researches and
  presents 2-3 genuine options with concrete trade-offs — costs, risks, what each forecloses —
  grounded in the actual requirements and constraints, not generic textbook comparisons. One
  option presented alone is not a decision; it's a default wearing a decision's costume.
- **ADR drafting, after the human picks.** The record captures the context, the options
  actually considered, the choice, and the consequences — including the unpleasant ones.
- **Contract and model drafting.** API contracts and the data model drafted from the
  requirements, carrying the Phase 1 error-behavior specs into concrete response codes,
  failure modes, and degradation behavior.
- **Consistency checking, both directions.** Every top-tier requirement lands somewhere in the
  design; every major design element traces back to a requirement or constraint. Orphans in
  either direction get flagged ("this service exists but nothing requires it" is how
  accidental scope is born).
- **Threat-model preparation.** Claude drafts the data-flow diagrams and candidate threat list
  the security session works from.

What Claude never does: choose an architecture, sign an ADR, accept a risk, or soften a
trade-off to make an option look better.

---

## 2. Day one to the last day

The default calendar is **5 business days**, stretching to 8-10 when the integration estate is
large (many external systems to connect to) or the client's review boards add latency. The week's spine: options early, decisions in
the middle, contracts and verification at the end. The Setup Owner's enablement work from
Phases 0-1 (pipeline groundwork, environment prep) continues in parallel and is why Phase 3
can start immediately after.

**Day 1 — design drivers and the option set.**
- The pod extracts the design drivers from the Phase 1 handoff: the few requirements and
  constraints that actually shape the architecture (the hard integration boundary, the surge
  sizing, the forward-compatibility rule, the regulatory clock). Most requirements don't
  drive architecture; finding the 5-8 that do is the day's craft.
- The open questions the handoff carried come due — their answers (an access approval, a
  sizing profile) are usually design inputs, which is why they were due now.
- Claude presents the option sets: for each major decision, 2-3 candidate approaches with
  trade-offs against *these* drivers. The Setup Owner reviews, kills the strawmen (the
  options that were never real contenders), and schedules the option session for the
  decisions worth a room. (Decisions not worth a room are settled asynchronously between the
  Setup Owner and the counterpart, and still get an ADR if they're hard to undo.)
- The riskiest assumptions get named, and spikes get assigned: anything the design would bet
  on that has only been verified on paper.

**Day 2 — spikes and the option session.**
- Orchestrators run the design spikes: small, throwaway, time-boxed to hours — does the
  integration respond the way its documentation claims, does the candidate approach survive
  the surge profile, does the access path actually open. Spike code is deleted; spike
  findings are recorded.
- The option session (90-120 min): Setup Owner and the client's lead engineer work through
  the major decisions, Claude's option framings on the table, spike results in hand. The
  humans choose. Product-facing trade-offs split off to the PO with the usual clock. The
  Setup Owner runs it. Per decision: the option framing is walked, the spike evidence
  weighed, the counterpart's questions answered, and the choice recorded with its reasons in
  session notes — those notes are the raw material for the next day's ADR drafts.
- By end of day, the architecture direction is chosen and the ADR list is known.

**Day 3 — decisions become records; the model takes shape.**
- Claude drafts the ADRs from the day-2 choices; the Setup Owner edits and signs; the client
  counterpart co-signs. An unsigned ADR is a conversation, not a decision.
- The data model and component design get drafted — starting where the handoff said to start
  (the element where the most constraints converge).
- The forward-compatibility check the constitution demanded runs against the draft model:
  does this design preclude the futures the client paid to keep open? Verified now, gated
  again at every design review. (The Setup Owner walks each constitution-protected future
  against the draft model and records the verdict — and what made it true — alongside the
  model.)

**Day 4 — contracts, threat review, and the proving plan.**
- API contracts completed: every operation with its request/response shapes, error semantics
  carried down from the Phase 1 error-behavior specs, degradation behavior under each
  dependency failure. A contract that only describes success is half a contract.
- The threat review session with client security: data-flow diagrams on the table, the
  candidate threat list worked through, mitigations assigned — some become design changes,
  some become build-time security gates on specific areas (these feed the risk-tier map the
  Build loop will use — the register listing each area of the codebase with its risk tier
  and any security gate guarding it, which Build triage reads when tiering specs).
- The Quality Engineer completes the proving plan: for each NFR, how it will be verified and
  where its number will be read; and the walking-skeleton definition — the thin end-to-end
  slice Phase 3 must make real to prove the architecture under the rails (the automated
  enforcement Phase 3 installs around every change).

**Day 5 — review, gate, and the handoff.**
- The design review: fresh eyes (a review agent that didn't draft the design, plus the QE and
  Pod Lead) challenge it from four angles — architecture (failure points, scale), product
  (does it serve the requirements), quality (is it testable), security (gaps the threat
  session missed). Findings get fixed or explicitly accepted with a name attached (the Setup
  Owner's, as the design's owner — or the client counterpart's when the accepted risk is
  theirs to carry; the acceptance lives in the review record).
- The consistency check runs both directions (requirements ↔ design); orphans resolved.
- The automated gate check runs; the Phase 3 handoff is drafted: the signed decisions, the
  contracts, the walking-skeleton definition, the build risks, the recommended first specs.
- Steering: the sponsor gets the design *narrative* — what was decided, what it costs, what
  it protects — not the component diagrams. The PO confirms the product-facing trade-offs.
  Sign-offs recorded; the engagement advances to Foundation.

### When the week stretches

- **The client has a formal architecture review board** — schedule it for day 4-5 from day 1;
  if its cadence can't fit the week, the phase stretches and the gate-based billing in the
  SOW (the statement of work) makes the latency visible rather than absorbed.
- **A spike falsifies a favored option** — good; that's the spike doing its job. Re-run the
  option session with the surviving candidates rather than bending the finding.
- **The counterpart keeps missing sessions** — escalate at steering; co-signature is not a
  formality, it's the handoff being built early.

---

## 3. The artifacts

> Worked example: [`phase-2-example.md`](phase-2-example.md) — Harbor Mutual's design week:
> four signed ADRs (one in full), the spike that found the replica's refresh window, the
> contract that carries REQ-014's error spec, the threat review, and the walking-skeleton
> definition.

| Artifact | Drafted by | Owned by | Done means |
|---|---|---|---|
| Design document | Claude (drafts), Setup Owner (shapes) | Setup Owner | The shape of the system: components, boundaries, data flow, deployment view — short enough to be read, current enough to be trusted; navigation for the ADRs, not a novel |
| Architecture decision records | Claude (after the choice) | Setup Owner + client counterpart (both sign) | Each ADR: the context, 2-3 options genuinely considered, the choice, the consequences including unpleasant ones, two signatures |
| Data model | Claude (drafts) | Setup Owner | Serves every top-tier requirement; passes the forward-compatibility check; the convergence constraints (audit, merge rules) are structural, not bolted on |
| API contracts | Claude (drafts), Orchestrators (refine) | Setup Owner | Every operation: shapes, error semantics from the Phase 1 specs, degradation behavior per dependency failure |
| Integration design | Orchestrators (spiked), Setup Owner | Setup Owner | Every external touchpoint verified by a spike against the live system, not the documentation |
| Spike findings | Orchestrators | Setup Owner | Each risky assumption: confirmed or falsified, with evidence; spike code deleted |
| Threat model + mitigation map | Claude (drafts), security session (decides) | Setup Owner + client security | Data flows reviewed; each threat mitigated in design or assigned as a build-time security gate |
| NFR proving plan | QE | QE | Per NFR: the verification method and where the number will be read |
| Walking-skeleton definition | QE + Setup Owner | Setup Owner | The thin end-to-end slice Phase 3 must ship: named, bounded, and sufficient to prove the architecture (the definition states the end-to-end path step by step, the environment it must run in, and the rails that must be live; sufficient means every ADR's chosen mechanism is exercised at least once on the path) |
| Consistency check record | Claude | Pod Lead | Requirements ↔ design traced both directions; orphans resolved or removed |
| Phase 3 handoff | Claude | Pod Lead | Decisions, contracts, skeleton definition, build risks, recommended first specs, open questions under their original IDs |

What is deliberately **not** produced: production code, the spec backlog (Phase 3 and triage
own that), provisioned environments (Phase 3), UI visual design beyond what product trade-offs
required, and estimates beyond the SOW's phase figures.

---

## 4. The cadences

| Rhythm | Who | What |
|---|---|---|
| **Daily 15-minute pod sync** | Whole pod | Spike results, decision status, contract progress |
| **The option session** | Setup Owner + client counterpart (+ Pod Lead) | The anchor event: options chosen by humans, day 2 |
| **The decision-list clock** | PO + Pod Lead | Still running — product-facing design trade-offs go to the PO at 2-business-day turnaround |
| **The threat review** | Setup Owner + client security + QE | Day 4; its outputs become design changes and build-time gates |
| **Biweekly steering** | Sponsor + Pod Lead | Falls mid-or-end of this phase: the design narrative, the trade-offs, what the decisions protect |

---

## 5. The exit gate

Phase 2 closes when all of these are true:

- [ ] The automated gate checks pass: artifacts exist, are complete, contain no placeholders
- [ ] Every ADR records 2-3 genuinely considered options and carries both signatures (Setup
      Owner + client counterpart)
- [ ] Every top-tier requirement maps to a design element, and every major design element
      traces to a requirement or constraint — no orphans in either direction
- [ ] Every external integration the design depends on was spiked against the live system
- [ ] Contracts carry error semantics and degradation behavior, not just success shapes
- [ ] The forward-compatibility rule from the constitution was checked against the data model
- [ ] The threat review happened; every identified threat is mitigated in design or assigned
      as a build-time security gate
- [ ] Every NFR has a proving method and a named place its number will be read
- [ ] The walking-skeleton definition exists and is sufficient to prove the architecture
- [ ] A named human on each side approved the advance — gates report, humans decide

---

## 6. What goes wrong in Phase 2

- **The single-option decision.** Claude (or the architect) presents one approach, everyone
  nods, and an ADR gets written around a default. The 2-3-options rule exists because the
  alternatives are where the thinking happens; an ADR with one option is documentation of a
  reflex.
- **Resume-driven architecture.** The interesting technology wins over the boring one that
  fits. The constitution's principles and the client's operational reality are the tiebreaker
  — they will run this system at 2 a.m., not us.
- **Designing around the constraint instead of with it.** The hard boundary (a batch window,
  a regulated data path) gets wished away with "and then we'll add a real-time feed later."
  Phase 0 resolved what's fixed; the design honors it or the engagement re-opens the
  conversation explicitly — never silently.
- **Faith-based integration.** The design bets on an interface nobody called. The
  spike-before-you-depend rule is cheap insurance; the alternative is discovering the truth
  in Build week 3, which is how the last vendor died.
- **The hundred-page design document.** Nobody loads it, so nobody follows it. The design
  document is navigation — the decisions live in ADRs, the details live in contracts, and
  all three stay short enough to stay true.
- **Happy-path contracts.** Contracts that specify success and leave failure to the
  implementer's imagination. The Phase 1 error-behavior specs exist precisely to flow into
  contract error semantics — if they don't, that work evaporates here.
- **Foreclosing the protected future — or gold-plating for an unfunded one.** The
  forward-compatibility check cuts both ways: don't preclude what the constitution protects,
  and don't build abstractions for futures nobody paid for. "Must not preclude" means the
  door stays open, not that the room gets furnished.
- **The absent counterpart.** ADRs signed by one side are an engagement artifact, not a
  client decision. If the counterpart can't engage now, the handoff is already failing —
  surface it at steering while it costs days, not at close when it costs the harness (the
  AI-agent setup and rules the client inherits).

---

Next: [Phase 3: Foundation](phase-3-foundation.md) — the harness gets installed, the rails go
live, and the walking skeleton becomes running code in the client's own dev environment.
