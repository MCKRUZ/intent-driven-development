# Phase C Worked Example: Harbor Mutual

The continuation of [the Phase 9 example](phase-9-example.md), companion to
[the Phase C deep-dive](phase-c-close.md), and the end of the Harbor Mutual story. The system
is live and observable; Harbor's operators hold the watch; the retrospective is written and the
harvest list is waiting. Three weeks — Monday 2026-08-10 to Friday 2026-08-28 — remain, and
they exist to prove one sentence: **Harbor can run all of this without us.**

The two arcs to watch: **Ines Roy**, who in July had never opened the repo and cold-verified
the README as a stranger, closes the engagement by orchestrating a HIGH-risk spec through the
loop. And **Wes Carter**, who co-signed the first ADR back in March, finishes as what the Phase
2 example promised he would become: Harbor's Setup Owner.

## What Phase C received

Harbor Mutual — a fictional regional insurer — hired a five-person pod to rebuild how
property-insurance claims get reported and decided. A claim took a median of **11.4 days** from
FNOL (first notice of loss) to a coverage decision; the target was **5 days or less**. The code
was done weeks ago. The system has been live since 7/23, observable, drilled, and
retrospected, and Harbor's operators hold the watch. Phase C does not start from a blank page —
it starts from a whole engagement's record and a running system, and it exists to prove one
sentence: **Harbor can run all of this without us.**

**Inherited from Phase 9 — the record, plus a system already in Harbor's hands:**

- `close-handoff.md` — the package Phase 9 assembled for this phase.
- `project-retrospective.md` — the harvest list waiting to be opened as a PR.
- The **running system** — live since 7/23.
- The **harness** — Harbor's since Foundation.

**Four questions, and deliberately nothing else.** Everything Phase C does answers exactly four
questions. New features are out of scope unless they are the *vehicle* — the specs run this
phase are real work from Harbor's own backlog, chosen because the close gate must run on
something that matters.

1. **Can their people run the loop?**
2. **Is the harness fully theirs?**
3. **Is the record complete and delivered?**
4. **Did we leave cleanly — and did the standard learn?**

**The two arcs to watch.** **Ines Roy** is the one to watch: in July she had never opened the
repo and cold-verified the README as a stranger; she closes the engagement by orchestrating a
HIGH-risk spec through the loop, solo. And **Wes Carter**, who co-signed the first ADR back in
March, finishes as what the Phase 2 example promised he would become: Harbor's Setup Owner —
proven by his merge history, not the org chart.

> **The entry bar, confirmed at the Step 0 HITL gate:** Client engineers named and available to
> orchestrate real specs — at least three with pod Checkers, then one solo. The Setup Owner
> named, ready to merge. The training workstream was priced into the SOW back in Phase 0.

**The cast:**

| Side              | Who                                                                                                                                                                                                                                    |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Our pod**       | Maya Chen (Pod Lead — the transfer is hers) · Rob Feld (Setup Owner — handing over; walks the audit and the revocation) · Jonah Kim & Sara Whitfield (Checkers only this phase, then silent observers) · Nadia Brooks (Quality Engineer — owns and records the gate evidence). |
| **Harbor Mutual** | Wes Carter (Harbor's Setup Owner as of this phase — merges the audit fixes and one change of his own) · Ines Roy (engineer — Orchestrator now; drives the solo close-gate spec) · Tom Reilly (platform engineer — Wes's harness deputy; executes the production deploy) · Luis Ortega (product owner — triage is his room now) · Dan Kowalski (IT security — signs the HIGH sign-off and the revocation) · Priti Shah (data lead — inherits the outcomes dashboard) · Karen Voss (sponsor — signs the close). |

**The ID codes, decoded.** Phase C leans on just two — the sequence has been running since
Foundation:

| Prefix     | Means                                                        | Born in       | Example here                                                          |
| ---------- | ----------------------------------------------------------- | ------------- | -------------------------------------------------------------------- |
| `NNNN`     | A spec — one change in one file, riding the full loop        | Foundation on | Build closed at 0044; the close phases continued 0045–0046; this phase adds 0047–0050 |
| `ADR-NNN`  | An architecture decision record — a signed choice           | Phase 2 on    | Complete through ADR-013, none open                                  |

The specs are the vehicle for the whole phase: 0047, 0048 and 0050 are the shadow-flip specs;
**0049** — decommission the legacy intake fallback — is the solo close-gate spec, HIGH tier,
real consequences, due 8/22.

## The procedure, week by week

Close is eight numbered steps in `claude-code-sdlc` and three working weeks in this standard —
the same close seen twice. Unlike the opening phases, this one runs on a calendar of **weeks,
not days**: a week to flip the roles, a week for the gate, a week to leave. Below they're
braided: what the tool runs, the human ritual the tool cannot perform, and the file each week
leaves behind.

**Reading the markers.** `▪` a command does it — and writes the file · `▸` a person does it —
and it is recorded · `⚠` a person does it — and nothing records it.

### Week 1 · Mon 8/10–Fri 8/14 — flip the roles: the client drives, the pod only checks
*plugin Steps 0–2 · their hands, our eyes*

**Tooling —** the Step 0 HITL gate (`AskUserQuestion`) · `/sdlc-status` → the flow-check queue,
typed by Harbor · Agent(`Explore`) → the read-only harness sweep · `▸` human decision — who
orchestrates, which specs are real.

**Artifacts out —** `⚠` `close-gate-evidence.md` (the shadow-flip section) · `⚠`
`harness-audit.md` (findings and fixes) · `⚠` `access-revocation-checklist.md` (drafted early,
from every grant).

The transfer opens by reversing the roles that built the project. A blocking human gate first:
Claude asks whether client engineers are named and available, whether the Setup Owner is ready
to merge, and which real backlog items are candidates — nothing begins until a human confirms
the transfer is real. Then the **shadow flip**: Harbor's engineers take the Orchestrator seat
on at least three real specs, and the pod serves only as Checkers, coaching by question, never
by taking the keyboard. In parallel, a read-only agent sweeps the repo for anything that would
strand the client if the pod vanished tonight.

> **At Harbor:** Three real specs ride the loop with Harbor Orchestrators and pod Checkers, the
> bar unchanged: **0047** (adjuster queue saved filters, Ines), **0048** (intake-supervisor
> daily digest, Ines), **0050** (claims-search timeout messaging, Wes). Jonah and Sara coach
> only by question and **log every place they wanted the keyboard** — each one a transfer gap
> with a name. The audit sweep returns only **two** findings after a five-month engagement,
> because Foundation's open-adaptation habit made every harness change a PR Wes had already read.

> ⚠ **The gap:** The shadow-flip record and the audit findings are *human work* — no command
> writes them. But watch where they land: `close-gate-evidence.md` and `harness-audit.md` are
> **required artifacts the gate checks for**. The plugin makes the human ritual leave a file and
> refuses to close without it. Hold that thought for the ledger.

### Week 2 · Mon 8/17–Fri 8/21 — one real change, solo, with the pod silent in the room
*plugin Step 3 · the close gate*

**Tooling —** *none from our side — Harbor types everything; the pod is silent* · `risk:high` →
`security.yml` → the `security-reviewer` agent.

**Artifacts out —** `⚠` `close-gate-evidence.md` (the solo observation, names and timestamps) ·
`⚠` `harness-audit.md` (the owner's own-change evidence) · `▸` the verdict — a human call, PASS
or re-run.

The phase's defining test. One real spec — real risk tier, real consequences — runs the loop
end to end with **nobody from the pod driving**: their triage, their spec, their bounds, their
plan approval, their Checker, their merge, the automatic deploy. The pod observes the way the
Quality Engineer observed the cold runs in Documentation and Deployment: present, silent,
taking notes. There is **no plugin command from the pod's side** — that is the test. A run that
needs help is void; the gap the help revealed is the finding, fixed and re-run on a different
real spec. This week the client Setup Owner also ships one harness change *of their own*.

> **At Harbor:** Spec **0049** — decommission the legacy intake fallback, tier **HIGH**, due
> 8/22. On Thursday 8/20 Ines orchestrates; the agent's plan drifts toward editing
> `deploy-dev.yml`, a gated path, and the hook **blocks the edit**. Ines escalates to Wes
> exactly as the rules prescribe; it ships as its own harness PR. Grader PASS, Wes the
> non-author Checker, Dan's HIGH sign-off, merged, production on Harbor's go/no-go — the
> fallback dark two days early. Wes ships an onboarding bootstrap skill of his own; Tom is named
> his harness deputy. **The wobble was the win**: the rails caught the drift and a Harbor
> engineer answered with the right judgment, unprompted.

> ⚠ **The gap** (the one place the plugin already does what this rewrite asks): `close-gate-evidence.md`
> is the positive example. Everywhere else a human ritual — a spike, a threat review — happens
> and leaves no receipt the gate checks. Here the close gate is a pure human ritual, and the
> plugin **requires** its receipt: the file is in `artifacts.required`, and `check_gates.py`
> refuses to close until it exists, is non-empty, and carries no placeholder. The ritual leaves
> a file the gate reads. That is the pattern the whole rewrite argues for.

### Week 3 · Mon 8/24–Fri 8/28 — hand over the record, revoke access, feed the standard, and go
*plugin Steps 4–8 · the clean exit*

**Tooling —** `generate_handoff_report.py` → `final-handoff-report.md` · Agent(`Explore`) →
fill the `[Fill:…]` slots; draft the harvest · `/sdlc-phase-report` → `generate_phase_report.py`
· `/visual-explainer` → `.sdlc/reports/close-visual.html` · `/sdlc-gate` → `check_gates.py`.

**Artifacts out —** `▪` `final-handoff-report.md` · `▪` `close-visual.html` · `▪`
`close-report.html` · `⚠` `access-revocation-checklist.md` (executed and signed) · `⚠`
`outcomes-dashboard-handover.md` · `⚠` the harvest PR + retro file (in the standard repo).

The last week is execution, not discovery. The record hands over into Harbor's own tooling: a
script drafts the final handoff report from the engagement's records, an agent fills the
narrative slots, and every phase report and the outcomes dashboard move to client ownership.
Access revokes on the checklist drafted in week one — every seat, token, and role removed and
**confirmed against Harbor's audit trail**. The harvest PR opens against the firm's own
standard repo, and a retro file is written into it. The gate runs, the report renders, and a
named human on each side signs the close.

> **At Harbor:** Every phase report ships; the outcomes dashboard is re-pointed to Priti with
> the **October** quarter-read on Harbor's calendar, caveats intact; the debt log sits in
> Harbor's tracker with Harbor owners. On Wednesday 8/26 Rob and Dan walk the revocation item by
> item, audit-confirmed, Dan signs — bookended with Phase 8's secrets rotation. The harvest PR
> opens against `MCKRUZ/delivery-standard` with four patterns, and `retros/2026-harbor-mutual.md`
> is written. Friday 8/28 the close steering: Karen gets the record and the 4.2-day read; the
> final milestone bills. The engagement ends.

> ⚠ **The gap** (where even Close reverts to unchecked human work): the exit gate *requires* the
> harvest PR opened and the retro file written — but neither lives in `.sdlc/`. They land in the
> standard repo, which `check_gates.py` never walks, and `harvest-pr-notes.md` is only optional.
> The same is true of the outcomes-dashboard handover: required to close, but its artifact is
> optional, so nothing verifies it. Three of Phase C's exit conditions have no automated eyes on
> them at all.

## What Phase C produced

The whole output of the close, named. Blue rows are written by a command. **Green rows are the
point of this page** — rituals only a person can perform, which the harness nonetheless
*requires to leave a file*, and which the gate then checks. Nobody's memory is load-bearing.
Amber rows are the work that still evaporates when the meeting ends.

Phase C is the only phase in the engagement that does this. Everywhere else, a threat review or
a spike or a cold-checkout test happens, matters, and leaves nothing behind. Here, the client's
engineer ships one real change alone with the pod silent in the room — and
`close-gate-evidence.md` records that it happened. **That is the pattern the other eight phases
are missing.**

**Marker key.** `▪` a command does it — and writes the file · `▸` a person does it — and it is
recorded · `⚠` a person does it — and nothing records it.

| Artifact | What it actually is | Written by | Signed by | Lives at | Feeds |
| -------- | ------------------- | ---------- | --------- | -------- | ----- |
| ▪ `final-handoff-report.md` | The engagement record in one place: every phase gate and sign-off, the phase-report index, the metrics history, the debt log, and who Harbor calls now | `generate_handoff_report.py` drafts; Explore agent + Pod Lead enrich | Pod Lead | `.sdlc/artifacts/close/` | Harbor's incoming team |
| ▪ `close-report.html` | The gate result and artifact inventory, self-contained — the document the sponsor reads before the final sign-off | `generate_phase_report.py` (via `/sdlc-gate`) | — | `.sdlc/reports/` | The close steering |
| ▪ `close-visual.html` | The transfer scorecard, the audit findings, the revocation tracker and the harvest summary, rendered | `/visual-explainer` | — | `.sdlc/reports/` | The close steering |
| ▸ `close-gate-evidence.md` | The shadow-flip record (≥3 specs) and the solo close-gate observation: names, timestamps, every stall and guardrail event, the merge that deployed, the verdict | **Quality Engineer, by hand** | Pod Lead | `.sdlc/artifacts/close/` — **required & gate-checked** | The close gate itself |
| ▸ `harness-audit.md` | Every transfer-risk finding, its fix and the client Setup Owner's merge, the owner's own change, and the "ask the pod" zero result | **Explore sweeps; Setup Owner walks and writes** | client Setup Owner | `.sdlc/artifacts/close/` — **required & gate-checked** | Harbor's operation of the harness |
| ▸ `access-revocation-checklist.md` | Every pod credential, its removal date, the audit-trail confirmation, and the production-secret rotation | **Setup Owner + client security, by hand** | client security | `.sdlc/artifacts/close/` — **required & gate-checked** | The clean exit |
| ⚠ `outcomes-dashboard-handover.md` | The dashboard re-pointed to client ownership, caveats intact, the quarter-read date on their calendar | **QE + client data lead** | Client | optional artifact — the gate never checks it | Harbor's own quarterly read |
| ⚠ harvest PR + `harvest-pr-notes.md` | The generalized skills, corrected templates, and repeatable patterns sent home to the standard, client specifics stripped | **Explore drafts; the pod opens the PR** | the standard's deputy | a PR in another repo — the gate can't see it | The next engagement |
| ⚠ retro file (`retros/….md`) | One file recording what this engagement changed about the standard and why | **Pod Lead, by hand** | the standard's owner | delivery-standard repo — outside `.sdlc/`, unchecked | The standard's compounding memory |

> ⚠ **The gap** (read the amber rows again — and notice which kind they are): six of Phase C's
> nine outputs are human-authored, not tool-written. Here is the difference that matters, and it
> is the whole argument of this rewrite: three of them — the **close-gate evidence**, the
> **harness audit**, and the **revocation checklist** — are required artifacts with a real path
> that `check_gates.py` refuses to close without. The plugin makes the human ritual leave a
> file. That is exactly what Phase 2's spikes and threat models should do and don't. The *other*
> three — the dashboard handover, the harvest PR, and the retro file — are the true gap:
> required to close, but the dashboard artifact is optional and the harvest lands in another
> repo the gate never walks. **Human work is not the problem. Human work without a receipt is —
> and Close is the one phase that mostly gets this right.**

Deliberately **not** produced in Phase C: a transition-services annex that quietly keeps the
pod on retainer — ongoing help is a new agreement made in daylight, with its own Phase 0 — and
any "final improvements" to Harbor's code outside the loop. The loop is theirs now, and so is
every change.

## The close gate — one real change, solo, observed

The engagement's last and most important gate, reproduced whole. The close-gate spec was real,
with a date attached: **0049 — decommission the legacy intake fallback**, due at day 30 of the
rollout (8/22). Luis confirmed at triage the fallback triggers had never fired in thirty days
of production; the room debated the tier and landed it **HIGH** — re-standing the legacy intake
would take days, and hard-to-undo is the definition. Nobody from the pod was in the discussion.
**The tier debate itself was the judgment transferring.**

On Thursday 8/20 Ines orchestrated: plan mode, bounds, the agent built. The wobble the
observers were waiting for arrived on schedule — the agent's plan drifted toward editing the
deploy workflow YAML to remove the fallback wiring, a gated path. The hook blocked the edit;
Ines stopped, took the workflow change to Wes, and it shipped as its own reviewed harness PR —
exactly the escalation the rules prescribe, executed by someone who learned those rules eight
weeks earlier. The pod, in the room, said nothing. Stalls are data; help voids the run.

```
Spec 0049 — decommission legacy intake fallback (HIGH)
Run: Thursday 2026-08-20. Observers: N. Brooks (record), M. Chen,
J. Kim, S. Whitfield. Pod participation: none.

09:05  Triage (Luis, Wes, Ines, Tom): fallback triggers 0 fires in 30
       days; tier debated, set HIGH (hard to undo). Spec finalized
       against Definition of Ready by Ines.
10:20  Plan mode: agent plan reviewed by Ines; scope bounded to intake
       routing + tests; deploy workflow change identified in plan as
       OUT of agent scope (gated path).
11:35  PreToolUse hook BLOCKED agent edit of .github/workflows/
       deploy-dev.yml. Ines halted, escalated to Wes per CLAUDE.md
       gated-path rule. Workflow change shipped as separate harness PR
       (Wes author, Tom deputy review). No pod involvement.
14:10  Build complete; Stop hook green; PR opened; risk:high label →
       security.yml → security-reviewer agent pass.
15:25  Grader verdict posted: PASS, all 5 acceptance checks mapped.
15:50  Non-author Checker: Wes. Named HIGH sign-off: D. Kowalski.
16:15  Merged. deploy-dev green. Test promotion smoke green.
17:00  Production promotion on Harbor go/no-go (their roles, their
       record; Tom executed). Fallback dark, two days ahead of its
       day-30 deadline.

VERDICT: Close gate PASSED — real spec, end to end, observed,
unassisted. One guardrail event (the blocked gated-path edit),
handled correctly by the client team without prompting.
```

The gate's best moment was the blocked edit — not because the agent drifted, but because the
rails caught it and a Harbor engineer responded with the right judgment, unprompted. A toy spec
would have proven nothing; 0049 fired the full HIGH path with zero pod hands. Mechanics
transfer in documents; judgment only shows up under observation. And this whole log is not a
nicety — it is `close-gate-evidence.md`, the required artifact the gate reads before it lets the
engagement close. The ritual and its receipt are the same object.

## The harness audit — and the owner it proved

The harness audit ran in parallel with the shadow flip: a read-only sweep plus Rob's walk of
every skill and hook, asking one question — *could Harbor operate this if the pod vanished
tonight?* After a five-month engagement the sweep found only **two** things, because the
open-adaptation habit from Foundation made every harness change a reviewed PR Wes could already
see. The point of the audit is not the findings; it is who *merged* them.

| # | Finding | Why it would have stranded Harbor | Fix — merged by Wes |
| - | ------- | --------------------------------- | ------------------- |
| 1 | The grader agent's prompt said "review per MCKRUZ standards" — a reference only the pod could resolve | A future Harbor engineer tuning the grader has no idea what the phrase binds to | Prompt rewritten to state the actual rules inline; PR merged by Wes |
| 2 | The stop-gate hook resolved a lint configuration from a path that existed on pod machines but not in the repo | The hook silently weakens the day Harbor runs it on a fresh machine | Configuration pinned into the repo; hook path repo-relative; PR merged by Wes |

**The test for a real owner: merge history, not the org chart.** "Harbor has a Setup Owner" is
a claim until it becomes a git log. Wes didn't just merge the two audit fixes — he shipped a
harness change **of his own**: an onboarding bootstrap skill for new Harbor engineers, born
from Ines's step-4 stall during [the Phase 7 cold README checkout](phase-7-example.md), turning
a bad day into a permanent practice. His PR, no plugin command — Wes deciding the harness needed
something and shipping it through the same loop everyone uses. "Ask the pod" must return
**zero** results before the gate. It did.

**The both-eyes rule transfers too.** Tom Reilly is named Wes's harness deputy — a Harbor
engineer who reviews the Setup Owner's own harness changes, the way the pod's deputy reviewed
the pod's. No role without a deputy was the rule that protected the pod from a single point of
failure; it survives the pod's departure. A Setup Owner named in a deck but who never merged
anything is a label. Wes is an owner because the git log says so.

## Capability is paid — and the clean exit

The ability Harbor now holds was not a farewell favor tossed in at the end. The training
workstream was **priced into the SOW back in Phase 0**, and the shadow flip and the close gate
are that capability being delivered and proven, on the clock, against real work. The specs run
this phase were real backlog items, not exercises — which is the only reason driving them proved
anything. Ines went from a stranger who cold-verified the README in July to the Orchestrator of
a HIGH-risk decommission in August. That distance is what the SOW paid for, and the close gate
is the receipt. A follow-on, if Harbor wants one, is a new agreement made in daylight with its
own Phase 0 — not a transition-services annex that quietly keeps the pod on retainer.

A close that leaves the client able but the pod still holding keys is only half done — so the
same week proves the other half. On Wednesday 8/26 every pod seat, token, repo permission,
environment role, and vault access was walked as a checklist by Rob and Dan, item by item, then
**confirmed against Harbor's audit trail**. By end of day the pod provably could not reach
production. The checklist wasn't improvised on the last day — Rob drafted it in week one from
everything the engagement was ever granted, so week three was execution, not archaeology.

> **At Harbor:** Dan signed the record. It went in the close packet next to the secrets rotation
> from Phase 8 — the engagement's bookends: **we never held production secrets, and now we hold
> nothing at all.**

> ⚠ **The traps to name out loud:** "We'll sort the seats out next sprint" un-revokes the whole
> thing — revocation is a dated, security-signed, audit-confirmed gate item or it didn't happen.
> And "before you go, could you just…" burns the calendar the close needs; hypercare reflexes
> that outlive their window un-transfer the engagement one free answer at a time. Harbor got a
> clean break: who they call now is their own team.

## The tooling behind this phase

The [Phase C deep-dive](phase-c-close.md) describes this work generically. What actually ran —
typed, from this phase on, by Harbor's hands:

| What got produced | How |
| ----------------- | --- |
| Shadow-flip specs (0047, 0048, 0050) | Harbor Orchestrators through the full loop; pod as Checkers only; coaching by question, never by keyboard |
| Harness audit | `/sdlc` → the `Explore` agent's read-only sweep + Rob's manual walk; both findings fixed by PRs **Wes** merged |
| Wes's own harness change | No plugin command — the onboarding bootstrap skill, his PR, Tom's deputy review |
| The close-gate run (0049) | Harbor end to end: their triage, plan mode, the hook blocking the gated path, `security.yml` on `risk:high` → the `security-reviewer` agent, Dan's sign-off, their go/no-go |
| Final report bundle | `/sdlc-phase-report` → `generate_phase_report.py`, every phase record 0 through C — typed by Wes |
| Close-steering record | `/visual-explainer` → the engagement record and the gate evidence for Karen |
| Access revocation | No plugin command — Rob and Dan, checklist item by item, confirmed against Harbor's audit trail |
| The harvest | No plugin command — the PR against our own standard repo, plus `retros/2026-harbor-mutual.md` |

## What Harbor keeps

There is no next phase — only what outlives the pod. Every other phase ends by handing the next
one a package. Close ends differently: there is **no next phase and no handoff out**. What
crosses the boundary here is not a handoff — it is everything that stays, now that the people
who built it are gone. The test of the whole engagement is that this list runs without them.

**Stays with Harbor — the operating system, not the operators:** the harness (`CLAUDE.md`,
`.claude/`, the agents & skills) · `specs/0001…0050` · `adr-registry.md` (ADR-001…013) ·
`RUNBOOK.md` · the outcomes dashboard + metrics history · the running system & its drilled
alerts · `final-handoff-report.md`.

**The decision history is the part that compounds.** The harness is the operating system — it
was Harbor's since Foundation, and it ran the project, not the people leaving. But the piece
that quietly matters most is `adr-registry.md`: every architectural choice from March onward,
ADR-001 through ADR-013, with the rejected options and their reasons still attached. When a
Harbor engineer asks in month nine "why does coverage read a nightly replica?", the answer is a
signed record with Wes's own name on it, not a Slack search that comes up empty. The specs, the
RUNBOOK, the risk-tier map, the cadence calendar — the whole factory, and the loop that runs
it, are Harbor's now. So is the debt log, in Harbor's tracker with Harbor owners and dates.

**What we keep — the harvest loop.** The engagement paid the *standard* back too. Four
generalized patterns went home through a single PR against the firm's own repo, client specifics
stripped, reviewed by the pod, merged by the standard's deputy:

- **kit/workflows + RUNBOOK template:** configuration versioned with the release artifact —
  rollback restores both (from spec 0046, found by the Phase 8 rehearsal failure).
- **kit/skills/test-writer:** timezone-boundary cases for every suite touching a date the
  business reads (from Build's escaped-bug answer).
- **kit/templates — alert definitions:** the suppression-window-plus-recovery-check pattern for
  designed downtime (from the replica refresh window decision).
- **kit/templates — alert definitions:** the vendor-blip severity split — warning on burst,
  critical on sustained (from hypercare day one).
- **`retros/2026-harbor-mutual.md`:** one file recording what this engagement changed about the
  standard and why, so the next pod inherits conclusions, not anecdotes.

The next pod starts where Harbor finished. **The harvest is a gate item, not a virtue** — an
engagement that ends without it taught the standard nothing. The retro file in `retros/` is the
harvest loop closing on itself.

**The close steering, Friday 8/28 — the last number, with its caveat intact.** **11.4 → 4.2
days** (median from FNOL to coverage decision in March → the completed-claims median in August,
under the 5-day target). Karen got the engagement record, the close-gate evidence, and the
metric's read — stated with the cohort caveat in writing. Completed claims skew fast; the
unbiased read is October's, on a dashboard Harbor owns, watched by alerts Harbor drilled, fed by
a system Harbor ships changes to through a loop Harbor runs. The SOW closed; the final milestone
billed with the gate evidence attached. Who Harbor calls now: their own team. What a future
engagement looks like: a new Phase 0. **The engagement ends the way it ran — underclaimed and
verifiable.**

---

The Harbor Mutual story ends here: 11.4 days when the pod arrived in March; a 4.2-day
completed-cohort median when it left in August, with the honest read scheduled for October on a
dashboard Harbor owns, watched by alerts Harbor drilled, fed by a system Harbor ships changes to
through a loop Harbor runs. That last sentence is the deliverable.
