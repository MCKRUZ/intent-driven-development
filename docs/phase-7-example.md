# Phase 7 Worked Example: Harbor Mutual

The continuation of [the Build loop example](build-loop-example.md), companion to
[the Phase 7 deep-dive](phase-7-documentation.md). Build closed Friday 2026-07-10,
feature-complete: 44 specs merged since Foundation, both hardening passes done, the system
running in Harbor's dev and test environments. The engagement enters the close. This week
answers one question: can Harbor understand, run, and operate this system without us in the
room?

One person joins the story: **Ines Roy**, a Harbor engineer hired three weeks ago, who has
never opened the repo. That is exactly why she was asked — she is this week's most valuable
contributor, because the README is for her.

**The story so far (you can start here):**

|                  |                                                                                                                                                                                                        |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The client**   | Harbor Mutual — a fictional regional insurer. They hired a five-person consulting pod to rebuild how property-insurance claims get reported and decided.                                              |
| **The problem**  | A claim takes a median of **11.4 days** from FNOL (first notice of loss — the policyholder reporting the damage) to a coverage decision. Target: **5 days or less**.                                  |
| **Where we are** | Build is feature-complete: 44 specs merged through the loop since Foundation. The FNOL→decision clock is instrumented; the production needle moves after Phase 8 (Deployment). This week: prove the documentation by use. |
| **The system**   | Portal/phone/email FNOL intake → a buffered claim queue → coverage verification against PolicyOne's nightly **snapshot replica** → fast-path recommendations for simple claims → acknowledgment dispatch. Claims live in a relational model plus an append-only event log. |
| **Our pod**      | Maya Chen (Pod Lead) · Rob Feld (Setup Owner) · Jonah Kim and Sara Whitfield (Orchestrators) · Nadia Brooks (Quality Engineer — this is her phase).                                                  |
| **Harbor's cast**| Wes Carter (lead engineer — inherits the decision record) · Tom Reilly (platform engineer — inherits the operations) · **Ines Roy (new engineer — the cold verifier)** · Luis Ortega (product owner) · Dan Kowalski (IT security) · Karen Voss (sponsor).                  |

**The IDs you'll see on this page:**

| ID         | What it is                                                                                                          |
| ---------- | ----------------------------------------------------------------------------------------------------------------------- |
| **NNNN**   | A spec — one feature in one file, `specs/NNNN-name.md`. Build's last feature spec was 0044.                          |
| **ADR-NN** | Architecture decision record — one hard-to-undo choice, signed by a named human on each side. ADR-001..011 exist entering this week. |
| **REQ-NN** | A requirement from the Phase 1 baseline.                                                                            |
| **C-NN**   | A constraint from Phase 0.                                                                                          |
| **Q-NN**   | An open question with a named owner (Q-18 produced the surge load-test dataset from the 2024 CAT — catastrophe — event, built before the first hardening pass). |
| **NFR-NN** | A non-functional requirement — a measurable quality target.                                                         |

**Words this page leans on** (every other term is explained where it first appears):

| Term                  | What it means                                                                                                                                                      |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Drift**             | A difference between what a Phase 2 contract promised and what the built system does — intentional (needs a documented why) or unintentional (a defect).            |
| **Cold verification** | Proving a document by following it with no help: someone who has never touched the system executes it exactly as written; every stall is a documentation defect.   |
| **RUNBOOK**           | The operations manual written for a reader who is exhausted, stressed, and new to the system, mid-incident: numbered steps, exact commands, a check after each one. |
| **The rails**         | The enforcement from Phase 3 — CI gates, the grader, branch protection, deploy pipeline. Doc PRs ride them like code.                                              |
| **The loop**          | Intent → Delegate → Discern, per spec. Closed for features; still how every fix this week gets made.                                                                |
| **The replica**       | PolicyOne's nightly-refreshed, read-only policy-data copy that coverage checks query — unavailable during its 02:00-04:30 refresh window (found by a Phase 2 spike). |

## 1. How the five days played out

> **Reading the Tooling lines.** **You run it** — a slash command you type (e.g. `/sdlc-gate`,
> `/sdlc-coach`). **It triggers** — an agent or script that command runs under the hood, always
> shown after a `→`. **No plugin command** — a human meeting, a cold run, or a spec riding the
> build loop; nothing the plugin drives directly.

**Monday 7/13 — scope, audiences, and the spec audit.**
**Tooling —** `/sdlc` → the Phase 7 workflow opens with its scoping gate (audiences, existing
docs, client standards) before anything gets written.

- The scope session, with Wes and Tom in the room: three audiences (Harbor engineers, Harbor
  ops, and the adjusters' supervisors for the user-facing guide), four documents to create
  (README, API docs, RUNBOOK, and the user guide for the intake supervisors), and one
  decision that shapes the week — Harbor has no
  documentation standard of its own, so ours becomes theirs, which means it has to stand
  alone.
- What already exists and is current by construction: 44 specs (each updated in the same PR
  as its behavior), ADR-001 through ADR-011, and the harness docs. Nobody writes a "system
  specification" — the spec library *is* the feature documentation, and forking it would
  create a second truth that starts lying within a quarter.
- Nadia runs the trust-but-verify pass: eight specs sampled against live behavior in dev.
  Eight match. The construction held.

**Tuesday 7/14 — the README and the contract diff, in parallel.**
**Tooling —** `/sdlc` → spawns the doc-updater agent (README, from the repo and a fresh
checkout) and the backend-architect agent (API docs, diffed endpoint-by-endpoint against the
Phase 2 contracts) in parallel — they touch nothing shared.

- The README draft comes from the repo as it is, not as anyone remembers it: prerequisites,
  step-by-step local setup, run modes, configuration, and how changes get made (the loop, in
  one page, because Harbor's engineers inherit the loop too). The same stream drafts the
  intake-supervisors' user guide; Luis and Dee Alvarez review it before Friday's gate.
- The diff against the Phase 2 contracts produces the **drift catalog: two entries** (section
  3). Wes reviews it with Maya the same afternoon — one drift gets a documented why, one gets
  a defect spec. A two-entry catalog after fourteen weeks of Build is the loop's discipline
  showing: contracts were carried through specs, so the system mostly *is* the contract.

**Wednesday 7/15 — the RUNBOOK, written for 3 a.m.**
**Tooling —** `/sdlc-coach` → drafts the RUNBOOK against the phase template, from the real
pipeline and Bicep; Rob corrects every procedure — the deploy, rollback, secrets, and scaling
steps are his to get right.

- Five failure scenarios, every one of them earned during the engagement rather than
  imagined: the replica's 02:00-04:30 refresh window (the Phase 2 spike finding that became
  REQ-014's degradation behavior), a failed PolicyOne nightly sync (replica staleness past 24
  hours), storm-surge queue depth (with scale steps sized from the 2024 CAT profile, Q-18's
  dataset), an email-extraction accuracy regression (the eval gate: CI re-runs the
  email-extraction golden set on any AI-behavior change and blocks on degradation — the
  AI-engineering rule that ran all through Build; the scenario covers what it blocks and
  what to do when it fires), and a bad deploy (the rollback, proven in Foundation and at
  both hardening passes).
- Every procedure: numbered steps, exact commands, an observable check after each, a recovery
  path if it fails. Each scenario ends with the alert that should catch it — Phase 9 will
  configure those alerts, and the runbook and the alerts must describe the same failures.
- "See the wiki" and "ask the team" appear zero times. After close, there is no team to ask.

**Thursday 7/16 — the decision sweep, and the defect fix.**
**Tooling —** `/sdlc` → the Explore agent sweeps the Build-era merge history and spec library
for unrecorded decisions; `/sdlc-coach` → drafts the resulting ADRs against the ADR template.
The defect fix is no plugin command — spec 0045 rides the loop.

- The sweep surfaces four candidates; Wes and Rob triage them to two real ones, and Claude
  drafts both ADRs:
  - **ADR-012 — surge queue retry and backoff policy.** Chosen in Build week 9 after a
    near-miss during the first hardening pass; it lived in a PR thread until today. Now it
    has context, options, consequences — and signatures.
  - **ADR-013 — claim-document retention tiering.** A storage-lifecycle choice made with
    Priti Shah — Harbor's data lead — in a Build review; significant, irreversible after
    go-live, and previously written down nowhere.
  - Both co-signed by Rob and Wes, like every ADR before them. The other two candidates are
    struck as implementation detail, recorded as struck. No open ADRs remain.
- The drift defect, spec **0045** (claims-search returns a bare 500 on replica timeout
  instead of the standard error envelope), rides the loop like any change — graded, checked
  by a non-author, merged, deployed to dev — and the API docs and contract now describe one
  truth.

**Friday 7/17 — the cold runs, then the gate.**
**Tooling —** The cold runs are no plugin command — that is the point. Then `/sdlc-gate` →
`check_gates.py` · `/visual-explainer` → the documentation audit for steering ·
`/sdlc-phase-report` → the durable phase record · `/sdlc-next` (after sign-off).

- **The cold checkout, 9:00.** Ines follows the README on a clean machine while Nadia watches
  and the pod stays silent. She stalls at step 4: the local-secrets bootstrap assumes a Key
  Vault read permission that new Harbor engineers don't have by default. Nobody helps her —
  the stall is the data. The fix (a bootstrap script plus a documented access-request path
  with Tom as the named approver) merges before lunch. **The 11:30 re-run is clean,
  end-to-end, forty minutes.** The README failing on a new hire's permissions in week one of
  the close instead of month one of ownership is the phase doing its job.
- **The cold walk-through, 13:00.** Tom executes from the RUNBOOK in dev, with his own
  permissions, the pod silent: a deploy, a rollback, and the simulated replica-window
  incident. One gap — the scale-up procedure named a subscription role the pod holds and
  Harbor doesn't; rewritten with Harbor's actual role names, re-walked clean.
- The gate passes; Karen signs at steering, with the documentation audit on screen and one
  honest line in the record: production topology and alert thresholds are documented as
  Phase 8 and Phase 9 pointers, not as content — they don't exist yet, and the docs say so
  rather than pretend. **Billing milestone 5.** The engagement advances to Deployment.

## 2. What to notice

- **The verifiers were the least qualified people available — on purpose.** Ines had never
  opened the repo; Tom ran procedures he didn't write with permissions the pod doesn't have.
  A README verified by its author's teammate has not been verified.
- **The stall was a success, not an embarrassment.** Step 4 failing under observation cost an
  hour. The same gap discovered by Harbor's next hire, alone, after close, costs a support
  escalation and a dent in trust. The cold run exists to buy failures early.
- **Two drifts after fourteen weeks is the loop's receipt.** Specs changed in the same PR as
  behavior all through Build, so the contract diff found almost nothing — and what it found,
  it found before deployment instead of after.
- **The runbook documents what the engagement learned, not what a template imagines.** The
  refresh window came from a Phase 2 spike; the surge numbers from Q-18's dataset; the
  rollback from rails proven since Foundation. Failure scenarios you've actually rehearsed
  read differently from ones you've guessed.
- **Decision debt got collected while the debtors were still in the room.** ADR-012 lived in
  a PR thread; ADR-013 lived in two people's memory. Both now have signatures from the people
  who'll live with them.
- **The fix rode the loop.** Even in a documentation week, spec 0045 went through intent,
  bounds, the grader, and a non-author Checker. The loop didn't pause because Build ended;
  it's how changes happen now, including ours.

## 3. Artifact: the drift catalog (complete)

| # | Contract said                                                                                       | System does                                                                                                  | Label                                                                                                                                | Resolution                                                                       |
| - | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| 1 | REQ-014 degraded response: coverage check returns `"pending verification"` when the replica is unreachable | Response also carries `staleness_as_of` — the replica's last refresh timestamp                                | **Intentional.** Added in Build week 7 so adjusters could judge how stale "pending" is; Luis approved it at triage; the why is now in the contract changelog | Contract updated; API docs carry the field and the rationale                     |
| 2 | All endpoints return the standard error envelope `{ "error": "<message>" }` on failure              | Claims-search returns a bare 500 with an empty body on replica timeout                                        | **Unintentional.** A timeout path added in Build week 11 bypassed the error middleware; no decision, no why — a defect                | Spec 0045, through the loop Thursday; fixed, graded, merged, deployed             |

Two entries, both resolved inside the week. The catalog is empty at the gate.

## 4. Artifact: RUNBOOK excerpt — failure scenario 1

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

Numbered, copy-pasteable, observable, recoverable — and the first branch is the question a
3 a.m. responder actually needs: *is this the window we already know about?*

## 5. Artifact: the Phase 8 handoff (summary)

- **Inventory:** README (created, cold-verified), API docs (created, diffed, one defect
  fixed), RUNBOOK (created, cold-walked), user guide for intake supervisors (created,
  reviewed by Luis and Dee Alvarez — Harbor's intake supervisor), ADR registry complete
  through ADR-013, spec library current (audited sample 8/8).
- **Honest gaps:** production topology and alert thresholds are pointers to Phases 8 and 9,
  not content; the RUNBOOK's scale procedures are dev/test-proven and get their production
  rehearsal in Phase 8.
- **Deployment checklist:** carried into Phase 8 — secrets rotation before go-live, the
  production Bicep promotion, the go/no-go ceremony roles.
- **ADR status:** none open; ADR-012 and ADR-013 signed this week.

## 6. The tooling behind this phase

The [Phase 7 deep-dive](phase-7-documentation.md) describes this work generically. What
actually ran, on the **claude-code-sdlc** plugin and its paired skills:

| What got produced                       | How                                                                                                                                          |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Documentation scope (audiences, gaps)    | `/sdlc` → the Phase 7 workflow's scoping gate, answered with Wes and Tom in the room                                                         |
| README + user-facing docs                | `/sdlc` → the doc-updater agent, drafting from the repo and a fresh checkout; corrected by what Ines's cold run found                        |
| API docs + drift catalog                 | `/sdlc` → the backend-architect agent, diffing every endpoint against the Phase 2 contracts; humans labeled each drift                       |
| RUNBOOK                                  | `/sdlc-coach` → drafted against the phase RUNBOOK template from the real pipeline and Bicep; Rob corrected; Tom cold-walked                  |
| Decision sweep                           | `/sdlc` → the Explore agent over the Build merge history and spec library; Wes and Rob triaged the candidates                                |
| ADR-012, ADR-013                         | `/sdlc-coach` → drafted against the ADR template; signed by Rob and Wes                                                                      |
| Defect fix (spec 0045)                   | No plugin command — rides the build loop: bounds, plan mode, grader, non-author Checker, deploy-dev                                          |
| The cold runs                            | No plugin command, deliberately: Ines on the README, Tom on the RUNBOOK — observed, unassisted                                               |
| Gate, audit visual, report, advance      | `/sdlc-gate` → `check_gates.py` · `/visual-explainer` → the documentation audit · `/sdlc-phase-report` → the phase record · `/sdlc-next`     |

---

Next: [the Phase 8 worked example](phase-8-example.md) — go-live week: the rollback rehearsal
that fails on Tuesday (and why that was the win), seven names on the go/no-go, and the first
real FNOL through production in 3.1 hours.
