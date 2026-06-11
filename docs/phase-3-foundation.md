# Phase 3: Foundation

Deep-dive on the fourth and last phase of the engagement's opening. This is the hinge: the
phase where the documents stop and the software starts. The harness gets installed, the rails
get built, the build loop runs for the first time, and the walking skeleton becomes running
code in the client's own dev environment. Foundation closes, and the engagement crosses out of
the gated phases and into the continuous Build loop.

**If you're starting here:**

|                          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The method**           | Claude (the AI coding agent) drafts documents and writes most code. Humans own every decision and verify every result.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **The rhythm**           | Numbered phases open and close the engagement; in between runs a continuous build loop. Each phase ends with automated checks (the **gate**) plus a named human sign-off. Gates are the billing milestones.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **Where we are**         | Phase 0 fixed the problem. Phase 1 produced a signed requirements baseline. Phase 2 chose the architecture and defined the walking skeleton. Phase 3 makes the architecture real and builds the factory that the Build loop will run in.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Our pod (4-6 people)** | Pod Lead · Setup Owner · Orchestrators · Quality Engineer. ([Team deep-dive](team.md))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

**Words this page leans on** (every other term is explained where it first appears):

| Term                  | What it means                                                                                                                                                                                                                                                  |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The harness**       | The project's CLAUDE.md, specs, skills, agents, hooks, and settings — the context and rules every AI agent loads when it starts work in the repo.                                                                                                              |
| **The kit**           | Our firm's reusable engagement starter: templates, the grader and security-reviewer agents, hooks, pipeline YAML, Bicep starters. It is built and improved **between** engagements (every engagement ends with a retro that feeds improvements back into it) and lives in our own standard repo. Phase 3 installs it into the client's repo and adapts it. The client never pays to build the kit — only to adapt it. |
| **A spec**            | One feature, described in one file in the repo (`specs/NNNN-name.md`): the goal, what is in and out of scope, testable acceptance checks, and a risk tier. It is what the agent builds from — no spec, no build.                                               |
| **The build loop**    | The per-spec cycle — Intent (decide and write what you want), Delegate (an agent builds it inside set bounds), Discern (checks and a non-author prove it) — that replaces batch implementation phases.                                                          |
| **Plan mode**         | The agent mode where Claude can read the repo and propose an approach but cannot change files. Plans get approved by a human before any code is written.                                                                                                        |
| **CI**                | Continuous integration — the automated checks (build, tests, lint, test coverage) that run on every proposed change before it can merge.                                                                                                                        |
| **The grader**        | A fresh AI agent that did **not** write the code. It reads the spec and the change, and posts a check-by-check verdict on the pull request. It is required to run, but its verdict advises — the human Checker decides.                                          |
| **The Stop hook**     | A script that fires when an agent tries to finish its turn. If tests fail or the build is broken, it refuses to let the agent stop. "Done" stops being the agent's opinion.                                                                                     |
| **Branch protection** | Repository settings that make the gates mandatory: no change can merge without CI green, the grader having run, and an approval from someone who didn't write it.                                                                                               |
| **Rails**             | All of the above enforcement, taken together: CI gates, the grader, branch protection, and the deploy pipeline. Called rails because nobody has to remember them — every change runs on them.                                                                   |
| **Walking skeleton**  | The thinnest end-to-end slice of the system, built first to prove the architecture works in practice, not on paper.                                                                                                                                             |
| **Risk tier**         | HIGH / MEDIUM / LOW, assigned per spec. Sets how tightly an agent is bounded and how much review a change gets.                                                                                                                                                 |
| **IaC / Bicep**       | Infrastructure as code: the cloud environment defined in version-controlled files instead of clicked together by hand. Bicep is Azure's language for doing this.                                                                                                |

Phase 3 answers four questions, and nothing else:

1. **Is the harness real and adapted?** (the kit installed into the client repo, CLAUDE.md
   rewritten in the client's own domain, owned by the Setup Owner and reviewed by a deputy)
2. **Are the rails real and enforced?** (CI hard gates, the grader workflow, the security
   workflow, the deploy pipeline, branch protection, the Bicep dev environment, secrets in the
   client's vault)
3. **Does the loop actually run?** (the first specs go Intent → Delegate → Discern → merged →
   deployed — including at least one HIGH-risk spec — so the loop is proven before Build scales
   it)
4. **Is the architecture real?** (the walking skeleton from Phase 2, running end-to-end in the
   client's dev environment through the real pipeline — proven by software, not by documents)

The full feature backlog, the test and production environments, and any feature breadth beyond
the thinnest skeleton are out of scope — they belong to the Build loop and the hardening passes.
Foundation builds the narrowest possible real thing on top of the real rails. Its product is not
a feature; it is a working factory with one part already moving through it.

---

## 1. Who is involved

Phase 3 is the Setup Owner's phase the way Phase 2 was the design authority's and Phase 1 was the
product owner's. The Setup Owner has been building toward this since Phase 0 — the pipeline
groundwork and environment prep ran in parallel while requirements and design closed. Foundation
is where that work lands, gets wired together, and gets exercised by real software.

### Our side

| Person                   | Load    | Workstream                                                                                                                                                                                                  |
| ------------------------ | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Setup Owner**          | 90-100% | The harness as a product: installs and adapts the kit, drafts the Bicep, drafts the pipeline YAML, owns branch protection and secrets. Never the sole approver of their own foundation work.                |
| **Setup Owner's deputy** | 20-30%  | Named on day one (the senior Orchestrator in a 4-6 pod). Reviews every harness change — the pipeline, the IaC, the CLAUDE.md adaptation. This is the both-eyes rule applied to the foundation.              |
| **Orchestrators**        | 60-80%  | Run the walking-skeleton specs through the full build loop — their first real Intent → Delegate → Discern cycles on this engagement. Author the first specs from the Phase 2 slices.                        |
| **Pod Lead**             | 40-50%  | Triages the skeleton into ordered specs, assigns risk tiers, schedules the Build cadences, runs the exit demo, owns the handoff into Build.                                                                 |
| **Quality Engineer**     | 40-50%  | Wires the mechanical gates (coverage, and the eval gate if a spec is agentic), then verifies the running skeleton against the Phase 2 walking-skeleton definition: does it actually prove the architecture? |

### Client side

| Person                                      | Needed for                                                                                                                                                                   | How much                       |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| **DevOps / platform engineer**              | The access realities: branch-protection admin, Actions enabled, runner policy, secrets in their Key Vault and GitHub. Reviews the pipeline — they operate it after we leave. | 4-6 hours across the two weeks |
| **Security**                                | Signs off on the pipeline, the secrets handling, and the data-flow brief; the build-time security gates from Phase 2 get wired and confirmed                                 | 2-3 hours                      |
| **Lead engineer / Setup Owner counterpart** | Pairs into the harness build and reviews the kit-adaptation PRs — the client's first concrete look at how we work                                                            | 4-6 hours                      |
| **Product Owner**                           | Confirms the skeleton slices are the right thinnest end-to-end path; light touch                                                                                             | ~1 hour                        |
| **Sponsor**                                 | The exit demo — working software in their own dev environment                                                                                                                | 45 min                         |

If the client cannot give DevOps the time to provision access and review the pipeline, that is a
gating problem, not a scheduling one — the rails cannot be proven without it, and it goes to the
sponsor at steering before the clock runs out.

### Claude's role in Phase 3

This is the phase where Claude writes the most code in the whole opening — and where that code is
under the tightest gating, because the code _is_ the factory. The risk taxonomy puts IaC and
pipeline changes at HIGH for exactly this reason.

- **Scaffolds the repo from the kit.** The harness lands as a working starting point, not a
  blank repo: CLAUDE.md template, spec template, settings, skills, the grader and
  security-reviewer agents, the Stop hook, the workflow YAML, the Bicep starters.
- **Adapts CLAUDE.md to the client.** The domain glossary in the client's own words, the stack
  standards, the risk taxonomy, the gated paths, the Definition of Checked. A generic CLAUDE.md
  means agents guess the domain, and guesses differ per run.
- **Drafts the Bicep and the pipeline YAML.** Both HIGH risk: human review on every change, the
  Setup Owner's deputy and the client's DevOps reading them before they merge.
- **Runs the walking-skeleton specs through the full loop.** Plan mode first, bounded per spec,
  the Stop hook blocking a failing build, the CI gates and grader on the PR (the pull request —
  the proposed change under review), a human Checker — someone who didn't write the change — on
  the merge. The skeleton is the loop's dress rehearsal — nothing gets skipped because it's
  "only the skeleton."

What Claude never does: merge IaC or pipeline without human review, act as the sole approver of
harness work, put a secret anywhere near the repo, or hand-build the skeleton off the rails to
save a day. The whole point of the phase is that the first real software went _through_ the
rails, not around them.

---

## 2. Day one to the last day

The default calendar is **two weeks (10 business days)** — the longest of the opening phases,
because it builds the factory and runs the first software through it. Week one is the rails:
access, the kit install, the environment, the pipeline. Week two is the skeleton: the four
slices riding the loop, the architecture proven end-to-end, the rails shaken down, the gate.

### Week one — the rails

**Day 1 — kickoff and access.**

- The Phase 0/1 access checklist gets closed: contributor access for the pod, branch-protection
  admin for the Setup Owner (or a named client admin applying our policy), GitHub Actions
  enabled, runner policy agreed (whose machines the pipeline automation runs on), secrets
  provisioning started in the client's Key Vault and GitHub secrets.
- The Anthropic access procured in Phase 0 gets a **live smoke test** — Claude Code actually runs
  on the client's seats and keys, against the client's repo, before anyone depends on it.
- The open questions the Phase 2 handoff carried get their owners and due dates re-confirmed.

**Day 2 — the kit install, in the open.**

- Claude scaffolds the client repo from the kit. The kit itself is not built here — it is our
  firm's standing asset, improved after every engagement; this phase spends its time adapting
  it to the client, never inventing it on the client's clock. The adaptation happens as
  reviewed PRs the client's lead engineer reads — these are the client team's first concrete
  look at how the pod works, months before the close transfer.
- CLAUDE.md gets adapted: the domain glossary in the client's words, the stack standards, the
  risk taxonomy, the gated paths, the Definition of Checked. This is Setup Owner craft, reviewed
  by the deputy.

**Day 3 — the dev environment.**

- Claude drafts the Bicep for the dev environment; HIGH risk, human-reviewed on every change; the
  environment provisions from code, not from clicks.
- Secrets land in the client's Key Vault and GitHub secrets — never in code, never in CLAUDE.md,
  never in a spec. The data-flow brief goes to client security: what goes to the API, what
  doesn't, where the keys live, who can see usage.

**Day 4 — the pipeline.**

- The four workflows get built and reviewed by the client's DevOps: CI (build, test, lint,
  coverage — hard gates), the grader (required to run on every PR; its verdict advises, the
  human decides), the security workflow (fires on the `risk:high` label), and deploy-dev (merge
  to main ships to the client dev environment).
- Branch protection turns on: CI green, the grader has run, and a non-author approval are
  required; `risk:high` adds the security workflow plus a named human sign-off.
- The build-time security gates from the Phase 2 threat review get wired into the security
  workflow.

**Day 5 — the first slice through the loop.**

- The first skeleton spec runs the **full** build loop for the first time on this engagement:
  Intent (the slice triaged into a ready spec), Delegate (the agent in plan mode, bounded, the
  Stop hook refusing to finish on a failing build), Discern (the CI gates and grader on the PR, a
  human Checker on the merge), then the automatic deploy to the client dev environment.
- The rails get exercised by real software. Anything broken in the rails — a gate that doesn't
  fire, a grader that doesn't post, a deploy that doesn't roll back — gets found and fixed here,
  while it is cheap. End of week one: one slice live in dev through the real pipeline.

### Week two — the skeleton

**Day 6 — the first HIGH-risk slice.**

- The slice that touches the riskiest seam (the regulated integration, the sensitive data path)
  runs the loop at HIGH risk: tight agent permissions, the security workflow firing on the
  `risk:high` label and running the security-reviewer agent, a named human sign-off recorded in
  the PR. The HIGH path of the loop gets proven before Build ever relies on it.

**Day 7 — the remaining slices.**

- The rest of the skeleton's slices ride the loop. The slice that emits the **outcome metric**
  gets special attention: it makes the engagement's success metric measurable from day one of
  Build, so the scorecard has real data before the second feature merges.
- Any build-time security gate that touches these slices (a template-review gate, an upload scan)
  fires on its first qualifying PR — proven, not just configured.

**Day 8 — the skeleton, end-to-end.**

- The slices connect into the running skeleton in the dev environment. The QE verifies the
  running software against the Phase 2 walking-skeleton definition: does it prove the
  architecture, end to end, under the rails?
- A first end-to-end smoke journey — an automated test that walks the same path a user would —
  runs across the skeleton: the thinnest proof that the whole thread holds together, not just
  each slice in isolation.

**Day 9 — harden the rails, not the features.**

- The rails get a deliberate shakedown: the Stop hook is proven to actually block a failing
  build, the grader is proven to actually post on a real PR, deploy-dev is proven to roll back
  cleanly. A rail that has never failed safely has not been proven.
- The setup review merges any harness corrections found during the week (Setup Owner + deputy).
- The Build cadences get scheduled — flow check, intent triage, retro+, setup review — and two
  numbers get agreed: the WIP cap (the limit on how many changes may be in flight at once) and
  the review-wait tripwire (the wait-time threshold that, once crossed, stops new work starting
  until the review queue clears).

**Day 10 — gate, demo, and the handoff into Build.**

- The automated gate check runs. The exit demo: the sponsor sees the walking skeleton running in
  their own dev environment, through the real pipeline, with the outcome metric ticking.
- The Build handoff gets drafted: the ordered spec backlog ready for triage, the risk-tier map
  (including the Phase 2 security gates), the cadence calendar, the open questions under their
  original IDs.
- Steering: gate sign-off recorded, billing milestone. The engagement crosses from the gated
  opening into the continuous Build loop.

### When the two weeks stretch

- **Access or secrets provisioning stalls on the client side** — the rails cannot be proven
  without them; this is a gating dependency, surfaced at steering on day one, not absorbed
  silently into a slipping schedule.
- **The dev environment fights the IaC** (a subscription policy, a missing role assignment) —
  expected friction; it is exactly what Phase 3 exists to discover before Build, not during.
- **A skeleton slice exposes a design gap** — good; the skeleton found in days what the documents
  missed. Re-open the relevant ADR explicitly rather than patching around it in code.
- **The client wants to widen the skeleton** ("while we're here, add…") — that is Build scope; it
  delays the rails being proven and the gate being reached. Hold the skeleton to the thinnest
  end-to-end path and let the backlog carry the rest.

---

## 3. The artifacts

> Worked example: [`phase-3-example.md`](phase-3-example.md) — Harbor Mutual's foundation: the
> adapted CLAUDE.md, the four pipeline workflows, the four skeleton specs (one HIGH-risk spec in
> full), the Bicep dev environment, the wired security gates, and the skeleton running in Harbor's
> dev environment with the FNOL→coverage clock already ticking.

| Artifact                                                      | Drafted by                                        | Owned by                      | Done means                                                                                                                                 |
| ------------------------------------------------------------- | ------------------------------------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Installed harness (CLAUDE.md, `.claude/`, `specs/`, settings) | Claude (scaffolds from kit), Setup Owner (adapts) | Setup Owner                   | Adapted to the client's domain, stack, and risk taxonomy; committed; reviewed by the deputy                                                |
| Bicep dev environment                                         | Claude (drafts)                                   | Setup Owner                   | Provisioned from code; HIGH-risk human review on every change; secrets in the client's vault                                               |
| Pipeline workflows (ci, grader, security, deploy-dev)         | Claude (drafts)                                   | Setup Owner                   | CI hard-gates; grader required to run; security fires on `risk:high`; deploy-dev on merge — all running, all reviewed by client DevOps     |
| Branch protection                                             | Setup Owner (or named client admin)               | Setup Owner                   | Enforces CI green + grader-ran + non-author approval; `risk:high` adds the security workflow + a named sign-off                            |
| Walking-skeleton specs                                        | Orchestrators (from the Phase 2 slices)           | Pod Lead                      | Each rides the full build loop; together they prove the architecture in running software                                                   |
| The walking skeleton (deployed)                               | The build loop                                    | Setup Owner + QE              | End-to-end in the client's dev environment through the real pipeline; verified against the Phase 2 definition                              |
| Build-time security gates (wired)                             | Claude (drafts), security (confirms)              | Setup Owner + client security | The Phase 2 gates enforced in the security workflow; each fired at least once on a real PR                                                 |
| Data-flow brief                                               | Claude (drafts), Setup Owner                      | Setup Owner                   | Client security has, in writing: what goes to the API, what doesn't, where keys live, who sees usage                                       |
| Cadence calendar + risk-tier map                              | Pod Lead                                          | Pod Lead                      | Flow check, intent triage, retro+, and setup review scheduled; WIP cap and review-wait tripwire set; the Phase 2 security gates on the map |
| Build handoff                                                 | Claude (drafts)                                   | Pod Lead                      | Ordered spec backlog, risk-tier map, cadences, open questions under their original IDs                                                     |

What is deliberately **not** produced: the full feature backlog (Build triage owns it), the test
and production environments (the first hardening pass and Phase 8 add them), and any feature
breadth beyond the thinnest skeleton.

---

## 4. The cadences

| Rhythm                          | Who                                | What                                                                                                  |
| ------------------------------- | ---------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **Daily 15-minute pod sync**    | Whole pod                          | Rails progress, spec status, blockers                                                                 |
| **The kit-adaptation PRs**      | Setup Owner + client lead engineer | The client's first look at how we work — reviewed in the open, not handed over finished               |
| **Setup review**                | Setup Owner + deputy               | Harness changes merged and reviewed; the first real run of a cadence that continues all through Build |
| **Intent triage (begins here)** | Pod Lead + Orchestrators           | The skeleton slices become ordered specs; the Build loop's weekly cadence starts in this phase        |
| **Biweekly steering**           | Sponsor + Pod Lead                 | Falls at the end of the phase: the exit demo — working software in the client's own dev environment   |

---

## 5. The exit gate

Phase 3 closes — and the engagement enters the Build loop — when all of these are true:

- [ ] The harness is installed, adapted to the client, committed, and reviewed by the Setup
      Owner's deputy (the Setup Owner is never the sole approver of their own foundation)
- [ ] The pipeline runs: CI hard gates, the grader required to run, the security workflow on
      `risk:high`, deploy-dev on merge — all reviewed by the client's DevOps
- [ ] Branch protection enforces CI green + grader-ran + non-author approval; `risk:high` adds
      the security workflow and a named sign-off
- [ ] The Bicep dev environment is provisioned from code; secrets live in the client's vault,
      never in code
- [ ] The build-time security gates from Phase 2 are wired, and each has fired on a real PR
- [ ] The walking skeleton is deployed to the client's dev environment through the real
      pipeline — running software, not a document — and verified against the Phase 2 definition
- [ ] At least one HIGH-risk spec has run the full loop (the HIGH path is proven before Build
      depends on it)
- [ ] The rails are proven, not just present: the Stop hook actually blocks, the grader actually
      posts, deploy-dev actually rolls back
- [ ] The outcome metric is measurable in dev (the metric slice exists and ticks)
- [ ] The Build cadences are scheduled and the WIP cap and review-wait tripwire are set
- [ ] A named human on each side approved the advance — gates report, humans decide

---

## 6. What goes wrong in Phase 3

- **Skipping the loop "because it's just the skeleton."** The skeleton is precisely where the
  loop must be proven. A skeleton hand-built off the rails teaches the team nothing and hides the
  rails' defects until Build, when they are expensive. Every skeleton slice runs the full
  discipline.
- **A pipeline that exists but was never exercised.** CI that is green because nothing real ran
  through it. The rails are proven by a spec breaking and being caught, not by the YAML being
  present. A rail that has never failed safely has not been proven.
- **The kit installed but not adapted.** A generic CLAUDE.md means agents guess the domain, and
  guesses differ per run. The adaptation in the open is the point of the phase, not a formality
  to rush past.
- **IaC or pipeline merged without review to move faster.** These are HIGH risk because they are
  hard to undo and run in production later. The Setup Owner is never the sole approver of their
  own foundation — the deputy and the client's DevOps read every change.
- **A secret in the repo.** The one unrecoverable mistake of the phase: a key in a commit is a
  rotation event and an audit-log review, not an edit. The client's vault from day one, never in
  code, never in CLAUDE.md, never in a spec.
- **A feature-rich skeleton.** The skeleton is the thinnest end-to-end slice that proves the
  architecture. Every slice added beyond that is Build scope wearing a Foundation badge — it
  delays the rails being proven and the gate being reached.
- **Deferring the deputy.** "I'll name a deputy later" means the Setup Owner is approving their
  own foundation right now. The deputy is named on day one, or the both-eyes rule the standard
  depends on is already broken.
- **The demo on a laptop.** The exit demo runs in the client's own dev environment, through the
  real pipeline, or it has not proven what Phase 3 exists to prove. A localhost demo proves the
  code compiles, not that the factory works.

---

Next: [The Build Loop](build-loop.md) — what the factory was built for: how every change from
here to feature-complete gets specified, bounded, built, and proven.
