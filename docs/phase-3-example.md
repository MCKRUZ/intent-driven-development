# Phase 3 Worked Example: Harbor Mutual

The continuation of [the Phase 2 example](phase-2-example.md), companion to
[the Phase 3 deep-dive](phase-3-foundation.md). Phase 2 closed Friday 2026-03-27 with four signed
ADRs, the contracts carrying REQ-014's error spec, two build-time security gates, and a
walking-skeleton definition sliced into four specs. Phase 3 turns that into running software.

Two roles shift this phase. **Wes Carter**, Harbor's lead engineer who co-signed every ADR,
becomes the Setup Owner counterpart — he pairs into the harness build and reviews the adaptation
PRs. And one person joins the story: **Tom Reilly**, Harbor's platform engineer, who owns branch
protection, the runners (the machines that execute the CI jobs), and the secrets, and who
reviews the pipeline he will operate after the pod leaves. His hours, like Wes's, are the handoff being built early.

**The story so far (you can start here):**

|                          |                                                                                                                                                                                                                                                                                |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **The client**           | Harbor Mutual — a fictional regional insurer. They hired a five-person consulting pod to rebuild how property-insurance claims get reported and decided.                                                                                                                       |
| **The problem**          | A claim takes a median of **11.4 days** from FNOL (first notice of loss — the policyholder reporting the damage) to a coverage decision.                                                                                                                                       |
| **The target**           | Median **5 days or less**.                                                                                                                                                                                                                                                     |
| **Where we are**         | Phases 0-2 fixed the problem, signed the requirements, and chose the architecture. This phase builds the factory and runs the first real software through it.                                                                                                                  |
| **The architecture**     | Coverage checks read the nightly **snapshot replica** of PolicyOne (Harbor's policy administration system) directly (ADR-001), behind a verification service that owns a staleness contract — the rules for how old the replica's data may be and what happens when it is older. Claims live in a relational model plus an append-only event log (ADR-002). Surge is absorbed by a buffered queue (ADR-003). |
| **The walking skeleton** | The thinnest end-to-end path, sliced into four specs — listed just below. Each rides the full loop; together they prove the architecture.                                                                                                                                      |
| **The security gates**   | Two build-time gates from the Phase 2 threat review: malware scanning on the document-upload path (HIGH), and a PII (personally identifiable information) template-review gate on acknowledgment letters.                                                                      |
| **Our pod**              | Maya Chen (Pod Lead) · Rob Feld (Setup Owner — builds and owns the harness) · Jonah Kim (Orchestrator, and Rob's named deputy) · Sara Whitfield (Orchestrator/Checker) · Nadia Brooks (Quality Engineer).                                                                      |
| **Harbor's cast**        | Karen Voss (VP Claims Operations — sponsor) · Luis Ortega (product owner) · Wes Carter (lead engineer, Setup Owner counterpart) · Tom Reilly (platform engineer) · Dan Kowalski (IT security) · Priti Shah (data and reporting lead).                                          |

**The four walking-skeleton specs:**

| Spec     | What it is                     |
| -------- | ------------------------------ |
| **0001** | Queue entry from a portal FNOL |
| **0002** | Replica verification read      |
| **0003** | Test-mode acknowledgment       |
| **0004** | Metric event                   |

**The IDs you'll see on this page** (IDs are stable across phases):

| ID               | What it is                                      |
| ---------------- | ----------------------------------------------- |
| **ADR-NN**       | Architecture decision record                    |
| **REQ-NN**       | Requirement                                     |
| **NFR-NN**       | Non-functional requirement                      |
| **Q-NN**         | Open question with a named owner                |
| **D-NN**         | Product decision                                |
| **C-NN**         | Constraint from Phase 0                         |
| **NNNN-name.md** | A spec file — one feature, one file in the repo |

**Words this page leans on** (everything else is explained where it first appears):

| Term                  | What it means                                                                                                                                                                                                                                                                                                    |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The harness**       | The project's CLAUDE.md, specs, skills, agents, hooks, and settings — the context and rules every AI agent loads when it starts work in the repo.                                                                                                                                                                 |
| **The kit**           | Our firm's reusable engagement starter: templates, the grader and security-reviewer agents, hooks, pipeline YAML, Bicep starters. Built and improved between engagements in our own standard repo; Phase 3 installs it into Harbor's repo and adapts it. Harbor never pays to build the kit — only to adapt it.   |
| **The build loop**    | The per-spec cycle — Intent (decide and write what you want), Delegate (an agent builds it inside set bounds), Discern (checks and a non-author prove it). When a spec "rides the loop," this is the ride.                                                                                                        |
| **Plan mode**         | The agent mode where Claude can read the repo and propose an approach but cannot change files. A human approves the plan before any code is written.                                                                                                                                                              |
| **CI**                | Continuous integration — the automated checks (build, tests, lint, test coverage) that run on every proposed change before it can merge.                                                                                                                                                                          |
| **The grader**        | A fresh AI agent that did **not** write the code. It reads the spec and the change, and posts a check-by-check verdict on the pull request. It is required to run, but its verdict advises — the human decides.                                                                                                   |
| **The Stop hook**     | A script that fires when an agent tries to finish. If tests fail or the build is broken, it refuses to let the agent stop.                                                                                                                                                                                        |
| **Branch protection** | Repository settings that make the gates mandatory: no change can merge without CI green, the grader having run, and an approval from someone who didn't write it.                                                                                                                                                 |
| **Rails**             | All of the above enforcement taken together: CI gates, the grader, branch protection, and the deploy pipeline. Every change runs on them.                                                                                                                                                                         |
| **Risk tier**         | HIGH / MEDIUM / LOW, assigned per spec. Sets how tightly an agent is bounded and how much review a change gets.                                                                                                                                                                                                   |
| **Bicep**             | Azure's language for infrastructure as code — the cloud environment defined in version-controlled files instead of clicked together by hand.                                                                                                                                                                      |

## 1. How the two weeks played out

> **Reading the Tooling lines.** **You run it** — a slash command you type (e.g. `/sdlc-gate`,
> `/e2e`). **It triggers** — an agent or script that command runs under the hood, always shown
> after a `→`. **No plugin command** — a human meeting, client-system work, repo scaffolding, or
> a spec riding the build loop; nothing the plugin drives directly. Foundation is the least
> plugin-driven phase of the opening: most of the work is code and rails, so most days carry the
> grey pill. The plugin returns at the gate.

### Week one — the rails

**Day 1 (Mon 3/30) — kickoff and access.**
**Tooling —** No plugin command. Access negotiation with Harbor's platform team; a live smoke
test of Claude Code on Harbor's procured seats.

- The Phase 0/1 access checklist closes: the pod gets contributor access to Harbor's repo, Rob
  gets branch-protection admin, Tom enables GitHub Actions and agrees the runner policy
  (Harbor-hosted), and secrets provisioning starts in Harbor's Key Vault (Azure's managed store
  for keys and secrets).
- The Anthropic access Harbor procured in Phase 0 gets a **live smoke test** — a quick
  does-it-actually-work check: Claude Code runs on
  Harbor's seats, against Harbor's repo, on Harbor's keys. It works — the fallback rider is never
  needed.
- The two open questions from Phase 2 get re-confirmed: **Q-17** (postal dispatch vendor — Dan +
  Harbor ops, due this phase) and **Q-18** (surge load-test dataset — Priti + Nadia, due before
  hardening pass 1).

**Day 2 (Tue 3/31) — the kit install, in the open.**
**Tooling —** No plugin command. Claude scaffolds Harbor's repo from the delivery-standard kit;
CLAUDE.md adapted in PRs Wes reviews.

- Claude scaffolds the repo from the kit: CLAUDE.md template, spec template, settings, the grader
  and security-reviewer agents, the Stop hook, the workflow YAML, the Bicep starters.
- CLAUDE.md gets adapted to Harbor in the open: the domain glossary in Harbor's words (FNOL,
  PolicyOne, the snapshot replica, the fast-path, the regulatory clock), the .NET 8 / Angular /
  SQL Server / Azure standards, the risk taxonomy, the gated paths (`infra/`, the replica
  adapter, migrations, acknowledgment-letter templates), and the Definition of Checked (what
  must be true before a change counts as done). **Wes reviews the adaptation PRs** — Harbor's
  first concrete look at how the pod works.

**Day 3 (Wed 4/1) — the dev environment.**
**Tooling —** No plugin command. Claude drafts the Bicep (HIGH risk, reviewed every change); the
data-flow brief goes to Dan.

- Claude drafts the Bicep for Harbor's dev environment; Rob and Tom review every change. The
  environment provisions from code: the app hosting, the buffered queue (ADR-003), and the
  **private endpoint to the snapshot replica** under the Q-15 controls.
- Secrets land in Harbor's Key Vault and GitHub secrets — the Anthropic key, the Azure
  credentials, the replica's read-only service-account reference. Nothing in code. The
  **data-flow brief** goes to Dan: what reaches the API (repo code context, specs), what is held
  out, where the keys live, who can see usage.

**Day 4 (Thu 4/2) — the pipeline.**
**Tooling —** No plugin command. Claude drafts the ci/grader/correctness/security/deploy-dev YAML; Tom
reviews and enables branch protection.

- The five workflows get built and reviewed by Tom: **ci.yml** (build, test, lint, 80% coverage —
  hard gates), **grader.yml** (claude-code-action: a fresh agent reads the spec in the diff and
  posts a check-by-check verdict; required to run, advisory verdict), **correctness.yml** (a fresh
  agent hunts the changed lines for plain logic defects; blocks on a high-confidence defect, with a
  named-human override on the record), **security.yml** (fires on
  the `risk:high` label, runs the security-reviewer agent), **deploy-dev.yml** (merge to main
  ships to Harbor's dev environment).
- Rob turns on branch protection: CI green, grader-ran, and a non-author approval are required;
  `risk:high` adds security.yml plus a named sign-off. The two Phase 2 security gates get wired —
  the upload malware scan and the acknowledgment-letter PII template-review gate.

**Day 5 (Fri 4/3) — the first slice through the loop.**
**Tooling —** No plugin command. Spec 0001 rides the loop: Orchestrator authors from the kit
spec-template, the agent codes in plan mode under bounds, the PR fires ci.yml + grader.yml, a
human Checker merges, deploy-dev.yml ships to dev.

- **Spec 0001 (queue entry from a portal FNOL)** runs the full build loop for the first time on
  this engagement. Sara authors the spec from the kit template (Goal, Why, Scope in/out,
  Acceptance checks, Risk tier MEDIUM, Delegation plan, Checking plan). The agent works in plan
  mode; Sara corrects the plan before any code. The Stop hook refuses to let it finish on a
  failing build.
- The PR fires ci.yml and grader.yml. The grader posts a check-by-check verdict; **Jonah** (not
  the author) reads it, approves, and merges. deploy-dev.yml ships it to Harbor's dev
  environment. One thing breaks in the rails — the coverage gate miscounts generated files — and
  is fixed here, on day five, where it is cheap. End of week one: a portal FNOL creates a queue
  entry in Harbor's dev environment, through the real pipeline.

### Week two — the skeleton

**Day 6 (Mon 4/6) — the first HIGH-risk slice.**
**Tooling —** No plugin command. Spec 0002 rides the loop at HIGH risk: the `risk:high` label
fires security.yml → the security-reviewer agent; Dan's named sign-off in the PR.

- **Spec 0002 (replica verification read)** is HIGH risk — it touches the replica integration and
  the Q-15 controls. The agent runs under tight permissions; the `risk:high` label fires
  security.yml, which runs the security-reviewer agent over the diff. **Dan reviews and records a
  named sign-off** in the PR.
- The Q-15 controls get verified live against the dev environment: the read-only service account,
  the private endpoint, the audit trail. The staleness contract from ADR-001 (the 02:00-04:30
  refresh-window degradation) goes in as real behavior — `pending-verification`, intake never
  blocked. The HIGH path of the loop is proven before Build relies on it.

**Day 7 (Tue 4/7) — the remaining slices.**
**Tooling —** No plugin command. Specs 0003 and 0004 ride the loop; the PII template-review gate
fires on 0003's PR.

- **Spec 0003 (test-mode acknowledgment)** wires the acknowledgment path in test mode (no letters
  actually leave the system). Its PR is the first to touch acknowledgment-letter templates, so
  the **PII template-review gate fires** — proven, not just configured.
- **Spec 0004 (metric event)** emits the FNOL→coverage clock as a structured event. It is the
  slice that lights up the outcome scorecard: Harbor's success metric becomes measurable from day
  one of Build, not as a Phase 9 afterthought.

**Day 8 (Wed 4/8) — the skeleton, end-to-end.**
**Tooling —** `/e2e` → a Playwright journey across the FNOL→metric path.

- The four slices connect in Harbor's dev environment: a portal FNOL → queue entry → replica
  coverage check → test-mode acknowledgment → metric event. **Nadia verifies the running
  skeleton against the Phase 2 walking-skeleton definition** — it proves the architecture, end to
  end, under the rails.
- A first E2E smoke journey — an automated end-to-end pass over the whole user path, checking
  that it works at all rather than testing it deeply — runs the whole thread with the `/e2e`
  skill: the thinnest proof that the slices hold together, not just each in isolation. Nadia confirms each NFR's proving method
  now has a real place to read its number, now that the metric event exists.

**Day 9 (Thu 4/9) — harden the rails, not the features.**
**Tooling —** No plugin command. The rails get a deliberate shakedown; the setup review merges
harness corrections.

- The rails get shaken down on purpose: a deliberately failing build proves the Stop hook
  **blocks**; a PR with a planted spec mismatch proves the grader **posts** the miss; a bad
  deploy proves deploy-dev **rolls back** cleanly (the environment returns itself to the last
  good version). A rail that has never failed safely has not been proven.
- The setup review (Rob + Jonah, his deputy) merges the week's harness corrections — the coverage
  gate fix, two CLAUDE.md glossary additions the agents kept missing. The Build cadences get
  scheduled — flow check (daily), intent triage (weekly), retro+ (the retro that feeds
  improvements back into the kit), setup review — and two flow limits get set: the WIP cap (the
  limit on how much work may be in flight at once — at most 2 streams per Orchestrator) and the
  review-wait tripwire (once the median review wait passes one working day, no new streams start
  until the queue clears).
- **Q-17 lands:** Dan and Harbor ops choose the postal dispatch vendor; credential provisioning
  starts. It surfaces one new open question — **Q-19** (the vendor's sandbox credentials for the
  acknowledgment-delivery spec), owner Tom + Harbor ops, due before the first
  acknowledgment-delivery spec in Build.

**Day 10 (Fri 4/10) — gate, demo, and the handoff into Build.**
**Tooling —** `/sdlc-gate` → `check_gates.py` · `/sdlc-phase-report` → `generate_phase_report.py`
· `/visual-explainer` → renders the demo narrative · `/sdlc-next` → `advance_phase.py` (after the
human sign-off).

- **`/sdlc-gate`** passes. **`/sdlc-phase-report`** renders the gate packet (the phase's
  evidence, bundled for sign-off). Claude drafts the
  Build handoff: the ordered spec backlog ready for triage, the risk-tier map (including the two
  security gates), the cadence calendar, and the open questions (Q-18, Q-19) under their IDs.
- **The exit demo:** Karen watches a portal FNOL flow end to end in Harbor's own dev environment,
  through the real pipeline, with the FNOL→coverage clock **ticking on the scorecard** — rendered
  with `/visual-explainer`, not slides. Working software, in their environment, on day one of the
  build.
- The phase review: Rob and Wes walk the harness, Tom confirms the pipeline he will operate, Dan
  confirms the security gates, Karen approves. **`/sdlc-next`** re-verifies the gates and advances
  the engagement out of the gated opening and into the **Build loop**. Billing milestone 4.

## 2. What to notice

- **Foundation is the least plugin-driven phase — and that is the point.** The plugin drives the
  document phases; Foundation is hands building the factory and the first real specs riding the
  loop. The Tooling bars go quiet because the work is code and rails, not drafts. The plugin
  returns only at the gate.
- **The skeleton ran the full loop, including a HIGH-risk spec.** Spec 0002 exercised the
  `risk:high` path — tight permissions, the security workflow, Dan's named sign-off — on software
  that was cheap to get wrong. The dress rehearsal happened before Build depended on the HIGH
  path working.
- **The metric event made the outcome measurable on day one of Build.** Spec 0004 means the
  FNOL→coverage clock ticks in dev from the first slice. The scorecard has real data before the
  second feature merges — the metric is not a Phase 9 retrofit.
- **The adaptation happened in the open.** Wes reviewed the CLAUDE.md adaptation PRs and Tom
  reviewed the pipeline YAML — Harbor's first concrete look at how the pod works, and the
  transfer rehearsed months before the close.
- **Secrets never touched the repo.** Harbor's Key Vault held the Anthropic key, the Azure
  credentials, and the replica service-account reference from day one. The data-flow brief gave
  Dan what he needed to sign off without a single secret in a commit.
- **A rail broke on day five, on purpose-adjacent timing.** The coverage gate miscounted
  generated files on the very first real spec — found and fixed while it cost an hour, not in
  Build week three when it would have blocked every PR.

---

## 3. Artifact: the adapted CLAUDE.md (excerpt)

_The kit template, adapted to Harbor in PRs Wes reviewed. The full file is longer; this is the
shape._

- **What this project is** — Harbor Mutual's property-claims intake rebuild; the FNOL→coverage
  median target of ≤5 days, and where that number is read from.
- **Domain glossary (Harbor's words)** — FNOL, PolicyOne, the snapshot replica, the fast-path
  (61% of claims, D-09), the duplicate-merge rule (D-07), the regulatory clock (C-04: 15 business
  days in two states).
- **Stack standards** — .NET 8 / Angular / SQL Server / Azure / GitHub Actions, immutability
  defaults, Result&lt;T&gt; for expected failures, FluentValidation at the boundary.
- **Risk taxonomy** — HIGH (the replica adapter, `infra/`, migrations, auth, acknowledgment-letter
  templates, public API contracts); MEDIUM (new business logic, integrations); LOW (UI in
  existing patterns, copy, additive CRUD).
- **Gated paths** — `infra/`, the replica adapter, `migrations/`, acknowledgment templates: the
  agent asks before touching these.
- **Definition of Checked** — the spec's acceptance checks pass; the Stop hook is green; the
  grader has run; a non-author approved; HIGH risk carries a named sign-off.

## 4. Artifact: the pipeline

_The five workflows, all reviewed by Tom, branch protection enforcing them._

| Workflow         | Trigger           | What it does                                                                                 | Blocks?                                 |
| ---------------- | ----------------- | -------------------------------------------------------------------------------------------- | --------------------------------------- |
| `ci.yml`         | Every PR          | Build, test, lint, 80% coverage on new code                                                  | Hard block                              |
| `grader.yml`     | Every PR          | claude-code-action: a fresh agent reads the spec in the diff, posts a check-by-check verdict | Required to run; verdict advisory       |
| `correctness.yml`| Every PR          | A fresh agent hunts the changed lines for plain logic defects                                | Blocks on a high-confidence defect (named-human override on the record) |
| `security.yml`   | `risk:high` label | Runs the security-reviewer agent over the diff                                               | Pass + named sign-off required to merge |
| `deploy-dev.yml` | Merge to `main`   | Ships to Harbor's dev environment                                                            | — (deploy step)                         |

**Branch protection on `main`:** CI green + grader-ran + one non-author approval. `risk:high`
adds security.yml passing and a named human sign-off recorded in the PR.

## 5. Artifact: the walking-skeleton specs

_Four specs, authored from the kit spec-template, each riding the full loop._

| Spec | Slice                          | Risk     | What it proved                                                                                                                    |
| ---- | ------------------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 0001 | Queue entry from a portal FNOL | MEDIUM   | The ingestion path and the buffered queue (ADR-003); the rails caught a coverage-gate defect on first run                         |
| 0002 | Replica verification read      | **HIGH** | The replica integration and the Q-15 controls live; the staleness/refresh-window degradation (ADR-001); the HIGH path of the loop |
| 0003 | Test-mode acknowledgment       | MEDIUM   | The acknowledgment path in test mode; fired the PII template-review security gate                                                 |
| 0004 | Metric event                   | LOW      | The FNOL→coverage clock as a structured event; the outcome scorecard measurable from Build day one                                |

## 6. Artifact: spec 0002 in full (the HIGH-risk one)

**Spec 0002 — Replica verification read**
Risk tier: **HIGH** · Authored: Jonah Kim · Checked: Sara Whitfield · Security sign-off: Dan
Kowalski · Merged 2026-04-06

**Goal.** A coverage-verification service reads the PolicyOne snapshot replica directly (ADR-001)
and returns coverage status with an as-of timestamp, honoring the staleness contract.

**Why.** REQ-014 promises same-business-day coverage status; ADR-001 chose the replica read as
the source. This slice proves the integration and its degradation behavior in running software.

**Scope in.** The replica adapter, the verification service, the staleness contract (as-of
timestamp; >36h escalates; refresh-window 02:00-04:30 degrades to `pending-verification`).
**Scope out.** The fast-path escalation logic (REQ-019, a Build spec); real acknowledgment
dispatch (0003 is test-mode).

**Acceptance checks.** Fresh data → status + as-of timestamp. Policy not found → `needs-review`
with a reason code, never a silent "verified." Refresh window or unreachable → `pending-verification`,
intake never blocked. Snapshot >36h → staleness warning, written-acknowledgment-state claims
escalate.

**Delegation plan.** The agent may touch the replica adapter and the verification service.
**Gated:** the Q-15 service-account configuration and the private-endpoint settings (the agent
proposes; a human applies). Plan-mode approval before any code.

**Checking plan.** Full ladder: CI hard gates, the grader, a non-author Checker (Sara). Because
HIGH: the security.yml security-reviewer pass and Dan's named sign-off in the PR.

**How it rode the loop.** Plan approved by Jonah → agent implemented under tight permissions →
Stop hook green → PR fired ci.yml, grader.yml, and (on the `risk:high` label) security.yml → Dan
signed off → Sara merged → deploy-dev shipped it. The Q-15 controls were verified live against
the dev environment the same afternoon.

## 7. Artifact: the Bicep dev environment (summary)

_Drafted by Claude, reviewed every change by Rob and Tom, provisioned from code._

- **Resource group + app hosting** for the intake service and the Angular portal.
- **The buffered ingestion queue** (ADR-003), sized for dev; the surge profile load test waits on
  Q-18 and a test environment at hardening pass 1.
- **The private endpoint to the snapshot replica** under the Q-15 controls — read-only service
  account, no public path, every access audited.
- **Key Vault references** for the Anthropic key, Azure credentials, and the replica service
  account. No secret in code, CLAUDE.md, or any spec.
- **The deploy-dev target** — what `deploy-dev.yml` ships to on merge.

## 8. Artifact: the build-time security gates, wired

_The two gates from the Phase 2 threat review, now enforced and each fired on a real PR._

- **Document-upload malware scan** — HIGH tier; security.yml runs on every PR touching the upload
  path. (The upload path itself is a Build spec; the gate is wired and tested with a probe PR — a
  throwaway change to the upload path opened solely to confirm the gate fires, then closed
  unmerged.) The template-review gate triggers on the templates path itself, independent of the
  risk label — which is why it fired on 0003's MEDIUM PR.
- **Acknowledgment-letter PII template-review gate** — fired live on spec 0003's PR, the first to
  touch acknowledgment templates. PII leaves the system on paper, so a human reviews any template
  change.

## 9. Artifact: the Build handoff (summary)

- **The factory:** the adapted harness, the five-workflow pipeline, branch protection, and the
  Bicep dev environment — all owned by Rob, reviewed by Jonah and Tom.
- **The proof:** the walking skeleton running in Harbor's dev environment, verified against the
  Phase 2 definition, with the FNOL→coverage clock ticking on the scorecard.
- **The risk-tier map:** the HIGH/MEDIUM/LOW taxonomy in CLAUDE.md, plus the two build-time
  security gates registered against the paths they guard.
- **The cadences:** flow check (daily), intent triage (weekly), retro+, setup review; WIP cap 2
  streams per Orchestrator; halt new streams past one working-day median review wait.
- **Open questions into Build:**

| ID   | Question                                                                                              | Owner                     | Due                                           |
| ---- | ----------------------------------------------------------------------------------------------------- | ------------------------- | --------------------------------------------- |
| Q-18 | Construction of the surge load-test dataset from the 2024 CAT (catastrophe) event (volume curve + channel mix) | Priti Shah + Nadia Brooks | Before hardening pass 1                       |
| Q-19 | Postal vendor sandbox credentials for the acknowledgment-delivery spec (follows Q-17's vendor choice) | Tom Reilly + Harbor ops   | Before the first acknowledgment-delivery spec |

- **Recommended first Build specs:** the fast-path escalation (REQ-019, builds on 0002), the
  document-upload path (triggers the malware-scan gate), and the email FNOL extraction (ADR-004 —
  the engagement's first agentic spec, where the feature itself runs on an AI model. That
  activates the AI-engineering module: a golden set (real example inputs with known correct
  answers) as acceptance criteria, the eval gate in CI (every change is scored against that set),
  prompt/model changes tiered HIGH).

---

## 10. The tooling behind this phase

The abstract Phase 3 page describes this work generically. What actually ran — and how little of
it was the plugin, which is itself the point:

| What got produced                        | How                                                                                                                                                         |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Repo scaffold + CLAUDE.md adaptation     | Claude scaffolds from the delivery-standard kit; adapted in PRs Wes reviewed; no plugin command — Foundation is hands-on                                    |
| Bicep dev environment                    | Claude drafts; HIGH risk, Rob + Tom review every change; secrets in Harbor's Key Vault                                                                      |
| Pipeline (ci/grader/correctness/security/deploy-dev) | Claude drafts the YAML against the kit workflow starters; Tom reviews; Rob enables branch protection                                                        |
| Walking-skeleton specs (0001-0004)       | Orchestrators author from the kit spec-template; each rides the full loop — plan mode, Stop hook, ci.yml + grader.yml, a non-author Checker, deploy-dev.yml |
| The HIGH-risk path (0002)                | `risk:high` label → security.yml → the security-reviewer agent; Dan's named sign-off in the PR                                                              |
| Skeleton smoke journey                   | `/e2e` → a Playwright journey across the FNOL→metric path                                                                                                   |
| Rails shakedown + setup review           | Manual — prove the Stop hook blocks, the grader posts, deploy-dev rolls back; Rob + Jonah (deputy) merge harness corrections                                |
| Gate, packet, demo, advance              | `/sdlc-gate`, `/sdlc-phase-report`, `/visual-explainer` (demo narrative), `/sdlc-next` (after the gate sign-off)                                            |

---

Next: [the Build loop worked example](build-loop-example.md) — one ordinary week of Build:
two specs end to end, and the grader catching a bug that eleven green tests missed.
