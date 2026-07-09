# Phase 9 Worked Example: Harbor Mutual

The continuation of [the Phase 8 example](phase-8-example.md), companion to
[the Phase 9 deep-dive](phase-9-monitoring.md). Production went live Thursday 2026-07-23;
hypercare is running on its two-week window, and Phase 9 runs inside it on purpose — the
system is finally producing real baseline data while the pod is still beside Harbor's
operators as they take the watch. Two weeks — Monday 2026-07-27 to Friday 2026-08-07 — and the
gate falls the day hypercare ends.

The spine of this phase is worth naming up front: back in design week the quality engineer
wrote an **NFR proving plan** — for every quality target, the method that would prove it and
*the named place its number would be read*. Phase 9 is where those promises come due. Nobody
new joins the story; the people who answer Harbor's pager are the people who sat in every
session.

## What Phase 9 received

Harbor Mutual — a fictional regional insurer — rebuilt how property-insurance claims get
reported and decided. A claim took a median of **11.4 days** from FNOL (first notice of loss)
to a coverage decision; the target is **5 days or less**. Production went live Thursday
**2026-07-23**; hypercare is running on its two-week window. Phase 9 does not start from a
blank page — it starts from a live system, a handoff on disk, and a plan written months ago
about where every number would be read.

**Inherited — the three inputs Phase 9 is built on, plus the system itself:**

- `phase9-handoff.md` — where the deployment left things.
- `RUNBOOK.md` — the failure scenarios every alert is written against.
- `nfr-proving-plan.md` — from Phase 2; the promises now coming due.
- The **live system** — producing real numbers, not a document.

**The through-line: Phase 2 said where each number would be read.** For every quality target,
the proving plan named the method that would prove it and the exact place its number would be
read. Phase 9 either reads it — on a dashboard, in an alert, on the scorecard — or flags it
modeled with a revisit date. A proving plan whose numbers never got read is homework nobody
graded.

- **NFR-01** (ingestion p95 < 5s) — "read from the monitoring dashboard." That dashboard gets
  built this week.
- **NFR-02** (the 10x surge) — "read from the load-test report." Late July gave Harbor no
  storm, so this one stays modeled.
- **ADR-004** eval gate (≥95% email-extraction accuracy) — "read from the eval suite in CI."
  Phase 9 turns that into a live production watch.

**Where Phase 9 starts.** The system: portal / phone / email FNOL intake → a buffered claim
queue → coverage verification against PolicyOne's nightly **snapshot replica** (unavailable
02:00–04:30 during refresh) → fast-path recommendations → acknowledgment dispatch through the
postal vendor.

> **From `phase9-handoff.md` — where we are:** "Live since 7/23 (cutover at intake; legacy
> fallback warm). Hypercare running. The first real numbers exist; nothing pages anyone yet."

**The cast** — nobody new joins the story; the people who answer Harbor's pager are the people
who sat in every session:

| Side              | Who                                                                                                                                                                                                                                          |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Our pod**       | Maya Chen (Pod Lead — this phase is hers, jointly with Harbor's operations) · Nadia Brooks (Quality Engineer — designs and owns the alert drill) · Rob Feld (Setup Owner — wires monitoring into Harbor's own stack) · Jonah Kim and Sara Whitfield (Orchestrators — draft alert/dashboard config and the playbook; fix through the loop). |
| **Harbor Mutual** | On-call lead & operators (own everything this phase produces; answer the drill from the playbook) · Tom Reilly (platform engineer — wires channels and paging; agrees the synthetic triggers) · Priti Shah (data & reporting — the business dashboards; named on the surge-threshold revisit) · Dan Kowalski (IT security — the security alert lane) · Luis Ortega (product owner — confirms the business metrics measure what the business means) · Dee Alvarez (intake supervisor — the intake-degraded communication path) · Karen Voss (VP Claims Operations — sponsor; hears the first honest metric read). |

**The ID codes, decoded.** Every artifact carries a stable identifier, so a promise made in
design week can still be traced when its number comes due in production:

| Prefix     | Means                                                                | Born in    | Example here                                    |
| ---------- | -------------------------------------------------------------------- | ---------- | ----------------------------------------------- |
| `NFR-NN`   | A non-functional requirement — a quality target with a number        | Phase 1    | NFR-01 ingestion p95 · NFR-02 the 10x surge     |
| `REQ-NNN`  | A functional requirement                                             | Phase 1    | REQ-014 same-business-day coverage status       |
| `ADR-NNN`  | An architecture decision record — a signed choice                    | Phase 2    | ADR-004 email-extraction eval gate              |
| `C-NN`     | A constraint — a hard limit the system must honor                    | Phase 0    | C-04 the acknowledgment regulatory clock        |
| `D-NN`     | A product decision                                                   | Phase 0/1  | D-09 the fast path (61% of claims)              |
| `Q-NN`     | An open question with an owner and a due date                        | any        | Q-18 the surge load-test dataset                |
| `NNNN`     | A spec — one feature in one file                                     | Foundation | Build closed at 0044; 0045–0046 were close-phase fixes |

## The procedure, step by step

Phase 9 is seven numbered steps in `claude-code-sdlc` and ten working days in this standard,
run inside the hypercare window. Below they're braided: what the tool runs, what the humans do
that the tool cannot, and the file each beat leaves behind. Two of the most important beats —
the drill and the what-healthy session — have no command at all.

**Reading the markers.** `▪` a command does it — and writes the file · `▸` a person does it —
and it is recorded · `⚠` a person does it — and nothing records it.

### Days 1–2 · Mon–Tue 7/27–28 — agree what "healthy" means, before anything is wired
*plugin Step 0 opens*

**Tooling —** `/sdlc-next` → the Step 0 HITL gate (`AskUserQuestion`) · *the what-healthy
session — humans in a room, no command.*

**Artifacts out —** `▸` the healthy / degraded / who-is-woken table (decided in the room, not
yet on disk).

The plugin's Step 0 is a blocking human gate: before configuring any monitoring, Claude asks
the client, via `AskUserQuestion`, the top failure modes, who gets paged and at what
threshold, and which stack the alerts live in. But those four questions are the thin version.
The phase's defining session is deeper and has no command: the pod and Harbor's operations
walk every RUNBOOK failure scenario and every top-priority journey and answer, for each, what
healthy looks like, what degraded looks like, and who gets woken versus who's told in the
morning. Operations' answers win ties — it is their 3 a.m.

> **At Harbor:** The deepest decision of the phase came from Harbor's side of the table. The
> replica is unavailable 02:00–04:30 nightly by design (REQ-014 degrades to "pending
> verification") — so an alert that fires every night at 02:00 would train the on-call to
> ignore the one that matters. They chose a **suppression window plus a post-04:30 recovery
> check**: don't page for the expected outage; do page if it fails to come back. Scope landed
> in writing — everything wires into **Harbor's Azure Monitor workspace**, where Tom's team
> already lives, paging through their existing rotation.

> ⚠ **The gap:** The session that shapes the whole phase — the healthy/degraded/who-is-woken
> table — is the standard's core human work, and **no command captures it**. The plugin's
> `doc-updater` later writes `monitoring-config.md` from the measured baseline, not from this
> session's transcript. The table only reaches disk if a human types it there. The phase's most
> important input has no receipt of its own.

### Days 3–4 · Wed–Thu 7/29–30 — measure what normal actually is; make it visible
*plugin Step 1*

**Tooling —** Agent → `performance-benchmarker` · Agent → `doc-updater` → `monitoring-config.md`.

**Artifacts out —** under `.sdlc/artifacts/09-monitoring/`: `▪` `monitoring-config.md` · `▪`
the baseline measurements (folded in).

Now the machine runs. Claude spawns the `performance-benchmarker` agent to establish the
production baseline against the Phase 1 NFR targets, then the `doc-updater` agent to write it
up as the monitoring configuration. Every number is recorded with the period it was measured
over. Dashboards go live in Harbor's own workspace: system health, application health, and —
built with Priti in Harbor's reporting language — the business layer.

> **At Harbor:** The measured baseline caught that production ran slightly *better* than the
> design-phase estimate: replica verification p95 came in at **165ms** against Phase 2's ~180ms
> spike number. Portal submit p95 410ms, intake error rate 0.3%, queue depth steady under 40.
> One honest gap, written down not papered over: **the surge path has no baseline** — late July
> gave Harbor no storm — so its thresholds derive from Q-18's modeled 2024 CAT dataset (peak
> 1,710 claims/day, nine elevated days), flagged modeled with Priti named on the revisit.

### Day 5 · Fri 7/31 — turn each failure mode into an alert, and cut the ones nobody would act on
*plugin Step 2*

**Tooling —** `/sdlc-coach` → `alert-definitions.md` · *threshold confirmation & fatigue review
— human work, no command.*

**Artifacts out —** `▪` `alert-definitions.md` · `▸` operations' confirmation on every
threshold · `⚠` the fatigue-review record (the method requires it; nothing writes it).

Claude drafts the alert table against the phase template — every critical failure mode gets a
condition derived from the baseline, a severity, a named recipient, and a playbook link, with
the derivation written next to the number. Then two pieces of human work the plugin does not
perform: the operators **confirm every threshold** (the named human stop of the phase), and
the **alert-fatigue review** replays each proposed condition over the hypercare history and
cuts anything that would fire weekly without demanding action.

> **At Harbor:** Six alerts shipped; the fatigue review cut two before they went live — a
> per-instance CPU alert (not actionable; the platform autoscales) and a portal-latency warning
> (it duplicated the intake error-rate signal). "2x the measured p95 over 10 minutes" survives
> an argument in six months; "500ms" would not. Six actionable alerts beat eight the on-call
> learns to swipe away.

### Days 6–7 · Mon–Tue 8/3–4 — write down what to do when it fires
*plugin Step 3*

**Tooling —** `/sdlc-coach` → `incident-response.md` · *the on-call lead's line-by-line
correction — human.*

**Artifacts out —** `▪` `incident-response.md`.

Claude drafts the incident playbook against the alert table and the Phase 7 RUNBOOK: per
alert, what it means, the first three diagnosis steps, the P1/P2/P3 classification, the
escalation names, and the communication templates — what users and leadership hear while it's
happening, and who says it. It cross-references the RUNBOOK for resolution rather than
repeating it. Harbor's on-call lead corrects it line by line.

> **At Harbor:** Every escalation name in the playbook was Harbor's own; the pod appears once,
> at the bottom of the chain — "escalation of last resort until Close." The playbook spelled
> out exactly what the claims office hears from Dee's intake team when intake degrades, and what
> leadership hears on a P1. One source of truth per failure, two lenses on it: the playbook
> detects and communicates, the RUNBOOK resolves.

### Day 8 · Wed 8/5 — fire every critical alert on purpose, and watch the client answer it
*no plugin step exists*

**Tooling —** *none — the drill is human work; no command, and no step in the plugin runs it.*

**Artifacts out —** `⚠` `drill-record.md` (the registry marks it optional; nothing writes it).

Each critical alert is triggered for real, one at a time, through a synthetic trigger agreed
with Tom in advance — replica reads blocked outside the window, a retry storm on the dispatch
test lane, flagged test messages pushed past the queue threshold, a staleness clock wound
forward. Harbor's on-call responds from the playbook while Nadia observes in silence. What
breaks gets fixed through the loop and re-drilled until clean.

> ⚠ **The gap:** The exit gate has a **teeth** condition — *"Alert drill executed: every
> critical alert fired and answered from the playbook."* Yet there is **no drill step in the
> plugin** — the workflow runs Step 0 through Step 6 and never mentions one — **no command**
> triggers it, and `drill-record.md` is listed *optional*. The single most valuable act of the
> phase, the one that separates a procedure from a wish, is required by the gate and produced by
> nothing. This is exactly the work that caught Harbor's silent-night bug.

> **At Harbor:** The drill earned its keep. VERIFY-DEGRADED routed to the general ops channel
> instead of the pager rotation — a routing-key typo that would have meant a silent night during
> a real incident. Fixed by reviewed PR, re-fired 11:05, paged in 38 seconds, closed clean. A
> second finding — a playbook step that opened a dashboard needing pod permissions — was caught
> and re-drilled clean the same day. Both fixes rode the full loop: specs, the grader, a
> non-author Checker, in a monitoring week.

### Day 9 · Thu 8/6 — ask the cumulative question: what did the whole engagement learn?
*plugin Step 4*

**Tooling —** Agent → `feedback-synthesizer` · `/visual-explainer` → the evidence pack · *the
candor — human; a flattering drafter produces a worthless retro.*

**Artifacts out —** `▪` `project-retrospective.md`.

Claude spawns the `feedback-synthesizer` agent in the background to assemble the hypercare
findings and intake-team feedback, and `/visual-explainer` renders the evidence pack the room
argues from. Then the half-day itself, which no command can do: the pod plus Harbor's core
people argue from receipts — the metrics history, the Retro+ log, every escaped bug with its
"which check should have caught it?" answer, the gate records. The AI assembles the evidence;
the humans own the candor.

> **At Harbor:** The retro argued from receipts, not adjectives. Not "security review was slow"
> but **2.1-day median against a 0.9-day general queue** — and a structural fix, a twice-weekly
> committed slot in Dan's calendar, not an exhortation. Three concrete outputs: the technical
> debt log, the client-facing improvements, and a four-item harvest list — among them the
> suppression-window-plus-recovery-check pattern born this very week.

### Day 10 · Fri 8/7 — hand over the watch, run the gate, read the metric honestly
*plugin Steps 5–6 · the gate*

**Tooling —** `/visual-explainer` → `.sdlc/reports/phase09-visual.html` · `/sdlc-gate` →
`check_gates.py` · `/sdlc-phase-report` → `generate_phase_report.py` · `/sdlc-next` →
`advance_phase.py --confirmed`.

**Artifacts out —** `▪` `.sdlc/reports/phase09-report.html` · `⚠` `close-handoff.md` (the
registry requires it; the phase body never says what it is) · `▸` the sponsor's signature —
billing milestone 7.

The machine renders the visual report and runs the gate. `check_gates.py` reports;
`advance_phase.py` will not move the engagement to Close without `--confirmed` — a named
human's sign-off. Because the gate falls at hypercare's end, signing it is also the moment the
pod formally hands over the watch: the dashboards, the pager rotation, and the playbook become
Harbor's, with the pod one escalation away until Close.

> ⚠ **The gap:** `check_gates.py` verifies that five files exist, are non-empty, and contain no
> placeholder text. The two conditions with real teeth — *every threshold derived from a
> measured baseline* and *the drill executed* — are free-text `check:` lines the script never
> evaluates. And one of the five required files, `close-handoff.md`, has **no Artifact
> Specification anywhere in the phase body** — the registry demands a file the instructions
> never describe. The human gate is real; what it verifies is thinner than what the standard
> asks.

> **At Harbor:** The outcome metric read spectacularly — and was deliberately underclaimed.
> **11.4 → 1.9 days** (all-claims baseline → fast-path claims, 61% of volume, over the two live
> weeks). Steering heard it with the caveat welded on: complex claims are mostly still in
> flight, so the *overall* median can't be read fairly until a full quarter. C-04 acknowledgment
> compliance: 100%, system-enforced. Karen signed — billing milestone 7. The watch became
> Harbor's.

## What Phase 9 produced

The monitoring phase's whole output, named. Blue rows are written by a command and checked by
the gate. **Amber rows are the method's human work** — required by this standard (and in one
case by the plugin's own gate), produced by no tool, and today leaving no file behind. Those
are the rows to argue about.

**Marker key.** `▪` a command does it — and writes the file · `▸` a person does it — and it is
recorded · `⚠` a person does it — and nothing records it.

| Artifact | What it actually is | Written by | Signed by | Lives at | Feeds |
| -------- | ------------------- | ---------- | --------- | -------- | ----- |
| ▪ `monitoring-config.md` | Dashboard inventory, metrics catalog, P0 coverage assessment, and the measured baseline — each number with its measurement period | `performance-benchmarker` measures; `doc-updater` writes | Quality Engineer | `.sdlc/artifacts/09-monitoring/` | Close — the monitoring inventory Harbor inherits |
| ▪ `alert-definitions.md` | The six alerts: condition and derivation, severity, recipient, playbook link; per-critical detail; the alert philosophy | Claude drafts; operations confirm every threshold | **Client operations** | `.sdlc/artifacts/09-monitoring/` | The playbook; the drill |
| ▪ `incident-response.md` | Per alert: meaning, first diagnosis steps, P1/P2/P3, escalation names, communication templates; cross-references the RUNBOOK | Claude drafts; on-call lead corrects | Client operations | `.sdlc/artifacts/09-monitoring/` | The drill; Close |
| ▪ `project-retrospective.md` | What worked and didn't with receipts, the SDLC review, the technical debt log, and the harvest list — "the most important Phase 9 artifact" | `feedback-synthesizer` assembles; the humans own the candor | Pod Lead | `.sdlc/artifacts/09-monitoring/` | The harvest PR (Phase C) |
| ▪ `phase09-report.html` · `phase09-visual.html` | The gate result and artifact inventory, self-contained — the document a sponsor actually reads before signing | `generate_phase_report.py` · `/visual-explainer` | — | `.sdlc/reports/` | The manual sign-off gate |
| ⚠ `drill-record.md` | Per critical alert: the trigger, detection time, where it routed, who responded, the outcome — pass, or the finding and its fix. The one proof the pager works | **Quality Engineer, by hand** | QE | optional in the registry — no step runs the drill | The gate packet; Close |
| ⚠ the what-healthy table | Per failure scenario and journey: healthy, degraded, who is woken, who is told in the morning. The session's entire output | **Pod + client operations** | On-call lead + Pod Lead | no path — folded into `monitoring-config.md` only if a human types it | Every alert definition |
| ⚠ the fatigue-review record | Each proposed alert replayed over hypercare history; anything firing weekly without action raised or cut, with the count | **Quality Engineer** | QE | no path — nothing writes it | The shipped alert set |
| ⚠ the outcome-metric first read | The engagement's headline number, read honestly for the first time in production, caveats attached | **Pod Lead + sponsor** | Sponsor | no path — on the business dashboard and spoken at steering | Close — the final scorecard |
| ⚠ `close-handoff.md` | Monitoring inventory, drill record, debt log, open items with owners — the package Phase C opens on | **Claude drafts — but the phase body never says how** | Pod Lead | gate demands the path; no step writes it | Phase C, directly |

> ⚠ **The gap:** Five of the eleven things Phase 9 is supposed to produce have nowhere the
> tooling puts them — and two of them are the phase's whole reason to exist. The drill that
> caught Harbor's silent-night routing typo is *required by the plugin's own exit gate* and
> produced by no step and no command. The what-healthy session that shapes every alert reaches
> disk only if someone types it up. **Human work is not the problem. Human work without a
> receipt is.**

Deliberately **not** produced in Phase 9: new features, a parallel monitoring stack of the
pod's own (we wire into Harbor's), an alert-tooling migration, and the formal harness handover
— that is Close's job. The backlog stays closed; hypercare defects ride the loop, as ever.

## The alert table, as shipped

An exhibit from `alert-definitions.md` — the six that shipped. Every row derives its threshold
from the measured baseline or says on its face that it's modeled. Every row pages a named
recipient and links a playbook step. An alert nobody acts on is noise wearing a badge; the two
proposals that couldn't survive the fatigue review aren't here, and that's the point.

| Alert | Condition (derivation) | Severity | Pages |
| ----- | ---------------------- | -------- | ----- |
| VERIFY-DEGRADED | Replica read failures sustained 5 min **outside 02:00-04:30** (suppression window + post-window recovery check) | Critical | On-call rotation |
| SYNC-MISSED | Replica staleness > 24 h (nightly sync failed) | Critical | On-call + Priti |
| QUEUE-DEPTH | Claim queue > 400 sustained 15 min (10x measured normal of ~40; **modeled** vs Q-18 surge curve — revisit at first CAT event) | Warning → critical at 1,200 | On-call rotation |
| INTAKE-ERROR-RATE | > 2% sustained 30 min (matches the Phase 8 fallback trigger — one number, two documents) | Critical | On-call + Dee notified |
| ACK-RETRY-BURST | Dispatch retries > 3x baseline per 10 min: warning; sustained 60 min: critical (hypercare day-one finding) | Warning → critical | On-call; vendor escalation path |
| EVAL-GATE-DRIFT | Email extraction accuracy < 95% on the golden set (the ADR-004 gate, now watched in production) | Warning | Quality owner (Harbor) |

Cut at the fatigue review: a per-instance CPU alert (not actionable under autoscale; capacity
already on Tom's dashboard) and a portal-latency warning (it duplicated INTAKE-ERROR-RATE's
signal). Six actionable alerts beat eight the on-call trains itself to ignore. No number here
"felt right" — every one can explain itself, and the one set from modeled data says so on its
face, with a named revisit.

## The proving plan, come due

An exhibit reading `nfr-proving-plan.md` against production. Phase 2's proving plan named, per
quality target, the method and the exact place its number would be read. This is the column
that came due. Some numbers are now live on a dashboard; one is still modeled and honestly
flagged; one became a standing production watch.

| NFR / gate | Phase 2 said it would be read… | …and in Phase 9 it is |
| ---------- | ------------------------------ | --------------------- |
| NFR-01 (ingestion p95 < 5s) | The monitoring dashboard | Live on the application dashboard — portal submit p95 **410 ms**, comfortably under the 5s target |
| NFR-02 (10x surge) | The load-test report; hardening pass 1 | No real storm yet — QUEUE-DEPTH ships **modeled** from Q-18, revisit at the first CAT event (Priti) |
| NFR-03 (99.5% business hours) | The ops dashboard, monthly | Uptime monitor on the intake endpoints, on Tom's system-health dashboard, read monthly |
| NFR-05 (PII boundary) | PR security-gate records | Carried by Dan's security alert lane — what pages security directly, bypassing the general queue |
| NFR-07 (audit completeness) | Test results; quarterly compliance sample | The event-log completeness suite stays in CI; the first compliance sample is on the quarter-read calendar |
| ADR-004 eval gate (≥95% accuracy) | The eval suite in CI; regression blocks changes | Extended into production as **EVAL-GATE-DRIFT** — the CI gate now has a live counterpart watching real extractions |

This is the through-line of the whole standard in one table: a number named in design week,
with the place it would be read written down, is either read here or flagged modeled with a
date — never quietly dropped. The one still modeled says so on its face and carries a named
owner. That is the difference between a proving plan and a wish list.

## The drill record

An exhibit — the artifact the plugin doesn't require but the phase can't do without. The drill
record is the receipt the registry marks optional and the gate's teeth depend on. Nadia kept
it by hand. Every critical alert, its synthetic trigger, when it fired, where it routed, who
answered, and the outcome — pass, or the finding and its fix. It went into the gate packet. An
alert that has never fired is a wish.

```
Wed 8/5   09:12  VERIFY-DEGRADED   synthetic replica block (outside window)
                 FAIL — alert fired but routed to #harbor-ops channel, not
                 the pager rotation (routing-key typo). On a real night:
                 nobody woken. Fixed (routing key corrected via reviewed
                 PR), re-fired 11:05: paged in 38 s, responder followed
                 playbook to RUNBOOK scenario 1, closed clean.
          13:20  ACK-RETRY-BURST   synthetic retry storm, test lane
                 PASS — warning at 10 min as designed; escalated to
                 critical on sustained simulation; vendor escalation
                 contact confirmed current.
          14:40  QUEUE-DEPTH       flagged test messages past threshold
                 PASS — paged; responder's playbook step 2 opened a
                 dashboard link that required pod permissions. Link
                 replaced with Harbor-scoped dashboard. Re-drilled clean.
          15:55  SYNC-MISSED       staleness clock advanced via test toggle
                 PASS — paged on-call + Priti; diagnosis path correct.
All critical alerts fired and answered by Harbor's on-call from the
playbook. Two findings, both fixed and re-drilled same day. Observed:
N. Brooks. Record attached to the gate packet.
```

The playbook the on-call answered from was Harbor's own — every escalation name theirs, the
pod appearing once as "escalation of last resort until Close." Both drill fixes went through
the full loop — specs, the grader, a non-author Checker — in a monitoring week. The loop is
simply how changes happen now, which is exactly what Harbor inherits.

## The retrospective's three outputs

An exhibit from `project-retrospective.md` — the honest cumulative look. The retro argued from
evidence, not adjectives — not "the grader was valuable" but *spec 0016, the bug eleven green
tests hid, dead on a branch*; not "security review was slow" but *2.1 days against 0.9*.
Accepted-as-is ended the engagement at 84% and rising. Three concrete outputs, priorities and
timing attached, feed straight into Close.

| Output | Items |
| ------ | ----- |
| **Technical debt log** | No un-merge path for a wrong claim merge (accepted in spec 0016 by design; revisit Q4 2026) · legacy intake fallback decommission at day 30 (owner: Tom) · modeled surge thresholds (revisit at first CAT event, Priti) |
| **Client-facing improvements** | A twice-weekly committed security-review slot in Dan's calendar, written into the Close handoff — the structural fix for the 2.1-day drift |
| **The harvest list** (4 items for the kit PR) | Config versioned with the release artifact (spec 0046 → kit pipeline starters) · the timezone-boundary test pattern (Build's escaped-bug answer → kit test-writer skill) · the suppression-window-plus-recovery-check alert pattern (this week's replica decision → kit alert template) · the vendor-blip warning/sustained-critical split. Phase C opens the PR. |

The harvest list closes the loop on the standard itself: the suppression-window pattern that
came from Harbor's what-healthy session becomes a kit alert template the next engagement
inherits. A lesson learned once, paid forward.

## The tooling behind this phase

The [Phase 9 deep-dive](phase-9-monitoring.md) describes this work generically. What actually
ran, on the **claude-code-sdlc** plugin and its paired skills:

| What got produced | How |
| ----------------- | --- |
| What-healthy-means decisions | No plugin command — the pod and Harbor's operations, the RUNBOOK scenarios on the wall |
| Production baseline | `/sdlc` → the `performance-benchmarker` agent, measured against the NFR targets over the first hypercare week |
| Monitoring configuration | `/sdlc` → the `doc-updater` agent writes it from the baseline; Rob wires it into Harbor's Azure Monitor workspace by reviewed PR |
| Alert definitions | `/sdlc-coach` → drafted against the phase template; every threshold confirmed by Harbor's operations |
| Incident playbook | `/sdlc-coach` → drafted from the alert table and the RUNBOOK; corrected line by line by Harbor's on-call lead |
| The drill | No plugin command — synthetic triggers agreed with Tom; Harbor's on-call responding; the two fixes rode the loop |
| Retrospective evidence pack | `/sdlc` → the `feedback-synthesizer` agent over hypercare findings and intake feedback · `/visual-explainer` → the evidence visuals |
| Gate, report, advance | `/sdlc-gate` → `check_gates.py` · `/sdlc-phase-report` → `generate_phase_report.py` · `/sdlc-next` → `advance_phase.py --confirmed` (after Karen's sign-off) |

## What Phase C receives

A phase ends by handing the next one a package, not a feeling. Everything below crosses the
boundary into Close & Transfer: the watched system now formally Harbor's, the drilled response,
the honest retrospective, and the questions still open — carried forward under their original
IDs, never silently dropped.

**Crosses into Phase C:** `monitoring-config.md` · `alert-definitions.md` ·
`incident-response.md` · `project-retrospective.md` · `⚠ drill-record.md` · `⚠ close-handoff.md`
(required, unspecified) · `⚠` the harvest list → the Phase C PR.

**The Close & Transfer handoff (summary)** — drafted day 10 by Claude for the Pod Lead to own,
against no template the plugin provides:

| Section | Contents |
| ------- | -------- |
| **Monitoring inventory** | Three dashboards (system / application / business), each with a named Harbor owner; six alerts, all drilled; the playbook cross-referenced to the RUNBOOK |
| **The watch** | Formally Harbor's as of 8/7; the pod one escalation away until Close |
| **Debt log** | Un-merge path (revisit Q4 2026) · legacy fallback decommission (Tom, day 30) · modeled surge thresholds (Priti, first CAT event) |
| **Open items** | The security-review slot change (Dan's calendar, structural fix from the retro) — to be observed working during Close |
| **Harvest list** | Four items for the kit PR (config-with-artifact, timezone test pattern, suppression-window alert pattern, vendor-blip severity split) — Phase C opens it |

**The questions that travel with it:**

| ID | Open question | Owner | Due |
| -- | ------------- | ----- | --- |
| Q-18 | Surge thresholds are modeled from the 2024 CAT dataset — revalidate against the first real catastrophe event | Priti Shah | First real CAT event |
| — | The overall (all-claims) median can't be read fairly until complex claims clear — the first honest reading | Karen Voss + Pod Lead | End of first full quarter |
| — | Legacy intake fallback still warm — decommission once production is proven stable | Tom Reilly | Day 30 post-go-live |

The engagement's credibility was banked, not spent: 1.9 days on fast-path stated with the
overall-median caveat welded on. Phase C is where the client proves it can run all of this
without the pod — the last thing to transfer is the watch itself.

---

Next: [the Phase C worked example](phase-c-example.md) — the close: Harbor's engineers take
the loop, the close gate runs on a HIGH spec with a deadline, access revokes on a checklist,
and the harvest sends four patterns home. The end of the Harbor Mutual story.
