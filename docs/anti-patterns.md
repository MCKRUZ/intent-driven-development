# Anti-Pattern Field Guide

_The nine ways this goes wrong. For each: the symptom you'll actually notice, the root cause, the
fix in our standard, and how to keep it from coming back. Use it to spot trouble before it ships._

The standard buries these inside each phase's "failure modes" section. This page pulls them into
one scannable place. Terms are defined in the [glossary](glossary.md).

---

## 1. Shipping with no checking

The most common and most dangerous mistake — letting the agent write straight to merge with nobody
verifying.

- **Symptom:** Changes go from agent to merged with no test run, no second pair of eyes, no gate.
  "It looked right" is the only sign-off. Production incidents start tracing back to code nobody
  actually read or tested.
- **Root cause:** Treating "the agent finished typing" as the work being done. The **Discern** beat
  is missing entirely.
- **Fix:** The checking ladder, enforced by branch protection. At minimum: mechanical gates (build,
  tests, lint, 80% coverage) as hard blocks, the grader required to run, the Stop hook blocking on
  red, and a non-author human approval on every PR. A change is done when it's **checked**, not when
  it's written.
- **Prevent:** Make **Definition of Checked** the standard, not Definition of Done. No change skips
  the three beats — not even a one-line fix.

## 2. Authors grading themselves

Checking theater: letting the thing that wrote the code also approve it.

- **Symptom:** The "review" is the same agent (or the person who drove it) confirming its own work.
  Approvals are instant, nothing ever bounces back, and the grader and the author are effectively
  the same.
- **Root cause:** You can't trust the thing that wrote the code to vouch for it, and a self-review
  quietly violates that.
- **Fix:** The grader is a **fresh agent that did not write the code**; the human Checker is never
  the change's author. On HIGH risk, a security-reviewer pass precedes a named human sign-off.
- **Prevent:** **The author is never the sole approver** — a hard rule at every team size. The
  Orchestrator/Checker swap makes it real on a small pod; subagents keep the grader separate by
  construction.

## 3. The junk flood

Optimizing for volume. You get churn and duplicate code, not progress.

- **Symptom:** Lots of code appearing fast, but rising churn, near-identical blocks, copy-paste
  everywhere, and refactoring dropping off. It feels productive while the codebase gets worse.
  (GitClear measured copy-paste blocks rising roughly 8×.)
- **Root cause:** Cheap code with no discipline. Junk is the default; volume was never the goal.
- **Fix:** Build against the mess — a grader that catches duplication, standards in CLAUDE.md the
  agent reads every session, and the one-canonical-pattern bound set per spec.
- **Prevent:** Watch **rework/revert rate** and **accepted-as-is rate**. If churn rises, the
  discipline isn't there yet. Never reward volume.

## 4. Counting the wrong things

Tracking PR or line counts. They look great while delivery slows.

- **Symptom:** Dashboards full of green — PR count up, lines up, commits up, leadership happy —
  while actual delivery is flat and people feel faster than they are (METR's gap between feeling and
  reality).
- **Root cause:** An agent inflates these numbers in seconds, and they hide rework. They measure
  output, not delivery.
- **Fix:** Drop lines, commits, and PR count — they're now actively harmful. Measure trust and flow
  instead: accepted-as-is, rework rate, review wait, change-fail rate, time-to-recover.
- **Prevent:** Keep the vanity numbers off every dashboard, and **never put activity metrics in
  client materials** (standard, section 5.5). If a number jumps when an agent runs faster, it isn't
  measuring delivery.

## 5. Cutting the safety net too early

Dropping the old rituals before the checking that replaces them exists. That's how you ship
instability.

- **Symptom:** A team announces "agents do everything now," loosens its process, and then delivery
  stability drops, escaped bugs rise, and releases start breaking. The old rituals are gone and
  nothing replaced them.
- **Root cause:** Velocity, estimation, and sprint planning were also a safety net. Removing them
  without the checking in place leaves the exact gap the DORA numbers warn about.
- **Fix:** Stand up the checking first — automatic gates, a separate grader, hooks that block on
  failure — and only then retire the ceremony the checking has taken over for.
- **Prevent:** The cardinal rule: **install the checking before removing any old ritual.** Never the
  other way around. (In a consulting engagement this is structural — the rails and the ladder exist
  from Phase 3, before the build loop opens at volume.)

## 6. Too many agents on one thing

Splitting tightly connected code across many agents. They clobber each other.

- **Symptom:** Several agents editing the same closely coupled code at once. They overwrite each
  other's changes, the result is tangled, and you've burned tokens for a worse outcome than one
  agent would have produced.
- **Root cause:** Most coding doesn't split cleanly across agents. Parallelizing connected writing
  fragments the work.
- **Fix:** Spread out to explore, line up to commit — many agents for read-only investigation and
  option comparison, **one agent for writing shared code**.
- **Prevent:** Default to a single thread for implementation. Reserve parallel subagents for "look
  into these three options," and isolated worktrees for the rare genuinely independent specs.

## 7. Letting the spec rot

Using the spec once to generate code, then never updating it. It drifts into a lie.

- **Symptom:** The spec says one thing, the code does another. Nobody trusts the spec anymore, so
  people read the code to find the truth — which defeats the point of having a spec.
- **Root cause:** The spec was treated as a throwaway prompt, not the source of truth. Used once and
  abandoned.
- **Fix:** Keep the spec a living, version-controlled file that rides in the PR diff. When behavior
  changes, update the spec first — it's the thing that lasts when the chat history is gone.
- **Prevent:** The Orchestrator owns keeping the spec current; at Retro+ and setup review, treat a
  drifted spec as a defect to fix, not a footnote.

## 8. Pretending review isn't the bottleneck

Cheering individual output while delivery stays flat. The work moved to review.

- **Symptom:** Everyone celebrates how much the agents produce, but things still take as long to
  actually ship. Changes pile up waiting to be checked, review is understaffed, and nobody's
  measuring the queue.
- **Root cause:** The bottleneck relocated from writing to review, and the team is still managing as
  if writing were the constraint.
- **Fix:** Staff review as the real work and make checking a respected job. Cap WIP, and measure
  **review wait** and **security-review wait** separately (security clears slower and would hide in
  an average).
- **Prevent:** Run the standup as a **flow check** ("how long is the review queue?"), not a status
  update. When review wait crosses the tripwire, stop opening streams.

## 9. One review depth for everything

Reading a typo fix as hard as an auth change — or waving everything through. Match the care to the
risk.

- **Symptom:** Either every diff gets the same heavy scrutiny (slow, and reviewers burn out on
  trivia), or everything gets rubber-stamped (and the auth change slips through with the typo fix).
  Risk and review effort are disconnected.
- **Root cause:** A single review depth ignores that risk varies. Trivial and dangerous changes get
  the same treatment.
- **Fix:** The **risk taxonomy** routes it — light checks for LOW, grader-plus-human for MEDIUM, a
  human plus security review for HIGH.
- **Prevent:** Build the tiered checking into the workflow. Assign the tier at triage, record it in
  the spec, and track security-review wait on its own.

---

_The structure that prevents most of these is in [the team](team.md) and the
[build-loop deep-dive](build-loop.md). The terms are in the [glossary](glossary.md). No checking is
just vibe coding — the loop closes it._
