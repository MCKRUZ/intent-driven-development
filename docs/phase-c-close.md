# Phase C: Close & Transfer

Deep-dive on the last phase of the engagement. The engagement does not end when the code is
done — the code was done weeks ago. It ends when the client can run all of this without us:
the system, the harness, the loop, and the judgment. Phase C is where that claim stops being
an intention and gets proven the same way everything else in this standard gets proven —
**by use, observed, without help.**

The whole engagement built toward this phase. The kit was adapted in the open in Foundation
so the client's engineers saw how it works. Their lead engineer co-signed every ADR. Their
platform engineer executed every promotion. Their newest hire cold-verified the README.
Their on-call answered the drill. Phase C is not a handover event; it is the moment the
handover that has been happening all along is tested — and then we leave, cleanly, and the
standard itself learns from the engagement before the door closes.

> **What closes the engagement** (full checklist in section 5): the harness audit found nothing only the
> pod understands, the client Setup Owner has merged harness changes themselves, client engineers
> completed at least three real specs as Orchestrators, and — the close gate — the client team ran
> one real spec end-to-end, observed and unassisted. Then our access is revoked and confirmed
> against the audit trail, and the harvest PR is opened. The failure mode to watch (section 6): a toy
> close-gate spec instead of a real one.

**If you're starting here:**

|                          |                                                                                                                                                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The method**           | Claude (the AI coding agent) drafts documents and writes most code. Humans own every decision and verify every result.                                                                                       |
| **The rhythm**           | Numbered phases open and close the engagement; in between ran the continuous build loop. Each phase ends with automated checks (the **gate**) plus a named human sign-off. Gates are the billing milestones. |
| **Where we are**         | Live in production, observable, drilled, retrospected. The client's operators hold the watch. One thing remains unproven: that the client's team can run the build loop — intent through deploy — without us in the driver's seat. |
| **Our pod (4-6 people)** | Pod Lead · Setup Owner · Orchestrators · Quality Engineer. ([Team deep-dive](team.md))                                                                                                                       |

**Words this page leans on** (every other term is explained where it first appears):

| Term                       | What it means                                                                                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **The loop**               | Intent → Delegate → Discern, per spec — how every change has been made since Foundation, and what the client's team inherits as a working practice, not a document. |
| **The harness**            | The project's CLAUDE.md, specs, skills, agents, hooks, and settings — versioned in the client's repo. After this phase it has a client owner, not a pod owner.       |
| **The client Setup Owner** | The named client engineer who owns the harness after close — and who must have **merged harness changes themselves** before we leave, not merely been told about them. |
| **The shadow flip**        | The role reversal that opens the phase: the client's engineers orchestrate specs while the pod only checks. The inverse of how Build started.                       |
| **The close gate**         | The phase's defining test: the client team runs one real spec end-to-end — triage, spec, delegate, grade, merge, deploy — without us driving. Observed, unassisted. |
| **The harness audit**      | A sweep for anything only we understand: undocumented skills, hooks with pod-only assumptions, knowledge living in pod memory instead of the repo.                  |
| **The harvest**            | The mandatory improvements PR against our own standard and kit, carrying what this engagement taught: generalized skills, corrected templates, patterns worth repeating. Opened in this phase, from the Phase 9 retrospective's list. |
| **Access revocation**      | The deliberate, audited removal of every pod credential, seat, and permission — a checklist item with a date, not an eventual cleanup.                              |
| **A real spec**            | A spec with stakes: something the client actually needs, with a real risk tier and real consequences. The close gate run on a toy spec proves nothing and counts for nothing. |

Phase C answers four questions, and nothing else:

1. **Can their people run the loop?** (their engineers orchestrate real specs with our
   Checkers first; then one real spec end-to-end with nobody from the pod driving)
2. **Is the harness fully theirs?** (the audit finds nothing undocumented; the client Setup
   Owner is named and has merged harness changes themselves)
3. **Is the record complete and delivered?** (every phase report, the outcomes dashboard,
   the debt log — handed over, in their hands, in their tooling)
4. **Did we leave cleanly — and did the standard learn?** (access revoked and audited; the
   harvest PR opened against our own repo before the engagement's lessons evaporate)

New features for the client are out of scope unless they are the vehicle — the specs run
during this phase are real work from the client's own backlog, chosen because the close gate
must be run on something that matters. A follow-on engagement, if there is one, is a new SOW
with its own Phase 0, not a quiet extension of this one.

---

## 1. Who is involved

Phase C is the Pod Lead's phase, and the pod spends it deliberately becoming less necessary:
hands off the keyboard in week one, out of the room by the gate, out of the building at the
end. The client's cast carries the phase — which is the point.

### Our side

| Person               | Load   | Workstream                                                                                                                                                        |
| -------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pod Lead**         | 60-80% | Runs the transfer: the shadow-flip schedule, the close-gate observation, the final steering, the clean exit. Holds the line against scope arriving dressed as closure. |
| **Orchestrators**    | 40-60% | Become Checkers only: review the client engineers' specs, coach by question rather than by keyboard, and then stop.                                              |
| **Setup Owner**      | 30-50% | Runs the harness audit with Claude, fixes findings by documented PR that the **client** Setup Owner merges, and hands over the last keys.                        |
| **Quality Engineer** | 20-40% | Verifies the transfer the way they verified everything: by observation. Owns the close-gate evidence and the final outcomes-dashboard handover.                   |

### Client side

| Person                    | Needed for                                                                                                                              | How much              |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| **Their engineers**       | Orchestrating real specs — at least three with our Checkers, then the close-gate spec solo                                               | The thread of the phase |
| **The client Setup Owner**| Named before the phase starts; merges the audit-finding PRs and at least one harness change of their own                                 | Steady hours          |
| **Product Owner**         | Their own intent triage — the decision clock and the vague-line test are theirs now                                                       | Their normal cadence  |
| **Operations / platform** | Confirm the access revocation against their audit trail; receive the last operational keys                                              | 2-3 hours             |
| **Sponsor**               | The close steering: the engagement record, the outcome read, the formal end                                                              | 1 hour                |

If the client cannot name engineers to run the loop, the close gate cannot be passed — and
that conversation belongs at steering **weeks before** this phase, which is why the training
workstream (priced into the SOW from Phase 0) existed. Phase C reveals the transfer's state;
it cannot manufacture one.

### Claude's role in Phase C

Claude is not handed over — Claude was never ours. The harness, the agents, the skills, and
the keys have been the client's since Foundation; what transfers in Phase C is the human
judgment around them. Claude's work this phase:

- **Audits the harness, read-only.** A sweep of the repo for anything that would strand the
  client: skills with pod-specific assumptions, hooks referencing paths or permissions only
  we had, conventions that live in pod memory instead of CLAUDE.md. Every finding becomes a
  documented fix the client Setup Owner merges.
- **Drafts the final handoff report** from the engagement's own records: every gate, every
  phase report, the metrics history, the debt log, the open items with owners.
- **Drafts the harvest PR** against our standard repo from the Phase 9 retrospective's list —
  client specifics stripped, patterns generalized — for the pod to review and our standard's
  deputy to merge.
- **Keeps working for the client.** During the shadow flip and the close gate, Claude is
  the same agent inside the same harness — driven now by the client's Orchestrators. That
  continuity is the proof the harness, not the pod, was the operating system.

What Claude never does: drive the close-gate spec (nobody from our side does — that is the
test), approve the client team's work as the gate evidence, or write the retrospective's
candor for them.

---

## 2. The three weeks

The default calendar is **three weeks** — long enough for the role flip to be real, short
enough that the pod's presence doesn't quietly become a dependency again.

### Week one — their hands, our eyes

- **The shadow flip.** The client's engineers take the Orchestrator seat on real specs from
  their own backlog — triage with their PO, spec writing, bounds, plan approval, driving the
  agent — while the pod serves only as Checkers. Coaching happens by question ("what does
  the spec say about that path?"), never by taking the keyboard. At least **three real
  specs** ride the loop this way, and the bar is the same bar: the grader runs, a non-author
  approves, merge deploys. The specs come out of the client's own intent triage like any
  other work — ordinary backlog items, mixed tiers, each sized to merge within the week.
  The Pod Lead confirms each one is real work, not an exercise built for the occasion.
- The pod Checkers log every place they had to coach — every moment they wanted the
  keyboard — because each one is a transfer gap with a name. The Quality Engineer rolls
  those logs into the shadow-flip spec record: per spec, who orchestrated, who checked, the
  grader and Checker outcomes, and the gaps.
- **The harness audit** runs in parallel: Claude's read-only sweep plus the Setup Owner's
  walk of every skill, hook, and convention, asking one question — *could their team operate
  this if we vanished tonight?* Findings get fixed by documented PRs that the **client
  Setup Owner** merges, which kills two birds: the gap closes, and the client owner's merge
  history starts being real.

### Week two — the close gate

- **The solo spec.** One real spec — something the client genuinely needs, with a real risk
  tier — runs the loop end to end with nobody from the pod driving: their triage, their
  spec, their bounds, their plan approval, their Checker, their merge, the automatic deploy.
  The client's triage picks the spec; the Pod Lead confirms it clears the real-spec bar —
  real need, real tier, real consequences — before the run is scheduled.
  The pod observes the way the QE observed the cold runs: present, silent, taking notes.
  The Quality Engineer's record captures each loop step with timestamps and names, every
  stall, every guardrail event and how the team responded, the merge and deploy that closed
  it, and the verdict. Stalls are data. Help — any answer, hint, or keyboard touch from our
  side — voids the run.
- A failed or wobbly run is information, not embarrassment: the gap gets named, fixed —
  more reps, a harness clarification, a missing playbook line — and the gate is **re-run on
  a different real spec**. "They got through it with a little help" fails the close gate for
  the same reason it failed the README checkout.
- The client Setup Owner ships at least one harness change of their own this week — their
  improvement, their PR, their deputy arrangement on their side (the no-role-without-a-deputy
  rule transfers too: a named client engineer reviews the client Setup Owner's harness
  changes, the way our deputy reviewed ours).

### Week three — the clean exit

- **The record hands over.** The final handoff report; every phase report from 0 through 9;
  the outcomes dashboard re-pointed to client ownership with its caveats intact; the debt
  log with owners and dates. Delivered into their tooling, not left in ours.
- **Access revokes, audited.** Every pod seat, token, repo permission, environment role, and
  vault access — removed on a checklist, confirmed against the client's audit trail by their
  security. The Setup Owner drafts the checklist in week one from everything the engagement
  was ever granted — the Phase 0/1 access checklist, CI secrets, environment roles, vault
  policies — so that week three is execution, not discovery. The engagement ends with the
  pod provably unable to touch the system, which is not distrust; it is the last deliverable
  of the security posture the engagement ran on.
- **The harvest PR opens** against our own standard repo: the generalized skills, the
  corrected templates, the patterns the Phase 9 retrospective flagged — reviewed by the pod,
  merged by the standard's deputy. This is the compounding asset doing its compounding; an
  engagement that ends without a harvest taught the standard nothing.
- **The close steering.** The sponsor gets the engagement record, the outcome metric's
  current read with its caveats, the formal end of the SOW, and the answer to the only
  question left: who they call now (their own team), and what a future engagement would look
  like (a new Phase 0). The last billing milestone lands with the close gate's evidence
  attached.

### When the three weeks stretch

- **The close gate fails.** The most important stretch there is. Name the gap honestly at
  steering, fix it, re-run on a different real spec. Leaving on schedule with an unpassed
  close gate is not closing — it is abandoning, with paperwork.
- **The backlog has no real specs** — everything queued is too big or too trivial for the
  gate window. That is a triage problem the client's PO now owns; solving it together *is*
  transfer work.
- **"One more feature" arrives dressed as closure.** Scope at close is still scope. It goes
  to a follow-on conversation with its own SOW, not into the close-gate window.
- **The pod becomes the pager again.** A production wobble during Phase C pulls the pod back
  into the driver's seat "just this once." Hold the Phase 9 handover: their watch, their
  playbook, the pod one escalation away — an escalation, not a reflex.

---

## 3. The artifacts

> Worked example: [`phase-c-example.md`](phase-c-example.md) — Harbor Mutual's close: Ines
> and Wes orchestrating with the pod checking, the harness audit's two findings, the solo
> spec that decommissions the legacy fallback ahead of its day-30 deadline, the access revocation Dan
> confirms against his own audit log, and the harvest PR that sends four patterns home.

| Artifact                     | Drafted by                                | Owned by            | Done means                                                                                                     |
| ---------------------------- | ------------------------------------------ | ------------------- | -------------------------------------------------------------------------------------------------------------- |
| Shadow-flip spec record      | Quality Engineer                           | Pod Lead            | At least three real specs orchestrated by client engineers with pod Checkers — the bar unchanged               |
| Harness audit + fixes        | Claude (sweep), Setup Owner (walk)         | Client Setup Owner  | Nothing only-we-understand remains; every finding fixed by a documented PR the client Setup Owner merged       |
| The close-gate evidence      | Quality Engineer (observation record)      | Pod Lead            | One real spec, end to end, client-driven, observed and unassisted — names, timestamps, and the merge that deployed |
| Final handoff report         | Claude (drafts)                            | Pod Lead            | The engagement record in one place: gates, reports, metrics history, debt log, open items with owners          |
| Outcomes dashboard handover  | Quality Engineer + client data lead        | Client              | Re-pointed to client ownership, caveats intact, the quarter-read date — the day the outcome metric gets its first full-period reading, resolving the caveats Phase 9's first read carried — on their calendar |
| Access revocation record     | Setup Owner + client security              | Client security     | Every pod credential removed, confirmed against the client's audit trail                                       |
| The harvest PR               | Claude (drafts), pod (reviews)             | Our standard's owner | Opened against our repo with client specifics stripped; merged by the standard's deputy                        |
| The retro file               | Pod Lead                                   | Our standard's owner | One file in our repo's retros/: what this engagement changed about the standard and why                        |

What is deliberately **not** produced: a transition-services annex that quietly keeps the
pod on retainer (if the client wants ongoing help, that is a new agreement made in daylight),
and any "final improvements" to the client's code outside the loop — the loop is theirs now,
and so is every change.

---

## 4. The cadences

| Rhythm                        | Who                                | What                                                                                          |
| ----------------------------- | ---------------------------------- | --------------------------------------------------------------------------------------------- |
| **Their daily flow check**    | Client team, pod observing         | Run by the client from week one — the queue numbers are theirs to read now                    |
| **Their intent triage**       | Client PO + their engineers        | The vague-line test and the decision clock, client-run; the pod watches the bar hold          |
| **The close-gate observation**| Client team driving, QE observing  | Week two's defining event — present, silent, recorded                                         |
| **The exit checklist walk**   | Setup Owner + client security      | Week three: access, keys, seats, audit trail — item by item                                   |
| **The close steering**        | Sponsor + Pod Lead                 | The formal end: the record, the read, the gate evidence, the goodbye                          |

---

## 5. The exit gate

The engagement closes when all of these are true:

- [ ] The harness audit ran and found nothing undocumented — no skill or hook only we
      understand; every finding fixed by a PR the client Setup Owner merged
- [ ] The client Setup Owner is named and has merged harness changes themselves — including
      at least one of their own
- [ ] Client engineers completed at least three real specs as Orchestrators with pod
      Checkers — the bar unchanged
- [ ] **The close gate: the client team ran one real spec end-to-end — triage, spec,
      delegate, grade, merge, deploy — without us driving.** Observed, unassisted; a run
      that needed help was re-run on a different real spec
- [ ] Every phase report is delivered and the outcomes dashboard is handed over, caveats
      intact, with the quarter-read date on the client's calendar
- [ ] The debt log is in the client's hands with owners and dates
- [ ] Our access is revoked — every seat, token, and permission — and confirmed against the
      client's audit trail
- [ ] The harvest PR is opened against our standard repo, and the retro file is written
- [ ] A named human on each side signed the close — gates report, humans decide, one last
      time

---

## 6. What goes wrong in Phase C

- **The indispensable pod member.** One person's head still holds how something really
  works, discovered the week after they leave. The harness audit exists for exactly this;
  "ask the pod" must return zero results before the gate.
- **The toy close gate.** The solo spec is a copy change with a LOW tier and no stakes,
  chosen so it cannot fail. It proves nothing, and everyone in the room knows it. Real spec,
  real tier, real consequences — or the gate did not run.
- **The helpful observer.** Forty minutes into the solo spec, someone from the pod answers
  one little question. The run is void — same rule as the cold checkout, same reason. The
  gap the question revealed is the finding; record it, fix it, re-run.
- **The Setup Owner in name only.** A client owner who was named in a deck but never merged
  anything. Merge history is the test: the audit fixes, plus at least one change of their
  own, or the harness has no owner — it has a label.
- **Access that lingers.** "We'll clean up the seats next sprint." Months later the pod can
  still reach production, which is a finding on somebody's audit eventually. Revocation is a
  dated checklist item confirmed by their security, not a cleanup intention.
- **Scope dressed as closure.** "Before you go, could you just—" at close burns the calendar
  the gate needs. New work is a new conversation with a new SOW; the Pod Lead holds that
  line precisely because everyone else in the room has an incentive not to.
- **The skipped harvest.** The pod rolls off to the next engagement and the PR never opens;
  the standard learns nothing, and the next pod re-discovers this engagement's lessons at a
  client's expense. The harvest is a gate item, not a virtue.
- **The quiet retainer.** Hypercare reflexes outlive their window and the pod keeps
  answering questions for free, indefinitely, off the record. It feels generous and it
  un-transfers the engagement one Slack message at a time. The close means the close; future
  help is a future agreement.

---

Back: [Phase 9: Monitoring](phase-9-monitoring.md) — the watch this phase hands over for
good.
