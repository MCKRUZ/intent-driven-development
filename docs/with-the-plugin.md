# With the claude-code-sdlc plugin, step by step

_Harbor Mutual, the fictional regional insurer the standard uses as its worked example, rebuilding
property-claims intake. A four-to-six person pod, the client's repo, and `claude-code-sdlc` 1.5.0
as the mechanism. Numbers are the walkthrough's, not a promise. This is the default mechanism;
the other two options are on [choose a mechanism](choose-a-mechanism.md)._

---

Every command below is a real command in the plugin as shipped; every file named is one the
plugin's phase registry requires. "Machine" is what the plugin and the agent do; "Human" is where a
named person decides or signs. The "route back" notes are the recorded ways to reopen a decision
later.

## 0 · Day 0 · Install the mechanism, check the machine

The Setup Owner installs the plugin once, then runs the day-one environment check in the client's
repo so nothing surprises the pod later.

- **Machine:** installs the orchestration commands and bundles the delivery harness;
  `/sdlc-doctor` verifies toolchain, platform CLI, credentials, repo access.
- **Human:** the Setup Owner names a deputy on day one, the person who reviews every harness
  change.

```
/plugin marketplace add MCKRUZ/claude-code-sdlc
/plugin install claude-code-sdlc@mckruz
/sdlc-doctor
```

## 1 · Day 1 · Set up the engagement and lay down the harness

One wizard: pick a profile (the client's stack, platform and compliance bar), and the plugin
initialises the phase state and installs the full harness into the repo.

- **Machine writes:** `.sdlc/state.yaml` (phase state, audit trail) and a frozen
  `.sdlc/profile.yaml`; governance `CLAUDE.md`, `.claude/` settings, hooks, agents, skills; the
  rails: `ci`, `grader`, `correctness`, `security`, `deploy-dev` plus eval and promotion
  workflows, rubrics, branch-protection ruleset.
- **Human decides:** the profile (`starter`, `microsoft-enterprise`, `ado-enterprise`,
  `ado-enterprise-python`, `creative-tooling`); project type, quality thresholds, compliance
  gates, confirmed, not defaulted.

```
/sdlc-setup            # profile → .sdlc/ + harness installed
/sdlc-status           # the dashboard you'll read every week
```

## 2 · Discovery · Frame the problem

Deep-dive: [Discovery](phase-0-discovery.md).

Karen Voss, VP Claims Ops, owns the problem: 11.4 days median from first notice to a coverage
decision; the target is five. The workshop forces the two decisions nobody had made: who the
product owner is, and whose AI keys the pod works on.

- **Machine drafts:** `/sdlc-brief`, the workshop brief from the sponsor's notes; `/sdlc-intake`,
  which catalogs the client's RFPs, specs and vendor docs; drafts of `constitution.md`,
  `problem-statement.md`, `success-criteria.md`, `constraints.md`, and the unmade decisions
  surfaced.
- **Human signs:** the problem statement is human-authored; the agent never invents the problem.
  PO decision: Luis Ortega, six hours a week. Tooling decision: client-procured Anthropic access,
  keys in their vault. `phase1-handoff.md`: the last artifact is named for the phase that
  consumes it.

```
/sdlc-brief
/sdlc-intake
/sdlc-coach            # guided completion of the phase's artifacts
/sdlc-gate             # the battery runs → HTML report opens
/sdlc-next             # gate passed → "Does this look correct?" → a named human signs
```

## 3 · Requirements · Sign the baseline

Deep-dive: [Requirements](phase-1-requirements.md).

Epics and stories drafted by the agent, owned by humans. Every numeric non-functional requirement
must say where it will be measured. The big discovery here: the core policy system only exposes a
nightly read-only replica, found in requirements, not production.

- **Machine drafts:** `requirements.md`, `non-functional-requirements.md`, `epics.md`;
  `/sdlc-review` in adversarial mode hunts the gaps; the decision list ("you haven't decided X")
  is generated, not remembered.
- **Human signs:** Luis answers every decision-list item on the two-business-day clock. The Pod
  Lead enforces Definition of Ready on every story. `phase2-handoff.md` signed at the gate.

```
/sdlc-review requirements.md --mode adversarial
/sdlc-gate && /sdlc-next
```

> **Route back, later:** when a signed requirement changes mid-build, `/sdlc-revise FR-012`
> routes the edit to its owning discipline, opens a decision-log row with an owner and a clock,
> re-runs this phase's gate, and lists what the change put at risk.

## 4 · Design · Choose the architecture

Deep-dive: [Design](phase-2-design.md).

The agent presents two or three architectures with concrete trade-offs; the Architect picks; every
decision record is signed, and Wes Carter, Harbor's own lead engineer, co-signs the decisions he
will live with. Unknowns are not guessed: they are spiked.

- **Machine drafts:** `design-doc.md`, `api-contracts.md`, `adrs/` and `adr-registry.md`;
  `threat-model.md`, `nfr-proving-plan.md`, `walking-skeleton-definition.md`; `/sdlc-spike` runs
  the bounded experiment on a `spike/` branch; its code can never merge; its finding is
  `spike-findings.md`.
- **Human signs:** architecture selection, a person picks, the agent does not. Each ADR, by the
  Architect; the client engineer co-signs. `phase3-handoff.md`.

```
/sdlc-spike "does the carrier API dedupe on our idempotency key?"
/sdlc-gate && /sdlc-next
```

> **Route back, later:** a spike during build disproves an assumption → `/sdlc-revise ADR-007`
> as a HIGH-risk change with a named signature; the old ADR is marked superseded, never edited
> away.

## 5 · Foundation · Build the factory and prove it

Deep-dive: [Foundation](phase-3-foundation.md).

The harness is adapted in the open (the client's first look at how we work), branch protection is
applied, and the thinnest end-to-end slice, four small specs, rides the whole loop into the
client's dev environment. Tom Reilly, Harbor's platform engineer, reviews the pipeline he will
operate after we leave.

- **Machine does:** `/sdlc-harness` refreshes the harness; `apply-branch-protection` makes the
  five checks required. Bicep for the dev environment drafted; pipeline YAML drafted. Specs
  0001–0004 built through the loop; `foundation-report.md`, `risk-tier-map.md`,
  `cadence-plan.md`, `data-flow-brief.md`.
- **Human signs:** every pipeline and infrastructure change is HIGH risk: human review, no
  exceptions. Exit demo: one real feature running in client dev. WIP cap and review-wait tripwire
  set from checking capacity; `build-handoff.md`.

```
/sdlc-harness
/sdlc-spec "walking skeleton: claim intake form → API → replica verify"
/sdlc-gate && /sdlc-next
```

## 6 · Build, 8–16 weeks · Run the loop, once per change

Deep-dive: [the build loop](build-loop.md).

No phases in the middle, just the loop, one spec at a time, with four short meetings a week. The
worked week: spec 0015 (a fast-path work queue, MEDIUM) and spec 0016 (duplicate-claim merge,
HIGH), where the grader catches an empty-policy-number bug that eleven green tests missed.

- **Intent, human:** `/sdlc-spec` turns a triaged story into `specs/0016-duplicate-claim-merge.md`:
  goal, why, scope in/out, testable acceptance checks, risk tier confirmed by the Pod Lead.
- **Delegate, machine, bounded:** plan mode first; the Orchestrator approves the plan.
  Permissions auto-allow build/test/lint; ask on installs, network, gated paths (auth,
  migrations). The Stop hook refuses "done" on a red build.
- **Discern, machines report:** `ci` blocks on build/tests/lint/coverage and on a newly
  introduced vulnerable package. `grader`: a fresh agent grades check-by-check, advisory, required
  to run. `correctness` blocks on a high-confidence defect; `security` blocks on HIGH.
- **Discern, a human signs:** a non-author Checker approves; on HIGH, Dan in security signs with
  a sentence; a bare name fails the `risk-signoff` check. Merge deploys to dev automatically.

```
/sdlc-spec "duplicate-claim merge"          # Intent → specs/0016-… (ready or bounced)
# plan mode → build → Stop hook → PR on spec/0016-duplicate-claim-merge
/sdlc-status                                 # queue, decision list, gate status — every flow check
/sdlc-refresh detect --spec specs/0016-duplicate-claim-merge.md   # after merge: did upstream drift?
/sdlc-retro                                  # Retro+: every escaped bug → "which check should have caught it?"
```

> **Routes back, from inside the loop:** unknown → `/sdlc-spike`; design wrong → `/sdlc-revise`
> the ADR (HIGH); requirement changed → `/sdlc-revise` the requirement; merged work drifted from
> its requirement → `/sdlc-refresh` proposes the upstream edit and a person applies it; stale
> artifacts anywhere → `/sdlc-audit-artifacts`.

## 7 · Documentation · Prove a stranger can run it

Deep-dive: [Documentation](phase-7-documentation.md).

The agent drafts the README, API docs and runbook from the code and the specs. Verification is by
use, not by reading: Ines Roy, hired three weeks earlier, follows the README cold and stalls at
step four on a vault permission, fixed the same day.

- **Machine drafts:** README, API docs, RUNBOOK; `/sdlc-enhance` produces the client-facing
  narrative companions.
- **Human signs:** `readme-verification.md`, the cold-walk record, by someone who has never seen
  the system. `phase8-handoff.md`.

```
/sdlc-enhance
/sdlc-gate && /sdlc-next
```

## 8 · Deployment · Rehearse, then go live

Deep-dive: [Deployment](phase-8-deployment.md).

Tuesday's rehearsal fails (configuration keys moved ahead of the release artifact) and becomes
spec 0046. Wednesday's re-rehearsal is clean. Thursday's go-live is boring, which is the point.
Promotion ships the exact bytes a named CI run produced; it cannot run without a configured
approver.

- **Machine does:** `deploy-promote`, manual trigger only, refuses an environment with no
  approver. `release-notes.md` drafted from merged specs; `smoke-test-results.md`;
  `deployment-checklist.md`.
- **Human signs:** `rollback-rehearsal.md`, the client's own operators rehearse deploy → roll
  back → redeploy. `go-no-go-record.md`, seven named roles; Dan holds until
  `secrets-rotation-record.md` is attached. `phase9-handoff.md`.

## 9 · Monitoring · Alerts from real baselines

Deep-dive: [Monitoring](phase-9-monitoring.md).

Six alerts ship, each modelled from measured baselines rather than guesses. A drill catches a
routing typo before it ever mattered. The retrospective is honest: 84% accepted-as-is, four escaped
bugs, the security queue running slow at 2.1 days, which becomes a standing twice-weekly security
slot.

- **Machine drafts:** `monitoring-config.md`, `alert-definitions.md`, `incident-response.md`;
  `/sdlc-retro` rolls up every ledger (gate outcomes, overrides, escaped bugs) into
  `project-retrospective.md`.
- **Human signs:** thresholds confirmed against real baseline data by the Pod Lead and client
  ops. `drill-record.md`; `close-handoff.md`.

## C · Close · The client runs it without us

Deep-dive: [Close & Transfer](phase-c-close.md).

Harbor's engineers run specs as Orchestrators with our Checkers; Wes becomes Harbor's Setup Owner
with Tom as deputy. The close gate is spec 0049, decommissioning the legacy fallback, HIGH risk,
driven end to end by Ines, with the hook correctly blocking a gated-path edit, Dan signing, and
Harbor's own go/no-go promoting it. Our access is revoked. Final read: 4.2 days median, under the
five-day target.

- **Machine assembles:** `final-handoff-report.md` from the engagement's own records (phase index,
  sign-offs, metrics history, spec backlog) with judgment sections left for humans;
  `harness-audit.md`, anything undocumented, any skill or hook only we understand.
- **Human signs:** `close-gate-evidence.md`, the real change the client shipped alone;
  `access-revocation-checklist.md`; the harvest retro PR back to the standard.

```
/sdlc-gate && /sdlc-next        # the close gate
/sdlc-retro                     # the harvest: what this engagement teaches the standard
```

## The other two options

This is the default mechanism, and the one the rest of the site assumes. It is one option, not the
definition: the standard is eight rules, and [choose a mechanism](choose-a-mechanism.md) lays out
the other two shapes (the same rails with any coding agent, and templates only) with the rules each
one enforces mechanically versus by discipline. What this option leaves in the repo, file by file,
is on [what's installed](whats-installed.md).
