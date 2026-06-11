# Phase 9 Worked Example: Harbor Mutual

The continuation of [the Phase 8 example](phase-8-example.md), companion to
[the Phase 9 deep-dive](phase-9-monitoring.md). Production went live Thursday 2026-07-23;
hypercare is running on its two-week window. Phase 9 runs inside it on purpose: the system is
finally producing real baseline data, and the pod is still beside Harbor's operators while
they take the watch. Two weeks — Monday 2026-07-27 to Friday 2026-08-07 — and the gate falls
the day hypercare ends.

Nobody new joins the story this phase either. The people who answer Harbor's pager are the
people in every session.

**The story so far (you can start here):**

|                  |                                                                                                                                                                                                      |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **The client**   | Harbor Mutual — a fictional regional insurer. They hired a five-person consulting pod to rebuild how property-insurance claims get reported and decided.                                            |
| **The problem**  | A claim took a median of **11.4 days** from FNOL (first notice of loss — the policyholder reporting the damage) to a coverage decision. Target: **5 days or less**.                                 |
| **Where we are** | Live since 7/23 (cutover at intake; legacy fallback warm). Hypercare running. The first real numbers exist; nothing pages anyone yet. This phase: dashboards, alerts derived from real baselines, a drilled response, and the engagement retrospective. |
| **The system**   | Portal/phone/email FNOL intake → buffered claim queue → coverage verification against PolicyOne's nightly **snapshot replica** (unavailable 02:00-04:30 during refresh) → fast-path recommendations → acknowledgment dispatch via the postal vendor.   |
| **Our pod**      | Maya Chen (Pod Lead — this phase is hers, jointly with Harbor's ops) · Rob Feld (Setup Owner) · Jonah Kim and Sara Whitfield (Orchestrators) · Nadia Brooks (Quality Engineer — owns the drill).    |
| **Harbor's cast**| Harbor's on-call lead and operators (they own everything this phase produces) · Tom Reilly (platform engineer) · Priti Shah (data and reporting lead) · Dan Kowalski (IT security) · Luis Ortega (product owner) · Dee Alvarez (intake supervisor) · Karen Voss (sponsor). |

**The IDs you'll see on this page:**

| ID         | What it is                                                                                                  |
| ---------- | ----------------------------------------------------------------------------------------------------------------- |
| **NNNN**   | A spec — one feature in one file. Build closed at 0044; 0045 and 0046 were the close-phase fixes.           |
| **C-NN**   | A constraint from Phase 0 (C-04: two states require claim acknowledgment within 15 business days).          |
| **Q-NN**   | An open question with a named owner (Q-18 produced the surge dataset from the 2024 CAT event).              |
| **NFR-NN** | A non-functional requirement (NFR-02 is the storm-surge capacity target).                                   |

**Words this page leans on** (every other term is explained where it first appears):

| Term                    | What it means                                                                                                                                          |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Baseline**            | What "normal" looks like per metric, measured from real production traffic — what every alert threshold is derived from.                              |
| **Warning vs critical** | Investigate in working hours vs wake someone up.                                                                                                      |
| **The alert drill**     | Firing each critical alert deliberately, in a controlled way, and having Harbor's on-call respond from the playbook while the pod watches silently.   |
| **Incident playbook**   | The detect-diagnose-escalate-communicate companion to the RUNBOOK; the RUNBOOK resolves, the playbook detects and communicates.                       |
| **Hypercare**           | The two-week post-go-live watch, running now — Harbor's operators driving, the pod beside them. Ends with this phase's gate.                          |
| **The harvest**         | The close-of-engagement improvements PR against our own standard and kit. This phase's retrospective decides what goes in it; Phase C opens it.       |

## 1. How the two weeks played out

> **Reading the Tooling lines.** **You run it** — a slash command you type (e.g. `/sdlc-gate`,
> `/sdlc-coach`). **It triggers** — an agent or script that command runs under the hood, always
> shown after a `→`. **No plugin command** — a human session, the drill, or the watch itself;
> nothing the plugin drives directly.

**Days 1-2 (Mon-Tue 7/27-28) — what does healthy mean?**
**Tooling —** No plugin command. The session is the pod and Harbor's operations in a room
with the RUNBOOK's five failure scenarios on the wall.

- For each failure scenario and each top-priority journey: what does healthy look like, what
  does degraded look like, who gets woken, and who merely gets told in the morning. Harbor's
  on-call lead's answers win ties — it is their 3 a.m.
- Two decisions shape everything after:
  - **The replica refresh window must not page.** The 02:00-04:30 unavailability is designed
    behavior (REQ-014 degrades to "pending verification"); an alert that fires every night at
    02:00 trains the on-call to ignore the one that matters. The verification alert gets an
    explicit suppression window — and a companion check that the system *recovered* after
    04:30, which is the part actually worth waking for.
  - **Vendor blips are warnings; sustained bursts are critical.** Hypercare day one already
    showed the acknowledgment dispatcher retrying hard through a brief postal-vendor blip and
    delivering on retry. The system behaving well shouldn't page; the same pattern sustained
    for an hour should.
- Scope lands in writing: everything wires into **Harbor's Azure Monitor workspace** — where
  Tom's team already lives — with paging through their existing rotation. No pod-owned stack.

**Days 3-4 (Wed-Thu 7/29-30) — the baseline and the dashboards.**
**Tooling —** `/sdlc` → the performance-benchmarker agent measures the production baseline
against the NFR targets; the doc-updater agent writes it up as the monitoring configuration.

- The baseline, from the first hypercare week of real traffic, each number with its
  measurement period: portal FNOL submit p95 **410 ms**; replica verification p95 **165 ms**
  (the Phase 2 spike said ~180 — production runs slightly better); intake error rate
  **0.3%**; claim-queue depth steady under **40**; acknowledgment dispatch median **22 min**
  from decision, every one inside the C-04 clock.
- One honest gap, written down rather than papered over: **the surge path has no baseline** —
  late July gave Harbor no storm. Surge thresholds derive from Q-18's modeled dataset (the
  2024 CAT event: peak 1,710 claims/day, nine elevated days) and are **flagged modeled,
  revisit at first real CAT event**, with Priti named on the revisit.
- Dashboards go live in Harbor's workspace, each with a named owner: system health (Tom),
  application health (on-call lead), and the business layer built with Priti in Harbor's own
  reporting language — the FNOL→decision clock, fast-path share, and the C-04 acknowledgment
  compliance, which the system now enforces rather than vigilance.

**Day 5 (Fri 7/31) — the alert definitions.**
**Tooling —** `/sdlc-coach` → drafts the alert table against the phase template; Harbor's
operations confirm every threshold — the named human stop of this phase.

- Six alerts ship (section 3), every threshold derived from the baseline or explicitly
  modeled, every one with a named recipient and a playbook link. The derivation is written
  beside each number: "2x baseline p95 sustained 10 minutes" survives an argument later;
  "500 ms" would not.
- The fatigue review cuts two proposals before they ship: a per-instance CPU alert (not
  actionable — the platform autoscales; Tom watches capacity on the dashboard) and a portal
  latency warning that duplicated the intake error-rate signal. Six actionable beats eight
  ignorable.

**Days 6-7 (Mon-Tue 8/3-4) — the incident playbook.**
**Tooling —** `/sdlc-coach` → drafts the playbook against the phase template, from the alert
table and the RUNBOOK; Harbor's on-call lead corrects it line by line.

- Per alert: what it means, the first three diagnosis steps, P1/P2/P3 classification, the
  escalation names (Harbor names — the pod appears only as "escalation of last resort until
  Close"), and the communication templates: what the claims office hears from Dee's team
  when intake degrades, what leadership hears at P1, who says it.
- The playbook detects and communicates; for resolution it points into the cold-verified
  RUNBOOK rather than duplicating it — one source of truth per failure, two lenses on it.

**Day 8 (Wed 8/5) — the drill.**
**Tooling —** No plugin command, deliberately. Synthetic triggers agreed with Tom; Harbor's
on-call responds from the playbook; Nadia observes, silent.

- Every critical alert fires for real, one at a time, through controlled synthetic triggers:
  replica reads blocked outside the window (VERIFY-DEGRADED), a synthetic retry storm against
  the dispatch queue's test lane (ACK-RETRY-BURST at its critical threshold), queue depth
  pushed past threshold with flagged test messages (QUEUE-DEPTH), a staleness clock wound
  forward in the test toggle (SYNC-MISSED).
- **Two failures, both the drill's job to find.** VERIFY-DEGRADED routed to the general ops
  channel instead of the pager rotation — a routing-key typo that would have meant a silent
  night during a real incident. And one playbook diagnosis step opened a dashboard link that
  assumed pod permissions — the same class of gap Tom caught in the Phase 7 RUNBOOK walk,
  caught again by the same method. Both fixed; both re-drilled clean by end of day.
- The drill record — every alert, trigger time, detection time, responder, outcome — goes in
  the gate packet.

**Day 9 (Thu 8/6) — the retrospective.**
**Tooling —** `/sdlc` → the feedback-synthesizer agent assembles the hypercare findings and
intake-team feedback · `/visual-explainer` → the evidence pack the room argues from. The
candor is no plugin command.

- Half a day, the pod plus Harbor's core people, arguing from receipts: the metrics history,
  the Retro+ log, every escaped bug with its "which check should have caught it?" answer,
  the gate records.
- **What worked, with evidence:** the grader's 0016 catch (the bug that eleven green tests
  hid, dead on a branch); Tuesday's failed rollback rehearsal (an outage bought at rehearsal
  prices, and spec 0046 out of it); the decision-list clock (Luis answered 31 of 34 items
  inside two days — the three late ones each stalled a spec, which is the argument for the
  clock, not against it); accepted-as-is ending at **84%** and rising.
- **What didn't, without blame:** the security-review queue drifted all engagement (2.1-day
  median in Build against a 0.9-day general queue) — the concrete fix is structural, not
  exhortative: a twice-weekly committed security-review slot in Dan's calendar, written into
  the Close handoff. And four escaped bugs total across the engagement, each already
  answered at its Retro+ with a harness change — the retro confirms the answers held.
- **The technical debt log,** priorities and timing attached: no un-merge path for a wrong
  claim merge (accepted in spec 0016 by design — auto-merge is conservative precisely
  because of this; revisit Q4 2026); the legacy intake fallback decommission at day 30
  (owner: Tom, date on the calendar); the modeled surge thresholds (revisit at first CAT
  event, Priti).
- **The harvest list** — what the next engagement inherits through the kit: config versioned
  with the release artifact (spec 0046's pattern → the kit's pipeline starters); the
  timezone-boundary test pattern (Build's escaped-bug answer → the kit's test-writer skill);
  the suppression-window-plus-recovery-check alert pattern (this week's replica decision →
  the kit's alert template); and the vendor-blip warning/sustained-critical split. Phase C
  opens the PR.

**Day 10 (Fri 8/7) — hypercare ends, the gate.**
**Tooling —** `/sdlc-gate` → `check_gates.py` · `/sdlc-phase-report` → the phase record ·
`/sdlc-next` (after sign-off).

- The watch hands over deliberately: dashboards, the pager rotation, and the playbook are
  formally Harbor's; the pod stands one escalation away until Close. Hypercare closes on its
  agreed date — two weeks, as written, not a quiet forever.
- The gate passes; Karen signs at steering. The outcome metric gets its first honest
  production read: **fast-path claims (61% of volume) decided at a median of 1.9 days** over
  the two live weeks, against the 11.4-day all-claims baseline — stated with its caveats, in
  writing: complex claims opened since go-live are mostly still in flight, so the *overall*
  median cannot be read yet and gets its first fair reading after a full quarter. C-04
  acknowledgment compliance: 100%, system-enforced. **Billing milestone 7.** The engagement
  advances to Close & Transfer.

## 2. What to notice

- **The suppression window is the deepest decision of the phase.** An alert that fires every
  night at 02:00 doesn't just annoy — it trains Harbor's on-call to ignore the alert that
  matters. Knowing what must *not* page is the operations knowledge the session existed to
  capture, and it came from Harbor's side of the table.
- **Every threshold can explain itself.** "2x measured p95 over 10 minutes" survives the
  argument in six months when someone wants to change it. The one set from modeled data says
  so on its face, with a named revisit. No number in the table "felt right."
- **The drill caught the silent-night bug.** A routing-key typo is invisible in review and
  catastrophic at 3 a.m. It cost ten minutes at drill prices — the same economics as the
  rollback rehearsal and the cold runs, applied to the pager.
- **The retro argued from receipts.** Not "the grader was valuable" but *0016, eleven green
  tests, dead on a branch*. Not "security review was slow" but *2.1 days against 0.9*. The
  evidence pack is what keeps a retrospective from being a feelings meeting.
- **The first metric read was underclaimed on purpose.** 1.9 days on fast-path is a
  spectacular number, and steering heard it with the overall-median caveat welded on. The
  pod banks credibility here that Phase C spends.
- **The fixes rode the loop to the end.** The routing fix and the playbook correction went
  through specs, the grader, and a non-author Checker in a monitoring week — the loop is
  simply how changes happen now, which is exactly what Harbor inherits.

## 3. Artifact: the alert table (as shipped)

| Alert              | Condition (derivation)                                                                                    | Severity            | Pages              |
| ------------------ | ---------------------------------------------------------------------------------------------------------- | ------------------- | ------------------ |
| VERIFY-DEGRADED    | Replica read failures sustained 5 min **outside 02:00-04:30** (suppression window + post-window recovery check) | Critical            | On-call rotation   |
| SYNC-MISSED        | Replica staleness > 24 h (nightly sync failed)                                                            | Critical            | On-call + Priti    |
| QUEUE-DEPTH        | Claim queue > 400 sustained 15 min (10x measured normal of ~40; **modeled** vs Q-18 surge curve — revisit at first CAT event) | Warning → critical at 1,200 | On-call rotation   |
| INTAKE-ERROR-RATE  | > 2% sustained 30 min (matches the Phase 8 fallback trigger — one number, two documents)                  | Critical            | On-call + Dee notified |
| ACK-RETRY-BURST    | Dispatch retries > 3x baseline per 10 min: warning; sustained 60 min: critical (hypercare day-one finding) | Warning → critical  | On-call; vendor escalation path |
| EVAL-GATE-DRIFT    | Email extraction accuracy < 95% on the golden set (the ADR-004 gate, now watched in production)           | Warning             | Quality owner (Harbor) |

Cut at the fatigue review: per-instance CPU (not actionable under autoscale), portal latency
warning (duplicated INTAKE-ERROR-RATE's signal).

## 4. Artifact: the drill record (excerpt)

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

## 5. Artifact: the Close & Transfer handoff (summary)

- **Monitoring inventory:** three dashboards (system / application / business), each with a
  named Harbor owner; six alerts, all drilled; the playbook cross-referenced to the RUNBOOK.
- **The watch:** formally Harbor's as of 8/7; the pod one escalation away until Close.
- **Debt log:** un-merge path (revisit Q4 2026) · legacy fallback decommission (Tom, day 30)
  · modeled surge thresholds (Priti, first CAT event).
- **Open items:** the security-review slot change (Dan's calendar, structural fix from the
  retro) — to be observed working during Close.
- **Harvest list:** four items for the kit PR (config-with-artifact, timezone test pattern,
  suppression-window alert pattern, vendor-blip severity split) — Phase C opens it.

## 6. The tooling behind this phase

The [Phase 9 deep-dive](phase-9-monitoring.md) describes this work generically. What actually
ran, on the **claude-code-sdlc** plugin and its paired skills:

| What got produced                  | How                                                                                                                              |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| What-healthy-means decisions        | No plugin command — the pod and Harbor's operations, the RUNBOOK scenarios on the wall                                            |
| Production baseline                 | `/sdlc` → the performance-benchmarker agent, measured against the NFR targets over the first hypercare week                       |
| Monitoring configuration            | `/sdlc` → the doc-updater agent writes it from the baseline; Rob wires it into Harbor's Azure Monitor workspace by reviewed PR    |
| Alert definitions                   | `/sdlc-coach` → drafted against the phase template; every threshold confirmed by Harbor's operations                               |
| Incident playbook                   | `/sdlc-coach` → drafted from the alert table and the RUNBOOK; corrected line by line by Harbor's on-call lead                     |
| The drill                           | No plugin command — synthetic triggers agreed with Tom; Harbor's on-call responding; the two fixes rode the loop                  |
| Retrospective evidence pack         | `/sdlc` → the feedback-synthesizer agent over hypercare findings and intake feedback · `/visual-explainer` → the evidence visuals |
| Gate, report, advance               | `/sdlc-gate` → `check_gates.py` · `/sdlc-phase-report` → the phase record · `/sdlc-next` (after Karen's sign-off)                 |

---

Next: [the Phase C worked example](phase-c-example.md) — the close: Harbor's engineers take
the loop, the close gate runs on a HIGH spec with a deadline, access revokes on a checklist,
and the harvest sends four patterns home. The end of the Harbor Mutual story.
