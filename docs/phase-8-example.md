# Phase 8 Worked Example: Harbor Mutual

The continuation of [the Phase 7 example](phase-7-example.md), companion to
[the Phase 8 deep-dive](phase-8-deployment.md). All names and numbers are invented but internally
consistent — the fictional Harbor Mutual engagement.

## What Phase 8 received

Harbor Mutual — a fictional regional insurer — hired a five-person pod to rebuild how
property-insurance claims get reported and decided. A claim takes a median of **11.4 days** from
FNOL (first notice of loss) to a coverage decision; the target is **5 days or less**. Phase 7
closed Friday 2026-07-17 with the documentation cold-verified by Harbor's own people. Deployment
builds nothing new — it starts from what Build proved and what Phase 7 wrote down.

**Inherited from Phase 7 — the deployment starts from these, on disk:**

- `phase8-handoff.md`
- `RUNBOOK.md`
- `README.md`
- `api-docs.md`
- `rc-1.0.0` — the release candidate, already proven in test

**The four things that shape the week.** Nothing about deployment is invented this week. Four rules
from the standard decide how it goes, and not one of them is a machine's to make.

- **Promote, never rebuild.** The exact artifact that passed test is the artifact that takes real
  traffic — `rc-1.0.0`, byte for byte, never a fresh build for production.
- **Rehearse the rollback.** Deploy → roll back → redeploy, run in test by the client's own hands
  before any production promotion. A rollback that has never run is a wish.
- **The client owns the rollout shape.** Cutover, pilot, or parallel run — decided by Harbor in
  writing, with triggers, before the ceremony.
- **Rotate the secrets.** Everything the pod ever touched moves to production-only values the pod
  cannot read — the handoff made literal.

**Where the week is headed.** Five business days, go-live deliberately mid-week — never the last day
before a weekend, because the day *after* go-live is a working day for finding what go-live shook
loose. **Nobody new joins the story.** That is the point of the week: every hand on the keyboard is
a hand that stays after the pod leaves. Tom Reilly executes every promotion; the production access
list never includes a pod member.

> "The system runs in dev and test; production exists as Bicep that has never taken a real claim.
> This week it takes its first."

**Our pod**

| Person | Role |
| ------ | ---- |
| Maya Chen | Pod Lead — owns the go/no-go ceremony |
| Rob Feld | Setup Owner — the release manager this week; owns the checklist |
| Jonah Kim | Orchestrator — ships the rollback fix, spec 0046 |
| Sara Whitfield | Orchestrator — checks the rollback fix |
| Nadia Brooks | Quality Engineer — owns the smoke suite and the production verification |

**Harbor Mutual**

| Person | Role |
| ------ | ---- |
| Tom Reilly | Platform engineer — executes every promotion and both rehearsals |
| Dan Kowalski | IT security — rotates the secrets; holds at the ceremony |
| Luis Ortega | Product owner — owns the rollout shape |
| Dee Alvarez | Intake supervisor — runs intake on the new system, go-live day |
| Karen Voss | Sponsor — signs the gate at steering |
| Harbor on-call lead | Operations — walks the rollback, drives hypercare |
| Wes Carter | Lead engineer — reviews the HIGH-risk Bicep promotion |

**The ID codes, decoded.** Every artifact in this engagement carries a stable identifier, so a
decision made in week two can still be traced in month nine. On this page you'll see four:

| Code | What it is | Born in | Example here |
| ---- | ---------- | ------- | ------------ |
| `NNNN` | A spec — one feature in one file, `specs/NNNN-name.md` | Build | Build closed at 0044; 0045 was Phase 7's defect fix; **0046** is this week's config-versioning fix (test-mode dispatch was built in Foundation as spec 0003) |
| `rc-X.Y.Z` | A release candidate — the exact built artifact, promoted up the environments unchanged | Build / Deploy | **rc-1.0.0** (Tuesday's rehearsal), **rc-1.0.1** (promoted to production Thursday) |
| `C-NN` | A constraint from Phase 0 — a hard limit the system must honor | Phase 0 | **C-04**: two states require claim acknowledgment within 15 business days — now enforced by the system, not by vigilance |
| `Q-NN` | An open question with a named owner | any | **Q-17**: the postal dispatch vendor, live for the first time this week |

Build closed at spec 0044; the backlog is feature-complete. The only new code this week is spec
0046 — the fix the rollback rehearsal forced. Everything else is promotion, not construction.

**Words this page leans on:**

| Term | What it means |
| ---- | ------------- |
| **Promotion** | Moving the same proven artifact up an environment: dev → test → production. Never a rebuild. |
| **Go/no-go** | The decision ceremony before production: evidence on the table, every named role asked in turn, the decision recorded. A human stop, always. |
| **Rollout shape** | How production traffic arrives — Harbor chose cutover-at-intake (below). |
| **Smoke test** | A fast, non-destructive check of a deployed system — one journey per top-priority story, using the test-mode paths, never writing real records. |
| **Rollback** | The exact, rehearsed procedure back to the previous version, with a written trigger condition. |
| **Hypercare** | The agreed window after go-live — Harbor's is two weeks — with dashboards open and Harbor's operators driving, the pod beside them. |
| **The rails** | The enforcement from Phase 3: CI gates, the grader, branch protection, the deploy pipeline. Production rides the same rails. |

## The procedure, step by step

Phase 8 is the least code-writing phase in the standard. The plugin runs a short, mostly
agent-driven sequence; the standard wraps it in the human work a real deployment needs — the
rehearsal, the rollout decision, the secrets rotation, and the one ceremony the whole method bends
around. Below, they're braided: what the tool runs, what the humans do that the tool cannot, and
the file each step leaves behind.

> **State markers.** `▪` a command does it — and writes the file · `▸` a person does it — and it
> is recorded · `⚠` a person does it — and nothing records it.

### Day 1 — Mon 7/20 · plugin Step 0 opens · Step 1: the checklist, the secrets, the rollout shape

Advancing into Phase 8 fires the plugin's first move: a **go/no-go HITL gate** (Step 0) that asks
the human the deployment target, the rollback plan, who to notify, staging-only or production, and
the window. Then Step 1 — Claude drafts the pre-deployment checklist from the proven RUNBOOK, and
the release notes from the merged specs.

**Tooling —** `/sdlc-next` → Step 0 HITL go/no-go; Step 1 drafts checklist + release notes.

**Artifacts out** — under `.sdlc/artifacts/08-deployment/`: `deployment-checklist.md`;
`release-notes.md`; the secrets rotation record (method requires it; no command writes it); the
rollout-shape decision (method requires it; no command writes it).

> ⚠ **The gap:** The plugin fires its *only* go/no-go here — a single `AskUserQuestion`, up front,
> before any rehearsal or smoke evidence exists. The standard's recorded ceremony (seven roles,
> evidence on the table) is Wednesday, after the dress rehearsal. And two of this day's biggest jobs
> — rotating every secret the pod touched, and deciding the rollout shape — are neither plugin steps
> nor plugin artifacts. Human work that today leaves no receipt.

> **At Harbor:** The checklist gets walked top to bottom; the production access list is cut to least
> privilege — two Harbor operators, Tom, the pipeline identity, no pod member. Dan and Tom rotate
> every credential the pod touched to production-only values in Harbor's Key Vault, and Dan signs.
> Luis, Dee, and Harbor's ops decide the rollout shape: **cutover at intake**, a 30-day warm
> fallback, written triggers — sustained intake error rate above 2% for 30 minutes, or verification
> down outside the replica window with the queue still growing.

### Day 2 — Tue 7/21 · plugin Step 1 verify · Step 2: promote the environment, rehearse the failure

The production environment provisions from the same infrastructure code that built dev and test — a
HIGH-risk change, reviewed line by line. Then the rehearsal the standard demands, run in test by the
hands that would run it at 2 a.m.: **deploy → roll back → redeploy**. The plugin's Step 2 spawns
`devops-automator` to deploy against the RUNBOOK; on a build failure it spawns
`build-error-resolver`.

**Tooling —** Step 2 → `devops-automator` (uses `RUNBOOK.md`); the rehearsal (*none — the client's
own hands; no command runs it*).

**Artifacts out —** the rollback rehearsal evidence (the timestamped timeline; no command writes
it); the go decision to promote the env (a human review).

> ⚠ **The gap:** Does the plugin rehearse the rollback? No. Step 1's checklist carries a "Rollback
> verification (deploy → roll back → redeploy)" line, and `rollback-procedure.md` exists as an
> *optional* artifact. But nothing writes the timestamped rehearsal evidence, and nothing requires
> the client's operators to be the ones who run it. The registry's exit gate says the rollback must
> be "rehearsed in test by the client's operators" — an exit criterion for evidence no command
> produces and no required file holds.

> **At Harbor:** Production provisions from the same Bicep that built dev and test — reviewed as the
> HIGH-risk change it is, Rob and Wes on the PR, executed by Tom. Then the rehearsal: the rollback
> **failed**. The previous app revision crash-looped on startup: two config keys added since had
> moved forward independently of the artifact, so the old code didn't know them. That is Tuesday
> doing its job. Jonah opens **spec 0046** — version the app configuration *with* the release
> artifact — and it rides the full loop: plan approved, built, graded, checked by Sara (non-author),
> merged. The RUNBOOK is corrected the same afternoon.

### Day 3 — Wed 7/22 · plugin Step 3 · Step 6 · the ceremony: a clean re-run, the smoke suite, then seven names

The re-rehearsal runs clean — the old revision healthy in under four minutes. The candidate promotes
to test through the full written procedure, and the plugin's Step 3 spawns `e2e-runner` to run the
smoke suite: one non-destructive journey per top-priority story. Then the human work the plugin does
not perform: the **go/no-go ceremony**, evidence packet on screen, every named role asked in turn.

**Tooling —** `/e2e` → `e2e-runner` (test); `/visual-explainer` → the evidence packet; the ceremony
(*none — humans in a room; no command runs it*).

**Artifacts out —** `smoke-test-results.md` (test); `.sdlc/reports/phase08-visual.html`; the
go/no-go record (the seven-role table; no command writes it).

> ⚠ **The gap:** The most protected stop has no required home. The go/no-go is the single most
> protected stop in the standard — yet the plugin's only form for it is `go-no-go-record.md`, marked
> *optional*. The registry's exit gate requires "a recorded go/no-go with every named role asked and
> answered," but the artifact that would hold that record is optional and nothing writes it. The
> seven-role table below is hand-authored.

> **At Harbor:** 16:00. Seven roles asked by name — release manager, platform, operations, security,
> product, quality, sponsor. Six immediate goes. Then Dan Kowalski, security: **held** until the
> secrets-rotation record was *attached* to the packet, not merely referenced — then go. Five minutes
> of friction, which is exactly what a real human stop looks like. Decision: GO. Window Thursday 07:00.

### Day 4 — Thu 7/23 · plugin Step 4 · go-live: the same artifact, now taking real claims

07:00: the promotion runs in the agreed window. The client's platform engineer executes; the release
manager calls each checklist step. The plugin's Step 4 re-spawns `e2e-runner` against the production
target — but the promotion itself is a human's hands, never the AI unattended. The same artifact that
passed test goes to production: **promoted, not rebuilt.**

**Tooling —** `/e2e` → `e2e-runner` (production, test-mode paths); the promotion (*none — Tom
executes, Rob calls the steps*).

**Artifacts out —** `smoke-test-results.md` (production appended); the first real traffic, watched
end to end.

> **At Harbor:** 07:25 production smoke green through the test-mode paths — no real letters
> dispatched, no real records left behind (synthetic warm-up messages pre-loaded so the first thing
> watched is the queue draining correctly). The replica connection is live on its read-only service
> account through a private endpoint, as designed in Phase 2. Monitoring confirmed receiving. 08:14
> the first real FNOL: a burst pipe, reported through the portal, traced end to end — queue entry,
> replica verification (140 ms), fast-path recommendation (single dwelling, no injury, under $25k,
> the 61% case measured back in Phase 1), acknowledgment through the postal vendor (Q-17, live for
> the first time), landing in Gail Tran's queue with a coverage recommendation **3 hours 6 minutes**
> after FNOL. 27 claims by close; the legacy fallback warm and untouched.

### Day 5 — Fri 7/24 · plugin Steps 5–7 · the gate: watch it live, draft the handoff, then a human signs

The two-week hypercare window opens — Harbor's operators driving, the pod beside them. Step 5 drafts
the Phase 9 handoff; Step 6 renders the visual report; Step 7 runs the gate. The gate checks the
files and stops; `advance_phase.py` will not move the engagement forward without a named human's
sign-off.

**Tooling —** `/sdlc-gate` → `check_gates.py`; `/sdlc-phase-report` → `generate_phase_report.py`;
`/sdlc-next` → `advance_phase.py --confirmed`.

**Artifacts out —** `phase9-handoff.md`; `.sdlc/reports/phase08-report.html`; the sponsor's
signature — billing milestone 6.

> ⚠ **The gap:** `check_gates.py` verifies that four files — `release-notes.md`,
> `deployment-checklist.md`, `smoke-test-results.md`, `phase9-handoff.md` — exist, are non-empty, and
> contain no placeholder text. It never enforces the registry's real conditions: *rollback rehearsed
> by the client's operators, a recorded go/no-go, production smoke passing.* Those are surfaced as
> manual review items and never block the exit code. The human is stopped and asked to sign; the
> checklist they should be signing against is never put in front of them.

> **At Harbor:** Day one of hypercare surfaces one finding — an acknowledgment-dispatch retry burst
> during a postal-vendor blip, no claim affected — logged as a Phase 9 alert candidate, not a defect.
> The release notes go out, written for people who never saw a spec: what the new intake does, what
> changes for the claims office, what is *not* in this release (auto-insurance, adjuster-initiated
> merges), and the C-04 acknowledgment clock now enforced by the system rather than by vigilance. The
> gate passes; Karen signs at steering with the first production numbers and the honest caveat.
> Billing milestone 6.

## What Phase 8 produced

The deployment's whole output, named. Blue (`▪`) rows are written by a command and checked by the
gate. **Amber (`⚠`) rows are the method's human work** — required by this standard, produced by no
tool, and today leaving no file behind. For a phase whose signature moves are a rehearsal, a
rotation, and a ceremony, the amber rows are most of what matters.

Key: `▪` a command does it — and writes the file · `▸` a person does it — and it is recorded ·
`⚠` a person does it — and nothing records it.

| Artifact | What it actually is | Written by | Signed by | Lives at | Feeds |
| -------- | ------------------- | ---------- | --------- | -------- | ----- |
| ▪ release-notes.md | What this release delivers, written for people who never saw a spec: features, fixes, limitations, what changes for users | Claude, from the 45 merged specs (Step 1) | Pod Lead | `.sdlc/artifacts/08-deployment/` | Harbor's stakeholders; go-live |
| ▪ deployment-checklist.md | Every step ordered and observable, with an expected outcome and a verification; the rollback procedure lives here as a checklist line | Claude, from the proven RUNBOOK (Step 1) | Setup Owner | `.sdlc/artifacts/08-deployment/` | The promotion; the rollback |
| ▪ smoke-test-results.md | One non-destructive journey per top-priority story, run in test then production, pass/fail per journey with evidence | `/e2e` → `e2e-runner` (Steps 3–4) | Quality Engineer | `.sdlc/artifacts/08-deployment/` | The go/no-go packet; Phase 9 |
| ▪ phase9-handoff.md | Deployment summary, current system state, monitoring requirements, known issues in production, escalation contacts | Step 5 drafts; Pod Lead completes | Pod Lead | `.sdlc/artifacts/08-deployment/` | Phase 9, directly |
| ▪ phase08-report.html · phase08-visual.html | The gate result and artifact inventory, and the rendered go/no-go evidence packet — self-contained HTML | `generate_phase_report.py`; `/visual-explainer` | — | `.sdlc/reports/` | The manual sign-off gate; the ceremony |
| ⚠ rollback rehearsal evidence | The timestamped deploy → roll back → redeploy timeline, run in test by the client's operators, with time-back-to-healthy — the proof the rollback is a procedure, not a wish | **The client's operators, by hand** | Setup Owner | no path — `rollback-procedure.md` is optional; nothing writes the evidence | The go/no-go packet |
| ⚠ rollout-shape decision | Cutover / pilot / parallel chosen; the in-flight-work answer; the fallback and its trigger conditions — owned by the client, in writing, before the ceremony | **Product Owner + operations** | Product Owner | no path — nothing writes it | The go/no-go packet; hypercare |
| ⚠ the go/no-go record | Every named role asked and answered, the decision and its rationale recorded with names — the durable proof a human said go | **Pod Lead, by hand** | Pod Lead | no path — `go-no-go-record.md` is optional; nothing writes it | The exit gate; the audit trail |
| ⚠ secrets rotation record | Production secrets rotated to values the pod never held, signed by the client's security — the handoff made literal | **Setup Owner + client security** | Client security | no path — nothing writes it | The go/no-go packet; Phase C access revocation |

**Read the amber rows again.** Four of the eight things Phase 8 is supposed to produce have nowhere
to live — and they are the four that *are* this phase: the rehearsal that found Harbor's crash-loop,
the rollout decision Luis owns, the ceremony seven people stood in, and the rotation that made the
handoff real. The plugin marks the go/no-go record and the rollback procedure **optional** while its
own registry demands both at the exit gate. **Human work is not the problem. Human work without a
receipt is.**

Deliberately **not** produced in Phase 8: alert definitions and thresholds (Phase 9 sets them
against real baseline data), new features of any kind, and any data migration that was not explicitly
scoped — the deployment door is not where scope arrives.

## A rollback that has never run is a wish, not a plan

On Tuesday the rehearsal rollback failed — the previous app revision crash-looped on startup because
two config keys added since had moved forward independently of the artifact. The fix rode the loop as
spec 0046; Wednesday's re-rehearsal ran clean. This is the evidence timeline, both runs, exactly as
it was attached to the go/no-go packet — the artifact the plugin never writes.

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

> ⚠ **Why Tuesday's failure was the win.** A rollback that fails in rehearsal, by appointment, cost
> an afternoon and produced spec 0046. The same failure during a Thursday-night incident would have
> been an outage with an audience. Both rehearsals went in the evidence packet — the failed one and
> the clean one — because "we found the hole and closed it" is stronger evidence than an unblemished
> record nobody stress-tested. Never promote past a failed rehearsal: fix it, re-rehearse, and move
> the window if you must.

## Artifact: the go/no-go record

Wednesday 16:00. The evidence packet on screen — Tuesday's failed rehearsal and Wednesday's clean one
(both), the smoke results, the rotation record, the rollout shape with its triggers, the notification
list, the window. Seven people asked in turn, by name. This is the record Maya kept — hand-authored,
because the plugin marks it optional and nothing writes it.

| Role | Name | Asked | Answer |
| ---- | ---- | ----- | ------ |
| Release manager | Rob Feld | 16:09 | Go — rehearsal evidence attached (Tue fail + Wed clean), checklist ready |
| Platform | Tom Reilly | 16:10 | Go — I executed both rehearsals; the procedure is mine |
| Operations | Harbor on-call lead | 16:11 | Go — rollback walked by my team, triggers understood |
| Security | Dan Kowalski | 16:18 | **Held** until the rotation record was attached to the packet — then go |
| Product | Luis Ortega | 16:19 | Go — rollout shape and in-flight answer are mine, in writing |
| Quality | Nadia Brooks | 16:20 | Go — smoke green per journey in test; production plan is test-mode only |
| Sponsor | Karen Voss | 16:21 | Go |

**Decision: GO.** Window Thursday 2026-07-23 07:00, maintenance window 90 minutes, fallback trigger
conditions attached. Recorded by Maya Chen.

> ⚠ **Dan's held answer is the ceremony working.** A go/no-go where friction is unwelcome is theater
> — and theater here is how outages get scheduled. Five minutes of "attach the record, don't
> reference it" is what a real human stop looks like. Anyone could have said no, and a no today is
> cheap.

## Check it for real — without the check itself causing the incident

07:25, production smoke green — every journey through the test-mode paths, no real letters dispatched,
no real records left behind beyond flagged test rows. Monitoring confirmed receiving. Then at 08:14
the first real claim arrived, and the room watched it end to end.

**11.4 days → 3h 6m** — median days-to-decision baseline → the first production claim, end to end.

**The smoke suite (test, then production).** One non-destructive journey per top-priority story,
test-mode paths only:

- Portal FNOL to acknowledgment (test mode)
- Phone intake with no policy number routing to manual review
- The fast-path recommendation surfacing to an adjuster queue
- A duplicate report joining its existing claim
- A replica-window degradation showing "pending verification" with its staleness timestamp

All green; results recorded per journey. Monitoring confirmed receiving — the dashboards Phase 3
wired show production telemetry. Tuning the alerts is Phase 9's job; today the requirement is simply
not flying blind.

**The first FNOL, traced.** A policyholder reported a burst pipe through the portal. Queue entry,
replica verification (140 ms), fast-path recommendation (single dwelling, no injury, under $25k — the
61% case), acknowledgment dispatched through the postal vendor (Q-17's integration, live for the
first time), and the claim landed in Gail Tran's queue with a coverage recommendation **3 hours and 6
minutes** after FNOL. Dee's team ran intake all day on the new system; 27 claims arrived by close of
business. The legacy fallback stayed warm and untouched.

> ⚠ **The first number was reported with its caveat.** 3.1 hours against an 11.4-day baseline is a
> thrilling data point — and steering heard "data point," not "result." One good day is a data point,
> not a median; the 5-day target gets judged on the median, in Phase 9 and beyond. The credibility
> spent overclaiming week one is never recovered at close.

## Artifact: the Phase 9 handoff (summary)

Drafted Friday by Claude (Step 5), carried into Monitoring.

- **Deployed:** rc-1.0.1 to production, Thursday 2026-07-23 07:00–07:25, by Harbor's platform
  engineer through the pipeline. Rollout: cutover at intake; legacy fallback warm for 30 days with
  written triggers.
- **System state:** all services healthy; replica verification live; acknowledgment dispatch live
  through the postal vendor; test-mode paths available for ongoing smoke.
- **Monitoring must cover:** the RUNBOOK's five failure scenarios (each names its alert), plus one
  new candidate from hypercare day one — acknowledgment-dispatch retry bursts during vendor blips.
  Thresholds to be set against real baseline data, not guesses.
- **Known issues:** none open; spec 0046 (config versioned with artifact) merged during rehearsal
  week.
- **Escalation:** Harbor on-call first; Tom for platform; the pod during the two-week hypercare
  window; contacts listed with hours.

## What Phase 9 receives

A phase ends by handing the next one a package, not a feeling. Everything below crosses the boundary
into Monitoring: the live system, the deployment record, the verification evidence, and the one
finding hypercare has already surfaced. The Build backlog closed at 0044 — no numbered open question
travels with this handoff; the questions now are thresholds, and those come from measured reality in
Phase 9.

**Crosses into Phase 9:**

- `phase9-handoff.md`
- `release-notes.md`
- `deployment-checklist.md`
- `smoke-test-results.md`
- `RUNBOOK.md` — the five failure scenarios
- `⚠` the go/no-go record + rehearsal evidence
- the first production baseline — a data point, not a median

All names, numbers, and documents are invented but internally consistent — the 11.4-day baseline, the
spec IDs, and the constraint and question IDs trace through every artifact on this page.

## The tooling behind this phase

The [Phase 8 deep-dive](phase-8-deployment.md) describes this work generically. What actually ran, on
the **claude-code-sdlc** plugin and its paired skills:

| What got produced | How |
| ----------------- | --- |
| Deployment checklist + release notes | `/sdlc-next` → Step 1, drafted against the phase templates, from the cold-verified RUNBOOK and the 45 merged specs |
| Secrets rotation | No plugin command — Dan and Tom in Harbor's Key Vault; the signed record goes in the packet |
| Production environment | No plugin command — the same Bicep promoted, HIGH-risk reviewed (Rob + Wes), executed by Tom |
| The rehearsal (and the fix) | No plugin command for the rehearsal — Tom's hands in test; Step 2's `devops-automator` deploys against the RUNBOOK; the fix rides the loop as spec 0046 |
| Smoke journeys (test, then production) | `/e2e` → `e2e-runner`, one journey per top-priority story, test-mode paths only |
| The go/no-go evidence packet | `/visual-explainer` → the packet visual: rehearsals, smoke results, rotation record, rollout shape, triggers |
| The promotion itself | No plugin command, deliberately — Tom executes, Rob calls steps; the plugin prepares evidence, people promote |
| Gate, report, advance | `/sdlc-gate` → `check_gates.py` · `/sdlc-phase-report` → `generate_phase_report.py` · `/sdlc-next` → `advance_phase.py --confirmed` (after Karen's sign-off) |

---

Next: [the Phase 9 worked example](phase-9-example.md) — the two hypercare weeks: alert thresholds
from a real baseline, the drill that catches a silent-night routing typo, and the retrospective that
sends four patterns back into the kit.
