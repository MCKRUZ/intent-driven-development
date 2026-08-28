# Choose a mechanism

_The standard is eight rules. `claude-code-sdlc` is the way we enforce them today: one option, not
the definition. The default option walked step by step is
[with the claude-code-sdlc plugin](with-the-plugin.md); the files it leaves in the repo are on
[what's installed](whats-installed.md)._

---

## The standard: eight rules

The method and the tooling are different things, and this page is the seam between them. The
standard is a short set of rules any mechanism must satisfy. If a mechanism enforces them, it
conforms; if it cannot, it does not, whatever it is called.

1. **One spec, one branch, one review.** Every change starts from a written, testable spec that
   travels in the same diff as the code.
2. **Ready before build.** No vague lines, scope in and out stated, silent decisions answered, a
   risk tier assigned. Enforced before an agent starts.
3. **Plan before code.** The agent proposes; a person approves the plan before anything is
   written.
4. **Nothing is done on red.** An agent cannot declare itself finished with failing tests or a
   broken build; CI is the universal backstop.
5. **The author never approves.** A separate grader that did not write the code, plus a
   non-author human, on every change. High risk adds security review and a named signature with
   a sentence.
6. **Gates report, humans advance.** No auto-advance anywhere. Every override carries a name, a
   reason and an expiry.
7. **Reopening is recorded.** A signed decision may be revised; the revision has an owner, a
   reason, a clock and a visible blast radius.
8. **Outcomes, never activity.** Success metric and delivery-stability trends; no velocity,
   points, PR or line counts. Empty reads "no data", never zero.

## The mechanism: two halves

Whatever enforces the rules has two halves, and they differ in one way that matters when you
choose: one half does not care which coding agent is in use, the other is specific to it.

**The rails** live in the repo and the pipeline. They do not care which local tool wrote the code.

- CI workflows: build, tests, lint, coverage
- The AI grader and reviewers running in the pipeline
- Branch protection and the required checks
- The deploy and promotion gates, with a named approver

**The harness** lives with the coding agent, and is specific to the one in use.

- The agent's permissions: what it may run, what it must ask about
- The stop-on-red hook that refuses "done" with a failing build
- The plan-first rule
- The phase state and the gates

That split is why the checking side of the method already works with any coding agent, and why
the intent and delegation side is where the options differ.

## The options, rule by rule

Pick one per engagement. For each rule: enforced **mechanically** (a check blocks), **by process**
(a meeting with a signed artifact), or **by discipline** (people remembering).

| Rule | claude-code-sdlc · today's default | Rails only, any agent · supported shape | Templates only · minimum |
|---|---|---|---|
| 1 · One spec, one branch, one review | Mechanically | Mechanically | By discipline |
| 2 · Ready before build | Mechanically | By discipline | By discipline |
| 3 · Plan before code | Mechanically | By discipline | By discipline |
| 4 · Nothing is done on red | Mechanically | Mechanically | By discipline |
| 5 · The author never approves | Mechanically | Mechanically | By process |
| 6 · Gates report, humans advance | Mechanically | Mechanically | By process |
| 7 · Reopening is recorded | Mechanically | By discipline | By discipline |
| 8 · Outcomes, never activity | Mechanically | Mechanically | By process |
| **What it is** | Full mechanism: the phase state machine and gates, the harness install, the rails, the spec / spike / revise / refresh commands, HTML gate reports. Claude Code only. | Cursor, Copilot, Codex or any agent writes; the same CI rails, grader and branch protection check. Phase gates run as reviewed checklists and signed records in the repo. | Spec, spike, rollback, alert and handoff templates plus the cadences and roles, with no orchestration tooling. Gates are meetings with signed artifacts. |
| **Requires** | Claude Code and the plugin marketplace. One install, one source of truth for the kit. | A "ready" check and a plan-approval step the tool may not give you. | Nothing beyond the repo. |
| **Best when** | You want all eight rules enforced by a check, not a habit. | The client has already standardised on another agent. | A locked-down environment allows nothing else. An honest fallback; not where we want to be for long. |

The walkthrough of the default option, one engagement step by step with every command, is
[with the claude-code-sdlc plugin](with-the-plugin.md). The files any option lays down in the repo
are listed on [what's installed](whats-installed.md).

## Where the seam is today

An honest note on how far the neutrality goes right now. The kit's "neutral core" is neutral on
stack and on CI platform: a stack pack and a CI/CD pack are composed on top of it, and the Azure
DevOps pack proves that shape is buildable. It is not yet neutral on the coding agent. The core
ships Claude Code artifacts unconditionally: `CLAUDE.md`, `.claude/hooks`, agents, skills and
`.mcp.json`.

The planned change is an _agent_ axis in the pack model. The core would declare the four
capabilities it needs (a session-context file, a pre-finish block on red, a non-author reviewer,
and a pre-push gate) and each agent pack would realise them in its own syntax, the same way the
CI/CD packs already realise the pipeline for GitHub Actions and Azure DevOps. Until that lands,
"rails only, any agent" is a supported shape you assemble by hand from the rails half of the kit,
not a pack you install.

Harbor Mutual, the standard's fictional worked example, runs on the default option throughout the
docs. The reason is only that it is the one we run today; the eight rules above are what the
engagement is held to, and they are the same under any of the three.
