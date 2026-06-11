# Phase C Worked Example: Harbor Mutual

The continuation of [the Phase 9 example](phase-9-example.md), companion to
[the Phase C deep-dive](phase-c-close.md), and the end of the Harbor Mutual story. The system
is live and observable; Harbor's operators hold the watch; the retrospective is written and
the harvest list is waiting. Three weeks — Monday 2026-08-10 to Friday 2026-08-28 — remain,
and they exist to prove one sentence: **Harbor can run all of this without us.**

The two arcs to watch: **Ines Roy**, who in July had never opened the repo and cold-verified
the README as a stranger, closes the engagement by orchestrating a HIGH-risk spec through the
loop. And **Wes Carter**, who co-signed the first ADR back in March, finishes as what the
Phase 2 example promised he would become: Harbor's Setup Owner.

**The story so far (you can start here):**

|                  |                                                                                                                                                                                                    |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The client**   | Harbor Mutual — a fictional regional insurer. They hired a five-person consulting pod to rebuild how property-insurance claims get reported and decided.                                          |
| **The problem**  | A claim took a median of **11.4 days** from FNOL (first notice of loss — the policyholder reporting the damage) to a coverage decision. Target: **5 days or less**.                               |
| **Where we are** | Live since 7/23. Hypercare closed on schedule; the watch is Harbor's. The build loop still runs daily — the question is whose hands are on it. This phase: flip the roles, run the close gate, leave cleanly, and send the lessons home. |
| **Our pod**      | Maya Chen (Pod Lead — the transfer is hers) · Rob Feld (Setup Owner, handing over) · Jonah Kim and Sara Whitfield (Checkers only, then observers) · Nadia Brooks (Quality Engineer — owns the gate evidence). |
| **Harbor's cast**| Wes Carter (**Harbor's Setup Owner** as of this phase) · Ines Roy (engineer — Orchestrator now) · Tom Reilly (platform engineer, and Wes's named harness deputy) · Luis Ortega (product owner — triage is his) · Dan Kowalski (IT security) · Priti Shah (data lead) · Karen Voss (sponsor). |

**The IDs you'll see on this page:**

| ID         | What it is                                                                                                       |
| ---------- | ----------------------------------------------------------------------------------------------------------------------- |
| **NNNN**   | A spec — one feature in one file. Build closed at 0044; the close phases continued the sequence (0045, 0046); this phase adds 0047-0050. |
| **ADR-NN** | Architecture decision record. Complete through ADR-013, none open.                                               |

**Words this page leans on** (every other term is explained where it first appears):

| Term                       | What it means                                                                                                                                       |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The shadow flip**        | The role reversal opening the phase: Harbor's engineers orchestrate; the pod only checks. The inverse of how Build began.                          |
| **The close gate**         | The engagement's final test: Harbor runs one real spec end-to-end — triage, spec, delegate, grade, merge, deploy — with nobody from the pod driving. |
| **The harness audit**      | The sweep for anything only the pod understands — undocumented skills, hooks with pod-only assumptions — each finding fixed by a PR **Wes** merges. |
| **The harvest**            | The improvements PR against our own standard repo, carrying Harbor's lessons (four items from the Phase 9 retro) into the next engagement's kit.   |
| **Gated paths**            | The parts of the repo (auth, migrations, pipeline, infrastructure) an agent may not touch without explicit human review — enforced by hooks, not by politeness. |
| **The rails**              | CI gates, the grader, branch protection, the deploy pipeline — running since Foundation, and not slowing down just because the pod is leaving.     |

## 1. How the three weeks played out

> **Reading the Tooling lines.** **You run it** — a slash command someone types (e.g.
> `/sdlc-status`, `/sdlc-phase-report`) — **and from this phase on, the hands typing are
> Harbor's.** **It triggers** — an agent or script the command runs under the hood, always
> after a `→`. **No plugin command** — a ceremony, an observation, or the leaving itself.

**Week one (8/10-14) — their hands, our eyes.**
**Tooling —** `/sdlc-status` → the queue numbers at the flow check, typed by Harbor;
`/sdlc` → the Explore agent runs the harness-audit sweep. The specs ride the loop, Harbor
orchestrating.

- **The shadow flip.** Harbor's flow check is run by Harbor; triage is Luis's room now. Three
  real specs from Harbor's own backlog ride the loop with Harbor Orchestrators and pod
  Checkers: **0047** (adjuster queue saved filters — Ines), **0048** (intake supervisor
  daily digest for Dee's team — Ines), and **0050** (claims-search timeout messaging — Wes).
  The bar does not move: plan mode, bounds, the grader, a non-author Checker. Jonah and Sara
  coach by question only — "what does the spec say about that path?" — and log every place
  they wanted to grab the keyboard, because each one is a transfer gap with a name.
- **The harness audit** runs in parallel: Claude's read-only sweep plus Rob's walk of every
  skill and hook, asking *could Harbor operate this if we vanished tonight?* **Two findings**
  (section 4): a grader-prompt phrase that referenced our internal standards by name instead
  of stating the rule, and the stop-gate hook assuming a lint configuration path that
  existed on pod machines but wasn't pinned in the repo. Both fixed by documented PRs that
  **Wes merges** — the gap closes, and Harbor's Setup Owner's merge history starts being
  real on day three.
- Wes also ships a harness change of his own, unprompted and perfect: an **onboarding
  bootstrap skill** for new Harbor engineers — born directly from Ines's step-4 stall in
  [the Phase 7 cold checkout](phase-7-example.md), turning that day's fix into a permanent
  practice. Tom is named as
  his harness deputy; the both-eyes rule survives the pod's departure.

**Week two (8/17-21) — the close gate.**
**Tooling —** No plugin command from our side — that is the test. Harbor types everything:
the spec rides their loop; the `risk:high` label fires security.yml → the security-reviewer
agent; Dan signs.

- The close-gate spec is real, with a date attached: **0049 — decommission the legacy intake
  fallback**, due at day 30 of the rollout (8/22). Luis confirms at triage that the fallback
  triggers never fired in thirty days of production; the room debates the tier and lands it
  **HIGH** — re-standing the legacy intake after decommission would take days, and
  hard-to-undo is the definition. Nobody from the pod is in the discussion. The tier debate
  itself is the judgment transferring.
- **Thursday 8/20, the run.** Ines orchestrates: plan mode, bounds, the agent builds. The
  wobble the observers were waiting for arrives on schedule — the agent's plan drifts toward
  editing the deploy workflow YAML to remove the fallback wiring, **a gated path**. The hook
  blocks the edit; Ines stops, takes the workflow change to Wes, and it ships as its own
  reviewed harness PR — exactly the escalation the rules prescribe, executed by someone who
  learned those rules eight weeks ago. The pod, in the room, says nothing.
- The rest is the loop being the loop: the grader walks the checks and passes, Wes reviews
  as the non-author Checker, **Dan's named HIGH sign-off** lands in the PR, merge, and
  deploy-dev → test → production on Harbor's go/no-go (their second ever; Tom executes,
  nobody blinks). The legacy fallback goes dark ahead of its day-30 deadline because
  Harbor's team took it there. Nadia's observation record — names, timestamps, the blocked edit, the
  escalation, the merge — is the close-gate evidence, and it is clean: **observed,
  unassisted, real.**

**Week three (8/24-28) — the clean exit.**
**Tooling —** `/sdlc-phase-report` → the full report bundle, typed by Wes; `/visual-explainer`
→ the close-steering record. The revocation and the goodbye are no plugin command.

- **The record hands over.** The final handoff report; every phase report, 0 through C; the
  outcomes dashboard re-pointed to Priti's ownership with the quarter-read date — **October
  2026** — on Harbor's calendar, caveats intact. The debt log sits in Harbor's tracker with
  Harbor owners: the un-merge path (Q4), the modeled surge thresholds (first CAT event,
  Priti), and 0049's own line item closed on time.
- **Wednesday 8/26: access revokes.** Every pod seat, token, repo permission, environment
  role, and vault access — walked as a checklist by Rob and Dan, item by item, then
  confirmed against Harbor's audit trail. By end of day the pod provably cannot touch the
  system it built. Dan signs the record; it goes in the close packet next to the secrets
  rotation from Phase 8 — the engagement's bookends: we never held production secrets, and
  now we hold nothing at all.
- **The harvest PR opens** against our standard repo: the four Phase 9 items —
  config-versioned-with-artifact into the kit's pipeline starters, the timezone-boundary
  test pattern into the test-writer skill, the suppression-window-plus-recovery-check
  pattern into the alert template, the vendor-blip severity split — client specifics
  stripped, reviewed by the pod, merged by the standard's deputy. A retro file lands in
  `retros/`: what Harbor taught the standard, and why. The next engagement starts where
  this one finished.
- **Friday 8/28: the close steering.** Karen gets the engagement record, the close-gate
  evidence, and the metric's current read: the completed-claims cohort sits at a **4.2-day
  median** — under the 5-day target, stated with the cohort caveat in writing (completed
  claims skew fast; the unbiased read is October's, and the dashboard that will show it is
  Harbor's). The SOW closes; the final milestone bills with the gate evidence attached. Who
  Harbor calls now: their own team. What a future engagement looks like: a new Phase 0.
  **The engagement ends.**

## 2. What to notice

- **Ines is the engagement's proof.** In July she had never seen the repo; the README had to
  survive her. In August she ran a HIGH-risk spec through the loop, hit a guardrail,
  escalated correctly, and shipped to production. The distance between those two sentences
  is what the engagement actually built.
- **The wobble was the win.** The close gate's best moment was the blocked edit — not
  because the agent drifted, but because the rails caught it and a Harbor engineer responded
  with the right judgment, unprompted. Mechanics transfer in documents; judgment only shows
  up under observation.
- **The close gate ran on a HIGH spec with a deadline.** A toy spec would have proven
  nothing. Decommissioning the fallback was real, dated, hard to undo, and fired the full
  HIGH path — security agent, named client sign-off, their go/no-go — with zero pod hands.
- **Wes's merge history is the handover.** Audit fixes, his own onboarding skill, a named
  deputy. "Harbor has a Setup Owner" stopped being an org-chart claim and became a git log.
- **The revocation is a deliverable, not a cleanup.** Walked, dated, signed, audit-confirmed
  — the security posture's last act. Bookended with Phase 8's rotation: never held the
  secrets, now hold nothing.
- **The standard got paid too.** Four patterns went home through the harvest PR. The second
  engagement starts where Harbor finished — which is the whole reason the kit exists.
- **The last number kept its caveat.** 4.2 days, under target, cohort bias stated, October's
  read named and scheduled on the client's own dashboard. The engagement ends the way it
  ran: underclaimed and verifiable.

## 3. Artifact: the close-gate evidence (as recorded)

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

## 4. Artifact: the harness audit findings

| #  | Finding                                                                                                          | Why it would have stranded Harbor                                              | Fix                                                                          |
| -- | ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| 1  | The grader agent's prompt said "review per MCKRUZ standards" — a reference only the pod could resolve            | A future Harbor engineer tuning the grader has no idea what the phrase binds to | Prompt rewritten to state the actual rules inline; PR merged by Wes           |
| 2  | The stop-gate hook resolved a lint configuration from a path that existed on pod machines but not in the repo    | The hook silently weakens the day Harbor runs it on a fresh machine             | Configuration pinned into the repo; hook path repo-relative; PR merged by Wes |

Two findings after a five-month engagement — the open-adaptation habit from Foundation
(every harness change a reviewed PR Wes could see) is why the list is short. The audit's
question — *could they operate this if we vanished tonight?* — now answers yes, in writing.

## 5. Artifact: the harvest PR (summary)

Opened against `MCKRUZ/delivery-standard`, reviewed by the pod, merged by the standard's
deputy:

- **kit/workflows + RUNBOOK template:** configuration versioned with the release artifact —
  rollback restores both (from spec 0046, found by the Phase 8 rehearsal failure).
- **kit/skills/test-writer:** timezone-boundary cases drafted into every suite touching a
  date the business reads (from Build's escaped-bug answer).
- **kit/templates — alert definitions:** the suppression-window-plus-recovery-check pattern
  for designed downtime (from the replica refresh window decision).
- **kit/templates — alert definitions:** the vendor-blip severity split — warning on burst,
  critical on sustained (from hypercare day one).
- **retros/2026-harbor-mutual.md:** the engagement retro file — what changed in the standard
  and why, so the next pod inherits conclusions, not anecdotes.

## 6. The tooling behind this phase

The [Phase C deep-dive](phase-c-close.md) describes this work generically. What actually ran
— typed, from this phase on, by Harbor's hands:

| What got produced                  | How                                                                                                                                  |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Shadow-flip specs (0047, 0048, 0050) | Harbor Orchestrators through the full loop; pod as Checkers only; coaching by question, never by keyboard                            |
| Harness audit                       | `/sdlc` → the Explore agent's read-only sweep + Rob's manual walk; both findings fixed by PRs **Wes** merged                         |
| Wes's own harness change            | No plugin command — the onboarding bootstrap skill, his PR, Tom's deputy review                                                      |
| The close-gate run (0049)           | Harbor end to end: their triage, plan mode, the hook blocking the gated path, security.yml on `risk:high`, Dan's sign-off, their go/no-go |
| Final report bundle                 | `/sdlc-phase-report` → every phase record, 0 through C — typed by Wes                                                                |
| Close-steering record               | `/visual-explainer` → the engagement record and the gate evidence for Karen                                                          |
| Access revocation                   | No plugin command — Rob and Dan, checklist item by item, confirmed against Harbor's audit trail                                      |
| The harvest                         | No plugin command — the PR against our own standard repo, plus `retros/2026-harbor-mutual.md`                                        |

---

The Harbor Mutual story ends here: 11.4 days when the pod arrived in March; a 4.2-day
completed-cohort median when it left in August, with the honest read scheduled for October
on a dashboard Harbor owns, watched by alerts Harbor drilled, fed by a system Harbor ships
changes to through a loop Harbor runs. That last sentence is the deliverable.
