# The Delivery Standard

How we use Claude to build software for clients, start to finish. This is the gold standard for
every engagement: who does what, what Claude does, what the templates are, how source control and
DevOps are structured, and what has to be true before anything merges, ships, or gets handed over.

**Owner:** Matt Kruczek. **Deputy:** named per the rule in section 4 (no role without a deputy).
**Version:** 1.0 (2026-06-10). Changes to this standard go through a PR reviewed by someone who
didn't write it, same as everything else.

This standard describes the **method as a concept**, kept independent of any one tool. Where it
names a specific tool — the SDLC orchestration plugin we drive it with (`claude-code-sdlc`), the
.NET/Azure stack, a particular CI system — treat that as **an example of how we implement the
method today**, not as part of the method itself. The specific tools and commands appear in full
in the worked examples (the fictional Harbor Mutual engagement that runs alongside each
deep-dive); the concept here should still make sense if you swapped every one of them out.

The method synthesizes two bodies of work: the Intent-Driven Development methodology
(`MCKRUZ/intent-driven-development`) and an SDLC orchestration plugin (`MCKRUZ/claude-code-sdlc`,
our example tool for running the phases). Where the two disagreed, this document is the
resolution; where it is silent, Intent-Driven Development is the tiebreaker.

> **The one rule.** Claude drafts and interrogates; humans decide and own. Every gate in this
> standard exists to enforce it: a machine reports, a named human signs.

> **New here?** This document is the full reference and assumes the vocabulary. For a softer way
> in: the [loop cheat-sheet](docs/cheatsheet.md) is the method in 20 seconds, the
> [glossary](docs/glossary.md) defines every term of art used below, the [FAQ](docs/faq.md)
> answers what clients and new pod members ask, and the [anti-pattern field guide](docs/anti-patterns.md)
> is the nine ways it goes wrong. None of them are required to read this — they're the on-ramp.

---

## 1. The shape of an engagement

An engagement has three parts, in order. An **opening** frames the problem and builds the
"factory" — the code repository, the build-and-deploy pipeline, and the set of rules and context
the AI agents work inside. A long **middle** is where the software actually gets built, one small
piece at a time. A **close** documents the system, ships it to production, and hands everything
over to the client.

The opening and the close run as **numbered phases**. Each phase ends at a **gate**: a checkpoint
where automated checks run and a named human has to sign off before the work advances. The middle
is different — it is not phased. It runs as a continuous **build loop**, repeating the same short
cycle for every piece of work.

A traditional software lifecycle phases the middle too: separate Implementation, Quality, and
Testing stages, each finishing before the next starts. We deliberately don't. Checking a large
batch of work only after it has all been built is the failure mode the delivery research warns
about — when AI agents write the code, the volume of code and pull requests can balloon while
delivery gets no faster, because the checking piles up unreviewed. So checking happens **per
change, inside the loop**, never as a later phase.

We run the phased opening and close with an example orchestration tool (the `claude-code-sdlc`
plugin), and only for its phase structure — deliberately with less automation than it offers.
Nothing about the shape below depends on that tool; any phase-gating mechanism that keeps a human
in the loop would do.

```
OPEN (gated phases — automated checks, then a human signs to advance)
  Phase 0  Discovery        problem, outcomes, constraints, tooling approval, PO decision
  Phase 1  Requirements     epics, stories, NFRs (drafted by Claude, owned by humans)
  Phase 2  Design           architecture, ADRs, API contracts (Claude proposes 2-3, human picks)
  Phase 3  Foundation       the factory built; thinnest end-to-end slice deployed to client dev

BUILD (the build loop — continuous, one piece of work at a time; replaces the batch middle phases)
  for every story:  Intent -> Delegate -> Discern -> merged & deployed to dev
  weekly cadence:   intent triage, flow check, retro+, setup review
  biweekly:         steering with the client (demo + outcome scorecard)
  hardening passes: scheduled, not a phase — see 5.6

CLOSE (gated phases — automated checks, then a human signs to advance)
  Phase 7  Documentation    README, API docs, RUNBOOK (Claude drafts, humans verify by using them)
  Phase 8  Deployment       promote to prod + release ceremony (pipeline already exists from Phase 3)
  Phase 9  Monitoring       alerts, incident response, retrospective
  Phase C  Close & Transfer consulting-only: client owns the harness, runs the loop solo, we leave
```

Phase advancement is **always manual**. Any auto-advance the orchestration tool offers is turned
off. Gates tell you whether you _may_ advance; a named human decides whether you _do_.

> Deep-dives, each phase day by day (who is involved, every artifact with its owner and
> done-condition, the cadences, the exit gate), with the Harbor Mutual worked example running
> alongside:
>
> - `docs/phase-0-discovery.md` + example `docs/phase-0-example.md`
> - `docs/phase-1-requirements.md` + example `docs/phase-1-example.md`
> - `docs/phase-2-design.md` + example `docs/phase-2-example.md`
> - `docs/phase-3-foundation.md` + example `docs/phase-3-example.md`
> - `docs/build-loop.md` — the Build loop that runs between the opening and closing phases
>   (+ example `docs/build-loop-example.md`)
> - `docs/the-rails.md` — the CI/CD and DevOps pipeline every change rides, as a standing
>   standard: the five workflows, the merge bar, deploy and promotion, the agent-safe IaC
>   pipeline, and the one principle (agent proposes, gate disposes)
>   (+ example `docs/the-rails-example.md`)
> - `docs/phase-7-documentation.md` + example `docs/phase-7-example.md`
> - `docs/phase-8-deployment.md` + example `docs/phase-8-example.md`
> - `docs/phase-9-monitoring.md` + example `docs/phase-9-example.md`
> - `docs/phase-c-close.md` + example `docs/phase-c-example.md`

Rough calendar for a typical engagement (4-6 person pod, medium-sized product): Open 4-6 weeks
(the phases overlap — the Setup Owner's enablement work runs ahead while requirements and design
close), Build 8-16 weeks, Close 2-3 weeks. These are planning figures, not promises; the SOW maps
billing milestones to phase gates, not to dates (section 12).

---

## 2. The human/AI collaboration model, phase by phase

The single most important rule: **Claude drafts and interrogates; humans decide and own.** Our
orchestration tooling can automate much of this; we deliberately run it with less automation than
it offers. The table below is the contract for every phase: what the human drives, what Claude
does, and where the mandatory stops are.

| Phase              | Human drives                                                                                                       | Claude does                                                                                                                                                | Mandatory human stops                                                                                            |
| ------------------ | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| 0 Discovery        | Sponsor states the problem and the one success metric. Pod Lead runs the outcome workshop.                         | Interrogates: surfaces unmade decisions, drafts constitution/problem-statement/constraints from workshop notes, runs document intake on client RFPs/specs. | Problem framing is human-authored. Claude never invents the problem. Phase advance.                              |
| 1 Requirements     | PO (client or proxy, per the Phase 0 decision) owns stories and priorities. Pod Lead enforces Definition of Ready. | Drafts candidate epics/stories from the brief, generates the decision list ("you haven't decided X, Y, Z"), drafts NFRs with measurement basis.            | Every silent decision on the decision list gets a human answer before the story is Ready. Phase advance.         |
| 2 Design           | Architect owns the design and signs every ADR.                                                                     | Researches options, presents 2-3 architectures with concrete trade-offs, drafts ADRs after the human picks, drafts API contracts.                          | Architecture selection. Each ADR. Phase advance.                                                                 |
| 3 Foundation       | Setup Owner builds and owns the harness. DevOps access negotiated with client.                                     | Scaffolds the repo from the kit, writes Bicep, writes pipeline YAML, implements the thin first feature through the full loop.                              | Pipeline and IaC are HIGH risk: human review on every change. Exit gate demo: one feature running in client dev. |
| Build loop         | Pod Lead triages and tiers specs. Orchestrators run agents. Checkers judge.                                        | Everything in section 5: plans, builds, self-checks, grades (as a separate grader), drafts test suites.                                                    | Plan approval before build. Checker approval before merge. Named sign-off on HIGH risk.                          |
| 7 Documentation    | Humans verify docs by following them cold (can a new person deploy from the RUNBOOK?).                             | Drafts README, API docs, RUNBOOK from the codebase and specs.                                                                                              | Docs verified by use, not by reading. Phase advance.                                                             |
| 8 Deployment       | Release manager (usually Setup Owner) owns the promote decision.                                                   | Drafts release notes from merged specs, runs smoke tests, prepares rollback plan.                                                                          | Go/no-go to production. Always.                                                                                  |
| 9 Monitoring       | Pod Lead + client ops define what "healthy" means.                                                                 | Drafts alert definitions, monitoring config, incident runbooks.                                                                                            | Alert thresholds confirmed against real baseline data.                                                           |
| C Close & Transfer | Pod Lead runs the transfer. Client team runs the loop solo, observed.                                              | Generates the final handoff report, audits the harness for anything undocumented.                                                                          | Close gate: client completed a real spec end-to-end without us driving.                                          |

---

## 3. The team

> Deep-dive: `docs/team.md` — the old-role-to-new-role mapping (PM, Architect, 2 devs, QA),
> the concrete job of each role, and the scaling model from one pod to many.

Designed for a 4-6 person pod running 2-3 parallel work streams. The constraint on parallelism is
**checking capacity, not headcount** — never open more agent streams than the team can review
without the queue growing.

### Roles

| Role                    | Owns                                                                                                    | Notes                                                                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Pod Lead**            | Intent. Stories become ready specs. Risk tiers. The decision list. Client steering.                     | Runs intent triage. Interface to the client PO (or plays proxy-PM in proxy mode, with the ratified decision log).                    |
| **Setup Owner**         | The harness as a product: CLAUDE.md, skills, agents, hooks, settings, pipeline, IaC, the kit install.   | Names a deputy on day one. Deputy reviews all harness changes (the Setup Owner is never sole approver of their own foundation work). |
| **Orchestrators (2-3)** | Running the build loop. Translating ready stories to specs. Approving agent plans. Driving integration. | They do not type most of the code. Their craft is bounds, plan correction, and the one-agent-vs-many call.                           |
| **Checkers**            | The verdict. Grading changes against the spec, reading the CI grader's output, owning the merge.        | Not a separate headcount: Orchestrators and Checkers swap per change. The author of a change is never its checker.                   |
| **Sponsor-side**        | The client sponsor owns the outcome and the metric. The client PO (if committed) owns stories.          | Their obligations are written into the SOW (section 12).                                                                             |

### Collapse rules (smaller engagements)

- 3 people: one person is Pod Lead + Setup Owner (deputy duty moves to the senior Orchestrator);
  two Orchestrator/Checkers swap per change. One stream, two at most.
- 2 people: only with an experienced pair, one stream, and the grader-in-CI carrying more weight.
  The rule that survives all collapsing: **the author of a change never solely approves it.**

### Certification

Nobody works a client spec until they have completed the IDD course (2-day format,
`intent-driven-development/course/`) and passed the competency rubric: demonstrably wrote a spec
that passes the vague-line test, ran the full loop on a practice feature, and operated the grader.
Demonstrated, not attested. The practice ground is internal projects, never client-billed work.

---

## 4. Source control and repository topology

### Where everything lives

- **Delivery repo** — in the **client's GitHub/ADO org from day one**. Contains the product code
  AND the harness (`CLAUDE.md`, `.claude/`, `specs/`), versioned together. Handoff at close is
  trivial: revoke our access. Their security team can audit everything from week one.
- **`MCKRUZ/delivery-standard`** (this repo) — private, ours. The gold standard docs plus the
  installable kit (section 10). Installed into the client repo at Phase 3; improvements harvested
  back after every engagement. Client-specific harness content stays with the client; generalized
  craft compounds with us. The SOW carves this out explicitly (section 12).

There is no separate per-client "system repo." The harness rides inside the delivery repo so
agents always load it, harness changes are PRs reviewed like code, and nothing needs syncing.

### Phase 0/1 checklist additions (because we're guests in their org)

- [ ] Contributor access for the pod; admin on branch protection for the Setup Owner (or a named client admin who applies our policy)
- [ ] GitHub Actions enabled; permission to add workflows and secrets (Anthropic API key, Azure credentials)
- [ ] Runner policy agreed (hosted vs self-hosted)
- [ ] Client's required org policies documented as constraints in the Phase 0 artifacts

### Branching and PRs

Trunk-based. **One spec = one branch = one PR.**

- Protected `main`. Branch per spec: `spec/0007-rate-limiting`.
- The spec file (`specs/0007-rate-limiting.md`) is part of the PR diff, so the reviewer sees
  intent and implementation in one view.
- Squash merge, conventional commit title (`feat: rate limiting per api key (spec 0007)`), branch
  deleted on merge.
- Branch protection requires: CI green (build, tests, lint, coverage), the grader check has run,
  and at least one non-author approval. HIGH-risk PRs carry a `risk:high` label that requires the
  security workflow plus a named human sign-off recorded in the PR.
- PRs stay small because specs are gated small at Definition of Ready. If a spec won't fit in a
  reviewable PR, it gets split at triage, not at review.
- GitFlow only where a client policy forces it, recorded as a deviation in the engagement log.

---

## 5. The build loop

> Deep-dive: `docs/build-loop.md` — the loop end to end: the three beats, the checking
> ladder, the weekly cadences, the client's view, and the metrics that steer it.

This is the middle of the engagement — it replaces the batch Implementation/Quality/Testing phases
of a traditional lifecycle. Every story runs the same three beats.

### 5.1 Intent

A story enters the loop only through **Definition of Ready**, enforced at weekly intent triage:

- Acceptance criteria pass the vague-line test (could two people build different things from this
  line? then it's not ready)
- Scope in / scope out stated
- Silent decisions answered (no open decision-list items for this story)
- Risk tier assigned by the Pod Lead (taxonomy below), recorded in the spec
- References the harness context the agent will have

The Orchestrator translates the ready story into `specs/NNNN-name.md` using the kit's spec
template: Goal, Why, Scope in/out, Acceptance checks, Risk tier, Delegation plan (what the agent
may touch, what's gated), Checking plan (which ladder rungs).

**Risk taxonomy** (lives in CLAUDE.md so agents see it too; challenges escalate up, never down,
without discussion):

| Tier   | What lands here                                                                                                                                                                                   | What it triggers                                                                                   |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| HIGH   | Auth/identity, payments, PII/client data handling, schema migrations, public API contract changes, IaC/pipeline changes, prompt/model/tool-definition changes (section 11), anything hard to undo | Tight agent permissions, full ladder, security-reviewer agent pass, named human sign-off in the PR |
| MEDIUM | New business logic, external integrations, changes to shared internal services                                                                                                                    | Standard permissions, grader + human Checker                                                       |
| LOW    | UI within existing patterns, copy, internal tooling, additive CRUD on established rails                                                                                                           | Lighter review; grader + mechanical gates still run                                                |

### 5.2 Delegate

- Start in plan mode. The agent proposes; the Orchestrator corrects or approves **before** code.
- Bounds set per spec: scope (file patterns it may touch), context (the one canonical pattern to
  reuse), permissions (`.claude/settings.json` auto-allows `dotnet test`, `dotnet build`,
  `ng test`, lint, reads; asks on package installs, network, and anything under gated paths like
  migrations or auth).
- One agent for tightly coupled code. Fan out only for independent, read-only exploration or for
  genuinely independent specs on separate branches.
- A blocking Stop hook (from the kit) refuses to let the agent finish with failing tests or a
  broken build. This is the single highest-value automation we keep.

### 5.3 Discern

- **Mechanical gates in CI** (hard blocks): build, tests, lint, 80% coverage on new code.
- **Grader in CI** (required to run, advisory verdict): a GitHub Actions workflow runs
  claude-code-action; a fresh agent that did not write the code reads the spec file in the diff
  and posts a check-by-check verdict as a PR comment. It cannot be skipped — "grader has run" is a
  required status check — but its verdict does not block. The human Checker reads it and makes the
  call. Machines gate the mechanical; humans own the judgment.
- **Human Checker** (hard block): non-author approval on every PR. On HIGH risk, additionally the
  security-reviewer agent's pass and a named human sign-off.
- Merge deploys to the client dev environment automatically (the rails from Phase 3).

### 5.4 Weekly cadence

| Meeting            | Length    | Replaces   | Output                                                                                            |
| ------------------ | --------- | ---------- | ------------------------------------------------------------------------------------------------- |
| Flow check (daily) | 10 min    | standup    | A Checker assigned to every waiting change; vague specs flagged; WIP cap enforced                 |
| Intent triage      | 60 min    | refinement | Stories -> ready specs; risk tiers; decision lists answered                                       |
| Retro+             | 60 min    | retro      | Every escaped bug answered with "which check should have caught it?"; harness improvement backlog |
| Setup review       | 30-60 min | (new)      | Versioned harness changes merged; Setup Owner's deputy reviews                                    |

### 5.5 Client cadence

Biweekly 45-minute steering: live demo of working software in the dev environment, the outcome
scorecard (their success metric, the DORA stability pair (change-fail rate and time-to-recover),
the accepted-as-is trend), the decision
list needing their answers, and gate status when a phase boundary is near. Weekly 5-bullet async
summary in between. **No activity metrics in client materials, ever** — no PR counts, no "AI
productivity" claims. Demos and outcomes only. The durable record is the HTML phase report our
tooling generates at each gate.

### 5.6 Hardening passes

Quality is per-change, but integration-level concerns (performance under load, E2E journeys,
penetration testing) run as scheduled hardening passes — typically one mid-Build and one before
Phase 8 — driven by end-to-end and security tooling (in our toolchain, the `/e2e` workflow). These
are scheduled work in the flow, not a phase that gates all other work.

---

## 6. The harness standard

> Cross-phase reference: [`docs/companion/artifact-flow.html`](docs/companion/artifact-flow.html) — what
> each phase receives and produces, where every file lives, and the handoff chain end to end. Each phase's
> final required artifact is named for the phase that consumes it.

What every client delivery repo contains after kit install (Phase 3). The harness is a product:
versioned, owned by the Setup Owner, changed only by reviewed PR.

```
client-repo/
├── CLAUDE.md                  # from kit template: stack standards, domain glossary, risk
│                              # taxonomy, Definition of Ready/Checked, spec conventions,
│                              # gated paths, "done means the hook lets you stop"
├── specs/                     # one file per feature: NNNN-name.md, the source of truth
├── .claude/
│   ├── settings.json          # permission rules: auto-allow safe, ask on gated
│   ├── skills/                # team practices as skills (test-writer, api-pattern, ...)
│   ├── agents/
│   │   ├── grader.md          # grades code against spec; never grades its own work
│   │   └── security-reviewer.md
│   └── hooks/
│       └── stop-gate.ps1      # blocking Stop hook: tests pass + build green or no finish
├── .github/workflows/
│   ├── ci.yml                 # build, test, lint, coverage — hard gates
│   ├── grader.yml             # claude-code-action grader, posts PR comment; required to RUN,
│   │                          # verdict advisory (never blocks)
│   ├── correctness.yml        # fresh agent (≠ grader, ≠ author) hunts changed lines for logic
│   │                          # defects; blocks on a high-confidence defect, named override on record
│   ├── security.yml           # security-reviewer on gated paths or risk:high label; blocks on HIGH
│   └── deploy-dev.yml         # merge to main -> client dev environment
├── infra/                     # Bicep: dev environment first, test/prod added at hardening
└── .sdlc/                     # orchestration-tool state, artifacts, phase reports (committed)
```

CLAUDE.md contents (the kit template, adapted per client in week one): what the project is, the
domain glossary in the client's words, the .NET/Angular/Azure standards (from the
microsoft-enterprise profile and our global coding rules), the spec convention, the risk taxonomy,
what requires plan approval, what paths are gated, and the Definition of Checked. An empty or
stale CLAUDE.md means agents guess, and guesses differ per run — keeping it current is Setup Owner
work, reviewed at setup review.

---

## 7. DevOps

> Deep-dive: `docs/the-rails.md` — the CI/CD and DevOps pipeline as a standing standard: the
> five workflows, the merge bar, deploy and promotion, the agent-safe IaC pipeline, agents working
> inside the pipeline, and the governing principle (agent proposes, gate disposes).

- **Stack default:** .NET 8 / Angular / SQL Server / Azure / GitHub Actions — the example profile
  we ship. A profile-swap appendix in this repo covers what changes for other stacks; everything
  else in this standard is stack-independent.
- **IaC:** Bicep, in-repo, HIGH risk tier. Dev environment provisioned in Phase 3; test and prod
  added at the first hardening pass; prod promoted in Phase 8.
- **Pipeline ownership:** Setup Owner builds it (with Claude drafting the YAML); the client's
  DevOps/security reviews it — they have to operate it after we leave.
- **Secrets:** client's Key Vault and client's GitHub secrets. Never in code, never in CLAUDE.md,
  never in specs. The Anthropic API key is client-procured (section 8).
- **Environments:** merge -> dev (automatic), dev -> test (on demand, smoke-tested), test -> prod
  (Phase 8 ceremony and thereafter on the client's release cadence, human go/no-go every time).

---

## 8. Claude access and the data boundary

Resolved in Phase 0, before anyone opens a terminal:

1. **Default:** the client procures Anthropic access (API or Claude for Work) under their own
   agreement, with Anthropic's standard no-training-on-API-data terms. Keys live in their Key
   Vault / GitHub secrets. The pod works on client-issued seats. Their contract, their keys,
   their audit trail. The kit includes a one-page data-flow brief for their security team:
   what goes to the API (code context from the repo, specs), what doesn't (we tag genuinely
   sensitive material out of agent context), where keys live, who can see usage.
2. **Fallback** (procurement stalled): our firm's keys with a signed client consent rider,
   migrated to client keys as soon as procurement lands.
3. **High-compliance path:** Claude via the client's Azure tenant (Microsoft Foundry). Verify
   current model availability and Claude Code compatibility at Phase 0 before promising it.

Model policy default: plan mode and design work on the strongest available model; implementation
on the standard model; the CI grader on the standard model. Token spend is a client-visible cost
once they hold the keys — the Setup Owner watches it and it appears in the internal dashboard,
never as a client-facing productivity claim.

---

## 9. Gates and metrics

### Phase gates

At every phase boundary an automated gate check runs a fixed battery of validations (integrity,
completeness, metrics, compliance, consistency, quality). Gates report; a named human advances.
(In our toolchain this is the `/sdlc-gate` check — the concept is the battery plus the human, not
the command.) Override rules: the mechanical gates are never overridden; a quality-gate override
requires written justification recorded with the phase state.

### Merge gates

Per section 5.3. Exceptions (a true emergency merge past a gate) require the Pod Lead and one
other human, a `gate-exception` label, and a Retro+ agenda item. Two exceptions in a month means
the gate or the specs are wrong — fix that, don't keep excepting.

### Metrics

Internal dashboard (baseline-and-trend, no vanity targets):

- **Accepted-as-is rate** — agent work merged without rework. The trust signal.
- **Review wait (median)** — the real bottleneck indicator. If it grows, stop opening streams.
- **Rework/revert rate** and **bounce-back-for-unclear rate** — intent quality signals.
- **Escaped bugs** — every one gets a "which check should have caught it?" answer at Retro+.
- **DORA four** — deploy frequency, lead time, change-fail rate, time-to-recover.
- **Security-review wait** — tracked separately; it clears slower and would hide in an average.

When a metric has no data yet, report **"no data"** — never a fabricated zero. A zero reads as a
measured result (zero escaped bugs, zero review wait) and steers the room wrong; "no data" tells
the truth, that nothing has been recorded to read.

Never tracked, never reported: velocity, story points, PR count, lines of code. Agents inflate
all of them, and the published delivery research shows PR volume can double while delivery stays
flat.

Client-facing scorecard: their success metric, the DORA stability pair, accepted-as-is trend,
and the demo. That's it.

---

## 10. The kit (what's in this repo)

The engagement starter. Phase 3 of every engagement begins by installing this into the client
repo and adapting it in the open (the adaptation PRs are the client team's first look at how we
work).

```
delivery-standard/
├── GOLD-STANDARD.md           # this document
├── docs/
│   ├── profile-swap.md        # what changes off the .NET/Angular/Azure default
│   ├── commercial.md          # section 12 expanded: SOW language, workshop agenda
│   ├── data-flow-brief.md     # the client-security one-pager
│   └── po-onboarding.md       # client PO guide: vague-line test, decision lists, their role
├── kit/
│   ├── CLAUDE.md.template
│   ├── spec-template.md
│   ├── settings.json
│   ├── skills/                # generalized skills harvested from engagements
│   ├── agents/                # grader.md, security-reviewer.md
│   ├── hooks/                 # stop-gate.ps1 (+ bash variant)
│   ├── workflows/             # ci.yml, grader.yml, correctness.yml, security.yml, deploy-dev.yml
│   │                          # (+ eval-regression.yml, eval-suite.yml for agentic specs — §11)
│   ├── infra/                 # Bicep starters
│   └── profile/               # microsoft-enterprise profile + SOC 2 gates
└── retros/                    # one file per engagement: what we changed and why
```

**Delivery mechanism:** `kit/` is the canonical source, but the team installs it via the
`claude-code-sdlc` plugin — `/plugin install claude-code-sdlc@mckruz` then `/sdlc-setup` lays the
kit into the client repo (or `/sdlc-harness` to (re)install just the harness). The plugin bundles a
copy of `kit/` regenerated via its `sync_kit` script, so there is one source of truth.

**The harvest loop:** after every engagement, a mandatory retro PR against this repo — skills
generalized (client specifics stripped), hooks improved, templates corrected, a retro file added.
The standard has an owner and a deputy; the deputy reviews harvest PRs. This is the compounding
asset: the second engagement starts where the first one finished.

---

## 11. The AI-engineering module (when the deliverable includes agents)

Activates whenever a spec's deliverable is LLM-powered. Same rigor as the core, because "tests
pass" is not sufficient verification for probabilistic behavior.

- **Evals are acceptance criteria.** An agentic spec includes a golden set (input scenarios with
  graded expected behavior) and a threshold ("correct on >= 95% of the golden set"). The golden
  set is versioned in the repo next to the spec. CI runs the eval suite like it runs tests.
- **Prompts, model selections, and tool definitions are HIGH risk.** Changing any of them is a
  spec with an eval-regression gate: the full golden set runs, and degradation blocks the same
  way a failing test does. No drive-by prompt edits.
- **Observability is a requirement, not a nice-to-have.** Agentic features ship with tracing
  (what the agent saw, decided, called), token cost per task, and failure-mode logging. The
  monitoring phase (9) includes agent-specific alerts: cost spikes, refusal rates, eval drift in
  production samples.
- **The worked example** (`docs/agentic-spec-example.md`, to be added with the first agentic
  engagement) will walk one agentic spec end-to-end: golden set construction,
  the eval harness, the CI wiring, and what the grader checks differently (behavior distribution
  against the golden set, not just code against acceptance lines).
- Security inherits the firm's AI rules: model output is untrusted input; no raw user input
  embedded in system prompts; tool permissions enforced server-side, not by prompt.

---

## 12. The commercial chapter (thin, deliberately)

What the SOW must contain for this methodology to survive contact:

1. **Phase-gated structure.** Billing milestones map to phase gates (the gate report is the
   acceptance artifact), not to calendar dates or feature lists.
2. **The PO clause.** Either the client commits a named product owner at >= 4 hours/week
   (attends intent triage, answers decision lists within 2 business days), or the proxy-mode
   rider applies: we make product decisions on their behalf, logged in a decision log they
   ratify at each steering. The Phase 0 workshop forces this choice explicitly.
3. **Tooling precondition.** Client-procured Anthropic access (or signed fallback rider) is a
   Phase 0 exit condition. The clock on Phase 1 doesn't start without it.
4. **IP terms.** Everything in the delivery repo — code and harness — is the client's. The
   carve-out: generalized methods, templates, skills, and tooling patterns (this repo) remain
   ours and may be reused, stripped of client-specific content. Stated plainly, agreed up front.
5. **Training as a line item.** The client-team capability workstream (their engineers pairing
   into the loop during Build, the PO onboarding, the close gate where they run a spec solo) is
   priced, not given away — it's a deliverable (the capability outcome from the Phase 0
   workshop), and unpaid work is the first thing that gets skipped.
6. **Pricing posture.** Fixed fee per phase, gates as the billing trigger. Outcome-based pricing
   is a future option once we have engagement-level accepted-as-is and outcome data trustworthy
   enough to price against — not before.

The Phase 0 outcome workshop agenda (in `docs/commercial.md`): the three outcomes (business,
software, capability), the one measurable success metric and where it will be read from, the PO
decision, the tooling decision, constraints, and pod introductions.

---

## 13. Close & Transfer (Phase C)

> Deep-dive: `docs/phase-c-close.md` — the shadow flip, the harness audit, the close gate,
> and the clean exit, week by week.

The engagement ends when the client can run this without us:

- [ ] Harness audit: nothing undocumented, no skill or hook only we understand
- [ ] Client Setup Owner named and has merged harness changes themselves
- [ ] Client engineers completed >= 3 specs as Orchestrator with our Checkers, then
- [ ] **The close gate: the client team ran one real spec end-to-end — triage, spec, delegate,
      grade, merge, deploy — without us driving**
- [ ] Final phase reports delivered; outcomes dashboard handed over
- [ ] Our access revoked; harvest retro PR opened against this repo

---

## 14. Defaults you can veto

Decisions made by the standard's author without a dedicated discussion, listed so they're visible:

- WIP cap: no Orchestrator runs more than 2 concurrent agent streams; the pod halts new streams
  when median review wait exceeds one working day.
- The grader uses the same model family as implementation (a fresh context, not a stronger model)
  — independence comes from not having written the code, not from model size.
- `.sdlc/` state and artifacts are committed to the client repo (their visibility, their record).
- Conventional commits enforced by convention and PR title check, not by hook.
- A narrative-companion generator (in our toolchain, `/sdlc-enhance`) produces client-facing
  artifacts at gates, generated by Claude and edited by the Pod Lead before any client sees them.
