# The Build Loop Worked Example: Harbor Mutual

The continuation of [the Phase 3 example](phase-3-example.md), companion to
[the Build loop deep-dive](build-loop.md). This page is the worked **Example** track for the loop —
one ready spec followed all the way round. Unlike a gated phase, the loop does not swallow a folder of
handoff files once and transform it; it takes in one thing, over and over: a single ready spec.

## What the loop receives

Harbor Mutual — a fictional regional insurer — hired a five-person pod to rebuild how
property-insurance claims get reported and decided. A claim takes a median of **11.4 days** from FNOL
(first notice of loss) to a coverage decision; the target is **5 days or less**. Foundation closed
Friday 2026-04-10 with the walking skeleton live in Harbor's dev environment and the rails proven;
Build began the following Monday. Unlike a gated phase, the loop does not swallow a folder of handoff
files once and transform it. **It takes in one thing, over and over: a single ready spec.**

**Received once, at Build's start** — the factory Foundation built, then left running:

- `CLAUDE.md` — the adapted rulebook
- `.claude/` — Stop hook, settings, skills, grader agent
- the five rails — `ci` · `grader` · `correctness` · `security` · `deploy-dev`
- `risk-tier-map.md`
- `build-handoff.md` — the ordered spec backlog

**Received again on every trip round the loop** — the real, repeating input:

- `specs/NNNN-name.md` — one ready spec

### Why the input is a spec, not a handoff

A gated phase eats the previous phase's whole output, transforms it, and hands the next phase a bundle
at a gate. The Build loop has no such shape. The factory built in Phase 3 — the rulebook, the Stop
hook, the grader, the five rails — sits still and runs. What moves is one spec at a time: a story that
cleared the **Definition of Ready** at triage, written to `specs/NNNN-name.md`, durable across
sessions.

The spec outlives the chat that produced it. The agent re-reads it every session; the grader grades
against it; when behavior changes later, the spec changes in the same PR. Everything this page shows
happens to one spec — then repeats.

### The week this page watches

This is **week four of Build** (Mon 2026-05-04 to Fri 2026-05-08), picked because it is deliberately
ordinary. Ten specs merged in the first three weeks; nothing on this week's board is special. Two
stories clear triage into ready specs — **0015** (fast-path queue, MEDIUM) and **0016**
(duplicate-claim merge, HIGH) — and a third bounces for vagueness. We follow **0016**, the HIGH one,
all the way round, because it exercises every beat and every rail.

> **The spec that rides the loop this week.** 0016 — duplicate-claim merge (D-07) · Risk: HIGH. The
> same loss reported twice becomes one claim — never a rejection, never two claims adjusted in
> parallel.

### The cast

**Our pod**

- **Maya Chen** — Pod Lead; owns the risk tiers and the cadences
- **Rob Feld** — Setup Owner; owns the harness, runs setup review
- **Jonah Kim** — Orchestrator / Checker; Rob's deputy
- **Sara Whitfield** — Orchestrator / Checker; delegates and checks 0016
- **Nadia Brooks** — Quality Engineer; runs the hardening passes

**Harbor Mutual**

- **Luis Ortega** — product owner; answers silent decisions on a 2-day clock
- **Wes Carter** — lead engineer; the named HIGH-risk sign-off
- **Dan Kowalski** — IT security; owns the security queue
- **Dee Alvarez** — intake supervisor; the source of check 3's realism
- **Gail Tran, Marcus Webb** — senior adjusters; drive the demo
- **Priti Shah** — data lead; owns the surge load-test dataset (Q-18)
- **Karen Voss** — VP Claims Ops; sponsor, sees outcomes at steering

### The ID codes, decoded

Every object in this engagement carries a stable identifier, so a decision made in week two can still
be traced in month nine. On this page you'll see:

| Prefix | Means | Born in | Example here |
| --- | --- | --- | --- |
| `NNNN` | A spec — one change, one branch, one PR | Build (triage) | 0015 fast-path queue · 0016 duplicate merge |
| `D-NN` | A logged product decision the PO owns | Phase 0/1 | D-07 merge rule · D-09 the fast path (61% simple) |
| `C-NN` | A constraint — a hard limit the build honors | Phase 0 | C-04 the 15-business-day regulatory clock |
| `REQ-NNN` / `NFR-NN` | A functional / non-functional requirement | Phase 1 | NFR-07 audit-logged claim actions |
| `ADR-NNN` | An architecture decision record — a signed choice | Phase 2 | ADR-001 the replica-staleness contract |
| `Q-NN` | An open question with an owner and a due date | any | Q-18 the surge load-test dataset, carried into Build |
| `risk:high` | A PR label — not an ID, but it fires the security rail and forces a named sign-off | Build | 0016 wears it |

Unlike the numbered phases, the loop mints only one new ID kind of its own — the spec `NNNN`.
Everything else it inherits and honors: a Build spec traces back to a D-, a C-, a REQ-, or an ADR-
from an earlier phase, or it is scope that crept in.

## The loop, beat by beat

This is not a calendar of days — it is the same three beats every change runs: **Intent** (decide and
write), **Delegate** (bound and build), **Discern** (prove, then merge). Each beat is braided four
ways: what the human does, what the agent does, what the harness enforces, and what lands on disk.
Follow spec 0016 — the HIGH-risk one — through all three.

### Beat 1 — Intent: decide, tier, and write

Nothing enters the loop as a conversation. A story becomes buildable only by clearing the **Definition
of Ready** at weekly intent triage. **The human** checks that every acceptance criterion passes the
vague-line test ("could two people build different things from this line?"), states scope in *and*
scope out, surfaces every silent product decision onto the decision list with an owner and an answer
clock, and — the Pod Lead's call, never the agent's — assigns a risk tier. **The agent** drafts
candidate specs from the kit template in-session and proposes a tier for a human to confirm. **The
harness** runs `check_spec.py`: the mechanical floor (required sections, a valid tier, scope both
ways, no placeholders) plus a vague-line lint, and it checks that the Checking Plan's ladder depth
equals the risk tier. A spec it reports NOT READY does not enter the loop.

**Tooling —** `/sdlc-spec` → `new_spec.py` allocates the next NNNN · `check_spec.py` → the Definition
of Ready · the risk tier is a human call.

**Artifacts out —** `specs/0016-duplicate-claim-merge.md` · `.sdlc/metrics/spec-log.jsonl` (+1 line,
the DoR result).

> **At Harbor — three stories, three fates.** The Monday flow check opens with the queue number, not a
> status round-robin: four changes waiting, oldest 1.2 days, spec 0012 (document upload, HIGH) sitting
> in the security queue, which is read on its own line because it clears slower. Then triage.
> *"Show adjusters similar past claims"* fails the vague-line test — nobody can write a check for
> "similar," so it bounces back to Luis and the agents never see it. *The fast-path work queue* (Gail
> and Marcus's demo feedback; D-09's simple 61%) sharpens into **spec 0015**, MEDIUM. *Duplicate-claim
> merge* (D-07) becomes **spec 0016**; Maya tiers it **HIGH** — a wrong merge mangles two
> policyholders' data. Triage surfaces the silent decision — *what does the second reporter see?* — and
> routes it to Luis on his 2-day clock rather than letting the agent quietly decide it.

### Beat 2 — Delegate: draw the box, approve the plan

Delegating is not "go build it." **The human** (the Orchestrator) makes the agent start in **plan
mode** — it proposes which files it will touch and how it meets each check before writing a line — then
corrects or approves, hunting the one decision the plan glosses. They draw three bounds: **Scope** (the
file patterns it may touch), **Context** (the one existing pattern to reuse, named), **Permissions**
(what it may run without asking). Freedom scales with risk: a loose leash on what's cheap to undo, a
tight one on what's expensive to get wrong. **The agent** builds from the approved plan, writing the
failing test first when TDD applies. **The harness** enforces the box: the **blocking Stop hook**
refuses to let the agent finish with red tests or a broken build — "the tests must pass" becomes a fact
about the world, not a request it can rationalize past.

**Tooling —** none — the loop runs on the rails, not commands: plan mode, then the blocking Stop hook ·
the approved plan is a human call in the session.

**Artifacts out —** a branch + draft PR (the code and its tests) · the approved plan, corrected in the
session and held in the PR — not a standalone file.

> **The gap — the one thing here that leaves no receipt.** Plan approval is the highest-leverage moment
> in the loop — it is where the dangerous decision nobody noticed being made gets noticed and
> corrected. Yet the approved plan is not written to a durable artifact of its own; it lives in the PR
> thread and the session. The spec and the grader's verdict get files; the plan correction that
> prevented the bug does not.

> **At Harbor.** Sara finalizes 0016. The check that matters most is written from Dee Alvarez's intake
> reality — phone reporters often don't have their policy number. She delegates with **two leashes**:
> tight on the matching keys and merge write path ("follow the plan exactly; deviate only by asking"),
> loose on the audit-log formatting ("your call"). In plan mode she pushes on the one thing the plan
> glosses — *what exactly is the match key when the policy number is absent?* — the agent's answer is
> vague, which is a tell, and the plan gets the explicit route-to-manual-review path before she
> approves it. Both of the week's specs get one agent each: they write into shared code, so fanning out
> would only clobber files. (0015 took about forty minutes of human time before a line was written.)
> Spread out to explore; line up to commit.

### Beat 3 — Discern: prove it, then merge

A change is done when it has been proven against its spec by something other than its author. The
proving climbs a **five-rung checking ladder**, and in the rails it lands as three layers on the PR.
**The harness** runs the mechanical gates in CI (build, tests, lint, 80% coverage — a hard block) and
the **grader** — a fresh agent, told plainly it did not write the code, that walks the acceptance
checks and posts a check-by-check verdict as a PR comment. It is required to run but only advises.
**The human** Checker reads that verdict and makes the call — a non-author approval on every PR,
because **the author never approves their own work**. A `risk:high` change adds the security rail and a
named human sign-off. Merge deploys to dev automatically. **What lands on disk:** the grader's finding
gets memory and a disposition in `findings-log.jsonl`; the merge gets a `spec_merged` line in
`loop-events.jsonl`.

**Tooling —** `record_findings.py` → `findings-log.jsonl` · `scorecard.py record` → `loop-events.jsonl`
· the Checker's judgment is a human call at the merge bar.

**Artifacts out —** the grader's verdict (a PR comment) · `.sdlc/metrics/findings-log.jsonl` (+1 line)
· `.sdlc/metrics/loop-events.jsonl` (+1 line, `spec_merged`) · the non-author approval + named sign-off
(required, no engagement file).

> **The gap — green tests are not done.** The agent finishes 0016 with **eleven green tests** and a
> clean build; the Stop hook lets it stop; CI goes green. On an unchecked team, this is where it ships.
> The grader fails it on **check 3**: the code normalizes a missing policy number to an empty string
> *before* the matcher runs, so every no-policy phone claim in a 7-day window shares one bucket — two
> unrelated storm-week reporters would be merged into one claim. The eleven tests only cover claims
> that *have* a policy number. Rung 4 is where the bug the author's own suite hid goes to die — and it
> only works because Intent wrote a checkable criterion for it to grade against.

> **At Harbor — the fix, and the merge bar cleared.** The fix routes no-policy claims to manual review
> before the matcher and adds a test for that path; re-graded clean. The security-reviewer agent passes
> the data-handling. **Wes signs off by name** — the HIGH-risk requirement — and **Jonah, not Sara,**
> checks and merges; deploy-dev ships it. The bug existed for roughly four hours, all of them on a
> branch. At the setup review, last week's Retro+ item lands: a UTC-timestamp escaped bug (C-04's
> regulatory clock) was answered with "which check should have caught it?", so the test-writer skill
> now drafts timezone-boundary cases into every suite that touches a business-read date.

## What one trip round the loop produces

A gated phase's ledger is the pile of artifacts it produces once. The loop's ledger is smaller and it
repeats: this is what a *single* spec's journey leaves on disk. Blue rows are written by a command or
the rails, at a real path. **Amber rows are the merge bar's human judgments** — required on every
change, recorded only in the PR's own state, with no file in the engagement's record.

State marker key:

- `▪` a command does it — and writes the file
- `▸` a person does it — and it is recorded
- `⚠` a person does it — and nothing records it

| Artifact | What it actually is | Written by | Signed by | Lives at | Feeds |
| --- | --- | --- | --- | --- | --- |
| ▪ `specs/0016-….md` | The change itself, as intent: goal, scope in/out, five testable checks, risk tier, delegation plan, checking plan. Durable across sessions — the agent's brief and the grader's rubric | `/sdlc-spec` scaffolds; the Orchestrator writes | Orchestrator (Sara) | `specs/` | The agent every session; the grader |
| ▪ the merged change | The code on the main branch, deployed to Harbor's dev environment through the real pipeline | `deploy-dev.yml` on merge | — | main branch + Harbor dev env | The running product; the outcome clock |
| ▪ the grader verdict | A check-by-check pass/fail against the spec, pinned to the changed lines. The verdict that caught check 3 | `grader.yml` — a fresh agent | — | the PR (durable copy → findings-log) | The human Checker's call |
| ▪ `spec-log.jsonl` | One appended line: this spec's Definition-of-Ready result at Intent — tier, author, checker | `check_spec.py` | — | `.sdlc/metrics/spec-log.jsonl` | Harness calibration (never client-facing) |
| ▪ `findings-log.jsonl` | One appended line per grader finding, with its severity and disposition — giving the verdict memory across re-grades | `record_findings.py` | — | `.sdlc/metrics/findings-log.jsonl` | Open-HIGH-debt count at the merge bar |
| ▪ `loop-events.jsonl` | One appended `spec_merged` event — the raw material the biweekly scorecard is computed from | `scorecard.py record` | — | `.sdlc/metrics/loop-events.jsonl` | The steering scorecard trend |
| ⚠ the non-author approval | The core merge-bar rule: a human who did not write the code approved it. The author never approves their own work | A human Checker (Jonah) | Checker | no path — nothing writes it | The merge |
| ⚠ the named HIGH-risk sign-off | The risk:high requirement: a named human accepted the risk of merging this change | A named human (Wes Carter) | Wes Carter | no path — nothing writes it | The merge, HIGH tier |

**Only two amber rows — and that is the point.** Compare this with the design phase, where six of
fourteen outputs had nowhere to live. The Build loop is the best-instrumented stretch of the
engagement: the spec, the verdict, and three metrics lines all land at real paths, automatically. The
only human work without a file is the pair of merge-bar judgments — the non-author approval and the
named sign-off — and even those live in the PR's own approval state. **Human work is not the problem;
human work without a receipt is — and here there is almost none.**

Deliberately **not** produced on a trip round the loop: a batch design document, a separate test plan,
a "specification document" duplicating the spec library, and — above all — any exit-gate artifact
bundle. There is no batch to gate, because the checking already happened, per change, inside the loop.

## Spec 0016, as merged

This is the whole of what the loop received for this trip: the thing the agent read, the Orchestrator
bounded, and the grader graded against, line by line. Everything in Beat 3 traces back to a numbered
check below — check 3 is the one the green tests hid and the grader caught.

```markdown
# 0016 — Duplicate-claim detection and merge

## Goal
The same loss reported twice becomes one claim — never a rejection, never two
claims adjusted in parallel (D-07).

## Why
Storm weeks produce duplicate reports across channels (portal, phone, email).
Today they become separate claims and get reconciled by hand at adjudication —
or not at all.

## Scope
- In: candidate matching at intake, the merge write path, the merge audit log,
  the second reporter's confirmation experience (per Luis's decision 5/6).
- Out: cross-policy fraud detection, retroactive merging of pre-Build claims,
  adjuster-initiated manual merges. Not now.

## Acceptance checks (each one is testable)
1. A second FNOL for the same policy number with a loss date inside a 7-day
   window of an open claim joins that claim; the event log records both
   reports with their channels and timestamps.
2. The second reporter receives "your report has been added to an existing
   claim for this loss" — a confirmation, never a rejection (D-07).
3. Matching is keyed per policy number plus the 7-day loss window,
   independently — one policy's candidate matches never affect another's. A
   claim arriving without a policy number is never auto-merged; it routes to
   the manual-review queue.
4. A merge is recorded in the append-only event log with both source reports;
   the merged claim's audit trail reconstructs who reported what, when, from
   which channel (NFR-07).
5. Merging never deletes a report. Un-merge (splitting a wrong merge) is out
   of scope for v1, which is exactly why auto-merge must be conservative:
   when in doubt, manual review.

## Risk: HIGH
Merging claim records is hard to undo and touches policyholder data. Full
ladder: tight permissions, security-reviewer pass, named human sign-off (Wes).

## Delegation plan
May touch: the intake matching service, the merge write path, their tests.
Gated: the claim schema (any migration is its own spec), the event log
contract. Reuse the existing event-log writer — do not invent a second one.

## Checking plan
All five rungs. Grader against every check; security-reviewer on the data
path; Wes's named sign-off before merge.
```

One file, seven headings, five checks — and it is simultaneously the agent's brief, the grader's
rubric, the Checker's yardstick, and the durable record after the chat is gone. A stale spec is a lie
to the next reader, so it changes in the same PR as the behavior.

## The grader's verdict, in full

On 0016's first build the agent finished with eleven green tests and a clean build. The grader — a
fresh agent, told plainly it did not write the code — walked the five checks and failed it on check 3.
The full PR comment, posted by the rails (`grader.yml`), verbatim:

```
VERDICT: FAIL

Check 1 (same policy + 7-day window joins the claim): MET — covered by
  tests/merge.candidate.test (4 cases, including window boundaries).
Check 2 (second reporter sees confirmation, never rejection): MET.
Check 3 (per-policy independence; no-policy-number claims never auto-merge):
  NOT MET. intake/matching.service normalizes a missing policy number to ""
  before keying candidate matches. Every claim without a policy number
  therefore shares one match bucket: two unrelated phone reporters with loss
  dates in the same 7-day window WILL be auto-merged into one claim. The
  test suite only exercises claims that have a policy number, so all 11
  tests pass with this bug live.
  Fix: route claims with no policy number to the manual-review queue before
  the matcher runs (the spec's stated path), and add a no-policy-number test.
Check 4 (append-only audit of merges): MET.
Check 5 (no deletion; conservative auto-merge): AT RISK via check 3 — the
  empty-string bucket makes auto-merge aggressive for exactly the claims the
  spec says to treat conservatively.

The tests prove what they test. They do not test the spec's claim of
per-policy independence for the no-policy path.
```

The trail after the fix, recorded in the PR: re-grade PASS (all five checks, including the new
no-policy-path test) · security-reviewer agent pass on the data path · **signed off: Wes Carter**
(named HIGH-risk sign-off) · checked and merged by Jonah Kim (non-author) · deploy-dev green.
`record_findings.py` appended the finding and its FIXED disposition to `findings-log.jsonl`, so the
catch survives past this PR. The bug existed for roughly four hours, all of them on a branch.

**Green tests are not done.** Eleven passing tests, a green build, a satisfied Stop hook — and a live
data-mangling bug. The author's tests prove what the author thought to test. That is why the author is
never the only approver, human or agent, and why the grader reads the spec rather than the test suite.

## The tier sets the climb, not the mood

The same triage produced a bounce, a MEDIUM, and a HIGH — and each fate was decided mechanically.
Neither ready spec was over- or under-checked; the tier on the spec set the climb, and the vague-line
test decided whether a story became a spec at all.

**The one that bounced.** *"Show adjusters similar past claims"* never reached an agent. Nobody can
write an acceptance check for "similar," so nobody can build it. It went back to Luis for sharpening;
the agents never saw it. A bounce at triage costs a conversation; the same vagueness found at the PR
costs a redo.

**The two that cleared, at different depths.**

> **Spec 0015** — fast-path queue — **MEDIUM.** New business logic, nothing hard to undo. The climb:
> grader plus one non-author Checker, cleared in a day. Jonah authored it, Sara checked it, deploy-dev
> shipped it. Accepted as-is.

> **Spec 0016** — duplicate-claim merge — **HIGH.** Merging claim records is hard to undo and touches
> policyholder data. The full ladder: tight permissions, the security-reviewer pass, and Wes's named
> sign-off.

**Why both specs got one agent, not many.** Each of the week's specs wrote into shared code — the
work-queue service, the intake matching service — so each got exactly one agent, start to finish.
Nothing here was independent enough to fan out; parallel agents in the same files clobber each other.
Fanning out would have been faster to start and slower to finish, once the conflicts surfaced. Spread
out to explore; line up to commit.

## One change, and the client sees outcomes — never activity

The loop's numbers are baseline-and-trend, no vanity targets. What the pod's internal dashboard showed
Friday:

| Number | This week | Read as |
| --- | --- | --- |
| Accepted-as-is | 11 of 14 specs (79%) | Trust rising — intent and bounds are working |
| Review wait (median) | 0.9 days | Under the one-working-day tripwire; no stop triggered |
| Security-review wait (median) | 2.1 days | Drifting up — flagged at Retro+, Maya owns it with Dan |
| Bounce-backs at triage | 1 ("similar claims") | The cheap place caught it |
| Escaped bugs | 0 (1 last week: the UTC clock) | Last week's answered with a harness change, merged Thursday |
| WIP | 5 of 6 cap | Headroom held all week |

Every number here is computed from `loop-events.jsonl` by `scorecard.py`, which **refuses** to record
velocity, story points, PR count, or lines of code, and reads "no data" rather than a fabricated zero.
What steering saw instead: the live demo, the outcome clock (instrumented, moves at rollout), the
stability and accepted-as-is trends, and the decision list. Gail drove the demo herself — the fast-path
queue and the duplicate-merge flow, live in Harbor's dev environment — and Karen was told plainly that
the production needle moves at rollout, not before. What steering never sees: PR counts, lines of code,
story points, "AI productivity." Q-18 (Priti and Nadia's surge load-test dataset, built from the 2024
CAT event) lands this week; hardening pass 1 is scheduled against it.

## The tooling behind the week

Build is the least plugin-driven stretch of the engagement — most days carry no slash command at all.
What actually ran, on the **claude-code-sdlc** plugin, the kit's rails, and the paired skills:

| What got produced | How |
| --- | --- |
| Flow-check queue numbers | `/sdlc-status` at the daily flow check; the security queue read on its own line |
| Ready specs (0015, 0016) | Triage is humans; `/sdlc-spec` scaffolds from the kit template (`new_spec.py` allocates NNNN); the Pod Lead tiers them |
| Definition-of-Ready check per spec | `check_spec.py` — mechanical floor + vague-line lint; appends the result to `.sdlc/metrics/spec-log.jsonl` |
| Spec 0015 (MEDIUM), end to end | Rides the loop: plan mode under bounds, Stop hook, `ci.yml` + `grader.yml` on the PR, non-author Checker, `deploy-dev.yml` on merge |
| Spec 0016 (HIGH), end to end | Same loop plus the HIGH path: `risk:high` label → `security.yml` → the security-reviewer agent; Wes's named sign-off in the PR |
| The 0016 catch, given memory | `grader.yml` posts the check-by-check verdict as a PR comment; `record_findings.py` appends it (with disposition) to `.sdlc/metrics/findings-log.jsonl` |
| The merge event + scorecard | `scorecard.py record` logs `spec_merged` to `.sdlc/metrics/loop-events.jsonl`; the biweekly scorecard is computed from it |
| Harness improvement (timezone checks) | Last week's Retro+ answer; the test-writer skill updated by reviewed PR, merged at the setup review (Rob + Jonah) |
| Steering demo narrative + scorecard visuals | `/visual-explainer`; Gail drives the live demo herself |
| Weekly five-bullet client summary | Claude drafts from the week's merged specs; Maya corrects and sends |

Those three `.sdlc/metrics/*.jsonl` receipts are real files this loop writes on every trip — and the
narrative docs never name them. All names, numbers, and IDs are invented but internally consistent:
the 11.4-day baseline, the spec sequence, and the D-/Q-/C-/ADR- IDs trace back through every earlier
phase example.

## The merge bar

The other phases on this site end at a gate: a batch of artifacts, checked once, a human sign-off,
advance. **The Build loop has no gate.** It has a merge bar — the same short list every single change
clears to land — and it is left not when a checker passes but when a **human declares the backlog
feature-complete**.

**The bar every change clears:**

- CI green — build, tests, lint, 80% coverage on new code
- The grader has run — required to run, its verdict advisory
- Correctness passed, or a named-human override recorded
- A non-author approval — **the author never approves their own work**, no exceptions; this rule
  survives every collapse of pod size

A `risk:high` change adds two more: the security workflow passes, and a named human signs off in the
PR. That is the whole of it — there is nothing further to clear at the end of a loop pass, because
every pass already cleared this.

**How the loop is left.** The loop ends when a human declares the backlog feature-complete — every
story the engagement committed to has ridden the loop and merged. That declaration is the only thing
that produces the loop's one required output:

- `phase7-handoff.md` — the single required output, produced by a declaration, not a gate.

`phase7-handoff.md` names what was built, the state of the system in dev, the open questions carried
under their original IDs, the deferred items with rationale, and what Documentation must cover. It is
the entry package for Phase 7 — not a gate receipt.

**How the plugin models this — and why it reads wrong.** The plugin's `phase-registry.yaml` lists
`build` as a phase (order 4) with `exit_gate.approval: manual` and
`artifacts.required: [phase7-handoff.md]` — the same shape it gives a genuinely gated phase. Taken at
face value, that frames the Build loop as ending at an artifact exit gate, which the standard is firm
it does not. Read it accurately: the loop's *only* required output is `phase7-handoff.md`, and it is
produced when a human declares feature-complete, not by a gate run. The gate script itself agrees — for
this phase `check_gates.py` reports the spec backlog as information and states plainly that *"Build is
feature-complete by human declaration, not by this count,"* verifying only that `phase7-handoff.md`
exists and is complete. The registry's framing is the thing to fix, not the loop's behavior.

Why no gate at all? Because a gate batches checking — write everything, then review everything — and
batched checking is the exact failure mode this loop exists to kill. When an agent can produce code in
minutes, the constraint is never building; it is proving. So the proving moves to per-change, inside
the loop, on the bar above — and the moment the pod starts skipping the loop for a "small" change is
the moment unchecked work creeps back in.

---

Next: [the Phase 7 worked example](phase-7-example.md) — Build closes feature-complete at spec 0044,
and the documentation week proves Harbor can run the system without us: a cold checkout that fails on
step 4 (on purpose), a 3 a.m. runbook, and two unwritten ADRs collected.
