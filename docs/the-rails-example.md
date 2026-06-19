# The Rails Worked Example: Harbor Mutual

Companion to [the rails deep-dive](the-rails.md). The rails are not a phase, so this example is
not a calendar. It is **seven episodes** from Harbor Mutual's engagement — each one a real change
meeting a real gate — ordered as they happened, from Build through go-live and hypercare into close.
Together they show the one principle doing its job seven different ways: the agent proposes, a gate
disposes.

**A note on what's real and what's invented.** Three of these episodes run on rails the plugin
ships today: the grader catch (spec 0016) and the rollback that failed in rehearsal (spec 0046) are
drawn straight from the Build and Phase 8 examples, and the correctness-rail refactor (spec 0051) is
new here but rides the plugin's own fifth workflow. The rest exercise pipeline machinery that **is
not in our plugin today**: self-healing CI, the infrastructure what-if/policy/drift gates, the
flaky-test state machine, and per-agent identities. Those are flagged inline as **(net-new to the
kit)** and collected honestly in section 3 — they are exactly what a first agentic-ops-heavy
engagement would build once and harvest back into the kit, not commands you can type today.

> **What's real today.** Episodes 1, 5, and 7 ran on the rails the plugin ships now. Episodes 2, 3,
> 4, and 6 use machinery that is **net-new to the kit** — not commands a pod can type today. The
> honest tally of what's plugin vs. invented is section 3.

**The story so far (you can start here):**

|                  |                                                                                                                                                                                                                       |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The client**   | Harbor Mutual — a fictional regional insurer. A five-person consulting pod is rebuilding how property-insurance claims get reported and decided.                                                                       |
| **The problem**  | A claim takes a median of **11.4 days** from FNOL (first notice of loss — the policyholder reporting the damage) to a coverage decision. Target: **5 days or less.**                                                   |
| **The rails**    | Built in Phase 3: five workflows (ci, grader, correctness, security, deploy-dev), branch protection on `main`, a blocking Stop hook, a Bicep dev environment. Proven on the walking skeleton. Everything since has ridden them.    |
| **Where we are** | These episodes span Build (2026-04-13 to 07-10), the Phase 8 go-live (week of 07-20), Phase 9 hypercare (from 07-27), and into Phase C close (08-17). The rails were built once and never stopped running.                  |
| **Our pod**      | Maya Chen (Pod Lead) · Rob Feld (Setup Owner — owns the rails) · Jonah Kim (Orchestrator, Rob's named deputy) · Sara Whitfield (Orchestrator/Checker) · Nadia Brooks (Quality Engineer).                              |
| **Harbor's cast**| Karen Voss (VP Claims Ops — sponsor) · Luis Ortega (product owner) · Wes Carter (lead engineer, signs HIGH changes) · Tom Reilly (platform engineer — owns branch protection, runners, secrets, the pipeline) · Dan Kowalski (IT security) · Priti Shah (data lead) · Ines Roy (Harbor engineer onboarding into the codebase). |

**Words this page leans on** (everything else is explained where it first appears):

| Term                            | What it means                                                                                                                                          |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The rails**                   | The enforcement taken together: the five CI workflows, branch protection, the deploy pipeline, the infrastructure pipeline. Every change runs on them. |
| **The grader**                  | A fresh AI agent that did **not** write the code; reads the spec and the diff and posts a check-by-check verdict on the PR. Required to run; advises.   |
| **The Stop hook**               | A script that refuses to let an agent finish its turn with a failing build or a red test. Done stops being the agent's opinion.                        |
| **The merge bar**               | What branch protection requires before a PR can merge: CI green, the grader ran, a non-author approval; HIGH adds the security pass + a named sign-off. |
| **Promotion**                   | Moving the **same proven artifact** up an environment (dev → test → prod) — never a rebuild.                                                            |
| **Dry-run / what-if**           | Running a change in read-only preview to see what it *would* do: `bicep what-if` shows exactly what would be created, changed, or deleted.             |
| **Policy-as-code**              | Rules about what infrastructure is allowed (no public storage, encryption on, tags present) written as a gate that runs mechanically on every change.  |
| **Drift**                       | When the real cloud environment no longer matches the code that's supposed to define it — usually because someone changed it by hand.                  |
| **Self-healing CI**             | An agent that, on a red pipeline, diagnoses the failure through bounded tools and proposes a fix **as a PR** — never pushing to a protected branch.    |
| **Least-privilege identity**    | Each actor — human or agent — runs under its own credential scoped to exactly its job. What an agent *can* do is its permissions, not its prompt.       |
| **(net-new to the kit)**        | A piece this example invents to show the rails in action; not in the claude-code-sdlc plugin today. Collected in section 3.                            |

**The IDs you'll see** (stable across phases): **REQ-NN** requirement · **ADR-NN** architecture
decision · **D-NN** product decision · **Q-NN** open question · **NNNN-name.md** a spec file (one
feature, one file in the repo) · **rc-X.Y.Z** a release candidate artifact.

---

## 1. Seven episodes on the rails

> **Reading the Tooling lines.** **You run it** — a slash command you type (e.g. `/sdlc-gate`,
> `/e2e`). **It triggers** — an agent or workflow that runs under the hood, shown after a `→`.
> **No plugin command** — a spec riding the build loop, a workflow firing on the rails, a human
> ceremony, or a piece marked **(net-new to the kit)**; nothing the plugin drives directly. The
> rails run on workflows and the loop, not on commands, so most lines here carry the grey pill —
> and several carry the net-new flag, because the rails deep-dive reaches past what the plugin
> ships today.

### Episode 1 — The merge bar holds: the grader catches what eleven green tests missed

_Build week four · Thursday 2026-05-07 · spec 0016 (duplicate-claim merge), HIGH risk_

**Tooling —** No plugin command. Spec 0016 rides the loop; the PR fires ci.yml + grader.yml;
`risk:high` fires security.yml → the security-reviewer agent; Wes's named sign-off in the PR.

- Spec 0016 implements D-07 — the same loss reported twice becomes one claim, never a rejection.
  Maya tiered it **HIGH**: merging claim records is hard to undo, and a wrong merge mangles two
  policyholders' data. The agent built it under tight permissions; the Stop hook held it to a
  green suite; **eleven tests passed.**
- On the PR, ci.yml went green. Then the **grader** — a fresh agent that did not write the code —
  walked the spec's acceptance checks one by one and flagged the hole the eleven tests never
  covered: two claims with an **empty policy number** were landing in the same match bucket and
  merging into one. Real bug, real data, invisible to a green suite that never thought to test the
  empty-key case.
- The grader **advised; it did not block.** Its verdict was a PR comment. Sara (not the author)
  read it, agreed, and bounced the change back to the same Orchestrator, who fixed the keying on
  the same branch. Every gate — including a fresh grader run — ran again on the updated PR.
- Because HIGH, `risk:high` fired security.yml and **Wes recorded a named sign-off** in the PR
  before merge. Then a non-author merged, and deploy-dev shipped it to dev.

> **The rail that mattered:** the grader (rung 4 of the checking ladder). This is the principle in
> its purest form — an agent produced a confident, green-looking change; a separate gate caught
> what the author was blind to; a human owned the call. Agent proposes, gate disposes.

### Episode 2 — Self-healing CI: a red pipeline gets a proposed fix, and stops there

_Build week six · Tuesday 2026-05-19 · **(net-new to the kit)**_

**Tooling —** No plugin command **(net-new to the kit)** — self-heal.yml → a bounded fix agent
(read/write/run-tests/run-lint only); emits a `fix/` PR, never a merge.

- A scheduled dependency bump landed a minor version of a JSON serializer that changed a default,
  and the nightly build on `main` went red — three integration tests failing on a serialization
  edge. Nothing a human had touched; the kind of break that eats a morning.
- A new kit workflow, **self-heal.yml**, pointed an agent at the failure. It did **not** get the
  repo and a shell. It got a **bounded tool surface** — read a file, write a file, run the tests,
  run the linter — and the failing job's log. It formed a hypothesis (the changed default), made
  the two-line fix, and **re-ran the tests from the environment until they went green.** It proved
  the fix; it did not assert it.
- Then it stopped. It opened a `fix/serializer-default` **pull request** with the diff and a
  one-paragraph explanation, and went no further. It cannot push to `main`; it cannot approve its
  own work. **Sara reviewed the proposed fix, agreed, and merged it** through the same merge bar
  as everything else.
- The agent ran under **its own least-privilege identity** — a workload credential scoped to read
  the repo and open a PR, nothing more. If its prompt had been steered somewhere bad, the identity
  is the wall that was still standing.

> **The rail that mattered:** the merge bar, applied to the pipeline's own repairs. A self-healing
> pipeline that pushed its own fix would have thrown away the only rule that makes it safe.
> Stopping at the PR is the whole design.

### Episode 3 — The flaky test that got quarantined, not "fixed"

_Hardening pass one · Wednesday 2026-05-27 · **(net-new to the kit)**_

**Tooling —** No plugin command **(net-new to the kit)** — the flaky-test state machine
(Active → Quarantined → Disabled) moves the test out of the blocking set; the real fix then rides
the loop.

- The replica refresh-window test — the one guarding the 02:00–04:30 staleness degradation from
  ADR-001 — started failing intermittently. Same code, different result run to run: roughly one PR
  in twelve went red on it, on changes that had nothing to do with the replica. It was beginning
  to block unrelated work.
- The wrong move would have been to point an agent at the red and let it "make it green." A flaky
  test is not always a bug to fix; sometimes it is a test to **quarantine while a human looks.** The
  **flaky-test state machine** moved it from **Active** to **Quarantined** only after it cleared
  eligibility thresholds — failing above a set rate, failing on the default branch, across more
  than one pipeline, not on a single unlucky run — so it stopped gating PRs while staying visible
  and tracked.
- Nadia investigated and found the real cause: the test built its boundary timestamps in local
  time while the service worked in UTC, so runs near midnight Chicago time straddled the window. A
  genuine clock-boundary race, not noise. The **fix rode the loop** like any change — a spec, a
  plan, a non-author Checker — and the test sat under a **grace period** before rejoining the
  blocking suite, so a stale branch couldn't re-break CI the day after the fix.
- The pattern — build time-boundary tests in the service's own clock — went on the harvest list as
  the **timezone test pattern.**

> **The rail that mattered:** triage over reflex. Active → Quarantined → Disabled with eligibility
> gating and a grace period beats "an agent fixes every red test" — which would have papered over a
> real race with a flakier assertion.

### Episode 4 — A HIGH-risk infrastructure change through the funnel

_Hardening pass one · Thursday 2026-05-28 · the test environment · **(net-new gates flagged)**_

**Tooling —** No plugin command **(net-new to the kit)** — iac.yml runs the funnel: schema-validate
→ PSRule policy gate → `bicep what-if` (Tom reads it) → human approval → scoped least-privilege
apply.

- Hardening pass one is where the **test environment** gets added alongside dev. That is a Bicep
  change, and Bicep is HIGH risk every time — hard to undo, and it is the shape production will
  take in Phase 8. Claude drafted the test-environment Bicep; then it went down the funnel, every
  step read-only until the last.
- **Schema validation** passed — the templates compiled against the resource schema. **The
  policy-as-code gate did not:** PSRule flagged two things — a storage account that would have
  defaulted to public network access, and a resource group missing the required cost-center tag.
  Caught mechanically, on the PR, not by a reviewer remembering to look. The agent fixed both; the
  gate went green.
- **`bicep what-if` produced the dry-run** — the exact list of what would be created in the test
  subscription. **Tom read it** before approving: the app hosting, the buffered queue, the private
  endpoint to the replica, the Key Vault — and nothing he didn't expect. An infrastructure change
  approved without reading its what-if is a change approved blind; this one wasn't.
- Only then did the **apply** run, under a **deploy identity scoped to the test resource group and
  nothing else.** The test environment came up from code, the same way dev had — and the same way
  prod would in eight weeks.

> **The rail that mattered:** the infrastructure funnel. Everything before the apply is read-only —
> the policy gate and the what-if did their work while nothing in the cloud had changed yet.

### Episode 5 — Promotion, and the rollback that failed in rehearsal first

_Phase 8 go-live week · 2026-07-20 to 07-23 · rc-1.0.1_

**Tooling —** No plugin command — the rehearsal and the go/no-go are human-run on the rails; spec
0046 rides the loop; `/sdlc-gate` at the Phase 8 boundary.

- **Tuesday, the rehearsal in test:** deploy → roll back → redeploy, run by the hands that would
  run it at 2 a.m. The deploy went fine. **The rollback failed.** The previous artifact came back,
  but a configuration key had moved ahead of it in a separate change, so the rolled-back app booted
  against config it didn't understand. A rollback that had only ever been written would have failed
  exactly here — in production, during an incident, instead of in test on a Tuesday.
- The fix rode the loop as **spec 0046 — configuration versioned with the release artifact**, so a
  promoted build always carries the config it was tested with and a rollback restores both
  together. Re-rehearsed **Wednesday: clean** — deploy, roll back, redeploy, with a timestamped
  timeline attached to the go/no-go packet. The failed first rehearsal went in the packet too:
  found-and-fixed is stronger evidence than never-stressed.
- **Thursday, go-live.** The **same artifact that passed test — rc-1.0.1 — was promoted to
  production, not rebuilt.** Tom executed; the release manager called each step; the pod and
  Harbor's operators watched the same dashboards. Production smoke ran green against live endpoints
  through the test-mode paths. The first real FNOL — a burst pipe, reported on the portal at 08:14
  — produced a coverage recommendation in **3 hours 6 minutes**, against the 11.4-day baseline.
- **Secrets had rotated before go-live** to production-only values the pod could not read; **Dan
  held his go** at the ceremony until the rotation record was attached, then gave it. The
  engagement reached production with the pod having never known a production secret.
- `/sdlc-gate` passed the Phase 8 gate; billing milestone 6.

> **The rails that mattered:** promotion (the proven artifact moved up, never rebuilt) and the
> rehearsed rollback (proven by failing safely in test, not assumed). Plus identity: secrets the
> pod never held.

### Episode 6 — Drift: proposed, never auto-applied

_Phase 9 hypercare · Monday 2026-07-28 · **(net-new to the kit)**_

**Tooling —** No plugin command **(net-new to the kit)** — drift-check.yml runs on a schedule,
compares real infrastructure to the code, and opens a remediation PR; a human decides.

- During a Friday-night hypercare hiccup — a postal-vendor blip causing an acknowledgment-dispatch
  retry burst — an on-call engineer widened a firewall rule on the **test** environment by hand to
  unblock a verification run. It worked, the night ended, and the change lived only in the cloud,
  not in the code.
- Monday morning, the scheduled **drift assessment** caught it: the real test environment no longer
  matched its Bicep. It did **not** silently re-apply the code over the hand change — that would
  have quietly undone something a human did for a reason. It **flagged the drift and opened a
  remediation PR** describing the difference, leaving the decision to a person.
- **Tom made the call.** The widened rule was legitimate and worth keeping, so he **absorbed it into
  the Bicep** rather than reverting — and now the code is the truth again, the proper way. Had the
  change been a mistake, the same PR would have reverted it. Either way: a human chose; the schedule
  only proposed.

> **The rail that mattered:** drift assessment that proposes, never auto-applies — the
> agent-proposes/gate-disposes rule, one more time, on the live environment itself.

### Episode 7 — The correctness rail clears a refactor that changed no behavior

_Phase C close & transfer · Monday 2026-08-17 · spec 0051 (extract the replica-staleness guard), MEDIUM risk_

**Tooling —** No plugin command — spec 0051 rides the loop; the PR fires ci.yml + grader.yml +
**correctness.yml**; Wes's non-author check at the merge bar.

- Close-and-transfer is when the codebase gets tidied for the people inheriting it. The **replica-
  staleness guard** — the 02:00–04:30 degradation rule from ADR-001 — lived in two copies: one on
  the intake path, one on the verification path. Ines, now driving on Harbor's side, had an agent
  **extract it into one shared check** so the client team inherits one hardened copy, not two that
  can drift apart. Same behavior, less surface.
- That is exactly the change a green suite can't vouch for. The tests passed — they always had —
  and the **grader was nearly silent**: there was no new behavior to check against the spec, because
  the spec promised none. A refactor is invisible to "does it meet the spec," and that is precisely
  where a silent regression hides.
- The **correctness rail** did the work. A fresh agent whose one job is _did this diff change
  behavior it shouldn't_ read the extraction against both originals and confirmed the invariant
  survived: the boundary still fired at 02:00 and cleared at 04:30, the degraded-response path was
  byte-for-byte the prior behavior, the check still ran before the call and not after. No drift —
  and it said so on the PR, the verdict that lets a refactor of a correctness-critical guard merge
  with confidence instead of crossed fingers.
- Because the diff was proven equivalent, not assumed so, **Wes (not the author) signed at the merge
  bar** on the strength of the correctness verdict, and every gate re-ran on the final commit before
  merge. The client team inherited one guard instead of two — and the proof that the one still
  behaves like the two it replaced.

> **The rail that mattered:** the correctness review — the no-regression twin of the grader. The
> grader asks _does this meet the spec_; correctness asks _did this break something it shouldn't_.
> On a refactor the spec hasn't moved, so the grader goes quiet and the correctness rail carries the
> load. The agent proposes a "safe" cleanup; the gate proves it is one.

---

## 2. What to notice

- **One sentence held seven times.** A green-looking change (the grader), a broken pipeline (self-
  heal), a flaky test (quarantine), an infra change (the funnel), a production promotion (the
  rollback), a hand-edited environment (drift), a behavior-preserving refactor (the correctness
  rail) — every one stopped the agent at a reviewable artifact and let a human dispose. The rails
  are not seven mechanisms; they are one principle wired into seven places.
- **The grader advises; it does not gate.** It caught the empty-policy-number bug and handed it to
  Sara. A blocking AI verdict would have been faster and worse — a polished, confident explanation
  is exactly how an agent talks a human into the wrong call. Machines gate the mechanical; humans
  own the judgment.
- **Nothing an agent did was unbounded.** The self-heal agent had four named tools and its own
  scoped identity; the deploy identity could touch one resource group; the secrets the pod could
  read were never the production ones. When prompts fail, identity is the wall that holds.
- **Read-only until the last step.** The infrastructure funnel did all its thinking — schema,
  policy, what-if — while the cloud was untouched. The drift check proposed without applying.
  Nothing changed in an environment until a named human had read exactly what would change.
- **A rail proven by failing safely.** The rollback rehearsal failing on Tuesday was the rails
  working, not the rails breaking. The expensive version of that failure is the one that waits for
  an incident.

---

## 3. What was net-new to the kit (the honest part)

Four of these episodes lean on machinery the **claude-code-sdlc plugin does not ship today.** The
plugin's rails are the five workflows (ci, grader, correctness, security, deploy-dev), the grader and
security-reviewer agents, the blocking Stop hook, and branch protection — everything Phase 3
installs and proves. The agentic-pipeline pieces below were invented for this example to show the
rails deep-dive in action. None of them is a command a pod can type now; each is the kind of thing
a first agentic-ops-heavy engagement would build once and **harvest back into the kit.**

| Piece                                | What it is                                                                                                          | In the plugin today?                            |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| **self-heal.yml + bounded fix agent**| On a red pipeline, an agent with a four-tool surface diagnoses, fixes, self-validates, and opens a `fix/` PR — never merges. | **No** — net-new; harvest candidate             |
| **iac.yml funnel gates**             | schema-validate → policy-as-code (PSRule) → `bicep what-if` dry-run → scoped least-privilege apply.                | **Partial** — Phase 3 ships ci/deploy; the policy + what-if gates are net-new |
| **drift-check.yml**                  | Scheduled real-infra-vs-code comparison that **proposes** a remediation PR; never auto-applies.                   | **No** — net-new                                |
| **The flaky-test state machine**     | Active → Quarantined → Disabled, with eligibility thresholds and a post-fix grace period.                          | **No** — net-new                                |
| **Per-agent least-privilege identity** | Each pipeline agent (the fix agent, the deploy identity) runs under its own scoped workload credential.           | **No** — net-new; an Entra Agent ID / federated-credential pattern |

This is the develop-*with*-agents track reaching toward the AI-as-product track. The rails deep-
dive's closing note points at the companion page that will cover autonomous operations in full;
the pieces in this table are where the two tracks first touch.

---

## 4. Artifact: spec 0046 in full (the rollback fix)

**Spec 0046 — Configuration versioned with the release artifact**
Risk tier: **HIGH** · Authored: Jonah Kim · Checked: Sara Whitfield · Security sign-off: Dan
Kowalski · Merged 2026-07-22

**Goal.** A promoted build carries the exact configuration it was tested with, so that a rollback
restores the application **and** its config together, never one without the other.

**Why.** The Tuesday rehearsal rolled back the artifact but not a config key that had moved ahead
of it; the rolled-back app booted against config it didn't understand. Promotion must move one
versioned thing, not an artifact plus a separately-drifting config.

**Scope in.** The release-packaging step, the config bundling, the rollback restore path.
**Scope out.** Application config *values* (those are environment settings, untouched); any change
to what the app reads at runtime.

**Acceptance checks.** A promoted artifact includes its config manifest, content-addressed.
Rollback restores artifact + config as one unit. A redeploy after rollback is byte-identical to
the prior good state. The Tuesday failure mode (config ahead of artifact) cannot recur — proven by
re-running the exact rehearsal.

**How it rode the loop.** Plan approved by Jonah → agent implemented under tight permissions →
Stop hook green → PR fired ci.yml, grader.yml, and (on `risk:high`) security.yml → Dan signed off
→ Sara merged → the Wednesday rehearsal proved it clean. It went into the kit harvest as
**config-with-artifact.**

## 5. Artifact: the infrastructure funnel (iac.yml)

_Net-new to the kit. Drafted by Claude, reviewed by Tom; every step before the apply is read-only._

| Step                       | What runs                                  | Blocks?                              |
| -------------------------- | ------------------------------------------ | ------------------------------------ |
| Schema validate            | `bicep build` against the resource schema  | Hard block on a malformed template   |
| Policy-as-code             | PSRule for Azure (public access, encryption, tags, region) | Hard block on a policy violation     |
| Dry-run                    | `bicep what-if` — the exact change preview | Posted to the PR; a human reads it   |
| Approval                   | A named human approves the what-if         | Required to proceed                  |
| Apply                      | Scoped, least-privilege deploy identity    | — (the only step that changes cloud) |
| Drift assessment (drift-check.yml) | Scheduled real-infra-vs-code compare | Opens a remediation PR; never auto-applies |

## 6. The tooling behind these episodes

| Episode                          | How it ran                                                                                                       |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 1 · Grader catch (0016)          | Spec rides the loop; ci.yml + grader.yml on the PR; security.yml on `risk:high` → security-reviewer agent; Wes's sign-off |
| 2 · Self-healing CI              | **Net-new:** self-heal.yml → a bounded fix agent; opens a `fix/` PR; a non-author merges                         |
| 3 · Flaky-test quarantine        | **Net-new:** the Active/Quarantined/Disabled state machine; the real fix then rides the loop                    |
| 4 · Infra funnel (test env)      | **Net-new gates:** iac.yml schema → PSRule policy → `bicep what-if` (Tom reads) → scoped apply                  |
| 5 · Promotion + rollback         | Human-run rehearsal and go/no-go on the rails; spec 0046 rides the loop; `/sdlc-gate` at the Phase 8 boundary    |
| 6 · Drift proposed               | **Net-new:** drift-check.yml on a schedule → a remediation PR; Tom decides                                       |
| 7 · Correctness-rail refactor (0051) | Spec rides the loop; ci.yml + grader.yml + **correctness.yml** on the PR; Wes's non-author sign-off at the merge bar |

---

Back: [The Rails](the-rails.md) — the deep-dive these episodes illustrate: the five workflows, the
merge bar, deploy and promotion, the infrastructure funnel, and the principle that governs all of
it.
