# FAQ

_Honest answers to the questions clients and new pod members actually ask. No overselling. Terms
are defined in the [glossary](glossary.md); the full method is the [standard](../GOLD-STANDARD.md)._

---

## About the method

**How do you trust code that Claude wrote and nobody read line by line?**

You don't trust it because someone read it — there's too much of it for that to scale. You trust it
because it climbed the [checking ladder](cheatsheet.md): mechanical gates (build, tests, lint,
coverage) block it, a separate grader that didn't write it reads the spec and grades the diff, and a
non-author human approves it — with a security pass and a named sign-off on anything HIGH risk. The
human attention is spent where the risk is, not on every line. Checking has to be mostly automatic;
that's the whole design.

**Isn't this just spec-driven development?**

It overlaps, and it borrows the describe-first idea directly. Where it goes further is the
**checking**. Spec-driven work gets you a good description; it doesn't tell you how to trust
high-volume agent output without reading every line. That gap — the [grader](glossary.md), the
ladder, the risk-tiered review — is the half this standard is built around. The spec is one half;
the checking is the other.

**Won't all this checking slow us down?**

Some of it, yes — and that's the point. When code got cheap, the work didn't vanish; it moved to
review and integration. The checking isn't extra work bolted on, it's the work that was always going
to happen, made deliberate and mostly automatic. The alternative is the documented failure mode: cut
the rituals, skip the checking, and delivery gets _less_ stable, not faster.

**How is this different from vibe coding?**

Vibe coding is casual prompting with no checking — fine for a throwaway prototype, dangerous for a
client system. This standard closes the loop: every change, even a small one, runs Intent → Delegate
→ Discern, and nothing is trusted until something other than its author proves it's good. The
one-liner: _no checking is just vibe coding; the loop closes it._

**Do we still run sprints? Does this replace Agile?**

There's no sprint-as-budget here. Sprints existed to ration how much a fixed team of people could
build; when code is cheap that forecast loses its point. What survives is the rhythm: a daily
[flow check](glossary.md), weekly intent triage and Retro+, biweekly client steering. The standard
keeps the parts of Agile that were never about coding speed — short feedback, working software as
the measure, a clear definition of done — and retires the parts that only budgeted scarce human
coding time (story points, velocity).

**How many agents can one person run?**

Nobody has a proven number, and be suspicious of anyone who gives you one. The real limit isn't
headcount, it's how much a person can **review**. The standard caps WIP (default 2 streams per
Orchestrator) and halts new streams when median review wait crosses one working day. Review
capacity is the ceiling, measured — not assumed.

**What's the single most important practice?**

Checking the work with something stronger than a glance, and matching the depth to the risk.
Everything else leans on it. Plenty of teams say review is the bottleneck now; almost none have
built the checking to handle the volume. That gap is the reason the method exists.

## About a client engagement

**Our requirements are always a bit vague. Will this still work?**

It will hurt before it helps, and you should know that going in. A vague spec doesn't get fixed by
the agent — it gets amplified, and the agent builds the wrong thing fast and confidently. That's
where most of the documented AI slowdown comes from. The standard front-loads this: the
[vague-line test](glossary.md) at triage, the decision list Claude generates ("you haven't decided
X, Y, Z"), and a named PO to answer it. "Being clear is the hard part now" isn't a slogan — it's the
job we price and staff for.

**What if we can't commit a full-time product owner?**

Then **proxy mode** applies, and it's decided explicitly at the Phase 0 workshop. Either you commit
a named PO at ≥ 4 hrs/week who answers decision lists within 2 business days, or the Pod Lead makes
product calls on your behalf, logged in a decision log you ratify at each steering. What doesn't
work is leaving decisions unanswered — that's what stalls agents and produces the wrong thing.

**Where does our code and data go? Who holds the keys?**

By default **you** procure Anthropic access under your own agreement (with the standard
no-training-on-API-data terms), keys live in your Key Vault, and the pod works on your seats — your
contract, your audit trail. The kit includes a one-page data-flow brief for your security team:
what goes to the API (repo code context, specs), what doesn't (we tag genuinely sensitive material
out of agent context), where keys live, who sees usage. A high-compliance path runs Claude inside
your own Azure tenant (standard, section 8).

**What will we actually see from you week to week?**

Working software, not activity reports. Biweekly steering is a live demo from your dev environment
plus an outcome scorecard — your success metric, the DORA stability pair, the accepted-as-is trend —
and the decisions we need from you. A 5-bullet async summary in between. **No PR counts, no "AI
productivity" claims, ever.** Demos and outcomes only.

**Is this only for greenfield code?**

No — and the evidence cuts the other way. The flashy "AI made me 55% faster" results were fresh,
self-contained tasks with no integration. The documented slowdowns happened on old, tangled,
mature projects — which is where most real client code lives. The checking ladder and the risk
tiers are built for exactly that harder setting.

**Do you have to use Claude / this specific tooling?**

The method is tool-neutral. The standard describes the concept; the .NET/Azure stack, the
orchestration plugin, and the CI system named in it are _an example of how we implement it today_,
and the worked examples are where the specific commands appear. Swap any of them out and the method
still holds. We use Claude Code because its features line up almost one-to-one with the beats —
plan mode, CLAUDE.md, skills, hooks, subagents, the ladder.

**What happens when the engagement ends — are we stuck depending on you?**

The opposite is the explicit goal. The harness lives in **your** repo from day one, so handoff is
mostly revoking our access. Phase C (Close & Transfer) doesn't end until your team has run a real
spec end-to-end — triage, spec, delegate, grade, merge, deploy — without us driving, and your named
Setup Owner has merged harness changes themselves (standard, section 13). The capability transfer is
a priced deliverable, not a favor.

**Can we keep our CI/CD and DORA tracking?**

Yes, and you'll lean on them more. Deploy frequency, lead time, change-fail rate, and time-to-recover
are exactly the flow and stability numbers the standard asks you to watch. They carry straight over.

**What metrics do you stop tracking?**

Story points and velocity (they forecast a capacity that no longer limits us), and lines, commits,
and PR count (now actively harmful — an agent inflates them in seconds and they hide rework). They
look great while delivery slows, which is exactly why they mislead.

---

_Still have a term you don't recognize? The [glossary](glossary.md) has it. Want the 20-second
shape of the method? The [loop cheat-sheet](cheatsheet.md)._
