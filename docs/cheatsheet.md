# The Loop — Wall Card

_Scannable in 20 seconds. The cycle every piece of work runs, from a one-line fix to a whole
feature. Print it, pin it. The full method is in the [standard](../GOLD-STANDARD.md); the
[build-loop deep-dive](build-loop.md) is the long version of this card._

---

## Intent → Delegate → Discern

```
  INTENT             DELEGATE            DISCERN
  ┌────────┐         ┌────────┐          ┌─────────┐
  │ decide │────────▶│  plan  │─────────▶│  check  │
  │ write  │         │ build  │          │  merge  │
  └────────┘         └────────┘          └─────────┘
   you own this       agent builds,       gates + a human
   (the spec)         you set the box     own the verdict
```

| Beat | Who owns it | The two moves |
| --- | --- | --- |
| **Intent** | Human (Pod Lead owns quality; PO owns the call) | **decide** what you want, then **write** it as a spec you can test |
| **Delegate** | Agent builds; Orchestrator sets the bounds | agent **plans** (you approve before code), then **builds** and self-checks |
| **Discern** | Gates check; a non-author human approves | **check** against the spec, then **merge** without breaking `main` |

_Discern just means working out whether the work is actually good before anyone trusts it._

---

## The checking ladder (quick → thorough)

A change climbs as far as its risk demands. Each rung is harder to skip than the last.

1. A **rule in CLAUDE.md** about what "done" means.
2. A **check that re-runs every turn** to confirm it.
3. A **blocking Stop hook** — won't let the agent finish while tests are red. Not optional, not
   persuadable.
4. A **separate grader** that reads the spec and grades the diff. The author never grades its own
   work.
5. A **human gate** for HIGH risk — a security-reviewer pass first, then a named sign-off in the PR.

Mechanical gates (build, tests, lint, 80% coverage) block. The grader runs but advises. The human
Checker decides. **Machines gate the mechanical; humans own the judgment.**

---

## Risk sets the leash

| Tier | Examples | Review |
| --- | --- | --- |
| **HIGH** | auth, payments, PII, migrations, public API / pipeline / IaC, prompt-model-tool changes | full ladder + security pass + named human sign-off |
| **MEDIUM** | new business logic, external integrations, shared services | grader + human Checker |
| **LOW** | UI in existing patterns, copy, internal tooling, additive CRUD | lighter review; grader + mechanical gates still run |

Read a typo fix lightly. Read an auth change hard. Challenges to a tier escalate **up**, never down.

---

## Do

- Write the goal as a concrete, testable spec **before** any code exists.
- Set the box the agent works in: scope, the one pattern to reuse, one agent or several.
- Run every change through all three beats — even the one-liners.
- Match review depth to the risk tier.
- Let a non-author grade the work; keep the spec file in the PR diff.

## Don't

- Don't ship what nobody checked. That's vibe coding to prod.
- Don't let the author approve its own work.
- Don't split tightly coupled code across many agents — they clobber each other.
- Don't open more streams than the pod can review (watch median review wait).
- Don't count PRs, lines, or velocity. They go up while delivery stays flat.

---

_No checking is just vibe coding. The loop closes it. → Next: the
[build-loop deep-dive](build-loop.md)._
