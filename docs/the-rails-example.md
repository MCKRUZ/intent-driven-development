# The Rails Worked Example: Harbor Mutual

Companion to [the rails deep-dive](the-rails.md). The rails are not a phase, so this example is not a
calendar. It is the worked **Example** track: what a pull request carries in, the five rails it rides,
what a cleared merge leaves behind, and seven episodes of the rails doing their job — each one a real
change meeting a real gate, showing the one principle seven different ways: the agent proposes, a gate
disposes.

## What rides the rails

Harbor Mutual — a fictional regional insurer — hired a five-person pod to rebuild how
property-insurance claims get reported and decided. A claim takes a median of **11.4 days** from FNOL
(first notice of loss) to a coverage decision; the target is **5 days or less**. The rails have no
calendar and no exit gate. They have a **merge bar**, and one thing arrives at it: a **pull request
from one spec**. One spec = one branch = one PR. This page walks what that PR carries in, the five
rails it rides, and what it leaves behind when it clears.

**What arrives at the bar** — the reviewable artifact and its context:

- `specs/NNNN-name.md`
- the diff (base … HEAD)
- risk tier — from `risk-tier-map.md`
- the co-authored commits (who, or what, wrote each line)

### The spec, the diff, the tier

Three things define a change before a single rail fires.

- **The spec.** A committed file, `specs/NNNN-name.md`, that rides in the PR's own diff — so intent
  and implementation sit in one view. The grader reads *this file*, not the PR description, as the
  authority on what the change was for.
- **The diff.** Everything the branch changed against `main`. A deterministic helper
  (`diff-anchors.sh`) turns it into a changed-line set the AI reviewers must anchor every finding to —
  no drifting, no skimming.
- **The risk tier.** HIGH / MEDIUM / LOW, assigned from the Phase-3 `risk-tier-map.md`. A HIGH change
  (or one touching a gated path) pulls in the security rail and a named sign-off; the tier is what
  decides how hard the change is gated.

### Before the rails: the local hooks

The rails are server-side, on the PR. But two gates fire earlier, on the agent's own machine, and they
are part of the story: **done means the hook lets you stop.**

- **The Stop hook** (`stop-gate.ps1`) refuses to let the agent end its turn on a red build — the
  environment's green, not the agent's opinion.
- **The review gate** (`review-gate.ps1`) refuses a push until `/code-review` and `/simplify` receipts
  exist for the exact commit.

> **The coverage boundary the hooks admit.** A hook only fires for actions taken through Claude Code. A
> human pushing from their own terminal sails past it — which is exactly why the same checks run again,
> server-side, as required rails. A rail that only holds when the well-behaved actor cooperates is not
> a rail.

### The cast

**The rails (automated actors)**

- `ci.yml` — build-and-test; the mechanical floor; hard block
- `grader.yml` — a fresh agent's verdict against the spec; advises
- `correctness.yml` — a fresh agent hunts logic defects; blocks on one
- `security.yml` — the security-reviewer on gated paths / `risk:high`; blocks on HIGH
- `deploy-dev.yml` — ships the merged artifact to dev; rolls back on failure

**The humans at the bar**

- **Maya Chen** — Pod Lead
- **Rob Feld** — Setup Owner; owns the rails as a product; merges none of it alone
- **Jonah Kim** — Rob's named deputy; reads every rails change
- **Sara Whitfield** — Orchestrator / Checker; the non-author at the merge bar
- **Nadia Brooks** — Quality Engineer; proves each rail fails safely
- **Tom Reilly** — Harbor platform; owns branch protection, runners, secrets
- **Wes Carter** — Harbor lead engineer; signs HIGH changes
- **Karen Voss** — VP Claims Ops; sponsor
- **Luis Ortega** — product owner
- **Dan Kowalski** — IT security; signs at go-live
- **Priti Shah** — data lead
- **Ines Roy** — Harbor engineer onboarding into the codebase (drives the Phase C refactor)

### The codes and labels, decoded

The rails run on a small vocabulary of stable IDs and GitHub labels. A change's identity, its tier,
and every override it uses are all one of these:

| Code / label | Means | Where it acts |
| --- | --- | --- |
| `NNNN-name.md` | A spec file — one feature, one branch, one PR | The grader reads it as the authority on intent |
| `risk:high` | A PR label declaring the change HIGH risk | Fires `security.yml`; adds a named sign-off to the bar |
| `accepted-risk:correctness` | A PR label recording an audited correctness override | Lets `correctness.yml` pass a BLOCK verdict |
| `gate-exception` | The label on a true emergency merge past a gate | Needs the Pod Lead + one human + a Retro+ item |
| `ADR-NN` | An architecture decision record — a signed choice | ADR-001 the replica staleness rule (02:00–04:30) |
| `REQ-NN` · `D-NN` · `Q-NN` | Requirement · product decision · open question | D-07 duplicate-merge; REQ-019 fast path; Q-15 replica access |
| `rc-X.Y.Z` | A release-candidate artifact — the proven bytes | rc-1.0.1 promoted to prod, never rebuilt (Phase 8) |

The required-check *names* are the job names, not the file names: `build-and-test`, `grader`,
`correctness-review`, `security-review`. Rename a job and you must rename its required-status-check
context in `branch-protection.json` or the bar stops enforcing it.

## The five rails, in order

A PR fires all five rails. Two **block** mechanically (a machine's call), two **advise or block on a
defect** (an AI agent's call, scaffolded so it is checkable), and one **ships**. Confusing block with
advise is how a team either ships unreviewed agent code or drowns every typo in ceremony. Below, each
rail is read from the actual YAML in `kit/workflows/`: what triggers it, what it does, whether it
blocks or advises, and what it leaves behind.

### Rail 1 — `ci` (job `build-and-test`)

*Fires on every PR and every push to main.* **Blocks — a hard gate.**

The only rail with no AI in it. It restores, builds, runs the test suite with coverage, and uploads
the built artifact. It answers only what a machine can answer for certain, and any red here is **a hard
block** — a closed door no human waves through without a recorded exception. The standard's 80%
coverage floor is enforced in the test runner so a coverage miss is a non-zero exit, not a low number
in a passing report.

**Tooling —** `ci.yml` → `build-and-test` · `ci.yml` → `eval-gate` (optional) · `gh pr checks`.

**Leaves behind —** the CI run (Actions log) · `coverage/` — the uploaded artifact deploy-dev
promotes.

> **At Harbor.** On the first walking-skeleton slice (spec 0001), the coverage gate **miscounted
> generated files** and read low. Caught on the PR, fixed cheap, before any feature depended on it. The
> optional `eval-gate` is a second hard block for agentic behavior that must not regress; a time-boxed
> bypass is *recorded* in `profile/eval-bypasses.md` — the gate still runs, the ledger only says why a
> known failure was accepted.

### Rail 2 — `grader` (job `grader`)

*Fires on every non-draft PR.* **Required to RUN; its verdict never blocks.**

An agent that did **not** write the code reads the committed spec file in the diff and walks its
acceptance checks one by one, pinning each verdict to a changed line, and posts one PR comment (updated
on re-runs). This rail is **required to run** — `grader` is a required check, so a PR can't merge until
it has run — but its **verdict never blocks.** "The grader ran" is what the method requires; *what it
said* is the human Checker's input, not a gate. It is the one rail that **fails soft**: the Claude step
is `continue-on-error`, so a missing key or an API hiccup never adds false red.

**Tooling —** `grader.yml` → `claude-code-action` (--model sonnet) · `diff-anchors.sh` → changed-line
set · `rubrics/grader.md`.

**Leaves behind —** the grader's PR comment (verdict, per-check, line-anchored) · the Checker's
decision — a human reads it and acts.

> **At Harbor.** On spec 0016 (duplicate-claim merge, HIGH), **eleven tests passed** and CI went green.
> The grader flagged the hole the eleven never covered: two claims with an **empty policy number**
> merging into one. It advised; it did not block. Sara (not the author) read it, agreed, and bounced it
> back — the principle in its purest form. The full episode is below.

> **The gap you should know about.** The grader's value depends on a human *reading* the advisory
> verdict — and nothing records that they did. The non-author approval at the bar implies it, but there
> is no receipt that the grader's comment was read and weighed. It is also lenient by design: if the PR
> carries no `specs/NNNN-*.md`, the grader falls back to the PR description and emits a *warning*, not a
> block.

### Rail 3 — `correctness` (job `correctness-review`)

*Fires on every PR; reviews when source changed.* **Blocks on a high-confidence defect — with a named
override on the record.**

The bug class the others miss: CI proves it compiles and tests pass, security covers exploitability,
the grader checks intent — none asks "is this code correct?" A fresh agent (neither the author nor the
grader) reviews the changed lines for off-by-ones, null paths, inverted conditions, and writes a
machine verdict. It **blocks on a high-confidence defect** (`CORRECTNESS_VERDICT: BLOCK`) unless a
named human records the `accepted-risk:correctness` label — an audited override on the PR timeline. It
**fails closed**: a source change whose review can't complete blocks rather than passes. When no source
changed, it short-circuits to a trivial pass, so it can be a required check without leaving low-risk
PRs stuck pending.

**Tooling —** `correctness.yml` → `claude-code-action` (--model opus) · verdict → runner temp
(anti-tamper) · `gh pr edit --add-label accepted-risk:correctness`.

**Leaves behind —** the correctness PR comment + the red/green check · the audited override label, when
a human accepts the risk.

> **At Harbor.** At Phase C close, spec 0051 extracted the replica-staleness guard into one shared
> check — a refactor the tests couldn't vouch for and the grader was silent on (the spec promised no
> new behavior). The correctness rail read the extraction against both originals, confirmed the
> 02:00–04:30 boundary and the degraded path were byte-for-byte the prior behavior, and cleared it. The
> refactor merged on proof, not crossed fingers (full episode below).

> **Where the local check can't bind.** A pre-push hook does correctness self-review on the agent's
> machine — but it binds only the *agent*; a human pushing from their terminal sails past. So this rail
> runs again server-side on every PR. The label is an audited override, **not** an authorization check:
> the workflow cannot reliably tell the label's applier from the author, so the "a non-author signs
> off" guarantee comes from the bar's non-author approval, not the label. The YAML says so in its own
> comments.

### Rail 4 — `security` (job `security-review`)

*Fires on every PR; reviews on gated paths / `risk:high`.* **Blocks on HIGH; advises otherwise.**

Path-triggered, not just tier-triggered: the workflow runs the security-reviewer agent on any PR
touching a guarded directory — the regex is
`(^\.github/|/Auth/|/Identity/|/Security/|/Migrations/|^infra/)` — or carrying the `risk:high` label. A
change tiered MEDIUM that touches the auth folder is caught regardless. It **blocks on a HIGH finding**
(`SECURITY_VERDICT: BLOCK`) and **fails closed** if the review can't complete. When no gated path
changed and no `risk:high` label is present, it passes trivially.

**Tooling —** `security.yml` → `security-reviewer` (--model opus) · `gh pr edit --add-label risk:high`
· `rubrics/security.md` · `CODEOWNERS`.

**Leaves behind —** the security PR comment + the red/green check · the named human sign-off — a PR
convention, not a tool receipt.

> **At Harbor.** On the walking skeleton's HIGH slice (spec 0002, the replica verification read),
> `risk:high` fired this rail; **Dan recorded a named sign-off** under the Q-15 controls before merge.
> The first PR to touch acknowledgment templates (spec 0003) tripped the PII template-review gate the
> same way — the path caught it, independent of its tier.

> **The override the YAML doesn't implement.** The merge bar promises a `risk:high` change can proceed
> on "a named human sign-off recorded in the PR," and the workflow's own error text says *"Resolve them
> or record a named accepted-risk sign-off."* But the enforce step has **no label** and **no
> condition** that lets a recorded sign-off pass — on a HIGH verdict it always `exit 1`. Unlike the
> correctness rail, there is no coded override; the sign-off is human convention the YAML never checks.
> (Drift, filed.)

### Rail 5 — `deploy-dev` (job `deploy-dev`)

*Fires on a successful CI run on main (the merge).* **Not a gate — it ships.**

The merge already cleared the bar. Triggered by a *successful CI run on main*, it **promotes the exact
artifact CI built** (downloaded from the triggering run — never a rebuild), captures the last known-good
version, deploys, health-checks, and **restores the last good version on any failure.** Merge → dev is
automatic and human-free; promotion beyond dev (dev → test → prod) is deliberate and human-gated, and
is *not* this workflow.

**Tooling —** `deploy-dev.yml` → `workflow_run(CI, success, main)` · `download-artifact` → promote,
never rebuild · restore last-good on `failure()`.

**Leaves behind —** the deployed dev environment (the GitHub dev Environment) · a rollback to the last
good version, on a failed deploy.

> **At Harbor.** The rollback path is proven by **failing safely first**. In the Phase 8 rehearsal it
> failed in test on a Tuesday — a config key had moved ahead of the artifact — which spec 0046 fixed by
> versioning config *with* the release. Thursday, **rc-1.0.1 was promoted to production, not rebuilt**;
> the first real FNOL (a burst pipe, 08:14) got a coverage recommendation in **3 hours 6 minutes**
> against the 11.4-day baseline (full episode below).

> **Ships as a starter that fails until wired.** This is the one rail **built fresh** to the standard,
> not generalized from the source harness — the source deferred deploy entirely. As shipped it
> *intentionally fails*: the deploy step is `echo "::error::<<DEPLOY_STEP>> not yet wired — this
> starter intentionally fails until adapted."; exit 1`. It encodes the §5 rules (promote never rebuild;
> a rollback that has never run is a wish) correctly, but the deploy and rollback steps are placeholders
> a client must wire and **rehearse** before trusting.

## What a merge leaves behind

A phase leaves a folder of artifacts; a merge leaves a **ledger of receipts**. Blue rows are written by
a rail and have a real place to live. **Amber rows are what the standard demands and no tool emits** —
the receipts that exist only as memory, convention, or a metric nobody records. Those are the rows to
argue about.

State marker key:

- `▪` a command does it — and writes the file
- `▸` a person does it — and it is recorded
- `⚠` a person does it — and nothing records it

| Artifact | What it actually is | Written by | Signed by | Lives at | Feeds |
| --- | --- | --- | --- | --- | --- |
| ▪ grader PR comment | A fresh agent's per-check verdict against the committed spec, each check pinned to a changed line; one comment, updated on re-runs | `grader.yml` (claude-code-action, sonnet) | — (advisory) | the PR conversation | The human Checker's decision |
| ▪ correctness verdict + comment | Logic-defect findings on the changed lines, plus a machine `PASS`/`BLOCK` token on the first line | `correctness.yml` (opus) | — | PR comment + the `correctness-review` check; verdict in runner temp (ephemeral, anti-tamper) | The merge bar — blocks on `BLOCK` |
| ▪ security verdict + comment | Security findings on the gated files, plus a `PASS`/`BLOCK` token; fires on gated paths or `risk:high` | `security.yml` (opus) | — | PR comment + the `security-review` check | The merge bar — blocks on HIGH |
| ▪ CI run + coverage artifact | Build, tests, lint, 80% coverage — and the deployable bytes deploy-dev promotes | `ci.yml` (build-and-test) | — | the Actions run + the uploaded `coverage/` artifact | deploy-dev (promotes the CI artifact) |
| ▪ review receipt | Proof `/code-review` and `/simplify` ran against this exact commit — the reviewer's own summary, commit-bound | `save-review-receipt.ps1` (local, pre-push) | the reviewer (the content is theirs) | `.claude/.review-receipts/<sha>.<kind>` (gitignored, per-clone) | The review gate (blocks the push until present) |
| ▪ co-authored merge commit | Provenance in the history: who, or what, wrote each line — agent commits carry a co-author trailer | the committer / agent | — | git history on `main` | Audit; Phase C transfer |
| ▪ deployed dev environment | The merged artifact, promoted (never rebuilt) and running in dev; a rollback record on a failed deploy | `deploy-dev.yml` (once wired) | — | the GitHub `dev` Environment | The Build loop's constant exercise of the rails |
| ⚠ the metrics line | Per-merge dashboard data — accepted-as-is rate, review wait, the DORA four, escaped bugs (GOLD §9) | nothing — no rail appends it | Setup Owner (would) | no path — nothing writes it | The internal dashboard; Retro+ |
| ⚠ the central provenance log | Every agent recommendation, applied artifact, and gate outcome, logged centrally (the-rails.md §9) | nothing emits it | Setup Owner | no path — nothing writes it | Audit after a poisoned tool-return |
| ⚠ the "grader was read" receipt | Evidence the human Checker read the advisory verdict and acted on it — the whole point of an advising rail | a human, un-recorded | the Checker | no path — the approval implies it, nothing records it | The merge decision |
| ⚠ the `risk:high` sign-off | A named human's recorded sentence accepting a HIGH risk — a name, not a thumbs-up | a human, by convention in a PR comment | the named signer | no path — nothing templates or checks it | The merge bar (HIGH path) |

**Read the amber rows again.** Four of the receipts the standard leans on have nowhere to live. The
DORA four and the accepted-as-is rate are the numbers the rails are supposed to be *watched* by — yet
no rail appends a metrics line, so the dashboard is hand-kept or absent. The central provenance log
the-rails.md calls "what makes the rails auditable rather than merely automated" is not written by
anything in the kit. And the two human receipts — that the grader was read, that a HIGH sign-off
happened — survive only as a PR approval and a comment. **Human work is not the problem. Human work
without a receipt is.**

Deliberately **not** produced by the rails: feature code (the specs and the loop own that), the test
and production environments (the first hardening pass and Phase 8 add those), and the metrics dashboard
itself. The rails emit *receipts*, not products — the enforcement, not the thing enforced.

## The rails doing their job

These episodes span Build (2026-04-13 to 07-10), the Phase 8 go-live (week of 07-20), Phase 9
hypercare (from 07-27), and into Phase C close (08-17). The rails were built once and never stopped
running. Three ran on rails the plugin ships today (episodes 1, 5, 7); four use machinery **net-new to
the kit**, flagged inline and tallied in the next section.

### Episode 1 — the grader catches what eleven green tests missed

*Build week four · Thursday 2026-05-07 · spec 0016 (duplicate-claim merge), HIGH risk.*

**Tooling —** No plugin command. Spec 0016 rides the loop; the PR fires `ci.yml` + `grader.yml`;
`risk:high` fires `security.yml` → the security-reviewer agent; Wes's named sign-off in the PR.

- Spec 0016 implements D-07 — the same loss reported twice becomes one claim, never a rejection. Maya
  tiered it **HIGH**: merging claim records is hard to undo, and a wrong merge mangles two
  policyholders' data. The agent built it under tight permissions; the Stop hook held it to a green
  suite; **eleven tests passed.**
- On the PR, `ci.yml` went green. Then the **grader** — a fresh agent that did not write the code —
  walked the spec's acceptance checks one by one and flagged the hole the eleven tests never covered:
  two claims with an **empty policy number** were landing in the same match bucket and merging into one.
  Real bug, real data, invisible to a green suite that never thought to test the empty-key case.
- The grader **advised; it did not block.** Its verdict was a PR comment. Sara (not the author) read
  it, agreed, and bounced the change back to the same Orchestrator, who fixed the keying on the same
  branch. Every gate — including a fresh grader run — ran again on the updated PR.
- Because HIGH, `risk:high` fired `security.yml` and **Wes recorded a named sign-off** in the PR before
  merge. Then a non-author merged, and deploy-dev shipped it to dev.

**The rail that mattered:** the grader (rung 4 of the checking ladder). An agent produced a confident,
green-looking change; a separate gate caught what the author was blind to; a human owned the call.
Agent proposes, gate disposes.

### Episode 2 — self-healing CI: a proposed fix that stops at a PR

*Build week six · Tuesday 2026-05-19 · **(net-new to the kit)**.*

**Tooling —** No plugin command **(net-new to the kit)** — `self-heal.yml` → a bounded fix agent
(read/write/run-tests/run-lint only); emits a `fix/` PR, never a merge.

- A scheduled dependency bump landed a minor version of a JSON serializer that changed a default, and
  the nightly build on `main` went red — three integration tests failing on a serialization edge.
  Nothing a human had touched; the kind of break that eats a morning.
- A new kit workflow, **self-heal.yml**, pointed an agent at the failure. It did **not** get the repo
  and a shell. It got a **bounded tool surface** — read a file, write a file, run the tests, run the
  linter — and the failing job's log. It formed a hypothesis (the changed default), made the two-line
  fix, and **re-ran the tests from the environment until they went green.** It proved the fix; it did
  not assert it.
- Then it stopped. It opened a `fix/serializer-default` **pull request** with the diff and a
  one-paragraph explanation, and went no further. It cannot push to `main`; it cannot approve its own
  work. **Sara reviewed the proposed fix, agreed, and merged it** through the same merge bar as
  everything else.
- The agent ran under **its own least-privilege identity** — a workload credential scoped to read the
  repo and open a PR, nothing more. If its prompt had been steered somewhere bad, the identity is the
  wall that was still standing.

**The rail that mattered:** the merge bar, applied to the pipeline's own repairs. A self-healing
pipeline that pushed its own fix would have thrown away the only rule that makes it safe. Stopping at
the PR is the whole design.

### Episode 3 — the flaky test that got quarantined, not "fixed"

*Hardening pass one · Wednesday 2026-05-27 · **(net-new to the kit)**.*

**Tooling —** No plugin command **(net-new to the kit)** — the flaky-test state machine (Active →
Quarantined → Disabled) moves the test out of the blocking set; the real fix then rides the loop.

- The replica refresh-window test — the one guarding the 02:00–04:30 staleness degradation from ADR-001
  — started failing intermittently. Same code, different result run to run: roughly one PR in twelve
  went red on it, on changes that had nothing to do with the replica. It was beginning to block
  unrelated work.
- A flaky test is not always a bug to fix; sometimes it is a test to **quarantine while a human
  looks.** The **flaky-test state machine** moved it from **Active** to **Quarantined** only after it
  cleared eligibility thresholds — failing above a set rate, failing on the default branch, across more
  than one pipeline, not on a single unlucky run — so it stopped gating PRs while staying visible and
  tracked.
- Nadia investigated and found the real cause: the test built its boundary timestamps in local time
  while the service worked in UTC, so runs near midnight Chicago time straddled the window. A genuine
  clock-boundary race, not noise. The **fix rode the loop** like any change — a spec, a plan, a
  non-author Checker — and the test sat under a **grace period** before rejoining the blocking suite, so
  a stale branch couldn't re-break CI the day after the fix.
- The pattern — build time-boundary tests in the service's own clock — went on the harvest list as the
  **timezone test pattern.**

**The rail that mattered:** triage over reflex. Active → Quarantined → Disabled with eligibility gating
and a grace period beats "an agent fixes every red test" — which would have papered over a real race
with a flakier assertion.

### Episode 4 — a HIGH-risk infrastructure change through the funnel

*Hardening pass one · Thursday 2026-05-28 · the test environment · **(net-new gates flagged)**.*

**Tooling —** No plugin command **(net-new to the kit)** — `iac.yml` runs the funnel: schema-validate →
PSRule policy gate → `bicep what-if` (Tom reads it) → human approval → scoped least-privilege apply.

- Hardening pass one is where the **test environment** gets added alongside dev. That is a Bicep change,
  and Bicep is HIGH risk every time — hard to undo, and it is the shape production will take in Phase 8.
  Claude drafted the test-environment Bicep; then it went down the funnel, every step read-only until
  the last.
- **Schema validation** passed — the templates compiled against the resource schema. **The
  policy-as-code gate did not:** PSRule flagged two things — a storage account that would have defaulted
  to public network access, and a resource group missing the required cost-center tag. Caught
  mechanically, on the PR, not by a reviewer remembering to look. The agent fixed both; the gate went
  green.
- **`bicep what-if` produced the dry-run** — the exact list of what would be created in the test
  subscription. **Tom read it** before approving: the app hosting, the buffered queue, the private
  endpoint to the replica, the Key Vault — and nothing he didn't expect. An infrastructure change
  approved without reading its what-if is a change approved blind; this one wasn't.
- Only then did the **apply** run, under a **deploy identity scoped to the test resource group and
  nothing else.** The test environment came up from code, the same way dev had — and the same way prod
  would in eight weeks.

**The rail that mattered:** the infrastructure funnel. Everything before the apply is read-only — the
policy gate and the what-if did their work while nothing in the cloud had changed yet.

### Episode 5 — promotion, and the rollback that failed in rehearsal first

*Phase 8 go-live week · 2026-07-20 to 07-23 · rc-1.0.1.*

**Tooling —** No plugin command — the rehearsal and the go/no-go are human-run on the rails; spec 0046
rides the loop; `/sdlc-gate` at the Phase 8 boundary.

- **Tuesday, the rehearsal in test:** deploy → roll back → redeploy, run by the hands that would run it
  at 2 a.m. The deploy went fine. **The rollback failed.** The previous artifact came back, but a
  configuration key had moved ahead of it in a separate change, so the rolled-back app booted against
  config it didn't understand. A rollback that had only ever been written would have failed exactly here
  — in production, during an incident, instead of in test on a Tuesday.
- The fix rode the loop as **spec 0046 — configuration versioned with the release artifact**, so a
  promoted build always carries the config it was tested with and a rollback restores both together.
  Re-rehearsed **Wednesday: clean** — deploy, roll back, redeploy, with a timestamped timeline attached
  to the go/no-go packet. The failed first rehearsal went in the packet too: found-and-fixed is stronger
  evidence than never-stressed.
- **Thursday, go-live.** The **same artifact that passed test — rc-1.0.1 — was promoted to production,
  not rebuilt.** Tom executed; the release manager called each step; the pod and Harbor's operators
  watched the same dashboards. Production smoke ran green against live endpoints through the test-mode
  paths. The first real FNOL — a burst pipe, reported on the portal at 08:14 — produced a coverage
  recommendation in **3 hours 6 minutes**, against the 11.4-day baseline.
- **Secrets had rotated before go-live** to production-only values the pod could not read; **Dan held
  his go** at the ceremony until the rotation record was attached, then gave it. The engagement reached
  production with the pod having never known a production secret.
- `/sdlc-gate` passed the Phase 8 gate; billing milestone 6.

**The rails that mattered:** promotion (the proven artifact moved up, never rebuilt) and the rehearsed
rollback (proven by failing safely in test, not assumed). Plus identity: secrets the pod never held.

### Episode 6 — drift: proposed, never auto-applied

*Phase 9 hypercare · Monday 2026-07-28 · **(net-new to the kit)**.*

**Tooling —** No plugin command **(net-new to the kit)** — `drift-check.yml` runs on a schedule,
compares real infrastructure to the code, and opens a remediation PR; a human decides.

- During a Friday-night hypercare hiccup — a postal-vendor blip causing an acknowledgment-dispatch retry
  burst — an on-call engineer widened a firewall rule on the **test** environment by hand to unblock a
  verification run. It worked, the night ended, and the change lived only in the cloud, not in the code.
- Monday morning, the scheduled **drift assessment** caught it: the real test environment no longer
  matched its Bicep. It did **not** silently re-apply the code over the hand change — that would have
  quietly undone something a human did for a reason. It **flagged the drift and opened a remediation
  PR** describing the difference, leaving the decision to a person.
- **Tom made the call.** The widened rule was legitimate and worth keeping, so he **absorbed it into the
  Bicep** rather than reverting — and now the code is the truth again, the proper way. Had the change
  been a mistake, the same PR would have reverted it. Either way: a human chose; the schedule only
  proposed.

**The rail that mattered:** drift assessment that proposes, never auto-applies — the
agent-proposes/gate-disposes rule, one more time, on the live environment itself. And underneath it
all: identity — every agent ran under its own scoped credential.

### Episode 7 — the correctness rail clears a refactor that changed no behavior

*Phase C close & transfer · Monday 2026-08-17 · spec 0051 (extract the replica-staleness guard), MEDIUM
risk.*

**Tooling —** No plugin command — spec 0051 rides the loop; the PR fires `ci.yml` + `grader.yml` +
**`correctness.yml`**; Wes's non-author check at the merge bar.

- Close-and-transfer is when the codebase gets tidied for the people inheriting it. The
  **replica-staleness guard** — the 02:00–04:30 degradation rule from ADR-001 — lived in two copies: one
  on the intake path, one on the verification path. Ines, now driving on Harbor's side, had an agent
  **extract it into one shared check** so the client team inherits one hardened copy, not two that can
  drift apart. Same behavior, less surface.
- That is exactly the change a green suite can't vouch for. The tests passed — they always had — and the
  **grader was nearly silent**: there was no new behavior to check against the spec, because the spec
  promised none. A refactor is invisible to "does it meet the spec," and that is precisely where a
  silent regression hides.
- The **correctness rail** did the work. A fresh agent whose one job is *did this diff change behavior
  it shouldn't* read the extraction against both originals and confirmed the invariant survived: the
  boundary still fired at 02:00 and cleared at 04:30, the degraded-response path was byte-for-byte the
  prior behavior, the check still ran before the call and not after. No drift — and it said so on the
  PR, the verdict that lets a refactor of a correctness-critical guard merge with confidence instead of
  crossed fingers.
- Because the diff was proven equivalent, not assumed so, **Wes (not the author) signed at the merge
  bar** on the strength of the correctness verdict, and every gate re-ran on the final commit before
  merge. The client team inherited one guard instead of two — and the proof that the one still behaves
  like the two it replaced.

**The rail that mattered:** the correctness review — the no-regression twin of the grader. The grader
asks *does this meet the spec*; correctness asks *did this break something it shouldn't*. On a refactor
the spec hasn't moved, so the grader goes quiet and the correctness rail carries the load. The agent
proposes a "safe" cleanup; the gate proves it is one.

## What was net-new to the kit

The plugin's rails are the five workflows (ci, grader, correctness, security, deploy-dev), the grader
and security-reviewer agents, the blocking Stop hook, and branch protection — everything Phase 3
installs and proves. The agentic-pipeline pieces below were invented for this example to show the rails
deep-dive in action. None is a command a pod can type now; each is the kind of thing a first
agentic-ops engagement would build once and **harvest back into the kit.**

| Piece | What it is | In the plugin today? |
| --- | --- | --- |
| **self-heal.yml + bounded fix agent** | On a red pipeline, an agent with a four-tool surface diagnoses, fixes, self-validates, and opens a `fix/` PR — never merges. | **No** — net-new; harvest candidate |
| **iac.yml funnel gates** | schema-validate → policy-as-code (PSRule) → `bicep what-if` dry-run → scoped least-privilege apply. | **Partial** — Phase 3 ships ci/deploy; the policy + what-if gates are net-new |
| **drift-check.yml** | Scheduled real-infra-vs-code comparison that **proposes** a remediation PR; never auto-applies. | **No** — net-new |
| **The flaky-test state machine** | Active → Quarantined → Disabled, with eligibility thresholds and a post-fix grace period. | **No** — net-new |
| **Per-agent least-privilege identity** | Each pipeline agent (the fix agent, the deploy identity) runs under its own scoped workload credential. | **No** — net-new; an Entra Agent ID / federated-credential pattern |

This is the develop-*with*-agents track reaching toward the AI-as-product track. The net-new pieces are
where the two tracks first touch — exactly what a first agentic-ops-heavy engagement would build once
and harvest back into the kit.

## Two artifacts, whole

The rollback fix (spec 0046) and the infrastructure funnel (`iac.yml`), reproduced in full — then the
per-episode tooling tally.

### Artifact: spec 0046 in full (the rollback fix)

**Spec 0046 — Configuration versioned with the release artifact**
Risk tier: **HIGH** · Authored: Jonah Kim · Checked: Sara Whitfield · Security sign-off: Dan Kowalski ·
Merged 2026-07-22

**Goal.** A promoted build carries the exact configuration it was tested with, so that a rollback
restores the application **and** its config together, never one without the other.

**Why.** The Tuesday rehearsal rolled back the artifact but not a config key that had moved ahead of it;
the rolled-back app booted against config it didn't understand. Promotion must move one versioned
thing, not an artifact plus a separately-drifting config.

**Scope in.** The release-packaging step, the config bundling, the rollback restore path. **Scope out.**
Application config *values* (those are environment settings, untouched); any change to what the app
reads at runtime.

**Acceptance checks.** A promoted artifact includes its config manifest, content-addressed. Rollback
restores artifact + config as one unit. A redeploy after rollback is byte-identical to the prior good
state. The Tuesday failure mode (config ahead of artifact) cannot recur — proven by re-running the exact
rehearsal.

**How it rode the loop.** Plan approved by Jonah → agent implemented under tight permissions → Stop hook
green → PR fired `ci.yml`, `grader.yml`, and (on `risk:high`) `security.yml` → Dan signed off → Sara
merged → the Wednesday rehearsal proved it clean. It went into the kit harvest as
**config-with-artifact.**

### Artifact: the infrastructure funnel (`iac.yml`)

*Net-new to the kit. Drafted by Claude, reviewed by Tom; every step before the apply is read-only.*

| Step | What runs | Blocks? |
| --- | --- | --- |
| Schema validate | `bicep build` against the resource schema | Hard block on a malformed template |
| Policy-as-code | PSRule for Azure (public access, encryption, tags, region) | Hard block on a policy violation |
| Dry-run | `bicep what-if` — the exact change preview | Posted to the PR; a human reads it |
| Approval | A named human approves the what-if | Required to proceed |
| Apply | Scoped, least-privilege deploy identity | — (the only step that changes cloud) |
| Drift assessment (`drift-check.yml`) | Scheduled real-infra-vs-code compare | Opens a remediation PR; never auto-applies |

### The tooling behind these episodes

| Episode | How it ran |
| --- | --- |
| 1 · Grader catch (0016) | Spec rides the loop; `ci.yml` + `grader.yml` on the PR; `security.yml` on `risk:high` → security-reviewer agent; Wes's sign-off |
| 2 · Self-healing CI | **Net-new:** `self-heal.yml` → a bounded fix agent; opens a `fix/` PR; a non-author merges |
| 3 · Flaky-test quarantine | **Net-new:** the Active/Quarantined/Disabled state machine; the real fix then rides the loop |
| 4 · Infra funnel (test env) | **Net-new gates:** `iac.yml` schema → PSRule policy → `bicep what-if` (Tom reads) → scoped apply |
| 5 · Promotion + rollback | Human-run rehearsal and go/no-go on the rails; spec 0046 rides the loop; `/sdlc-gate` at the Phase 8 boundary |
| 6 · Drift proposed | **Net-new:** `drift-check.yml` on a schedule → a remediation PR; Tom decides |
| 7 · Correctness-rail refactor (0051) | Spec rides the loop; `ci.yml` + `grader.yml` + **`correctness.yml`** on the PR; Wes's non-author sign-off at the merge bar |

## The merge bar

Branch protection is what turns five workflows from suggestions into rails. It is repository
configuration — set by the Setup Owner or a named client admin — and it makes the gates mandatory at the
one moment that matters: the merge. Behind it stands the whole reason agent-built software can be
trusted to ship: **the agent proposes, a gate disposes.** An agent may produce any change, but only as
a reviewable artifact; a deterministic policy layer plus a named human decides whether it takes effect.

**Every PR, to merge, must clear:**

- **CI green** — build, tests, lint, coverage, all passing. Hard block.
- **The grader has run** — the workflow completed and posted its verdict. The verdict can say anything;
  the *running* is required.
- **Correctness review passed** — no high-confidence defect, or a named human recorded the
  `accepted-risk:correctness` override.
- **A non-author approval** — someone who did not write the change approved it.

A `risk:high` change adds two more: **the security workflow passed** (blocking on HIGH) and **a named
human sign-off recorded in the PR** — a person, by name, accepting the risk. Not a thumbs-up; a recorded
sentence with a name attached.

**The non-author rule.** The author of a change is **never its checker**. The platform forbids an agent
from approving or merging its own work exactly as it forbids a human author from being their own
approver — and the correctness override is honest about it: a label records who accepted a defect, but
the guarantee that the person clearing it is not the author comes from this rule, not the label.

> **The rule that survives every collapse of pod size.** Even a two-person pod holds it. An agent pushes
> only to branches it creates (`spec/NNNN-*`), never to main; every commit it makes is co-authored, so
> who — or what — wrote a line is never a guess.

**The one escape hatch — deliberately expensive.** A true emergency merge past a gate requires the Pod
Lead *plus one other human*, a `gate-exception` label, and a Retro+ agenda item. Two exceptions in a
month is not bad luck — it means the gate or the specs are wrong. Fix that; do not normalize the bypass.
On a single-maintainer repo, GitHub forbids self-approval, so the ruleset ships **armed with an owner
bypass** (`bypass_mode: pull_request`): the owner can self-merge a PR, but even they cannot push
*directly* to main skipping CI — every change still rides a PR and its checks. Remove the bypass the
moment a second reviewer joins.

That is the merge bar: not a phase boundary the engagement crosses once, but a standing line every
change clears, forever. The rails do not report to a calendar. They report to the bar — and the bar
reports to a human. **Gates report; humans decide.**

---

Back: [The Rails](the-rails.md) — the deep-dive these episodes illustrate: the five workflows, the merge
bar, deploy and promotion, the infrastructure funnel, and the principle that governs all of it.
