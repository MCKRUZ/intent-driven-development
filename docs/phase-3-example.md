# Phase 3 Worked Example: Harbor Mutual

The continuation of [the Phase 2 example](phase-2-example.md), companion to
[the Phase 3 deep-dive](phase-3-foundation.md). Phase 2 closed Friday 2026-03-27 with four signed
ADRs, the contracts carrying REQ-014's error spec, two build-time security gates, and a
walking-skeleton definition sliced into four specs. Phase 3 turns that into running software.

This page mirrors the Example track of the Phase 3 companion: what Foundation received, the
ten-day procedure, the artifact ledger, the factory as installed, the HIGH-risk slice in full,
and what crosses into the Build loop. Two roles shift this phase — **Wes Carter**, Harbor's lead
engineer, becomes the Setup Owner counterpart, and **Tom Reilly**, Harbor's platform engineer,
joins to own branch protection, the runners, and the secrets. Their hours are the handoff being
built early.

## What Phase 3 received

Phase 2 closed Friday 2026-03-27 with four signed ADRs, contracts carrying REQ-014's error spec,
two build-time security gates named, and a walking skeleton sliced into four specs. Harbor Mutual
— a fictional regional insurer rebuilding how property-insurance claims get reported and decided,
cutting an **11.4-day** median from FNOL (first notice of loss) to a coverage decision down to
**5 days or less** — had a signed problem, signed requirements, and a chosen architecture, and
**not one line of it running anywhere**. Foundation turns that into running software.

**Inherited from Phase 2** — on disk under `.sdlc/artifacts/02-design/`:

- `phase3-handoff.md`
- `design-doc.md`
- `api-contracts.md`
- `adrs/` + `adr-registry.md`
- `deep-plan-checkpoint.yaml`

**Also inherited** — but as knowledge in a head, because Phase 2 wrote no file for any of them:

- the walking-skeleton definition
- the threat mitigation map — becomes the risk-tier map
- the NFR proving plan

Read that second row twice. Three of the things Phase 3 builds directly on never became files.
The method required each of them; no command in `claude-code-sdlc` wrote any of them. They cross
the boundary as what Nadia and Rob remember from Phase 2's Thursday — which is exactly why the
people who were in that room are the people who build the foundation.

> **The architecture Phase 3 has to make real.** Coverage checks read the nightly snapshot replica
> of PolicyOne directly (**ADR-001**), behind a verification service that owns the staleness
> contract. Claims live in a relational model plus an **append-only event log** (**ADR-002**). Surge
> is absorbed by a buffered ingestion queue and autoscaling (**ADR-003**). Email FNOL is extracted by
> an LLM with per-field confidence thresholds (**ADR-004**). Every one of those four mechanisms has
> to be exercised at least once by the walking skeleton — that is what makes the skeleton a proof
> rather than a demo.

**What crossed on disk, and what didn't.** The signed decisions, the contracts, and the planner's
session state are files Phase 3 can open. The three things it most needs to *act on* — the exact
slice to build, the two gates to wire, the numbers to prove — are not.

- **The walking-skeleton definition.** Four slices, portal FNOL to metric event. Nadia carries
  it; on day 8 she verifies the running skeleton against it.
- **The threat mitigation map.** Nine threats, seven mitigated in the design, two handed forward
  as build-time security gates. It becomes `risk-tier-map.md` this phase.
- **The NFR proving plan.** Per quality target, the method and the place its number is read — the
  input to how the metric slice gets built.

**Where the two weeks are headed.** Week one builds the factory: access, the kit, the environment,
the pipeline. Week two proves it, by pushing the thinnest real software all the way through —
including one HIGH-risk slice — and then breaking the rails on purpose to prove they catch. **Two
people to watch:** Wes Carter, Harbor's lead engineer, reviews the harness adaptation — the first
real handoff, months before the close. Tom Reilly, Harbor's platform engineer, joins this phase:
he holds branch-protection admin, the runners, and the secrets, and reviews the pipeline he will
operate after the pod leaves.

> **Carried in from Phase 2, still open on Monday:** Q-17 — postal dispatch vendor and who
> provisions its credentials (Dan + Harbor ops) · Q-18 — the surge load-test dataset from the 2024
> CAT event (Priti + Nadia).

**Our pod:**

- **Maya Chen** — Pod Lead (triages the skeleton into specs, runs the exit demo, owns the Build handoff)
- **Rob Feld** — Setup Owner (the harness as a product; owns branch protection and secrets; never sole approver)
- **Jonah Kim** — Orchestrator / Checker (Setup Owner's deputy; authors spec 0002; reviews every harness change)
- **Sara Whitfield** — Orchestrator / Checker (authors the first slice; Checks and merges spec 0002)
- **Nadia Brooks** — Quality Engineer (wires the gates, verifies the running skeleton against the Phase 2 definition)

**Harbor Mutual:**

- **Karen Voss** — VP Claims Operations (sponsor; watches the exit demo, approves the advance)
- **Wes Carter** — Lead engineer (Setup Owner counterpart; reviews the CLAUDE.md adaptation PRs)
- **Tom Reilly** — Platform engineer (branch-protection admin, runners, secrets; reviews the pipeline)
- **Dan Kowalski** — IT security (signs the data-flow brief; named sign-off on spec 0002; confirms the gates)
- **Luis Ortega** — Product owner (confirms the skeleton is the right thinnest slice; light touch)

**The four walking-skeleton specs:**

| Spec | What it is |
|------|------------|
| 0001 | Queue entry from a portal FNOL |
| 0002 | Replica verification read |
| 0003 | Test-mode acknowledgment |
| 0004 | Metric event |

**The ID codes, decoded.** Every artifact in this engagement carries a stable identifier, so a
decision made in design week can still be traced in month nine. The ones Foundation leans on:

| Prefix | Means | Born in | Example here |
|--------|-------|---------|--------------|
| `ADR-NNN` | An architecture decision record — a signed choice | Phase 2 | ADR-001 replica read · ADR-003 buffered queue |
| `REQ-NNN` | A functional requirement | Phase 1 | REQ-014 same-business-day coverage · REQ-019 fast path |
| `C-NN` / `D-NN` | A constraint, or a product decision | Phase 0/1 | C-04 regulatory clock · D-07 merge · D-09 fast path |
| `Q-NN` | An open question with an owner and a due date | any | Q-15 replica controls · Q-17, Q-18, Q-19 |
| `NFR-NN` | A non-functional requirement — a quality target | Phase 1 | NFR-02 the 10x surge |
| `NNNN` | A build spec — one feature in one file, `specs/NNNN-name.md` | Phase 3 on | 0001–0004, the walking-skeleton slices |

The spec ID is new this phase. From here to close, no code changes without a `specs/NNNN-name.md`
in front of it — the unit the whole Build loop turns on.

**Words this page leans on** (everything else is explained where it first appears):

| Term | What it means |
|------|---------------|
| **The harness** | The project's CLAUDE.md, specs, skills, agents, hooks, and settings — the context and rules every AI agent loads when it starts work in the repo. |
| **The kit** | Our firm's reusable engagement starter: templates, the grader and security-reviewer agents, hooks, pipeline YAML, Bicep starters. Built and improved between engagements in our own standard repo; Phase 3 installs it into Harbor's repo and adapts it. Harbor never pays to build the kit — only to adapt it. |
| **The build loop** | The per-spec cycle — Intent (decide and write what you want), Delegate (an agent builds it inside set bounds), Discern (checks and a non-author prove it). When a spec "rides the loop," this is the ride. |
| **Plan mode** | The agent mode where Claude can read the repo and propose an approach but cannot change files. A human approves the plan before any code is written. |
| **CI** | Continuous integration — the automated checks (build, tests, lint, test coverage) that run on every proposed change before it can merge. |
| **The grader** | A fresh AI agent that did **not** write the code. It reads the spec and the change, and posts a check-by-check verdict on the pull request. It is required to run, but its verdict advises — the human decides. |
| **The Stop hook** | A script that fires when an agent tries to finish. If tests fail or the build is broken, it refuses to let the agent stop. |
| **Branch protection** | Repository settings that make the gates mandatory: no change can merge without CI green, the grader having run, and an approval from someone who didn't write it. |
| **Rails** | All of the above enforcement taken together: CI gates, the grader, branch protection, and the deploy pipeline. Every change runs on them. |
| **Risk tier** | HIGH / MEDIUM / LOW, assigned per spec. Sets how tightly an agent is bounded and how much review a change gets. |
| **Bicep** | Azure's language for infrastructure as code — the cloud environment defined in version-controlled files instead of clicked together by hand. |

## The procedure, step by step

Foundation is the **least plugin-driven phase of the opening**. Most days are code and rails, not
drafts, so most carry no plugin command — the machine goes quiet and the humans build. Below, the
two weeks are braided: what the tool does when it does anything, what the humans do that no
command performs, and the file each day leaves behind. Each step shows a **Tooling** line (the
command, or *none — humans in a room*) and an **Artifacts out** line; `> **At Harbor:**` carries
the worked example, and `> ⚠ **The gap:**` marks the work the plugin never records.

### Day 1 — Mon 3/30 · plugin Step 0 HITL gate — Get the keys, prove they work, and confirm the plan before installing anything

**Tooling —** `/sdlc-next` → Step 0 HITL gate (human decision).
**Artifacts out —** the rails plan and the deputy, confirmed — not yet on disk.

Before the harness touches the repo, the plugin opens a blocking human gate: confirm which single
skeleton slice carries the highest risk, confirm where the dev environment lives and who holds
branch-protection admin, Actions, runner policy, and the secrets vault, and name the Setup Owner's
deputy. Then the access checklist closes and the AI access procured in Phase 0 gets a live smoke
test — does Claude Code actually run on the client's own seats and keys, before anyone depends on
it?

> **At Harbor:** Pod contributor access granted; **Rob** gets branch-protection admin; **Tom**
> enables Actions and agrees Harbor-hosted runners; secrets provisioning starts in Harbor's Key
> Vault. Jonah is named Setup Owner's deputy. The smoke test passes — Claude Code runs on Harbor's
> seats and keys, the Phase 0 fallback rider never needed. Q-17 and Q-18 get their owners and due
> dates re-confirmed.

### Day 2 — Tue 3/31 · plugin Step 1 — Install the rulebook, then rewrite it in the client's own words

**Tooling —** *none — Claude scaffolds from the kit; the adaptation lands as reviewed PRs.*
**Artifacts out —** committed at the repo root, not under `.sdlc/`: `CLAUDE.md`, `specs/`,
`.claude/settings.json`, `.claude/hooks/stop-gate.ps1`, `.claude/agents/grader.md`,
`harness-inventory.md`.

Claude scaffolds the repo from the firm's kit — the CLAUDE.md template, the spec template,
settings, skills, the grader and security-reviewer agents, the Stop hook, the workflow YAML, the
Bicep starters. A working starting point, not a blank page, built and improved between engagements
so the client never pays to build it. Then the real work: adapting CLAUDE.md to the client's own
domain, stack, risk taxonomy, and Definition of Checked — as reviewed PRs the client's lead
engineer reads.

> **At Harbor:** CLAUDE.md rewritten in Harbor's language, reviewed by **Wes**: the domain
> glossary (FNOL, PolicyOne, the snapshot replica, the fast path at 61%, D-07 merge, the C-04
> regulatory clock), the .NET 8 / Angular / SQL Server / Azure standards, the risk tiers, and the
> Definition of Checked. Wes reviewing those PRs *was* the engagement's first real handoff —
> rehearsed months before the close.

### Day 3 — Wed 4/1 · plugin Step 4 — Provision the environment from code, never from clicks

**Tooling —** *none — Claude drafts the Bicep against the kit starters; two humans review every change.*
**Artifacts out —** `infra/` — the Bicep dev environment; the data-flow brief (the standard
requires it; the plugin emits no file).

Claude drafts the dev environment as version-controlled Bicep — rated HIGH risk on purpose, so a
human reads every line. The environment provisions from code, not from a portal, so it can be
rebuilt and reasoned about. Secrets land in the client's vault. A data-flow brief goes to
security: what reaches the API, what doesn't, where the keys live, who can see usage.

> **At Harbor:** Rob and Tom review every Bicep change. It provisions app hosting for the intake
> service and the Angular portal, the buffered ingestion queue (ADR-003) sized for dev, and a
> private, read-only, fully-audited endpoint to the snapshot replica under the Q-15 controls. Key
> Vault references hold the Anthropic key, the Azure credentials, and the replica service account
> — no secret in code, in CLAUDE.md, or in any spec. Dan gets the data-flow brief.

> ⚠ **The gap:** The standard lists a data-flow brief as a Phase 3 artifact — client security has,
> in writing, what goes to the API and where the keys live. The plugin's registry lists no such
> file. Dan gets the briefing; nothing on disk records that he did. Human work, no receipt.

### Day 4 — Thu 4/2 · plugin Steps 2–3 — Build the rails, lock them on, and confirm the Phase 2 gates got wired

**Tooling —** *none — Claude drafts the workflow YAML and the risk-tier map; client DevOps reviews.*
**Artifacts out —** `.github/workflows/{ci,grader,correctness,security,deploy-dev}.yml`;
`risk-tier-map.md`; branch protection (a GitHub setting, not a committed file).

Five workflows get built and reviewed by the client's platform engineer — the CI checks, the
grader, the correctness review, the security review, and the deploy. Then branch protection turns
on: nothing merges without CI green, the grader having run, and a non-author approval; `risk:high`
adds the security workflow and a named sign-off. The risk-tier map gets written from Phase 2's
threat mitigation map — and this is the **confirmation pass** on the threat review: are the two
build-time security gates from Phase 2 actually wired into the risk-tier map and the security
workflow?

> **At Harbor:** Tom reviews the five workflows he will operate after the pod leaves; Rob turns on
> branch protection. The two Phase 2 gates get wired into `security.yml`: the document-upload
> malware scan (HIGH tier) and the acknowledgment-letter PII template-review gate, each registered
> against the path it guards so it fires independent of a spec's risk label.

> ⚠ **The gap:** The threat review is a live method question. The standard runs a design-level
> threat review in **Phase 2**, producing the mitigation map. The plugin mentions threat modeling
> in **only one place** — `phases/03-foundation.md`. The resolution taken here: it is genuinely
> both. Phase 2 is the design-level review; this is the *foundation-level confirmation pass* that
> the two gates it named actually got wired. Two passes, two phases, one map — logged as drift so
> the plugin repo can put the design-level step back where it belongs.

### Day 5 — Fri 4/3 · plugin Step 5a — Real software hits the rails for the first time

**Tooling —** `/sdlc-spec` → `new_spec.py`; then the spec rides the loop — agent, hooks, gates,
human Checker.
**Artifacts out —** `specs/0001-queue-entry.md`; one slice live in dev via `deploy-dev.yml`.

The first skeleton spec rides the full Build loop end to end: authored from the kit template
(Intent), built by a bounded agent in plan mode with the Stop hook refusing to finish on a broken
build (Delegate), then CI and the grader on the PR and a non-author on the merge (Discern), then
the automatic deploy to dev. Whatever is broken in the rails surfaces here, on cheap software,
while it costs an hour.

> **At Harbor:** Spec 0001 (queue entry from a portal FNOL, MEDIUM): Sara authors it, the agent
> codes in plan mode under bounds, the Stop hook refuses on a failing build, the PR fires `ci.yml`
> and `grader.yml`, Jonah (non-author) approves and merges, `deploy-dev.yml` ships to dev. The
> coverage gate miscounts generated files on this very first run — found and fixed for an hour, not
> in Build week three when it would have blocked every PR.

### Day 6 — Mon 4/6 · plugin Step 5b — a hard exit condition — Prove the riskiest path before Build ever depends on it

**Tooling —** *none — the HIGH-risk spec rides the loop; `risk:high` fires security.yml.*
**Artifacts out —** `specs/0002-replica-read.md`; Dan's named security sign-off in the PR.

At least one slice must run the HIGH-risk path — tightest agent permissions, the security workflow
firing, the security-reviewer agent reading the change, a named human sign-off recorded in the PR.
The plugin marks this a hard exit condition: the HIGH path of the loop gets proven on cheap
software, before any real feature relies on it working.

> **At Harbor:** Spec 0002 (replica verification read) touched the regulated integration, so it
> ran HIGH: tight permissions, the `risk:high` label firing `security.yml` and the security-reviewer
> agent, Dan's named sign-off. The Q-15 controls were verified live against dev the same afternoon;
> ADR-001's staleness contract went in as real behavior. Reproduced in full in the exhibit below.

### Day 7 — Tue 4/7 · plugin Step 5c — Finish the skeleton — including the slice that emits the metric

**Tooling —** *none — the specs ride the loop.*
**Artifacts out —** `specs/0003-ack-testmode.md`; `specs/0004-metric-event.md`; the outcome metric
measurable in dev (a property, not a file).

The remaining slices ride the loop. The slice that emits the outcome metric gets special
attention: it makes the engagement's number measurable from day one of Build, not retrofitted at
the end. Any build-time security gate these slices touch fires on its first qualifying PR —
proven, not just configured; if none touch a gate, a throwaway probe PR proves it fires anyway.

> **At Harbor:** Spec 0003 (test-mode acknowledgment, MEDIUM) is the first PR to touch
> acknowledgment templates, so the PII template-review gate fires live — proven, not just wired.
> Spec 0004 (metric event, LOW) emits the FNOL→coverage clock as a structured event; Harbor's
> headline number becomes measurable from Build day one. The document-upload malware gate had no
> qualifying PR yet, so a probe PR proved it fires, then closed unmerged.

### Day 8 — Wed 4/8 · plugin Step 5d — Connect the bones and walk them

**Tooling —** `/e2e` → smoke journey.
**Artifacts out —** `walking-skeleton-spec.md` — per-slice loop evidence; the deployed skeleton,
verified (running software, not a file).

The slices connect into a running skeleton in dev: portal FNOL → queue entry → replica coverage
check → test-mode acknowledgment → metric event. The Quality Engineer verifies it against the
Phase 2 walking-skeleton definition — the one that never became a file. A first automated smoke
journey walks the whole thread, the thinnest proof it holds together end to end.

> **At Harbor:** Nadia walks the four slices against what she carried out of Phase 2's Thursday and
> confirms the architecture is proven in running software, not on paper. The E2E smoke journey
> follows the same path a claimant would. The verification has no artifact of its own — it is
> Nadia's judgment against a definition that only ever lived in her notes.

### Day 9 — Thu 4/9 · plugin Steps 6–7 — Break the rails on purpose — before they break by accident

**Tooling —** *none — a deliberate manual shakedown, then the humans set the cadences.*
**Artifacts out —** `pipeline-proof.md`; `cadence-plan.md`.

A pipeline that is green because nothing real ever stressed it has proven nothing. So each rail
gets forced to fail and watched to catch it: a deliberately failing build, a planted spec
mismatch, a known-bad deploy. Then the cadence plan gets set — the flow check, intent triage,
retro+, and setup review scheduled, and two flow limits agreed. This is human work end to end; the
plugin prompts none of it and checks none of it.

> **At Harbor:** The failing build proves the Stop hook **blocks**; the planted mismatch proves the
> grader **posts**; the bad deploy proves `deploy-dev.yml` **rolls back** to the last good version.
> The setup review (Rob + Jonah) merges the week's harness corrections. WIP cap set at two streams
> per Orchestrator; the review-wait tripwire at a one-working-day median. Q-17 lands (the postal
> vendor); Q-19 surfaces (its sandbox credentials, owner Tom + Harbor ops).

> ⚠ **The gap:** "The rails are proven, not just present" is one of the plugin's exit conditions —
> but `check_gates.py` can only confirm that `pipeline-proof.md` exists and is non-empty. It cannot
> know whether the Stop hook truly blocked or whether a human simply wrote that it did. The most
> important verification of the phase rests entirely on a human's word.

### Day 10 — Fri 4/10 · plugin Steps 8–10 · the gate — Working software in the client's environment, then the gate

**Tooling —** `/sdlc-gate` → `check_gates.py` · `/sdlc-phase-report` → `generate_phase_report.py`
· `/visual-explainer` · `/sdlc-next` → `advance_phase.py --confirmed`.
**Artifacts out —** `build-handoff.md`; `foundation-report.md`; `.sdlc/reports/phase03-report.html`;
the sponsor's signature — billing milestone 4.

The machine returns for the finish. The gate check runs, the phase report renders, the sponsor
watches the walking skeleton run in their own dev environment through the real pipeline with the
outcome metric ticking — working software, not slides — and a named human on each side signs the
advance. `advance_phase.py` will not move the engagement into Build without `--confirmed`.

> **At Harbor:** The gate passes; the report renders. Karen watches a portal FNOL flow end to end
> in Harbor's dev environment with the clock ticking on the scorecard. Rob and Wes walk the
> harness, Tom confirms the pipeline, Dan confirms the gates, Karen approves. `/sdlc-next` advances
> into the Build loop. The four gated phases are done.

> ⚠ **The gap:** The plugin's registry lists eleven exit conditions — branch protection enforced,
> each security gate fired on a real PR, the outcome metric measurable, the rails proven. But
> `check_gates.py` verifies only that four files exist and are placeholder-free, and renders the
> rest as manual REVIEW items it never blocks on. **The human gate is real. Most of what it should
> be signing against, no code puts in front of them.**

## What Phase 3 produced

Foundation's output is a working factory, not a document set — which is why the ledger reads
differently here. Blue rows are files committed to the repo and checked by the gate. **Amber rows
are the phase's real product that no file captures**: running software, a GitHub setting, a
briefing, an event that ticks. Those are the rows to argue about — because the gate's own exit
conditions turn on them, and the gate cannot see them.

State marker key:

- `▪` a command does it — and writes the file
- `▸` a person does it — and it is recorded
- `⚠` a person does it — and nothing records it

| Artifact | What it actually is | Written by | Signed by | Lives at | Feeds |
|----------|---------------------|------------|-----------|----------|-------|
| ▪ `CLAUDE.md` + `.claude/` + `specs/` | The installed, adapted harness — the rulebook, templates, skills, the grader and security-reviewer agents, the Stop hook. The rules every agent loads before it works | Claude scaffolds from the kit; Setup Owner adapts | Setup Owner + deputy | `CLAUDE.md`, `.claude/`, `specs/` | Every Build spec, forever |
| ▪ workflows (×5) | ci, grader, correctness, security, deploy-dev — the rails as code: hard checks, a fresh-agent verdict, defect-hunt, security pass, the deploy | Claude drafts the YAML | Setup Owner + client DevOps | `.github/workflows/` | Every PR in Build |
| ▪ `infra/` (Bicep) | The dev environment as version-controlled code: app hosting, the buffered queue, the private replica endpoint. Provisioned, not clicked | Claude drafts; Setup Owner + platform engineer review every change | Setup Owner | `infra/` | deploy-dev; Phase 8 |
| ▪ `specs/0001–0004.md` | The four walking-skeleton slices, each authored from the kit template and ridden through the full loop | Orchestrators, from the kit spec-template | Pod Lead (triage) | `specs/` | The running skeleton |
| ▪ `risk-tier-map.md` | HIGH/MEDIUM/LOW taxonomy mirroring CLAUDE.md, with the two Phase 2 security gates registered against the paths they guard | Setup Owner, from the Phase 2 mitigation map | Setup Owner + client security | `.sdlc/artifacts/03-foundation/` | The Build loop's tier→ladder rule |
| ▪ `cadence-plan.md` | The Build calendar — flow check, intent triage, retro+, setup review — plus the WIP cap and review-wait tripwire; bans activity metrics | Pod Lead | Pod Lead | `.sdlc/artifacts/03-foundation/` | Every Build week |
| ▪ `pipeline-proof.md` | The forced-failure evidence: each rail broken on purpose and shown to catch it | Setup Owner + deputy | Setup Owner | `.sdlc/artifacts/03-foundation/` | foundation-report.md; the gate |
| ▪ `harness-inventory.md` / `walking-skeleton-spec.md` | The record of what got installed, and the per-slice loop evidence for the skeleton | Setup Owner / QE | Setup Owner | `.sdlc/artifacts/03-foundation/` | Close harness audit; QE verification |
| ▪ `build-handoff.md` / `foundation-report.md` | The ordered spec backlog, risk-tier map, cadences, and open questions — plus the phase's own summary and forced-failure cross-reference | Pod Lead / Setup Owner | Pod Lead | `.sdlc/artifacts/03-foundation/` | The Build loop, directly |
| ▪ `phase03-report.html` | The gate result and artifact inventory, self-contained — what the sponsor reads before signing | `generate_phase_report.py` | — | `.sdlc/reports/` | The manual sign-off gate |
| ⚠ the deployed walking skeleton | The four slices running end-to-end in the client's dev environment, verified against the Phase 2 definition. The phase's whole point — and running software, not a file | **The loop; QE verifies** | Setup Owner + QE | no path — running software, not a file | The Build loop; Phase 8 |
| ⚠ branch protection | The rule that makes the rails mandatory: CI green + grader-ran + non-author approval; `risk:high` adds security + a named sign-off | **Setup Owner, in GitHub** | Setup Owner | no path — a GitHub setting, not a file | Every merge, forever |
| ⚠ data-flow brief | What goes to the API, what doesn't, where the keys live, who sees usage — in security's hands, in writing | **Setup Owner** | Client security | no path — the plugin emits no file | Security sign-off |
| ⚠ the security gates, fired | Proof that each build-time gate actually fired on a real (or probe) PR — not just that it is configured | **The security workflow, on a PR** | Client security | no path — PR history, not a committed file | The gate's "each has fired" check |
| ⚠ the outcome metric, ticking | The FNOL→coverage clock, measurable in dev from the metric slice — the scorecard has real data before feature two | **Spec 0004, running** | QE | no path — a measured property, not a file | The scorecard; Phase 9 |

> ⚠ **The gap:** Five of the things Foundation is judged on have nowhere to live. Four of the
> plugin's eleven exit conditions — the skeleton deployed and verified, the rails proven, each
> security gate fired, the metric measurable — describe running software and GitHub state, and
> `check_gates.py` can confirm none of them. The factory is real; the receipt that it works is a
> human's word. **Human work is not the problem. Human work without a receipt is.**

Deliberately **not** produced in Phase 3: the full feature backlog (Build triage owns it), the
test and production environments (the first hardening pass and Phase 8 add them), and any feature
breadth beyond the thinnest skeleton.

## Install the rulebook, then rewrite it in the client's own words

The factory is three things committed to Harbor's repo: a rulebook rewritten in Harbor's language,
five workflows that enforce the discipline so nobody has to remember it, and a dev environment
defined in code. Each is reviewed by the Harbor engineer who will own it after the pod leaves.

### The adapted CLAUDE.md (the shape)

Scaffolded from the kit, adapted to Harbor in PRs Wes reviewed. The full file is longer; this is
the shape:

- **What this project is** — Harbor's property-claims intake rebuild; the FNOL→coverage median
  target of ≤5 days, and where that number is read from.
- **Domain glossary (Harbor's words)** — FNOL, PolicyOne, the snapshot replica, the fast path (61%
  of claims, D-09), the duplicate-merge rule (D-07), the regulatory clock (C-04: 15 business days
  in two states).
- **Stack standards** — .NET 8 / Angular / SQL Server / Azure / GitHub Actions, immutability
  defaults, Result<T> for expected failures, FluentValidation at the boundary.
- **Risk taxonomy** — HIGH (the replica adapter, `infra/`, `migrations/`, auth, acknowledgment-letter
  templates, public API contracts); MEDIUM (new business logic, integrations); LOW (UI in existing
  patterns, copy, additive CRUD).
- **Gated paths** — `infra/`, the replica adapter, `migrations/`, acknowledgment templates: the
  agent asks before touching these.
- **Definition of Checked** — the spec's acceptance checks pass; the Stop hook is green; the grader
  has run; a non-author approved; HIGH risk carries a named sign-off.

### The pipeline — five workflows

Built and reviewed by Tom; branch protection enforcing them:

| Workflow | Trigger | What it does | Blocks? |
|----------|---------|--------------|---------|
| `ci.yml` | Every PR | Build, test, lint, 80% coverage on new code | Hard block |
| `grader.yml` | Every PR | A fresh agent reads the spec in the diff, posts a check-by-check verdict | Required to run; verdict advisory |
| `correctness.yml` | Every PR | A fresh agent hunts for defects in the diff, posts high-confidence findings | Blocks on a high-confidence defect |
| `security.yml` | `risk:high` label or a gated path | Runs the security-reviewer agent over the diff | Pass + named sign-off required to merge |
| `deploy-dev.yml` | Merge to `main` | Ships to Harbor's dev environment; restores the last good version on a failed deploy | — (deploy step) |

**Branch protection on `main`:** CI green + grader-ran + one non-author approval. `risk:high` adds
`security.yml` passing and a named human sign-off recorded in the PR.

### The Bicep dev environment, and the wired security gates

**`infra/` — provisioned from code:**

- Resource group + app hosting for the intake service and the Angular portal.
- The buffered ingestion queue (ADR-003), sized for dev; the surge load test waits on Q-18 and a
  test environment at hardening pass 1.
- The private endpoint to the snapshot replica under the Q-15 controls — read-only service account,
  no public path, every access audited.
- Key Vault references for the Anthropic key, the Azure credentials, and the replica service
  account. No secret in code, CLAUDE.md, or any spec.

**The two build-time security gates, wired** — the two gates Phase 2's threat review handed
forward, now enforced in `security.yml` and each fired on a real (or probe) PR:

- **Document-upload malware scan — HIGH tier.** Runs on every PR touching the upload path. The
  upload path itself is a Build spec, so a throwaway probe PR proved the gate fires, then closed
  unmerged.
- **Acknowledgment-letter PII template-review — fired live on 0003.** Triggers on the templates
  path itself, independent of the risk label — which is why it fired on spec 0003's MEDIUM PR. PII
  leaves the system on paper, so a human reviews any template change.

> ⚠ **The gap:** The one unrecoverable mistake is a secret in the repo — a key in a commit is a
> rotation event and an audit-log review, not an edit. Harbor's Key Vault held the Anthropic key,
> the Azure credentials, and the replica service-account reference from day one — the data-flow
> brief gave Dan what he needed to sign off without a single secret in a commit.

## The skeleton is the loop's dress rehearsal — nothing gets skipped

Harbor's skeleton was four slices and deliberately nothing more: a portal claim creates a queue
entry → a coverage check reads the replica → a test-mode acknowledgment → a metric event. End to
end, no width. Spec 0002 (replica verification read) was the HIGH-risk one — it touched the
regulated integration and the Q-15 controls, and it ran the loop at HIGH risk on day 6, on cheap
software, before any real feature relied on it. This is one `specs/NNNN-name.md` in full.

**Spec 0002 — Replica verification read**
Risk tier: **HIGH** · Authored: Jonah Kim · Checked: Sara Whitfield · Security sign-off: Dan
Kowalski · Merged 2026-04-06

**Goal.** A coverage-verification service reads the PolicyOne snapshot replica directly (ADR-001)
and returns coverage status with an as-of timestamp, honoring the staleness contract.

**Why.** REQ-014 promises same-business-day coverage status; ADR-001 chose the replica read as the
source. This slice proves the integration and its degradation behavior in running software.

**Scope in.** The replica adapter, the verification service, the staleness contract (as-of
timestamp; >36h escalates; refresh-window 02:00–04:30 degrades to `pending-verification`).
**Scope out.** The fast-path escalation logic (REQ-019, a Build spec); real acknowledgment dispatch
(0003 is test-mode).

**Acceptance checks.** Fresh data → status + as-of timestamp. Policy not found → `needs-review`
with a reason code, never a silent "verified". Refresh window or unreachable → `pending-verification`,
intake never blocked. Snapshot >36h → staleness warning, written-acknowledgment-state claims
escalate.

**Delegation plan.** The agent may touch the replica adapter and the verification service.
**Gated:** the Q-15 service-account configuration and the private-endpoint settings (the agent
proposes; a human applies). Plan-mode approval before any code.

**Checking plan.** Full ladder: CI hard gates, the grader, a non-author Checker (Sara). Because
HIGH: the `security.yml` security-reviewer pass and Dan's named sign-off in the PR.

**How it rode the loop.** Plan approved by Jonah → agent implemented under tight permissions → Stop
hook green → PR fired `ci.yml`, `grader.yml`, and (on the `risk:high` label) `security.yml` → Dan
signed off → Sara merged → `deploy-dev` shipped it. The Q-15 controls were verified live against
the dev environment the same afternoon.

Spec 0002 is the hard exit condition made concrete: at least one HIGH-risk slice runs the full
loop, so the riskiest path is proven before Build ever depends on it. The other three slices —
0001 (MEDIUM), 0003 (MEDIUM, fired the PII gate), 0004 (LOW, emitted the metric) — rode the same
loop; nothing was hand-built off the rails to save a day.

## Break the rails on purpose — before they break by accident

On day 9 the rails got shaken down on purpose — and one defect had already surfaced early, for
cheap, on day 5. A pipeline that is green because nothing real ever stressed it has proven
nothing. A rail that has never failed safely has not been proven.

**The shakedown — recorded in `pipeline-proof.md`** — each rail forced to fail and proven to catch
it:

- A deliberately failing build proves the Stop hook **blocks**.
- A PR with a planted spec mismatch proves the grader **posts** the miss.
- A known-bad deploy proves `deploy-dev` **rolls back** cleanly — the environment returns itself to
  the last good version.

The setup review (Rob + Jonah, his deputy) merged the week's harness corrections — the coverage-gate
fix, two CLAUDE.md glossary additions the agents kept missing. The Build cadences got scheduled,
and two flow limits set: WIP cap at two streams per Orchestrator, and no new streams once the
median review wait passes one working day.

> **The rail that broke first, day five:** the coverage gate miscounted generated files on the
> very first real slice — found and fixed while it cost an hour, not in Build week three when it
> would have blocked every PR.

**Q-17 lands:** Dan and Harbor ops choose the postal dispatch vendor; it surfaces **Q-19** (vendor
sandbox credentials), owner Tom + Harbor ops, due before the first acknowledgment-delivery spec in
Build.

> ⚠ **The gap:** `pipeline-proof.md` records that each rail caught its planted failure. But the
> gate only checks the file exists and is placeholder-free — not that the shakedown truly happened.
> The proof is a human's word, written down.

## What the Build loop receives

A phase ends by handing the next one a package, not a feeling. Everything below crosses the
boundary out of the gated opening and into the continuous Build loop: the factory, the proof it
runs, the ordered backlog, and the questions still open — carried forward under their original IDs,
never silently dropped.

**Crosses into the Build loop:** `build-handoff.md`, `risk-tier-map.md`, `cadence-plan.md`,
`foundation-report.md`, `CLAUDE.md` + `.claude/` + `specs/`, the deployed skeleton running in dev,
the outcome metric ticking.

### The Build handoff (summary)

Drafted day 10; the phase closed day 10 — billing milestone 4.

- **The factory:** the adapted harness, the five-workflow pipeline, branch protection, and the
  Bicep dev environment — all owned by Rob, reviewed by Jonah and Tom.
- **The proof:** the walking skeleton running in Harbor's dev environment, verified against the
  Phase 2 definition, with the FNOL→coverage clock ticking on the scorecard.
- **The risk-tier map:** the HIGH/MEDIUM/LOW taxonomy in CLAUDE.md, plus the two build-time
  security gates registered against the paths they guard.
- **The cadences:** flow check (daily), intent triage (weekly), retro+, setup review; WIP cap two
  streams per Orchestrator; halt new streams past a one-working-day median review wait.

### Recommended first Build specs

The skeleton proved the architecture; these are the first features to ride the proven loop.

- **Fast-path escalation (REQ-019)** — builds directly on spec 0002's replica read.
- **The document-upload path** — the first PR to trigger the malware-scan gate for real.
- **Email FNOL extraction (ADR-004)** — the engagement's first agentic spec, where the feature
  itself runs on an AI model. That activates the AI-engineering module: a 200-email golden set (real
  example inputs with known correct answers) as acceptance criteria, the eval gate in CI (every
  change is scored against that set), and prompt and model changes tiered HIGH.

### Open questions into Build

| ID | Open question | Owner | Due |
|----|---------------|-------|-----|
| Q-18 | Construction of the surge load-test dataset from the 2024 CAT (catastrophe) event — volume curve + channel mix | Priti Shah + Nadia Brooks | Before hardening pass 1 |
| Q-19 | Postal vendor sandbox credentials for the acknowledgment-delivery spec (follows Q-17's vendor choice) | Tom Reilly + Harbor ops | Before the first acknowledgment-delivery spec |

The engagement crosses here from the gated opening into the continuous Build loop. There is no
next gate — only the merge bar every change clears, and the cadences that keep it honest.

---

## The tooling behind this phase

The abstract Phase 3 page describes this work generically. What actually ran — and how little of
it was the plugin, which is itself the point:

| What got produced | How |
|---|---|
| Repo scaffold + CLAUDE.md adaptation | Claude scaffolds from the delivery-standard kit; adapted in PRs Wes reviewed; no plugin command — Foundation is hands-on |
| Bicep dev environment | Claude drafts; HIGH risk, Rob + Tom review every change; secrets in Harbor's Key Vault |
| Pipeline (ci/grader/correctness/security/deploy-dev) | Claude drafts the YAML against the kit workflow starters; Tom reviews; Rob enables branch protection |
| Walking-skeleton specs (0001–0004) | Orchestrators author from the kit spec-template; each rides the full loop — plan mode, Stop hook, `ci.yml` + `grader.yml`, a non-author Checker, `deploy-dev.yml` |
| The HIGH-risk path (0002) | `risk:high` label → `security.yml` → the security-reviewer agent; Dan's named sign-off in the PR |
| Skeleton smoke journey | `/e2e` → a Playwright journey across the FNOL→metric path |
| Rails shakedown + setup review | Manual — prove the Stop hook blocks, the grader posts, deploy-dev rolls back; Rob + Jonah (deputy) merge harness corrections |
| Gate, packet, demo, advance | `/sdlc-gate`, `/sdlc-phase-report`, `/visual-explainer` (demo narrative), `/sdlc-next` (after the gate sign-off) |

---

Next: [the Build loop worked example](build-loop-example.md) — one ordinary week of Build: two
specs end to end, and the grader catching a bug that eleven green tests missed.
