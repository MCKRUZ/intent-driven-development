# Phase 7 Worked Example: Harbor Mutual

The continuation of [the Build loop example](build-loop-example.md), companion to
[the Phase 7 deep-dive](phase-7-documentation.md). Examples come from a fictional but fully
worked engagement — Harbor Mutual, a regional insurer. Names and numbers are invented but
internally consistent.

## What Phase 7 received

Harbor Mutual — a fictional regional insurer — hired a five-person pod to rebuild how
property-insurance claims get reported and decided. A claim takes a median of **11.4 days**
from FNOL (first notice of loss) to a coverage decision; the target is **5 days or less**. The
Build loop is not a gated phase — it ends when a human *declares the backlog feature-complete*.
That declaration came Friday 2026-07-10: **44 specs** merged since Foundation, both hardening
passes done, the system running in Harbor's dev and test environments. Documentation does not
start from a blank page — it starts from the system as built and the record already on disk.

**Inherited from the Build loop — the feature-complete declaration's package:**

- `phase7-handoff.md`
- `specs/` — 44 merged
- `api-contracts.md` — Phase 2
- `adr-registry.md` — ADR-001…011
- the running dev & test system

**The one question — and what is already true by construction.** Everything this week produces
is what Harbor lives with after the pod leaves. So the week has exactly one question: **can
Harbor understand, run, and operate this system without us in the room?** Most of the record
already exists. Specs stayed current in the same PR as the behavior; ADRs were signed when the
decisions were made; the harness is versioned in the repo. Phase 7 is not "write the docs at the
end" — it is consolidate, diff against the system *as built*, close the decision debt, write the
operations manual, and then **prove all of it by use**.

> "Can Harbor understand, run, and operate this system without us in the room?"

**The one new face — and why she matters.** One person joins the story: **Ines Roy**, a Harbor
engineer hired three weeks ago, who has never opened the repo. That is exactly why she was asked
— she is this week's most valuable contributor, because the README is for her. This is **Nadia
Brooks's** phase. The Quality Engineer owns what "verified" means here, and makes sure the people
doing the verifying are *not the pod*.

The system, in one line: portal/phone/email FNOL intake → a buffered claim queue → coverage
verification against PolicyOne's nightly **snapshot replica** → fast-path recommendations for
simple claims → acknowledgment dispatch. Claims live in a relational model plus an append-only
event log.

**Our pod**

| Person | Role |
| ------ | ---- |
| Maya Chen | Pod Lead — owns the drift triage and the Phase 8 handoff |
| Rob Feld | Setup Owner — owns the RUNBOOK's truth; co-signs the swept ADRs |
| Jonah Kim | Orchestrator / Checker — drives the drafting agents; fixes doc defects through the loop |
| Sara Whitfield | Orchestrator / Checker — runs the contract diff |
| Nadia Brooks | Quality Engineer — this is her phase; owns what "verified" means |

**Harbor Mutual**

| Person | Role |
| ------ | ---- |
| Karen Voss | VP Claims Operations — sponsor; approves the advance |
| Wes Carter | Lead engineer — reviews the drift catalog, co-signs the ADRs; inherits the decision record |
| Tom Reilly | Platform engineer — runs the RUNBOOK cold walk-through; inherits operations |
| Ines Roy | New engineer — the cold README verifier, three weeks in |
| Luis Ortega | Product owner — confirms the user-facing docs |
| Dan Kowalski | IT security — the access boundary behind the cold checkout's step 4 |

**The ID codes, decoded.** Every artifact in this engagement carries a stable identifier, so a
decision made in week two can still be traced in month nine. The ones that surface this week:

| Prefix | Means | Born in | Example here |
| ------ | ----- | ------- | ------------ |
| `ADR-NNN` | An architecture decision record — a signed choice | Phase 2, or swept here | ADR-001–011 (current); ADR-012, ADR-013 (found by the sweep) |
| `REQ-NNN` | A functional requirement | Phase 1 | REQ-014 same-business-day coverage status |
| `Q-NN` | An open question with an owner and a due date | any | Q-18 the 2024 surge load-test dataset (feeds the RUNBOOK scale steps) |
| `NNNN` spec | A Build-loop spec — one change, ridden through the loop | Build | 0045, the drift-defect fix that ran the loop this week (Build's last feature spec was 0044) |
| `C-NN` | A constraint from Phase 0 — a hard limit the system must honor | Phase 0 | the source limits the specs still trace back to |
| `NFR-NN` | A non-functional requirement — a measurable quality target | Phase 1 | the coverage-check latency budget the replica path holds to |
| `DOC-NNN` | A client document taken in at intake | Phase 0 | the source corpus the specs still trace back to |

The plugin's Phase 7 begins by reading `phase7-handoff.md` and diffing every endpoint against
Phase 2's `api-contracts.md`. A drift with no label at the end of the week is a gate failure —
that is the thread tying the Build loop's output to Phase 7's.

**Words this page leans on:**

| Term | What it means |
| ---- | ------------- |
| **Drift** | A difference between what a Phase 2 contract promised and what the built system does — intentional (needs a documented why) or unintentional (a defect). |
| **Cold verification** | Proving a document by following it with no help: someone who has never touched the system executes it exactly as written; every stall is a documentation defect. |
| **RUNBOOK** | The operations manual written for a reader who is exhausted, stressed, and new to the system, mid-incident: numbered steps, exact commands, a check after each one. |
| **The rails** | The enforcement from Phase 3 — CI gates, the grader, branch protection, deploy pipeline. Doc PRs ride them like code. |
| **The loop** | Intent → Delegate → Discern, per spec. Closed for features; still how every fix this week gets made. |
| **The replica** | PolicyOne's nightly-refreshed, read-only policy-data copy that coverage checks query — unavailable during its 02:00–04:30 refresh window (found by a Phase 2 spike). |

## The procedure, step by step

Phase 7 is a short workflow in `claude-code-sdlc` and five working days in this standard. The
first half **drafts and diffs**; the second half **verifies by use** and fixes what the
verification finds. Below, they're braided: what the tool runs, what the humans do that the tool
cannot, and the file each day leaves behind.

> **State markers.** `▪` a command does it — and writes the file · `▸` a person does it — and it
> is recorded · `⚠` a person does it — and nothing records it.

### Day 1 — Mon 7/13 · plugin Step 0 opens: scope the docs, then trust-but-verify the specs

The plugin's Step 0 is a **blocking human gate**: before writing anything, Claude asks who reads
each document, what already exists, what must be created, and which client standards apply. Then
the human work no command performs — the Quality Engineer samples specs and executes their
acceptance checks by hand against dev, the pass that proves the specs really did stay current all
through Build.

**Tooling —** `/sdlc` → the Phase 7 scoping HITL gate; human decision.

**Artifacts out —** documentation scope, decided with the client (not yet on disk); the
spec-library sample audit (no plugin step runs it; no file records it).

> ⚠ **The gap:** The standard makes the spec-library sample audit a Phase 7 deliverable and a
> gate line (*"the spec library sample audit passed"*). No step in `claude-code-sdlc` performs
> it, and no artifact records it. It happens because the QE runs it — and its receipt is a memory.

> **At Harbor:** Scope session with Wes and Tom — three audiences (Harbor engineers, ops,
> adjusters' supervisors), four documents to create (README, API docs, RUNBOOK, intake-supervisor
> user guide), and one decision: Harbor has no documentation standard, so ours becomes theirs.
> Current by construction: 44 specs, ADR-001–011, the harness docs. Nadia samples **eight specs**
> against live behavior in dev — eight match.

### Day 2 — Tue 7/14 · plugin Steps 1–2 · two streams at once: the README and the contract diff

Two drafting agents spawn in a single message because they share nothing: one drafts the README
and user-facing docs from the repo as it actually is; the other reads every endpoint and
**diffs** it against the Phase 2 contracts. The diff — never a transcription — produces the drift
catalog, reviewed with the client's lead engineer, because the contracts are theirs after close.

**Tooling —** `/sdlc` → `doc-updater` + `backend-architect`, in parallel.

**Artifacts out —** `README.md`; `api-docs.md`; `drift-catalog.md` (optional in the registry; the
gate never checks it).

> **At Harbor:** README drafted from the repo — prerequisites, local setup, run modes, the loop in
> one page. The intake-supervisor user guide drafted alongside, reviewed by Luis and Dee Alvarez.
> The diff against the Phase 2 contracts produces a **two-entry drift catalog** — two differences
> after fourteen weeks of Build; Wes reviews it with Maya. One documented *why*, one defect. The
> full catalog is below.

### Day 3 — Wed 7/15 · plugin Step 3: write the operations manual for 3 a.m.

The RUNBOOK is drafted from the real pipeline and infrastructure for one reader: someone
exhausted, stressed, and seeing the system for the first time, mid-incident. Every procedure is
numbered steps, exact copy-pasteable commands, an observable check after each, and a recovery
path. The failure scenarios come from what the engagement actually learned, not a template's
imagination.

**Tooling —** `/sdlc-coach` → RUNBOOK template, from the real pipeline & Bicep. Rob corrects — the
Setup Owner owns the RUNBOOK's truth.

**Artifacts out —** `RUNBOOK.md`.

> **At Harbor:** Five failure scenarios, every one earned: the replica's 02:00–04:30 refresh
> window (a Phase 2 spike finding), a failed PolicyOne nightly sync, storm-surge queue depth (scale
> steps sized from the 2024 CAT profile, Q-18's dataset), an email-extraction accuracy regression,
> and a bad deploy. Each scenario names its Phase 9 alert. **"See the wiki" and "ask the team"
> appear zero times.** Scenario 1, verbatim, is below.

### Day 4 — Thu 7/16 · plugin Step 4 · plus the defect fix: sweep for decisions nobody wrote down

A read-only Explore sweep reads the Build-era merge history and spec library for hard-to-undo
choices that never got a written record. Each candidate becomes a drafted ADR — context, options,
decision, consequences — for humans to sign or strike. Any defect the documenting surfaced rides
the loop like any change, even in a docs week.

**Tooling —** `/sdlc` → `Explore` sweep; `/sdlc-coach` → ADR template; spec 0045 (no plugin
command — it rides the Build loop).

**Artifacts out** — the new ADRs land under `.sdlc/artifacts/02-design/adrs/`: `adrs/ADR-012,
ADR-013`; `adr-registry.md` (updated); spec `0045` (through the loop).

> ⚠ **The gap:** The plugin's sweep prompt tells Explore to "search the git history *from Phase 4
> onward*." There is no Phase 4 — Implementation, Quality, and Testing collapsed into the
> continuous Build loop. The sweep should read the whole Build history; the prompt names a phase
> that does not exist. It's a drift, logged, not repeated here.

> **At Harbor:** The sweep surfaces **four candidates**; Wes and Rob triage to two real ones.
> **ADR-012** (surge queue retry and backoff, lived in a PR thread since a week-9 near-miss) and
> **ADR-013** (claim-document retention tiering, made with Priti Shah in a Build review,
> irreversible after go-live, written down nowhere), both co-signed by Rob and Wes. The other two
> struck as implementation detail, recorded as struck. The drift defect — spec **0045**,
> claims-search returning a bare 500 — rides the loop: graded, non-author checked, merged, deployed
> to dev.

### Day 5 — Fri 7/17 · plugin Steps 5–7 · the gate: verify by use, then a human decides

The teeth of the week. A client engineer who has never opened the repo follows the README on a
clean machine while the pod stays silent; the ops engineer walks real RUNBOOK procedures in dev
with their own permissions. Defects fixed and re-run clean. Then the automated gate runs,
generates the report, and stops — `advance_phase.py` will not move the engagement without a named
human's sign-off.

**Tooling —** the cold runs (*none — no plugin command; that is the point*); `/sdlc-gate` →
`check_gates.py`; `/visual-explainer`; `/sdlc-phase-report`; `/sdlc-next` → `advance_phase.py
--confirmed`.

**Artifacts out —** `phase8-handoff.md`; `.sdlc/reports/phase07-report.html`; the README
cold-checkout record (the doc-defect log); the RUNBOOK cold walk-through record; the sponsor's
signature — billing milestone 5.

> ⚠ **The gap:** `check_gates.py` verifies that four files — `README.md`, `api-docs.md`,
> `RUNBOOK.md`, `phase8-handoff.md` — exist, are non-empty, and contain no placeholder text. The
> two *cold-run* conditions the registry lists as verification teeth are prose `check:` strings the
> script never executes. **The human gate is real. The cold runs it should demand, the code cannot
> see.**

> **At Harbor:** **9:00 cold checkout:** Ines on a clean machine, pod silent; she stalls at step 4
> (the local-secrets bootstrap assumed a Key Vault read permission new hires lack). Fix merges
> before lunch; the 11:30 re-run is clean, end-to-end, forty minutes. **13:00 cold walk-through:**
> Tom executes a deploy, a rollback, and the simulated replica-window incident with his own
> permissions; one gap (a scale-up step named a subscription role the pod holds and Harbor
> doesn't), rewritten and re-walked clean. Gate passes; Karen signs at steering. Billing milestone
> 5; advance to Deployment.

## What Phase 7 produced

The documentation week's whole output, named. Blue (`▪`) rows are written by a command or agent
and checked by the gate. **Amber (`⚠`) rows are the method's human work** — required by this
standard, produced by no tool, and today leaving no file behind. The amber rows here are the
phase's own teeth: the cold runs that *are* the verification.

Key: `▪` a command does it — and writes the file · `▸` a person does it — and it is recorded ·
`⚠` a person does it — and nothing records it.

| Artifact | What it actually is | Written by | Signed by | Lives at | Feeds |
| -------- | ------------------- | ---------- | --------- | -------- | ----- |
| ▪ README.md | The setup manual, proven against a fresh checkout: prerequisites, local setup, run modes, how to contribute. Not done until a stranger ran it | `doc-updater` agent, from the repo | Quality Engineer | repo root — `README.md` | The cold checkout; Harbor's next hire |
| ▪ api-docs.md | Every current endpoint: request/response shapes, auth, the error catalog, and the changelog of drift from the Phase 2 contracts. Diffed, never transcribed | `backend-architect` agent | Setup Owner | `.sdlc/artifacts/07-documentation/` | Phase 8; the client's engineers |
| ▪ drift-catalog.md | Every difference between the signed contracts and the built system, each human-labeled intentional (with its why) or defect. One row per drift | `backend-architect` diff; humans label | Pod Lead (with client lead engineer) | `.sdlc/artifacts/07-documentation/` | The API-doc corrections; Phase 8 blockers |
| ▪ RUNBOOK.md | The 3 a.m. operations manual: deployment, configuration reference, common operations, the top failure scenarios, and each one's Phase 9 alert. Proven by a cold walk-through | `/sdlc-coach` drafts; Setup Owner corrects | Setup Owner | repo root — `RUNBOOK.md` | Phase 8 checklist; Phase 9 alerts |
| ▪ adrs/ADR-012, ADR-013 · adr-registry.md | The Build-era decisions the sweep found, now written down and co-signed; the registry closed with no open ADRs | Claude drafts from the Explore sweep | **Setup Owner + client counterpart — both** | `.sdlc/artifacts/02-design/adrs/` | Close — the decision history Harbor inherits |
| ▪ phase8-handoff.md | Documentation inventory, the honest gaps, the deployment checklist, and ADR status — the package Phase 8 opens | Claude drafts; Pod Lead completes | Pod Lead | `.sdlc/artifacts/07-documentation/` | Phase 8, directly |
| ▪ phase07-report.html · phase07-visual.html | The gate packet and the documentation-completeness audit, self-contained. This is the document the sponsor reads before signing | `generate_phase_report.py` · `/visual-explainer` | — | `.sdlc/reports/` | The manual sign-off gate |
| ⚠ README cold-checkout record | The doc-defect log: each stall a cold verifier hit — the step, what was missing, what they did instead — logged as it happened. "A little help" is a fail | **Quality Engineer, observing** | QE | no path — nothing writes it | The same-day fixes; the gate's teeth |
| ⚠ RUNBOOK cold walk-through record | A deploy, a rollback, and one failure scenario, executed cold by the client's ops engineer with their own permissions — the gaps found and rewritten | **Client ops engineer + QE** | QE | no path — nothing writes it | The RUNBOOK rewrite; the gate's teeth |
| ⚠ spec-library sample audit | Five to ten specs, weighted to HIGH-risk and recently changed, their acceptance checks executed by hand against dev — the trust-but-verify pass that proves the construction held | **Quality Engineer** | QE | no path — no plugin step performs it | The exit gate ("spec library audit passed") |

**Read the amber rows again.** Three of the phase's deliverables have nowhere to live — and they
are the *teeth*. The two cold runs are the standard's verification teeth, and the plugin registry
lists them as gate conditions, yet `check_gates.py` never executes those `check:` strings and no
file records what the runs found. The spec-library audit has no plugin step at all. **Human work
is not the problem. Human work without a receipt is** — and here the receipt-less work is exactly
what decides whether the phase passed.

Deliberately **not** produced in Phase 7: documentation for things that don't exist yet
(production topology is Phase 8, alert thresholds are Phase 9 — the RUNBOOK *points* at them, it
doesn't invent them), new features of any kind (the Build loop is closed), and a separate "system
specification" duplicating the spec library — two sources of truth means one starts lying.

## Diff the docs against the code — never transcribe

The diff against the Phase 2 contracts produced the drift catalog: two entries. A two-entry
catalog after fourteen weeks of Build is the loop's discipline showing — contracts were carried
through specs, so the system mostly *is* the contract. One of each kind; both resolved inside the
week.

**Artifact: the drift catalog (complete)**

| # | Contract said | System does | Label | Resolution |
| - | ------------- | ----------- | ----- | ---------- |
| 1 | REQ-014 degraded response: coverage check returns `"pending verification"` when the replica is unreachable | Response also carries `staleness_as_of` — the replica's last refresh timestamp | **Intentional.** Added in Build week 7 so adjusters could judge how stale "pending" is; Luis approved it at triage; the why is now in the contract changelog | Contract updated; API docs carry the field and the rationale |
| 2 | All endpoints return the standard error envelope `{ "error": "<message>" }` on failure | Claims-search returns a bare 500 with an empty body on replica timeout | **Unintentional.** A timeout path added in Build week 11 bypassed the error middleware; no decision, no why — a defect | Spec 0045, through the loop Thursday; fixed, graded, merged, deployed |

Two entries, both resolved inside the week. The catalog is empty at the gate — and what it found,
it found before deployment instead of after.

## Prove the README by handing it to someone who has never seen the repo

Ines Roy — three weeks at Harbor, never opened the repo — followed the README on a clean machine
while Nadia watched and the pod stayed silent. She stalled at step 4. The stall was the data.

**9:00 — the cold checkout.** The local-secrets bootstrap assumed a Key Vault read permission that
new Harbor engineers don't have by default. Nobody helped her — the stall is the data.

> **Where she stalled — step 4:** The local-secrets bootstrap assumes a Key Vault read permission
> new Harbor engineers don't have by default.

> **The fix, then the clean re-run:** A bootstrap script plus a documented access-request path
> (Tom as the named approver) merged before lunch. The 11:30 re-run was clean, end-to-end, forty
> minutes.

**Why the stall was the win.** Step 4 failing under observation cost an hour. The same gap
discovered by Harbor's next hire, alone, after close, costs a support escalation and a dent in
trust. The cold run exists to buy failures early. The README failing on a new hire's permissions
in week one of the close — instead of month one of ownership — *is the phase doing its job*.

> ⚠ **The verifiers were the least qualified people available — on purpose.** Ines had never
> opened the repo; Tom ran procedures he didn't write with permissions the pod doesn't have. A
> README verified by its author's teammate has not been verified.

## The operations manual is written for someone exhausted, stressed, and new

Five failure scenarios, every one earned during the engagement rather than imagined: the replica's
refresh window (a Phase 2 spike finding), a failed nightly sync, storm-surge queue depth (scale
steps sized from the 2024 CAT profile), an email-extraction accuracy regression, and a bad deploy.
The first scenario's first branch is the question a 3 a.m. responder actually needs.

**Artifact: RUNBOOK excerpt — failure scenario 1**

```markdown
## Failure scenario 1: coverage checks degraded ("pending verification")

Symptom: portal and adjuster screens show "pending verification" on new
claims; the verification-service dashboard shows replica read failures.

First question — what time is it?
- 02:00-04:30 Eastern: this is the replica's nightly refresh window.
  EXPECTED. Do nothing. Intake is not blocked (claims queue normally and
  verify after the window). Confirm recovery after 04:30 at step 4.
- Any other time: continue to step 1.

1. Check replica availability:
       az sql db show --name policyone-replica --resource-group harbor-claims-prod ...
   You should see: status "Online". If not, go to scenario 2 (failed
   nightly sync).
2. Check the verification service's circuit state:
       curl -s https://<env>/api/internal/verification/health
   You should see: { "replica": "open" | "closed", "staleness_as_of": "<timestamp>" }
3. If the circuit is open and the replica is online, restart the
   verification service:
       az containerapp revision restart ...
   You should see: new revision Healthy within 2 minutes. If not, roll
   back the latest deploy (Common operations > Rollback).
4. Confirm recovery: claims created in the last hour move from "pending
   verification" to a coverage status within 10 minutes of the replica
   returning.
Alert cross-reference: VERIFY-DEGRADED fires after 5 minutes of replica
read failures outside the refresh window (configured in Phase 9).
```

Numbered, copy-pasteable, observable, recoverable — and the first branch is the question a 3 a.m.
responder actually needs: *is this the window we already know about?* Each scenario ends with the
alert that should catch it — Phase 9 configures those alerts, and the runbook and the alerts must
describe the same failures.

## Sweep the build history for decisions nobody wrote down

The Explore sweep over the Build-era merge history and spec library surfaced four candidates; Wes
and Rob triaged them to two real ones. Both now have signatures from the people who'll live with
them.

**The two ADRs the sweep found.**

> **ADR-012 — surge queue retry and backoff policy.** Chosen in Build week 9 after a near-miss
> during the first hardening pass; it lived in a PR thread until today. Now it has context,
> options, consequences — and signatures.

> **ADR-013 — claim-document retention tiering.** A storage-lifecycle choice made with Priti Shah
> (Harbor's data lead) in a Build review; significant, irreversible after go-live, and previously
> written down nowhere.

Both co-signed by Rob and Wes, like every ADR before them. The other two candidates were struck as
implementation detail, recorded as struck. No open ADRs remain.

**The defect fix rode the loop.** The drift defect, spec **0045** (claims-search returns a bare 500
on replica timeout instead of the standard error envelope), rode the loop like any change — graded,
checked by a non-author, merged, deployed to dev — and the API docs and contract now describe one
truth.

> **What to notice:** ADR-012 lived in a PR thread; ADR-013 lived in two people's memory. Decision
> debt got collected while the debtors were still in the room.

## What Phase 8 receives

A phase ends by handing the next one a package, not a feeling. Everything below crosses the
boundary into Deployment: the docs a stranger proved, the decision record closed and co-signed, and
the gaps named honestly — the things Phase 7 could not document because they do not exist yet,
carried forward as pointers, never invented.

**Crosses into Phase 8:**

- `README.md` — cold-verified
- `api-docs.md` — diffed, one defect fixed
- `RUNBOOK.md` — cold-walked
- `phase8-handoff.md`
- `drift-catalog.md` — empty at the gate
- `adr-registry.md` — through ADR-013, none open
- `⚠` the two cold-run records — no receipt on disk

**The Phase 8 handoff (summary).** Maya's, drafted Friday, completed at the gate.

- **Inventory:** README (created, cold-verified), API docs (created, diffed, one defect fixed),
  RUNBOOK (created, cold-walked), user guide for intake supervisors (created, reviewed by Luis and
  Dee Alvarez), ADR registry complete through ADR-013, spec library current (audited sample 8/8).
- **Honest gaps:** production topology and alert thresholds are pointers to Phases 8 and 9, not
  content — they don't exist yet, and the docs say so rather than pretend; the RUNBOOK's scale
  procedures are dev/test-proven and get their production rehearsal in Phase 8.
- **Deployment checklist:** carried into Phase 8 — secrets rotation before go-live, the production
  Bicep promotion, the go/no-go ceremony roles.
- **ADR status:** none open; ADR-012 and ADR-013 signed this week.

**The open threads, carried forward under their original IDs.** No numbered question is dropped;
each crosses the boundary with an owner.

| Thread | Carried as | Owner | Lands in |
| ------ | ---------- | ----- | -------- |
| Production topology | A pointer in the RUNBOOK and handoff — documented as "provisioned in Phase 8", not invented now | Rob Feld + Tom Reilly | Phase 8 |
| Alert thresholds | Each RUNBOOK failure scenario names the alert that should catch it; the thresholds themselves are set against real baseline data | Nadia Brooks + Harbor ops | Phase 9 |
| RUNBOOK scale procedures | Sized from Q-18's 2024 CAT dataset and proven in dev/test; the production rehearsal is Phase 8's | Tom Reilly | Phase 8 |

One honest line went on the record at steering: production topology and alert thresholds are
documented as pointers to the next phases — not as content, because they don't exist yet. **Billing
milestone 5.** The engagement advanced to Deployment.

## The tooling behind this phase

The [Phase 7 deep-dive](phase-7-documentation.md) describes this work generically. What actually
ran, on the **claude-code-sdlc** plugin and its paired skills:

| What got produced | How |
| ----------------- | --- |
| Documentation scope (audiences, gaps) | `/sdlc` → the Phase 7 workflow's scoping gate, answered with Wes and Tom in the room |
| README + user-facing docs | `/sdlc` → the `doc-updater` agent, drafting from the repo and a fresh checkout; corrected by what Ines's cold run found |
| API docs + drift catalog | `/sdlc` → the `backend-architect` agent, diffing every endpoint against the Phase 2 contracts; humans labeled each drift |
| RUNBOOK | `/sdlc-coach` → drafted against the phase RUNBOOK template from the real pipeline and Bicep; Rob corrected; Tom cold-walked |
| Decision sweep | `/sdlc` → the `Explore` agent over the Build merge history and spec library; Wes and Rob triaged the candidates |
| ADR-012, ADR-013 | `/sdlc-coach` → drafted against the ADR template; signed by Rob and Wes |
| Defect fix (spec 0045) | No plugin command — rides the build loop: bounds, plan mode, grader, non-author Checker, deploy-dev |
| The cold runs | No plugin command, deliberately: Ines on the README, Tom on the RUNBOOK — observed, unassisted |
| Gate, audit visual, report, advance | `/sdlc-gate` → `check_gates.py` · `/visual-explainer` → the documentation audit · `/sdlc-phase-report` → the phase record · `/sdlc-next` |

---

Next: [the Phase 8 worked example](phase-8-example.md) — go-live week: the rollback rehearsal that
fails on Tuesday (and why that was the win), seven names on the go/no-go, and the first real FNOL
through production in 3.1 hours.
