# Glossary

_Every term the Delivery Standard leans on, defined in plain words. Alphabetical. Written for
anyone joining a pod, onboarding from the client side, or reading the standard for the first time
and hitting a word they don't recognize._

This is the on-ramp, not the law. Where a term has a precise home in the standard, the entry
points you there: **the standard** means `GOLD-STANDARD.md`; a **deep-dive** is the matching page
under `docs/`.

---

**Accepted-as-is rate.** How often Claude's work merges without anyone having to redo it. The
clearest single sign that the specs are sharp and the harness is tuned. Tracked on the internal
dashboard as a trend, never a target (standard, section 9). The trust signal of the whole method.

**ADR (Architecture Decision Record).** A short written record of one design decision and why it
was made over the alternatives. Claude researches the options and drafts the ADR; the Architect
(Setup Owner at one-pod scale) signs it. Produced in Phase 2 (see `docs/phase-2-design.md`).

**Agent.** A run of Claude doing work — reading, planning, writing code, or grading. "One agent
vs. many" is a real decision in the loop: one agent for tightly coupled code, many only for
independent read-only exploration (see [the build loop](build-loop.md)). See also **subagent**.

**The author is never the sole approver.** The rule that whoever produced a change doesn't get to
be the only one who signs it off — not for code, not for a harness change, not for a spec, not for
this document. A fresh grader and a non-author human carry the verdict. This is the practical
answer to "how do you trust code you didn't write." Survives every team size (see
[the team](team.md)).

**Bicep.** Microsoft's infrastructure-as-code language for Azure — the cloud environment described
as files in the repo instead of clicked together by hand. Always HIGH risk; lives in `infra/`.
See **IaC** and [the rails](the-rails.md).

**Branch protection.** GitHub/ADO settings on `main` that block a merge until the rules are met:
CI green, the grader has run, a non-author has approved. It's how the merge bar is enforced by the
platform rather than by good intentions (standard, section 4).

**Build loop.** The middle of an engagement, and the heart of the method. Instead of separate
Implementation, Quality, and Testing phases run in a batch, every story runs the same short cycle
— **Intent → Delegate → Discern** — and ships before the next one starts. Checking happens per
change, never piled up for later. Deep-dive: [build-loop.md](build-loop.md).

**Checker.** The role that owns the verdict on a change: reads the grader's report, grades the
work against the spec, probes an edge the tests missed, and approves or bounces. Not a separate
headcount — Orchestrators and Checkers swap per change, and the author of a change is never its
Checker. See [the team](team.md).

**Checking ladder** (also **verification ladder**). The series of checks a change climbs, each
rung harder to skip than the last: (1) a "what done means" rule in CLAUDE.md, (2) a check that
re-runs every turn, (3) a blocking **Stop hook** that won't let the agent finish with red tests,
(4) a separate **grader** agent that didn't write the code, (5) a human gate for HIGH-risk work
(with a security-reviewer pass first). It is not "please check your work." Detail in
[build-loop.md](build-loop.md).

**CLAUDE.md.** The file every agent session loads first. It holds the project's standards: the
stack rules, the domain glossary in the client's words, the risk taxonomy, the spec convention,
the gated paths, and the Definition of Checked. A stale CLAUDE.md means agents guess, and guesses
differ per run — keeping it current is Setup Owner work. Versioned and PR-reviewed like code
(standard, section 6).

**Definition of Checked.** What replaces "Definition of Done." A change is done when it has been
specified, tested, graded by someone other than its author, approved by a human where the risk
demands it, and merged without breaking anything. "The agent finished typing" is not done.

**Definition of Ready (DoR).** The bar a story has to clear before it enters the build loop,
enforced at intent triage: acceptance criteria pass the vague-line test, scope in/out is stated,
every silent decision for that story is answered, a risk tier is assigned, and the harness context
the agent will have is named (standard, section 5.1).

**Delegate.** The middle beat of the loop. The agent proposes a plan, the Orchestrator corrects or
approves it **before** any code, then the agent builds and self-checks inside the bounds it was
given (scope, context, one-agent-or-many). The building is the agent's job, not the human's.

**Deputy.** The named second person who reviews work the owner can't review alone — above all, the
Setup Owner's deputy, who reviews every harness change so the Setup Owner is never sole approver of
their own foundation. "No role without a deputy" is a standing rule (standard, section 4; see
[the team](team.md)).

**Discern.** The last beat of the loop, and the one the whole method is built around. Discern just
means working out whether the change is actually good before anyone trusts it: mechanical gates in
CI, the grader's check-by-check verdict, and a non-author human's approval — plus a named sign-off
on HIGH risk. A change is done only when something other than its author has proven it.

**DORA.** Google's long-running research program on what makes software delivery work (named for
the DevOps Research and Assessment team). Its 2024–2025 reports found that as teams leaned harder
on AI, delivery stability dropped two years running — AI makes a strong team faster and a sloppy
team worse. The standard tracks the DORA "four": deploy frequency, lead time, change-fail rate,
time-to-recover (standard, section 9).

**Evals / golden set.** For deliverables that are themselves AI-powered: a versioned set of input
scenarios with graded expected behavior (the golden set) and a pass threshold ("correct on ≥ 95%
of the set"). Evals are acceptance criteria, run in CI like tests. Changing a prompt, model, or
tool definition runs the full golden set as a regression gate (standard, section 11).

**Flow check.** What the daily standup becomes — 10 minutes, not "what did you do" (the agents did
plenty) but "what's waiting to be checked, which specs are vague, how long is the review queue."
Every waiting change leaves with a Checker assigned and the WIP cap enforced (standard, section
5.4).

**Gate.** A checkpoint where automated checks run and a named human signs before work advances.
**Phase gates** open and close the engagement (a fixed battery of validations, then a human
advances — advancement is always manual). **Merge gates** guard `main` inside the build loop. Gates
report; humans decide (standard, section 9).

**Grader.** A fresh agent whose only job is to grade work it did not write. It runs in CI, reads
the spec file in the diff, and posts a check-by-check verdict as a PR comment. Its run is required
(can't be skipped); its verdict is advisory (doesn't block) — the human Checker reads it and makes
the call. Machines gate the mechanical; humans own the judgment (standard, section 5.3).

**Hardening pass.** Scheduled integration-level work — load and performance, end-to-end journeys,
penetration testing — typically one mid-Build and one before deployment. It is scheduled work in
the flow, not a phase that gates everything else (standard, section 5.6).

**The harness.** Everything the agents work inside: `CLAUDE.md`, the `.claude/` directory (skills,
agents, hooks, settings), the CI workflows, and `infra/`. The Setup Owner treats it as a product —
versioned, owned, changed only by reviewed PR. A line in CLAUDE.md is a design decision enforced a
hundred times a day (standard, section 6).

**The harvest loop.** After every engagement, a mandatory retro PR against this repo: skills
generalized (client specifics stripped), hooks improved, templates corrected, a retro file added.
This is the compounding asset — the second engagement starts where the first finished (standard,
section 10).

**Hook.** An automatic gate that fires on its own at a set point — for example, when an agent tries
to stop. A **blocking** hook (the **Stop hook** / `stop-gate`) refuses to let the agent finish
while tests fail or the build is broken. It isn't optional or persuadable. The single
highest-value automation the kit ships (standard, section 5.2).

**IaC (Infrastructure as Code).** Defining the cloud environment as files in the repo rather than
configuring it by hand, so it's reviewable, repeatable, and auditable. Always HIGH risk; runs
through a generate → validate → policy → what-if → approve → scoped-apply → drift-check funnel.
See [the rails](the-rails.md).

**Intent.** The first beat of the loop, and the one humans own outright. Decide what you want, then
write it as something you can test ("returns 401 for a bad token," not "make auth good"). Vagueness
here is amplified by the agent, not fixed by it. Intent quality is the Pod Lead's charge; product
decisions inside it belong to the PO.

**The kit.** The installable engagement starter in this repo: CLAUDE.md template, spec template,
settings, skills, agents (grader, security-reviewer), hooks, CI workflows, Bicep starters, and the
stack profile. Phase 3 of every engagement begins by installing it into the client repo and
adapting it in the open (standard, section 10).

**Mechanical gates.** The hard blocks in CI that no human overrides: build, tests, lint, and 80%
coverage on new code. Distinct from the grader (required to run, advisory verdict) and the human
Checker (a hard block of a different kind). See [the rails](the-rails.md).

**METR.** A 2025 study in which 16 experienced developers ran 246 real tasks on their own mature
projects. They were about 19% slower with AI while believing they were 20% faster. A small study,
but the best causal evidence available, and it points opposite to the hype — most of the slowdown
came from people fixing work they hadn't described well. The standing argument for sharp intent.

**PO (Product Owner).** The person who owns what gets built and what "done" means, written clearly
enough to test. Either the client commits a named PO (≥ 4 hrs/week, answers decision lists within 2
business days) or **proxy mode** applies: the Pod Lead makes product calls on the client's behalf,
logged in a decision log the client ratifies at each steering. The Phase 0 workshop forces this
choice (standard, section 12).

**Plan mode.** A mode where the agent can read and think but change nothing. The Orchestrator works
out the approach and approves the plan here, before any code exists — corrections cost minutes in
plan mode and hours after the build (standard, section 5.2).

**Pod.** The delivery team that runs the loop: 4–6 people running 2–3 parallel work streams. The
limit on parallelism is **checking capacity, not headcount**. A pod never grows past 6 — when
there's more work than it can check, you add a pod, not a seventh person (see [the team](team.md)).

**Pod Lead** (was: Project Manager). Owns intent: every spec sharp, every decision answered, every
gate earned. Runs intent triage, the flow check, and client steering; assigns risk tiers; is the
interface to the client PO (or plays proxy-PM in proxy mode). See [the team](team.md).

**Quality Engineer** (was: QA). Stops _performing_ checks and starts _building the machinery_ that
checks every change: the grader definition, the Stop hook, the CI test gates, test infrastructure,
and (for agentic deliverables) the eval harness. Takes a regular turn as Checker. See
[the team](team.md).

**The rails.** The agentic CI/CD and DevOps pipeline every change rides — the four workflows (CI,
grader, security, deploy), the merge bar, deploy and promotion, and the agent-safe IaC funnel. Not
a numbered phase; a standing standard. Governing principle: **agent proposes, gate disposes.**
Deep-dive: [the-rails.md](the-rails.md).

**Review wait (median).** How long a change sits waiting to be checked. The real bottleneck
indicator under this model, and the number that caps parallelism — when it grows past the tripwire
(default: one working day), the pod stops opening new streams. Cheering output while this climbs is
the trap (standard, section 9).

**Retro+.** The retrospective, with one non-negotiable question added: for every bug that escaped
to production, "which check should have caught it?" The answer becomes a concrete change to a rung
of the checking ladder. An escaped bug that doesn't change a check is a wasted bug (standard,
section 5.4).

**Risk tier (HIGH / MEDIUM / LOW).** The taxonomy the Pod Lead assigns to every spec at triage,
recorded in the spec and in CLAUDE.md so agents see it too. HIGH (auth, payments, PII, migrations,
public API or pipeline/IaC changes, prompt/model/tool changes, anything hard to undo) triggers the
full ladder, a security-reviewer pass, and a named human sign-off. Challenges escalate up, never
down (standard, section 5.1).

**Setup Owner** (was: Architect). Owns the harness as a product — CLAUDE.md, skills, agents, hooks,
settings, the pipeline, the IaC, the kit install. Names a deputy on day one. The keystone role and
the known bus-factor risk, which is why the deputy rule exists. See [the team](team.md).

**Setup review.** The weekly 30–60 minute meeting where the week's harness changes merge, Retro+
findings become new checks or skills, and token spend is reviewed. The Setup Owner's deputy reviews
(standard, section 5.4).

**Skill.** A written-down team practice or runbook the agent loads when it's relevant (a
test-writing pattern, an API convention). Skills keep their detail out of the way until needed, so
the agent isn't carrying everything at once. Generalized skills are harvested back into the kit
between engagements.

**Spec.** The written description of one piece of work plus how it will be checked —
`specs/NNNN-name.md`, one file per feature. The real source of truth: the code is just one way to
satisfy it, and the spec lasts when the chat history is gone. The spec file rides in the PR diff so
the reviewer sees intent and implementation together (standard, sections 4 and 5).

**Sponsor.** The client executive who owns the business outcome and the one success metric. Their
obligations are written into the SOW (standard, section 12).

**Steering.** The biweekly 45-minute client meeting: a live demo of working software in the dev
environment, the outcome scorecard, the decision list the client needs to answer, and gate status
near a phase boundary. **No activity metrics, ever** — demos and outcomes only (standard, section
5.5).

**Stop hook** (`stop-gate`). The blocking hook that refuses to let an agent finish a turn while the
tests fail or the build is broken. See **hook**.

**Subagent.** A separate agent instance run alongside the main one, used two ways: fanned out in
parallel for read-only investigation or option comparison, and kept separate from the author so the
grader never reviews its own work. A side-quest's mess stays out of the main conversation.

**Trunk-based.** The branching model: a protected `main`, one short-lived branch per spec
(`spec/0007-rate-limiting`), one PR, squash-merged and deleted on merge. **One spec = one branch =
one PR** (standard, section 4).

**Vague-line test.** The bar for an acceptance line: _could two people build different things from
this line?_ If yes, it isn't ready — it bounces back to the PO, not down to an agent. The Pod
Lead's first filter at triage (standard, section 5.1).

**Vibe coding.** Casual prompting with no checking — letting the agent write straight to production
with nobody verifying. Fine for a throwaway prototype, dangerous for a system. The thing this
standard exists to replace: no checking is just vibe coding; the loop closes it.

**Walking skeleton** (also **thin slice**). The thinnest possible end-to-end feature, built through
the full loop and deployed to the client's dev environment — the exit proof of Phase 3 (Foundation)
that the factory actually works before the build loop opens at volume (see
`docs/phase-3-foundation.md`).

**WIP cap.** The hard limit on concurrent agent streams — default: no Orchestrator runs more than 2
at once, and the pod halts new streams when median review wait exceeds one working day. A
checking-capacity limit, not a headcount one (standard, section 14).

---

_New to the method? Read the [loop cheat-sheet](cheatsheet.md) next, then the
[FAQ](faq.md). No checking is just vibe coding — the loop closes it._
