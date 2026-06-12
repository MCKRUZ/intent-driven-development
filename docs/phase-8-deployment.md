# Phase 8: Deployment

Deep-dive on the second phase of the close: promoting the system to production. In this
method, Phase 8 invents nothing — the pipeline has existed since Foundation, the test
environment since the first hardening pass, and every merge for months has deployed itself to
dev through the same rails that will now touch production. What Phase 8 adds is the part
machines must never own: the rollout decision, the rehearsal, and a named human saying
**go** — out loud, on the record, with the rollback plan on the table.

A good Phase 8 is boring. The drama gets spent in rehearsal, where it costs nothing. This is
also the week the engagement's success metric stops being instrumentation and starts being
real: production traffic puts the first true numbers on the clock the client hired us to fix.

> **What closes Phase 8** (full checklist in section 5): the rollback was rehearsed in test by the
> client's own operators, a go/no-go was recorded with every named role asked, the proven artifact
> was promoted to production — not rebuilt — through the pipeline, production smoke passed, and
> monitoring is receiving real data. The single most protected stop: the go/no-go. The failure
> mode to watch (section 6): go/no-go theater — a ceremony where no one could plausibly say no.

**If you're starting here:**

|                          |                                                                                                                                                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The method**           | Claude (the AI coding agent) drafts documents and writes most code. Humans own every decision and verify every result.                                                                                       |
| **The rhythm**           | Numbered phases open and close the engagement; in between ran the continuous build loop. Each phase ends with automated checks (the **gate**) plus a named human sign-off. Gates are the billing milestones. |
| **Where we are**         | Build closed feature-complete; Phase 7 proved the documentation by use. The system runs in dev and test; production exists as code but has never taken real traffic. This week it does.                       |
| **Our pod (4-6 people)** | Pod Lead · Setup Owner · Orchestrators · Quality Engineer. ([Team deep-dive](team.md))                                                                                                                       |

**Words this page leans on** (every other term is explained where it first appears):

| Term                  | What it means                                                                                                                                                                       |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Promotion**         | Moving the same proven artifact up an environment: dev → test → production. The same pipeline, the same code, a different target — never a rebuild, never a hand-copy.              |
| **The release manager** | The named human who owns the promote decision — usually the Setup Owner. One person says go; everyone knows who.                                                                  |
| **Go/no-go**          | The decision ceremony before production: the evidence on the table, every named role asked in turn, and an explicit human decision. The single most protected stop in the standard. |
| **Rollout shape**     | How production traffic arrives: full cutover, a pilot cohort, or a parallel run alongside the old process. A product and operations decision, made by the client, before the ceremony. |
| **Smoke test**        | A fast, non-destructive check that the deployed system actually works — one test per top-priority user journey, reads and harmless writes only. If it can corrupt data, it is not a smoke test. |
| **Rollback**          | The exact, rehearsed procedure that returns production to the previous version — with a written trigger ("roll back if X"), not a judgment call invented mid-incident.              |
| **Hypercare**         | The agreed window right after go-live when the pod watches production deliberately — dashboards open, response times short, the client's operators driving with us beside them.     |
| **Release notes**     | What this release delivers, written for people who didn't build it: features, fixes, limitations, and what (if anything) users must do differently.                                |
| **The rails**         | The enforcement from Phase 3: CI gates, the grader, branch protection, the deploy pipeline. Production deploys ride the same rails as everything else.                              |
| **IaC / Bicep**       | Infrastructure as code — the environments defined in version-controlled files. The production environment is provisioned from the same code that built dev and test.               |

Phase 8 answers four questions, and nothing else:

1. **Is the path to production proven?** (deploy → roll back → redeploy, rehearsed in test —
   a rollback that has never run is a wish, not a plan)
2. **Is the rollout shape decided and owned?** (cutover, pilot, or parallel run — chosen by
   the client's product owner and operations, with the trigger conditions written down)
3. **Did a named human say go?** (the ceremony: evidence presented, every role asked, the
   decision recorded — gates report, humans decide, and this is the decision the rule exists
   for)
4. **Is production verifiably healthy?** (smoke tests green against live endpoints,
   monitoring receiving real data, the first real traffic watched end to end)

New features, alert tuning, and incident-response drills are out of scope — the backlog is
closed, and monitoring is Phase 9's job (this phase only confirms data is flowing). Data
migration is in scope **only** if the engagement scoped it; a migration nobody signed up for
does not sneak in through the deployment door.

---

## 1. Who is involved

Phase 8 is the release manager's phase — usually the Setup Owner, named in writing. But the
hands on the keyboard are deliberately the client's: their platform engineer executes the
promotion the pod rehearsed, because in a few weeks they will do this without us.

### Our side

| Person               | Load   | Workstream                                                                                                                                                 |
| -------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Setup Owner**      | 80-100% | The release manager: owns the checklist, the rehearsal, the secrets rotation, the promote decision at the ceremony. Pairs with the client's platform engineer who executes. |
| **Quality Engineer** | 60-80% | Owns the smoke suite (one journey per top-priority story, non-destructive), the rehearsal evidence, and the production verification after go-live.        |
| **Pod Lead**         | 40-60% | Owns the go/no-go ceremony itself: the roles, the evidence packet, the recorded decision. Routes the rollout-shape decision to the client. Runs steering. |
| **Orchestrators**    | 20-40% | Drive the release-notes and checklist drafting; fix anything the rehearsal surfaces — through the loop, like any change.                                  |

### Client side

| Person                       | Needed for                                                                                                                                | How much            |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| **Platform / DevOps engineer** | Executes the rehearsal and the production promotion with their own permissions — the pod beside them, not on the keyboard               | The week, on and off |
| **Product Owner**            | The rollout shape: who gets the new system, when, and what happens to work in flight. Decided before the ceremony, not at it              | 2-3 hours           |
| **Security**                 | Signs the secrets rotation and the production access list; sits in the ceremony                                                            | 1-2 hours           |
| **Operations / on-call**     | The people who answer the pager: walk the rollback themselves in rehearsal week, sit in the ceremony, drive during hypercare              | 3-4 hours           |
| **Sponsor**                  | The go/no-go (informed, and asked) and the gate steering                                                                                    | 1-2 hours           |

If the client's operators cannot make rehearsal week, the deployment moves — not the
rehearsal. Going live ahead of the people who will run the system is how a successful deploy
becomes next month's incident.

### Claude's role in Phase 8

The least code-writing phase of the engagement, and deliberately so. Claude prepares
evidence; humans make the only decision that matters here.

- **Drafts the release notes from the merged specs.** Every spec since Foundation is a
  feature with a written goal and acceptance checks — the release notes assemble them for an
  audience that never saw a spec: what's new, what's fixed, what's not in this release, what
  users do differently.
- **Drafts the deployment checklist and rollback procedure** from the RUNBOOK Phase 7 proved,
  ordered and observable: every step has an expected outcome and a verification.
- **Runs the smoke suite** against test and, after go-live, against production — and reports
  results per journey, pass/fail, with evidence.
- **Watches the first real traffic** alongside the humans: the first production transactions
  traced end to end against expected behavior.

What Claude never does: deploy to production unattended, decide go or no-go, pick the rollout
shape, or mark its own smoke results as the final word. The go/no-go is the mandatory human
stop the whole standard bends around — **always**, this release and every release after it.

---

## 2. Day one to the last day

The default calendar is **5 business days**, with go-live mid-week — never the last day
before a weekend, because the day after go-live is a working day for finding what go-live
shook loose. It stretches when the rehearsal fails (good — that is its job) or the client's
change-control board adds latency.

**Day 1 — the checklist, the secrets, and the rollout shape.**

- The Phase 7 handoff's deployment checklist gets walked: configuration per environment
  reviewed, the production access list confirmed against least privilege, stakeholder
  notifications drafted with the deployment window.
- **Secrets rotate before go-live.** Everything the pod ever touched gets rotated into
  production-only values the pod cannot read; the client's security signs the rotation. The
  engagement should end with us never having known a production secret.
- The Pod Lead convenes the rollout-shape session; the product owner and operations decide —
  cutover, pilot, or parallel run; what happens to work in flight in the old process; what
  the fallback is and for how long. Written down, with trigger conditions, before any
  ceremony.
- The hypercare window gets agreed with the client's operations the same day — length and
  response expectations written down before the ceremony, so it goes in the packet as a
  commitment, not a courtesy. One to two weeks is the usual shape.

**Day 2 — promote the environment, rehearse the failure.**

- The production environment provisions from the same infrastructure code that built dev and
  test — reviewed like the HIGH-risk change it is, executed by the client's platform
  engineer.
- **The rehearsal, in test: deploy → roll back → redeploy.** The rollback runs for real, by
  the hands that would run it at 2 a.m., from the RUNBOOK Phase 7 cold-verified. A rollback
  that has never executed is a hope; after today it is a procedure with evidence. (The
  evidence: a timestamped timeline of each step — deploy, roll back, redeploy — with the
  outcome of each and the time back to healthy, attached to the go/no-go packet. A failed
  first rehearsal goes in alongside the clean one: found-and-fixed is stronger evidence than
  never-stressed.) Anything the rehearsal breaks gets fixed through the loop and
  re-rehearsed.

**Day 3 — the dress rehearsal and the ceremony.**

- The release candidate deploys to test through the full procedure; the smoke suite runs —
  one journey per top-priority story, non-destructive, results recorded per test. The suite
  is not written this week: the Quality Engineer assembles it from the end-to-end journeys
  the hardening passes already built, trimmed to the non-destructive, test-mode paths.
- **The go/no-go ceremony**, end of day: the evidence packet on the table (rehearsal results,
  smoke results, the rollback trigger, the rollout shape, the notification list), every named
  role asked in turn — release manager, platform engineer, operations, security, product
  owner, quality, sponsor. Anyone can say no, and a no is cheap today. The decision and its
  rationale are recorded with names. Each role answers go, no, or held — a held answer names
  its condition, and the ceremony waits until it is met or it becomes a no. The Pod Lead
  records every answer with the name, the time, and one line of rationale; that record, plus
  the decided window, is the artifact. A go/no-go where no one could plausibly say no is
  theater, and theater here is how outages get scheduled.

**Day 4 — go-live.**

- The promotion runs in the agreed window: the client's platform engineer executes, the
  release manager calls each checklist step, the pod and operations watch the same
  dashboards. The same artifact that passed test goes to production — promoted, not rebuilt.
- Production smoke runs against live endpoints (non-destructive, using the test-mode paths
  built for exactly this (test-mode paths: production endpoints that accept flagged
  synthetic transactions, exercising the full journey without dispatching anything real or
  leaving unflagged records — built during Foundation and Build precisely so production can
  be verified safely)). The Quality Engineer confirms monitoring is **receiving** production
  data — alert tuning is Phase 9, but blind is unacceptable today.
- The first real traffic gets watched end to end, deliberately: the first true transactions
  traced against expected behavior, with the people who own the outcome looking at the same
  screen.

**Day 5 — hypercare day one, then the gate.**

- The agreed hypercare window begins: dashboards open, short response times, the client's
  operators driving with the pod beside them. The first day's findings are triaged like
  anything else — a defect rides the loop; a surprise becomes a Phase 9 alert candidate.
- Release notes go out to the client's stakeholders. The automated gate check runs; the
  Phase 9 handoff is drafted: what was deployed when and where, the current system state,
  what monitoring must cover, known issues, and who to call.
- Steering: the gate sign-off, the billing milestone — and the first production numbers on
  the outcome scorecard, however early.

### When the week stretches

- **The rehearsal fails.** The rollback doesn't roll back, a migration won't reverse, a
  config diverges between test and production. This is the phase working — fix it through
  the loop, re-rehearse, move the window. Never promote past a failed rehearsal.
- **Change control adds a board.** Many clients gate production behind their own process —
  expected; the evidence packet is built to pass it. Surface the latency at steering; don't
  absorb it.
- **The rollout shape unravels late** — operations discovers the parallel-run staffing, or
  the in-flight-work answer, doesn't hold. Better the week stretches than the shape gets
  improvised at the ceremony.
- **Someone says no at the go/no-go.** Then no is the answer. The ceremony exists to make
  that cheap; the date moves, the reason gets fixed, and nobody is ever punished for the no
  that prevented the outage.

---

## 3. The artifacts

> Worked example: [`phase-8-example.md`](phase-8-example.md) — Harbor Mutual's go-live week:
> the rollback rehearsal that failed on Tuesday (and why that was the win), the go/no-go with
> seven names on it, the first real FNOL traced through production on Thursday morning, and
> the clock's first true numbers.

| Artifact                       | Drafted by                                  | Owned by         | Done means                                                                                                            |
| ------------------------------ | -------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Release notes                  | Claude (from the merged specs)               | Pod Lead         | Readable by people who never saw a spec: features, fixes, limitations, what changes for users                          |
| Deployment checklist           | Claude (from the proven RUNBOOK)             | Setup Owner      | Every step ordered, observable, and verified in rehearsal; sign-off lines for the ceremony roles                       |
| Rollback procedure + evidence  | Claude (drafts), client ops (executes)       | Setup Owner      | Executed in test by the client's own operators — deploy, roll back, redeploy — with the trigger condition written down |
| Rollout-shape decision         | Product owner + operations                   | Product Owner    | Cutover/pilot/parallel chosen; in-flight work answered; fallback and trigger conditions recorded                        |
| Smoke results (test + prod)    | Claude (runs), Quality Engineer (owns)       | Quality Engineer | One non-destructive journey per top-priority story, green in both environments, results recorded per test              |
| The go/no-go record            | Pod Lead                                     | Pod Lead         | Every named role asked and answered, decision and rationale recorded — the durable proof a human said go               |
| Secrets rotation record        | Setup Owner + client security                | Client security  | Production secrets rotated to values the pod never held; signed                                                        |
| Phase 9 handoff                | Claude (drafts)                              | Pod Lead         | Deployment summary, system state, monitoring requirements, known issues, escalation contacts                           |

What is deliberately **not** produced: alert definitions and thresholds (Phase 9 sets them
against real baseline data), new features of any kind, and any data migration that was not
explicitly scoped — the deployment door is not where scope arrives.

---

## 4. The cadences

| Rhythm                       | Who                                   | What                                                                                              |
| ---------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Daily 15-minute pod sync** | Whole pod                             | Checklist state, rehearsal findings, the window countdown                                          |
| **The rehearsal**            | Client platform + ops, pod beside them | Deploy → roll back → redeploy in test, by the hands that will own it                              |
| **The go/no-go ceremony**    | All named roles                       | Evidence presented, every role asked, decision recorded — the phase's defining event              |
| **Hypercare**                | Client operators driving, pod beside  | The agreed post-go-live window: dashboards open, findings triaged into the loop or Phase 9        |
| **Steering**                 | Sponsor + Pod Lead                    | Falls at the gate: the deployment record and the first production numbers on the outcome scorecard |

---

## 5. The exit gate

Phase 8 closes when all of these are true:

- [ ] The rollback was executed in test by the client's own operators — deploy, roll back,
      redeploy — before any production promotion
- [ ] The production environment was provisioned from code and the secrets were rotated to
      values the pod never held, signed by client security
- [ ] The rollout shape is decided, written, and owned by the client — including the
      in-flight-work answer and the fallback trigger
- [ ] A recorded go/no-go happened: every named role asked, the decision and rationale on
      record
- [ ] Production deployment succeeded through the pipeline — the same artifact that passed
      test, promoted, not rebuilt
- [ ] Production smoke tests passed: one non-destructive journey per top-priority story
- [ ] Monitoring is receiving production data (tuning comes in Phase 9; blind does not)
- [ ] The first real traffic was traced end to end and matched expected behavior
- [ ] Hypercare is underway on its agreed window, and release notes went to stakeholders
- [ ] The Phase 9 handoff exists: state, monitoring requirements, known issues, escalation
      contacts
- [ ] A named human on each side approved the advance — gates report, humans decide

---

## 6. What goes wrong in Phase 8

- **The Friday deploy.** Going live the last day before a weekend, so the system's first
  hard day happens with nobody watching. Go live mid-week; the day after go-live is a
  working day on purpose.
- **The rollback that was only ever written.** Documented, reviewed, never run — then
  executed for the first time during an incident, where every surprise costs minutes of
  downtime. Rehearse it in test, by the client's own hands, before the ceremony.
- **Go/no-go theater.** The decision was really made days ago; the meeting exists to nod.
  The tell: nobody in the room could plausibly say no. Make the no cheap and the evidence
  real, or the ceremony protects nothing.
- **The rebuilt artifact.** Production gets a fresh build "real quick" instead of the
  promoted artifact that passed test — and now production runs something no environment ever
  verified. Promote, never rebuild.
- **Destructive smoke tests.** A verification step that writes real records into a
  day-old production system. Smoke tests are reads and harmless writes through the test-mode
  paths built for this; anything else is the verification causing the incident.
- **Deploying ahead of the operators.** The system goes live before the people who run it
  have rehearsed, because the date was sacred and their calendar wasn't. The date moves; the
  rehearsal doesn't.
- **Scope through the deployment door.** "While we're at it, migrate the old claims" — a
  migration nobody scoped, attempted under a deadline, against production data. If it wasn't
  scoped, it isn't in this release.
- **Hypercare as a courtesy.** Treating the post-go-live window as optional goodwill instead
  of part of the deployment. The first week of production is where the system meets reality;
  being absent for it forfeits the cheapest learning the engagement will ever get.

---

Back: [Phase 7: Documentation](phase-7-documentation.md) — the docs this week's procedures
were proven against.

Next: [Phase 9: Monitoring](phase-9-monitoring.md) — making production observable: alert
thresholds from real baselines, the drill, and the engagement retrospective.
