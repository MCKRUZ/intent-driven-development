# The Team

Deep-dive on section 3 of the Delivery Standard. Three parts: how a typical team's roles map to
the new ones, the concrete job of each role, and how the model scales from one pod to many.

**If you're starting here:**

| | |
|---|---|
| **The method** | Claude (the AI coding agent) drafts documents and writes most code. Humans own every decision and verify every result. |
| **The loop** | A human writes a short, testable description of one piece of work (a **spec**) → an agent builds it → someone who didn't build it checks it → it ships. |
| **This page** | Defines the team that runs the loop — a small delivery group called a **pod** — and the rules for growing from one pod to several. |

The starting point is the team most clients (and most of our own engagements) already have:
**one PM, one architect, two developers, one QA.** Five people. Nobody gets fired and nobody
gets a fancy new title for its own sake — every old role maps to a new one, but the *content*
of each job changes, in some cases by more than half. The biggest single shift across all five:
writing code stopped being the bottleneck, so the valuable work moved to two places — deciding
clearly (intent) and proving it's right (checking). Every role below is the old role rebuilt
around that fact.

---

## 1. The mapping, old to new

| Old role | New role | The shift in one line |
|---|---|---|
| Project Manager | **Pod Lead** | From tracking activity (backlog, velocity, status decks) to owning intent: every spec sharp, every decision answered, every gate earned. |
| Architect | **Setup Owner** | From design documents and review boards to owning the harness as a product: the agent environment, the pipeline, and the architecture decisions, all versioned and reviewed. |
| Developer (x2) | **Orchestrator / Checker** (swap per change) | From typing the code to directing agents that type it, and grading each other's agent output against the spec. |
| QA Engineer | **Quality Engineer** | From executing tests after the work to building the checking machinery that runs on every change: graders, hooks, test infrastructure, eval suites. |

Two rules survive every mapping and every scale:

1. **The author of a change is never its sole approver.** Not for code, not for harness changes,
   not for specs, not for this document.
2. **Checking capacity is the constraint.** Nobody opens more agent streams than the team can
   review without the queue growing. Headcount doesn't set the limit; review wait does.

---

## 2. The jobs, concretely

Each role below: what changed, what they do per spec / daily / weekly / per phase, and what they
explicitly stopped doing. "Per spec" means every time a story moves through the build loop.

### 2.1 Pod Lead (was: Project Manager)

The PM's old day was status collection and ceremony administration. Agents made that work
worthless: activity numbers are inflated and meetings about estimates answer questions nobody
asks anymore. What replaced it is more valuable and harder: the Pod Lead owns **intent quality**.
Vagueness at their desk compounds downhill into confident-wrong code, so the sharpest thinking
in the pod happens here.

**Per spec:**
- Run every incoming story through the vague-line test at triage (could two people build
  different things from this line?). Bounce what fails — back to the PO, not down to an agent.
- Assign the risk tier (HIGH / MEDIUM / LOW per the taxonomy in section 5 of the standard) and
  record it in the spec. Hear challenges; challenges escalate up only.
- Keep the decision list moving: every silent decision Claude surfaces gets a human answer
  within 2 business days — from the client PO in PO mode, or from the Pod Lead with a decision-log
  entry the client ratifies at steering in proxy mode.

**Daily:**
- Run the 10-minute flow check: a Checker assigned to every PR waiting for review, vague specs
  flagged, WIP cap enforced, security queue glanced at.

**Weekly:**
- Run intent triage (60 min): stories become ready specs, oversized stories get split there
  (never at review), decision lists get answered.
- Write the 5-bullet async client summary.

**Biweekly:**
- Run client steering: live demo from the dev environment, outcome scorecard, decision list,
  gate status when a phase boundary is near.

**Per phase:**
- Run the Phase 0 outcome workshop (the three outcomes, the one metric, the PO decision, the
  tooling decision).
- Own the recommendation at every phase gate: gates report, the Pod Lead recommends, the human
  chain signs.
- Run Phase C: the transfer checklist, the client-solo close gate.

**Stopped doing:** story-point estimation, velocity tracking, sprint planning and sprint reviews
as ceremonies, status decks built from activity metrics, being a passthrough between client and
team (they're a filter and a sharpener, not a relay).

**Doing it right looks like:** the bounce-back-for-unclear rate falls week over week; agents
rarely stall on an unanswered decision; the client sponsor can state the current success-metric
reading without looking.

### 2.2 Setup Owner (was: Architect)

The architect's old leverage was the design document and the review board — influence applied
occasionally and late. The new leverage is the **harness**: CLAUDE.md, skills, agents, hooks,
permissions, pipeline, and infrastructure that every agent session loads every time. A line in
CLAUDE.md is a design decision enforced a hundred times a day. This is the keystone role and the
known bus-factor risk, which is why the deputy rule exists.

**Day one of every engagement:**
- Name a deputy (the senior Orchestrator). The deputy reviews every harness change; the Setup
  Owner is never sole approver of their own foundation work.

**Per harness change:**
- Harness changes are PRs like everything else: reviewed by the deputy, version-bumped,
  changelogged. "Harness" means CLAUDE.md, anything under `.claude/`, the CI workflows, and
  `infra/`.

**Daily:**
- Watch for friction signals: hook failures, permission prompts the team keeps hitting, pipeline
  flakes, agents repeatedly misreading a convention. Fix same-day or ticket it into the setup
  backlog — a harness papercut taxes every spec in flight.

**Weekly:**
- Run setup review (30-60 min): merge the week's harness changes, turn Retro+ findings into new
  checks or skills ("which check should have caught this?" answers land here as work), review
  token spend.

**Per phase:**
- Phase 2: drive design with Claude researching and presenting 2-3 options with trade-offs; a
  human picks; the Setup Owner signs every ADR.
- Phase 3: install the kit into the client repo, adapt CLAUDE.md with the client's domain
  glossary, build the pipeline and Bicep, prove the walking skeleton end-to-end.
- Phase 8: own the release mechanics and the rollback plan.
- Phase C: hand the harness to the client's named Setup Owner; the audit ("nothing only we
  understand") is theirs to pass.

**Stopped doing:** writing design documents nobody loads into context, gatekeeping decisions
through meetings (the harness gates instead), writing most of the code, being the only person
who can fix the pipeline.

**Doing it right looks like:** a new pod member is productive in under a day because the harness
explains the project better than any person could; the deputy has merged harness changes alone;
agents stop making the same mistake twice because the lesson became a skill or a check.

### 2.3 Orchestrator / Checker (was: Developer)

The two developers keep the deepest technical work but lose the keyboard time. Each spec gets
two of them in fixed, opposite roles: one **Orchestrator** who directs the agent, one **Checker**
who judges the result. They swap per change — Priya orchestrates spec 0007 and Marcus checks it;
Marcus orchestrates 0008 and Priya checks it. The swap is what makes "author never sole
approver" real on a small team, and it keeps both sharp at both crafts.

**Per spec, as Orchestrator:**
- Translate the ready story into `specs/NNNN-name.md`: goal, why, scope in/out, testable
  acceptance checks, risk tier, delegation plan, checking plan.
- Surface anything the story left silent; send real decisions up to the Pod Lead rather than
  letting an agent guess.
- Start the agent in plan mode. Read the proposed plan like a senior reviewing a junior's
  approach — correct it there, where corrections cost minutes, not after the build, where they
  cost hours.
- Set the bounds: file patterns the agent may touch, the one canonical pattern to reuse,
  permissions per `.claude/settings.json`. Tier sets the leash: loose on LOW, tight on HIGH.
- Decide one-agent-vs-many: one agent for tightly coupled code; fan out only for independent
  read-only exploration or genuinely independent specs.
- Supervise the build, drive integration, keep the blocking Stop hook honest (no gaming tests
  green), open the PR with the spec file in the diff.

**Per spec, as Checker:**
- Read the CI grader's check-by-check verdict first — it's a brief, not a verdict to rubber-stamp.
- Grade against the **spec**, not against the author's tests. The author's tests share the
  author's blind spots; the rate-limiting bug that ships is the keyless request nobody's test
  sent.
- Probe one edge the tests didn't cover. Run the code, don't just read it.
- Approve, or bounce with specifics tied to acceptance checks. On HIGH risk: confirm the
  security workflow passed and add the named sign-off.

**Daily:** flow check; at most 2 concurrent agent streams; pick up waiting reviews before
starting new streams (the queue outranks new work).

**Weekly:** intent triage (they do the story-to-spec translation there), Retro+.

**Stopped doing:** typing most of the implementation, style-nit code review (linters and
CLAUDE.md conventions handle it), long-lived feature branches, "it works on my machine"
demos — the dev environment is the demo.

**Doing it right looks like:** plans get corrected in plan mode more often than PRs get
bounced; their accepted-as-is rate climbs; as Checker they catch things the grader missed at
least occasionally (if they never do, they're rubber-stamping).

### 2.4 Quality Engineer (was: QA)

The old QA job — execute test plans after development, file bugs, regression-cycle before
release — dies completely in this model, and not because quality matters less. It's the
opposite: checking became the scarce, valuable work, so the QA person stops *performing* checks
and starts *building the machinery that checks everything, every change*. This is a promotion
in everything but title.

**Owns outright:**
- The verification ladder as working machinery: the re-checking rules in CLAUDE.md, the blocking
  Stop hook, the CI test gates, the grader agent definition, the security workflow wiring.
- The grader's prompt and behavior. When the grader misses something or pedantically blocks on
  nothing, the Quality Engineer tunes it.
- Test infrastructure: fixtures, factories, `WebApplicationFactory` harnesses, Playwright setup,
  coverage configuration.
- For agentic deliverables (section 11 of the standard): the golden sets, the eval harness, and
  the eval-regression gate in CI.

**Per spec:**
- At triage, vet acceptance checks for testability — they're the second pair of eyes on the
  vague-line test, asking "how would a check prove this line?"
- Confirm the checking plan matches the risk tier before the spec goes to an Orchestrator.

**Daily:**
- Take a regular turn in the Checker rotation. They're often the strongest Checker in the pod,
  and the rotation needs their capacity.

**Weekly:**
- Bring the escaped-bug analysis to Retro+: for every defect that reached production, name the
  rung of the ladder that should have caught it, and leave with a concrete change to that rung
  (a new grader instruction, a new hook condition, a new test category). An escaped bug that
  doesn't change a check is a wasted bug.

**Per Build:**
- Plan and run the hardening passes (one mid-Build, one before Phase 8): E2E journeys, load and
  performance, penetration-test coordination.

**Stopped doing:** manual regression cycles, test-case spreadsheets, end-of-cycle test phases,
being downstream of development (they're upstream now — their machinery runs before any human
sees the PR).

**Doing it right looks like:** escaped bugs trend toward zero and each one strengthens a check;
the grader catches spec violations the author's tests missed; hardening passes find performance
issues, not functional bugs (functional bugs should already be dead).

### 2.5 What no one owns anymore

Listed because vacated ground breeds turf wars: sprint ceremonies (replaced by flow check,
intent triage, Retro+, setup review), the estimation poker ritual, the staging-only "QA
environment" sign-off step, the change-advisory-board meeting (the ladder plus named HIGH-risk
sign-off replaces it), and any dashboard with story points on it.

---

## 3. Scaling: one pod to many

### 3.1 Principles

1. **The pod is the unit of replication.** A pod never grows past 6 people; when there's more
   work than a pod can check, you add a pod, not a seventh person.
2. **Roles that touch a spec stay in the pod.** Intent, orchestration, checking, and quality
   machinery are per-pod, always. Roles that touch the *system* — the shared harness, the
   architecture, cross-pod flow, security policy — are the ones that graduate to spanning pods.
3. **A shared role's span is set by review capacity, measured, not assumed.** When a shared
   person becomes the queue (foundation PRs waiting, ADRs waiting, sign-offs waiting), the span
   is too wide — split the role before the pods start routing around it.
4. **Every shared role has a deputy.** Same bus-factor rule as in-pod, and the deputy comes from
   a pod, which keeps the shared role honest about ground truth.

### 3.2 What triggers a second pod

All four, not any one:

- [ ] The outcome genuinely needs parallel workstreams (scope, not impatience)
- [ ] Pod 1's flow is healthy: median review wait stable or falling for 4+ weeks, accepted-as-is
      trending up
- [ ] The harness is extracted and versioned well enough that pod 2 installs it rather than
      rebuilds it
- [ ] A second Pod Lead and at least two certified Orchestrator/Checkers actually exist

The measurable claim that proves the model is compounding: **pod 2 ships its first spec faster
than pod 1 did.** If it doesn't, the foundation isn't real yet — fix that before pod 3.

### 3.3 In-pod versus shared

| Role | Lives | Ratio | Notes |
|---|---|---|---|
| Pod Lead | In pod | 1 per pod | Never shared. Intent ownership doesn't split. |
| Orchestrator / Checker | In pod | 2-3 per pod | The swap rule needs at least 2. |
| Quality Engineer | In pod | 1 per pod | Machinery is per-product; standards are guild-shared (below). |
| Harness deputy | In pod (a hat) | 1 per pod | An Orchestrator who handles pod-local harness changes and reviews the shared maintainer's work. |
| Foundation Maintainer | Shared | 1 per 2-4 pods | The Setup Owner role, graduated. Half-time at 2 pods, full-time at 3+. Always with a named deputy. |
| Architect (design authority) | Shared | 1 per 2-3 pods | Signs ADRs, owns cross-pod technical coherence. At 1 pod this is the Setup Owner's other hat. |
| Manager of Agents (flow) | Shared | Appears at 3 pods; 1 per 2-3 pods | Watches cross-pod flow metrics, rebalances, removes blocks. A flow manager, not a people manager. |
| Security lead | Shared | 1 per engagement | Owns the HIGH-risk sign-off policy and the security-reviewer agent. A hat on the Architect or a QE until ~3 pods. |
| Engagement Lead | Shared | 1 per client | The client sees one face for steering. At 1 pod this is the Pod Lead. |
| Sponsor / Client PO | Client side | Per the SOW | PO mode: one PO can serve at most 2 pods before decision latency shows. |

### 3.4 One pod (5 people) — the typical team, mapped

```
POD 1
  Pod Lead            (was PM)         + wears Engagement Lead hat
  Setup Owner         (was Architect)  + wears design-authority and security-lead hats
  Orchestrator/Checker (was Dev 1)     + wears harness-deputy hat
  Orchestrator/Checker (was Dev 2)
  Quality Engineer    (was QA)         + in Checker rotation
```

Everything in section 2 as written. 2-3 parallel agent streams, capped by review wait.

### 3.5 Two pods (9-11 people)

The Setup Owner graduates: pod-local harness work goes to each pod's harness deputy; the
graduated role — now the **Foundation Maintainer** — owns what's shared.

```
SHARED (1.5-2 people of capacity, usually from pod 1 veterans)
  Foundation Maintainer   (was pod 1's Setup Owner) ~half-time
      owns the shared kit: CLAUDE.md baseline, skills, agents, hooks, workflows, profile
      reviews promotions: a pod wants its local skill shared -> promotion PR, maintainer gates it
      promotion bar: used by both pods or honestly general; three similar lines in two pods
      beat one premature shared abstraction
  Architect (design authority) ~half-time, often the same person at this scale only if
      the deputy rule still holds (their foundation PRs reviewed by a pod deputy)
  Engagement Lead: one of the two Pod Leads, named, owns client steering

POD 1                                POD 2
  Pod Lead                             Pod Lead
  Orchestrator/Checker x2              Orchestrator/Checker x2-3
  Quality Engineer                     Quality Engineer
  (one O/C wears harness-deputy hat)   (one O/C wears harness-deputy hat)
```

What changes operationally:

- **Harness becomes two-layer.** The shared kit is versioned and released by the Foundation
  Maintainer; each pod pins a version and layers pod-local additions in its own repo. Pods pull
  upgrades on their schedule; the maintainer never force-pushes convention changes mid-spec.
- **Promotion flow starts.** Pod-local skills/hooks that prove out get promoted to the shared
  kit by PR; the maintainer is the gate against junk-primitive flood.
- **Steering merges.** One biweekly client steering covering both pods, run by the Engagement
  Lead; each Pod Lead brings their pod's demo and scorecard. Pods keep their own daily/weekly
  cadences separately.
- **Cross-pod dependency rule.** A spec that needs a change in the other pod's area is checked
  by someone from *that* pod — the non-author rule applied at pod granularity.

### 3.6 Three pods (14-16 people)

Two roles stop being hats and become jobs:

```
SHARED (3-4 people)
  Foundation Maintainer    full-time now, + named deputy (a pod harness deputy, rotating)
  Architect                full-time across 3 pods; signs all ADRs; runs a monthly
                           cross-pod design review (the only new meeting at this scale)
  Manager of Agents        NEW. Owns cross-pod flow: watches review wait, accepted-as-is,
                           rework, and WIP per pod; rebalances specs between pods; kills or
                           splits streams when a pod's checking queue grows; runs the
                           cross-pod flow check (15 min, 3x week, Pod Leads attend).
                           Explicitly not a people manager: no reviews, no reporting lines.
  Security lead            now a real fraction of someone (usually the Architect or the
                           strongest QE): HIGH-risk sign-off policy, security agent tuning,
                           security-review wait watched as its own metric

POD 1            POD 2            POD 3
  (same 4-5 person shape as 3.5, every pod identical)
```

What changes operationally:

- **The QE guild forms.** The three Quality Engineers meet biweekly, own grader/eval standards
  jointly, and share check improvements through the foundation. Chaired by the security lead or
  the senior QE.
- **Metrics roll up.** Each pod's dashboard feeds an engagement dashboard the Manager of Agents
  and Engagement Lead read. Per-pod numbers are flow signals, never league tables — comparing
  pods on output recreates the velocity pathology with extra steps.
- **Foundation gets a release cadence.** Biweekly versioned releases with a changelog; pods pin
  and upgrade deliberately.

### 3.7 Four or more pods

This is past single-engagement scale and into the IDD Scale/Production stages
(`methodology/scaling/` in the IDD repo governs). The short version: replicate the 3.6 shared
group per 2-3 pods, add the quarterly org-level loop (portfolio steering, foundation funding),
and treat the foundation as a product with its own owner, deputy, roadmap, and users. Do not
invent a new coordination layer inside one client engagement — if one client needs 4+ pods,
the engagement should probably be two engagements with two outcomes.

### 3.8 The anti-patterns this structure exists to prevent

- **The seventh chair.** Growing a pod instead of splitting it. Past 6 people the flow check
  stops working and checking assignments blur.
- **The shared-role bottleneck.** Foundation PRs or ADRs queuing for days. The fix is narrowing
  the span or naming the deputy for real — not pods quietly forking the foundation.
- **The junk-primitive flood.** Promoting every pod-local convenience to the shared kit.
  The promotion bar exists; the maintainer's job is mostly saying "not yet."
- **Pod league tables.** Cross-pod output comparisons. The only cross-pod questions are flow
  questions: where is checking queuing, and why?
- **The absentee hat.** A shared role assigned to someone with no pod contact. Every shared
  role keeps one foot in real spec flow (deputy duty, checker rotation, or pairing) or their
  decisions drift from ground truth.
