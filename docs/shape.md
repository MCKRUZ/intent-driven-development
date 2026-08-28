# The shape of an engagement

_Eight decisions, each signed by a named person with evidence attached, arranged around one
continuous build loop. The order is real; the dates are not fixed; any decision can be reopened
through a route that leaves a record. The three-minute summary for a sponsor is
[the three-minute version](sponsor.md); the routes back are
[what happens when things change](when-things-change.md)._

---

## The drawing

![The shape of an engagement — eight signed decisions around one continuous loop](assets/shape-of-an-engagement.png)

Four decisions open the engagement, signed in order. The middle is a loop, not a phase: Intent →
Delegate → Discern, once per change, for 8–16 weeks, every merge checked by a machine and by a
non-author. Four decisions close it. The dashed routes are where the loop reaches back into a
signed decision. [Open the full-resolution sheet](assets/shape-of-an-engagement-2x.png).

Harbor Mutual, the fictional regional insurer the standard uses as its worked example, runs this
whole shape in [one engagement, start to finish](journey.md). This page is the shape on its own.

## The eight decisions

For each: the decision, the phase it closes, who signs, what evidence sits under the signature,
and what reopens it later.

### OPEN · 1 · Problem framed

- **Closes:** Discovery ([deep-dive](phase-0-discovery.md))
- **Who signs:** The sponsor, on the problem and the metric; the sponsor and the candidate
  product owner, on the PO decision; the sponsor with security, on whose AI account and keys the
  pod works with.
- **Evidence:** The problem statement in the client's own words, human-authored. One success
  metric and the place it will be read from, verified with the data owner. A named product owner
  at 4 or more hours a week, or proxy mode acknowledged. The tooling decision, with a one-page
  data-flow brief for the security team.
- **What reopens it:** Changing the problem, the metric, the PO mode or the tooling. It is the
  most expensive reopening there is, because billing maps to gates, so it is a SOW conversation at
  steering. It does happen.

### OPEN · 2 · Baseline signed

- **Closes:** Requirements ([deep-dive](phase-1-requirements.md))
- **Who signs:** The product owner; the Pod Lead enforces the definition of ready on every story
  before it gets there.
- **Evidence:** Epics and stories drafted by the agent and owned by humans. Non-functional
  requirements that each say where they will be measured. The decision list ("you haven't decided
  X") generated, and every item answered on the two-business-day clock.
- **What reopens it:** A requirement changing after signature. It is revised in place with an
  owner, a reason and a clock; the affected downstream artifacts are listed; this phase's gate is
  re-run so the change is visible rather than absorbed. When merged work drifts from a
  requirement, the reverse runs: the merged change proposes the upstream edit and a person
  confirms it.

### OPEN · 3 · Architecture chosen

- **Closes:** Design ([deep-dive](phase-2-design.md))
- **Who signs:** A person picks from the options; the Architect signs each decision record; the
  client's lead engineer co-signs, because they will live with it after handoff.
- **Evidence:** Two or three architectures with concrete trade-offs. Signed decision records
  (ADRs). A threat model and a plan for proving the non-functional requirements. Unknowns are not
  guessed; they are spiked.
- **What reopens it:** A spike disproving an assumption the design rests on. The revision goes
  through as a HIGH-risk change with a named signature; the old record is marked superseded,
  never edited away.

### OPEN · 4 · Factory proven

- **Closes:** Foundation ([deep-dive](phase-3-foundation.md))
- **Who signs:** The Setup Owner, with a deputy reviewing every harness change (the Setup Owner
  is never sole approver of their own foundation work); the client's platform engineer reviews
  the pipeline they will operate after we leave; the sponsor sees the exit demo.
- **Evidence:** The rails live and branch protection applied. The thinnest end-to-end slice, four
  small pieces of work, ridden through the whole loop into the client's dev environment. One real
  feature running there.
- **What reopens it:** Nothing reopens the phase. Every later pipeline or infrastructure change is
  a HIGH-risk change riding the loop, with human review and no exceptions.

### CLOSE · 5 · Docs proven by use

- **Closes:** Documentation ([deep-dive](phase-7-documentation.md))
- **Who signs:** Someone who has never seen the system, on the record of following the README
  cold; an operations engineer on the runbook walk; the lead engineer co-signs any new decision
  records the drift catalog produced.
- **Evidence:** The README, API docs and runbook drafted by the agent from the code and the
  specs, then verified by use, not by reading: a stranger deploys it from the runbook.
- **What reopens it:** Nothing reopens the phase. Any later change that alters behaviour carries
  its documentation in the same change; a stale document is a defect, not a reason to rerun
  Documentation.

### CLOSE · 6 · Go / no-go

- **Closes:** Deployment ([deep-dive](phase-8-deployment.md))
- **Who signs:** A named approver, always a person, never automatic; the sponsor is informed and
  asked. Promotion beyond dev cannot run without a configured approver.
- **Evidence:** A rollback rehearsed by the client's own operators (deploy, roll back, redeploy).
  Release notes drafted from what merged. Smoke-test results. The secrets-rotation record
  attached.
- **What reopens it:** A failed rehearsal: it becomes a piece of work in the loop and the
  rehearsal is run again before anyone goes live. Going live ahead of the people who will run the
  system is how a successful deploy becomes next month's incident, so the deployment moves, not
  the rehearsal.

### CLOSE · 7 · Healthy in production

- **Closes:** Monitoring ([deep-dive](phase-9-monitoring.md))
- **Who signs:** The Pod Lead and the client's operations team, who co-author what "healthy"
  means and confirm the thresholds against real baseline data.
- **Evidence:** Alerts modelled from measured baselines rather than guesses. A drill run from the
  playbook, by the people who will answer the pager. The engagement's retrospective.
- **What reopens it:** An alert that fires more than once a week without action: raise the
  threshold or delete the alert. Thresholds are revised the same way they were set, with
  operations, against data.

### CLOSE · 8 · Client runs it alone

- **Closes:** Close & Transfer ([deep-dive](phase-c-close.md))
- **Who signs:** The client's named Setup Owner, with a deputy; the sponsor, at the close
  steering.
- **Evidence:** One real change, end to end, driven by the client's own engineers without us. A
  harness audit showing nothing only we understand. Our access revoked, confirmed against the
  client's audit trail.
- **What reopens it:** Nothing on our side; this signature ends the engagement. What the
  engagement taught goes back into the standard through the harvest retrospective.

## Why it isn't a line

**Gates sit on decisions, not dates.** A gate is an automated battery of checks followed by a
named human's signature. The battery reports whether you may advance; the person decides whether
you do. Because billing milestones map to those gates and not to calendar dates, a phase that
needs more time takes it, and a gate that fails simply has not been passed yet.

**The phases overlap.** In the opening, the Setup Owner's enablement work runs ahead while
requirements and design close, which is why Discovery through Foundation is planned as 4–6 weeks
in total rather than as four sequential blocks. The signatures are ordered; the work that earns
them is not.

**The middle is not phased.** A traditional lifecycle phases the middle too, with separate
implementation, quality and testing stages. This standard deliberately doesn't. Checking a large
batch of work only after it has all been built is the failure mode the delivery research warns
about, so checking happens per change, inside the loop, never as a later phase. The
[build loop](build-loop.md) is the whole middle.

## The checking ladder

Inside the loop, every change is proven by something other than its author before it merges. The
proof climbs five rungs; each catches what the one below cannot, and the risk tier decides how high
a change climbs.

| Rung | The check | What it catches that the rung below can't |
|---|---|---|
| 1 | The done-rule in the harness | Sets the bar ("done means checked, not typed"); persuasion only, it enforces nothing by itself. |
| 2 | The agent re-checks each turn | The agent's own mechanical slips: the broken import, the test it broke two steps back. |
| 3 | The blocking Stop hook | The agent declaring itself done anyway; it cannot finish with red tests or a broken build. A hook enforces the tests that exist; it cannot enforce a test nobody wrote, and on a bug fix the repro-gate asks the next question down: would this test have caught it? |
| 4 | The separate grader | The hole the author was blind to. It grades check-by-check against the spec, not against the tests, so it catches the case the author never thought to test. It runs on the strongest model available; independence comes from not having written the code, capability is a separate axis. |
| 5 | The human / security gate | The judgment calls no machine should own: the risk acceptance, the product call, the security sign-off on a HIGH change. |

The four routes back into a signed decision, with owners, records and costs, are on
[what happens when things change](when-things-change.md). The loop itself, day by day, is the
[build loop](build-loop.md).
