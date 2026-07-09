# Plugin sync — reconciling `claude-code-sdlc` with the standard

> **Status:** change spec, not yet applied. Nothing in `MCKRUZ/claude-code-sdlc` was modified.
> **Written:** 2026-07-09, while rewriting the per-phase Example tabs against the plugin's real behavior.
> **Premise:** `claude-code-sdlc` is the mechanism; this standard is the process that documents it. They
> should be in sync. The legitimate difference is that the standard carries far more human-in-the-loop
> work than the plugin performs — and that difference should be *visible and recorded*, not silent.

---

## The one finding that matters

**The human gate is real. What it asks for is not.**

`advance_phase.py` will not move an engagement forward without `--confirmed`. That flag represents a named
person's sign-off, and there is no path around it. The machine cannot walk a client engagement forward on
its own. This is exactly what the standard promises — *gates report, humans decide* — and it is faithfully
implemented.

But grep `exit_gate` or `conditions` across every script in the plugin and you get **zero hits**:

```
$ grep -rn "exit_gate\|conditions" scripts/*.py
(no output)
```

`phase-registry.yaml` declares each phase's exit conditions. **No code ever reads them** — not to check
them (many are unmachineable, and that's fine), not even to *display* them.

So a human is stopped at the gate and asked to sign. What they are shown is `check_gates.py`'s output: a
list of files that exist, are non-empty, and do not contain the strings `TODO`, `TBD`, `${`,
`PLACEHOLDER`, `[INSERT`, or `<!-- REQUIRED:`. The ten-bullet checklist they should be signing *against* —
*every ADR carries two signatures; every integration was spiked against the live system; no orphans in
either direction; the threat review happened* — sits in a YAML file that nothing opens.

The standard has the checklist. The plugin has the gate. Nothing connects them.

### Fix 1 — render the exit-gate conditions at the moment of sign-off

`check_gates.py` should read `exit_gate.conditions[]` from the registry and emit every prose condition as a
`MANUAL` result (`passed: None`) alongside the automated artifact checks. `advance_phase.py` already
handles `passed is None` correctly — it prints `REVIEW REQUIRED — N manual gate(s) need human sign-off`
and refuses to advance without `--confirmed`. The plumbing exists. Only the input is missing.

Effect: the human sees what they are vouching for. No new blocking behavior; nothing that passes today
starts failing. This is the highest-value, lowest-risk change in this document, and it should ship first
and alone.

### Fix 2 — the `approval` field is dead

`phase-registry.yaml` sets `approval: manual` on all nine phases. No script reads it:

```
$ grep -rn "approval" scripts/ | grep -v tests/ | grep -v risk_model | grep -v validate_profile
scripts/advance_phase.py:5:  AND manual approval has been given (--confirmed flag), advances state.yaml
```

— and that is a docstring. Either wire the field or delete it. A configuration key that nothing reads is a
lie the next maintainer will believe.

---

## The second finding: human work leaves no receipt

The standard requires a pod to do a great deal that no command performs. Some of it can never be
automated — that is the point. A spike is a person touching a live system; a threat review is an argument
in a room. But **human work without a receipt cannot be gated, cannot be reported, and cannot be audited a
year later.**

Phase C already shows the right pattern — three times over. `close-gate-evidence.md`, `harness-audit.md`
and `access-revocation-checklist.md` are all registry-required, gate-checked files that record human
rituals no command can perform: the client's own engineer shipping one real change alone with the pod
silent in the room; the audit of everything still living in our heads; the proof that our access was
actually revoked. A person does the work; a file records that it happened; the gate can see it.

**Phase C is the only phase that does this.** Every artifact in the standard is one of three things, and
the middle one is the one to grow. Counted across the ten rewritten Example-tab ledgers — one hundred
artifacts, the whole engagement:

| | Written by | Gate sees it | Count |
|---|---|---|---|
| **Machine artifact** | a command | yes | **55** |
| **Human receipt** | a person | yes | **3** — all three in Phase C |
| **Unrecorded work** | a person | no | **42** — spread across every other phase |

Forty-two. The threat review. Every spike. The consistency check. The cold-checkout test. The rollback
rehearsal. The alert drill. The go/no-go ceremony. The option session. Each one is load-bearing, each one
is the reason a client pays for a pod rather than a prompt, and none of them leaves a trace a machine or
an auditor can find.

The per-phase breakdown, by drift kind, from the nine reconciliation passes (75 rows; full tables in the
appendix below):

| Page | Missing artifact | Undocumented output | Name mismatch | Internal contradiction | Other | Total |
|---|---|---|---|---|---|---|
| Phase 0 | 2 | 5 | 2 | 4 | — | 13 |
| Phase 1 | 4 | 3 | 4 | 2 | — | 13 |
| Phase 3 | 3 | 1 | 1 | 1 | 1 wrong-phase | 7 |
| Phase 7 | 3 | — | — | 4 | — | 7 |
| Phase 8 | 3 | 2 | 2 | 3 | — | 10 |
| Phase 9 | 4 | 1 | — | 3 | — | 8 |
| Phase C | 2 | — | 2 | 3 | — | 7 |
| Build loop | — | 3 | — | — | 1 wrong-framing | 4 |
| The Rails | 2 | 1 | 1 | 2 | — | 6 |
| **Total** | **23** | **16** | **12** | **22** | **2** | **75** |

**Fix 3 — apply the `close-gate-evidence.md` pattern to the other unreceipted rituals.** For each, add an
artifact spec to the phase body and a `required` (or `optional`) entry to the registry. Claude does not
perform the work; it prompts for the receipt and refuses to leave the field blank.

The candidates are listed per phase below. The pattern is invariant:

```yaml
# phases/phase-registry.yaml
artifacts:
  required:
    - "spike-findings.md"      # human runs the spike; the finding is written down
```

```markdown
### `spike-findings.md` (REQUIRED)
Per risky assumption: what was assumed, what was tested against which live system, what was found,
and whether the assumption survived. The spike code is deleted. The finding is not.
> **HITL GATE:** Claude does not run spikes. Ask the human which integrations the design depends on,
> and refuse to advance until each has a recorded finding or an explicit, named waiver.
```

---

## Cross-cutting defects found while reconciling

| # | Kind | Detail | Where |
|---|------|--------|-------|
| X-1 | DEAD-CONFIG | `exit_gate.conditions[]` parsed by nothing | `phases/phase-registry.yaml` → all phases |
| X-2 | DEAD-CONFIG | `approval: manual` read by nothing | `phases/phase-registry.yaml` → all phases |
| X-3 | STALE-REFERENCE | Phase 7's Entry Criteria requires "Phase 6 exit gate passed". Phases 4/5/6 do not exist — they were collapsed into the Build loop. Phase 1 also points NFR thresholds at "Phase 6" measurement | `phases/07-documentation.md`, `phases/01-requirements.md` |
| X-4 | WRONG-FRAMING | The registry models `build` as a gated phase with `artifacts.required: [phase7-handoff.md]` and `approval: manual`. The standard is explicit that the Build loop **has no gate** — it has a merge bar every change clears, and it ends when a human declares feature-complete | `phases/phase-registry.yaml` → `build` |
| X-5 | INTERNAL-CONTRADICTION | Phase 2's Exit Criteria require `architecture-diagrams.html` and `deep-plan-checkpoint.yaml`, but the registry marks the first RECOMMENDED and the second Optional — so `check_gates.py` never checks either, and the exit criteria are decorative | `phases/02-design.md` vs registry |
| X-6 | INTERNAL-CONTRADICTION | `close-handoff.md` is a registry-required Phase 9 artifact with **no Artifact Specification** in the phase body. It is produced but unspecified | `phases/09-monitoring.md` |
| X-7 | WEAK-CHECK | `exists_and_complete` is a placeholder-token scan, not a completeness check. A directory (`adrs/`) passes on being non-empty. Cross-reference and cross-phase-consistency checks are `SHOULD` severity and never block | `scripts/check_gates.py` |
| X-8 | WRONG-PHASE | Threat modeling appears only in `phases/03-foundation.md`. The standard runs a **design-level** threat review in Phase 2, producing the mitigation map that becomes Phase 3's build-time security gates. **Resolution: it is genuinely both** — a design-level review in Phase 2, and a foundation-level pass in Phase 3 confirming the gates got wired. Both phases need the step | `phases/02-design.md`, `phases/03-foundation.md` |

---

## Three functional defects — these are bugs, not documentation drift

Each was found while reconciling the docs, and each was then confirmed by reading the plugin's code
directly. They are ordered by how badly they break a real engagement.

### D-1 — Phase 2's blocking human gate reads a section nothing writes

`phases/02-design.md` Step 0 is the most important human gate in the method:

> **HITL GATE:** Read `phase2-handoff.md`. Extract every **AQ-NN** (Architectural Question) listed in
> **"What Design Must Address"**. For each AQ, present 2–3 concrete options … Collect human decisions for
> ALL AQs **before writing any artifact**. These human decisions become the ADRs — Claude encodes them,
> not invents them.

The string `AQ` does not appear anywhere in `phases/01-requirements.md`. Phase 1 is never told to write a
"What Design Must Address" section, never told to assign `AQ-NN` identifiers. Its `phase2-handoff.md`
artifact spec requires six sections; the nearest is *"Open questions Phase 2 must resolve"* — a different
name with no ID scheme.

```
$ grep -rn "AQ\|What Design Must Address" phases/01-requirements.md
(no output)
$ grep -rl "AQ-NN" phases/ commands/
phases/02-design.md
commands/sdlc-next.md
```

**Consequence.** Phase 2's gate has no defined input. Claude improvises architectural questions from
whatever it finds. The ADRs that result — the signed, two-signature, this-is-why records the whole
engagement rests on — trace back to identifiers the process never assigned.

**Fix.** Add `AQ-NN` to Phase 1's `phase2-handoff.md` artifact spec as a required "What Design Must
Address" section, with an ID scheme and one line per question. Phase 1's exit gate should refuse to close
with an architectural implication that has no `AQ-NN`. This closes the loop that Phase 2 already assumes.

### D-2 — Phase 7's gate checks a copy of the deliverable, not the deliverable

`check_gates.py` resolves every required artifact under the phase's own directory:

```python
artifacts_dir = artifacts_base / phase_def["slug"]      # .sdlc/artifacts/07-documentation
path = artifacts_dir / artifact                          # …/07-documentation/README.md
```

There is no special-casing for `README.md` or `RUNBOOK.md` anywhere in the file. But Phase 7's own
guidance says: *"Test your README against a fresh checkout — clone the repo to a temp directory and follow
the instructions verbatim."* That can only mean the **repo-root** README.

**Consequence.** Either a team duplicates `README.md` into `.sdlc/artifacts/07-documentation/`, where it
immediately drifts from the real one, or Phase 7's gate never opens. The phase whose entire purpose is
*prove a stranger can run it* validates a file no stranger would ever run from.

**Fix.** Let an artifact declare its location. Simplest form — a path-bearing entry in the registry:

```yaml
artifacts:
  required:
    - "api-docs.md"                       # relative to the phase dir, as today
    - path: "README.md"   root: repo      # resolved from the repo root
    - path: "RUNBOOK.md"  root: repo
```

### D-3 — the gate ignores `project_type`; five phase bodies do not

`phases/{00,03,07,08,09}-*.md` adapt their required artifacts by `project_type` (read from `state.yaml`).
Phase 7 is explicit: a `library` or `cli` project should *"Skip RUNBOOK — there is no server to operate"*,
and a `skill` project should skip `api-docs.md` too.

```
$ grep -rn "project_type" scripts/check_gates.py scripts/phase_model.py
(no output)
```

`artifacts.required[]` is a static list. `RUNBOOK.md` and `api-docs.md` are on it unconditionally.

**Consequence.** Every non-service project is instructed to skip artifacts the gate then blocks on.
`claude-code-sdlc` cannot close Phase 7 on a CLI, a library, or a skill — including, presumably, on itself.

**Fix.** Make `artifacts.required[]` conditional on `project_type`, or move the project-type variants into
the registry so one source of truth governs both the body and the gate.

---

## Per-phase drift

Every row from the nine reconciliation tables, per phase, with the systemic issues folded up into the
cross-cutting table (X-1..X-8) and the three functional defects (D-1..D-3) above rather than repeated here.
Where a phase's original row was only a local instance of one of those, it is suppressed and named in the
note under that phase's table. Phase 2 is reconciled by hand; its rows are derived from the prose above.

### Phase 0 — Discovery

Standard = `docs/companion/phase-0.html` Reference track + `GOLD-STANDARD`; plugin = `phases/00-discovery.md` + `phase-registry.yaml` + `scripts/check_gates.py`.

| # | Kind | The standard says | The plugin does | Where |
|---|------|-------------------|-----------------|-------|
| 0-1 | MISSING-ARTIFACT | "PO decision record — owned by Sponsor — mode chosen in writing; PO named with committed hours, or a proxy rider signed." It is an exit-gate item with billing teeth. | No artifact. Not in `artifacts.required` or `artifacts.optional`; no step writes a `po-decision-record.md`. The PO fact survives only if a human folds it into `constitution.md` (Decision Authority). | standard Reference "The artifacts" row 7 vs `phase-registry.yaml` Phase 0 `artifacts.*` + `phases/00-discovery.md` (no step) |
| 0-2 | MISSING-ARTIFACT | "Tooling record — owned by Setup Owner — Anthropic access live under the client's account, or a fallback rider signed with a date." Exit-gate item with billing teeth. | No artifact. Not in the registry; no step writes a `tooling-record.md`. Survives only folded into `constraints.md` (C-06). | standard Reference "The artifacts" row 8 vs registry Phase 0 `artifacts.*` |
| 0-3 | UNDOCUMENTED-OUTPUT | The workshop brief is a real Phase 0 artifact (curated by a human, questions only) that the outcome workshop runs on. | Step 0d / `/sdlc-brief` drafts it and a HITL gate governs it ("curated, not generated"), but it is in neither `artifacts.required` nor `artifacts.optional`, is never committed, and the gate never sees it. | `phases/00-discovery.md` Step 0d + line 74 HITL vs `phase-registry.yaml` `artifacts.*` |
| 0-4 | NAME-MISMATCH | "Decision list — owned by Pod Lead — every unmade decision named; answered, or carried to the handoff as a numbered question." | Emits `question-list.md` (Q-NN entries + resolution logs) via Step 0d. Same object; the plugin never calls it a "decision list." | standard Reference "The artifacts" row 5 vs `phases/00-discovery.md` Step 0d |
| 0-5 | UNDOCUMENTED-OUTPUT | (Implicit — the contradiction analysis is the phase's signature technique; its output is a named artifact CON-NN.) | Step 0d writes `.sdlc/artifacts/00-discovery/contradiction-list.md` (CON-NN), but it appears in neither `artifacts.required` nor `artifacts.optional`, and `check_gates.py` never checks it. | `phases/00-discovery.md` Step 0d vs registry `artifacts.*` |
| 0-6 | UNDOCUMENTED-OUTPUT | The question/decision list is a tracked Phase 0 artifact carried into Phase 1 under original IDs. | Step 0d writes `.sdlc/artifacts/00-discovery/question-list.md`, but the registry lists it under neither required nor optional; nothing gate-checks it. | `phases/00-discovery.md` Step 0d vs registry `artifacts.*` |
| 0-7 | INTERNAL-CONTRADICTION | "Document registry — owned by Setup Owner — every document has a DOC ID and summary; contradictions listed." Treated as a core Phase 0 artifact; the whole engagement's DOC-NNN traceability depends on it. | Registry marks `document-registry.md` **optional**, "opt-in via `profile.documentation`." If the profile flag is off, the engagement's traceability spine is simply not produced. | registry `artifacts.optional` (`document-registry.md`) vs standard Reference "The artifacts" row 6 |
| 0-8 | UNDOCUMENTED-OUTPUT | (Not in the standard's Phase 0 artifact table at all.) | Step 0b (brownfield detection) writes `.sdlc/artifacts/00-discovery/workspace-analysis.md`; it is in neither the registry nor the standard's artifact list. | `phases/00-discovery.md` Step 0b vs registry `artifacts.*` + standard Reference artifacts |
| 0-9 | NAME-MISMATCH | (Standard doesn't name the report file.) The registry itself names the optional report `phase0-report.html`. | Step 8 writes `.sdlc/reports/phase00-report.html` (double-zero). The registry's own optional entry (`phase0-report.html`) doesn't match the path the phase body emits. | registry `artifacts.optional` (`phase0-report.html`) vs `phases/00-discovery.md` Step 8 |
| 0-10 | UNDOCUMENTED-OUTPUT | (No visual-report artifact named.) | Step 7 (`/visual-explainer`) writes `.sdlc/reports/phase00-visual.html`; the registry lists no visual report artifact of any name. | `phases/00-discovery.md` Step 7 vs registry `artifacts.*` |

Also affected by X-1, X-2: the three original exit-gate rows — the sponsor signature on the constitution, the success metric "read from its source system," and the two billing-teeth preconditions (PO decision in writing; Anthropic access live or fallback rider) — are all invisible to `check_gates.py` because the registry's exit conditions and its `approval: manual` field are read by nothing.

### Phase 1 — Requirements

Standard = `docs/companion/phase-1.html` Reference track; plugin = `phases/01-requirements.md` + `phase-registry.yaml` (`artifacts.required = requirements.md, non-functional-requirements.md, epics.md, phase2-handoff.md`).

| # | Kind | The standard says | The plugin does | Where |
|---|------|-------------------|-----------------|-------|
| 1-1 | MISSING-ARTIFACT | Decision list / decision log — continuously regenerated, the PO's work queue, every open call numbered + owned + aged on a 2-business-day clock; "empty, or every survivor is a numbered open question with an owner and a due date" at the gate | No decision-list file exists in Phase 1. Step 0 HITL only *asks* the human whether open questions are answered, in conversation via `AskUserQuestion`; nothing writes, ages, or gate-checks a list. The SOW's 2-day clock has no artifact behind it. | `01-requirements.md` Step 0; `phase-registry.yaml` Phase 1 `artifacts.required` (4 files, no decision log) |
| 1-2 | MISSING-ARTIFACT | Feasibility spike notes — Orchestrators run read-only feasibility spikes against handoff risks; each risk verified against the live system or converted to a requirement change; owned by Pod Lead | The word "spike" appears nowhere in `01-requirements.md`. No command runs one; no file records findings. (At Harbor the spike is what found the PolicyOne snapshot replica → Q-15.) | `01-requirements.md` (all steps); `phase-registry.yaml` |
| 1-3 | MISSING-ARTIFACT | Scope-out record — the explicit not-in-v1 list, shown to the sponsor at the review; a gate item ("the scope-out record exists and the sponsor has seen it") | No scope-out file. Step 4 only says "Confirm P3 items are genuinely deferred"; Guidance says P3 items are "documented, not ignored — they become Phase 2 scope inputs" but names no artifact and no location. | `01-requirements.md` Step 4 + Guidance; `phase-registry.yaml` |
| 1-4 | MISSING-ARTIFACT | Adversarial review record — a day-5 *structured adversarial review* (`/sdlc-review --adversarial` → `multi-reviewer`) that attacks the set from product/quality/security and produces catches (REQ-022 bounce-to-postal; the fast-path/regulatory-clock conflict) | Phase 1 Step 4 is a plain human "Stakeholder Review" walk-through. The phase body never mentions `/sdlc-review`, an adversarial pass, or a review-record artifact; nothing writes the catches down. | `01-requirements.md` Step 4 vs standard calendar day 5 |
| 1-5 | NAME-MISMATCH | "Error behavior specs (top tiers)" listed as a distinct owned artifact (Claude drafts / Pod Lead + QE) | Required as an "Error Specification" (Accepts / Returns / Errors) **section inside `requirements.md`** (Step 1) — no independent file, no independent gate. | `01-requirements.md` Step 1 + `requirements.md` Artifact Spec |
| 1-6 | NAME-MISMATCH | "Traceability matrix" listed as a distinct owned artifact (Claude / QE), requirement→source and requirement→outcome | Required as a "Traceability matrix" **section inside `requirements.md`** — no independent file. (Note: the standard adds an outcome-trace column; the plugin's matrix traces requirement→Phase 0 stakeholder pain only.) | `requirements.md` Artifact Spec |
| 1-7 | NAME-MISMATCH | "Epic map" and "User stories" listed as two separate artifacts (Epic map owned by PO; User stories drafted by Claude) | One file, `epics.md`, holds both — the "as a / I want / so that" story format *is* the epic content (Step 3). No separate user-stories artifact. | `01-requirements.md` Step 3 + `epics.md` Artifact Spec |
| 1-8 | UNDOCUMENTED-OUTPUT | The Reference 11-row artifact table never lists a gate HTML report (closest is the optional "Narrative companion") | Step 7 (`/sdlc-gate` → `generate_phase_report.py`) writes `.sdlc/reports/phase01-report.html` — the self-contained sponsor-read gate report. | `01-requirements.md` Step 7 |
| 1-9 | UNDOCUMENTED-OUTPUT | Standard names only a "Narrative companion (optional)" (Claude / Pod Lead edits) | Step 6 (`/visual-explainer`) writes `.sdlc/reports/phase01-visual.html`, described as "the stakeholder review artifact" — a specific file/path the standard never names. | `01-requirements.md` Step 6 |
| 1-10 | UNDOCUMENTED-OUTPUT | The standard never mentions a glossary artifact for Phase 1 | `phase-registry.yaml` Phase 1 `artifacts.optional` includes `glossary.md`. | `phase-registry.yaml` Phase 1 `artifacts.optional` |
| 1-11 | NAME-MISMATCH | Exit gate requires "the top tier respected its budget" — a hard P0 cap (12 slots at Harbor) enforced in the priority session, with a cut list | `requirements.md` carries a Priority column (P0/P1/P2/P3), but the plugin has **no budget/cap concept** and no record of what was cut to fit it. The priorities exist; the budget and the cut decision do not. | Standard Phase 1 exit gate vs `01-requirements.md` Step 1 priorities |

Also affected by D-1, X-3: the original AQ-NN handoff seam — Phase 2 Step 0 extracts `AQ-NN` from a "What Design Must Address" section Phase 1's `phase2-handoff.md` spec never writes — is D-1; the `[aspirational — validate in Phase 6]` NFR routing to a Phase 6 that does not exist (the registry collapses Implementation/Quality/Testing into the Build loop) is X-3.

### Phase 2 — Design

Reconciled by hand; its drift lives in the prose above. Standard = the Phase 2 companion Reference track, whose artifact table names **11 artifacts** and shows no filename anywhere; plugin = `phases/02-design.md` + `phase-registry.yaml`, whose `artifacts.required` names **5** (`design-doc.md`, `api-contracts.md`, `adrs/`, `adr-registry.md`, `phase3-handoff.md`).

| # | Kind | The standard says | The plugin does | Where |
|---|------|-------------------|-----------------|-------|
| 2-1 | MISSING-ARTIFACT | Spike findings — per risky assumption, what was assumed, what was tested against which live system, and whether the assumption survived. | The word "spike" appears in **no plugin phase file at all**. No step runs one; no artifact records findings. | standard Phase 2 artifact table vs `phases/02-design.md` (no "spike") + `phase-registry.yaml` |
| 2-2 | MISSING-ARTIFACT | The NFR proving plan names, per NFR, the measurement method and the place its number will later be read; Phase 9 cashes it. | No Phase 2 step emits a proving plan; the read-location promises exist nowhere in tooling. | standard Phase 2 artifact table vs `phases/02-design.md` + `phase-registry.yaml` (cf. row 9-5) |
| 2-3 | MISSING-ARTIFACT | The walking-skeleton definition names the thinnest end-to-end slice Phase 3 builds against. | No Phase 2 artifact records it; Phase 3 Step 5d is told to "verify against the Phase 2 walking-skeleton definition" — a definition not on disk. | standard Phase 2 artifact table vs `phases/02-design.md` + `phase-registry.yaml` (cf. row 3-3) |
| 2-4 | MISSING-ARTIFACT | The consistency-check record — the design read back against requirements and NFRs, contradictions listed and resolved. | No Phase 2 step emits it; no `consistency-check.*` in `artifacts.required` or `artifacts.optional`. | standard Phase 2 artifact table vs `phase-registry.yaml` |
| 2-5 | NAME-MISMATCH | The standard's "Design document" (no filename shown anywhere). | Required as `design-doc.md`. Same object; the standard never prints the filename. | standard Phase 2 artifact table vs `phase-registry.yaml` `artifacts.required` |
| 2-6 | NAME-MISMATCH | The standard's "Phase 3 handoff" (no filename shown). | Required as `phase3-handoff.md`. Same object; the standard never prints the filename. | standard Phase 2 artifact table vs `phase-registry.yaml` `artifacts.required` |
| 2-7 | NAME-MISMATCH | The standard's "Integration design". | Maps to the **optional** `integration-notes.md` — same object, plugin filename, and demoted to optional. | standard Phase 2 artifact table vs `phase-registry.yaml` `artifacts.optional` |
| 2-8 | NAME-MISMATCH | The standard's "data model" is a Phase 2 output. | It is plugin **Step 6** but has **no artifact file** — folded into `design-doc.md`. Logged NAME-MISMATCH, not INTERNAL-CONTRADICTION: it is the same object with no independent file (nothing self-contradicts — the plugin never claims a separate data-model artifact), exactly parallel to Phase 1's error-spec and traceability sections folded into `requirements.md`. | `phases/02-design.md` Step 6 vs `phase-registry.yaml` `artifacts.required` |
| 2-9 | UNDOCUMENTED-OUTPUT | (Not in the standard anywhere.) | `phase-registry.yaml` requires `adr-registry.md`; it appears nowhere in the standard. | `phase-registry.yaml` `artifacts.required` vs standard Phase 2 artifact table |
| 2-10 | UNDOCUMENTED-OUTPUT | (Not in the standard anywhere.) | `architecture-diagrams.html` is emitted; it appears nowhere in the standard. | `phases/02-design.md` + `phase-registry.yaml` vs standard (see X-5) |
| 2-11 | UNDOCUMENTED-OUTPUT | (Not in the standard anywhere.) | `research-notes.md` appears nowhere in the standard. | `phase-registry.yaml` vs standard |
| 2-12 | UNDOCUMENTED-OUTPUT | (Not in the standard anywhere.) | `deep-plan-checkpoint.yaml` appears nowhere in the standard. | `phases/02-design.md` + `phase-registry.yaml` vs standard (see X-5) |
| 2-13 | UNDOCUMENTED-OUTPUT | (Not in the standard anywhere.) | `external-reviews/` appears nowhere in the standard. | `phase-registry.yaml` vs standard |
| 2-14 | UNDOCUMENTED-OUTPUT | (Not in the standard anywhere.) | `.sdlc/reports/phase02-report.html` appears nowhere in the standard. | `phases/02-design.md` vs standard |

Also affected by X-8, D-1, X-5: the threat model + mitigation map — a Phase 2 design-level output the plugin omits — is X-8; the AQ-NN contract Phase 2's Step 0 gate depends on is D-1; and `architecture-diagrams.html` (2-10) and `deep-plan-checkpoint.yaml` (2-12) are the two artifacts X-5 flags as required by Phase 2's Exit Criteria but marked recommended/optional in the registry, so `check_gates.py` never checks either.

### Phase 3 — Foundation

Standard = `docs/companion/phase-3.html` Reference track + Phase 2 handoff; plugin = `phases/03-foundation.md` + `phase-registry.yaml` + `scripts/check_gates.py`.

| # | Kind | The standard says | The plugin does | Where |
|---|------|-------------------|-----------------|-------|
| 3-1 | MISSING-ARTIFACT | The **data-flow brief** is a Phase 3 artifact (Reference artifacts table, owned by Setup Owner): "Client security has, in writing: what goes to the API, what doesn't, where keys live, who sees usage." | Step 3/Step 4 prose says "data-flow brief to security," but `phase-registry.yaml` Phase 3 `artifacts.required`/`artifacts.optional` list **no** `data-flow-brief` file. Nothing writes it; the gate cannot check it. | `phases/03-foundation.md` Step 4 / `phase-registry.yaml` Phase 3 artifacts. |
| 3-2 | MISSING-ARTIFACT | The **central products** of Foundation are the installed harness, the pipeline, the Bicep environment, branch protection, and the deployed walking skeleton — the factory itself. | Registry `artifacts.required` = `foundation-report.md`, `risk-tier-map.md`, `cadence-plan.md`, `build-handoff.md` — four report/map files. The harness/pipeline/env/skeleton appear only as `check:` exit conditions or as the *optional* `harness-inventory.md`/`walking-skeleton-spec.md`/`pipeline-proof.md`. The gate checks the reports **about** the factory, never the factory. | `phase-registry.yaml` Phase 3 `artifacts.required` vs `exit_gate.conditions.check[]`. |
| 3-3 | MISSING-ARTIFACT | Phase 3 depends on three Phase 2 outputs it must **act on**: the walking-skeleton definition (built against), the threat mitigation map (→ risk-tier map), and the NFR proving plan (→ how the metric slice is built). | Phase 2 emitted **no file** for any of the three (they are Phase 2's own amber rows). They cross the boundary as knowledge in Nadia's/Rob's heads. Phase 3 Step 5d has QE "verify against the Phase 2 walking-skeleton definition" — a definition that is not on disk to verify against. | `phases/02-design.md` (no walking-skeleton / mitigation-map / proving-plan artifact) → `phases/03-foundation.md` Steps 3, 5d. |
| 3-4 | UNDOCUMENTED-OUTPUT | — | Step 9 emits `.sdlc/reports/phase03-visual.html` via `/visual-explainer`, a distinct artifact from Step 10's `phase03-report.html` (`generate_phase_report.py`). The companion Example/Reference tracks never name `phase03-visual.html` (day 10 cites `/visual-explainer` only for the demo/scorecard). | `phases/03-foundation.md` Step 9 / `phase-registry.yaml` Phase 3 `artifacts.optional`. |
| 3-5 | NAME-MISMATCH | The Reference artifacts table bundles **"Cadence calendar + risk-tier map"** as one artifact row, owned by Pod Lead. | The plugin splits the same objects into **two separate required files** — `cadence-plan.md` (Pod Lead) and `risk-tier-map.md` (owned with client security) — with different owners. Same objects, one row vs two files, two owners. | standard Phase 3 Reference artifacts table vs `phase-registry.yaml` Phase 3 `artifacts.required`. |

Also affected by X-8, X-1, X-7: the design-level threat review belongs in Phase 2 (with a Phase 3 confirmation pass) — that is X-8. The 11 exit criteria vs `check_gates.py` verifying only the 4 required artifacts, with `check:` items and manual approval rendered as non-blocking `passed: None` REVIEW entries, are local instances of X-1 and X-7. Row 3-3's three upstream artifacts are Phase 2's own missing walking-skeleton definition and NFR proving plan (rows 2-3, 2-2) and the threat mitigation map (X-8).

### Build loop

The Build loop is deliberately not a gated phase; the drift is the plugin modelling it as if it were, plus three real receipts the narrative never surfaces. Plugin = `phases/build-loop.md` + `phase-registry.yaml` + `scripts/`.

| # | Kind | The standard says | The plugin does | Where |
|---|------|-------------------|-----------------|-------|
| B-1 | UNDOCUMENTED-OUTPUT | The companion Build-loop page (and `docs/build-loop-example.md`) name no metrics receipt at all — the loop's outputs are described as the merged PR, the spec, and the grader verdict only. | `check_spec.py` appends one line per Definition-of-Ready check to `.sdlc/metrics/spec-log.jsonl` on every spec at Intent. Real, per-trip, never surfaced in the Build-loop companion. (Named in the plugin phase doc line 40, and in the cross-cutting `artifact-flow.html`, but not in the Build-loop narrative.) | `claude-code-sdlc/scripts/check_spec.py:245,259`; `phases/build-loop.md:40` · absent from `docs/companion/build-loop.html` + `docs/build-loop-example.md` |
| B-2 | UNDOCUMENTED-OUTPUT | Same as B-1 — the Build-loop narrative names no metrics file. | `scorecard.py record` appends `spec_merged`/`spec_reverted`/… events to `.sdlc/metrics/loop-events.jsonl` on every loop outcome; the biweekly steering scorecard is computed from it. Real, per-trip, never surfaced in the Build-loop companion. (Named in plugin phase doc line 147 and in `artifact-flow.html`, not in the narrative.) | `claude-code-sdlc/scripts/scorecard.py:4–5,211`; `phases/build-loop.md:147` · absent from `docs/companion/build-loop.html` + `docs/build-loop-example.md` |
| B-3 | UNDOCUMENTED-OUTPUT | Same as B-1 — the Build-loop narrative names no metrics file, and describes the grader verdict as a PR comment with no durable on-disk receipt. | `record_findings.py` appends every grader finding — with severity and disposition — to `.sdlc/metrics/findings-log.jsonl`, giving the verdict memory across re-grades and driving the open-HIGH-debt count at the merge bar. **This one is undocumented even in the plugin's own `phases/build-loop.md`** (it appears in no line of the phase doc), as well as in the companion. | `claude-code-sdlc/scripts/record_findings.py:5,225,265` · absent from `phases/build-loop.md`, `docs/companion/build-loop.html`, `docs/build-loop-example.md` |

Also affected by X-4: the registry modelling `build` as a gated phase (`order: 4`, `exit_gate.approval: manual`, `artifacts.required: [phase7-handoff.md]`) while its own `description` says "there is no artifact exit gate" — the original WRONG-FRAMING row — is X-4.

### The Rails

Drift = where `docs/the-rails.md` / GOLD-STANDARD describes blocking behavior the YAML in `kit/workflows/` does not implement, or vice versa. Every row quotes the YAML/JSON.

| # | Kind | The standard says | The plugin does | Where |
|---|------|-------------------|-----------------|-------|
| R-1 | INTERNAL-CONTRADICTION | A `risk:high` change may proceed on **"a named human sign-off recorded in the PR"** (the-rails.md §4; RAILS.md merge bar). `security.yml`'s own enforce-step error even says *"Resolve them or record a named accepted-risk sign-off."* | `security.yml` enforce step has **no override**: `case "$FIRST" in "SECURITY_VERDICT: BLOCK"*) echo "::error::Security review found HIGH severity issue(s)..." exit 1 ;;` — no label check, no `HAS_ACCEPTED_RISK`, no `exit 0` path. Contrast `correctness.yml`, which *does* implement one: `HAS_ACCEPTED_RISK: ${{ contains(...'accepted-risk:correctness') }}` → on BLOCK `if [ "$HAS_ACCEPTED_RISK" = "true" ]; then ... exit 0`. So a recorded HIGH sign-off cannot make the security check pass; the promised override is doc/comment-only. | `kit/workflows/security.yml` L108–133 (esp. L123–126) vs `kit/workflows/correctness.yml` L121–156 (L130, L144–147); `docs/the-rails.md` §4 |
| R-2 | MISSING-ARTIFACT | The rails must be **watched by the delivery numbers** — "accepted-as-is rate, review wait, the DORA four, escaped bugs" on the internal dashboard (GOLD §9) — and **"Log everything with provenance ... logged centrally, with co-authorship on the commits"** so the rails are "auditable rather than merely automated" (the-rails.md §9). | **Nothing in the kit emits a metrics or provenance receipt.** No workflow or hook appends a metrics line, and there is no central log file (`grep` for `metrics.*jsonl` / `.sdlc/metrics` over `kit/` and `GOLD-STANDARD.md` returns nothing). Co-authorship on commits is a convention, not written by any rail. The dashboard the standard demands has no producer. | `GOLD-STANDARD.md` §9 (L386–406) and `docs/the-rails.md` §9 vs `kit/workflows/*.yml`, `kit/hooks/*` (no emitter exists) |
| R-3 | MISSING-ARTIFACT | deploy-dev **"Deploys the merged artifact to the client's dev environment"** and **"Merge → dev, automatically"** (the-rails.md §3 table, §5). | `deploy-dev.yml` ships as a **non-functional starter that intentionally fails**: Deploy step `echo "::error::<<DEPLOY_STEP>> not yet wired — this starter intentionally fails until adapted."` then `exit 1`; the rollback step likewise ends `exit 1`. It encodes the §5 rules (promote-never-rebuild via `workflow_run` download; restore-on-`failure()`) but the deploy/rollback are placeholders. The "deployed dev environment" receipt does not exist until a client wires **and rehearses** it. (README/RAILS flag this; the-rails.md deep-dive presents it as functioning.) | `kit/workflows/deploy-dev.yml` L99–109, L126–140 vs `docs/the-rails.md` §3, §5 |
| R-4 | UNDOCUMENTED-OUTPUT | the-rails.md §3 defines **ci** as "Build, tests, lint, 80% coverage on new code. The mechanical floor." — a single hard gate, no eval gate mentioned. | `ci.yml` ships a **second optional HARD gate**, job `eval-gate` (blocks on any failing eval fixture), with a recorded-bypass ledger at `profile/eval-bypasses.md`. It is documented only in `ci.yml` comments, `RAILS.md`, and `README.md` — never in the `the-rails.md` deep-dive that the companion page mirrors. | `kit/workflows/ci.yml` L111–153 (+ `kit/profile/eval-bypasses.md`), `kit/workflows/RAILS.md` L22 vs `docs/the-rails.md` §3 |
| R-5 | NAME-MISMATCH | the-rails.md §1/§3/§4 name the five rails **ci / grader / correctness / security / deploy-dev** (and prose refers to "the security workflow," "correctness review"). | The **required status-check contexts are the JOB names**, which differ: `build-and-test`, `grader`, `correctness-review`, `security-review`. So "ci" ≠ `build-and-test`, "correctness" ≠ `correctness-review`, "security" ≠ `security-review`. RAILS.md itself warns "Rename a job → rename its required-check context." The workflow display-name and the enforced-check name are not the same string. | `kit/profile/rulesets/branch-protection.json` L30–35 (+ job `name:` lines: `ci.yml` L35, `correctness.yml` L50, `security.yml` L38) vs `docs/the-rails.md` §3 |
| R-6 | INTERNAL-CONTRADICTION | `kit/workflows/README.md` "Known drift" asserts **GOLD-STANDARD §6 lists only four workflows and "omits `correctness.yml`,"** and files an action for the standard's owner to add it. | GOLD-STANDARD §6's harness tree **already lists `correctness.yml`** with a full description ("fresh agent ... blocks on a high-confidence defect, named override on record"). The drift the README documents is already fixed upstream — so the README's own "Known drift" note is now stale and contradicts the current standard. | `kit/workflows/README.md` L72–88 vs `GOLD-STANDARD.md` §6 L307–314 (L311) |

### Phase 7 — Documentation

Registry slug `07-documentation`; standard = the Phase 7 companion Reference/Example tracks; plugin = `phases/07-documentation.md` + `phase-registry.yaml` + `scripts/check_gates.py`.

| # | Kind | The standard says | The plugin does | Where |
|---|------|-------------------|-----------------|-------|
| 7-1 | INTERNAL-CONTRADICTION | The two cold runs are the phase's **verification teeth** and are explicit exit-gate lines: "README cold checkout completed by someone new to the repo, unassisted" and "RUNBOOK deploy + rollback + one failure scenario executed cold by the ops engineer." | The **phase body's Exit Criteria omit both cold runs** — it lists "README allows a new developer to set up and run the project from scratch" (satisfiable by reading), with no cold-checkout and no cold-walk-through requirement. The registry `exit_gate.conditions` **does** carry the two `check:` teeth. Body and registry disagree on whether the teeth are gate conditions. | `phases/07-documentation.md` lines 138–143 vs `phase-registry.yaml` (`07-documentation.exit_gate.conditions`) |
| 7-2 | MISSING-ARTIFACT | The **spec-library sample audit** is a Phase 7 deliverable (Reference artifact, QE-owned) and an exit-gate line: "The spec library sample audit passed (or its mismatches became defect specs, now merged)." The QE samples 5–10 specs weighted to HIGH-risk/recently-changed and executes their acceptance checks by hand against dev. | **No step performs it and no artifact captures it.** The workflow is Step 0 scope → Step 1 parallel docs → Step 2 API diff → Step 3 RUNBOOK → Step 4 ADR finalization → Step 5 handoff → 6/7 reports. There is no spec-audit step, and no `spec-library-audit.*` in `artifacts.required` or `artifacts.optional`. | standard Phase 7 Reference + exit gate; plugin `phases/07-documentation.md` (no counterpart) + `phase-registry.yaml` `07-documentation.artifacts` |
| 7-3 | MISSING-ARTIFACT | The cold checkout and cold walk-through produce a **doc-defect log** — the QE logs each stall (the step, what was missing, what the verifier did instead). That log is the record the gate is signed against. | The two cold runs exist only as prose `check:` **strings** in the registry `exit_gate.conditions`. **No artifact records the run**, and `check_gates.py` never evaluates `check:` conditions — it validates only `artifacts.required[]` existence/completeness (+ placeholder scan). The verification teeth are unrecorded on disk and unenforced by code (advisory to the human gate only). | `phase-registry.yaml` (`07-documentation.exit_gate.conditions` `check:` lines) vs `scripts/check_gates.py` (`check_phase_gates` ignores `check:` strings) |
| 7-4 | MISSING-ARTIFACT | The **drift catalog** is a required, gated deliverable (Reference artifact "The drift catalog", Pod-Lead-owned; the API-docs "done means" and the exit gate both depend on it: "the drift catalog is empty or every open item has an owner and an explicit Phase 8 blocker decision"). | Step 2 produces the diff, but `drift-catalog.md` is listed under **`artifacts.optional`**, not `artifacts.required`, and it appears in **no** `exit_gate.condition`. The catalog can be emitted but is never required and never gate-checked — the standard's gated artifact is optional in the plugin. | `phase-registry.yaml` (`07-documentation.artifacts.optional` includes `drift-catalog.md`; not in `required` or `exit_gate`) vs standard Phase 7 Reference + exit gate |

Also affected by X-3, D-2, D-3, X-1: Phase 7's Entry Criteria requiring "Phase 6 exit gate passed" and its Step 4 sweep "from Phase 4 onward" both reference phases that collapsed into the Build loop — instances of X-3. The gate resolving `README.md`/`RUNBOOK.md` under `.sdlc/artifacts/07-documentation/` instead of the repo root is D-2. Phase 7 is also the origin of D-3 (its body skips `RUNBOOK.md`/`api-docs.md` for `library`/`cli`/`skill` projects, but the gate blocks on them unconditionally). The cold-run enforcement gap noted inside 7-3 (`check_gates.py` never evaluating `check:` strings) is X-1.

### Phase 8 — Deployment

Standard = the Phase 8 companion + GOLD-STANDARD; plugin = `phases/08-deployment.md` + `phase-registry.yaml` + `scripts/`.

| # | Kind | The standard says | The plugin does | Where |
|---|------|-------------------|-----------------|-------|
| 8-1 | MISSING-ARTIFACT | **Rollout-shape decision** is a required artifact: cutover / pilot / parallel chosen by the client, in writing, with the in-flight-work answer and the fallback trigger conditions, *before the ceremony* (exit-gate bullet 3). | Step 0's HITL asks "(1) Deployment target and strategy" verbally, but no step writes a rollout-shape artifact and none is in `artifacts.required` or `artifacts.optional`. Nothing writes it. | `phases/08-deployment.md` Step 0; registry `08-deployment.artifacts` |
| 8-2 | MISSING-ARTIFACT | **Secrets rotation record** is required and gated: production secrets rotated to values the pod never held, signed by client security (exit-gate bullet 2). | Phase 8 has no secrets-rotation step and no such artifact. The plugin's only rotation is Phase C's `access-revocation-checklist.md` (pod-access revocation at close), which is a different action at a different time. Nothing in Phase 8 writes it. | `phases/08-deployment.md`; registry `08-deployment.artifacts`; cf. `phases/close.md` |
| 8-3 | MISSING-ARTIFACT | **Rollback rehearsal evidence**: the timestamped deploy → roll back → redeploy timeline, executed in test *by the client's operators*, with time-back-to-healthy, attached to the go/no-go packet. "A rollback that has never run is a wish." | Step 1's checklist carries a "Rollback verification (deploy → roll back → redeploy)" *line*, and `rollback-procedure.md` exists only as an **optional** artifact. No command writes a timestamped rehearsal-evidence file, and nothing requires the client's operators to be the ones who run it. | `phases/08-deployment.md` Step 1; registry `08-deployment.artifacts.optional` (`rollback-procedure.md`) |
| 8-4 | INTERNAL-CONTRADICTION | The go/no-go is the single most protected stop: **a recorded go/no-go with every named role asked and answered**, evidence on the table, after the dress rehearsal (exit-gate bullet 4; registry `check:`). | Registry `exit_gate` includes the `check:` "Recorded go/no-go with every named role asked and answered," yet the artifact that would hold it, `go-no-go-record.md`, is in `artifacts.optional` — not required. Worse, the only mechanism (Step 0 `AskUserQuestion`) asks a *single* human *up front*, before any rehearsal or smoke evidence exists, and enumerates no roles. The exit check demands a multi-role recorded ceremony the plugin's mechanism cannot produce. | registry `08-deployment.exit_gate.conditions` + `artifacts.optional`; `phases/08-deployment.md` Step 0 |
| 8-5 | INTERNAL-CONTRADICTION | The rollback must be **rehearsed in test by the client's operators before production promotion** (registry `check:`; exit-gate bullet 1). | Registry `exit_gate` carries that `check:`, but (a) `rollback-procedure.md` is only optional, and (b) the phase body's own Exit Criteria weakens it to "Rollback procedure documented and tested" — no client-operator requirement and no before-promotion ordering. The registry contradicts the phase body. | registry `08-deployment.exit_gate.conditions`; `phases/08-deployment.md` "Exit Criteria" |
| 8-6 | NAME-MISMATCH | The verification artifact is **"Smoke results (test + prod)"**; the phase section is titled **"Check it for real."** | The required artifact is `smoke-test-results.md`. Same object, different name; and the plugin frames it as a two-run staging+prod test-results table (Step 3 staging, Step 4 production). | registry `08-deployment.artifacts.required`; `phases/08-deployment.md` Steps 3–4 |
| 8-7 | NAME-MISMATCH | Environments are **dev → test → production**; the pre-production environment is "**test**"; production smoke runs through **test-mode paths**. | Step 2 is "**Staging** Deployment" and the body Exit Criteria read "Staging deployment successful / All staging smoke tests passing." Plugin "staging" = standard "test." | `phases/08-deployment.md` Steps 2–3 + Exit Criteria |
| 8-8 | UNDOCUMENTED-OUTPUT | The standard's Phase 8 Reference artifact table lists 8 artifacts; no report HTML among them. | The plugin emits `.sdlc/reports/phase08-visual.html` (Step 6, `/visual-explainer`) and `.sdlc/reports/phase08-report.html` (Step 7, `generate_phase_report.py`) — neither named in the standard's artifact ledger. (The companion Example now surfaces both as blue rows / the evidence packet.) | `phases/08-deployment.md` Steps 6–7 |
| 8-9 | UNDOCUMENTED-OUTPUT | The standard names no deployment-log artifact. | The plugin lists `deployment-log.md` in `artifacts.optional`; the standard's artifact table and exit gate never mention it. | registry `08-deployment.artifacts.optional` |

Also affected by X-1: `check_gates.py` never enforcing the registry `check:` items — surfacing them as manual `passed: None` REVIEW items that never affect the exit code — is a local instance of X-1.

### Phase 9 — Monitoring

Plugin = `phases/09-monitoring.md` + `phase-registry.yaml` + `scripts/check_gates.py`; standard = the Phase 9 companion + the Phase 2 NFR proving-plan through-line.

| # | Kind | The standard says | The plugin does | Where |
|---|------|-------------------|-----------------|-------|
| 9-1 | INTERNAL-CONTRADICTION | "Done" means the teeth are met: every threshold derived from a measured baseline (or flagged modeled with a revisit date), and the drill executed with every critical alert fired and answered. | The registry `exit_gate.conditions` carry both teeth `check:` lines, but the phase body's **Exit Criteria** section lists neither — its five criteria stop at "at least one alert per CRITICAL failure mode" and "retrospective completed." The two definitions of done disagree. | Registry `exit_gate.conditions` (2 `check:`) vs `09-monitoring.md` §Exit Criteria (lines 146–151) |
| 9-2 | MISSING-ARTIFACT | The alert drill is the phase's signature act — "an alert that has never fired is a wish." Every critical alert fired via a pre-agreed synthetic trigger, answered by the client's on-call, recorded per alert (trigger, detection, routing, responder, outcome) in the gate packet. | No workflow step runs a drill (Steps 0–6 are HITL scope, monitoring-config, alert defs, playbook, retrospective, visual report, phase report). No command triggers it. `drill-record.md` is listed **optional**. The gate's teeth check requires the drill; nothing produces it or its record. | `09-monitoring.md` Workflow (no drill step) + registry `drill-record.md` optional vs registry `exit_gate` "Alert drill executed" |
| 9-3 | MISSING-ARTIFACT | Before any alert ships, the alert-fatigue review replays each proposed condition over hypercare history and cuts/raises anything that would fire weekly without demanding action; that the review ran is a gate item. | The fatigue rule appears only as **Guidance** prose ("If an alert fires more than once a week non-critically, raise the threshold or eliminate it"). No step, no command, no artifact/record that the review was performed. | Standard exit gate ("alert-fatigue review ran") vs `09-monitoring.md` §Guidance (advice only, no step/record) |
| 9-4 | MISSING-ARTIFACT | The "what healthy means" session is *the phase*: per failure scenario and journey, capture healthy / degraded / who-is-woken / who-is-told-in-the-morning, and that table is what the alert definitions are written from. | Step 0 (HITL) asks only four scoping questions via `AskUserQuestion`. Step 1's `doc-updater` writes `monitoring-config.md` from the **baseline measurements**, not from the session. The session's table reaches disk only if a human types it there — no command captures it. | Standard §"Decide what healthy means" vs `09-monitoring.md` Step 0 + Step 1 (doc-updater from baseline) |
| 9-5 | MISSING-ARTIFACT | Phase 9 cashes the NFR proving plan written in Phase 2 — the plan named, per NFR, the method and the *place its number would be read*. Phase 9 reads each there (dashboard, alert, scorecard) or flags it modeled with a revisit date. | Neither the plugin's Phase 2 nor Phase 9 emits a proving plan. Phase 9 Step 1 measures the baseline "against NFR targets from `non-functional-requirements.md`" — the raw NFRs, with no artifact recording where each number is read. The read-location promises exist nowhere in tooling. | Standard Phase 2 NFR proving plan / Phase 9 through-line vs `09-monitoring.md` Step 1 (raw NFRs, no proving-plan artifact) |
| 9-6 | UNDOCUMENTED-OUTPUT | Baseline lives inside the monitoring configuration — "what normal looks like for each key metric," each with its measurement period. | Registry `artifacts.optional[]` offers a standalone `baseline-data.md`, but the phase body folds baseline into `monitoring-config.md` ("Baseline measurements … from `performance-benchmarker` output") and never names or specifies `baseline-data.md`. The registry offers an output the workflow never documents or writes. | Registry `09-monitoring` optional `baseline-data.md` vs `09-monitoring.md` §Artifact Specifications (folded into monitoring-config) |
| 9-7 | INTERNAL-CONTRADICTION | (n/a — declared tooling should be used or not declared.) | Registry `skills.secondary` declares `["/session-insights"]` for Phase 9, but the phase body never invokes or mentions `/session-insights` — Step 4's retrospective uses the `feedback-synthesizer` agent instead. A declared skill the workflow never touches. | Registry `09-monitoring` `skills.secondary` vs `09-monitoring.md` Workflow (no `/session-insights`) |

Also affected by X-6: `close-handoff.md` being registry-required (and an `exit_gate` condition) with **no Artifact Specification** in the phase body — the plugin requires a file it never tells you how to write — is X-6. Row 9-5's NFR proving plan is the Phase 9 end of Phase 2's own missing proving-plan artifact (row 2-2). Two findings outside the five-kind taxonomy, preserved from the drift pass: the incident playbook is capped at "top 5 alert types" in the body Exit Criterion where the standard requires coverage of every critical alert; and Step 0 permits building the monitoring stack "from scratch" where the standard wires into the client's existing stack only.

### Phase C — Close & Transfer

Standard = `docs/companion/phase-c.html` reference track; plugin = `phases/close.md`, `phase-registry.yaml` (slug `close`, terminal), `scripts/check_gates.py` / `generate_handoff_report.py`.

| # | Kind | The standard says | The plugin does | Where |
|---|------|-------------------|-----------------|-------|
| C-1 | INTERNAL-CONTRADICTION | The outcomes dashboard handover is a **close condition** — "Every phase report delivered and the outcomes dashboard handed over, caveats intact, with the quarter-read date on the client's calendar" (exit-gate bullet; reference artifacts table lists "Outcomes dashboard handover", owned by Client). | Its only artifact, `outcomes-dashboard-handover.md`, is in `artifacts.optional`. `check_gates.py` G1/G2 iterate `artifacts.required[]` only, so nothing verifies the handover ever happened. A required-to-close item whose sole artifact is optional. | `close.md` Exit Criteria bullet 6 + `phase-registry.yaml` `close.artifacts.optional`; `check_gates.py` `check_phase_gates`. |
| C-2 | MISSING-ARTIFACT | The retro file is a **gate item**: "the harvest PR is opened against the delivery-standard repo, **and the retro file is written**" — one file in `retros/` recording what the engagement changed about the standard and why (reference artifacts table: "The retro file", owned by the standard's owner). | No command writes it — Step 6's `Agent(Explore, …)` only **drafts** harvest content. The file lives in the **delivery-standard repo, outside `.sdlc/`**, which `check_gates.py` never walks (it indexes the `.sdlc/` tree and the project root only). The method requires a file no tool emits and no gate can see. | `close.md` Step 6 + Exit Criteria bullet 9; `check_gates.py` `check_cross_references` walk scope. |
| C-3 | MISSING-ARTIFACT | The harvest PR itself is a **registry exit check**: `check: "Harvest PR opened against the delivery-standard repo"`. | No command opens the PR (`Agent(Explore)` drafts content; a human opens it), and `harvest-pr-notes.md` is only `artifacts.optional`. `check_gates.py` never evaluates the free-text `check:` conditions, so nothing enforces the PR was opened. | `close.md` Step 6; `phase-registry.yaml` `close.exit_gate` `check[]`. |
| C-4 | NAME-MISMATCH | Reference artifacts table names a standalone **"Shadow-flip spec record"** (drafted by QE, owned by Pod Lead): ≥3 real specs orchestrated by client engineers with pod Checkers. | There is **no standalone file**. Step 1 says "Record this in `close-gate-evidence.md` (the shadow-flip section)." Same object, folded into another required artifact under a different name. | reference-track Phase C artifacts table vs `close.md` Step 1. |
| C-5 | NAME-MISMATCH | Reference artifacts table names the credential artifact the **"Access revocation record"** (Setup Owner + client security draft; client security owns). | The plugin/registry filename is `access-revocation-checklist.md`. Same object — "record" vs "checklist" — a naming inconsistency between the reference narrative and the plugin artifact. | reference-track Phase C artifacts table vs `close.md` Artifact Specifications + `phase-registry.yaml` `close.artifacts.required`. |
| C-6 | INTERNAL-CONTRADICTION | The phase is **terminal**: "Close is the final phase … There is **no next phase and no handoff out**." | The "HTML Report" section says `close-report.html` "is generated automatically when you run `/sdlc-gate` **or `/sdlc-next`**." `/sdlc-next` runs `advance_phase.py` to move to a next phase, which does not exist for a terminal phase — a stale instruction copied from non-terminal phases. | `close.md` "HTML Report" section vs "Terminal Phase" section + `phase-registry.yaml` `close.terminal: true`. |

Also affected by X-1: `check_gates.py` never reading or evaluating the `close.exit_gate` `check:` strings — the close gate ran one real spec solo, ≥3 shadow-flip specs, access revoked and audit-confirmed, harvest PR opened — is a local instance of X-1. (Phase C is also the one place the plugin already does the receipt-for-human-ritual pattern right: `close-gate-evidence.md`, `harness-audit.md`, and `access-revocation-checklist.md` are human-authored yet registry-required and gate-checked — not drift.)

---

## Recommended order

1. **Fix 1 alone** (render exit conditions at sign-off). No behavior change, immediate value, trivially
   reversible.
2. **X-3, X-5, X-6** — the stale reference and the two internal contradictions. Documentation-level
   corrections inside the plugin; nothing starts failing.
3. **X-4** — remove `build`'s exit gate and `approval`, or rename what it models. Requires a decision about
   what `phase7-handoff.md` is if it is not a gate artifact.
4. **X-8** — add the Phase 2 design-level threat review step, keep the Phase 3 confirmation pass.
5. **Fix 3 / Fix 2** — the receipt artifacts, and wiring or deleting `approval`. **These change what
   `/sdlc-gate` blocks on.** Any engagement mid-flight would newly fail on a missing `threat-model.md`.
   Ship behind a profile flag, or on a major version, with a migration note. Do not fold this into a
   documentation commit.
