# Phase 2 Worked Example: Harbor Mutual

The continuation of [the Phase 1 example](phase-1-example.md), companion to
[the Phase 2 deep-dive](phase-2-design.md). Phase 1 closed Friday 2026-03-20 with a signed
requirements baseline, two open questions (Q-15, Q-16), and a recommendation: start design at
the claim data model, where three constraints converge.

One person joins the story: **Wes Carter**, Harbor's lead engineer — the design counterpart
who co-signs every ADR and, at close, becomes Harbor's Setup Owner. His hours this week are
the handoff being built early.

**The story so far (you can start here):**

| | |
|---|---|
| **The client** | Harbor Mutual — a fictional regional insurer. They hired a five-person consulting pod to rebuild how property-insurance claims get reported and decided. |
| **The problem** | A claim takes a median of **11.4 days** from FNOL (first notice of loss — the policyholder reporting the damage) to a coverage decision. |
| **The target** | Median **5 days or less**. |
| **Where we are** | Phase 1 closed last Friday with a signed requirements baseline. This week decides the architecture. |
| **Design driver 1** | Harbor's policy data lives in **PolicyOne**, an aging core system that syncs data only once per night — but Phase 1 discovered a **snapshot replica**: a read-only copy of PolicyOne's policy data, refreshed nightly, queryable in milliseconds. Whether security allows reading it was open question **Q-15**. |
| **Design driver 2** | **Storm season:** catastrophe events spike claim volume to roughly 10x normal for about a week (NFR-02). The exact surge profile was open question **Q-16**. |
| **Design driver 3** | **61% of claims are simple** (single dwelling, no injury, under $25k) and get a "fast-path": the system recommends a decision, a human adjuster confirms with one click (decision D-09). |
| **Design driver 4** | The data design **must not preclude Harbor's auto-insurance business** later (constraint C-03, "auto-proof") — v1 ships property claims only. |
| **Our pod** | Maya Chen (Pod Lead) · Rob Feld (Setup Owner — the design authority) · Jonah Kim, Sara Whitfield (Orchestrator/Checkers) · Nadia Brooks (Quality Engineer). |
| **Harbor's cast** | Karen Voss (VP Claims Operations — sponsor) · Luis Ortega (product owner) · Wes Carter (lead engineer) · Dan Kowalski (IT security) · Priti Shah (data and reporting lead). |

**The IDs you'll see on this page:**

| ID | What it means |
|---|---|
| **ADR-NN** | Architecture decision record — one hard-to-undo choice written down: the options considered, the decision, and its consequences. Signed by a named human on each side. |
| **Q-NN** | Open question with a named owner. |
| **D-NN** | Product decision. |
| **REQ-NN** | Requirement from the Phase 1 baseline. |
| **NFR-NN** | Non-functional requirement — a measurable quality target (speed, capacity, availability). |
| **C-NN** | Constraint from Phase 0. |
| **CON-NN** | Contradiction resolved in Phase 0. |

## 1. How the five days played out

> **Reading the Tooling lines.** **You run it** — a slash command you type (e.g. `/sdlc-gate`,
> `/sdlc-coach`). **It triggers** — an agent or script that command runs under the hood, always
> shown after a `→`. **No plugin command** — a human meeting, client-system work, or an
> exploratory spike; nothing the plugin drives. Drafting phase artifacts runs through
> `/sdlc-coach` (which fills the phase templates, e.g. the ADR template); option research uses
> the `/deep-plan` skill; spikes are exploratory Claude coding with no plugin command.

**Day 1 (Mon 3/23) — design drivers and the option sets.**
**Tooling —** `/deep-plan` → structures the option research for the design drivers.
- The pod extracts the design drivers from the handoff — the short list that actually shapes
  architecture: the nightly batch window (C-02), the storm surge (NFR-02), auto-proof (C-03),
  the regulatory clock (C-04: two states require claim acknowledgment within 15 business
  days), PII (personally identifiable information) stays in Harbor's cloud tenant (C-05),
  and the duplicate-merge rule (D-07: the same
  loss reported twice becomes one claim, never a rejection).
- Both open questions land on schedule:
  - **Q-15** (Dan): replica read access approved — dedicated read-only service account,
    private endpoint, no PII columns in scope, every access audited.
  - **Q-16** (Priti): the 2024 catastrophe data says the surge is real — peak 1,710 claims on
    day 2 of the event, nine elevated days, channel mix shifting hard toward portal and phone.
- Claude presents the option sets in-session (the plugin pairs this phase with the deep-plan
  skill for structuring the design work): three candidate approaches each for the four
  decisions worth a room — verification source, claim store, surge handling, email parsing.
  Rob kills one strawman per set and books the option session.
- Spikes assigned (a spike is small throwaway code that tests a risky assumption against
  reality before the design depends on it): Jonah takes the replica (does it answer fast,
  and when is it unavailable?);
  Sara takes email extraction (can the parser hit useful accuracy on real redacted samples?).

**Day 2 (Tue 3/24) — spikes and the option session.**
**Tooling —** No plugin command. The spikes are throwaway Claude coding on scratch branches;
the option session is humans choosing.
- The spikes run as Orchestrator-driven Claude sessions on throwaway branches, hours-boxed:
  - **Jonah** tests the snapshot replica — the nightly-refreshed, read-only copy of
    PolicyOne's policy data that coverage checks would query. It answers in 180 milliseconds
    at the 95th percentile (95 of every 100 queries come back at least that fast),
    comfortably inside the same-business-day promise. The catch
    nobody's documentation mentioned: the replica is **unavailable during its 02:00-04:30
    refresh window** each night. That finding flows straight into the coverage-check
    requirement's degradation behavior (REQ-014: when the replica is unreachable, show
    "pending verification" and never block intake) instead of surfacing as a 2 a.m. incident
    in month four.
  - **Sara:** the mail API sustains the volume, and LLM (large language model) field
    extraction on 50 redacted
    sample emails hits **88% accuracy** — promising, below target, exactly the data the
    threshold design needs.
- The option session, two hours, Rob and Wes working through Claude's framings with spike
  results on the table. Four decisions come out chosen; four ADRs go on the list. One
  product-facing trade-off (what the portal shows users during surge degradation) splits off
  to Luis with the usual 2-day clock.

**Day 3 (Wed 3/25) — decisions become records; the model takes shape.**
**Tooling —** `/sdlc-coach` → drafts the four ADRs and the data model (fills the ADR template).
- Claude drafts the four ADRs from the option-session choices against the ADR template; Rob
  edits; **Rob and Wes both sign**. An unsigned ADR is a conversation, not a decision.
- The claim data model gets drafted — starting exactly where the handoff said: claim, event
  log, channel sources, the merge rules from D-07 structural rather than bolted on.
- The auto-proof check (C-03) runs against the draft and forces one change: claim type moves
  from a code-level enum to a reference table with an extensible coverage schema — the auto
  book becomes a data change, not a schema migration.

**Day 4 (Thu 3/26) — contracts, threat review, and the first steering.**
**Tooling —** `/sdlc-coach` → drafts the API contracts · `/visual-explainer` → renders the
steering narrative · the threat review is a human session with client security (no plugin command).
- API contracts complete. The Phase 1 error-behavior specs flow down: REQ-014's
  accepts/returns/fails-how becomes the verification endpoint's response codes, staleness
  header, and refresh-window degradation behavior. A contract that only describes success is
  half a contract.
- The threat review with Dan (Claude drafted the data-flow diagrams and candidate threat list;
  the humans decide): nine threats identified, seven mitigated in the design, two assigned as
  **build-time security gates** — malware scanning on the document upload path, and a
  template-review gate on acknowledgment letters (PII leaves the system on paper).
- Nadia completes the proving plan (every NFR with its verification method and reading place)
  and the **walking-skeleton definition** — the thinnest end-to-end slice of the system,
  built first to prove the architecture works in practice, not on paper. Here, that means:
  one portal FNOL → queue entry → replica coverage
  check → acknowledgment dispatched in test mode → metric event recorded, running in Harbor's
  dev environment through the real pipeline. That's what Phase 3 must make true.
- The first biweekly steering, afternoon: Karen gets the design narrative (what was decided,
  what it costs, what it protects) — rendered with the visual-explainer skill, not raw
  component diagrams. One decision surfaces in the room: document retention. It becomes
  **D-12**; Luis answers next morning (seven years, per the stricter state's regulation), and
  it lands in the data model as a retention attribute, not a TODO.

**Day 5 (Fri 3/27) — review, gate, and the handoff.**
**Tooling —** `/sdlc-review --all` → `multi-reviewer` agent · `/sdlc-gate` → `check_gates.py` ·
`/sdlc-phase-report` → `generate_phase_report.py` · `/sdlc-next` → `advance_phase.py` (after the
human sign-off).
- **`/sdlc-review --all`** runs the `multi-reviewer` agent in all three modes (council,
  adversarial, edge-cases) (council debates the design from several reviewer perspectives;
  adversarial tries to break it; edge-cases hunts boundary conditions). Three findings
  survive Rob's triage (agent findings that misread the design get dropped; the rest get
  fixed or accepted by name):
  - **HIGH:** no back-pressure behavior (what the portal does when claims arrive faster than
    the queue can absorb them) defined for surge — the contract gains an explicit
    degraded-acceptance mode (accept, queue deeper, never reject a FNOL).
  - **MEDIUM:** the replica staleness flag wasn't wired into the fast-path escalation rule —
    fixed in the design, traced to REQ-019.
  - **MEDIUM:** an orphan — a notification-preferences service that no requirement asked
    for had crept into the component diagram. Cut. Accidental scope dies in design, not build.
- The consistency check runs both directions: every P0 (top-priority) requirement lands in a
  design element;
  every remaining element traces back. Clean after the orphan cut.
- **`/sdlc-gate`** passes; **`/sdlc-phase-report`** renders the review packet. Claude drafts
  the Phase 3 handoff: the four signed ADRs, the contracts, the walking-skeleton definition,
  the two build-time security gates, and the recommended first specs (the skeleton's slices,
  in order — a spec is one feature described in one repo file, what an agent builds from).
- The phase review: Rob and Wes walk the ADRs, Luis confirms the product trade-offs, Karen
  approves on the strength of Thursday's steering. **`/sdlc-next`** re-verifies the gates and
  advances the engagement to Phase 3: Foundation. Billing milestone 3.

## 2. What to notice

- **The spike found the refresh window.** The replica's 02:00-04:30 outage appears in no
  document; one hour of throwaway code found it, and the degradation contract is designed
  around reality instead of discovered against it.
- **ADR-002 records the rejection, not just the choice.** Full event sourcing (storing every
  change as an event and rebuilding all state from that history) was considered and rejected
  as unfunded gold-plating — in writing, with reasons. Nobody relitigates it in
  month three, and nobody wonders whether it was considered.
- **Wes's signature is the transfer event in miniature.** Every ADR carries Harbor's own
  engineer's name next to Rob's. At close, the harness (the AI-agent setup and rules Harbor
  inherits) hands to someone who chose this architecture, not someone it happened to.
- **The AI-engineering module activates on ADR-004.** The email parser is an LLM-powered
  component, so it gets the agentic discipline: a 200-email golden set (a fixed,
  human-verified test set) as acceptance criteria, an eval gate in CI (continuous
  integration — the automated checks every change runs through), and prompt/model changes
  tiered HIGH (the strictest risk tier, drawing the most review). The 88% spike baseline is
  the starting line the eval suite measures improvement from.
- **The review cut a service.** The orphaned notification-preferences component is exactly how
  accidental scope is born; the both-directions consistency check is what killed it for free.

---

## 3. Artifact: the ADR registry

*Four decisions, all signed Rob Feld + Wes Carter, 2026-03-25.*

| ID | Decision | Chosen | Rejected (and why) |
|----|----------|--------|--------------------|
| ADR-001 | Coverage verification source | Read the PolicyOne nightly snapshot replica directly (per Q-15 controls) | Batch request queue (adds a day back — defeats the metric); building a real-time PolicyOne API (cost and risk unfunded for v1; deferred to the auto phase) |
| ADR-002 | Claim store shape | Relational model + append-only event log; auto-proof via line-of-business reference table and extensible coverage schema | Full event sourcing (unfunded gold-plating; team operability cost); document store (weak fit for the merge and audit rules) |
| ADR-003 | Surge handling | Buffered ingestion queue + autoscaling, load-tested at the Q-16 surge profile | Permanent overprovisioning (pays for the storm all year); serverless rearchitecture (foreign to Harbor's operating model — they run this at 2 a.m.) |
| ADR-004 | Email FNOL extraction | LLM extraction with per-field confidence thresholds; below-threshold fields route to the human triage view (REQ-009) | Deterministic template parser (insurer emails are too varied — Sara's spike); permanent manual triage (the no-SLA inbox is the problem being solved) |

## 4. Artifact: ADR-001 in full

**ADR-001: Coverage verification reads the nightly snapshot replica**
Status: accepted · Signed: Rob Feld (pod), Wes Carter (Harbor) · 2026-03-25

**Context.** REQ-014 promises same-business-day coverage status. PolicyOne syncs downstream
nightly (C-02, CON-01); the 2023 API inventory listed only batch interfaces, but the Phase 1
spike (Jonah, 3/19) found a read-only nightly snapshot replica, and security approved direct
read access under controls (Q-15).

**Options considered.**
1. **Read the snapshot replica directly.** Fresh-as-of-yesterday data in milliseconds.
   Requires the Q-15 controls and a staleness contract.
2. **Queue batch requests through the existing PolicyOne interface.** No new access path, but
   answers arrive next business day — re-adds the day the metric exists to remove.
3. **Build a real-time read API on PolicyOne.** True real-time, but mainframe-side work
   Harbor can't staff this year; CON-01 already deferred real-time to the auto phase.

**Decision.** Option 1. The replica read, behind a verification service that owns the
staleness contract.

**Consequences.**
- Every coverage answer carries an as-of timestamp; data older than 36 hours triggers the
  escalation path (REQ-014's error spec).
- The replica is unavailable 02:00-04:30 during refresh (Jonah's spike, 3/24): the service
  degrades to "pending verification" and intake is never blocked.
- Access runs under the Q-15 controls: read-only service account, private endpoint, audited.
- The unpleasant one: v1's accuracy ceiling is "as of last night." If Harbor later funds
  real-time, this service is the seam where it lands — the contract doesn't change, the
  source behind it does.

## 5. Artifact: the data model (summary)

*Drafted day 3; one structural change from the auto-proof check.*

- **Claim** — the aggregate (the root record every other piece attaches to); carries
  line-of-business as a **reference table** (the auto-proof
  change: adding the auto book is a data change, not a schema migration), an extensible
  coverage-schema attribute, and a 7-year retention attribute (D-12).
- **Claim event log** — append-only (entries are only ever added, never changed); every
  state change with actor and timestamp. NFR-07's
  audit requirement is structural, not bolted on; the duplicate-merge (D-07) is an event pair
  (merge-in / merged-from), so history survives the merge.
- **FNOL source** — one claim, many sources (the duplicate rule); each source keeps its
  channel, raw payload reference, and received-at.
- **Acknowledgment record** — dispatch attempts, form (email/postal), bounce chain (REQ-022),
  and the regulatory-clock fields the escalation rules read.

## 6. Artifact: contract excerpt — the verification endpoint

*REQ-014's error spec, now as contract behavior:*

| Condition | Response |
|-----------|----------|
| Policy found, data fresh | Coverage status + `as-of` timestamp |
| Policy not found | `needs-review` with reason code — never a silent "verified"; queue flag raised same business day |
| Replica in refresh window (02:00-04:30) or unreachable | `pending-verification`; queue entry shows the degradation; **intake never blocks** |
| Snapshot older than 36h | Status carries a staleness warning; written-acknowledgment-state claims escalate instead of auto-proceeding |
| Surge back-pressure (added by the day-5 review) | Portal acceptance never rejects a FNOL: accept, queue deeper, show the degraded-confirmation message Luis approved |

## 7. Artifact: threat review outcomes

*Day 4, with Dan. Claude drafted the data flows and candidate list; the session decided.*

- 9 threats identified; 7 mitigated in the design (private endpoint for the replica,
  per-channel input validation at the adapters, audit log integrity, least-privilege service
  accounts among them).
- 2 assigned as **build-time security gates**, feeding the Build loop's risk-tier map (the
  HIGH / MEDIUM / LOW ratings that set how much review each area's changes get):
  - Document upload path → malware scanning, HIGH tier, security workflow on every touching
    PR (pull request — the proposed change under review).
  - Acknowledgment letter templates → PII template-review gate (data leaves the system on paper).

## 8. Artifact: the proving plan and the walking skeleton

*Nadia's, day 4.*

| NFR | Proven by | Read from |
|-----|-----------|-----------|
| NFR-01 (ingestion p95 < 5s — 95 of 100 intakes finish in under 5 seconds) | Load test + continuous gateway metric | Monitoring dashboard |
| NFR-02 (10x surge) | Load test at the Q-16 profile (1,710/day peak, 9 days) before go-live | Load-test report; hardening pass 1 (the first pre-go-live quality push) |
| NFR-03 (99.5% business hours) | Uptime monitor on intake endpoints | Ops dashboard, monthly |
| NFR-05 (PII boundary) | Security checklist per change touching claim data | PR security gate records |
| NFR-07 (audit completeness) | Event-log completeness suite in CI | Test results; quarterly compliance sample |
| ADR-004 eval gate | 200-email golden set, ≥95% field accuracy | Eval suite in CI; regression blocks prompt/model changes |

**The walking skeleton** (what Phase 3 must make real): one portal FNOL flows end to end —
queue entry → replica coverage check → test-mode acknowledgment → metric event — deployed to
Harbor's dev environment through the real pipeline, with the blocking hooks (scripts that
refuse to let an agent finish with failing tests) and the grader (a fresh AI reviewer that
did not write the code) live.

## 9. Artifact: the Phase 3 handoff (summary)

- **Signed decisions:** ADR-001 through ADR-004; the two build-time security gates registered
  for the risk-tier map.
- **Open questions:**

| ID | Question | Owner | Due |
|----|----------|-------|-----|
| Q-17 | Postal dispatch vendor: which provider, and who provisions API credentials for acknowledgment letters? | Dan Kowalski + Harbor ops | Foundation week |
| Q-18 | Construction of the surge load-test dataset from the 2024 CAT (catastrophe) event (volume curve + channel mix) | Priti Shah + Nadia Brooks | Before hardening pass 1 |

- **Recommended first specs:** the walking skeleton, sliced — 0001 queue entry from portal
  FNOL, 0002 replica verification read, 0003 test-mode acknowledgment, 0004 metric event.
  Each rides the full loop; together they prove the architecture under the rails (the
  enforced checks every change runs on).

---

## 10. The tooling behind this phase

The abstract Phase 2 page describes this work generically. What actually ran, on the
**claude-code-sdlc** plugin and its paired skills:

| What got produced | How |
|---|---|
| Option sets with trade-off framings | Claude in-session, plan-mode research (read-and-propose, no file changes); the plugin pairs Phase 2 with the deep-plan skill for structuring the design work |
| ADRs (001-004) | Drafted by Claude from the option-session choices against `templates/phases/02-design/adrs/ADR-template.md`; edited by Rob; signed by Rob + Wes; indexed in the ADR registry |
| Design document + steering visuals | Drafted in-session against `templates/phases/02-design/`; diagrams and the steering narrative rendered with the visual-explainer skill |
| Spike findings (replica window, extraction accuracy) | Orchestrator-driven Claude sessions on throwaway branches; findings recorded as spike notes; code deleted |
| Data model + API contracts | Claude drafts carrying the Phase 1 error specs down into contract behavior; Rob shapes; Wes reviews |
| Threat model + mitigation map | Claude drafts the data-flow diagrams and candidate threat list; the day-4 session with Dan decides; outputs feed the Build risk-tier map |
| Design review (day 5) | `/sdlc-review --all` — the `multi-reviewer` agent in council, adversarial, and edge-cases modes; report written as a phase artifact |
| Consistency check | Cross-artifact reference checks inside `/sdlc-gate`; locked-metric consistency via the frozen-layer validation (the plugin's check that values locked in earlier phases — the success metric, the constraints — haven't been silently altered by later artifacts) |
| Gate, review packet, advance | `/sdlc-gate`, `/sdlc-phase-report`, `/sdlc-next` (after the four-signature phase review) |

---

Next: [the Phase 3 worked example](phase-3-example.md) — the kit (our firm's reusable
engagement starter) lands in Harbor's repo, the
rails get shaken down, and specs 0001-0004 ride the loop to running software in Harbor's dev
environment.
