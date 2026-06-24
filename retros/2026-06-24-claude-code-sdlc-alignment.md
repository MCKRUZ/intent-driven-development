# Retro — claude-code-sdlc alignment engagement

**Date:** 2026-06-24
**Engagement:** Reshaping the `claude-code-sdlc` plugin (the executable "how") to enforce this
delivery standard (the written "why"), run as five work chunks.
**What this file is:** the harvest required by Phase C, Step 6 — what this engagement changed
about the standard and why. The "client" here is internal tooling, so there are no client
specifics to strip.

---

## Headline: the standard held up under mechanization

The engagement's real test of the standard was whether its prescriptions could be turned into
mechanical gates without softening them. They could. A drift scan of the written standard against
the now-aligned tooling (build-loop, the-rails, phase-c-close, anti-patterns, the phase docs)
found **no major drift** — the spec-as-unit model, the Definition of Ready, the risk-tier →
checking-ladder mapping, the steering scorecard with its forbidden activity metrics, and the
Close handoff/harvest flow were all already stated explicitly enough to implement against
verbatim. A standard that can be executed without reinterpretation is the point; this engagement
is evidence the standard clears that bar.

The five elements verified present and mechanizable as written:

| Standard element | Where it lives | Mechanized as |
|------------------|----------------|---------------|
| Spec = branch = PR (sections are a *design* aid, not the build unit) | GOLD §4, build-loop §2 | `track_specs.py` reads backlog from spec frontmatter; section/DAG machinery rescoped to Phase 2 |
| Definition of Ready (scope in/out, vague-line test, risk a first-class field) | build-loop §2, GOLD §5.1 | `check_spec.py` (MUST floor + vague-line lint) |
| Risk tier sets the ladder climb | build-loop §4, anti-patterns §9 | `risk_model.py` (single source of truth) + `check_spec.py` depth enforcement |
| Steering on outcomes; activity metrics forbidden | GOLD §9, build-loop §8 | `scorecard.py` (computes the four-plus; *refuses* velocity/points/PR-count/LOC) |
| Close handoff assembled from records; harvest + retro back to the standard | phase-c-close §3 | `generate_handoff_report.py` (this session) + this retro |

---

## The one change made to the standard

**"No data," not a fabricated zero** — added to the metrics guidance in `GOLD-STANDARD.md §9` and
`docs/build-loop.md §8`.

The standard said "baseline-and-trend, no vanity targets" but did not address the empty case. When
the tooling computed the scorecard it became obvious that a zero is a *lie* for an unrecorded
metric: "0 escaped bugs" and "0h review wait" read as measured results and steer a steering meeting
wrong, when the truth is nothing has been recorded yet. The scorecard tool encodes this (it returns
"no data", never 0); the standard now says so in words. Small, but it is exactly the kind of edge
the written rule glosses and the mechanical implementation cannot.

---

## Generalizable patterns surfaced (candidates for the standard, not yet adopted)

These came out of building the tooling. They are recorded here as harvest candidates; adopting any
of them into the standard's text is a separate decision for the standard's owner.

1. **Two-pass "draft from records."** The Close handoff report is assembled deterministically by a
   script (phase index, gate/sign-off table, metrics history, spec backlog) with the judgment
   sections left as explicit `[Fill: …]` slots for the agent/human. Mechanical where it can be,
   human where it must be — a pattern that fits any "draft from the engagement's own records"
   artifact, not just the handoff. Worth a line in phase-c-close if the standard wants to name it.

2. **Standalone-or-workflow as a design rule.** Every tool was built to run two ways: composed
   into the engagement (`--state` reading `.sdlc/`) and pointed at an arbitrary repo with no
   engagement context (`--repo`, degrading gracefully and saying so in output headers). This keeps
   the parts reusable outside a full engagement — useful for a standalone audit or a one-off spec.

3. **Cold-render catches doc drift that review misses.** Smoke-rendering the Close report surfaced
   that the tooling docs described an init step (`init_project` "copies phase templates") that the
   code never performed. The standard already values cold checkout for docs (Phase 7); this is a
   reminder that the same discipline applies to a tool's *own* documentation, verified by running
   it, not reading it.

## Gotchas worth an anti-pattern line

- **The `.gitignore` build/ trap.** A generic Python `build/` ignore rule silently swallowed the
  `templates/phases/build/` directory, so a *required* Build-loop artifact template was never
  tracked and nobody noticed until it was needed. Anchored ignore rules / a `git status` check when
  adding files under a generated-sounding path. (Tooling-specific, but the failure mode — an
  artifact that looks present locally and is absent in the repo — is general.)

---

## Status

- Standard edits: applied to `GOLD-STANDARD.md` and `docs/build-loop.md` (the "no data" rule).
- Tooling: all five chunks merged and pushed in `claude-code-sdlc` (`master`).
- Open: the four harvest candidates above are recorded, not adopted — the standard's owner decides.
