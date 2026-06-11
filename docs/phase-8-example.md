# Phase 8 Worked Example: Harbor Mutual

The continuation of [the Phase 7 example](phase-7-example.md), companion to
[the Phase 8 deep-dive](phase-8-deployment.md). Phase 7 closed Friday 2026-07-17 with the
documentation cold-verified by Harbor's own people. The system runs in dev and test;
production exists as Bicep that has never taken a real claim. This week it takes its first —
and the 11.4-day clock Harbor hired the pod to fix meets production traffic for the first
time.

Nobody new joins the story. That is the point of this week: every hand on the keyboard is a
hand that stays after the pod leaves.

**The story so far (you can start here):**

|                  |                                                                                                                                                                                                       |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **The client**   | Harbor Mutual — a fictional regional insurer. They hired a five-person consulting pod to rebuild how property-insurance claims get reported and decided.                                              |
| **The problem**  | A claim takes a median of **11.4 days** from FNOL (first notice of loss — the policyholder reporting the damage) to a coverage decision. Target: **5 days or less**.                                  |
| **Where we are** | 44 feature specs built and verified; documentation proven by use in Phase 7. Production has never seen real traffic. This week: rehearse the failure, hold the ceremony, go live.                     |
| **The system**   | Portal/phone/email FNOL intake → a buffered claim queue → coverage verification against PolicyOne's nightly **snapshot replica** → fast-path recommendations for simple claims → acknowledgment dispatch (test-mode capable, built in Foundation as spec 0003). |
| **Our pod**      | Maya Chen (Pod Lead) · Rob Feld (Setup Owner — the **release manager** this week) · Jonah Kim and Sara Whitfield (Orchestrators) · Nadia Brooks (Quality Engineer).                                  |
| **Harbor's cast**| Tom Reilly (platform engineer — executes every promotion) · Dan Kowalski (IT security) · Luis Ortega (product owner — owns the rollout shape) · Dee Alvarez (intake supervisor) · Wes Carter (lead engineer) · Karen Voss (sponsor).                          |

**The IDs you'll see on this page:**

| ID         | What it is                                                                                                |
| ---------- | --------------------------------------------------------------------------------------------------------------- |
| **NNNN**   | A spec — one feature in one file, `specs/NNNN-name.md`. Build closed at 0044; Phase 7's defect fix was 0045. |
| **C-NN**   | A constraint from Phase 0 (C-04: two states require claim acknowledgment within 15 business days).        |
| **Q-NN**   | An open question with a named owner (Q-17 was the postal dispatch vendor, resolved in Foundation).        |

**Words this page leans on** (every other term is explained where it first appears):

| Term                  | What it means                                                                                                                                                |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Promotion**         | Moving the same proven artifact up an environment: dev → test → production. Never a rebuild.                                                                |
| **Go/no-go**          | The decision ceremony before production: evidence on the table, every named role asked in turn, the decision recorded. A human stop, always.                |
| **Rollout shape**     | How production traffic arrives — Harbor chose cutover-at-intake (below).                                                                                     |
| **Smoke test**        | A fast, non-destructive check of a deployed system — one journey per top-priority story, using the test-mode paths, never writing real records.             |
| **Rollback**          | The exact, rehearsed procedure back to the previous version, with a written trigger condition.                                                              |
| **Hypercare**         | The agreed window after go-live — Harbor's is two weeks — with dashboards open and Harbor's operators driving, the pod beside them.                          |
| **The rails**         | The enforcement from Phase 3: CI gates, the grader, branch protection, the deploy pipeline. Production rides the same rails.                                |

## 1. How the five days played out

> **Reading the Tooling lines.** **You run it** — a slash command you type (e.g. `/sdlc-gate`,
> `/sdlc-coach`). **It triggers** — an agent or script that command runs under the hood, always
> shown after a `→`. **No plugin command** — a human ceremony, a rehearsal, or work executed by
> Harbor's own hands; nothing the plugin drives directly. Deployment is the most human phase in
> the standard: the plugin prepares evidence; people promote.

**Monday 7/20 — the checklist, the secrets, and the rollout shape.**
**Tooling —** `/sdlc-coach` → drafts the deployment checklist (from the cold-verified RUNBOOK)
and the release notes (from the 45 merged specs) against the phase templates. The rotation and
the rollout session are no plugin command.

- The Phase 7 handoff's checklist gets walked top to bottom: per-environment configuration
  reviewed, the production access list cut to least privilege (two Harbor operators, Tom, and
  the pipeline's identity — no pod member holds production write access).
- **Secrets rotate.** Every credential the pod ever touched gets rotated into
  production-only values held in Harbor's Key Vault; Dan executes the rotation with Tom and
  signs the record. From today, there is no production secret the pod has ever seen.
- **The rollout shape**, decided in a two-hour session with Luis, Dee, and Harbor's ops:
  **cutover at intake** — from go-live, every *new* FNOL in every channel enters the new
  system; claims already in flight finish in the legacy process and drain where they started
  (no migration — none was scoped, none sneaks in). The legacy intake stays warm as a
  fallback for 30 days, with written triggers: sustained intake error rate above 2% for 30
  minutes, or verification down outside the replica window with the queue still growing.
  Luis owns the decision; it goes in the go/no-go packet in writing.

**Tuesday 7/21 — promote the environment, rehearse the failure (and find one).**
**Tooling —** No plugin command. The Bicep promotion and the rehearsal are Tom's hands; the
fix rides the loop as spec 0046.

- Production provisions from the same Bicep that built dev and test — reviewed as the
  HIGH-risk change it is (Rob and Wes on the PR), executed by Tom.
- **The rehearsal, in test: deploy → roll back → redeploy. The rollback fails.** The previous
  app revision comes back up — and crashes on startup, because two configuration keys added
  since that revision are required by the *current* config and unknown to the old code.
  Config had been moving forward independently of the artifact. The fix (spec 0046): version
  the app configuration **with** the release artifact, so config rolls back when the revision
  does; the RUNBOOK's rollback procedure gets the corrected steps the same day.
- This is Tuesday doing its job: a rollback that fails in test, in rehearsal, by appointment,
  costs an afternoon. The same failure on Thursday night would have been an outage with an
  audience. Wednesday morning's re-rehearsal runs clean: deploy, roll back (old revision
  healthy in under four minutes), redeploy.

**Wednesday 7/22 — the dress rehearsal and the ceremony.**
**Tooling —** `/e2e` → the Playwright smoke journeys against test · `/visual-explainer` → the
go/no-go evidence packet. The ceremony itself is no plugin command, deliberately.

- The release candidate promotes to test through the full written procedure — the same
  procedure, the same hands, that production will get. The smoke suite runs: one
  non-destructive journey per top-priority story — portal FNOL to acknowledgment (test
  mode), phone intake with no policy number routing to manual review, the fast-path
  recommendation surfacing to an adjuster queue, a duplicate report joining its claim, a
  replica-window degradation showing "pending verification" with its staleness timestamp.
  All green; results recorded per journey.
- **The go/no-go, 16:00.** The evidence packet on screen: Tuesday's failed rehearsal and
  Wednesday's clean one (both — the failure is evidence the procedure is now real), the
  smoke results, the rotation record, the rollout shape with its triggers, the notification
  list, the window. Seven people asked in turn, by name: Rob (release manager), Tom
  (platform), Harbor's on-call lead (operations), Dan (security), Luis (product), Nadia
  (quality), Karen (sponsor). **Dan holds his answer** until the rotation record is attached
  to the packet rather than referenced — five minutes of friction, exactly the kind the
  ceremony exists to make cheap. Seven goes, recorded with names and rationale. Window:
  Thursday 07:00, before the claims office's morning peak.

**Thursday 7/23 — go-live.**
**Tooling —** No plugin command for the promotion — Tom executes, Rob calls each step.
`/e2e` → the production smoke journeys (test-mode paths only).

- 07:00: the promotion runs. The same artifact that passed test moves to production —
  promoted, not rebuilt. Each checklist step gets called, executed, verified: services
  healthy, the replica connection live (read-only service account, private endpoint, as
  designed in Phase 2), the queue draining its synthetic warm-up messages.
- 07:25: production smoke green — every journey through the test-mode paths, no real letters
  dispatched, no real records left behind beyond flagged test rows.
- Monitoring confirmed **receiving**: the dashboards Phase 3 wired show production telemetry.
  Tuning the alerts is Phase 9's job; today the requirement is simply not flying blind.
- **08:14: the first real FNOL.** A policyholder reports a burst pipe through the portal.
  The room watches it end to end: queue entry, replica verification (140 ms), fast-path
  recommendation (single dwelling, no injury, under $25k — the 61% case), acknowledgment
  dispatched through the postal vendor (Q-17's integration, live for the first time), and
  the claim lands in Gail's queue with a coverage recommendation **3 hours and 6 minutes**
  after FNOL. The clock that read 11.4 days has a production data point.
- Dee's team runs intake all day on the new system; 27 claims arrive by close of business.
  The legacy fallback stays warm and untouched.

**Friday 7/24 — hypercare day one, then the gate.**
**Tooling —** `/sdlc-gate` → `check_gates.py` · `/sdlc-phase-report` → the phase record ·
`/sdlc-next` (after sign-off). Hypercare is no plugin command — it is people watching
dashboards together.

- Hypercare begins on its agreed two-week window, Harbor's operators driving. Day one
  surfaces one finding: the acknowledgment dispatch queue retried more aggressively than
  expected during a brief postal-vendor blip — no claim affected, letters delivered on
  retry, but the retry burst is exactly what an alert should catch. It becomes a named alert
  candidate in the Phase 9 handoff rather than a defect: the system behaved; the visibility
  should improve.
- Release notes go to Harbor's stakeholders — written for people who never saw a spec: what
  the new intake does, what changes for the claims office, what is not in this release
  (auto-insurance, adjuster-initiated merges), and the C-04 acknowledgment clock now
  enforced by the system rather than by vigilance.
- The gate passes; Karen signs at steering with the first production numbers on the
  scorecard — 27 claims day one, first fast-path recommendation in 3.1 hours — and the
  honest caveat attached: one good day is a data point, not a median; the 5-day target gets
  judged on the median, in Phase 9 and beyond. **Billing milestone 6.** The engagement
  advances to Monitoring.

## 2. What to notice

- **Tuesday's failure was the week's most valuable event.** The rollback failing in
  rehearsal, by appointment, cost an afternoon and produced spec 0046. The same failure
  during a Thursday-night incident would have been an outage. The rehearsal exists to buy
  failures at rehearsal prices.
- **Both rehearsals went in the evidence packet.** The failed one and the clean one — because
  "we found the hole and closed it" is stronger evidence than an unblemished record nobody
  stress-tested.
- **Dan's held answer is the ceremony working.** A go/no-go where friction is unwelcome is
  theater. Five minutes of "attach the record, don't reference it" is what a real human stop
  looks like.
- **The pod never touched production.** Tom executed every promotion; the access list never
  included a pod member; the secrets rotated to values the pod has never seen. The handoff
  isn't a future phase — it has been happening since Foundation, and this week it was simply
  true.
- **The same artifact moved up.** What ran in test on Wednesday is byte-for-byte what took
  Harbor's first claim on Thursday. Every "quick rebuild for prod" is an unverified system
  wearing a verified one's badge.
- **The first number was reported with its caveat.** 3.1 hours against an 11.4-day baseline
  is a thrilling data point — and steering heard "data point," not "result." The credibility
  spent overclaiming week one is never recovered at close.

## 3. Artifact: the go/no-go record

| Role            | Name                  | Asked   | Answer                                                                  |
| --------------- | --------------------- | ------- | ------------------------------------------------------------------------ |
| Release manager | Rob Feld              | 16:09   | Go — rehearsal evidence attached (Tue fail + Wed clean), checklist ready |
| Platform        | Tom Reilly            | 16:10   | Go — I executed both rehearsals; the procedure is mine                   |
| Operations      | Harbor on-call lead   | 16:11   | Go — rollback walked by my team, triggers understood                     |
| Security        | Dan Kowalski          | 16:18   | **Held** until the rotation record was attached to the packet — then go  |
| Product         | Luis Ortega           | 16:19   | Go — rollout shape and in-flight answer are mine, in writing             |
| Quality         | Nadia Brooks          | 16:20   | Go — smoke green per journey in test; production plan is test-mode only  |
| Sponsor         | Karen Voss            | 16:21   | Go                                                                        |

**Decision: GO. Window Thursday 2026-07-23 07:00, maintenance window 90 minutes, fallback
trigger conditions attached. Recorded by Maya Chen.**

## 4. Artifact: the rollback rehearsal evidence (timeline)

```
Tue 7/21  14:02  Test env: deploy release candidate rc-1.0.0      OK (9 min)
          14:31  Execute RUNBOOK rollback to previous revision    FAIL
                 Previous revision crash-looped on startup: required
                 config keys (added wk 9, wk 12) absent from old code,
                 present in current app configuration. Config had moved
                 forward independently of the artifact.
          15:10  Spec 0046 opened: version app configuration WITH the
                 release artifact (config snapshot per revision; rollback
                 restores both). Rides the loop: plan approved, built,
                 graded, checked by non-author, merged.
          17:40  RUNBOOK rollback procedure corrected; deploy-test green.
Wed 7/22  08:05  Re-rehearsal: deploy rc-1.0.1                    OK (8 min)
          08:19  Rollback to previous revision + its config       OK (3 min 52 s,
                 old revision Healthy)
          08:31  Redeploy rc-1.0.1                                OK (8 min)
                 Procedure executed end-to-end by Tom Reilly. Evidence
                 (logs + timings) attached to the go/no-go packet.
```

## 5. Artifact: the Phase 9 handoff (summary)

- **Deployed:** rc-1.0.1 to production, Thursday 2026-07-23 07:00-07:25, by Harbor's
  platform engineer through the pipeline. Rollout: cutover at intake; legacy fallback warm
  for 30 days with written triggers.
- **System state:** all services healthy; replica verification live; acknowledgment dispatch
  live through the postal vendor; test-mode paths available for ongoing smoke.
- **Monitoring must cover:** the RUNBOOK's five failure scenarios (each names its alert),
  plus one new candidate from hypercare day one — acknowledgment-dispatch retry bursts
  during vendor blips. Thresholds to be set against real baseline data, not guesses.
- **Known issues:** none open; spec 0046 (config versioned with artifact) merged during
  rehearsal week.
- **Escalation:** Harbor on-call first; Tom for platform; the pod during the two-week
  hypercare window; contacts listed with hours.

## 6. The tooling behind this phase

The [Phase 8 deep-dive](phase-8-deployment.md) describes this work generically. What actually
ran, on the **claude-code-sdlc** plugin and its paired skills:

| What got produced                     | How                                                                                                                                      |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Deployment checklist + release notes   | `/sdlc-coach` → drafted against the phase templates, from the cold-verified RUNBOOK and the 45 merged specs                              |
| Secrets rotation                       | No plugin command — Dan and Tom in Harbor's Key Vault; the signed record goes in the packet                                              |
| Production environment                 | No plugin command — the same Bicep promoted, HIGH-risk reviewed (Rob + Wes), executed by Tom                                             |
| The rehearsal (and the fix)            | No plugin command for the rehearsal — Tom's hands in test; the fix rides the loop as spec 0046                                           |
| Smoke journeys (test, then production) | `/e2e` → Playwright journeys, one per top-priority story, test-mode paths only                                                           |
| The go/no-go evidence packet           | `/visual-explainer` → the packet visual: rehearsals, smoke results, rotation record, rollout shape, triggers                             |
| The promotion itself                   | No plugin command, deliberately — Tom executes, Rob calls steps; the plugin prepares evidence, people promote                            |
| Gate, report, advance                  | `/sdlc-gate` → `check_gates.py` · `/sdlc-phase-report` → the phase record · `/sdlc-next` (after Karen's sign-off)                        |

---

Next: [the Phase 9 worked example](phase-9-example.md) — the two hypercare weeks: alert
thresholds from a real baseline, the drill that catches a silent-night routing typo, and the
retrospective that sends four patterns back into the kit.
