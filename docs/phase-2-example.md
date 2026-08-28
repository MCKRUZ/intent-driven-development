# Phase 2 Worked Example: Harbor Mutual

The continuation of [the Phase 1 example](phase-1-example.md), companion to
[the Phase 2 deep-dive](phase-2-design.md). Phase 1 closed Friday 2026-03-20 with a signed
requirements baseline, two open questions (Q-15, Q-16), and a recommendation: start design at
the claim data model, where three constraints converge.

This page mirrors the Example track of the Phase 2 companion: what Design received, the
procedure day by day, the artifact ledger it produced, the real documents, and what crosses
into Phase 3. One person joins the story — **Wes Carter**, Harbor's lead engineer — the design
counterpart who co-signs every ADR and, at close, becomes Harbor's Setup Owner.

## What Phase 2 received

Harbor Mutual — a fictional regional insurer — hired a five-person pod to rebuild how
property-insurance claims get reported and decided. A claim takes a median of **11.4 days** from
FNOL (first notice of loss — the policyholder reporting the damage) to a coverage decision; the
target is **5 days or less**. Phase 1 closed Friday 2026-03-20. Design does not start from a
blank page — it starts from these files, on disk, in the client's own repository.

**Inherited from Phase 1** — read by `synthesize_spec.py` into one design brief:

- `phase2-handoff.md`
- `requirements.md`
- `non-functional-requirements.md`
- `epics.md`
- `constraints.md`

**The four design drivers, and the two unknowns.** Most of a requirements baseline doesn't
shape architecture. Four things here do — and two of them are still questions, which is why
they're due this week.

- **PolicyOne & the replica.** Policy data lives in an aging core that syncs only once a night;
  Phase 1 found a read-only nightly **snapshot replica**, queryable in milliseconds. Whether
  security allows reading it is open question **Q-15**.
- **Storm season.** Catastrophe events spike claim volume ~10x for about a week (NFR-02). The
  exact surge profile is **Q-16**.
- **The fast path.** 61% of claims are simple (single dwelling, no injury, under $25k) and get a
  recommend-then-one-click-confirm decision (D-09).
- **Auto-proof.** The data design must not preclude Harbor's auto-insurance business later
  (C-03); v1 ships property only.

Those four drivers converge on one place — the claim data model — which is why Phase 1's handoff
recommended starting design there. Everything decided this week is either a consequence of them
or a bet being tested against them. **Wes Carter is the one to watch:** Harbor's lead engineer
co-signs every decision record next to Rob's name. At close, the harness hands to someone who
*chose* this architecture, not someone it happened to.

> **Carried in from Phase 1, still unanswered on Monday:** Q-15 — may we read the replica
> directly? (Dan) · Q-16 — what does the surge actually look like? (Priti)

**Our pod:**

- **Maya Chen** — Pod Lead
- **Rob Feld** — Setup Owner (the design authority; signs every ADR)
- **Jonah Kim** — Orchestrator / Checker (runs the replica spike)
- **Sara Whitfield** — Orchestrator / Checker (runs the email-extraction spike)
- **Nadia Brooks** — Quality Engineer (owns the proving plan)

**Harbor Mutual:**

- **Karen Voss** — VP Claims Operations (sponsor; approves the advance)
- **Wes Carter** — Lead engineer (co-signs every ADR; becomes Setup Owner at close)
- **Luis Ortega** — Product owner (decides product trade-offs on a 2-day clock)
- **Dan Kowalski** — IT security (answers Q-15; runs the threat review)
- **Priti Shah** — Data & reporting (answers Q-16)

**The ID codes, decoded.** Every artifact in this engagement carries a stable identifier, so a
decision made in week two can still be traced in month nine.

| Prefix | Means | Born in | Example here |
|--------|-------|---------|--------------|
| `DOC-NNN` | A client document taken in at intake | Phase 0 | The 2023 API inventory that turned out to be wrong |
| `C-NN` | A constraint — a hard limit the design must honor | Phase 0 | C-02 nightly sync · C-03 auto-proof |
| `CON-NN` | A contradiction resolved in Phase 0 | Phase 0 | CON-01 same-business-day vs. the nightly sync — real-time deferred to the auto phase |
| `D-NN` | A decision the client's product owner owes us | Phase 0/1 | D-07 merge rule · D-09 fast path · D-12 retention |
| `Q-NN` | An open question with an owner and a due date | any | Q-15 replica access · Q-16 surge profile |
| `REQ-NNN` | A functional requirement | Phase 1 | REQ-014 same-business-day coverage status |
| `NFR-NN` | A non-functional requirement — a quality target | Phase 1 | NFR-02 the 10x surge |
| `AQ-NN` | An architectural question Design must answer | Phase 1 handoff | The four that become ADR-001–004 |
| `ADR-NNN` | An architecture decision record — a signed choice | Phase 2 | ADR-001 coverage verification source |

The plugin's Phase 2 begins by reading every `AQ-NN` out of `phase2-handoff.md`. An
architectural question with no ADR at the end of the week is a gate failure — that's the thread
tying Phase 1's homework to Phase 2's output.

## The procedure, step by step

Phase 2 is ten numbered steps in `claude-code-sdlc` and five working days in this standard. They
are the same week seen twice. Below, they're braided: what the tool runs, what the humans do
that the tool cannot, and the file each step leaves behind. Each step shows a **Tooling** line
(the command, or *none — humans in a room*) and an **Artifacts out** line; `> **At Harbor:**`
carries the worked example, and `> ⚠ **The gap:**` marks the work the plugin never records.

### Day 1 — Mon 3/23 · plugin Step 0 opens — Pull the architectural questions; put real options on the table

**Tooling —** `/sdlc-next` → Step 0 HITL gate (human decision).
**Artifacts out —** AQ decisions — made by humans; recorded as ADRs on day 3.

Claude reads `phase2-handoff.md` and extracts every `AQ-NN` Phase 1 left for Design. For each
one it presents two to three concrete options with honest costs. This is a **blocking human
gate** in the plugin: *collect human decisions for all AQs before writing any artifact.* Claude
encodes decisions; it does not invent them. The pod also brings its own day-1 craft, which no
command performs: reading the baseline for the five-to-eight requirements that actually shape
architecture, and killing the strawman options before a human ever sees them. Two Phase 1
questions come due today, because their answers are design inputs.

> **At Harbor:** Drivers extracted — C-02 batch window, NFR-02 surge, C-03 auto-proof, C-04
> regulatory clock, C-05 PII-in-tenant, D-07 merge rule. Both open questions land. **Q-15**
> (Dan): replica read approved under controls. **Q-16** (Priti): the surge is real — peak 1,710
> claims on day 2, nine elevated days. Claude presents three options for each of four decisions;
> Rob kills one strawman per set and books the option session for tomorrow.

### Day 2 — Tue 3/24 · the option session · no command runs — Test the risky bets against the real thing, then let humans choose

**Tooling —** *none — exploratory coding on a throwaway branch, then humans in a room.*
**Artifacts out —** `spike-findings.md` (the method requires it; no command writes it); four
decisions, made and owned.

Before anyone commits to an option, the assumptions underneath it get tested. Orchestrators run
**spikes**: throwaway code, hours-boxed, on branches that get deleted, pointed at the client's
live systems rather than the client's documentation. Then the option session — 90 to 120
minutes, the Setup Owner and the client's engineer, spike results in hand — and they choose.
This closes the plugin's Step 0 gate.

> ⚠ **The gap:** Phase 2's exit gate says *"every external integration the design depends on was
> spiked against the live system."* The word "spike" appears in no file in `claude-code-sdlc`.
> Nothing prompts you to run one, and nothing checks that you did. This is human work that
> currently leaves no receipt — and it is exactly the work that saved Harbor a 2 a.m. incident
> in month four.

> **At Harbor:** Jonah's spike — the replica answers in **180ms at the 95th percentile** — and
> is **unavailable 02:00–04:30 nightly** during its refresh. No document mentioned that. Sara's
> spike — LLM email-field extraction hits **88%** on 50 redacted samples — promising, below
> target, and exactly the number ADR-004's confidence-threshold design needs. In the option
> session Rob and Wes choose all four decisions. One product-facing trade-off — what the portal
> shows users during surge degradation — splits off to Luis on the 2-business-day clock.

### Day 3 — Wed 3/25 · plugin Steps 1–6 — The machine runs; decisions become signed records

**Tooling —** `synthesize_spec.py` → `planning/spec.md` · `/deep-plan` → `planning/claude-plan.md`
· `map_deep_plan_artifacts.py` · `/sdlc-coach` → ADRs · `/sdlc-experience` → the Design seat's
three artifacts, once the architecture is chosen.
**Artifacts out —** all under `.sdlc/artifacts/02-design/`: `design-doc.md`, `api-contracts.md`,
`adrs/ADR-001…004.md`, `adr-registry.md`, `phase3-handoff.md`, `research-notes.md`,
`integration-notes.md`, `deep-plan-checkpoint.yaml`; and under `experience/`: `user-journey.md`,
`surface-layout.md`, `channel-interaction-spec.md`.

With every architectural question answered, the tool is finally allowed to write. Six steps fire
in sequence: synthesize the design brief, run the planner, map its output into the engagement's
artifact directory, write the ADRs from yesterday's human decisions, fill the gaps in the
generated skeletons, and define the data model. **An unsigned record is just a conversation.**
Claude drafts each ADR against the template; the Setup Owner edits; the Setup Owner *and* the
client's counterpart both sign. Two names, or it isn't a decision.

> **At Harbor:** Four ADRs drafted, edited by Rob, signed by Rob and Wes, dated 2026-03-25. The
> claim data model gets drafted where the constraints converge. Running the forward-compatibility
> check against C-03 (auto-proof) forces exactly one structural change: claim type moves from a
> code-level enum to a **reference table** with an extensible coverage schema. Adding the auto
> book later becomes a data change, not a schema migration. Door open; room unfurnished.

> **At Harbor — the Design seat.** The adjuster console is a customer surface, so it gets the
> Design seat, and it gets it *today*, after ADR-001 and ADR-002 — the layout of a queue depends
> on what the store and the verification service can answer. `/sdlc-experience` reads the
> feature's channel — a screen — routes to the visual designer, and interviews Rob and Luis. The
> **user journey** carries the path nobody draws unprompted: the abandon path when the replica
> is stale. An adjuster opens a claim whose coverage reads `pending-verification` and cannot
> decide it; the journey says what happens instead of a dead end — the as-of timestamp and the
> state shown in words, the claim parked back to the queue with a reason, no one-click confirm
> on last night's data. The **surface layout** is the queue and the claim detail, as screens.
> The **interaction contract** is the console's event contract, co-authored with Engineering —
> Jonah and Wes at the same table — because for a screen the interaction contract *is* the API
> the screen speaks. Wes co-signs it. Luis signs the journey.

### Day 4 — Thu 3/26 · plugin Step 7 · plus the threat review — Pin the edges, walk the attack surface, plan the proof

**Tooling —** `/sdlc-coach` → contracts · `/sdlc-data` → the Data seat's three artifacts,
alongside the contracts · `/visual-explainer` → `.sdlc/reports/architecture-diagrams.html` ·
threat review — a human session; Claude drafts the data flows and the candidate list.
**Artifacts out —** `data/data-contract.md`, `data/data-readiness.md`, `data/lineage-audit.md`;
`architecture-diagrams.html`; `threat-model.md` + mitigation map; `nfr-proving-plan.md`;
`walking-skeleton.md`.

The API contracts get completed — not just what success looks like, but every failure path and
every degradation behavior, flowed down from the Phase 1 error specs. The tool renders the
architecture as five diagrams, one of which is a **trust-boundary diagram**. Then the humans
attack it: a security session walks each data flow and assigns every threat — mitigate it in the
design now, or guard it with a build-time gate later.

> **At Harbor:** REQ-014's error spec becomes contract behavior: policy not found returns
> `needs-review` with a reason code, never a silent "verified"; the replica's refresh window
> returns `pending-verification` and **intake never blocks**. The threat review with Dan finds
> **9 threats: 7 mitigated in the design, 2 handed forward as build-time security gates** —
> malware scanning on document upload, and a PII template-review gate on acknowledgment letters,
> because that data leaves the system on paper. Nadia writes how each NFR will be proven and
> where its number will be read. Steering with Karen surfaces document retention, which becomes
> D-12.

> **At Harbor — the Data seat.** A claim is personal data from its first field, so alongside the
> contracts the Data seat runs. `/sdlc-data` interviews Priti and Wes and drafts the **claims
> data contract**: claimant name, policy number, property address, loss description, photos,
> loss date, claim type, channel, the as-of timestamp — each with its source and type, and each
> with a **PII column**. Claude proposes the classification; **Dan confirms it**, field by
> field, because PII is a risk-tier driver: any spec that touches a classified field is HIGH
> before it is written. The **readiness assessment** flags the gap everybody already half-knew:
> the nightly snapshot replica is absent during its refresh window and only ever as fresh as
> last night, so a coverage answer is not always *there* to read. Flagged, not blocked — it goes
> on the decision list under Priti's name on the 2-business-day clock, where steering sees it.
> The **lineage audit** follows a claim from the intake form (portal, phone, email — each
> through its adapter) → the intake API → the replica verification read → the adjuster queue,
> with D-12's seven-year retention on the record and two audit points: the append-only event
> log (NFR-07) and the audited replica read (the Q-15 controls).

### Day 5 — Fri 3/27 · plugin Steps 8–9 · the gate — Fresh eyes attack it, the gate reports, a human decides

**Tooling —** `/sdlc-review --all` · `/sdlc-gate` → `check_gates.py` · `/sdlc-phase-report` →
`generate_phase_report.py` · `/sdlc-next` → `advance_phase.py --confirmed`.
**Artifacts out —** `.sdlc/reports/phase02-report.html`; `consistency-check.md`; the sponsor's
signature — billing milestone 3.

A reviewer that did not draft the design challenges it from four angles. The consistency check
runs both directions — every top-tier requirement lands in a design element, every design
element traces back to a requirement. Then the gate runs, generates a report for the
stakeholders, and stops. `advance_phase.py` will not move the engagement forward without
`--confirmed`: a named human's sign-off.

> ⚠ **The gap:** `check_gates.py` verifies that five files exist, are non-empty, and contain no
> placeholder text. It never reads the twelve-bullet exit-gate checklist the standard names —
> that list lives in `phase-registry.yaml`, and no code opens it. The human is stopped at the
> gate and asked to sign; the checklist they should be signing against is never put in front of
> them. *The human gate is real. What it asks is not.*

> **At Harbor:** Three review findings survive Rob's triage. **HIGH:** no back-pressure behavior
> defined for surge — the contract gains an explicit degraded-acceptance mode. **MEDIUM:** the
> staleness flag isn't wired to fast-path escalation — fixed, traced to REQ-019. **MEDIUM:** a
> notification-preferences service that no requirement asked for had crept into the component
> diagram — **cut**. Accidental scope dies in design, not in build. Consistency check clean
> after the cut. Rob and Wes walk the ADRs, Luis confirms the product trade-offs, Karen approves
> — and the advance records, beside her signature, the discipline sign-offs by name: Dan on the
> PII column, Wes on the interaction contract, Luis on the journey.

## What Phase 2 produced

The design phase's whole output, named. Blue rows are written by a command and checked by the
gate. **Amber rows are the method's human work** — required by this standard, produced by no
tool, and today leaving no file behind. Those are the rows to argue about.

State marker key:

- `▪` a command does it — and writes the file
- `▸` a person does it — and it is recorded
- `⚠` a person does it — and nothing records it

| Artifact | What it actually is | Written by | Signed by | Lives at | Feeds |
|----------|---------------------|------------|-----------|----------|-------|
| ▪ `design-doc.md` | The shape of the system: components, boundaries, data flow, deployment view. Navigation for the ADRs — short enough to be read, not a novel | `/deep-plan` drafts; Setup Owner enriches | Setup Owner | `.sdlc/artifacts/02-design/` | Phase 3 skeleton |
| ▪ `adrs/ADR-NNN.md` | One decision each: context, 2–3 options genuinely considered, the choice, the consequences including the unpleasant ones | Claude drafts from the Step 0 human decisions | **Setup Owner + client counterpart — both** | `.sdlc/artifacts/02-design/adrs/` | Phase 3 build; every later argument |
| ▪ `adr-registry.md` | The index of every ADR with its status — active, superseded, proposed | `/sdlc-coach` | Setup Owner | `.sdlc/artifacts/02-design/` | Close — the decision history Harbor inherits |
| ▪ `api-contracts.md` | Every operation: request and response shapes, auth, error semantics, degradation behavior per dependency failure. A contract that only describes success is half a contract | `/deep-plan` drafts; Setup Owner completes | Setup Owner | `.sdlc/artifacts/02-design/` | Phase 3 specs |
| ▪ `data/data-contract.md` *(conditional — the feature touches personal data)* | Every field the feature reads or writes, with source, type, and an explicit PII column. The column is what a named human confirms, because PII drives the risk tier | `/sdlc-data` — the Data seat, interview-driven | **Dan Kowalski** (the PII column), recorded at the advance | `.sdlc/artifacts/02-design/data/` | Every dependent spec's tier; Build triage |
| ▪ `data/data-readiness.md` *(conditional)* | Is the data actually there, complete, and trustworthy — advisory; each gap becomes a decision-list item with an owner and a clock, never a block | `/sdlc-data` | Setup Owner | `.sdlc/artifacts/02-design/data/` | The decision list; steering |
| ▪ `data/lineage-audit.md` *(conditional)* | Source → transform → sink, with retention and the audit points | `/sdlc-data` | Setup Owner + client security | `.sdlc/artifacts/02-design/data/` | The threat review; Phase 9's compliance sample |
| ▪ `experience/user-journey.md` *(conditional — the feature has a customer surface)* | The adjuster's path through the console, including the abandon path when the replica is stale | `/sdlc-experience` — the Design seat, via the visual designer | **Luis Ortega** | `.sdlc/artifacts/02-design/experience/` | The console specs' acceptance checks |
| ▪ `experience/surface-layout.md` *(conditional)* | The queue and the claim detail as screens — drafted after ADR-001 and ADR-002, because the layout depends on them | `/sdlc-experience` | Setup Owner | `.sdlc/artifacts/02-design/experience/` | Build specs for the console |
| ▪ `experience/channel-interaction-spec.md` *(conditional)* | The console's event contract: each screen-channel dimension → a concrete contract → the acceptance check it becomes | `/sdlc-experience`, co-authored with Engineering | **Wes Carter** co-signs — it is an API | `.sdlc/artifacts/02-design/experience/` | `/sdlc-channel` at Intent — spec 0015's checks |
| ▪ `phase3-handoff.md` | Decisions, contracts, section breakdown, implementation order, build risks, open questions under their original IDs | `map_deep_plan_artifacts.py` drafts; Pod Lead completes | Pod Lead | `.sdlc/artifacts/02-design/` | Phase 3, directly |
| ▪ `architecture-diagrams.html` | Five rendered diagrams — layers, request flow, data flow, section dependencies, and the trust boundary | `/visual-explainer` | — | `.sdlc/reports/` | Stakeholder review; the threat session |
| ▪ `research-notes.md` / `integration-notes.md` / `deep-plan-checkpoint.yaml` | The planner's working memory: what it researched, what it learned about the client's systems, and enough session state for Phase 3 to resume | `/deep-plan` | — | `.sdlc/artifacts/02-design/` | Phase 3 resumption |
| ▪ `phase02-report.html` | The gate result and artifact inventory, self-contained. This is the document a sponsor actually reads before signing | `generate_phase_report.py` | — | `.sdlc/reports/` | The manual sign-off gate |
| ⚠ spike findings | Each risky assumption confirmed or falsified against the live system, with evidence. The spike code is deleted; the finding is not | **A human, on a throwaway branch** | Setup Owner | no path — nothing writes it | The ADRs it should have informed |
| ⚠ threat model + mitigation map | Data flows reviewed; each threat either mitigated in the design or assigned as a build-time security gate | **Setup Owner + client security** | Both | no path — nothing writes it | Phase 3's risk-tier map |
| ⚠ NFR proving plan | Per quality target: the verification method, and the named place its number will be read | **Quality Engineer** | QE | no path — nothing writes it | Phase 9 monitoring |
| ⚠ walking-skeleton definition | The thin end-to-end slice Phase 3 must ship — named, bounded, and sufficient to exercise every ADR's chosen mechanism at least once | **Setup Owner + QE** | Setup Owner | no path — nothing writes it | Phase 3, day 6 |
| ⚠ consistency check record | Requirements traced against design in both directions; orphans resolved or removed | **Pod Lead** | Pod Lead | no path — nothing writes it | The exit gate |
| ⚠ data model | Serves every top-tier requirement; passes the forward-compatibility check; convergence constraints are structural, not bolted on | Plugin Step 6 — but into `design-doc.md`, not its own file | Setup Owner | folded into `design-doc.md` | Phase 3 schema |

> ⚠ **The gap:** Six of the twenty things Phase 2 is supposed to produce have nowhere to live.
> The threat review happens, and its output survives as a memory and a couple of GitHub labels.
> The spike that found Harbor's 02:00–04:30 refresh window leaves no artifact at all — the
> finding reaches the ADR only because Jonah was in the room on Wednesday. **Human work is not
> the problem. Human work without a receipt is.**

Deliberately **not** produced in Phase 2: production code, the spec backlog (Phase 3 and triage
own that), provisioned environments (Phase 3), UI visual design beyond what the product
trade-offs required, and estimates beyond the SOW's phase figures.

## Write down what you rejected, not just what you chose

Four architectural questions came in from Phase 1; four ADRs go out. Claude drafted them against
the template; Rob edited; **Rob and Wes both signed**, dated 2026-03-25. Each records the
rejected options *with their reasons* — the part that stops the argument coming back in month
three.

| ID | Decision | Chosen | Rejected (and why) |
|----|----------|--------|--------------------|
| ADR-001 | Coverage verification source | Read the PolicyOne nightly snapshot replica directly (per Q-15 controls) | Batch request queue (adds a day back — defeats the metric); building a real-time PolicyOne API (cost and risk unfunded for v1; deferred to the auto phase) |
| ADR-002 | Claim store shape | Relational model + append-only event log; auto-proof via line-of-business reference table and extensible coverage schema | Full event sourcing (unfunded gold-plating; team operability cost); document store (weak fit for the merge and audit rules) |
| ADR-003 | Surge handling | Buffered ingestion queue + autoscaling, load-tested at the Q-16 surge profile | Permanent overprovisioning (pays for the storm all year); serverless rearchitecture (foreign to Harbor's operating model — they run this at 2 a.m.) |
| ADR-004 | Email FNOL extraction | LLM extraction with per-field confidence thresholds; below-threshold fields route to the human triage view (REQ-009) | Deterministic template parser (insurer emails are too varied — Sara's spike); permanent manual triage (the no-SLA inbox is the problem being solved) |

### ADR-001 in full

Coverage verification reads the nightly snapshot replica. Status: accepted · Signed: Rob Feld
(pod), Wes Carter (Harbor) · 2026-03-25.

**Context.** REQ-014 promises same-business-day coverage status. PolicyOne syncs downstream
nightly (C-02, CON-01); the 2023 API inventory listed only batch interfaces, but the Phase 1
spike (Jonah, 3/19) found a read-only nightly snapshot replica, and security approved direct
read access under controls (Q-15).

**Options considered.**

1. **Read the snapshot replica directly.** Fresh-as-of-yesterday data in milliseconds. Requires
   the Q-15 controls and a staleness contract.
2. **Queue batch requests through the existing PolicyOne interface.** No new access path, but
   answers arrive next business day — re-adds the day the metric exists to remove.
3. **Build a real-time read API on PolicyOne.** True real-time, but mainframe-side work Harbor
   can't staff this year; CON-01 already deferred real-time to the auto phase.

**Decision.** Option 1. The replica read, behind a verification service that owns the staleness
contract.

**Consequences.**

- Every coverage answer carries an as-of timestamp; data older than 36 hours triggers the
  escalation path (REQ-014's error spec).
- The replica is unavailable 02:00–04:30 during refresh (Jonah's spike, 3/24): the service
  degrades to "pending verification" and intake is never blocked.
- Access runs under the Q-15 controls: read-only service account, private endpoint, audited.
- The unpleasant one: v1's accuracy ceiling is "as of last night." If Harbor later funds
  real-time, this service is the seam where it lands — the contract doesn't change, the source
  behind it does.

Wes's signature is the transfer event in miniature. Every ADR carries Harbor's own engineer's
name next to Rob's — at close, the harness hands to someone who chose this architecture, not
someone it happened to.

## A contract that only describes success is half a contract

An exhibit from `api-contracts.md` — the coverage-verification endpoint. REQ-014's error
specification flowed straight down into contract behavior: response codes, the staleness header,
and what the endpoint does when its dependency is simply gone. Every row below is a *failure*
case — the part the next person cannot guess and will otherwise invent.

| Condition | Response |
|-----------|----------|
| Policy found, data fresh | Coverage status + `as-of` timestamp |
| Policy not found | `needs-review` with reason code — never a silent "verified"; queue flag raised same business day |
| Replica in refresh window (02:00–04:30) or unreachable | `pending-verification`; queue entry shows the degradation; **intake never blocks** |
| Snapshot older than 36h | Status carries a staleness warning; written-acknowledgment-state claims escalate instead of auto-proceeding |
| Surge back-pressure (added by the day-5 review) | Portal acceptance never rejects a FNOL: accept, queue deeper, show the degraded-confirmation message Luis approved |

The surge back-pressure row was a day-5 review finding (HIGH): no back-pressure behavior was
defined for surge, so the contract gained an explicit degraded-acceptance mode.

## Every field, and whether it is a person

An exhibit from `data/data-contract.md` — the claims data contract, drafted by the Data seat on
day 4 alongside the API contracts. The column that matters is the third one. Claude proposed
every row; Dan confirmed the PII column field by field, and that confirmation — not the drafting
— is what sets the tier of every spec that later touches these fields.

| Field | Source | PII? | Why it matters |
|-------|--------|------|----------------|
| Claimant name | Intake form (any channel) | **Yes** | Names a person; shown on the claim detail, never in a queue row |
| Policy number | Intake form → replica lookup | **Yes** — customer-linked | Resolves to a household; the key the audited replica read is made on |
| Property address | Intake form; verified against the replica | **Yes** | A home; the acknowledgment letter carries it — the PII template-review gate exists for this |
| Loss description | Intake form; email extraction (ADR-004) | **Yes** — treat as such | Free text; policyholders write names, phone numbers, and neighbours into it |
| Photos | Portal upload | **Yes** | Faces, plates, interiors; the document-upload path is already a HIGH area with a malware gate |
| Loss date, claim type, channel | Intake form; reference table | No | Operational; safe in a queue row |
| Coverage status + as-of timestamp | Replica verification read | No | Derived; the staleness contract rides on the timestamp |

**What the column changed.** Two things, both before a single spec existed. First, every spec
that shows or stores a Yes-row is HIGH — the claim detail, the acknowledgment dispatch, the
duplicate merge (when 0016 reaches triage in the Build week, Maya's HIGH is the contract's HIGH,
not a judgement call). Second, the adjuster **queue row** was designed to carry only No-rows —
claim number, loss type, channel, extraction confidence, as-of — so the fast-path work queue
could be a MEDIUM spec. The PII column did not just label the data; it drew the line between
two screens.

**The readiness gap.** `data-readiness.md` is advisory and says so in its header. It flags one
gap: coverage data is only as fresh as last night's snapshot and is absent altogether during the
refresh window, so a coverage answer is not always there to read. Nothing blocks on it. It goes
on the decision list under Priti's name on the 2-business-day clock, and it goes to steering,
where Karen sees it as a line item now rather than as an incident in month four.

**The lineage** (`lineage-audit.md`): intake form — portal, phone, email, each through its own
adapter → intake API → replica verification read → adjuster queue. Retention: the claim record
and its event log for seven years (D-12). Audit points: every state change in the append-only
event log (NFR-07), and every replica read, under the Q-15 controls. Dan reads this on day 4 as
an input to the threat review; the two are the same afternoon.

## The console designed after the architecture, not after the contract

An exhibit from `experience/` — the adjuster console, the feature's one customer surface, so it
gets the Design seat. `/sdlc-experience` read the channel (a screen), routed to the visual
designer, and drafted three files on day 3 — *after* ADR-001 and ADR-002, because the shape of a
queue depends on what the store and the verification service can answer, and *before* the API
contracts closed, so the two could close together.

**`user-journey.md`.** The happy path is short: open the queue, take the top claim, see coverage
verified and the extraction confidence, one-click confirm (D-09). The journey exists for the
other paths. The one that earned its place: the **abandon path when the replica is stale.** The
adjuster opens a claim whose coverage reads `pending-verification` (refresh window) or carries
the staleness warning (snapshot older than 36h). The console shows the as-of timestamp and the
state in words; the one-click confirm is not offered; the adjuster parks the claim back to the
queue with a reason, and it re-surfaces when the verification read succeeds. No dead end, and no
fast-path decision on last night's data — the day-5 finding that wired the staleness flag to
fast-path escalation (REQ-019) landed in this file too.

**`surface-layout.md`.** The queue (No-rows only, per the data contract) and the claim detail
(the Yes-rows, HIGH), as screens. Markdown in the repo; the hi-fi mock is linked, not pasted.

**`channel-interaction-spec.md`.** For a screen, the interaction contract *is* the event
contract the console speaks, so it was co-authored with Engineering — Jonah and Wes — and Wes
co-signed it. Each of the screen channel's acceptance dimensions traces to a concrete contract
and the acceptance check it becomes:

| Dimension | Contract | Becomes the check |
|-----------|----------|-------------------|
| Confidence display | Every extracted field carries its confidence; the console renders it beside the value, never hides it | A below-threshold field shows its confidence and routes to triage (REQ-009), not to one-click confirm |
| Approval | A decision is a human event with an actor; the console never emits a decision on the adjuster's behalf | The confirm event carries the adjuster's identity and the as-of timestamp it was made on |

This is the file `/sdlc-channel` reads at Intent: when spec 0015 (the fast-path work queue) is
bound to the screen channel in the Build week, these rows become its acceptance checks, and
nothing downstream knows they came from a channel.

## Ship only what's funded, but leave the right seams

An exhibit from `design-doc.md` — where the constraints converge. The model was drafted starting
exactly where Phase 1's handoff pointed: the claim, its event log, its channel sources, with
D-07's merge rules structural rather than bolted on. The coverage service is the *seam* where
real-time can land later without the contract changing.

**The data model (summary):**

- **Claim** — the aggregate; carries line-of-business as a reference table (the auto-proof
  change), an extensible coverage-schema attribute, and a 7-year retention attribute (D-12).
- **Claim event log** — append-only; every state change with actor and timestamp. NFR-07's audit
  requirement is structural; the duplicate-merge (D-07) is an event pair, so history survives the
  merge.
- **FNOL source** — one claim, many sources; each keeps its channel, raw payload reference, and
  received-at.
- **Acknowledgment record** — dispatch attempts, form (email/postal), bounce chain (REQ-022), and
  the regulatory-clock fields the escalation rules read.

**The one change the constitution forced.** Phase 0's constitution said the design must not
*preclude* Harbor's future auto-insurance business (C-03) — while v1 ships property only. Walking
that protected future against the draft model forced exactly one structural change: claim type
moved from a code-level enum to a **reference table** with an extensible coverage schema. Adding
the auto book later becomes a **data change**, not a schema migration — door open, room
unfurnished. "Must not preclude" means the door stays open, not that the room gets furnished. The
nightly sync (C-02) was honored the same way: the replica read *is* the design, not a workaround
pasted over it. D-12 (document retention) surfaced at Thursday's steering; Luis answered next
morning — seven years, per the stricter state's regulation — and it landed in the model as a
retention attribute, not a TODO.

> **The check that keeps it honest.** On day 5 the consistency check runs both directions: every
> top-tier requirement must land in a design element, and every remaining element must trace
> back to a requirement. It found a notification-preferences service that no requirement had
> asked for, sitting in the component diagram. **Cut.** Accidental scope dies in design, not in
> build.

## What Phase 3 receives

A phase ends by handing the next one a package, not a feeling. Everything below crosses the
boundary into Foundation: the signed decisions, the slice that proves them, the security gates to
wire, and the questions that are still open — carried forward under their original IDs, never
silently dropped.

**Crosses into Phase 3:** `phase3-handoff.md`, `design-doc.md`, `api-contracts.md`, `adrs/` +
`adr-registry.md`, `data/` (the contract with its PII column, readiness, lineage), `experience/`
(the journey, the surface layout, the interaction contract `/sdlc-channel` reads at Intent),
`deep-plan-checkpoint.yaml`, the walking-skeleton definition, the threat mitigation map →
risk-tier map, the NFR proving plan.

### Threat review outcomes

Day 4, with Dan. Claude drafted the data flows and candidate list; the session decided. Two of
the nine become **Phase 3's build-time security gates** — this is the one place a Phase 2 human
session reaches directly into the factory Phase 3 builds.

- 9 threats identified; 7 mitigated in the design (private endpoint for the replica, per-channel
  input validation at the adapters, audit log integrity, least-privilege service accounts among
  them).
- 2 assigned as **build-time security gates**, feeding the Build loop's risk-tier map: document
  upload path → malware scanning, HIGH tier, security workflow on every touching PR; acknowledgment
  letter templates → PII template-review gate (data leaves the system on paper).

### The proving plan and the walking skeleton

Nadia's, day 4.

| NFR | Proven by | Read from |
|-----|-----------|-----------|
| NFR-01 (ingestion p95 < 5s) | Load test + continuous gateway metric | Monitoring dashboard |
| NFR-02 (10x surge) | Load test at the Q-16 profile (1,710/day peak, 9 days) before go-live | Load-test report; hardening pass 1 |
| NFR-03 (99.5% business hours) | Uptime monitor on intake endpoints | Ops dashboard, monthly |
| NFR-05 (PII boundary) | Security checklist per change touching claim data | PR security gate records |
| NFR-07 (audit completeness) | Event-log completeness suite in CI | Test results; quarterly compliance sample |
| ADR-004 eval gate | 200-email golden set, ≥95% field accuracy | Eval suite in CI; regression blocks prompt/model changes |

**The walking skeleton** (what Phase 3 must make real): one portal FNOL flows end to end — queue
entry → replica coverage check → test-mode acknowledgment → metric event — deployed to Harbor's
dev environment through the real pipeline, with the blocking hooks and the grader (a fresh AI
reviewer that did not write the code) live.

### The Phase 3 handoff (summary)

- **Signed decisions:** ADR-001 through ADR-004; the two build-time security gates registered for
  the risk-tier map.
- **Recommended first specs:** the walking skeleton, sliced — 0001 queue entry from portal FNOL,
  0002 replica verification read, 0003 test-mode acknowledgment, 0004 metric event. Each rides the
  full loop; together they prove the architecture under the rails.

| ID | Open question | Owner | Due |
|----|---------------|-------|-----|
| Q-17 | Postal dispatch vendor: which provider, and who provisions API credentials for acknowledgment letters? | Dan Kowalski + Harbor ops | Foundation week |
| Q-18 | Construction of the surge load-test dataset from the 2024 CAT (catastrophe) event (volume curve + channel mix) | Priti Shah + Nadia Brooks | Before hardening pass 1 |

---

## The tooling behind this phase

The abstract Phase 2 page describes this work generically. What actually ran, on the
**claude-code-sdlc** plugin and its paired skills:

| What got produced | How |
|---|---|
| Option sets with trade-off framings | Claude in-session, plan-mode research (read-and-propose, no file changes); the plugin pairs Phase 2 with the `deep-plan` skill for structuring the design work |
| ADRs (001–004) | Drafted by Claude from the option-session choices against `templates/phases/02-design/adrs/ADR-template.md`; edited by Rob; signed by Rob + Wes; indexed in the ADR registry |
| Design document + steering visuals | Drafted in-session against `templates/phases/02-design/`; diagrams and the steering narrative rendered with the `visual-explainer` skill |
| Spike findings (replica window, extraction accuracy) | Orchestrator-driven Claude sessions on throwaway branches; findings recorded as spike notes; code deleted |
| Data model + API contracts | Claude drafts carrying the Phase 1 error specs down into contract behavior; Rob shapes; Wes reviews |
| Data contract, readiness, lineage (`data/`) | `/sdlc-data` — the `data-analyst` agent, interview-driven; the PII column confirmed by Dan at its human gate; each readiness gap written to the decision log with an owner and a clock |
| User journey, surface layout, interaction contract (`experience/`) | `/sdlc-experience` — routed by channel to the `visual-designer` agent (a screen); the interaction contract co-authored with Engineering and co-signed by Wes; read later by `/sdlc-channel` at Intent |
| Threat model + mitigation map | Claude drafts the data-flow diagrams and candidate threat list; the day-4 session with Dan decides; outputs feed the Build risk-tier map |
| Design review (day 5) | `/sdlc-review --all` — the `multi-reviewer` agent in council, adversarial, and edge-cases modes; report written as a phase artifact |
| Consistency check | Cross-artifact reference checks inside `/sdlc-gate`; locked-metric consistency via the **frozen-layer validation** (the plugin's check that values locked in earlier phases — the success metric, the constraints — haven't been silently altered by later artifacts) |
| Gate, review packet, advance | `/sdlc-gate`, `/sdlc-phase-report`, `/sdlc-next` (after the four-signature phase review) |

---

Next: [the Phase 3 worked example](phase-3-example.md) — the kit (our firm's reusable engagement
starter) lands in Harbor's repo, the rails get shaken down, and specs 0001–0004 ride the loop to
running software in Harbor's dev environment.
