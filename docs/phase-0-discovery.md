# Phase 0: Discovery

Deep-dive on the first phase of the Delivery Standard. What happens from the first day of the
engagement to the day Phase 0 closes: who is in the room, what gets made, what runs on a
schedule, and what has to be true before Phase 1 starts.

**If you're starting here:**

| | |
|---|---|
| **The method** | Claude (the AI coding agent) drafts documents and writes most code. Humans own every decision and verify every result. |
| **The rhythm** | Numbered phases. Each ends with automated checks (the **gate**) plus a named human sign-off. Gates are the billing milestones. |
| **Our pod (4-6 people)** | Pod Lead · Setup Owner · Orchestrators · Quality Engineer. ([Team deep-dive](team.md)) |
| **Client side** | Sponsor · PO · the corpus — defined in the table below. |

**Words this page leans on** (every other term is explained where it first appears):

| Term | What it means |
| ---- | ------------- |
| **Sponsor** | The client executive who owns the budget and the outcome, and signs the phase. |
| **PO** | Product owner — the client-side person who answers product questions during the build. Getting this role committed, in writing, is one of Phase 0's four jobs. |
| **PO mode / proxy mode** | The two ways product questions get answered during the build: the client names a PO with committed hours and decision turnaround (PO mode), or we answer day-to-day product questions ourselves under a signed rider, log every decision, and the client ratifies them at steering (proxy mode). |
| **The corpus** | The documents the client hands over on day 1 — RFPs (requests for proposal), decks, specs, prior attempts. Everything written about the problem; unsorted is fine. |
| **The SOW** | The statement of work — the signed contract for the engagement. It carries the phase-gated billing and the Phase 0 preconditions. |
| **The fallback rider** | A pre-agreed rider (a short contract amendment) that lets the pod start under our own Anthropic account, with a named migration date, if the client's procurement isn't done in time. |
| **The data-flow brief** | A short document for client security: exactly what data the AI tooling sees, where it flows, and where it is stored. |
| **The decision list** | The running list of product decisions nobody has made yet ("you haven't decided X"), each needing a named human answer. |
| **The build loop** | The cycle the build phases run on: Intent (decide and write what you want), Delegate (an AI agent builds it inside set bounds), Discern (checks and a non-author prove it). Phase 0 only briefs the client on it. |
| **Steering** | The recurring decision meeting between the pod and the client's leadership. Biweekly from Phase 1 on; the day-10 phase review is the first one in all but name. |

**The IDs you'll see on this page:**

| ID | What it means |
| -- | ------------- |
| **DOC-NN** | A client document cataloged at intake. |
| **CON-NN** | A contradiction found between two client documents. |
| **Q-NN** | An open question with a named owner. |

Phase 0 answers four questions, and nothing else:

1. **What problem are we solving, and how will we know we solved it?** (one measurable metric)
2. **Who decides product questions during the build?** (the PO decision)
3. **Can we legally and technically work?** (tooling, access, data boundary)
4. **What constraints are non-negotiable?** (technical, regulatory, organizational)

Everything that looks like requirements, design, or planning is deliberately out of scope — that
work has its own phases, and pulling it forward before these four answers exist is how
engagements end up building the wrong thing precisely.

---

## 1. Who is involved

Phase 0 is deliberately thin on our side. Most of the pod is not yet billing; the work is two
people running two parallel workstreams, with Claude doing the reading and drafting.

### Our side

| Person | Load | Workstream |
|---|---|---|
| **Pod Lead** | 60-80% | **Understanding**: the workshop, stakeholder interviews, every artifact's content, the decision list, sponsor sign-off |
| **Setup Owner** | 40-50% | **Enablement**: Anthropic procurement, repo and access checklist, data-flow brief to client security, the empty delivery repo with the engagement structure initialized |
| **Quality Engineer** | ~10% | One job: vet the success criteria for measurability ("what query, on what system, produces this number?") |
| **Orchestrators** | 0-10% | Not yet staffed, or assisting document intake. They arrive for real in Phase 1. |

The Pod Lead and Setup Owner roles are defined in [the team deep-dive](team.md). If the
engagement is multi-pod from the start, the Engagement Lead runs Phase 0 once for the
engagement; pods do not run separate discoveries.

### Client side

| Person | Needed for | How much |
|---|---|---|
| **Sponsor** (owns budget and outcome) | The workshop, the PO decision, phase sign-off | Workshop half-day + two 30-min checkpoints |
| **Candidate PO** | The workshop; the PO-mode commitment decision | Workshop + one conversation |
| **Security / IT** | Anthropic procurement, repo access, data-flow brief review | Hours, but with lead time — engage day 1 |
| **Domain experts** (2-4 people who live the problem) | Interviews in week 1 | 45-60 min each |
| **Ops / data owner** | Verifying the success metric is actually readable | One working session |

The hardest person to get is usually the data owner. Book them early: an unverifiable success
metric is the most common Phase 0 failure.

### Claude's role in Phase 0

Phase 0 is the phase with the strictest human-in-the-loop rule in the whole standard: **the
problem statement is human-authored.** Claude never invents the problem. What Claude does do,
heavily:

- **Document intake.** The client's corpus (RFPs, prior vendor docs, API specs, strategy decks)
  gets ingested on day 1-2: per-document summaries, a registry with DOC-NNN IDs for
  traceability (so anything built later can be traced back to the exact source document), and
  a contradiction list ("the RFP says X, the architecture deck says Y").
- **Interrogation.** Before the workshop, Claude generates the question list from the corpus:
  gaps, ambiguities, unstated assumptions. After the workshop, it generates the decision list —
  every decision the humans haven't made yet, named explicitly.
- **Drafting.** Every artifact below is drafted by Claude from human-generated raw material
  (workshop notes, interview notes) and then corrected by the Pod Lead and ratified by the
  sponsor. Drafting is cheap; the humans spend their time on whether it's *true*.

What Claude is not in the room for: the workshop itself and the interviews. Those are human
conversations. Claude preps the questions going in and structures the notes coming out.

---

## 2. Day one to the last day

The default calendar is **10 business days**. The constraint is rarely effort — it's lead time
on the client side (procurement, security review, calendars). The two workstreams run in
parallel the whole way so that lead-time waits never idle the phase.

### Before day 1 (pre-engagement, no billing)

- SOW signed with the Phase 0 preconditions in it (section 12 of the standard): phase-gated
  billing, the PO clause, the tooling precondition, IP terms, training line item.
- Workshop scheduled — the sponsor, the candidate PO, and the right domain experts in one room
  is the long pole; book it for day 3-4 before the engagement starts.
- Document corpus requested: "everything written about this problem — RFPs, decks, prior
  attempts, API docs, org charts. Unsorted is fine."

### Week 1 — understand

**Day 1 — kickoff (half day).**
- 60-minute kickoff: introductions, the how-we-work briefing (the build loop, the gates, what the
  client will see biweekly, what we need from them and when).
- Setup Owner opens the enablement workstream with client IT: Anthropic procurement
  conversation started, data-flow brief handed to security, repo/access checklist issued
  (contributor access, Actions enabled, secrets permissions, runner policy).
- Document corpus received; intake begins.

**Day 2 — intake and prep.**
The most tool-dense day of the phase. Claude does the heavy reading; the Pod Lead curates
every output before it travels.
- **Document intake.** Every corpus document is cataloged with a stable ID (DOC-001, DOC-002,
  ...). The Pod Lead reviews the catalog and sets priorities — which documents matter most,
  which to skip. Claude then writes a budgeted summary per document, a human-readable
  registry, and a condensed index that loads at the start of every later session. The catalog
  is locked once complete so document references stay stable all the way into requirements
  traceability.
- **Cross-document analysis.** A fresh analysis agent (one that has not been part of the
  conversation so far) compares the documents against each other and produces two artifacts:
  - The **contradiction list** — every place the documents disagree (CON-01, CON-02, ...),
    each entry carrying two verbatim quotes with their sources, a severity rating, and the
    question a human must answer to resolve it.
  - The **question list** — everything no document answers (Q-01, Q-02, ...), grouped by
    workshop agenda block, each question routed one of three ways: *workshop* (only the room
    can answer it), *pre-workshop* (answerable by email before day 3), or *interview* (better
    asked one-on-one on day 5).
- **The cheap questions go out by email today.** Anything routed pre-workshop gets sent now,
  so room time on day 3 is spent only on what that room can uniquely answer.
- **The workshop brief gets drafted, curated, and sent.** Claude assembles the candidates;
  the Pod Lead chooses what makes the one page — which contradictions, which questions, the
  3-5 decisions the room must leave with — and fills in attendees, logistics, and the agenda.
  The Pod Lead edits the draft and sends it personally. One page, readable in five minutes,
  or it won't be read. Claude never sends anything to the client.

**Day 3 — the outcome workshop (half day, the anchor event).**
The agenda, run by the Pod Lead, humans only:

| Block | Time | Output |
|---|---|---|
| The problem, in the sponsor's words | 45 min | Raw problem narrative; current state; who hurts and how much |
| The three outcomes | 45 min | Business outcome, software outcome, capability outcome — each one sentence |
| The one metric | 30 min | The single measurable success metric, its current baseline (or the admission nobody knows it), and the named system it will be read from |
| Constraints | 30 min | Technical, regulatory, budget, timeline, political — what's fixed and what's negotiable |
| The PO decision | 20 min | Forced explicitly: can the client commit a named PO at >= 4 hrs/week with 2-business-day decision turnaround? Yes -> name them. No -> proxy-mode rider acknowledged. |
| Tooling status | 10 min | Where procurement stands; who unblocks it; fallback rider trigger date agreed |

**Day 4 — first drafts.**
- Claude drafts from the workshop notes: `problem-statement.md`, `success-criteria.md`,
  `constraints.md`. Pod Lead corrects them the same day — drafts age badly.
- Claude generates decision list v1: every unmade decision the workshop surfaced or dodged.
- Interview slots confirmed for day 5 against the decision list's biggest gaps.

**Day 5 — interviews and the first checkpoint.**
- Stakeholder interviews (45-60 min each, 2-4 people): the people who live the problem daily,
  not just the people who fund it. Notes go to Claude for structuring; contradictions with the
  sponsor's framing get flagged, not smoothed over.
- 30-minute sponsor checkpoint: draft problem statement and success criteria reviewed out loud.
  This is where "that's not actually the problem" surfaces — better on day 5 than day 50.

### Week 2 — verify and close

**Day 6 — the metric gets proven.**
- Working session with the client's data owner: actually run the query / open the dashboard /
  pull the report that the success metric will be read from. Record the baseline number in
  `success-criteria.md` with its source named.
- If the number cannot be produced, this is a Phase 0 finding, not a footnote: either the
  metric changes, or "instrument the metric" becomes the first epic (the first big named block
  of requirements work) of Phase 1.
- The Quality Engineer vets every success criterion: baseline, target, measurement method,
  reading cadence.

**Day 7 — constitution and the PO decision land.**
- Claude drafts `constitution.md` — the project's identity document: what this is, what done
  means, the three outcomes, the metric, the constraints, the guiding principles. The sponsor
  will sign this; the Pod Lead makes it short enough that they actually read it.
- PO decision finalized in writing: **PO mode** (named person, triage invitations on their
  calendar, the PO onboarding guide delivered) or **proxy mode** (rider
  signed, decision log created, ratification added to the steering agenda).

**Day 8 — enablement converges.**
- Tooling checkpoint with teeth: Anthropic access live (client keys in their secret store, pod
  seats issued) or the fallback rider invoked today — not "next week."
- Delivery repo exists in the client org with the engagement state and artifact structure
  initialized; all Phase 0 artifacts move into the discovery artifacts folder in the repo
  (they lived in a shared workspace until the repo existed; from today the repo is the only
  home).
- Access checklist closed out or escalated to the sponsor by name.

**Day 9 — gate run.**
- Claude drafts `phase1-handoff.md`: summary, decisions made, the open-questions list (numbered
  Q-01, Q-02...), risks spotted, recommended starting point for requirements.
- The automated gate check runs against the artifacts; placeholder content and missing
  sections get fixed today.
- Claude generates the narrative companion for the sponsor — the artifacts retold in plain
  stakeholder language.

**Day 10 — phase review and sign-off.**
- 45-minute phase review with the sponsor: walk the constitution, the metric with its verified
  baseline, the constraints, the PO decision, the open questions. The sponsor signs the outcome
  statement.
- Pod Lead recommends advance; the human sign-off is recorded; the engagement formally
  advances to Phase 1. This is also billing milestone 1.

### When the calendar slips

The two-week figure assumes client lead times cooperate. When they don't:

- **Procurement stalls** -> the fallback rider exists precisely for this; invoke it on day 8 as
  planned, don't extend the phase waiting.
- **The workshop can't be scheduled inside week 1** -> the phase start should move, not stretch;
  raise it before day 1, since billing is gate-based.
- **Useful idle time** while waiting on the client: deepen document intake, draft interview
  syntheses, prep the Phase 1 requirements workspace. What the pod never does is start Phase 1
  work early "since we're waiting anyway" — requirements built on an unsigned problem statement
  get rebuilt.

---

## 3. The artifacts

Everything Phase 0 produces, who owns it, and what "done" means for each. All of it ends up in
the discovery artifacts folder of the delivery repo, committed, by day 8.

> Worked example: [`phase-0-example.md`](phase-0-example.md) — a complete, filled-in Phase 0
> for a fictional insurer (Harbor Mutual): registry, contradictions, question list, workshop
> brief, problem statement, verified success criteria, constraints, constitution, and handoff,
> each mapped to the day that produced it.

| Artifact | Drafted by | Owned by | Done means |
|---|---|---|---|
| `constitution.md` | Claude | Sponsor (signs) | Identity, three outcomes, the metric, constraints, principles — short enough to be read, signed at phase review |
| `problem-statement.md` | Claude from workshop notes | Pod Lead | Root cause and quantified impact in the sponsor's language; **human-authored framing**, Claude only structured it |
| `success-criteria.md` | Claude | Pod Lead + Quality Engineer | Every criterion has baseline, target, measurement method, and a named source system; the baseline was actually produced on day 6, not promised |
| `constraints.md` | Claude | Pod Lead | Technical, business, regulatory, resource constraints, each with a rationale and a fixed/negotiable flag |
| Decision list | Claude (generated) | Pod Lead | Every unmade decision named; each either answered in an artifact or carried into the handoff as a numbered open question |
| Document registry + summaries | Claude (intake) | Setup Owner | Every corpus document has a DOC-NNN ID and a summary; contradictions listed |
| Data-flow brief | From the kit | Setup Owner | Delivered to client security; questions answered; no open objections |
| Tooling record | Setup Owner | Setup Owner | Anthropic access live under client account, or fallback rider signed with a migration date |
| PO decision record | Pod Lead | Sponsor | Mode chosen in writing; PO named with calendar commitments, or rider signed and decision log created |
| Access checklist | From the kit | Setup Owner | Repo, Actions, secrets, runners: granted or escalated by name |
| `phase1-handoff.md` | Claude | Pod Lead | Summary, decisions, numbered open questions, risks, recommended Phase 1 starting point |
| Stakeholder notes (optional) | Claude-structured | Pod Lead | Interview syntheses; disagreements with the sponsor framing flagged, not smoothed |
| Narrative companion (optional) | Claude | Pod Lead (edits) | The artifacts in stakeholder language, edited by a human before any client sees it |

What is deliberately **not** produced in Phase 0: requirements, user stories, architecture
options, technology selections, estimates beyond the SOW's phase figures, and any code other
than the empty repo scaffold. Each of those has a phase, and each done early is rework.

---

## 4. The cadences

Phase 0 is too short for the full meeting structure of the Build loop. It runs three rhythms:

| Rhythm | Who | What |
|---|---|---|
| **Daily 15-minute sync** (our side only) | Pod Lead + Setup Owner | The two workstreams trade status: what's blocked on the client, what lands today. Replaces nothing; it's just coordination. |
| **Sponsor checkpoints** (day 1, 5, 10) | Pod Lead + Sponsor | Kickoff, draft review, phase review. Three touches, 30-45 min each. The day-5 one is the cheap-correction point. |
| **The anchor events** | Per the calendar | The workshop (day 3), the metric session (day 6), the gate run (day 9). These move only if the people can't be gotten — never to "polish artifacts." |

The biweekly steering cadence does **not** start in Phase 0 — the phase review on day 10 is the
first steering in all but name, and the regular cadence starts in Phase 1.

---

## 5. The exit gate

Phase 0 closes when all of these are true, verified at the day-10 review:

- [ ] The automated gate checks pass: artifacts exist, are complete, contain no placeholders
- [ ] The sponsor signed the outcome statement (constitution)
- [ ] The success metric was **read from its source system** at least once, baseline recorded
- [ ] The PO decision is in writing: named PO with calendar commitments, or signed proxy rider
- [ ] Anthropic access is live under the client's account, or the fallback rider is signed
- [ ] The repo exists in the client org with artifacts committed; the access checklist is closed
- [ ] The handoff document carries every open question, numbered, with an owner
- [ ] A named human (sponsor side) approved the advance — gates report, humans decide

Two of these are SOW preconditions with billing teeth (the PO decision and tooling): if either
is unresolved on day 10, the phase does not close, and the SOW's gate-based billing is what
makes that the client's problem to unblock rather than ours to absorb.

---

## 6. What goes wrong in Phase 0

Named failure modes, because every one of these has happened to somebody:

- **The deliverables list wearing an outcome costume.** The workshop produces "build an API, a
  portal, and a dashboard" instead of an outcome. Test: an outcome survives the deliverable
  changing. If the sentence names a system, keep asking why.
- **The unreadable metric.** Everyone agrees on "reduce processing time 30%" and nobody can say
  what query produces the current processing time. Day 6 exists because of this. If the
  baseline can't be read, instrumenting it is Phase 1's first epic — decided now, not
  discovered in week 9.
- **The dodged PO decision.** "We'll figure out product ownership as we go" means proxy mode
  chosen implicitly, without the rider, without the decision log — the worst of both modes. The
  workshop agenda forces the question; the record makes the answer durable.
- **Procurement drift.** "Tooling will sort itself out during Phase 1" — and then the pod is
  three weeks in, working under our keys with no rider, which is exactly the data-boundary
  ambiguity the standard exists to prevent. Day 8 is the hard checkpoint.
- **The sponsor who nods.** Claude drafts a beautiful problem statement, the sponsor skims and
  nods, and on day 50 it turns out the problem was something else. The defense is the day-5
  checkpoint read *out loud*, and interviews with people who live the problem — their
  disagreements with the sponsor's framing are the most valuable finding Phase 0 produces.
- **Discovery that won't end.** Week 4 of "just two more interviews." Phase 0 answers four
  questions; it does not achieve certainty. Open questions go in the handoff, numbered, with
  owners — that's what the list is *for*.

---

Next: [Phase 1: Requirements](phase-1-requirements.md) — what happens to the handoff, the open
questions, and the epic map in the following week.
