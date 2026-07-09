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

## What Phase 0 received

No prior phase — only the client's own documents, and they disagree.

Harbor Mutual — a fictional regional property insurer of roughly 400 employees — hired a
two-person pod to rebuild how property-claims intake works. A claim takes a median of **11.4
days** from FNOL (first notice of loss) to a coverage decision, and policyholders who wait more
than seven days renew measurably less often. Claims live in "PolicyOne," a mainframe-era core
with a nightly batch window. Phase 0 has no phase before it. It does not inherit a handoff; it
inherits a *corpus* — eight documents written by different people at different times, plus the
SOW (statement of work). Design does not start from requirements. It starts from
**contradictions**.

**Taken in at intake** — cataloged by `intake_documents.py` into `.sdlc/context/intake/`:
`claims-modernization-rfp.pdf`, `policyone-architecture-overview.pdf`,
`fnol-intake-process-flows.docx`, `2024-modernization-postmortem.pdf`,
`claims-ops-q4-2025-report.pdf`, `it-security-standards.md`, `integration-api-inventory.md`,
`claims-2027-strategy-deck.pdf`, and the SOW.

**The four questions the two weeks must answer.** Nothing else. Requirements, design, and code
each have their own phase; pulled forward, they get rebuilt. Phase 0 answers four:

1. **What problem, and how will we know we solved it?** One measurable number, not a feature list.
2. **Who decides product questions during the build?** A named PO, in writing.
3. **Can we legally and technically work?** Tooling, access, the data boundary.
4. **What is non-negotiable?** The constraints that can't be designed away.

Engagement start: Monday 2026-03-02. Every artifact on this page shows its end-of-phase state —
the 11.4-day baseline, the CR-204 report, and the open question IDs trace through all of them.

**Why Harbor is watching this one.** Harbor had already lived the failure. An earlier attempt to
modernize the same system was cancelled in its sixth month.

> **From Harbor's own post-mortem (DOC-004):** "Cancelled in month six. No single internal owner;
> integration scope only surfaced in month five."

**Karen Voss is the one to watch.** Harbor's VP of Claims Operations owns the budget and the
outcome, and signs the phase. Phase 0 is the countermeasure to 2024: surface the scope in week
one, and name an owner before a line ships.

**The cast.**

| Side | Person | Role |
|------|--------|------|
| Pod | Maya Chen | Pod Lead — runs the workshop and interviews, owns every artifact, gets the sponsor's signature |
| Pod | Rob Feld | Setup Owner — chases access, the repo, and the data-flow brief |
| Pod | Quality Engineer | ~10% — one job: vet that every success criterion is actually readable (Nadia Brooks, from Phase 1) |
| Pod | Claude | Reads the corpus, surfaces contradictions, drafts — never decides |
| Harbor | Karen Voss | VP Claims Operations — sponsor; owns budget and outcome; signs the phase |
| Harbor | Luis Ortega | Claims Product Manager — candidate, and eventual, PO |
| Harbor | Priti Shah | BI lead — data owner for claims metrics; runs CR-204 live |
| Harbor | Dan Kowalski | IT Security — procurement, the data boundary, access |
| Harbor | Gail Tran, Marcus Webb | Senior adjusters — domain experts |
| Harbor | Dee Alvarez | Intake supervisor — domain expert |

**The ID codes, decoded.** Every artifact in this engagement carries a stable identifier, so a
decision made in week one can still be traced in month nine. Phase 0 mints most of them. You'll
see these throughout:

| Prefix | Means | Born in | Example here |
|--------|-------|---------|--------------|
| `DOC-NNN` | A client document taken in at intake | Phase 0, day 2 | DOC-004 the 2024 post-mortem · DOC-007 the 2023 API inventory |
| `CON-NN` | A contradiction — two documents that disagree | Phase 0, day 2 | CON-01 real-time vs. the nightly batch |
| `Q-NN` | An open question with an owner and a route | Phase 0, day 2 | Q-13, Q-14 — still open at exit, carried to Phase 1 |
| `C-NN` | A constraint — a hard limit the build must honor | Phase 0 | C-02 nightly sync · C-03 auto-proof |
| `CR-NNN` | A client BI report the metric is read from | client system | CR-204, the 11.4-day baseline |
| `S-N` | A secondary success metric | Phase 0, day 6 | S1 ack compliance · S2 adjuster touches |

The plugin's Phase 0 opens by asking a human, not by reading. Its first act (Step 0) is a
blocking gate: the sponsor answers five scoping questions before Claude drafts anything — and the
plugin twice repeats *never fabricate a stakeholder persona*. The corpus anchors the questions; a
human anchors the answers.

## The procedure, step by step

Phase 0 is a numbered sequence of steps in `claude-code-sdlc` and ten working days in this
standard — the same two weeks seen twice. Below, they're braided: what the tool runs, what the
humans do that the tool cannot, and the file each day leaves behind. Two streams run in parallel
the whole time — **understanding** (the workshop, the metric, the artifacts) and **enablement**
(access, the repo, the data boundary) — so lead-time waits never idle the phase. **Step through
it.**

The state markers used throughout:

- `▪` a command does it — and writes the file
- `▸` a person does it — and it is recorded
- `⚠` a person does it — and nothing records it

### Day 1 — Mon 3/2 · plugin Step 0 opens

**Frame the problem with a human, not the corpus — and start the slow clock.**

**Tooling —** `/sdlc-setup → init_project.py` · `Step 0 HITL gate` · *human decision*
**Artifacts out —** `project_type → state.yaml` · ▸ *the sponsor's five answers, held in the session*

Before Claude reads a single document, the plugin opens with a **blocking human gate**. Step 0
asks the sponsor five scoping questions with `AskUserQuestion` and records the system type in
`state.yaml`; nothing is drafted until a person answers. In parallel, the enablement work that
waits on other people — procurement, access, the data-flow brief — starts *today*. Step 0b (a
brownfield code scan) is conditional and skipped here: Harbor's rebuild has no existing codebase
to analyze.

> **At Harbor:** 60-minute kickoff with Karen, Luis, and Dan: the loop, the gates, the demo
> cadence. Eight documents arrive. Rob hands Dan the data-flow brief, opens Anthropic procurement
> (~2-week lead, Q-10), and issues the access checklist. Karen answers Step 0's five questions;
> `project_type = service`.

> ⚠ **The gap:** *Never fabricate stakeholder personas.* The plugin repeats it in Step 0 and again
> in its artifact rules: Claude records only the people Karen actually names — no hypothetical
> reviewers, no invented end users. The problem framing is anchored to human answers, not
> synthesized from the corpus.

### Day 2 — Tue 3/3 · plugin Steps 0c–0d · the most tool-dense day

**The AI reads everything — then reads it against itself.**

**Tooling —** `/sdlc-intake → intake_documents.py` · `/sdlc-brief → discovery-analyst`
**Artifacts out —** `.sdlc/context/intake/` (catalog.json, index.md, DOC summaries) ·
`contradiction-list.md` · `question-list.md` · ⚠ *the workshop brief — curated & sent by a human;
never committed*

Document intake (Step 0c, `/sdlc-intake`) catalogs every document: a stable `DOC-NNN` id, a
token-budgeted summary, and a locked index, all under `.sdlc/context/intake/`. A human prioritizes
the catalog at the intake HITL gate. Then a fresh `discovery-analyst` agent (Step 0d) reads the
documents *against each other* and emits the contradiction list and the question list. The
workshop brief is drafted by `/sdlc-brief` — but a HITL gate governs it.

> **At Harbor:** Intake catalogs DOC-001…008 (~96,000 estimated tokens); Maya prioritizes at the
> HITL gate; the catalog locks 3/3. `discovery-analyst` produces CON-01…04 and Q-01…14. Three
> pre-workshop questions go out by email — all three answered the same day (Q-05, Q-07, Q-12).
> Maya curates the brief to one page and sends it herself.

> ⚠ **The gap:** The plugin forbids drafting outcomes, metrics, or solutions into the workshop
> brief — *questions only*. The human chooses its contents, edits the draft, and distributes it;
> Claude never sends anything to the client. It is a real artifact the method leans on, and it
> leaves no committed file behind.

### Day 3 — Wed 3/4 · no command runs — humans in a room

**The one meeting that must happen in a room.**

**Tooling —** *none — humans in a room, Maya facilitating*
**Artifacts out —** ▸ *four contradictions resolved & the PO decision — in workshop notes, not yet
on disk*

Half a day, the right people, no AI in the room. The contradictions get settled, the real problem
gets named in the sponsor's own words, the single success metric gets chosen, and the PO decision
is forced explicitly rather than left to drift.

> **At Harbor:** Three hours, room 4B, six attendees. All four contradictions resolved: CON-01
> same-business-day for v1 (real-time deferred); CON-02 property-only, auto-proof; CON-03
> 40,000/yr design target; CON-04 the metric is FNOL-to-coverage-decision. Six questions answered.
> The PO decision lands: **Luis Ortega, 6 hrs/week** (Q-09).

### Day 4 — Thu 3/5 · plugin Steps 1–4

**Drafted by the AI, corrected by a human the same day.**

**Tooling —** `/sdlc-coach → drafts the artifacts`
**Artifacts out —** all under `.sdlc/artifacts/00-discovery/`: `problem-statement.md` ·
`success-criteria.md` · `constraints.md` · `question-list.md` — regenerated as decision list v1

With workshop notes in hand, the tool is finally allowed to write. Four steps fire: identify the
problem and its root cause (Step 1, Five Whys), analyze the current state (Step 2), define success
with baselines and targets (Step 3), and set the scope and constraints (Step 4). The Pod Lead
corrects each the same day — drafts age badly.

> **At Harbor:** Claude drafts the problem statement, success criteria, and constraints from Maya's
> notes; Maya corrects all three the same day. The corpus framed this as an *adjuster-efficiency*
> problem, so the first draft inherits that framing — the error corrected tomorrow.

### Day 5 — Fri 3/6 · no command runs

**The cheap-correction point.**

**Tooling —** *none — human interviews, then the sponsor checkpoint*
**Artifacts out —** ▸ *the reframed problem statement — corrected in place*

Interviews with the people who live the problem daily, then the draft problem statement read
*aloud* to the sponsor. This is where "that's not actually the problem" surfaces — on day 5 rather
than day 50.

> **At Harbor:** Interviews with Gail, Marcus, Dee, and compliance close Q-08 (15-business-day
> acknowledgment in two states; 96.2% compliance today) and Q-11 (email FNOL lands in a shared
> Outlook inbox, triaged twice daily, no SLA). Then Maya reads the draft aloud; Karen reframes it:
> **efficiency → renewal churn**, roughly **$3.4M/yr** in property premium. The single most
> valuable correction of the phase — the corpus framed this as adjuster overtime; the sponsor owned
> the truth.

### Day 6 — Mon 3/9 · no command runs — the client's own system

**Produce the number, live.**

**Tooling —** *none — the report runs on the client's BI system, with the data owner*
**Artifacts out —** `success-criteria.md` — baseline field, now filled from a live read

Sit with the data owner and actually run the report on the real system. Read the baseline off the
screen and record it with its source named. A promised metric isn't good enough; a proven one is
the bar. The baseline lands in `success-criteria.md` — its home.

> **At Harbor:** A session with Priti: report **CR-204** is run live, and the **11.4-day** baseline
> is read off the screen and recorded with its source. The report's caption said "to first
> payment," but the underlying query measured to coverage decision — caption wrong, query right,
> flagged to BI. The Quality Engineer vets all three criteria.

> ⚠ **The gap:** The live read is exactly the human work the automated gate cannot verify.
> `check_gates.py` confirms `success-criteria.md` exists and has a baseline field; it cannot tell
> whether the number was read from a live system or typed from memory. The receipt is a human's
> word.

### Day 7 — Tue 3/10 · plugin Step 5

**Write the thing the sponsor will sign; put ownership in writing.**

**Tooling —** `/sdlc-coach → constitution.md`
**Artifacts out —** `constitution.md` · ⚠ *PO decision record — method requires it; no command
writes it* · ⚠ *tooling record — method requires it; no command writes it*

Step 5 drafts the **constitution** — the project's short identity document: what it is, what
"done" means, the metric, the principles, who decides. The PO decision is finalized in writing,
and the tooling status is checked against the fallback trigger date.

> **At Harbor:** Claude drafts the constitution; Maya keeps it short. The PO decision is recorded in
> writing: Luis Ortega, 6 hrs/week, 2-business-day turnaround, triage on his calendar.

> ⚠ **The gap:** The standard wants a **PO decision record** signed by the sponsor and a **tooling
> record** owned by the Setup Owner. The plugin emits neither file. At Harbor these facts survive
> only folded into the constitution's decision authority and constraint C-06 — the standard's two
> signed records leave no dedicated artifact.

### Day 8 — Wed 3/11 · no command runs — the checkpoint with teeth

**Access goes live; the repo becomes the only home.**

**Tooling —** *none — procurement lands, the repo goes live, artifacts are committed*
**Artifacts out —** every 00-discovery artifact — committed to the client-org repo

The enablement stream converges on a hard checkpoint: access goes live under the client's own
account, or the fallback rider is invoked *today* — not "next week." Every artifact produced so
far moves into the client-org repository and is committed. From here, the repo is the only home.

> **At Harbor:** Harbor's Anthropic agreement is signed **two days ahead** of the fallback-rider
> trigger. Keys land in Harbor's Key Vault; pod seats issue under Harbor's account; Azure-only, PII
> inside the Harbor tenant (Q-07, Q-12). The delivery repo goes live in Harbor's GitHub org and
> every Phase 0 artifact is committed. The access checklist closes.

### Day 9 — Thu 3/12 · plugin Steps 6–8

**Package the handoff; the machine checks the work.**

**Tooling —** `/sdlc-gate → check_gates.py` · `/sdlc-enhance` ·
`/sdlc-phase-report → generate_phase_report.py`
**Artifacts out —** `phase1-handoff.md` · `.sdlc/reports/phase00-report.html` ·
`.sdlc/reports/phase00-visual.html`

Step 6 packages the Phase 1 handoff. Steps 7–8 render the sponsor's narrative companion and the
gate report. `/sdlc-gate` runs `check_gates.py` over the artifacts; anything incomplete gets fixed
today, and any still-open question is written down to carry forward under its original ID.

> **At Harbor:** Claude drafts the handoff; Q-13 and Q-14 carry forward under the same IDs. The gate
> finds one completeness failure — a leftover placeholder in the constraints file — which the
> `gate-repair` agent fixes; the check re-runs clean. The narrative companion is generated and the
> HTML report rendered.

> ⚠ **The gap:** `check_gates.py` verifies that five files exist, are non-empty, and contain no
> placeholder text. This standard's exit gate has **eight** bullets — the sponsor's signature, the
> metric read from a live source, the PO decision in writing, access live under the client's
> account — and the script reads none of them. It confirms the files are present; a human confirms
> they are true. *The gate is real. What it checks is a fraction of what must be signed.*

### Day 10 — Fri 3/13 · plugin advance

**A signature, and the meter starts.**

**Tooling —** `/sdlc-next → advance_phase.py --confirmed`
**Artifacts out —** ▸ *the sponsor's signature — billing milestone 1*

A 45-minute review walks the constitution, the metric with its verified baseline, the constraints,
the PO decision, and the open questions. The sponsor signs. `advance_phase.py` will not move the
engagement forward without `--confirmed` — a named human's sign-off.

> **At Harbor:** 45 minutes with Karen: the constitution page by page, the metric with its verified
> baseline, the constraints, the PO record, the two open questions. Karen signs the outcome
> statement. The advance is approved and recorded; state moves to Phase 1. **Billing milestone 1.**

## What Phase 0 produced

The whole output of the opening two weeks, named. Blue (`▪`) rows are written by a command and
checked by the gate. **Amber (`⚠`) rows are the method's human work** — required by this standard,
produced by no tool, and today leaving no file behind. Those are the rows to argue about.

State markers:

- `▪` a command does it — and writes the file
- `▸` a person does it — and it is recorded
- `⚠` a person does it — and nothing records it

| Artifact | What it actually is | Written by | Signed by | Lives at | Feeds |
|----------|---------------------|------------|-----------|----------|-------|
| ▪ `constitution.md` | The project's identity: mission, three outcomes, the one metric, principles, decision authority — short enough that the sponsor actually reads it | `/sdlc-coach` drafts (Step 5) | **Sponsor** | `.sdlc/artifacts/00-discovery/` | Every later phase; the auto-proof rule gates Phase 2 |
| ▪ `problem-statement.md` | Root cause and quantified impact in the sponsor's language — human-authored framing, never invented by Claude | Claude drafts from human notes; Pod Lead owns | Pod Lead | `.sdlc/artifacts/00-discovery/` | Phase 1 requirements |
| ▪ `success-criteria.md` | Every criterion with baseline, target, method, source; the baseline read live on day 6, not promised | Claude drafts (Step 3); QE vets | Pod Lead + QE | `.sdlc/artifacts/00-discovery/` | Phase 1; Phase 9 monitoring |
| ▪ `constraints.md` | Each constraint with a rationale and a fixed/negotiable flag (C-01…C-09) | Claude drafts (Step 4); Pod Lead completes | Pod Lead | `.sdlc/artifacts/00-discovery/` | Phase 2 design |
| ▪ `phase1-handoff.md` | Summary, decisions, numbered open questions with owners, risks, recommended starting point | Claude drafts (Step 6); Pod Lead completes | Pod Lead | `.sdlc/artifacts/00-discovery/` | Phase 1, directly |
| ▪ `contradiction-list.md` + `question-list.md` | Every place the documents disagree (CON-NN) and every unanswered question (Q-NN), each with a severity, a route, and a resolution log | `discovery-analyst` (Step 0d) | Pod Lead | `.sdlc/artifacts/00-discovery/` | The workshop; open Q-NN into Phase 1 |
| ▪ intake catalog | Every client document with a stable DOC-NNN id, a token-budgeted summary, and a locked index | `intake_documents.py` (Step 0c) + Claude | Setup Owner | `.sdlc/context/intake/` | Requirements traceability (DOC-NNN) |
| ▪ `phase00-report.html` + `phase00-visual.html` | The gate result and inventory, and the sponsor's narrative companion — self-contained HTML | `generate_phase_report.py` / `/sdlc-enhance` (Steps 7–8) | — | `.sdlc/reports/` | The day-10 sign-off |
| ⚠ PO decision record | The PO mode chosen in writing: a named PO with committed hours, or a signed proxy rider. An SOW precondition with billing teeth | **A human; the sponsor** | Sponsor | no path — folded into the constitution, no file | Phase 1's decision-list clock |
| ⚠ tooling record | Access live under the client's account, or a fallback rider signed with a date. The other precondition with billing teeth | **Setup Owner** | Setup Owner | no path — folded into constraint C-06 | The exit gate |
| ⚠ workshop brief | Questions only — curated by a human, edited, and distributed by a human; never drafts outcomes, metrics, or solutions | **A human, from Claude's draft** | Pod Lead | no path — curated & sent, never committed | The day-3 workshop |

> ⚠ **The gap — read the amber rows again:** Three of the eleven things Phase 0 is meant to produce
> have nowhere to live. The workshop brief — the artifact the plugin itself calls *curated, not
> generated* — is sent to the client and never committed. The two records this standard asks a human
> to sign, the PO decision and the tooling status, survive only folded into other files. **Human
> work is not the problem. Human work without a receipt is.**

Deliberately **not** produced in Phase 0: requirements, user stories, architecture options,
technology selections, or any code beyond the empty repo scaffold. Each has its own phase; each
done early is rework.

## Reading the documents against each other

This is the signature work of Phase 0: not summarizing the pile, but reading it *against itself*.
Harbor handed over eight documents, written by different people at different times. The
`discovery-analyst` agent found four contradictions — each a decision nobody realized they had to
make, surfaced while it was still cheap. Harbor's four answers to the phase's four questions:
renewal churn, measured as FNOL-to-coverage-decision (11.4 today); Luis Ortega, 6 hrs/week;
Azure-only with PII in Harbor's tenant; and a once-a-night core that stays, with a
15-business-day acknowledgment clock in two states.

The document registry — produced day 2 by document intake. Locked 2026-03-03: 8 documents,
~96,000 estimated tokens; file types pdf (5), docx (1), md (2).

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

### The four contradictions

Produced day 2 by the `discovery-analyst` agent; resolutions recorded at the day-3 workshop.

#### CON-01 — Real-time adjudication vs. the nightly batch window

Type: assumption · Severity: blocks-outcome

> **DOC-001 section 3.2:** "The solution shall provide real-time adjudication for eligible claims
> at the point of first notice of loss."

> **DOC-002 section 4.1:** "Policy and coverage records are synchronized to downstream systems via
> the nightly batch cycle (21:00–04:30); intraday reads reflect the prior business day."

**Why it matters:** The RFP's headline requirement is impossible against the current core system.
Either "real-time" gets redefined, or the engagement includes a PolicyOne read-path nobody has
scoped or priced.

**The question for the room:** Is a same-business-day coverage decision acceptable for v1, or is
true real-time a hard requirement worth the integration cost?

> **Resolution (Karen Voss, 2026-03-04):** Same-business-day accepted for v1; true real-time
> deferred to the auto-claims phase.

#### CON-02 — v1 scope: property only, or property and auto?

Type: scope · Severity: blocks-outcome

> **DOC-001 section 2.1:** "This procurement covers the property claims intake and triage process."

> **DOC-008 slide 9:** "Unified intake across property and auto books by FY2027 — single platform,
> single queue."

**Why it matters:** Scope determines volume targets, data model, and timeline. Designing for
property-only and discovering auto in month four is the 2024 failure replayed.

**The question for the room:** Is v1 property-only, and if so, what must the design not preclude
for auto?

> **Resolution (Karen Voss, 2026-03-04):** v1 is property-only; the claim data model and queue
> design must not preclude adding the auto book — gated at Phase 2 design review.

#### CON-03 — Annual claim volume: 38,000 or 60,000?

Type: fact · Severity: shapes-design

> **DOC-005 p.3:** "Property claims received FY2025: 38,142."

> **DOC-001 section 1.4:** "Harbor processes approximately 60,000 claims annually."

**Why it matters:** Sizing, load assumptions, and fast-path eligibility analysis all key off
volume. A 60% disagreement is not a rounding error.

**The question for the room:** Which number is the design target, and what does 60,000 include?

> **Resolution (Priti Shah, 2026-03-04):** 60,000 includes the auto book; property design target is
> 40,000/yr with 25% headroom.

#### CON-04 — What "cycle time" means

Type: terminology · Severity: shapes-design

> **DOC-005 p.2:** "Median cycle time (FNOL to first indemnity payment): 11.4 days."

> **DOC-008 slide 4:** "Target: claims cycle time (FNOL to coverage decision) under 3 days by 2027."

**Why it matters:** The engagement's success metric is unusable until one definition wins — the
two definitions can move in opposite directions.

**The question for the room:** Which definition does the success metric use?

> **Resolution (Priti Shah, 2026-03-04; verified at the 2026-03-09 metric session):** FNOL to
> coverage decision. The 11.4-day baseline was confirmed to be FNOL-to-decision in the underlying
> CR-204 query despite the DOC-005 caption (caption error flagged to BI).

### The full question list

Produced day 2; 6 routed to the workshop, 3 emailed pre-workshop, 3 to the day-5 interviews, 2
still open at phase exit and carried to Phase 1.

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

The three pre-workshop questions went out by email day 2 — and all three came back the same day
(Q-05, Q-07, Q-12).

## The success metric

A target with no readable baseline is a wish. On day 6 the pod sat with Priti and ran report
CR-204 live — the 11.4-day baseline was read off the screen and recorded with its source. The
criteria were drafted day 4; baselines verified live at the day-6 metric session.

**11.4 → ≤ 5.0** — days from FNOL to coverage decision today → the target within twelve months of
go-live.

**Primary — the one metric:** median days from FNOL to coverage decision, property claims.

| Field | Value |
|-------|-------|
| Definition | FNOL timestamp to coverage-decision timestamp, median, property book, reopened claims excluded (Q-05); definition fixed by CON-04 |
| Baseline | **11.4 days** (FY2025) — read live with the data owner on 2026-03-09 |
| Source system | Report CR-204, ClaimsCenter BI; weekly batch, on-demand capable |
| Target | ≤ 5.0 days median within 12 months of go-live |
| Stretch / partial / failure | ≤ 3.0 days · **Partial success:** ≤ 7.0 (clears the churn threshold) · **Failure:** no meaningful movement |

Secondary: **S1** regulatory acknowledgment compliance (baseline 96.2% → target 100%); **S2**
adjuster touches per claim (baseline 7.3 → target ≤ 4.0). Explicitly *not* success metrics:
features shipped, PR (pull request) counts, story points, agent productivity figures.

Instrumentation debt carried to Phase 1: S1's read is quarterly and manual today (automating it is
Phase 1 scope); Q-14 blocks fast-path target-setting.

> ⚠ **The gap — the caption-vs-query catch:** A surprise at the live run: report CR-204's caption
> said "to first payment," but the underlying query measured to coverage decision — the caption was
> wrong, the query was right. Flagged to Harbor BI. You only see that by actually running the
> report. The pod's Quality Engineer then vetted all three criteria for measurability.

## The documents a human authored

Two Phase 0 artifacts are never Claude's to own. The **workshop brief** is curated by a human and
carries questions only — the plugin forbids drafting an outcome into it. The **problem statement**
is human-authored framing: Claude drafts from human notes, but what the project is *for* is a
human's to write. Both are reproduced in full below.

### The workshop brief, in full

Drafted day 2 via `/sdlc-brief`, curated by Maya at its HITL gate, sent by Maya. The one page, as
sent:

> **Workshop Brief — Harbor Mutual Outcome Workshop**
>
> Wednesday 2026-03-04, 9:00–12:00, Harbor HQ room 4B · runs 3 hours
> Attendees: Karen Voss (VP Claims Ops, sponsor), Luis Ortega (Claims PM), Priti Shah (BI), Dan
> Kowalski (IT Security), Gail Tran (senior adjuster), Dee Alvarez (intake supervisor)
> Facilitator: Maya Chen · Pre-reading: this page only
>
> **What we read.** 8 documents provided by your team. The load-bearing three: DOC-001 (the
> modernization RFP), DOC-002 (PolicyOne architecture), DOC-005 (Q4 2025 claims ops report).
>
> **What the documents say.**
> - Median property-claim cycle time is 11.4 days; an average claim is touched 7.3 times (DOC-005)
> - FNOL arrives by phone (55%), portal (30%), and email (15%) (DOC-003)
> - Policy data syncs on a nightly batch; intraday reads show yesterday (DOC-002 section 4.1)
> - A 2024 modernization attempt was cancelled in month six (DOC-004)
>
> **Where the documents disagree.**
> 1. DOC-001 section 3.2 requires real-time adjudication; DOC-002 section 4.1 says the nightly batch
>    makes intraday policy reads stale. *Is same-business-day acceptable for v1?* (CON-01)
> 2. DOC-001 scopes property; DOC-008 plans property + auto by 2027. *Is v1 property-only, and what
>    must the design not preclude?* (CON-02)
> 3. 38,142 claims/yr (DOC-005) vs ~60,000 (DOC-001). *Which is the design target?* (CON-03)
> 4. Cycle time to first payment (DOC-005) vs to coverage decision (DOC-008). *Which definition does
>    the success metric use?* (CON-04)
>
> **What nobody has written down.** Problem: who is hurt most — policyholders or the claims team?
> (Q-01) What killed the 2024 attempt? (Q-02) Outcomes: should Harbor's engineers run this model
> after we leave? (Q-03) Constraints: is the PolicyOne retirement funded? (Q-06) Ownership: can
> Harbor commit a named PO at ~4-6 hrs/week? (Q-09) Tooling: who owns Anthropic onboarding? (Q-10)
>
> **Decisions we need from the room.** 1. The one success metric — definition and source system. 2.
> v1 scope. 3. Real-time vs same-business-day. 4. The PO commitment.
>
> **Agenda.** The problem in your words (45) · the three outcomes (45) · the one metric (30) ·
> constraints (30) · product ownership (20) · tooling status (10).

Questions only — the brief never proposes an outcome. Every framing appears as an attributed claim
with a DOC reference. That is the plugin's HITL rule made visible.

### The problem statement, in full

Drafted day 4 from workshop notes; reframed day 5 at the sponsor checkpoint; signed day 10.

**The problem.** Property policyholders wait a median of 11.4 days from first notice of loss to a
coverage decision. Claimants who wait more than 7 days renew at a rate 2.1 points lower — on
Harbor's property book, approximately $3.4M in annual premium. The cost of the delay is paid at
renewal time, by retention, not primarily in claims-department overtime. (That framing is the
sponsor's, corrected at the day-5 checkpoint: the corpus framed this as adjuster efficiency; Karen
Voss reframed it as retention. Efficiency improves as a consequence, not as the goal.)

**Observable symptoms.** Median FNOL-to-decision 11.4 days (CR-204, verified live 3/9); 7.3
touches by 5 people per average claim; email FNOL (15% of volume) lands in a shared Outlook inbox
triaged manually twice a day with no SLA; portal FNOL re-keyed into PolicyOne by hand; intraday
policy reads show yesterday because of the nightly batch — a built-in extra day on every same-day
claim.

**Who is affected.** Policyholders at the worst moment of their relationship with Harbor; 64
property adjusters spending touches on coordination instead of decisions; the 9-person intake
team; Harbor's renewal book, where the cost actually lands.

**Why now.** The 2024 attempt failed (no internal owner, late integration scope), the 2027
strategy depends on a working property platform to extend to auto, and Q4 2026 is the first
renewal season a fixed cycle time could protect.

**Root cause.** Five-whys (asking "why" repeatedly until the answers stop changing) converges on
two causes: (1) no single queue — three FNOL channels with three intake mechanics and no shared
prioritization; (2) coverage verification blocked on a nightly batch. Everything else is
downstream of those two.

## The constitution the sponsor signs

The constitution is the project's identity in one short document: what it is, what "done" means,
the metric, the principles, and who decides — kept short enough that the sponsor actually reads
it. The PO decision (Luis Ortega, 6 hrs/week, 2-business-day turnaround) and the tooling status
live inside it, since the plugin gives them no file of their own.

Drafted day 7; signed by the sponsor at the day-10 phase review.

**Identity.** Harbor Claims Intake — a unified property-claims intake and triage system replacing
three disconnected FNOL channels with one queue and same-business-day coverage decisions,
integrated with PolicyOne. Project type: service.

**Mission.** Get property policyholders a coverage decision in days, not weeks, so that a claim
becomes a reason to renew instead of a reason to leave.

**The three outcomes.** Business: median FNOL-to-decision ≤ 5 days (from 11.4), protecting renewal
retention. Software: one intake system across phone, portal, email; a single prioritized queue;
fast-path triage for simple claims; PolicyOne integration that lives with the batch window.
Capability: four named Harbor engineers run this delivery model independently by engagement close.

**Governing principles.** (1) Retention is the frame — when efficiency and claimant experience
conflict, claimant experience wins. (2) The batch window is real — v1 designs with it, not around
an unfunded retirement. (3) Property-only, auto-proof — checked at every design gate. (4)
Regulatory clocks are acceptance criteria, tested not remembered. (5) No PII in model context
outside the approved Azure path.

**Decision authority.** Outcome, budget, phase sign-off: Karen Voss. Product decisions and
decision-list answers (2-business-day turnaround): Luis Ortega. ADRs (architecture decision
records): pod Setup Owner, co-signed by Harbor's lead engineer from Phase 2. Security and data
boundary: Dan Kowalski. Scope changes: Karen, on Luis's recommendation.

### The constraints

Drafted day 4; signed day 10. C-06 is where the tooling record lives; C-06 and the decision
authority above are where the standard's two signed records survive.

| # | Constraint | Fixed / Negotiable | Source |
|---|-----------|--------------------|--------|
| C-01 | Azure is the only approved cloud | Fixed | DOC-006 section 2; Q-07 |
| C-02 | PolicyOne stays; the nightly batch window is a hard integration boundary for v1 | Fixed | Q-06; CON-01 |
| C-03 | v1 property-only; design must not preclude the auto book | Fixed | CON-02; gated at Phase 2 |
| C-04 | 15-business-day acknowledgment in two regulated states | Fixed | Q-08 — becomes acceptance criteria and test cases |
| C-05 | Claim documents and PII stay in the Harbor tenant; no PII in model context outside the approved Azure path | Fixed | Q-12 |
| C-06 | Anthropic access under Harbor's agreement; keys in Harbor Key Vault | Fixed | Signed 3/11 |
| C-07 | Fixed fee per phase; gates are the billing milestones | Fixed | SOW (statement of work) |
| C-08 | Go-live before the Q4 2026 renewal season (Oct 1) | Negotiable | Karen prefers scope cuts over date slips, in that order |
| C-09 | Design target 40,000 property claims/yr including headroom | Negotiable | CON-03; revisit after Q-14 |

## What Phase 1 receives

A phase ends by handing the next one a package, not a feeling. Everything below crosses the
boundary into Requirements: the signed identity and constraints, the proven metric, and the two
questions still open — carried forward under their original IDs, never silently dropped. Drafted
day 9; the phase closed day 10 (billing milestone 1).

**Crosses into Phase 1:** `constitution.md` · `problem-statement.md` · `success-criteria.md` ·
`constraints.md` · `phase1-handoff.md` · `contradiction-list.md` + `question-list.md` · intake
catalog (DOC-NNN) · ⚠ PO decision record · ⚠ tooling record.

### The Phase 1 handoff (summary)

**Key findings.** The business problem is renewal churn, not adjuster overtime. Two root causes:
no single queue, and verification blocked on the nightly batch. v1 property-only (40k/yr target),
auto-proof. Same-business-day accepted; real-time deferred. Two regulated states impose a
15-business-day acknowledgment clock. The 2024 attempt failed on ownership and late integration
scope — the PO commitment and the Phase 3 walking skeleton (the thinnest end-to-end slice of the
system, built first to prove the architecture works in practice) are the direct countermeasures.
Harbor wants the capability outcome: four engineers trained.

**Open questions for Phase 1.**

| ID | Question | Owner | Due |
|----|----------|-------|-----|
| Q-13 | Do the two states' acknowledgment rules apply differently to the portal channel? | Luis Ortega | Phase 1, week 1 |
| Q-14 | What share of property claims is "simple" and fast-path eligible? | Priti Shah | Phase 1, week 1 |

**Risks carried forward.** PolicyOne integration surprises (killed the 2024 attempt; DOC-007's API
inventory is dated 2023 — Phase 2 design spike, a short timeboxed technical investigation, against
the live inventory before any contract is drawn). CR-204 caption/definition drift (BI fix
confirmed before the metric goes on the steering scorecard). Email-channel mechanics undocumented
(Phase 1 interviews the intake team, not just the supervisor). Renewal-season deadline pressure
(scope cuts decided at steering, never silently in the flow).

**Recommended Phase 1 starting point.** Start requirements with the single queue (channel
unification), not the fast-path: the queue is the prerequisite for everything, and the email
channel is the least understood. Fast-path requirements wait on Q-14's segmentation.

### The gate run and the sign-off

**Day 9 — the check.** `/sdlc-gate` ran the completeness check: one failure — a leftover
placeholder in the constraints file — which the `gate-repair` agent fixed (structural repair
only), and the gate re-ran clean. `/sdlc-enhance` generated the narrative companion for Karen;
`/sdlc-phase-report` rendered the stakeholder HTML report.

**Day 10 — sign-off.** Karen signs the outcome statement. The advance is approved and recorded
with `/sdlc-next`, which re-verifies the gates and moves the engagement state to Phase 1.
**Billing milestone 1.**

All names, numbers, and documents are invented but internally consistent — the 11.4-day baseline,
the CR-204 report, and the open question IDs trace through every artifact on this page.

## The tooling behind this phase

The abstract Phase 0 page describes this work generically. In practice, the engagement ran on the
**claude-code-sdlc** plugin. What produced what:

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
