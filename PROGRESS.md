# Delivery Standard — Progress Snapshot

**Last saved:** 2026-06-11
**Owner:** Matt Kruczek

This file is the resume point. Read it first next session.

---

## What this project is

A "gold standard" for how Matt's consulting team uses Claude (the AI coding agent) to build
software for clients — with a primary focus on **developing WITH agents** (and a secondary
AI-engineering track for when the deliverable IS agents). It synthesizes two source repos:

- `MCKRUZ/intent-driven-development` — the IDD methodology (the "why")
- `MCKRUZ/claude-code-sdlc` — the executable plugin (the "how": commands, agents, gates)

The standard lives in a NEW repo: **`MCKRUZ/delivery-standard`** (this folder). Not yet
`git init`ed — that's deferred to Matt.

---

## The 17 locked decisions (from the original grilling)

1. Deliverable focus: develop WITH agents (primary); AI-as-product is secondary.
2. Spine: **hybrid** — claude-code-sdlc phases open/close the engagement; the IDD build loop
   replaces phases 4-6. LESS automation than the plugin defaults; humans + AI collaborate at
   every phase.
3. Team: **4-6 person pod**, designed for that, with collapse rules for smaller.
4. Intent ownership: **varies** — client PO mode OR proxy mode (Pod Lead owns, client ratifies).
5. Stack default: **.NET 8 / Angular / SQL Server / Azure / GitHub Actions** (microsoft-enterprise profile).
6. Repos: client's org from day one.
7. Topology: harness in the delivery repo + a private internal foundation repo (Track C).
8. Branching: trunk-based, 1 spec = 1 branch = 1 PR.
9. Merge gate: grader in CI (advisory), human decides; hard blocks = build/test/lint/coverage/grader-ran/non-author-approval.
10. Claude access: client procures Anthropic access (their keys, their account).
11. Phase 1 (Foundation) exit: walking skeleton deployed to client dev env via pipeline.
12. Reporting: biweekly steering + working demo; NO activity metrics to client.
13. Risk tiers: Pod Lead assigns at triage (HIGH/MEDIUM/LOW taxonomy in GOLD-STANDARD.md §5).
14. Training: pod certified before; client trained during (priced workstream).
15. AI-engineering module: full rigor (evals as acceptance criteria, prompts tiered HIGH).
16. Commercial: thin chapter (SOW must-haves, PO clause, pricing posture).
17. Home: one repo = standard docs + installable kit.

---

## Files that exist (delivery-standard repo)

### Top level
- `GOLD-STANDARD.md` + `.html` — the master standard, 14 sections. The HTML is the front door
  with a linked deep-dive index. Calendar note: "Open 4-6 weeks" (corrected from 2-4).
- `PROGRESS.md` — this file.

### docs/ (deep-dives, each paired .md + .html, same dark-sidebar styling)
- `team.md/.html` — §3 deep-dive: old-role→new-role mapping (PM/Architect/2 devs/QA →
  Pod Lead/Setup Owner/Orchestrator-Checkers/Quality Engineer), concrete jobs, 1→3 pod scaling.
- `phase-0-discovery.md/.html` — Phase 0 (Discovery) deep-dive. **Tool-GENERIC** (no plugin
  names). 10-business-day calendar, who's involved, artifacts, cadences, exit gate, failure modes.
- `phase-0-example.md/.html` — Harbor Mutual worked example for Phase 0. **Tool-SPECIFIC**
  (names plugin commands).
- `phase-1-requirements.md/.html` — Phase 1 deep-dive. Tool-generic. 5-day calendar.
- `phase-1-example.md/.html` — Harbor Mutual Phase 1 example. Tool-specific.
- `phase-2-design.md/.html` — Phase 2 deep-dive. Tool-generic. 5-day calendar.
- `phase-2-example.md/.html` — Harbor Mutual Phase 2 example. Tool-specific.
- `phase-3-foundation.md/.html` — Phase 3 (Foundation) deep-dive. Tool-generic. Two-week
  calendar. The hinge phase: kit install, rails, first build-loop runs, walking skeleton
  deployed to client dev env.
- `phase-3-example.md/.html` — Harbor Mutual Phase 3 example. Tool-specific. Specs 0001-0004
  ride the full loop; 0002 is the HIGH-risk proving spec.
- `build-loop.md/.html` — the Build loop deep-dive (the heart of the method, expands
  GOLD-STANDARD §5): the three beats, the risk taxonomy, the 5-rung checking ladder, the
  weekly cadences, the client's view, hardening passes, metrics, failure modes. Tool-generic.
  Sources: GOLD-STANDARD §5/§9 + IDD course modules 2-5 (v2) + ceremonies/flow-check.md.
  NO worked example yet — that's the next doc to write.

### Referenced but NOT yet built (named in GOLD-STANDARD §10, do not exist as files yet)
- `docs/profile-swap.md`, `docs/commercial.md`, `docs/data-flow-brief.md`, `docs/po-onboarding.md`
- `kit/` — the entire installable engagement starter (CLAUDE.md.template, spec-template,
  settings.json, skills/, agents/ grader+security-reviewer, hooks/ stop-gate, workflows/
  ci+grader+security+deploy-dev, infra/ Bicep, profile/). NONE built yet.
- `retros/` — empty.

---

## The Harbor Mutual worked example (continuity facts — keep consistent)

Fictional regional insurer. Rebuild property-claims intake. Median 11.4 days FNOL→coverage
decision; target ≤5 days. Core system "PolicyOne" syncs nightly (the batch window). Phase 1
found a read-only nightly **snapshot replica**. Storm surge ~10x for a week. 61% of claims are
"simple" (fast-path). Auto-insurance must not be precluded (C-03 "auto-proof").

- **Pod:** Maya Chen (Pod Lead), Rob Feld (Setup Owner), Jonah Kim + Sara Whitfield
  (Orchestrator/Checkers), Nadia Brooks (Quality Engineer).
- **Harbor:** Karen Voss (VP Claims Ops, sponsor), Luis Ortega (PO, 6 hrs/wk), Priti Shah (BI/data),
  Dan Kowalski (IT security), Wes Carter (lead engineer, Phase 2 ADR co-signer), Dee Alvarez
  (intake supervisor), Gail Tran + Marcus Webb (senior adjusters).
- **ID schemes:** DOC-NN (docs), CON-NN (contradictions), Q-NN (open questions), C-NN (constraints),
  D-NN (decisions), E-NN (epics), REQ-NN (requirements), NFR-NN, ADR-NN. IDs are stable across phases.
- Dates: Phase 0 = engagement week of 2026-03-02; Phase 1 = wk 3/16; Phase 2 = wk 3/23
  (closed Friday 2026-03-27); Phase 3 = two weeks following.
- Open threads into Phase 3: Q-17 (postal vendor), Q-18 (surge load-test dataset). Walking
  skeleton = 4 sliced specs (0001 queue entry, 0002 replica verify, 0003 test-mode ack, 0004 metric event).
- **Phase 3 additions (keep consistent):** Wes Carter becomes the Setup Owner counterpart
  (pairs into the harness build, reviews adaptation PRs). NEW character: **Tom Reilly**,
  Harbor's platform engineer — owns branch protection, runners, secrets; reviews the pipeline
  he'll operate post-engagement. Jonah Kim is Rob's **named deputy** on the harness (the
  both-eyes rule). 0002 (replica verify) is the HIGH-risk spec that proves the security rails.
- **Build + Phase 7 additions (keep consistent):** Build ran 2026-04-13 to **2026-07-10**,
  feature-complete at **spec 0044**; both hardening passes done; WIP cap 6; review-wait
  tripwire = one working day. Build-example week = wk4 (5/4-5/8): specs 0015 (fast-path
  queue, MEDIUM) + 0016 (duplicate merge, HIGH; the empty-policy-number bucket catch; Wes
  signs). Phase 7 = **2026-07-13 to 07-17**, billing milestone 5. NEW character: **Ines
  Roy**, Harbor engineer hired 3 wks earlier — the README cold verifier (stalled at step 4:
  Key Vault perms; fixed same day). Tom cold-walks the RUNBOOK. Drift catalog: 2 entries —
  intentional `staleness_as_of` on REQ-014's degraded response; defect spec **0045**
  (claims-search bare 500). Decision sweep → **ADR-012** (surge queue retry/backoff) +
  **ADR-013** (claim-document retention tiering); ADRs complete through 013, none open.

---

## Established documentation conventions (apply to ALL future phase docs)

1. **Every page stands alone.** Each deep-dive opens with an "If you're starting here" primer;
   each example opens with "The story so far (you can start here)". Both are **scannable label
   tables** (NOT paragraphs): rows like The method / The rhythm / Where we are / Our pod /
   ID legend. Terms defined at first use; IDs legended; story recapped.
   **(2026-06-11, Matt feedback) NEVER cram multiple definitions into one table cell with
   mid-dots.** Vocabulary lives in its own two-column table ("Words this page leans on" —
   Term | What it means) directly after the primer; ID legends get the same treatment. Cells
   that merely list names with mid-dots are fine. And the casual-reader rule: every term of
   art on a page either appears in that vocabulary table or gets a short plain-language
   definition at first use in the body (grader, Stop hook, branch protection, WIP cap, etc.).
   Reference pattern: phase-3-foundation.md/.html.
2. **Abstractions are tool-GENERIC** (no claude-code-sdlc command names). **Examples are
   tool-SPECIFIC** (name the commands).
3. **Examples carry a per-day "Tooling" bar** showing exactly what ran. Taxonomy:
   - **Green pill = "You run it"** — a slash command you type (`/sdlc-gate`, `/sdlc-coach`).
   - **Slate pill = "It triggers"** — an agent/script the green command runs under the hood,
     ALWAYS shown after a `→` (never standalone).
   - **Grey pill = "No plugin command / Human-client"** — a meeting, client-system work, or an
     exploratory spike. Nothing the plugin drives.
   - Each day's bar is **stacked rows** (`<div class="trow">`), one command-group per line, so
     pills never run together. Each example has a legend table + a foot note.
   - **Drafting artifacts = `/sdlc-coach`** (fills the phase templates). Document intake =
     `/sdlc-intake`. NEVER show raw `.py` invocations — always the command that wraps them.
   - Templates are files Claude READS — named in artifacts, never as tool pills.
4. Each example ends with a "tooling behind this phase" table (artifact → how produced).
5. Plain language, no consultant-speak, no emojis (Matt is firm). Straight quotes.
6. Cross-link: gold standard → deep-dive → example → next phase, in BOTH formats.
7. HTML styling: shared dark-sidebar template, accent #0f5c8c, pill CSS, legend-tbl, trow flex.
   Re-render HTML after any .md edit (they're paired).
8. **Forward nav, two places in HTML:** a bottom `callout` "Next:" link (all pages) AND a
   sidebar `class="back"` "Next: ... →" link with `margin-top: 16px` (introduced with the
   Phase 3 pages; retrofitted to phase-2-design and phase-2-example). Markdown pages carry the
   bottom "Next:" link only. NOTE: phase-0/1 pages still lack the sidebar next link —
   inconsistency flagged for cleanup, not yet retrofitted.

---

## Changes made to claude-code-sdlc (the plugin repo)

These are NEW additions Matt asked for, sitting uncommitted in that repo's working tree:

- **`agents/discovery-analyst.md`** — cross-document analysis (contradictions + questions).
  Has standalone mode (`--docs`).
- **`commands/sdlc-brief.md`** — `/sdlc-brief`: workshop brief with curation HITL gate.
- **`commands/sdlc-intake.md`** — `/sdlc-intake`: wraps `intake_documents.py` (so nobody calls
  the .py directly). NEWEST addition.
- **`templates/phases/00-discovery/`** — added `contradiction-list.md`, `question-list.md`,
  `workshop-brief.md`.
- **`phases/00-discovery.md`** — added Step 0c (now points to `/sdlc-intake`) and Step 0d
  (discovery workshop prep, conditional, questions-only HITL rule).
- **Docs caught up:** `docs/agents.md` (4→8 agents documented), `docs/commands.md` (now lists
  all 12 incl. /sdlc-intake, /sdlc-brief, /sdlc-enhance, /sdlc-coach, /sdlc-review),
  `references/agent-roster.md`, `CLAUDE.md` (12 commands, 8 agents, + "Standalone or Workflow"
  design rule: every agent/command runs both in-workflow and standalone).
- Plugin now: **12 commands, 8 agents.**
- **Removed:** the `examples/phase-0-discovery/` folder I initially added there (content moved
  to delivery-standard/docs/phase-0-example).

Nothing committed in either repo. Both working trees are dirty and ready for Matt's review.

---

## Open question Matt should weigh in on

- I represent **`/sdlc-coach`** as the artifact-drafting command. Accurate (it's the plugin's
  artifact-producing dialogue command), but a pod could instead run `/sdlc` (phase guidance) +
  draft manually. If the team's real habit is `/sdlc`, switch the drafting-day pills.

---

## NEXT STEPS (where to resume)

Phases done as deep-dive + example: **0, 1, 2, 3.** Phase 3 (2026-06-11) is fully cross-linked
in both formats and indexed in GOLD-STANDARD §10. Matt has NOT yet reviewed the rendered
Phase 3 HTML. Remaining work, in likely order:

1. ~~Build loop deep-dive + worked example~~ DONE 2026-06-11: `build-loop.md/.html` +
   `build-loop-example.md/.html` (week four of Build, Mon 5/4-Fri 5/8 2026; specs 0015
   fast-path work queue MEDIUM + 0016 duplicate-claim merge HIGH; the grader catches the
   empty-policy-number match-bucket bug — eleven green tests, live bug; Wes's named HIGH
   sign-off; Q-18 lands; security-queue drift flagged at 2.1 days). Fully cross-linked:
   GOLD-STANDARD §1+§5, phase-3-foundation, phase-3-example. Specs 0005-0014 exist by
   week 4 but are not itemized — keep future references consistent.
2. ~~Casual-reader clarity pass~~ DONE 2026-06-11 (all four phase pairs + examples; team.md
   was already clean; see convention 1 for the binding rules).
3. ~~Phase 7 (Documentation)~~ DONE 2026-06-11: `phase-7-documentation.md/.html` +
   `phase-7-example.md/.html`, fully cross-linked (build-loop pair Next links, GOLD-STANDARD
   index). Phase 7 ends with Back-link only — add its Next link when phase-8 exists.
4. ~~Phase 8 (Deployment)~~ DONE 2026-06-11: `phase-8-deployment.md/.html` +
   `phase-8-example.md/.html`, fully cross-linked. **Phase 8 continuity facts:** week =
   2026-07-20 to 07-24; go-live **Thu 2026-07-23 07:00**, rc-1.0.1, billing milestone 6.
   Rollout shape = cutover at intake (new FNOLs only; in-flight claims drain in legacy; no
   migration; legacy fallback warm 30 days; triggers: >2% intake errors 30 min sustained, or
   verification down outside replica window with growing queue). Tue rehearsal rollback
   FAILED (config keys moved ahead of artifact) → **spec 0046** (config versioned with the
   release artifact); re-rehearsed clean Wed. Go/no-go: 7 named roles, Dan held until the
   rotation record was attached. First real FNOL Thu 08:14 (burst pipe, portal): coverage
   recommendation in **3h 06m**; 27 claims day one. Secrets rotated — pod never held prod
   values. Hypercare = two weeks; day-one finding: ack-dispatch retry burst during postal
   vendor blip → Phase 9 alert candidate. Phase 8 ends with Back-link only — add its Next
   when phase-9 exists.
5. ~~Phase 9 (Monitoring)~~ DONE 2026-06-11: `phase-9-monitoring.md/.html` +
   `phase-9-example.md/.html`, fully cross-linked. **Phase 9 continuity facts:** two weeks
   inside hypercare, 2026-07-27 to 08-07; gate = hypercare end; billing milestone 7. Six
   alerts shipped (VERIFY-DEGRADED w/ 02:00-04:30 suppression window + recovery check,
   SYNC-MISSED, QUEUE-DEPTH — modeled from Q-18, revisit at first CAT event, INTAKE-ERROR-RATE
   — same 2%/30min number as the Phase 8 fallback trigger, ACK-RETRY-BURST, EVAL-GATE-DRIFT);
   two cut at fatigue review. Baseline: portal p95 410ms, replica verify p95 165ms, error
   0.3%, queue <40, ack median 22min. Drill 8/5: VERIFY-DEGRADED routing typo caught + one
   pod-permissions playbook link — both fixed, re-drilled. Retro receipts: accepted-as-is
   84%, 4 escaped bugs total, security queue 2.1d vs 0.9d (fix: committed twice-weekly
   security slot), Luis 31/34 decisions inside clock. Debt log: un-merge path (Q4 2026),
   legacy fallback decommission (Tom, day 30), modeled surge thresholds (Priti). Harvest
   list (4): config-with-artifact, timezone test pattern, suppression-window alert pattern,
   vendor-blip severity split. First metric read: fast-path median **1.9 days** (overall
   median needs a quarter — caveat stated). Phase 9 ends with Back-link only — add Next when
   phase-C exists.
6. **Phase C (Close & Transfer)** deep-dive + example — the last phase pair; completes the
   engagement arc. C's gate: client team runs one real spec end-to-end without us driving
   (GOLD-STANDARD §13). The harvest PR opens here (the 4-item list above).
3. **Build the `kit/`** — the actual installable artifacts (templates, agents, hooks, CI YAML,
   Bicep). Currently only described in GOLD-STANDARD §10, not built. Phase 3 docs now name its
   contents in use — keep the kit consistent with what the example shows running.
4. **The four `docs/` support files** (profile-swap, commercial, data-flow-brief, po-onboarding).
5. Optional cleanup: retrofit the sidebar "Next" link to the phase-0/1 pages (convention 8).
6. Eventually: `git init` both repos, commit, push (Matt's call — deferred).

Matt works through this incrementally: typically "do the deep-dive, then the example, then move
to the next phase," reviewing the rendered HTML between steps.
