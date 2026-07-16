# What the harness installs — a guided tour

> Source of record for [`whats-installed.html`](whats-installed.html). A client-facing version
> ships inside every install as `docs/harness.md` (kit source: `kit/HARNESS.md`). This page adds
> the one thing client repos don't need: how the install is *assembled*.

When `/sdlc-setup` runs against a product repo, it installs the delivery harness: the rules for
how work gets built, checked, and shipped — whether a person or an AI is doing the work.

## The 60-second version

| Piece | What it does |
|---|---|
| `CLAUDE.md` | The working agreement the AI reads at the start of every session |
| `.claude/settings.json` | What the AI may do freely, must ask about, and can never do |
| `.claude/hooks/` | Barriers: the AI can't finish on a broken build or push unreviewed code |
| `.claude/agents/` | Six AI specialists — two arrive automatically (security, build repair) |
| `.claude/skills/` | The team's runbooks (specs, tests, bugs, APIs, PRs, evals) |
| `.mcp.json` | Shared plug-ins that give the AI extra abilities — approved once per developer |
| `.github/workflows/` | The pull-request checks that apply to everyone, human or AI |
| `specs/`, `.sdlc/`, `infra/` | Feature specs, phase tracking, infrastructure starter |

## Two ideas explain the design

1. **The rules live in the repo, not on anyone's machine.** Clone it and you have everything —
   the same guardrails, AI crew, and checks as every teammate.
2. **Enforcement happens twice.** `.claude/` files stop the **AI** on the developer's machine,
   early and cheaply. The pull-request checks stop **everyone** at the server. The AI can't
   skip the first; nobody can skip the second.

## How the install is assembled

The installer builds each repo's copy in layers. Every layer may add to or replace what came
before, so the most specific layer wins:

```
1. core             the neutral standard — identical everywhere
2. stack pack       how we build in this technology        (from the profile's language)
3. CI/CD pack       which platform runs the checks         (from the profile's platform)
4. frontend packs   for repos with screens: a generic UX layer, then the framework's (react)
5. tools packs      optional tools the team opted into     (from the profile's tools list)
6. customer profile one company's standards (coverage bar, compliance)
7. repo adaptation  the repo's own edits during setup — owned by the repo from then on
```

If a layer doesn't exist yet for a given choice (say, a language with no pack built), setup
installs the neutral core for that piece and says so — it never fails for lack of a pack.

## CLAUDE.md — the working agreement

Every AI session in the repo starts by reading this file: how the team works, the coding
standards for the stack, what the project's words mean. That's why the AI behaves the same for
every developer — everyone's sessions start from the same page. It's assembled at setup from
the standard's base, the stack's coding standards, and the customer profile; the repo owns it
from then on.

## settings.json — the three buckets

Everything the AI could do falls into one of three buckets: **do freely** (building, testing,
reading history — safe and reversible), **ask first** (pushing code; touching login/security
code, database migrations, infrastructure, or the checks themselves — a human clicks yes in
the moment), and **never** (force-pushing, wiping work, piping downloads into a shell, reading
secrets files — refused outright).

Two details: a developer's personal settings can loosen "do freely" for themselves but can
never cancel a team "never" — hard limits are team property. And the AI changing its own
guardrails is itself an ask-first action.

## hooks/ — the barriers

Written rules get forgotten under pressure, so these ones are machinery instead:

- **The done-gate.** The AI cannot end its work turn while the build is broken — the turn is
  refused and the errors are handed back. Documentation-only turns skip the build.
- **The ship-gate.** The AI cannot push code until the required reviews provably ran against
  the exact version being pushed. Change the code afterward and the evidence no longer
  matches — the gate demands a fresh review.

The barriers only stop the AI; a human in their own terminal walks past them on purpose. The
pull-request checks below catch everyone. If the *environment* is broken (a tool missing) the
hooks warn and step aside; if the *code* is provably broken they block.

## agents/ — the AI crew

Six specialists the AI can hand work to. Each starts with fresh eyes — it sees the code and
the requirements, not the reasoning that produced the code, which is what makes its review
honest. Planner and architect (called for big features and hard design choices), grader
(scores code against requirements — advice, not a veto), debugger (root-causes weird
failures) — and two that arrive **automatically**, because forgetting to ask is the real
risk: the security reviewer (any change to login, payments, identity, secrets — can block)
and the build fixer (any broken build).

Repos with a user interface get a seventh specialist: **`ux-reviewer`** (from the frontend
pack). It reviews screens the way the grader reviews code — do all the states exist (loading,
empty, error, success), is it keyboard-reachable, does it follow the house pattern — and
drives the changed flow in a real browser when it can. On React repos it arrives React-aware.
Advisory: it reports, a human decides.

## skills/ — the runbooks

Standard procedures the AI follows when the situation matches. The rules they lock in: **no
spec, no build**; **a bug fix starts with a failing test**; tests explain *why*; new code
copies the house pattern instead of inventing one; PRs map the change to the requirements;
AI-powered features get a fixed test suite before they're built. Each runbook can only use
the tools its job needs.

## .mcp.json — the shared plug-ins

Plug-ins give the AI extra abilities. The committed file is the team's shared set — open the
repo once, approve once, and they're there for everyone: `context7` (accurate library docs),
`sequential-thinking` (step-by-step reasoning aid), and `playwright` (drives a real browser)
in every repo; `microsoft-learn` arrives with the .NET pack; `github` (issues, PRs, CI runs —
per-developer GitHub sign-in) with the GitHub pack; `azure-devops` (work items, PRs,
pipelines) with the Azure DevOps pack. Two hard rules: **exact versions only** (a plug-in
that always pulls "latest" is an open door for tampered software), and **no credentials in
the file, ever** — sign-in is always per developer. Personal plug-ins stay in personal
machine config; self-installing tools (GitNexus) ship printed instructions instead.

## The pull-request checks — workflows/

These run at the server and apply to every change, whoever wrote it. Build & tests **block** —
and the job opens with a secret scan, so a committed credential fails the build before anything
else runs. A broken build or a committed secret is a fact, and facts block. The AI grader **advises only**: its review must
happen, but "the AI approved it" never replaces the human approver. Correctness and security
reviews **block** on concrete, demonstrable findings, with a visible, recorded human
override. Branch protection tops it off: blocking checks are mandatory and a person who
didn't write the change must approve it. In one sentence: *machines verify the facts; a human
makes the call.*

Before trusting any gate, run the drills in `RAILS.md`: break the build on purpose, plant a
defect, commit a fake secret — and watch each gate catch it.

## Where the pieces come from (custody chain)

```
delivery-standard/kit      the source of truth (this repo)
        │  sync_kit.py
claude-code-sdlc/harness   the plugin's bundled copy — generated, never hand-edited
        │  install_harness.py --profile
product repo               composed core + packs, then adapted during setup
```

After install there is no live link back. Updating a repo is deliberate — update the plugin,
re-run the installer — and existing files are never overwritten unless forced, so a repo's own
adaptations are safe.
