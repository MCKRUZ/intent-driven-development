# Phase 7: Documentation

Deep-dive on the first phase of the engagement's close. Build is feature-complete; the gated
phases resume. Phase 7 exists to answer one question: **can someone who isn't us understand,
run, and operate this system from its documentation alone?** In a consulting engagement that
question is not hygiene — it is the handoff. Everything this phase produces is what the
client's team lives with after we leave.

This method generates most of its documentation as it goes: specs stay current by
construction (the spec changes in the same PR as the behavior), ADRs were signed when
decisions were made, and the harness is versioned in the repo. So Phase 7 is not "write the
docs at the end." It is: consolidate what exists, verify it against the system **as built**,
close the decision debt, write the operational docs — and then prove all of it by use, not by
reading.

> **What closes Phase 7** (full checklist in section 5): a client engineer new to the repo completed the
> README cold checkout unassisted on a clean machine, the client's ops engineer executed a deploy,
> a rollback, and a failure scenario from the RUNBOOK cold, the API docs match the implementation,
> and the drift catalog is empty or every item has an owner and a Phase 8 decision. The bar (section 6):
> "they managed with a little help" is a fail — a failed cold run is fixed and re-run clean.

**If you're starting here:**

|                          |                                                                                                                                                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The method**           | Claude (the AI coding agent) drafts documents and writes most code. Humans own every decision and verify every result.                                                                                       |
| **The rhythm**           | Numbered phases open and close the engagement; in between ran the continuous build loop. Each phase ends with automated checks (the **gate**) plus a named human sign-off. Gates are the billing milestones. |
| **Where we are**         | Phases 0-3 opened the engagement; the Build loop grew the walking skeleton into the product, spec by spec, and is now feature-complete. The close begins: Documentation, then Deployment, Monitoring, and Close & Transfer. |
| **Our pod (4-6 people)** | Pod Lead · Setup Owner · Orchestrators · Quality Engineer. ([Team deep-dive](team.md))                                                                                                                       |

**Words this page leans on** (every other term is explained where it first appears):

| Term                   | What it means                                                                                                                                                                  |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A spec**             | One feature, described in one file in the repo (`specs/NNNN-name.md`). Specs are the per-feature source of truth and stayed current all through Build — behavior changes changed the spec in the same PR. |
| **ADR**                | Architecture decision record: one hard-to-undo choice written down — the options considered, the decision, its consequences — signed by a named human on each side.            |
| **API contract**       | Exactly how a piece of the system behaves at its boundary, failures included — what callers may rely on. Signed in Phase 2, carried through Build.                              |
| **Drift**              | A difference between what a Phase 2 contract promised and what the built system actually does. Drift is either intentional (a decision someone made, needing a documented why) or unintentional (a defect). |
| **README**             | The front door of the repo: what the system is, what you need, and step-by-step local setup that a newcomer can follow exactly.                                                 |
| **RUNBOOK**            | The operations manual, written for a reader who is exhausted, stressed, and seeing the system for the first time during an incident: deployment, configuration, common operations, and the top failure scenarios — every step copy-pasteable. |
| **Cold verification**  | Proving a document by following it with no help: a person who has never touched the system executes it exactly as written, and every place they stall is a documentation defect. |
| **The harness**        | The project's CLAUDE.md, specs, skills, agents, hooks, and settings — versioned in the repo, owned by the Setup Owner, and itself part of what the client inherits.            |
| **PR**                 | Pull request — the proposed change under review. Documentation changes ride the same rails as code.                                                                            |
| **The rails**          | The enforcement from Phase 3: CI gates, the grader, branch protection, the deploy pipeline. Still running; docs PRs are not exempt.                                            |

Phase 7 answers four questions, and nothing else:

1. **Is the written system the built system?** (API docs diffed against the Phase 2 contracts,
   every drift explained or fixed; specs spot-audited against behavior)
2. **Can a stranger run it?** (the README, proven by a cold checkout)
3. **Can a stranger operate it at 3 a.m.?** (the RUNBOOK, proven by a cold walk-through of
   real procedures in a real environment)
4. **Is the decision record complete?** (every significant Build-era decision has an ADR;
   nothing lives only in someone's head)

New features, deployment to production, and monitoring configuration are out of scope — they
belong to the Build loop (now closed), Phase 8, and Phase 9. Defects *found by documenting* —
an unintentional drift, a broken setup step — are in scope and ride the build loop as specs
before the phase can close.

---

## 1. Who is involved

Phase 7 is the Quality Engineer's phase the way Foundation was the Setup Owner's: the QE owns
what "verified" means here, and the verification is done by people who must not be us.

### Our side

| Person               | Load   | Workstream                                                                                                                                                      |
| -------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Quality Engineer** | 70-90% | Owns the verification design: who does each cold run, what counts as a stall, how doc defects get triaged. Audits the spec library against behavior on a sample. |
| **Setup Owner**      | 50-70% | Owns the RUNBOOK's truth — the deploy, rollback, secrets, and scaling procedures are theirs to get right. Owns the harness documentation the client inherits.    |
| **Orchestrators**    | 40-60% | Drive the drafting agents, run the contract diff, fix the doc defects the cold runs surface — through the loop, like any change.                                |
| **Pod Lead**         | 30-40% | Routes drift decisions (intentional or defect?) to the right owner, schedules the client verifiers' time, runs the gate and the steering.                       |

### Client side

| Person                       | Needed for                                                                                                                                          | How much  |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | --------- |
| **An engineer new to the repo** | The README cold checkout — deliberately someone who has never opened the project, because that is who the README is for                              | 2-3 hours |
| **Ops / platform engineer**  | The RUNBOOK cold walk-through in the real dev environment: a deploy, a rollback, one simulated failure scenario — with their own permissions, not ours | 3-4 hours |
| **Lead engineer**            | Reviews the drift catalog and co-signs the new ADRs — the decision record is theirs after close                                                       | 2-3 hours |
| **Product Owner**            | Confirms any user-facing documentation matches what users actually do                                                                                  | ~1 hour   |
| **Sponsor**                  | Steering at the gate: the documentation audit and the deployment readiness picture                                                                     | 45 min    |

If the client cannot field a cold verifier — someone genuinely new to the repo — that is a
finding about the handoff, not a scheduling nuisance. A README verified by someone who
already knows the system has not been verified.

### Claude's role in Phase 7

Claude wrote most of the system; now it drafts most of the record of it. The human rule of
the phase: **Claude drafts from the code and the specs; humans verify by use.**

- **Drafts the README and user-facing docs** from the repo as it actually is, including setup
  against a fresh checkout — then gets corrected by what the cold run finds.
- **Generates the API documentation by diffing, not transcribing.** Every endpoint is read
  from the implementation and compared against the Phase 2 contracts. Each drift gets a what,
  a when, and a why — or a defect flag. Transcribing the code would faithfully document the
  bugs; the diff is what finds them.
- **Sweeps the Build history for undocumented decisions.** A read-only pass over the merge
  history and spec library, looking for the choices that never got an ADR: a dependency
  added, a pattern changed, an alternative rejected in a PR thread. Each finding becomes a
  drafted ADR for humans to sign or strike.
- **Drafts the RUNBOOK procedures** from the real pipeline and infrastructure — then gets
  corrected by the ops walk-through.

What Claude never does: declare a document verified, decide whether a drift was intentional,
or sign an ADR. Reading its own output back is not verification — that is the author grading
the author, and the rule survives the Build loop intact.

---

## 2. Day one to the last day

The default calendar is **5 business days**. The first half drafts and diffs; the second half
verifies by use and fixes what the verification finds. It stretches when the drift catalog is
long or a cold run fails badly — both of which are the phase doing its job.

**Day 1 — scope, inventory, and audiences.**

- The documentation scope gets decided with the client before anything is written: who reads
  each document (their engineers, their ops, their users), what already exists and is current
  (the spec library, the ADR registry, the harness docs), what must be created (README, API
  docs, RUNBOOK), and any client documentation standards the deliverables must follow.
- The spec library gets a sample audit: the QE picks a handful of specs and checks them
  against live behavior in dev. Specs stayed current by construction all through Build — this
  is the trust-but-verify pass that proves the construction held. (A handful: five to ten,
  weighted toward HIGH-risk and recently changed specs. Checking means executing each spec's
  acceptance checks by hand against dev — not re-reading the spec.)

**Day 2 — parallel drafts: the README and the contract diff.**

- Two drafting streams run at once, because they touch nothing shared: one drafts the README
  and user-facing docs from the repo; the other reads every endpoint implementation and diffs
  it against the Phase 2 API contracts.
- The diff produces the **drift catalog**: every difference between the contracts and the
  built system, each labeled by a human — *intentional* (the decision and its why get
  documented, the contract updated) or *unintentional* (a defect spec, into the loop, fixed
  before the phase closes). One row per drift: what the contract said, what the system does,
  the label, and the resolution. The catalog is reviewed with the client's lead engineer —
  the contracts are theirs after close.

**Day 3 — the RUNBOOK, written for 3 a.m.**

- The reader of a runbook is exhausted, stressed, and possibly seeing the system for the
  first time, mid-incident. Every procedure is written for that reader: numbered steps, exact
  copy-pasteable commands, an observable check after each step ("you should now see…"), and a
  recovery path if the step fails.
- The failure scenarios come from what the engagement actually learned: the constraints from
  Phase 0, the degradation behaviors designed in Phase 2, the incidents and near-misses from
  Build. Each scenario notes what Phase 9's monitoring should alert on — the runbook and the
  alerts must end up describing the same failures.
- "See the wiki" and "ask the team" are banned strings. After close, there is no team to ask.

**Day 4 — the decision sweep.**

- Claude's read-only sweep of the Build-era history surfaces candidate undocumented
  decisions. Humans triage — the Setup Owner with the client's lead engineer: each real one
  becomes an ADR — context, options, decision,
  consequences — co-signed by the client's lead engineer like every ADR before it. Open ADRs
  get closed as accepted or superseded.
- This is debt collection. An unwritten decision is tribal knowledge, and at close, the
  tribe leaves.

**Day 5 — verified by use, then the gate.**

- **The cold checkout:** a client engineer who has never opened the repo follows the README
  exactly, on a clean machine (a clean machine: a fresh OS account or VM with none of the
  project's toolchain pre-installed — the verifier installs everything the README tells them
  to, and nothing it doesn't), while the pod watches without helping. Every stall, every
  assumed tool, every "wait, what's my…" is a documentation defect, fixed the same day and
  re-run. A stall is any step the verifier cannot complete as written without information
  from outside the document — having to ask, guess, or go searching counts; a typo they can
  read past does not. The QE observes and logs each stall as it happens: the step number,
  what was missing, and what the verifier did instead. That log is the doc-defect list. The
  re-run is the same verifier, from step one, end to end — a partial run that starts at the
  failed step proves nothing about the fixes upstream, and the verifier is still cold for
  every step they never reached.
- **The cold walk-through:** the client's ops engineer executes real RUNBOOK procedures in
  the dev environment — a deploy, a rollback, one simulated failure scenario — using their
  own permissions. A procedure that silently assumed the pod's access fails here, which is
  exactly where it should fail. The QE picks the scenario and stages it in dev ahead of
  time — inducing the failure condition or faking its symptoms — and hands the ops engineer
  only the symptom. They respond from the RUNBOOK alone, the pod silent, same rule as the
  checkout.
- The automated gate check runs; the Phase 8 handoff is drafted: the documentation inventory,
  the honest gaps, the deployment checklist (the deployment checklist: the ordered list of
  what Phase 8 must do before go-live — drawn from the RUNBOOK's deploy and rollback
  procedures plus what this phase knowingly left open: secrets rotation, production
  infrastructure promotion, the ceremony roles), the ADR status. Steering: the sign-off, the
  billing milestone, and the engagement advances to Deployment.

### When the week stretches

- **The drift catalog is long.** Many unintentional drifts is a Build-quality finding, not a
  documentation chore — each is a defect spec, and the phase holds until the catalog is
  resolved or each open item has an owner and a Phase 8 blocker decision.
- **The cold checkout fails early and often.** Good — that is the test working. Budget a
  re-run; never let "they got through it with a little help" count as a pass.
- **The decision sweep dredges up a disagreement** — a Build-era choice the client's engineer
  would not have signed. Better surfaced now, in a room, than discovered after close. It gets
  an ADR with the disagreement recorded, or a re-opened decision, explicitly.
- **The client can't free the verifiers.** The verification is the phase. Slip the gate
  rather than verify by reading — and say so at steering.

---

## 3. The artifacts

> Worked example: [`phase-7-example.md`](phase-7-example.md) — Harbor Mutual's documentation
> week: the drift catalog (one intentional, one defect), the 3 a.m. RUNBOOK with the replica
> refresh window as failure scenario one, the decision sweep that found two unwritten ADRs,
> and the cold checkout that failed on step 4 — which was the system working.

| Artifact                  | Drafted by                                | Owned by         | Done means                                                                                                               |
| ------------------------- | ------------------------------------------ | ---------------- | -------------------------------------------------------------------------------------------------------------------------- |
| README + user-facing docs | Claude (from the repo), Orchestrators      | Quality Engineer | A client engineer who never saw the repo completed the cold checkout exactly as written                                  |
| API documentation         | Claude (diff against the Phase 2 contracts) | Setup Owner      | Every endpoint current with the implementation; every drift labeled intentional-with-why or fixed                        |
| The drift catalog         | Claude (drafts), humans (label each entry) | Pod Lead         | Empty, or every open item has an owner and an explicit Phase 8 blocker decision                                          |
| RUNBOOK                   | Claude (drafts), Setup Owner (corrects)    | Setup Owner      | The client's ops engineer executed a deploy, a rollback, and a failure scenario from it, cold, with their own permissions |
| ADR closeout              | Claude (sweep + drafts), humans (sign)     | Setup Owner      | No open ADRs; every significant Build decision recorded and co-signed; superseded ones marked                            |
| Spec library audit        | Quality Engineer                           | Quality Engineer | The sample matches live behavior; any mismatch became a defect spec                                                      |
| Phase 8 handoff           | Claude (drafts)                            | Pod Lead         | Documentation inventory, honest gaps, the deployment checklist, ADR status                                               |

What is deliberately **not** produced: documentation for things that don't exist yet
(production topology is Phase 8, alert definitions are Phase 9 — the RUNBOOK points at them,
it doesn't invent them), and a separate "specification document" duplicating the spec
library — the specs are the feature documentation, and forking that truth creates two
versions where one will start lying.

---

## 4. The cadences

| Rhythm                       | Who                              | What                                                                                                   |
| ---------------------------- | -------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Daily 15-minute pod sync** | Whole pod                        | Draft status, drift triage, cold-run scheduling, doc-defect queue                                       |
| **Drift review**             | Pod Lead + client lead engineer  | Each catalog entry labeled: intentional (document the why) or defect (into the loop)                    |
| **The cold runs**            | Client verifiers + QE observing  | The README checkout and the RUNBOOK walk-through — the phase's actual verification events               |
| **Setup review**             | Setup Owner + deputy             | Continues from Build: doc PRs and harness-doc changes merge reviewed, on the rails like everything else |
| **Steering**                 | Sponsor + Pod Lead               | Falls at the gate: the documentation audit, the drift story, deployment readiness                       |

---

## 5. The exit gate

Phase 7 closes when all of these are true:

- [ ] A client engineer new to the repo completed the README cold checkout exactly as
      written — observed, unassisted, on a clean machine
- [ ] The client's ops engineer executed a deploy, a rollback, and at least one failure
      scenario from the RUNBOOK, cold, in the dev environment, with their own permissions
- [ ] API documentation matches the implementation; the drift catalog is empty or every open
      item has an owner and an explicit Phase 8 blocker decision
- [ ] No open ADRs; the decision sweep ran and every significant Build-era decision is
      recorded and co-signed
- [ ] The spec library sample audit passed (or its mismatches became defect specs, now
      merged)
- [ ] Doc defects found by the cold runs are fixed and the failed run was re-run clean —
      "they managed with a little help" is a fail
- [ ] The Phase 8 handoff exists: inventory, gaps, deployment checklist, ADR status
- [ ] A named human on each side approved the advance — gates report, humans decide

---

## 6. What goes wrong in Phase 7

- **Verified by reading.** Someone senior reads the README, nods, approves. Reading checks
  prose; only use checks truth. The cold run is the phase — protect it.
- **Documenting the plan, not the build.** API docs transcribed from the Phase 2 contracts
  instead of diffed against the code. The drift goes undetected and the docs lie from day
  one. Diff, never transcribe.
- **Transcribing the code, bugs and all.** The opposite failure: docs generated from the
  implementation with no contract comparison faithfully document the defects as features.
  The diff against the signed contracts is what makes drift visible.
- **"See the wiki."** Every pointer to knowledge that lives outside the repo is a 3 a.m.
  failure deferred. The runbook reader has nobody to ask — write it down or it doesn't exist.
- **The helpful cold run.** Someone leans over the verifier's shoulder: "oh, you just need
  to…" The run is now void. Stalls are the data; helping erases the data.
- **ADR debt walking out the door.** Build-era decisions that live in PR threads and pod
  memory. At close, that memory leaves the building. The sweep and the signatures are the
  collection mechanism.
- **The documentation fork.** A shiny new "system specification" duplicating what the specs
  already say. Two sources of truth means one is lying within a quarter. Consolidate and
  point; don't fork.
- **Treating the phase as a formality.** It's "just docs" until the client's on-call engineer
  is alone with the system. In a consulting engagement, this phase *is* the product the
  client keeps.

---

Back: [The Build Loop](build-loop.md) — the continuous middle this phase closes out.

Next: [Phase 8: Deployment](phase-8-deployment.md) — promoting to production through the
pipeline that has existed since Foundation: the rehearsal, the ceremony, and a named human
saying go.
