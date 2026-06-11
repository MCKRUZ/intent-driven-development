# Phase 0 Worked Example: Harbor Mutual

The companion to [the Phase 0 deep-dive](phase-0-discovery.md): a complete, filled-in Phase 0
for a fictional engagement, showing what every artifact looks like when it's done and which day
produced it. All names, numbers, and documents are invented but internally consistent — the
11.4-day baseline, the CR-204 report, and the open question IDs trace through every artifact.

**If you're starting here:**

| | |
|---|---|
| **The method** | Claude (the AI coding agent) drafts documents and writes most code. Humans own every decision and verify every result. |
| **This phase** | Phase 0 (discovery) is the two-week opening that pins down the problem, one measurable success metric, who decides product questions, and the constraints — before any requirements or code. |

**Words this page leans on** (every other term is explained where it first appears):

| Term | What it means |
| ---- | ------------- |
| **The pod** | Our four-to-six person delivery team. In Phase 0 it is mostly two people: the Pod Lead and the Setup Owner. |
| **PO** | Product owner — the client-side person who answers product questions during the build. |
| **The gates** | The automated checks plus a named human sign-off that close a phase. Gates are the billing milestones. |
| **The loop** | The build loop the later phases run on: Intent (decide and write what you want), Delegate (an agent builds it inside set bounds), Discern (checks and a non-author prove it). |
| **The decision list** | The running list of product decisions nobody has made yet, each needing a named human answer. |
| **Steering** | The recurring decision meeting between the pod and the client's leadership; biweekly from Phase 1 on. |
| **The fallback rider** | A pre-agreed contract amendment that would let the pod start under its own Anthropic account, with a migration date, if the client's procurement ran late. |
| **The data-flow brief** | A short document for client security: what data the AI tooling sees, where it flows, and where it is stored. |
| **A HITL gate** | A human-in-the-loop pause built into a command: the tool stops and a named person reviews and decides before anything moves on. |
| **RFP** | Request for proposal — the document a company issues to ask vendors to bid. |
| **Adjudication** | Deciding a claim: is it covered, and what gets paid. |
| **A book** | Insurance shorthand for a portfolio of policies — the property book, the auto book. |
| **PII** | Personally identifiable information — data that identifies a person; claim files are full of it. |
| **SLA** | Service-level agreement — a promised maximum handling or response time. |

**The IDs you'll see on this page** (they stay stable for the whole engagement — a question
raised here is traceable through every later phase):

| ID | What it means |
| -- | ------------- |
| **DOC-NN** | A client document cataloged at intake. |
| **CON-NN** | A contradiction found between two client documents. |
| **Q-NN** | An open question with a named owner and due date. |
| **C-NN** | A constraint. |

## 1. The scenario

**Harbor Mutual Insurance Group** (regional property and auto insurer, ~400 employees) hires
the pod to modernize property-claims intake. Today a claim takes a median of 11.4 days from
first notice of loss (FNOL) to a coverage decision; policyholders who wait more than 7 days
renew measurably less often. A 2024 modernization attempt with another vendor failed. Claims
live in "PolicyOne," a mainframe-era core system with a nightly batch window (policy data
syncs to other systems only once a night).

**The cast:**

| Side | Person | Role |
|------|--------|------|
| Harbor | Karen Voss | VP Claims Operations — sponsor, owns budget and outcome |
| Harbor | Luis Ortega | Claims Product Manager — candidate (and eventual) PO |
| Harbor | Priti Shah | BI (business intelligence) lead — data owner for claims metrics |
| Harbor | Dan Kowalski | IT Security — procurement, data boundary, access |
| Harbor | Gail Tran, Marcus Webb | Senior adjusters — domain experts |
| Harbor | Dee Alvarez | Intake supervisor — domain expert |
| Pod | Maya Chen | Pod Lead |
| Pod | Rob Feld | Setup Owner |

## 2. How the ten days played out

Engagement start Monday 2026-03-02. The artifacts below show end-of-phase state (resolution
and answer logs filled in after the workshop).

> **Reading the Tooling lines.** **You run it** — a slash command you type (e.g. `/sdlc-gate`,
> `/sdlc-coach`). **It triggers** — an agent or script that command runs under the hood, always
> shown after a `→` (e.g. `/sdlc-gate → check_gates.py`). **No plugin command** — a human
> meeting, client-system work, or an exploratory spike; nothing the plugin drives. Drafting
> phase artifacts runs through `/sdlc-coach`, guided dialogue that fills the phase templates;
> the templates themselves are files Claude reads, named in the artifacts, not here.

**Day 1 (Mon 3/2) — kickoff.**
**Tooling —** `/sdlc-setup` → runs `init_project.py` to create the engagement scaffold.
- 60-minute kickoff with Karen, Luis, and Dan: introductions, the how-we-work briefing (the
  loop, the gates, the biweekly demo cadence, what the pod needs from Harbor and when).
- The document corpus arrives: 8 documents, unsorted, exactly as requested.
- Rob hands Dan the data-flow brief and opens the Anthropic procurement conversation — Dan
  owns vendor onboarding and quotes a typical two-week lead time.
- Rob issues the access checklist: contributor access, GitHub Actions enabled, secrets
  permissions, runner policy.
- Rob initializes the engagement scaffold (the standard folder-and-state structure every
  engagement starts from) with **`/sdlc-setup`** (microsoft-enterprise profile) in the pod
  workspace; it moves into the Harbor repo on day 8. The corpus goes into the configured
  intake folder.

**Day 2 (Tue 3/3) — intake and prep.**
**Tooling —** `/sdlc-intake` → runs the `intake_documents.py` cataloger (you never call the
script directly); then `/sdlc-brief` → spawns the `discovery-analyst` agent and drafts the brief.
- Document intake runs (**Phase 0 Step 0c**: the `intake_documents.py` cataloger, then Claude
  summarization): all 8 documents cataloged as DOC-001 through DOC-008. Maya prioritizes the
  catalog at the HITL gate (the RFP, the architecture overview, and the ops report first).
  Claude writes a summary per document plus the registry; the catalog is locked so document
  references stay stable into requirements.
- The **`discovery-analyst`** agent (**Step 0d**) compares the corpus and produces two
  artifacts:
  - Four contradictions (CON-01 through CON-04), each with two verbatim quotes — including
    the big one: the RFP demands real-time adjudication while the architecture document's
    nightly batch makes it impossible.
  - Fourteen questions (Q-01 through Q-14), grouped by agenda block and routed: 6 for the
    workshop, 3 answerable by email, 3 for the day-5 interviews (2 would surface later).
- The three pre-workshop questions go out by email — and all three come back the same day:
  reopened claims are excluded from the cycle-time figure (Q-05, Priti), the cloud is Azure
  only (Q-07, Dan), and PII stays inside Harbor's own cloud tenant (Q-12, Dan).
- **`/sdlc-brief`** drafts the workshop brief through its curation gate: Maya picks what makes
  the page — all four contradictions, six questions, four decisions the room must leave with.
  She edits the draft and sends it to the six attendees herself (the command never sends).

**Day 3 (Wed 3/4) — the outcome workshop.**
**Tooling —** No plugin command. The workshop is humans in a room.
- Three hours, Harbor HQ room 4B, six attendees, Maya facilitating. Humans only.
- All four contradictions get resolved in the room: same-business-day decisions for v1
  (CON-01), property-only scope that must not preclude auto (CON-02), a 40,000-claims/yr
  design target (CON-03), and the metric defined as FNOL-to-coverage-decision (CON-04).
- Six questions answered, including the two that shape the engagement: the business pain is
  renewal churn — policyholders leaving when their policies come up for renewal (Q-01) — and
  the 2024 attempt died from having no internal owner (Q-02).
- The PO decision lands: Luis Ortega, named, 6 hours per week, triage on his calendar.

**Day 4 (Thu 3/5) — first drafts.**
**Tooling —** `/sdlc-coach` → drafts the problem statement, success criteria, and constraints
from the workshop notes (fills the discovery templates).
- Claude drafts the problem statement, success criteria, and constraints from Maya's workshop
  notes.
- Maya corrects all three the same day — drafts age badly.

**Day 5 (Fri 3/6) — interviews and the first checkpoint.**
**Tooling —** No plugin command. Interviews and the sponsor checkpoint are human conversations.
- Interviews: Gail and Marcus (senior adjusters), Dee (intake supervisor), and Harbor
  compliance. Two more questions close: the 15-business-day acknowledgment rule in two states
  (Q-08), and the email channel's dirty secret — a shared Outlook inbox triaged manually twice
  a day with no SLA (Q-11).
- The sponsor checkpoint: Maya reads the draft problem statement to Karen out loud. Karen
  stops her — the corpus framed this as an adjuster-efficiency problem; the real pain is
  renewal churn. The problem statement is reframed the same afternoon. This is the single most
  valuable correction of the phase.

**Day 6 (Mon 3/9) — the metric gets proven.**
**Tooling —** No plugin command. The metric session runs on the client's own reporting system.
- Working session with Priti: report CR-204 is run live, the 11.4-day baseline is read off
  the screen and recorded with its source.
- A surprise: the report's caption says "to first payment" but the underlying query measures
  to coverage decision — the caption is wrong, the query is right. Flagged to Harbor BI.
- The pod's Quality Engineer vets all three success criteria for measurability.

**Day 7 (Tue 3/10) — constitution and the PO record.**
**Tooling —** `/sdlc-coach` → drafts the constitution (fills the constitution template).
- Claude drafts the constitution; Maya keeps it short enough that Karen will actually read it.
- The PO decision is recorded in writing: PO mode, Luis Ortega, 6 hours/week, 2-business-day
  decision turnaround.

**Day 8 (Wed 3/11) — enablement converges.**
**Tooling —** No plugin command. Procurement, keys, and repo access; the day-1 scaffold moves
into the Harbor repo.
- Harbor's Anthropic agreement is signed — two days ahead of the fallback-rider trigger. Keys
  go into Harbor's Key Vault (their cloud secret store); pod seats are issued under Harbor's
  account.
- The delivery repo is live in Harbor's GitHub org with the engagement structure initialized;
  every Phase 0 artifact moves in and is committed. The repo is now the only home.
- The access checklist closes.

**Day 9 (Thu 3/12) — the gate run.**
**Tooling —** `/sdlc-gate` → runs `check_gates.py`, then spawns the `gate-repair` agent on the
one failure · `/sdlc-enhance` → spawns the `narrative-enhancer` agent · `/sdlc-phase-report` →
runs `generate_phase_report.py`.
- Claude drafts the Phase 1 handoff; the two still-open questions (Q-13, Q-14) carry into it
  under their original IDs, each with an owner and a due date.
- **`/sdlc-gate`** runs the six-gate check: one completeness failure — a leftover placeholder
  in the constraints file — which the **`gate-repair`** agent fixes (structural repair only),
  and the gate re-runs clean.
- **`/sdlc-enhance`** generates the plain-language narrative companion for Karen (the
  `narrative-enhancer` agent); Maya edits it before it goes anywhere.
- **`/sdlc-phase-report`** renders the stakeholder HTML report for tomorrow's review.

**Day 10 (Fri 3/13) — phase review and sign-off.**
**Tooling —** `/sdlc-next` → re-runs `check_gates.py`, then `advance_phase.py` after the human
sign-off.
- 45 minutes with Karen: the constitution walked page by page, the metric shown with its
  verified baseline, the constraints, the PO record, and the two open questions with their
  owners.
- Karen signs the outcome statement. The advance is approved and recorded with
  **`/sdlc-next`**, which re-verifies the gates and moves the engagement state to Phase 1.
  Billing milestone 1.

## 3. What to notice

- **The contradiction that paid for the phase:** CON-01 (the RFP demands real-time
  adjudication; the architecture doc makes it impossible). Resolved in 20 minutes in a room;
  would have been weeks of rework discovered mid-build.
- **The metric definition fight (CON-04):** two Harbor documents measured "cycle time"
  differently. The success metric is worthless until the room picks one. They picked
  FNOL-to-coverage-decision.
- **The reframe on day 5:** the corpus framed the problem as adjuster efficiency; the sponsor,
  hearing the draft read aloud, corrected it to renewal churn. That one correction changed the
  primary metric's "why" — and it's exactly what the day-5 checkpoint exists to catch.
- **Questions only:** the brief never proposes an outcome. Every framing appears as an
  attributed claim with a DOC reference.
- **Q-NN continuity:** Q-13 and Q-14 are still open at phase exit and appear in the handoff
  under the same IDs.

---

## 4. Artifact: the document registry

*Produced day 2 by document intake (Step 0c: `intake_documents.py` + Claude summarization).
Registry locked 2026-03-03.*

| Metric | Value |
|--------|-------|
| Total Documents | 8 |
| Total Estimated Tokens | ~96,000 |
| File Types | pdf (5), docx (1), md (2) |

| ID | Filename | Est. Tokens | Key Topics |
|----|----------|-------------|------------|
| DOC-001 | claims-modernization-rfp.pdf | 22,000 | scope, requirements, real-time adjudication, volumes |
| DOC-002 | policyone-architecture-overview.pdf | 18,500 | PolicyOne core, nightly batch, integration points |
| DOC-003 | fnol-intake-process-flows.docx | 9,000 | FNOL channels (phone 55%, portal 30%, email 15%), triage steps |
| DOC-004 | 2024-modernization-postmortem.pdf | 7,500 | prior vendor attempt, integration failure, lessons |
| DOC-005 | claims-ops-q4-2025-report.pdf | 12,000 | cycle time 11.4 days, 38,000 property claims/yr, adjuster touches 7.3 |
| DOC-006 | it-security-standards.md | 8,000 | Azure-only cloud policy, data residency, vendor onboarding |
| DOC-007 | integration-api-inventory.md | 6,000 | PolicyOne APIs, document store, payment gateway |
| DOC-008 | claims-2027-strategy-deck.pdf | 13,000 | auto-claims expansion, PolicyOne retirement ambition, cycle-time goals |

Topic clusters: **Current state** (DOC-002/003/005/007), **Ambition** (DOC-001/008),
**Constraints** (DOC-006/002), **History** (DOC-004).

## 5. Artifact: the contradiction list

*Produced day 2 by the `discovery-analyst` agent (Step 0d); resolutions recorded at the day-3
workshop.*

### CON-01: Real-time adjudication vs. the nightly batch window

- **Type:** assumption · **Severity:** blocks-outcome
- **DOC-001 §3.2:** "The solution shall provide real-time adjudication for eligible claims at
  the point of first notice of loss."
- **DOC-002 §4.1:** "Policy and coverage records are synchronized to downstream systems via
  the nightly batch cycle (21:00–04:30); intraday reads reflect the prior business day."
- **Why it matters:** The RFP's headline requirement is impossible against the current core
  system. Either "real-time" gets redefined, or the engagement includes a PolicyOne read-path
  nobody has scoped or priced.
- **The question for the room:** Is a same-business-day coverage decision acceptable for v1,
  or is true real-time a hard requirement worth the integration cost?
- **Resolution:** Same-business-day accepted for v1; true real-time deferred to the
  auto-claims phase. (Karen Voss, 2026-03-04)

### CON-02: v1 scope — property only, or property and auto?

- **Type:** scope · **Severity:** blocks-outcome
- **DOC-001 §2.1:** "This procurement covers the property claims intake and triage process."
- **DOC-008 slide 9:** "Unified intake across property and auto books by FY2027 — single
  platform, single queue."
- **Why it matters:** Scope determines volume targets, data model, and timeline. Designing for
  property-only and discovering auto in month four is the 2024 failure replayed.
- **The question for the room:** Is v1 property-only, and if so, what must the design not
  preclude for auto?
- **Resolution:** v1 is property-only; the claim data model and queue design must not preclude
  adding the auto book — gated at Phase 2 design review. (Karen Voss, 2026-03-04)

### CON-03: Annual claim volume — 38,000 or 60,000?

- **Type:** fact · **Severity:** shapes-design
- **DOC-005 p.3:** "Property claims received FY2025: 38,142."
- **DOC-001 §1.4:** "Harbor processes approximately 60,000 claims annually."
- **Why it matters:** Sizing, load assumptions, and fast-path eligibility analysis all key off
  volume. A 60% disagreement is not a rounding error.
- **The question for the room:** Which number is the design target, and what does 60,000 include?
- **Resolution:** 60,000 includes the auto book; property design target is 40,000/yr with 25%
  headroom. (Priti Shah, 2026-03-04)

### CON-04: What "cycle time" means

- **Type:** terminology · **Severity:** shapes-design
- **DOC-005 p.2:** "Median cycle time (FNOL to first indemnity payment): 11.4 days."
- **DOC-008 slide 4:** "Target: claims cycle time (FNOL to coverage decision) under 3 days by
  2027."
- **Why it matters:** The engagement's success metric is unusable until one definition wins —
  the two definitions can move in opposite directions.
- **The question for the room:** Which definition does the success metric use?
- **Resolution:** FNOL to coverage decision. The 11.4-day baseline was confirmed to be
  FNOL-to-decision in the underlying CR-204 query despite the DOC-005 caption (caption error
  flagged to BI). (Priti Shah, 2026-03-04; verified at the 2026-03-09 metric session)

## 6. Artifact: the question list

*Produced day 2 by the `discovery-analyst` agent (Step 0d). 14 questions: 6 routed workshop,
3 pre-workshop (emailed day 2), 3 interview, 2 still open at phase exit.*

| ID | Block | Question | Route | Answer |
|----|-------|----------|-------|--------|
| Q-01 | Problem | Who is hurt most by the 11.4 days — policyholders or the claims team? | workshop | Renewal churn is the frame: claimants waiting >7 days renew 2.1 points lower (Karen, 3/4) |
| Q-02 | Problem | What actually killed the 2024 attempt? | workshop | No named internal owner; integration scope found in month five (Karen, 3/4) |
| Q-03 | Outcomes | Should Harbor's engineers run this delivery model after handoff? | workshop | Yes — four engineers trained into the loop (Karen, 3/4) |
| Q-04 | Metric | What exact report produces the 11.4-day figure; can it run on demand? | interview | CR-204, ClaimsCenter BI, weekly, on-demand capable; run live 3/9 (Priti) |
| Q-05 | Metric | Does the figure include reopened claims? | pre-workshop | No — tracked separately (Priti, email 3/3) |
| Q-06 | Constraints | Is the PolicyOne retirement date funded and fixed, or aspirational? | workshop | Aspirational, unfunded — treat PolicyOne as permanent for v1 (Karen, 3/4) |
| Q-07 | Constraints | Azure-only, or is anything on AWS? | pre-workshop | Azure only; the AWS reference was the failed vendor's proposal (Dan, email 3/3) |
| Q-08 | Constraints | Do state regulations bound acknowledgment or decision timelines? | interview | 15-business-day acknowledgment in two states; 96.2% compliance today (compliance, 3/6) |
| Q-09 | PO | Can Harbor commit a named PO at the agreed hours with 2-day turnaround? | workshop | Luis Ortega, 6 hrs/week, triage on his calendar (Karen, 3/4) |
| Q-10 | Tooling | Who owns Anthropic vendor onboarding; what lead time? | workshop | Dan owns it; ~2 weeks; started day 1, signed 3/11 — fallback rider not needed |
| Q-11 | Other | Where does FNOL email volume land; who triages it? | interview | Shared Outlook inbox, manual triage twice daily, no SLA (Dee, 3/6) |
| Q-12 | Other | Can claim documents (PII) appear in agent context? | pre-workshop | PII stays in Harbor tenant; intake corpus was redacted (Dan, email 3/3) |
| Q-13 | Other | Do the two states' acknowledgment rules apply differently to the portal channel? | interview | **OPEN** — carried to handoff (owner Luis, due Phase 1 wk 1) |
| Q-14 | Other | What share of property claims is "simple" (single dwelling, no injury, <$25k) and fast-path eligible? | interview | **OPEN** — carried to handoff (owner Priti, due Phase 1 wk 1) |

## 7. Artifact: the workshop brief

*Drafted day 2 via `/sdlc-brief`, curated by Maya at its HITL gate, sent by Maya. The one
page, as sent:*

> **Workshop Brief — Harbor Mutual Outcome Workshop**
> Wednesday 2026-03-04, 9:00–12:00, Harbor HQ room 4B · runs 3 hours
> Attendees: Karen Voss (VP Claims Ops, sponsor), Luis Ortega (Claims PM), Priti Shah (BI),
> Dan Kowalski (IT Security), Gail Tran (senior adjuster), Dee Alvarez (intake supervisor)
> Facilitator: Maya Chen · Pre-reading: this page only
>
> **What we read.** 8 documents provided by your team. The load-bearing three: DOC-001 (the
> modernization RFP), DOC-002 (PolicyOne architecture), DOC-005 (Q4 2025 claims ops report).
>
> **What the documents say.**
> - Median property-claim cycle time is 11.4 days; an average claim is touched 7.3 times (DOC-005)
> - FNOL arrives by phone (55%), portal (30%), and email (15%) (DOC-003)
> - Policy data syncs on a nightly batch; intraday reads show yesterday (DOC-002 §4.1)
> - A 2024 modernization attempt was cancelled in month six (DOC-004)
>
> **Where the documents disagree.**
> 1. DOC-001 §3.2 requires real-time adjudication; DOC-002 §4.1 says the nightly batch makes
>    intraday policy reads stale. *Is same-business-day acceptable for v1?* (CON-01)
> 2. DOC-001 scopes property; DOC-008 plans property + auto by 2027. *Is v1 property-only, and
>    what must the design not preclude?* (CON-02)
> 3. 38,142 claims/yr (DOC-005) vs ~60,000 (DOC-001). *Which is the design target?* (CON-03)
> 4. Cycle time to first payment (DOC-005) vs to coverage decision (DOC-008). *Which definition
>    does the success metric use?* (CON-04)
>
> **What nobody has written down.** Problem: who is hurt most — policyholders or the claims
> team? (Q-01) What killed the 2024 attempt? (Q-02) Outcomes: should Harbor's engineers run
> this model after we leave? (Q-03) Constraints: is the PolicyOne retirement funded? (Q-06)
> Ownership: can Harbor commit a named PO at ~4-6 hrs/week? (Q-09) Tooling: who owns Anthropic
> onboarding? (Q-10)
>
> **Decisions we need from the room.** 1. The one success metric — definition and source
> system. 2. v1 scope. 3. Real-time vs same-business-day. 4. The PO commitment.
>
> **Agenda.** The problem in your words (45) · the three outcomes (45) · the one metric (30) ·
> constraints (30) · product ownership (20) · tooling status (10).

## 8. Artifact: the problem statement

*Drafted day 4 from workshop notes; reframed day 5 at the sponsor checkpoint; signed day 10.*

**The problem.** Property policyholders wait a median of 11.4 days from first notice of loss
to a coverage decision. Claimants who wait more than 7 days renew at a rate 2.1 points lower —
on Harbor's property book, approximately $3.4M in annual premium. The cost of the delay is
paid at renewal time, by retention, not primarily in claims-department overtime. (That framing
is the sponsor's, corrected at the day-5 checkpoint: the corpus framed this as adjuster
efficiency; Karen Voss reframed it as retention. Efficiency improves as a consequence, not as
the goal.)

**Observable symptoms.** Median FNOL-to-decision 11.4 days (CR-204, verified live 3/9); 7.3
touches by 5 people per average claim; email FNOL (15% of volume) lands in a shared Outlook
inbox triaged manually twice a day with no SLA; portal FNOL re-keyed into PolicyOne by hand;
intraday policy reads show yesterday because of the nightly batch — a built-in extra day on
every same-day claim.

**Who is affected.** Policyholders at the worst moment of their relationship with Harbor; 64
property adjusters spending touches on coordination instead of decisions; the 9-person intake
team; Harbor's renewal book, where the cost actually lands.

**Why now.** The 2024 attempt failed (no internal owner, late integration scope), the 2027
strategy depends on a working property platform to extend to auto, and Q4 2026 is the first
renewal season a fixed cycle time could protect.

**Root cause.** Five-whys (asking "why" repeatedly until the answers stop changing) converges
on two causes: (1) no single queue — three FNOL channels
with three intake mechanics and no shared prioritization; (2) coverage verification blocked on
a nightly batch. Everything else is downstream of those two.

## 9. Artifact: the success criteria

*Drafted day 4; baselines verified live at the day-6 metric session.*

**Primary — the one metric: median days from FNOL to coverage decision, property claims.**

| Field | Value |
|-------|-------|
| Definition | FNOL timestamp to coverage-decision timestamp, median, property book, reopened claims excluded (Q-05); definition fixed by CON-04 |
| Baseline | **11.4 days** (FY2025) — read live with the data owner on 2026-03-09 |
| Source system | Report CR-204, ClaimsCenter BI; weekly batch, on-demand capable |
| Target | ≤ 5.0 days median within 12 months of go-live |
| Stretch | ≤ 3.0 days · **Partial success:** ≤ 7.0 (clears the churn threshold) · **Failure:** no meaningful movement |

Secondary: **S1** regulatory acknowledgment compliance (baseline 96.2% → target 100%);
**S2** adjuster touches per claim (baseline 7.3 → target ≤ 4.0). Explicitly not success
metrics: features shipped, PR (pull request) counts, story points, agent productivity figures.

Instrumentation debt (measurement work that still has to be built) carried to Phase 1: S1's read is quarterly and manual today (automating
it is Phase 1 scope); Q-14 blocks fast-path target-setting.

## 10. Artifact: the constraints

*Drafted day 4; signed day 10.*

| # | Constraint | Fixed / Negotiable | Source |
|---|-----------|--------------------|--------|
| C-01 | Azure is the only approved cloud | Fixed | DOC-006 §2; Q-07 |
| C-02 | PolicyOne stays; the nightly batch window is a hard integration boundary for v1 | Fixed | Q-06; CON-01 |
| C-03 | v1 property-only; design must not preclude the auto book | Fixed | CON-02; gated at Phase 2 |
| C-04 | 15-business-day acknowledgment in two regulated states | Fixed | Q-08 — becomes acceptance criteria and test cases |
| C-05 | Claim documents and PII stay in the Harbor tenant; no PII in model context outside the approved Azure path | Fixed | Q-12 |
| C-06 | Anthropic access under Harbor's agreement; keys in Harbor Key Vault | Fixed | Signed 3/11 |
| C-07 | Fixed fee per phase; gates are the billing milestones | Fixed | SOW (statement of work) |
| C-08 | Go-live before the Q4 2026 renewal season (Oct 1) | Negotiable | Karen prefers scope cuts over date slips, in that order |
| C-09 | Design target 40,000 property claims/yr including headroom | Negotiable | CON-03; revisit after Q-14 |

## 11. Artifact: the constitution

*Drafted day 7; signed by the sponsor at the day-10 phase review.*

**Identity.** Harbor Claims Intake — a unified property-claims intake and triage system
replacing three disconnected FNOL channels with one queue and same-business-day coverage
decisions, integrated with PolicyOne. Project type: service.

**Mission.** Get property policyholders a coverage decision in days, not weeks, so that a
claim becomes a reason to renew instead of a reason to leave.

**The three outcomes.** Business: median FNOL-to-decision ≤ 5 days (from 11.4), protecting
renewal retention. Software: one intake system across phone, portal, email; a single
prioritized queue; fast-path triage for simple claims; PolicyOne integration that lives with
the batch window. Capability: four named Harbor engineers run this delivery model
independently by engagement close.

**Governing principles.** (1) Retention is the frame — when efficiency and claimant experience
conflict, claimant experience wins. (2) The batch window is real — v1 designs with it, not
around an unfunded retirement. (3) Property-only, auto-proof — checked at every design gate.
(4) Regulatory clocks are acceptance criteria, tested not remembered. (5) No PII in model
context outside the approved Azure path.

**Decision authority.** Outcome, budget, phase sign-off: Karen Voss. Product decisions and
decision-list answers (2-business-day turnaround): Luis Ortega. ADRs (architecture decision records): pod Setup Owner,
co-signed by Harbor's lead engineer from Phase 2. Security and data boundary: Dan Kowalski.
Scope changes: Karen, on Luis's recommendation.

## 12. Artifact: the Phase 1 handoff

*Drafted day 9; phase closed day 10 (billing milestone 1).*

**Key findings.** The business problem is renewal churn, not adjuster overtime. Two root
causes: no single queue, and verification blocked on the nightly batch. v1 property-only
(40k/yr target), auto-proof. Same-business-day accepted; real-time deferred. Two regulated
states impose a 15-business-day acknowledgment clock. The 2024 attempt failed on ownership and
late integration scope — the PO commitment and the Phase 3 walking skeleton (the thinnest
end-to-end slice of the system, built first to prove the architecture works in practice) are
the direct countermeasures. Harbor wants the capability outcome: four engineers trained.

**Open questions for Phase 1.**

| ID | Question | Owner | Due |
|----|----------|-------|-----|
| Q-13 | Do the two states' acknowledgment rules apply differently to the portal channel? | Luis Ortega | Phase 1, week 1 |
| Q-14 | What share of property claims is "simple" and fast-path eligible? | Priti Shah | Phase 1, week 1 |

**Risks carried forward.** PolicyOne integration surprises (killed the 2024 attempt; DOC-007's
API inventory is dated 2023 — Phase 2 design spike, a short timeboxed technical
investigation, against the live inventory before any contract is drawn). CR-204 caption/definition drift (BI fix confirmed before the metric goes
on the steering scorecard). Email-channel mechanics undocumented (Phase 1 interviews the
intake team, not just the supervisor). Renewal-season deadline pressure (scope cuts decided at
steering, never silently in the flow).

**Recommended Phase 1 starting point.** Start requirements with the single queue (channel
unification), not the fast-path: the queue is the prerequisite for everything, and the email
channel is the least understood. Fast-path requirements wait on Q-14's segmentation.

---

## 13. The tooling behind this phase

The abstract Phase 0 page describes this work generically. In practice, the engagement ran on
the **claude-code-sdlc** plugin. What produced what:

| What got produced | How |
|---|---|
| Engagement scaffold (state, profile, artifact folders) | `/sdlc-setup` with the `microsoft-enterprise` profile (day 1, pod workspace; moved into the Harbor repo day 8) |
| Document catalog, summaries, registry, intake index | Phase 0 Step 0c: `scripts/intake_documents.py` catalogs with DOC-NNN IDs; Claude writes the summaries and registry; Maya prioritizes at the HITL gate; catalog locked |
| Contradiction list, question list | The `discovery-analyst` agent (Phase 0 Step 0d) |
| Workshop brief | `/sdlc-brief` — analysis reused, Maya curates at the HITL gate, Maya sends |
| Problem statement, success criteria, constraints, constitution, handoff | Drafted in-session against the `templates/phases/00-discovery/` templates, following the `/sdlc` phase guidance |
| Gate check (day 9) | `/sdlc-gate` (the six-gate check via `check_gates.py`); the structural placeholder fixed by the `gate-repair` agent |
| Narrative companion for Karen | `/sdlc-enhance` (the `narrative-enhancer` agent), edited by Maya |
| Stakeholder HTML report | `/sdlc-phase-report` |
| Phase advance + billing milestone record | `/sdlc-next` (re-runs gates, records the human sign-off, moves state to Phase 1) |

---

Next: [the Phase 1 worked example](phase-1-example.md) — what happened to Q-13, Q-14, and the
recommended starting point in the week that followed.
