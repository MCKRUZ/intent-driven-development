# The Build Loop

Deep-dive on the heart of the method: the per-spec cycle that replaces the implementation,
testing, and review phases of a traditional SDLC. The gated phases open the engagement (0-3)
and close it (7-9, C); everything in between — typically 8 to 16 weeks, the bulk of the
engagement — runs as this loop. There is no exit gate at the end of a loop pass, because the
loop is not a phase. It is how every single change gets built, from the day the Foundation
gate closes to the day the backlog is done.

> **What gates every change** (the checking ladder, section 4): nothing merges without CI green (build,
> tests, lint, 80% coverage), the grader having run (advisory), and a non-author approval — HIGH
> risk adds a security pass and a named sign-off. The depth scales by risk tier, and the author
> never approves their own work. The failure mode to watch (section 9): the author grading itself —
> checking theater that catches nothing.

**If you're starting here:**

|                          |                                                                                                                                                                                                             |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The method**           | Claude (the AI coding agent) drafts documents and writes most code. Humans own every decision and verify every result.                                                                                      |
| **The rhythm**           | Numbered phases open and close the engagement; in between runs this continuous build loop. Phases end with gates (automated checks plus a named human sign-off); the loop has no gate — it has a merge bar that every change clears. |
| **Where we are**         | Phase 0 fixed the problem. Phase 1 signed the requirements. Phase 2 chose the architecture. Phase 3 built the factory — the harness, the pipeline, the rails — and proved it on the walking skeleton. The loop now runs everything else. |
| **Our pod (4-6 people)** | Pod Lead · Setup Owner · Orchestrators · Quality Engineer. ([Team deep-dive](team.md))                                                                                                                      |

**Words this page leans on** (every other term is explained where it first appears):

| Term                      | What it means                                                                                                                                                                                                            |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A spec**                | One feature, described in one file in the repo (`specs/NNNN-name.md`): the goal, what is in and out of scope, testable acceptance checks, and a risk tier. It is what the agent builds from — no spec, no build.         |
| **A story**               | A user-facing piece of work as the backlog holds it — what a spec is before it has been made ready and written down precisely.                                                                                            |
| **Definition of Ready**   | The bar a story clears before anyone builds it: acceptance criteria pass the vague-line test, scope in/out stated, the silent decisions answered, a risk tier assigned, the harness context named.                       |
| **The vague-line test**   | "Could two people build different things from this line?" If yes, the line is a wish, not a check.                                                                                                                       |
| **The decision list**     | The running list of product decisions nobody has made yet ("you haven't decided X"), each needing a named human answer — on the client clock agreed in Phase 1. Each item records the question, the date raised, the named client owner, the clock date, and the answer once given; the list lives in the repo with the phase artifacts and goes to every steering. |
| **Plan mode**             | The agent mode where Claude can read the repo and propose an approach but cannot change files. Plans get approved by a human before any code is written.                                                                  |
| **PR**                    | Pull request — the proposed change under review. One spec = one branch = one PR.                                                                                                                                          |
| **CI**                    | Continuous integration — the automated checks (build, tests, lint, test coverage) that run on every PR before it can merge.                                                                                               |
| **The grader**            | A fresh AI agent that did **not** write the code. It reads the spec and the change, and posts a check-by-check verdict on the PR. It is required to run, but its verdict advises — the human Checker decides.             |
| **The Checker**           | The pod member who approves a change. Never its author — the author of a change is never its only approver.                                                                                                              |
| **The Stop hook**         | A script that fires when an agent tries to finish its turn. If tests fail or the build is broken, it refuses to let the agent stop. "Done" stops being the agent's opinion.                                              |
| **Rails**                 | The enforcement built in Phase 3, taken together: CI gates, the grader, branch protection (the repo settings that make the gates mandatory), and the deploy pipeline. Every change runs on them; nobody has to remember them. |
| **Risk tier**             | HIGH / MEDIUM / LOW, assigned per spec at triage. Sets how tightly the agent is bounded and how much review the change gets.                                                                                              |
| **WIP cap**               | The limit on how many changes may be in flight at once. Set at the end of Phase 3 from checking capacity (the standard's default: no Orchestrator runs more than two concurrent agent streams), enforced at the daily flow check. |
| **Review-wait tripwire**  | The wait-time threshold that, once crossed, stops new work starting until the review queue clears (default: median one working day; set alongside the WIP cap at the end of Phase 3). Review is the loop's real bottleneck; this number is how the pod refuses to bury it. |

The loop is three beats, run for every change, large or small:

1. **Intent** — decide what you want, clearly enough to check, and write it down as a spec.
2. **Delegate** — an agent builds it, inside bounds a human set, from a plan a human approved.
3. **Discern** — checks and a non-author prove it before anyone trusts it; merge deploys it.

The moment the pod starts skipping the loop for "small" changes is the moment unchecked work
creeps back in. Small and risky is exactly the cheap-to-type, expensive-to-get-wrong case: the
worst bugs in agent-built code ship inside changes someone decided were too small to bother
checking.

> Worked example: [`build-loop-example.md`](build-loop-example.md) — one ordinary week of
> Harbor Mutual's Build: two specs end to end, the grader catching a bug that eleven green
> tests missed, a story bounced for vagueness, and the numbers steering gets shown.

---

## 1. Who is involved

The opening phases each had an owner; the loop has a rotation. Every Orchestrator authors
specs, runs agents, and serves as a Checker on changes they didn't write — the hats move
per change, the rules don't.

### Our side

| Person               | Load   | In the loop                                                                                                                                                                      |
| -------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pod Lead**         | 50-70% | Owns triage: stories become ready specs, risk tiers get assigned, the WIP cap holds. Routes decision-list items to the client. Runs the cadences and the steering. First escalation point when the queue grows. |
| **Orchestrators**    | 90-100% | Run the loop all day: author specs from triaged stories, set the bounds, approve plans, drive agents, and check each other's changes. The craft of the role is in the bounds and the checking, not the keystrokes. |
| **Quality Engineer** | 60-80% | Owns the checking: the checking plan per spec, the health of the rails, the escaped-bug answer at every retro ("which check should have caught it?"), and the scheduled hardening passes. |
| **Setup Owner**      | 30-50% | The harness stays a product all through Build: CLAUDE.md current, skills and hooks improved by reviewed PR, the deputy reviewing every harness change, token spend watched.        |

### Client side

| Person             | Needed for                                                                                                                       | How much                                  |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| **Product Owner**  | The decision list — every silent product decision gets their named answer on the agreed clock; acceptance of what the demos show | Steady hours weekly, agreed in the SOW    |
| **Domain experts** | Pulled into intent when a spec touches their ground truth (the intake rule, the ledger quirk)                                    | As specs demand                           |
| **Security**       | The named sign-off on every HIGH-risk change; their queue is tracked separately because it clears slower                          | Per HIGH change                           |
| **Sponsor**        | The biweekly steering: a live demo and the outcome scorecard, not activity reports                                               | 45 minutes biweekly                       |

### Claude's role in the loop

Claude does most of the building and much of the checking — but never both on the same change.

- **Builds, bounded.** From an approved plan, inside the scope, context, and permissions set
  per spec. The Stop hook means it cannot call its own work finished with a red test or a
  broken build.
- **Grades, as a separate agent.** The grader that judges a change is a fresh agent that did
  not write it, told so plainly, grading check-by-check against the spec. The author — human
  or agent — is never the only approver.
- **Drafts the connective tissue.** Candidate specs from triaged stories, test suites from
  acceptance checks, the weekly client summary from merged work. Humans correct and own all
  of it.

What Claude never does: merge, approve its own work, assign a risk tier, answer a decision-list
item, or downgrade a challenge. Risk challenges escalate up, never down, without discussion
(anyone — human or agent — can raise a tier on the spot; lowering one always takes a
discussion with the Pod Lead, who owns the tier).

---

## 2. Intent — decide and write

Nothing enters the loop as a conversation. A story becomes buildable only by clearing the
**Definition of Ready** at weekly intent triage:

- Every acceptance criterion passes the vague-line test. "Handle errors gracefully" is a wish;
  "a duplicate submission returns 409 with `{ "error": "duplicate claim" }`" is a check.
- Scope in and scope out are both stated. What the change must not touch is as load-bearing as
  what it must do.
- The silent decisions are answered. A real product choice left unwritten (fail open or fail
  closed? what does a blocked user see?) does not disappear — the agent makes it for you, fast,
  under no supervision, and you find out what it chose when something breaks.
- A risk tier is assigned by the Pod Lead and recorded in the spec.
- The harness context the agent will rely on is named — which existing pattern this change
  reuses, so the agent extends the codebase instead of inventing a second way to do something
  it already does.

The Orchestrator then writes the spec — one file, in the repo, durable across sessions:
Goal, Why, Scope in/out, Acceptance checks, Risk tier, Delegation plan (what the agent may
touch, what is gated), Checking plan (how high this change climbs the checking ladder,
section 4). The spec outlives the chat that produced it; the agent reads it every session,
the grader grades against it, and when behavior changes later, the spec changes in the same
PR — a stale spec is a lie that misleads the next reader and the next agent.

**The risk taxonomy** (it lives in the harness so agents see it too):

| Tier   | What lands here                                                                                                                                                                                  | What it triggers                                                                                       |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| HIGH   | Auth/identity, payments, personal or client data handling, schema migrations, public API contract changes, infrastructure and pipeline changes, AI-behavior changes (prompts, models, tool definitions), anything hard to undo | Tight agent permissions, the full checking ladder, a security review pass, a named human sign-off in the PR |
| MEDIUM | New business logic, external integrations, changes to shared internal services                                                                                                                   | Standard permissions, grader plus a human Checker                                                       |
| LOW    | UI within existing patterns, copy, internal tooling, additive CRUD on established rails                                                                                                          | Lighter review; the grader and the mechanical gates still run                                           |

Intent is the highest-leverage hour anyone spends in the loop. When the agent can produce the
code in minutes, what decides whether you get what you wanted is how clearly you said it —
vague intent doesn't get fixed downstream, it gets built, fast, wrong.

---

## 3. Delegate — bound and build

Delegating is not "go build it." It is drawing the box the agent works inside, and approving
its plan before it starts.

**Plan first, always.** The agent starts in plan mode: it reads the repo and the spec and
proposes an approach — which files it will touch, how it will satisfy each acceptance check —
before it may write anything. The Orchestrator corrects or approves the plan, and looks for
the one decision the plan glosses over ("what is the counter key when the request has no
key?"). Correcting a plan costs a sentence; correcting a finished build costs a redo. The most
dangerous decisions in agent-built code are the ones nobody noticed being made — plan approval
is where they get noticed.

**Three bounds, set per spec:**

- **Scope** — the file patterns the change may touch. Everything else is out, and "if you
  think something outside this needs to change, stop and ask" is part of the handoff.
- **Context** — the one canonical pattern to reuse, named explicitly. An agent not pointed at
  the existing pattern will happily invent a second one, and now the codebase has two.
- **Permissions** — what the agent may do without asking. The harness auto-allows the safe
  commands (build, test, lint, reads) and forces a human confirm on the rest: package
  installs, network calls, anything under a gated path like migrations or auth.

**Freedom by risk, within one change.** The parts that are cheap to undo get a loose leash
("implement the log throttling however reads cleanest"); the parts that are expensive to get
wrong get a tight one ("for the keying and the auth check, follow the plan exactly — deviate
only by asking"). Stay out of the keystrokes on the easy stuff; stay in the big calls on the
hard stuff.

**One agent or many.** Fan out to explore: independent investigations (three candidate
approaches, each written up by its own agent) run in parallel because they touch nothing
shared. Single-thread to build: one feature writing into shared code paths gets exactly one
agent, start to finish, because parallel agents in the same files clobber each other. The
test: are the pieces independent (fan out) or tangled (single-thread)? Spread out to explore,
line up to commit.

**The box is enforced, not requested.** The permission rules hold whether or not anyone is
watching, and the Stop hook refuses to let the agent finish with failing tests or a broken
build. This hook is the single highest-value automation in the standard: it turns "the tests
must pass" from a request the agent might rationalize past into a fact about the world.

---

## 4. Discern — prove, then merge

Written is cheap now; checked is the bar. A change is done when it has been proven against
its spec by something other than its author, not when the code exists. The proving climbs a
**checking ladder** — five rungs, each catching what the one below cannot:

| Rung | The check                  | What it catches that the rung below can't                                                                                                          |
| ---- | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | The done-rule in the harness | Sets the bar ("done means checked, not typed"); persuasion only — it enforces nothing by itself                                                     |
| 2    | The agent re-checks each turn | The agent's own mechanical slips: the broken import, the test it broke two steps back                                                              |
| 3    | The blocking Stop hook       | The agent declaring itself done anyway — it cannot finish with red tests or a broken build. But a hook enforces the tests that exist; it cannot enforce a test nobody wrote |
| 4    | The separate grader          | The hole the author was blind to: it grades check-by-check against the spec, not against the tests, so it catches the case the author never thought to test |
| 5    | The human / security gate    | The judgment calls no machine should own: the risk acceptance, the product call, the security sign-off on a HIGH change                              |

Rung 4 is where the bug the author's green test suite hid goes to die — and it only works
because Intent wrote checkable acceptance criteria for it to grade against. A vague spec gives
the grader nothing to test, and the bug ships. The ladder is the payoff of the spec.

In the rails, the ladder lands as three layers on every PR:

- **Mechanical gates in CI** (hard blocks): build, tests, lint, 80% coverage on new code.
- **The grader in CI** (required to run, advisory verdict): a fresh agent reads the spec in
  the diff and posts a check-by-check verdict as a PR comment. It cannot be skipped — "the
  grader has run" is a required status check — but its verdict does not block. The human
  Checker reads it and makes the call. Machines gate the mechanical; humans own the judgment.
  A failed check — the grader's verdict or the Checker's bounce — goes back to the same
  Orchestrator, who drives the fix on the same branch. Every gate, including a fresh grader
  run, runs again on the updated PR before merge.
- **The human Checker** (hard block): non-author approval on every PR. On HIGH risk, also a
  security review pass and a named human sign-off recorded in the PR.

You do not run every change up all five rungs — that recreates the review bottleneck the loop
exists to remove. The risk tier sets the climb: LOW stops after the grader's advisory pass and
a light human look, MEDIUM gets the standard grader-plus-Checker treatment, HIGH goes all the
way up. One depth for everything fails in both directions — reading a typo fix as hard as an
auth change burns the pod's scarce review attention, and waving an auth change through on a
glance ships the instability the industry's own delivery research keeps warning about.

Merge deploys to the client's dev environment automatically — the rails from Phase 3. A true
emergency merge past a gate requires the Pod Lead plus one other human, an exception label,
and a retro agenda item. Two exceptions in a month means the gate or the specs are wrong —
fix that, don't keep excepting.

---

## 5. The week

Four short meetings replace the ceremony calendar. None of them asks "what did you do
yesterday" — when agents do the building, that answer is "the agents wrote a lot," and the
number means nothing. The meetings point at the two things that actually constrain the loop:
the clarity of intent going in, and the review queue coming out.

| Meeting                | Length    | Replaces   | What it does                                                                                                                                        |
| ---------------------- | --------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Flow check** (daily) | 10-15 min | standup    | The queue number first: how many changes wait for checking, how long the oldest has waited. Walk the in-flight changes nearest-done first — start with PRs waiting on a Checker, end with work not yet started — reading from wherever the pod tracks changes in flight. Every waiting change gets a Checker; vague specs get flagged back to triage; the WIP cap gets enforced; one commitment each (each person names the one thing they will move or unblock today). |
| **Intent triage**      | 60 min    | refinement | Stories become ready specs: vague lines sharpened, silent decisions surfaced onto the decision list, risk tiers assigned, the backlog ordered.        |
| **Retro+**             | 60 min    | retro      | Every escaped bug gets the same question — "which check should have caught it?" — and the answer becomes a harness improvement, not a resolution to try harder. |
| **Setup review**       | 30-60 min | (new)      | The week's harness changes merge: CLAUDE.md updates, skill and hook improvements, permission tuning — versioned, PR'd, reviewed by the Setup Owner's deputy. |

The Pod Lead runs the flow check and intent triage (whole pod attends; the Quality Engineer
vets checks for testability at triage); the Quality Engineer brings the escaped-bug list to
Retro+ (whole pod); the Setup Owner and their deputy run the setup review.

Two numbers run the week. The **WIP cap** keeps the pod from opening more changes than its
checking capacity can clear — agents can always write more code; the constraint is proving
it. The **review-wait tripwire** is the alarm on the same constraint: when the median wait
crosses the agreed threshold, the pod stops starting new work and clears the queue. The
security queue is read separately at every flow check — it clears slower, and averaged in
with the rest it hides until something HIGH has quietly waited a week.

---

## 6. The client's view

The client never sees the loop's internals — they see working software on a steady rhythm.

- **Biweekly steering, 45 minutes:** a live demo in the dev environment, the outcome
  scorecard (their success metric, the delivery-stability trend, the accepted-as-is trend),
  the decision list needing their answers, and gate status when a phase boundary is near.
- **A weekly five-bullet async summary** in between. Written for a busy reader: what shipped,
  what's next, what we need from you. Claude drafts it from the week's merged work; the Pod
  Lead corrects and sends it.
- **No activity metrics in client materials, ever.** No PR counts, no "AI productivity"
  claims. Agents inflate every activity number; demos and outcomes don't lie.

The decision list is the client-facing edge of Intent: every silent decision surfaced at
triage that belongs to the product lands there, with the agreed answer clock. A stalled
decision list is the loop's most common external blocker, and it goes to steering as a
delivery risk, not absorbed as quiet guessing.

---

## 7. Hardening passes

Quality in the loop is per-change; some concerns only exist at the integration level —
performance under load, end-to-end journeys across many features, penetration testing. The
Quality Engineer plans and runs them as **scheduled hardening passes** — typically one
mid-Build and one before deployment prep — using the end-to-end and security tooling. The
first hardening pass is also where
the test environment gets added alongside dev. Hardening is scheduled work inside the flow —
specs, triage, the loop — not a phase that gates all other work.

---

## 8. The numbers that steer the loop

Internal dashboard, baseline-and-trend, no vanity targets:

- **Accepted-as-is rate** — agent work merged without rework. The trust signal: rising means
  intent and bounds are working.
- **Review wait (median)** — the real bottleneck indicator. If it grows, stop opening
  streams; more building throughput cannot fix a checking constraint.
- **Rework / revert rate** and **bounce-back-for-unclear rate** — intent quality signals. A
  spec that bounces back as unbuildable is a triage miss, not an agent failure.
- **Escaped bugs** — every one answered at Retro+ with "which check should have caught it?"
- **The DORA four** — deploy frequency, lead time, change-fail rate, time-to-recover: the
  industry-standard delivery health measures, watched as trends.
- **Security-review wait** — on its own line, always.

A metric with nothing recorded reads **"no data"**, not zero — a fabricated zero looks like a
measured result and steers the room wrong.

Never tracked, never reported: velocity, story points, PR count, lines of code. Agents
inflate all of them, and the published research backs the caution — measured teams have
doubled PR volume while actual delivery stayed flat.

---

## 9. What goes wrong in the loop

- **Skipping Intent.** Typing the wish straight to the agent ("add rate limiting, go"). The
  agent builds something plausible and fast, and the undescribed case is the one it gets
  wrong. Everything enters through a ready spec, every time.
- **The author grading itself.** The agent that wrote the code confirming it works, or the
  Orchestrator who drove it approving it. Checking theater — it catches nothing the author
  didn't already think of. Author never approves, no exceptions.
- **One review depth for everything.** Gating every typo behind a human recreates the
  bottleneck; waving auth changes through on a glance ships the incident. The tier sets the
  climb.
- **"Too small to bother."** The loop skipped for small changes. Small and risky is the
  expensive case; the discipline is the same at forty lines as at four hundred.
- **The unbounded handoff.** No scope, no named pattern, no permissions — the agent fills
  every gap with a guess and touches three things nobody wanted touched.
- **Fanning out a build.** Parallel agents writing the same files clobber each other. Fan out
  only to explore; one agent writes shared code.
- **The rotting spec.** Behavior changes, the spec doesn't, and now the source of truth lies
  to the next agent and the next human. The spec changes in the same PR as the behavior.
- **A hook that passes by hiding the failure.** Skipping the flaky test to go green is the
  rail lying to you. Fix the cause; never suppress the check.
- **Ignoring the queue number.** Review wait creeps up, everyone keeps starting work, and the
  loop silts up invisibly until nothing merges. The tripwire exists to make stopping
  automatic, not heroic.
- **Quiet gate exceptions.** Emergency merges that stop being emergencies. Two in a month
  means the gate or the specs are wrong — fix the system, don't normalize the bypass.

---

Back: [Phase 3: Foundation](phase-3-foundation.md) — the phase that built the rails this loop
runs on.

Next: [Phase 7: Documentation](phase-7-documentation.md) — when Build is feature-complete,
the close begins: proving a stranger can understand, run, and operate the system from its
documentation alone.
