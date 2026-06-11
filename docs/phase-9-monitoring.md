# Phase 9: Monitoring

Deep-dive on the third phase of the close: making production observable, making the alerts
real, and writing down what the engagement learned. Phase 9 runs **inside the hypercare
window on purpose** — the system is finally producing the one thing alert thresholds must be
built from (real baseline data), and the pod is still in the room while the client's
operators take the controls.

The phase has a second job that matters as much as the first: the **engagement
retrospective**. The weekly Retro+ answered "which check should have caught it?" all through
Build; Phase 9 asks the cumulative version — what worked, what didn't, what the next
engagement inherits — and produces the raw material for the harvest that closes the loop on
the standard itself.

**If you're starting here:**

|                          |                                                                                                                                                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The method**           | Claude (the AI coding agent) drafts documents and writes most code. Humans own every decision and verify every result.                                                                                       |
| **The rhythm**           | Numbered phases open and close the engagement; in between ran the continuous build loop. Each phase ends with automated checks (the **gate**) plus a named human sign-off. Gates are the billing milestones. |
| **Where we are**         | The system is live — Phase 8 promoted it through a rehearsed pipeline and a recorded go/no-go. Hypercare is running. This phase makes production observable, drills the response, and captures what the engagement learned. |
| **Our pod (4-6 people)** | Pod Lead · Setup Owner · Orchestrators · Quality Engineer. ([Team deep-dive](team.md))                                                                                                                       |

**Words this page leans on** (every other term is explained where it first appears):

| Term                    | What it means                                                                                                                                                              |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Baseline**            | What "normal" looks like for each key metric, measured from real production traffic — the number every alert threshold is derived from. Never an intuition, never a round number that "feels right." |
| **Alert**               | A condition that demands a human response. Every alert is actionable; a notification nobody acts on is noise wearing an alert's badge.                                     |
| **Warning vs critical** | Two thresholds per alert: warning means investigate during working hours; critical means wake someone up. The difference is who suffers if it waits until morning.         |
| **Alert fatigue**       | What happens when alerts fire often and mean little: the team learns to ignore them, and then misses the real one. The standing rule: fires more than once a week without action — raise the threshold or delete the alert. |
| **The alert drill**     | Deliberately triggering each critical alert in a controlled way and having the client's on-call respond from the playbook. An alert that has never fired is a wish — the same rule the rollback rehearsal enforced in Phase 8. |
| **Incident playbook**   | The detect-diagnose-communicate companion to the RUNBOOK: what each alert means, first diagnosis steps, who escalates to whom, and what to tell users while it's happening. |
| **Hypercare**           | The agreed post-go-live window (running now): dashboards open, the client's operators driving, the pod beside them. Phase 9's gate falls at its end.                       |
| **Retro+**              | The weekly Build ceremony where every escaped bug got "which check should have caught it?" answered with a harness change. Phase 9's retrospective is its cumulative finale. |
| **The harvest**         | The mandatory close-of-engagement improvements PR against our own standard and kit — generalized skills, corrected templates, patterns worth repeating. Phase 9's retrospective produces its raw material; Phase C opens the PR. |
| **The outcome metric**  | The one number the client hired us to move (fixed in Phase 0, instrumented since Foundation). This phase gives it its first honest production read — with the caveats stated. |

Phase 9 answers four questions, and nothing else:

1. **Can the client see the system?** (dashboards with owners, every top-priority feature
   observable, business metrics alongside system metrics)
2. **Will the right person find out, at the right urgency?** (alerts derived from measured
   baselines, routed to named people, covering every critical failure mode the RUNBOOK
   describes)
3. **Does the response actually work?** (the incident playbook, proven by drill — detected,
   diagnosed, communicated by the client's own on-call)
4. **What did the engagement learn?** (the honest retrospective: product, process, debt, and
   the patterns the kit inherits)

New features, alert tooling migrations, and the formal handover of the harness are out of
scope — the backlog stays closed, the client's existing monitoring stack is the one we wire
into, and Close & Transfer is the next phase's job. Defects surfaced by hypercare ride the
loop, as ever.

---

## 1. Who is involved

Phase 9 is the Pod Lead's phase jointly with the client's operations — because the central
session of the week, "what does healthy mean?", cannot be answered by either side alone. The
pod knows what the system does; operations knows what 3 a.m. is like in this company.

### Our side

| Person               | Load   | Workstream                                                                                                                                                 |
| -------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pod Lead**         | 60-80% | Runs the what-healthy-means session, owns the retrospective, routes threshold decisions to the named owners, runs the gate and steering.                  |
| **Quality Engineer** | 60-80% | Owns observability coverage (every top-priority feature has at least one metric someone watches), the alert-fatigue review, and the drill design.          |
| **Setup Owner**      | 50-70% | Wires dashboards and alert rules into the client's stack; owns the baseline capture; keeps every monitoring change versioned and reviewed like the harness change it is. |
| **Orchestrators**    | 20-40% | Drive the drafting (alert definitions, playbook, dashboard config); fix what hypercare and the drill surface — through the loop.                          |

### Client side

| Person                  | Needed for                                                                                                                            | How much             |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| **Operations / on-call** | Co-author what healthy means; receive the routing; **respond to the drill from the playbook** — they own all of this in a few weeks   | The thread of the phase |
| **Platform engineer**   | Wires alert channels and paging into their tooling; confirms the dashboards live where their team already looks                        | 3-4 hours            |
| **Data / reporting lead** | The business-metric dashboards: the outcome metric and its honest caveats, in the client's own reporting language                     | 2-3 hours            |
| **Security**            | The security alert lane: what pages security directly, bypassing the general queue                                                      | 1-2 hours            |
| **Product Owner**       | Confirms the business metrics measure what the business means by them                                                                   | ~1 hour              |
| **Sponsor**             | The gate steering: the first honest production read of the outcome metric, caveats included                                            | 45 min               |

If operations cannot co-author the thresholds, the phase produces our alerts in their
tooling — which become noise the week we leave. The session is the phase; protect it like
Phase 7 protected the cold runs.

### Claude's role in Phase 9

- **Establishes the baseline from production data.** Response times, throughput, error
  rates, queue depths, resource usage — measured against the NFR targets, captured as the
  reference every threshold derives from.
- **Drafts the alert definitions** — condition, severity, recipient, response time, runbook
  link — with each threshold derived from the measured baseline (alert at a stated multiple
  of normal, never at a number that felt right), and the derivation written down.
- **Drafts the incident playbook** from the RUNBOOK's failure scenarios: same failures,
  different lens — the RUNBOOK resolves; the playbook detects, classifies, and communicates.
- **Drafts the retrospective's evidence base.** The engagement's own records — the metrics
  dashboard history, the Retro+ log, the escaped-bug answers, the gate records — assembled
  so the humans argue from facts, not vibes.

What Claude never does: confirm a threshold (the named human stop of this phase — every
threshold is confirmed against real baseline data by the people who'll be paged), declare
the drill passed, or soften the retrospective. An honest retro written by a flattering
drafter is worthless; the humans own the candor.

---

## 2. Day one to the last day

The default calendar is **two weeks, deliberately inside hypercare** — week one needs the
production baseline to accumulate; week two needs the pod still present for the drill. The
gate falls at hypercare's end, closing both together.

### Week one — see the system

**Days 1-2 — what does healthy mean?**

- The session that shapes the phase: the pod and the client's operations walk the RUNBOOK's
  failure scenarios and the top-priority user journeys and answer, for each, what healthy
  looks like, what degraded looks like, and who should be woken for what. Operations'
  answers win ties — they are the ones being paged.
- The monitoring scope lands in writing: which stack (theirs — we wire into what their team
  already watches), which dashboards, which alert channels, who owns each dashboard. A
  dashboard without a named owner is decoration.

**Days 3-4 — the baseline and the dashboards.**

- The production baseline gets captured from the first hypercare weeks' real traffic:
  request rates, latency percentiles, error rates, queue depths, dependency health — each
  recorded with the period it was measured over. Where production hasn't yet exercised a
  path (the seasonal surge, the rare failure), the threshold derives from the engagement's
  modeled data instead — **flagged as modeled, with a revisit date**, never silently
  presented as baseline.
- Dashboards go live in the client's stack: system health, application health, and the
  business layer — the outcome metric and what feeds it — in the client's own reporting
  language, co-built with their data lead.

**Day 5 — the alert definitions.**

- Every critical failure mode from the RUNBOOK gets its alert; every alert gets a condition
  derived from the baseline, a severity, a named recipient, a response expectation, and a
  link to its playbook entry. The derivation is written next to the threshold — "2x the
  measured p95 over 10 minutes" survives an argument; "500ms" does not.
- The alert-fatigue review runs on everything proposed: anything that would have fired more
  than once a week during hypercare without demanding action gets raised or cut now, not
  after the team has learned to ignore it.

### Week two — prove the response, and learn

**Days 6-7 — the incident playbook.**

- The playbook gets written against the alert table: per alert, what it means, the first
  three diagnosis steps, the severity classification, the escalation names, and the
  communication templates — what users and stakeholders are told, by whom, while it's
  happening. It cross-references the RUNBOOK rather than duplicating it: the playbook
  detects and communicates; the RUNBOOK resolves.

**Day 8 — the alert drill.**

- Each critical alert fires for real, triggered in a controlled way, and the client's
  on-call responds from the playbook while the pod observes silently — the same discipline
  as Phase 7's cold runs and Phase 8's rehearsal. Routing that goes to the wrong channel, a
  playbook step that assumes pod access, a threshold that doesn't actually trigger: all of
  it fails here, by appointment, at drill prices.
- What the drill breaks gets fixed through the loop and re-drilled.

**Day 9 — the retrospective.**

- A half-day, the pod plus the client's core people, arguing from the assembled evidence:
  what worked (with the receipts), what didn't (without blame), which gates caught real
  issues and which were rubber-stamped, which artifacts earned their cost and which were
  written and never read.
- Three outputs, all concrete: the **technical debt log** (every known shortcut, with a
  priority and a suggested timing — logged debt is managed, unlogged debt is a future
  crisis), the **client-facing improvements** (what Harbor's team changes about how they run
  the system and the loop), and the **harvest list** — the patterns, skills, hook
  improvements, and template corrections the next engagement inherits through the kit.
  Phase C opens the harvest PR; this day decides what goes in it.

**Day 10 — hypercare ends, the gate.**

- Hypercare closes on its agreed date with a deliberate handover of the watch: the client's
  operators have been driving for two weeks; now the dashboards, the pager, and the playbook
  are formally theirs, with the pod one escalation away until Close.
- The automated gate check runs; the Close & Transfer handoff is drafted: monitoring
  inventory, the drill record, the debt log, open items with owners. Steering: the gate
  sign-off, the billing milestone, and the outcome metric's first honest production read —
  stated with its caveats, because the credibility protected all engagement gets spent or
  banked here.

### When the two weeks stretch

- **The baseline is too thin.** Two quiet weeks may not exercise the paths that matter.
  Thresholds on unexercised paths ship as modeled-with-revisit-date; the phase does not wait
  for a storm to make the numbers honest.
- **The drill fails badly** — routing wrong, playbook unusable, the on-call lost. Good:
  better at drill prices. Fix, re-drill, and if the gap is people rather than config, say so
  at steering — Close & Transfer cannot paper over an operations team that isn't ready.
- **The retrospective gets political.** A candid finding lands on someone's toes. The retro
  is for the teams, not for performance reviews — the Pod Lead holds that line, and the
  written artifact records findings, not names attached to blame.
- **Hypercare keeps finding defects.** Each rides the loop; a steady stream is a quality
  finding that belongs in the retrospective, not a reason to quietly extend hypercare
  forever. Extend deliberately, with the sponsor, or close on schedule.

---

## 3. The artifacts

> Worked example: [`phase-9-example.md`](phase-9-example.md) — Harbor Mutual's two weeks: the
> what-healthy-means session, thresholds derived from a real baseline (and the surge
> thresholds honestly flagged as modeled), the drill where the retry-burst alert from
> hypercare day one fires on cue, and the retrospective that sends two patterns back into
> the kit.

| Artifact                  | Drafted by                                  | Owned by              | Done means                                                                                                       |
| ------------------------- | -------------------------------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Monitoring configuration  | Claude (drafts), Setup Owner (wires)         | Setup Owner → client  | Dashboards live in the client's stack, each with a named owner; every top-priority feature observable             |
| Production baseline       | Claude (measures)                            | Quality Engineer      | Normal recorded per key metric with its measurement period; modeled values flagged with revisit dates             |
| Alert definitions         | Claude (drafts), ops (confirm)               | Client operations     | Every critical failure mode covered; every threshold derived from baseline and confirmed by the people being paged |
| Incident playbook         | Claude (drafts), ops (correct)               | Client operations     | Detect-diagnose-escalate-communicate per alert; templates included; cross-referenced to the RUNBOOK               |
| The drill record          | Quality Engineer                             | Quality Engineer      | Every critical alert fired and answered by the client's on-call from the playbook; failures fixed and re-drilled  |
| Engagement retrospective  | Claude (evidence base), humans (the candor)  | Pod Lead              | Product and process findings with receipts; debt log; harvest list — concrete items, not platitudes               |
| Close & Transfer handoff  | Claude (drafts)                              | Pod Lead              | Monitoring inventory, drill record, debt log, open items with owners                                              |

What is deliberately **not** produced: a parallel monitoring stack of our own (we wire into
theirs), alerts for things nobody would act on, and a sanitized retrospective for external
consumption — the steering gets the summary; the teams keep the honest version.

---

## 4. The cadences

| Rhythm                        | Who                                  | What                                                                                            |
| ----------------------------- | ------------------------------------ | --------------------------------------------------------------------------------------------------- |
| **Daily 15-minute pod sync**  | Whole pod                            | Hypercare findings, baseline capture state, drill prep                                          |
| **Hypercare watch**           | Client operators driving, pod beside | Continues throughout; its findings feed thresholds and the debt log                             |
| **What-healthy-means session**| Pod + client operations              | The phase's defining event, week one: healthy, degraded, and who gets woken, per failure mode  |
| **The alert drill**           | Client on-call responding, QE observing | Week two: every critical alert fired and answered from the playbook                          |
| **The retrospective**         | Pod + client core team               | Week two: the honest cumulative look, from evidence — produces the debt log and the harvest list |
| **Steering**                  | Sponsor + Pod Lead                   | Falls at the gate: the watch handover, the drill record, the outcome metric's first honest read |

---

## 5. The exit gate

Phase 9 closes — and hypercare ends with it — when all of these are true:

- [ ] Every top-priority feature has at least one observable metric on a dashboard with a
      named owner
- [ ] Every critical failure mode in the RUNBOOK has an alert; every threshold is derived
      from the measured baseline (or explicitly flagged as modeled, with a revisit date) and
      confirmed by the client's operations
- [ ] The alert-fatigue review ran: nothing ships that would fire weekly without demanding
      action
- [ ] The incident playbook covers every critical alert — detection, diagnosis, escalation
      names, communication templates
- [ ] The drill happened: every critical alert fired in a controlled way and was answered by
      the client's own on-call from the playbook; what failed was fixed and re-drilled
- [ ] The watch was handed over: dashboards, paging, and the playbook are formally the
      client's, with the pod one escalation away until Close
- [ ] The retrospective exists with receipts: findings, the technical debt log, and the
      harvest list — concrete, honest, owned
- [ ] The outcome metric has its first production read on the scorecard, caveats stated
- [ ] The Close & Transfer handoff exists: monitoring inventory, drill record, debt log,
      open items with owners
- [ ] A named human on each side approved the advance — gates report, humans decide

---

## 6. What goes wrong in Phase 9

- **Thresholds by intuition.** "500ms feels right" is not engineering. Measure the baseline,
  alert at a stated multiple, write the derivation down. A threshold that can't explain
  itself can't be tuned later.
- **Our monitoring, their pager.** The pod builds alerts in its own image, in a stack the
  client's team doesn't watch, routed by assumptions. The week we leave, it's noise. Their
  stack, their names, their session.
- **Alert fatigue shipped on day one.** Fifty alerts feels thorough and guarantees the team
  ignores all of them within a month — and then misses the real one. Fewer, actionable,
  derived, reviewed.
- **The undrilled pager.** Routing and playbooks that have never fired, discovered broken
  during the first real incident. The drill is to alerts what the rehearsal was to rollback:
  the difference between a procedure and a wish.
- **The dashboard nobody owns.** A beautiful screen no one reviews is decoration. Every
  dashboard has a named owner or it doesn't ship.
- **Monitoring the system but not the business.** All RED metrics, no outcome metric — the
  client can see requests but not whether the thing they bought is working. The business
  layer is co-built with their data lead, in their language.
- **The platitude retrospective.** "Great teamwork, communicate better next time" — written
  for management, useless to everyone. Honest, specific, evidence-backed, or skip the
  meeting and admit it.
- **Debt left unlogged.** The shortcuts everyone knows about but nobody wrote down become
  next year's crisis with no paper trail. Logged debt is managed debt; the log is a gate
  item for a reason.
- **Hypercare that never ends.** Quietly extending the watch because closing feels risky.
  Extend deliberately with the sponsor and a new end date, or close on schedule — an
  open-ended hypercare is a handoff that's failing in slow motion.

---

Back: [Phase 8: Deployment](phase-8-deployment.md) — the go-live this phase makes observable.
