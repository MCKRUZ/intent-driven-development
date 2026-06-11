# The Build Loop Worked Example: Harbor Mutual

The continuation of [the Phase 3 example](phase-3-example.md), companion to
[the Build loop deep-dive](build-loop.md). The Foundation gate closed Friday 2026-04-10 with
the walking skeleton live in Harbor's dev environment and the rails proven. Build began the
following Monday.

This page is **week four of Build** (Mon 2026-05-04 to Fri 2026-05-08) — picked because it is
deliberately ordinary. Ten specs have merged in the first three weeks; nothing on this week's
board is special. What the week shows is the loop itself: one MEDIUM spec riding through
clean, one HIGH spec where the grader catches a bug the author's green tests missed, one story
bounced at triage for vagueness, and the cadences and numbers that steer all of it.

**The story so far (you can start here):**

|                  |                                                                                                                                                                                                                       |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The client**   | Harbor Mutual — a fictional regional insurer. They hired a five-person consulting pod to rebuild how property-insurance claims get reported and decided.                                                              |
| **The problem**  | A claim takes a median of **11.4 days** from FNOL (first notice of loss — the policyholder reporting the damage) to a coverage decision.                                                                              |
| **The target**   | Median **5 days or less**.                                                                                                                                                                                            |
| **Where we are** | Phases 0-3 fixed the problem, signed the requirements, chose the architecture, and built the factory. The walking skeleton runs in Harbor's dev environment. Build is the continuous loop that now grows it into the product, spec by spec. |
| **The rails**    | Every change rides the same enforcement, installed in Phase 3: CI hard gates, the grader, branch protection, and automatic deploy to dev on merge.                                                                    |
| **Our pod**      | Maya Chen (Pod Lead) · Rob Feld (Setup Owner) · Jonah Kim (Orchestrator, Rob's deputy) · Sara Whitfield (Orchestrator/Checker) · Nadia Brooks (Quality Engineer).                                                     |
| **Harbor's cast**| Luis Ortega (product owner, on the 2-business-day decision clock) · Wes Carter (lead engineer) · Dan Kowalski (IT security) · Dee Alvarez (intake supervisor) · Gail Tran and Marcus Webb (senior adjusters) · Karen Voss (VP Claims Ops, sponsor) · Priti Shah (data lead). |

**The IDs you'll see on this page:**

| ID          | What it is                                                                                                       |
| ----------- | ------------------------------------------------------------------------------------------------------------------ |
| **NNNN**    | A spec — one feature in one file, `specs/NNNN-name.md`. The walking skeleton was 0001-0004; Build continues the sequence. |
| **D-NN**    | A product decision, made by a named human and logged.                                                            |
| **C-NN**    | A constraint from Phase 0.                                                                                       |
| **REQ-NN**  | A requirement from the Phase 1 baseline.                                                                         |
| **Q-NN**    | An open question with a named owner and a due date.                                                              |

**Words this page leans on** (every other term is explained where it first appears):

| Term                     | What it means                                                                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Plan mode**            | The agent mode where Claude can read the repo and propose an approach but cannot change files. A human approves the plan before any code is written.                  |
| **The Stop hook**        | A script that fires when an agent tries to finish; if tests fail or the build is broken it refuses to let the agent stop.                                             |
| **CI**                   | Continuous integration — the automated checks (build, tests, lint, coverage) that run on every PR (pull request — the proposed change under review) before it can merge. |
| **The grader**           | A fresh AI agent that did **not** write the code. It reads the spec and the change, and posts a check-by-check verdict on the PR. Required to run; its verdict advises — the human Checker decides. |
| **The Checker**          | The pod member who approves a change. Never its author.                                                                                                               |
| **Risk tier**            | HIGH / MEDIUM / LOW, assigned per spec at triage. Sets how tightly the agent is bounded and how much review the change gets.                                          |
| **The decision list**    | The running list of product decisions nobody has made yet, each needing Luis's named answer within the agreed 2 business days.                                        |
| **WIP cap**              | The limit on changes in flight at once — Harbor's pod set it at 6 at the end of Foundation.                                                                           |
| **Review-wait tripwire** | The agreed threshold (median one working day) that, once crossed, stops new work starting until the review queue clears.                                              |
| **Accepted-as-is**       | Agent work merged without rework — the dashboard's trust signal.                                                                                                      |

## 1. How the week played out

> **Reading the Tooling lines.** **You run it** — a slash command you type (e.g. `/sdlc-status`,
> `/e2e`). **It triggers** — an agent or script that command runs under the hood, always shown
> after a `→`. **No plugin command** — a human meeting, a decision, or a spec riding the build
> loop; nothing the plugin drives directly. Build is the least plugin-driven stretch of the
> engagement: the loop runs on the rails, not on commands, so most lines carry the grey pill.

**Monday 5/4 — flow check, then intent triage.**
**Tooling —** `/sdlc-status` → the queue and wait numbers read at the flow check; the triage
itself is humans deciding, with Claude drafting candidate specs from the kit spec-template
in-session.

- **The flow check, 10 minutes, queue number first.** Four changes waiting to be checked,
  oldest 1.2 days — spec 0012 (document upload, HIGH), sitting in the security queue, which is
  read separately because it clears slower. Maya takes chasing Dan as her commitment. The WIP
  cap (6) holds; one Checker assignment moves so nothing waits on Sara alone. Nobody reports
  what an agent did yesterday — the meeting walks the work, not the people.
- **Intent triage, 60 minutes.** Three stories on the table:
  - *"Show adjusters similar past claims"* fails the vague-line test — nobody can write an
    acceptance check for "similar," so nobody can build it. It goes back for sharpening with
    Luis; agents never see it. A bounce at triage costs a conversation; the same vagueness
    discovered mid-build costs a redo.
  - *The fast-path work queue* (from Gail and Marcus's feedback on the skeleton demo) sharpens
    cleanly into **spec 0015**: fast-path claims (D-09's simple 61%) surface first in the
    adjuster queue. MEDIUM — new business logic, nothing hard to undo.
  - *Duplicate-claim merge* (D-07: the same loss reported twice becomes one claim, never a
    rejection) becomes **spec 0016**. Maya tiers it **HIGH** — merging claim records is hard
    to undo, and a wrong merge mangles two policyholders' data. Triage also surfaces a silent
    decision: *what does the second reporter see when their claim joins an existing one?*
    Nobody answers it in the room; it goes on the decision list with Luis's 2-day clock.

**Tuesday 5/5 — 0015 rides the loop, clean.**
**Tooling —** No plugin command. Spec 0015 rides the loop: authored from the kit
spec-template, plan mode under bounds, ci.yml + grader.yml on the PR, a non-author Checker,
deploy-dev.yml on merge.

- Jonah authors the spec — five acceptance checks, each one testable ("a fast-path claim
  created after a standard claim still sorts above it; ties break by FNOL timestamp,
  oldest first").
- He sets the bounds: scope is the work-queue service and its tests, nothing else; context is
  the existing queue read model ("reuse it — do not invent a second one"); permissions are
  the standard set. The agent's plan glosses sort stability; Jonah makes it explicit and
  approves. Total human time before code: about forty minutes.
- The agent builds. The Stop hook holds it to a green suite; the PR fires CI and the grader;
  the grader walks all five checks and reports clean; Sara — who didn't write it — checks and
  merges. Deploy-dev ships it. Gail has the new queue in dev before the end of the day.
  Accepted as-is: no rework, no drama. **Most specs should look like this one.**

**Wednesday 5/6 — 0016: intent sharpened, then delegated tight.**
**Tooling —** No plugin command. Luis's decision lands inside his clock; spec 0016 enters the
loop at HIGH.

- Luis answers the decision-list item within his clock: the second reporter sees *"your report
  has been added to an existing claim for this loss"* — a confirmation, never a rejection,
  honoring D-07's spirit. The answer goes in the spec, not in anyone's memory.
- Sara finalizes the spec. The check that matters most is the one written from Dee Alvarez's
  intake reality — phone reporters often don't have their policy number:

  > **Check 3.** Matching is keyed per policy number plus a 7-day loss window, independently —
  > one policy's candidate matches never affect another's. A claim arriving **without** a
  > policy number is never auto-merged; it routes to the manual-review queue.

- She delegates with two leashes: tight on the matching keys and the merge write path
  ("follow the plan exactly; deviate only by asking"), loose on the merge-audit log
  formatting ("your call"). In plan mode she pushes on the one thing the plan glosses —
  *what exactly is the match key when the policy number is absent?* — and the agent's answer
  is vague, which is a tell. The plan gets the explicit route-to-manual-review path before
  she approves it.

**Thursday 5/7 — 0016: the grader catches what green tests missed.**
**Tooling —** No plugin command. The `risk:high` label fires security.yml → the
security-reviewer agent; grader.yml posts the verdict; Wes's named sign-off lands in the PR.
The setup review (Rob + Jonah) merges the week's harness changes.

- The agent finishes. Its own tests pass — eleven of them, all green. The Stop hook lets it
  stop. The PR opens; CI goes green. On an unchecked team, this is where it ships.
- The grader — a fresh agent, told plainly it did not write this code — walks the acceptance
  checks and fails it on check 3. Despite the approved plan, the built code normalizes a
  missing policy number to an empty string *before* the matcher runs, so every no-policy
  phone claim inside a 7-day window shares one match bucket. Two unrelated phone reporters in
  the same storm week would have been merged into one claim. The author's eleven tests only
  cover claims that *have* a policy number — the suite is green and the bug is live. (The
  full verdict is in section 4.)
- The fix goes back through the same loop: no-policy claims route to manual review before the
  matcher, plus a test for the no-policy path. Re-graded clean. The security-reviewer agent
  passes the data-handling. **Wes signs off by name** — the named human sign-off HIGH risk
  requires — and Jonah, not Sara, checks and merges. Deploy-dev ships it.
- At the setup review, Rob and Jonah (his deputy) merge the week's harness changes — including
  last week's Retro+ item: an escaped bug (acknowledgment timestamps rendered in UTC, which
  showed the wrong day against the 15-business-day regulatory clock, C-04) was answered with
  "which check should have caught it?" — so the test-writer skill now drafts timezone-boundary
  cases into every suite that touches a date the business reads.

**Friday 5/8 — Retro+, then the biweekly steering.**
**Tooling —** `/visual-explainer` → the steering demo narrative and scorecard visuals; the
weekly five-bullet summary drafted by Claude, corrected by Maya. The retro is humans.

- **Retro+.** Zero escaped bugs this week. The 0016 catch is read out loud — not as a
  near-failure but as the system working: the check existed because intent was sharp, the
  grader caught it because the check gave it something to grade, and it never reached dev.
  The "similar claims" bounce gets the same framing: the cheap place caught it. One trend
  flagged: the security queue's wait (2.1 days median) is drifting up; Maya takes it to Dan
  outside the room.
- **Steering, 45 minutes.** Gail drives the demo herself — the fast-path queue and the
  duplicate-merge flow, live in Harbor's dev environment. The scorecard: 11 of 14 Build specs
  merged accepted-as-is (79%); median review wait 0.9 days (under the one-working-day
  tripwire); the FNOL→decision clock is instrumented and ticking in dev — Karen is told
  plainly that the production needle moves at rollout, not before. Q-18 (Priti and Nadia's
  surge load-test dataset, built from the 2024 CAT event) lands this week — hardening pass 1
  is scheduled against it. The decision list carries one new item for Luis. No PR counts, no
  "AI productivity" numbers — demos and outcomes only.

## 2. What to notice

- **The catch happened because the check existed.** The grader found the empty-string bucket
  *because* check 3 said "per policy, independently, never auto-merge without a number." A
  vague spec ("detect duplicate claims") would have given it nothing to grade against, and
  the bug ships. Sharp intent is what makes checking possible — the beats are one system.
- **Green tests are not done.** Eleven passing tests, a green build, a satisfied Stop hook —
  and a live data-mangling bug. The author's tests prove what the author thought to test.
  That is why the author is never the only approver, human or agent.
- **The depth matched the risk.** 0015 (MEDIUM) cleared with the grader plus one Checker in a
  day. 0016 (HIGH) got tight bounds, the security agent, and a named sign-off. Neither was
  over- or under-checked; the tier decided, not the mood.
- **The bounce at triage is the loop protecting itself.** "Similar claims" never reached an
  agent. The vague-line test at intent costs a conversation; the same gap found at the PR
  costs a build.
- **The queue numbers ran the week.** The flow check opened with them every day, the security
  queue was read on its own line (and its drift got an owner before it became a stall), and
  the WIP cap kept the pod from outrunning its own checking.
- **The client saw outcomes.** Gail demoed software she uses; Karen saw the scorecard and an
  honest statement about when the metric moves. Nobody saw a PR count.

## 3. Artifact: spec 0016 (as merged)

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

## 4. Artifact: the grader's verdict that mattered

The grader's PR comment on 0016's first build, posted by the rails (grader.yml), verbatim:

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
no-policy-path test) · security-reviewer agent pass on the data path · **signed off: Wes
Carter** (named HIGH-risk sign-off) · checked and merged by Jonah Kim (non-author) ·
deploy-dev green. The bug existed for roughly four hours, all of them on a branch.

## 5. Artifact: the week by the numbers

What the pod's internal dashboard showed Friday (baseline-and-trend, no targets):

| Number                        | This week           | Read as                                                              |
| ----------------------------- | ------------------- | ------------------------------------------------------------------- |
| Accepted-as-is                | 11 of 14 specs (79%) | Trust rising — intent and bounds are working                        |
| Review wait (median)          | 0.9 days            | Under the one-working-day tripwire; no stop triggered               |
| Security-review wait (median) | 2.1 days            | Drifting up — flagged at Retro+, Maya owns it with Dan              |
| Bounce-backs at triage        | 1 ("similar claims") | The cheap place caught it                                           |
| Escaped bugs                  | 0 (1 last week: the UTC clock) | Last week's answered with a harness change, merged Thursday |
| WIP                           | 5 of 6 cap          | Headroom held all week                                              |

What steering saw instead: the live demo, the outcome clock (instrumented, moves at rollout),
the stability trend, the accepted-as-is trend, and the decision list. What steering never
sees: PR counts, lines of code, story points, "AI productivity."

## 6. The tooling behind this week

The [Build loop deep-dive](build-loop.md) describes this work generically. What actually ran,
on the **claude-code-sdlc** plugin, the kit's rails, and the paired skills:

| What got produced                       | How                                                                                                                                                       |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Flow-check queue numbers                | `/sdlc-status` at the daily flow check; the security queue read on its own line                                                                          |
| Ready specs (0015, 0016)                | Triage is humans; Claude drafts candidate specs from the kit spec-template in-session; the Pod Lead tiers them                                            |
| Spec 0015 (MEDIUM), end to end          | Rides the loop: plan mode under bounds, Stop hook, ci.yml + grader.yml on the PR, non-author Checker, deploy-dev.yml on merge                            |
| Spec 0016 (HIGH), end to end            | Same loop plus the HIGH path: `risk:high` label → security.yml → the security-reviewer agent; Wes's named sign-off in the PR                             |
| The 0016 catch                          | grader.yml — a fresh agent grading check-by-check against the spec in the diff; verdict posted as a PR comment, read by the human Checker                |
| Harness improvement (timezone checks)   | Last week's Retro+ answer; the test-writer skill updated by reviewed PR, merged at the setup review (Rob + Jonah)                                        |
| Steering demo narrative + scorecard     | `/visual-explainer` → the demo walkthrough and scorecard visuals; Gail drives the live demo herself                                                      |
| Weekly five-bullet client summary       | Claude drafts from the week's merged specs; Maya corrects and sends                                                                                      |
