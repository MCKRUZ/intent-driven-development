# The Harness Kit — Research & Design

*How to build the best possible Claude Code harness for a team delivering under this standard,
worked against the `microsoft-agentic-harness` codebase. Research synthesized mid-2026; the
buildable result is `kit/`.*

---

## 0. What this is and how to read it

The Delivery Standard's **§6 (the harness standard)** and **§10 (the kit)** describe what every
client repo contains after kit install — but the `kit/` directory did not exist yet (PROGRESS:
"NONE built yet"). This document is the research behind, and the design of, the first build of
that kit. The kit itself ships as drop-in files under `kit/`; this report explains *why each
choice was made*, flags every feature by **maturity tier**, and records the drifts a maintainer
should reconcile.

It was produced from four parallel research streams:
1. **Requirements** — every harness obligation extracted from the standard.
2. **Capability map** — current Claude Code feature surface, maturity-tiered.
3. **Gating/grader/eval patterns** — citation-verified against Anthropic's own docs.
4. **Audit** — the existing harness in `microsoft-agentic-harness`, judged against §6.

### Maturity legend (used throughout and in the kit files)
- 🟢 **STABLE** — GA since early 2025, schema unchanged, safe to depend on.
- 🟡 **NEWER** — GA but still evolving; adopt deliberately, expect minor churn.
- 🔴 **BLEEDING-EDGE** — emerging; pin versions, isolate, treat as opt-in.

---

## 1. The decision frame

Eight choices set the shape of this build (all confirmed with the requester):

| # | Decision | Choice |
|---|---|---|
| 1 | Role of `microsoft-agentic-harness` | **Worked example → reusable kit.** The kit is generic; that repo is the realistic test case. |
| 2 | The repo already has a `.claude/` | **Audit, then evolve** — lift what's strong, replace what's weak. |
| 3 | Harness scope | **Full §6 stack** — CLAUDE.md + `.claude/` + workflows + infra gates + eval module. |
| 4 | Deliverable | **Report + drop-in template** (this file + `kit/`). |
| 5 | Feature currency | **Newest, flagged by maturity** — use the current surface, tier every piece. |
| 6 | Template stack shape | **Neutral skeleton + a worked .NET-10 / agentic profile.** |
| 7 | §11 eval module | **Build it** — the target is itself an agent; evals are the differentiator. |
| 8 | Research method | **Hybrid** — parallel doc-verified streams + direct repo audit. |

---

## 2. What the standard requires of a harness

The standard is unusually specific. The harness must encode the **build loop** (Intent → Delegate
→ Discern), a **Definition of Ready** (the vague-line test), a **Definition of Checked** ("proven
against its spec by something other than its author"), a **risk taxonomy** (HIGH/MEDIUM/LOW), the
**five-rung checking ladder**, and a set of **gates with teeth**. The load-bearing obligations:

- **The Stop hook** is "the single highest-value automation we keep" — it refuses to let the agent
  finish on a red test or broken build. CLAUDE.md states the rule as *"done means the hook lets
  you stop."*
- **Five CI workflows, not four.** `ci` (blocks), `grader` (advises — required to run, verdict
  never blocks), `correctness` (blocks on a high-confidence logic defect), `security` (blocks on
  HIGH, path- or label-triggered), `deploy-dev` (ships to dev, restores on failure).
  > **Drift flag #1:** GOLD-STANDARD §6's tree lists only four (`ci/grader/security/deploy`).
  > `docs/the-rails.md`, PROGRESS, and the 2026-06-19 retro all say **five** — `correctness` is
  > the fifth. Five is authoritative; §6's tree was stale. The kit ships five.
  > **Resolved 2026-06-30:** the §6 and §10 trees (in `GOLD-STANDARD.md` and `.html`) were updated
  > to list five.
- **The merge bar:** CI green + grader-has-run + correctness-passed (or recorded named override) +
  **a non-author approval**; HIGH adds security pass + a named sign-off recorded in the PR. The
  agent pushes only to `spec/NNNN-*`, can't self-merge, commits co-authored.
- **An agent gate may block on a defect, never on a judgment.** That single line explains the whole
  split: `ci`/`correctness`/`security` block (mechanical or concrete-defect); the grader advises
  (spec-match is a judgment a human must own). *"A polished, plausible explanation is exactly how
  an agent talks a human into approving harm."*
- **Prove the rails before trusting them.** Before Foundation closes, each rail is forced to fail:
  a failing test trips the Stop hook, a planted spec-mismatch makes the grader post the miss, a
  planted logic defect blocks correctness *and* the override clears it, a known-bad deploy
  restores, a probe PR on a guarded path fires security. *"A rail that has only ever seen green has
  not been tested; it has been assumed."*
- **Metrics that don't lie:** report **"no data," never a fabricated zero** (the change the
  2026-06-24 retro made to the standard); **never track** velocity, story points, PR count, or LOC.
- **§11 (when the deliverable is an agent):** evals are acceptance criteria (golden set versioned
  next to the spec, a threshold, CI runs them like tests); prompts/models/tool-definitions are HIGH
  risk and gated by an **eval-regression** check; observability (tracing, token cost, failure-mode
  logging) is required, not optional.
- **Constraints:** secrets in the client's Key Vault — never in code, CLAUDE.md, or specs; the LLM
  key is client-procured; `.sdlc/` state committed to the client repo; the delivery repo lives in
  the client's org from day one ("guests in their org").

---

## 3. Claude Code capability map (maturity-tiered)

Verified against `code.claude.com/docs` and the Anthropic engineering posts. Where the first-pass
research returned plausible-but-unverifiable specifics (hallucinated skill frontmatter fields,
non-existent hook handler types, a stale model id), those were **discarded** and the canonical
schema used instead.

| Capability | Tier | Harness use |
|---|---|---|
| CLAUDE.md / memory, `@imports`, precedence | 🟢 STABLE | The governance contract. Keep lean; `@import` depth. |
| `settings.json` permissions / hooks / env | 🟢 STABLE | Permission rails + hook registration. |
| Hooks (`PreToolUse`, `PostToolUse`, `Stop`, `SubagentStop`, `SessionStart/End`, `UserPromptSubmit`, `PreCompact`) | 🟢 STABLE | Stop-gate, review-gate. |
| Subagents (`.claude/agents/*.md`) | 🟢 STABLE | grader, security-reviewer. |
| Subagent auto-spawn triggers | 🟡 NEWER | security-reviewer "use proactively". |
| Skills (`.claude/skills/*/SKILL.md`, progressive disclosure) | 🟡 NEWER | spec-writer, test-writer. |
| Slash commands (legacy) | 🟢 STABLE (superseded by skills) | Prefer skills. |
| Plugins + marketplaces | 🟡 NEWER | Optional packaging of the kit (see §6). |
| Output styles | 🟡 NEWER | Optional team voice; not load-bearing. |
| Background tasks / `/bg` | 🟡 NEWER | Long builds; not in the gate path. |
| Workflows / Tasks API | 🔴 BLEEDING-EDGE | Multi-agent orchestration; opt-in. |
| MCP — stdio | 🟢 STABLE | Local tools. |
| MCP — HTTP / OAuth / remote | 🟡 NEWER → 🔴 | Team/prod tool servers. |
| `claude-code-action@v1` (CI) | 🟡 NEWER | grader/security/correctness/eval workflows. |

**Verified hook contract (the part that's easy to get wrong):**
- A `Stop` hook **blocks** by writing top-level JSON `{"decision":"block","reason":"…"}` to stdout
  **and** `exit 2`. **`exit 1` is silently ignored** (treated as a non-blocking error).
  `hookSpecificOutput` is **invalid on Stop** and silently drops the block — put everything in
  `reason`, which is the only channel surfaced back to the model.
- `stop_hook_active` is the **loop guard** — `exit 0` when true, so the gate pushes back exactly
  once per stretch. Claude force-ends after **8 consecutive blocks** (a backstop, not a substitute
  for the guard).
- `PreToolUse` is different: it *does* use `hookSpecificOutput.permissionDecision: "deny"`.

**Verified permission model:** evaluation order is **`deny → ask → allow`**, and **deny cannot
carry exceptions**. A user's local `settings.json` can loosen `allow` but must not be able to undo
a team prohibition — therefore the **shared** `settings.json` leans on `deny` for hard stops; `.env`
and `secrets/**` belong in `deny`, not `ask` (there's no safe reason for the agent to read raw
secrets).

**Packaging the kit across many repos** (for the harvest loop):

| Method | Verdict |
|---|---|
| **Template repo / kit install** (current §10 model) | ✅ Default. Full control, adapted-in-the-open per client (the adaptation PRs are the client's first look at how we work). |
| **Plugin + marketplace** | ✅ **Built (2026-07-01).** The kit ships via the `claude-code-sdlc` plugin (`/plugin install claude-code-sdlc@mckruz` → `/sdlc-setup`), which scaffolds it into the client repo. Gives one-command install + `/plugin update` across repos. |
| **Git submodule** | ❌ Not recommended — workflow friction, breaks often. |

---

## 4. Verified gating, grader, and eval patterns

These are the citation-verified foundations the kit's gates implement.

- **Stop-hook gating** — the only hook that decides whether the agent is *allowed to be finished*.
  Reference design ships as `kit/hooks/stop-gate.{ps1,sh}`: loop-guard on `stop_hook_active`, run
  build/tests/format, `block()` = print `{"decision":"block","reason":…}` then `exit 2`,
  `timeout`-wrap every check. **Test it three ways before trusting it** — a passing case (stays
  quiet), a failing case (blocks), and a turn it shouldn't apply to (steps aside). "Until you have
  seen the gate do all three with your own eyes, you do not have a gate."
- **Grader ≠ author, structurally.** The grader runs in a fresh context / clean checkout and sees
  only the diff and the spec, not the reasoning that produced the change. Reliability levers that
  separate a real grader from theater: a structured rubric (not vibes), anchor to the spec/
  reference, **grade the product not the path**, report gaps not style, and — critically — the
  verdict must be able to fail the build to matter. The standard's resolution: the **grader
  advises** (spec-match is judgment), the **correctness gate blocks** (a concrete logic defect is
  checkable). Both run in CI in a clean checkout, so author≠grader is enforced by construction.
- **Agent evals** (Anthropic, *Demystifying evals for AI agents*): start with **20–50 tasks from
  real failures**; **deterministic graders first**, LLM graders only where needed; **grade the
  output, not the trajectory** (exact tool-call sequences are too brittle); **isolated clean env
  per trial** (shared state both correlates failures and lets the agent cheat — Anthropic caught
  Claude reading prior-trial git history); **run multiple trials, track variance**; combine
  state-check + transcript-constraint + llm-rubric graders. Gate PRs on a **small fast (~30-case,
  <5 min) regression suite** with a regression trip-wire.
  > **Calibration note:** the ~±3% trip-wire, ~30 cases, <5 min, and 85–90% judge-vs-human
  > agreement are **practitioner conventions** from the field sources, **not** Anthropic-published
  > constants. The kit ships them as defaults to calibrate against your own measured variance.

---

## 5. The audit — two harnesses, and where the gaps are

The decisive finding: `microsoft-agentic-harness` contains **two** things that both speak
Claude-ish vocabulary, and only one is the §6 harness.

1. **The delivery harness** — `.claude/`, hooks, and `.github/` rails that govern *how agents build
   the repo*. **This is §6's subject.**
2. **The product's own agentic harness** — top-level `agents/`, `skills/`, `plugins/`, MCP, RAG.
   These are **Microsoft Agent Framework runtime artifacts** (the application), not Claude Code
   config. `skill_type`, `model_override`, `AGENT.md` are *product* fields, not Claude Code ones.

Conflating them would have produced a broken kit. The kit generalizes only layer (1).

**What's strong (lifted into the kit, generalized):** the `.github/` rails *exceed* §6 — a
fail-soft advisory `grader.yml`, a fail-closed anti-tamper `security-review.yml` (verdict written
outside the worktree so the agent can't edit its own grade), a `correctness-review.yml`, the
rubric-as-separate-file pattern, an `eval-bypasses.md` override ledger, branch-protection-as-code
with an idempotent applier, deterministic line-anchors, and an exemplary `RAILS.md` with a
**shakedown-drill** section that is exactly §9's "prove the rails" discipline written down. The
`stop-build-gate.ps1` is best-in-repo: fail-closed, loop-guarded, dirty-source-scoped. The
`settings.json` allow/ask/deny split is a near-perfect §6 reference.

**What was missing (authored fresh — the "intent spine"):**
- **`specs/` + a governance CLAUDE.md.** The existing CLAUDE.md is an *architecture* doc — no
  domain glossary, no risk taxonomy, no DoR/DoC, no gated-paths list, no "done means the hook lets
  you stop." Specs were deferred entirely; the grader graded against the **PR description**, not a
  committed spec file in the diff.
- **Local `.claude/agents/`** — grader/security existed only as CI prompts; the §6 subagent form
  (and "the grader never grades its own work" as an agent definition) was absent.
- **`infra/` + `deploy-dev.yml` + `.sdlc/`** — deliberately deferred (no cloud yet).
- **A rules-loading bug worth flagging:** `.claude/rules/*.md` carry Cursor-style `paths:`
  frontmatter, which **Claude Code does not natively honor**, and CLAUDE.md doesn't `@import` them
  — so that governance may never reach the agent. The kit's CLAUDE.md keeps stack standards inline
  / `@import`-ed instead.

---

## 6. The kit, file by file

The build pairs the repo's strong enforcement machinery with the freshly-authored intent spine.
**L** = lifted & generalized from the source repo · **N** = newly authored · **F** = built fresh
(the source deferred it).

```
kit/
├── CLAUDE.md.template        N  governance: build loop, DoR/DoC, risk taxonomy, ladder,
│                                gated paths, metrics discipline, agentic-work rules, profile
├── spec-template.md          N  the 7-part spec; one spec = one branch = one PR
├── settings.json             L  allow/ask/deny (deny-leaning shared file) + Stop/PreToolUse hooks
├── hooks/
│   ├── stop-gate.ps1/.sh     L+F  blocking Stop hook (verified contract) + bash twin
│   ├── review-gate.ps1/.sh   L+F  PreToolUse: no push without /code-review + /simplify receipts
│   └── save-review-receipt.* L+F  commit-bound review receipts
├── agents/                   N  6 agents, model-tiered (see §6a); README = catalog + on-demand menu
│   ├── planner.md            N  opus — Delegate: plan before code (MEDIUM/HIGH, 5+ files)
│   ├── architect.md          N  opus — HIGH-risk design decisions feeding a spec
│   ├── grader.md             N  sonnet — advisory, spec-by-spec, line-anchored, never grades own work
│   ├── security-reviewer.md  N  opus — auto-spawn; blocks on HIGH, gated-path/label-triggered
│   ├── build-error-resolver.md N sonnet — auto-spawn; clears the Stop hook's block, minimal diff
│   └── debugger.md           N  sonnet — isolated root-cause; returns a distilled diagnosis
├── skills/                   N  6 team-practice skills
│   ├── spec-writer/          N  story → Definition-of-Ready spec (vague-line test)
│   ├── test-writer/          N  tests that encode WHY; failing-test-first for bugs
│   ├── api-pattern/          N  add a surface the way the codebase already does it (§6-named)
│   ├── pr-writer/            N  branch → conventional commit → spec-mapped PR + test plan
│   ├── eval-builder/         N  build a versioned golden set for an agentic spec (§11)
│   └── diagnose/             N  bug-fix procedure: failing test first, then fix, then prove
├── workflows/
│   ├── ci.yml                L  build + test + coverage (hard block)
│   ├── grader.yml            L  advisory; grades the spec FILE in the diff (reconciled)
│   ├── correctness.yml       L  blocks on high-confidence logic defect; named override
│   ├── security.yml          L  fail-closed, anti-tamper; blocks on HIGH
│   ├── deploy-dev.yml        F  merge → dev; restore last good on failure; promote, don't rebuild
│   ├── eval-regression.yml   F  per-PR eval gate for prompt/model/tool/agent changes
│   ├── eval-suite.yml        L  large periodic benchmark suite
│   └── RAILS.md              L  operator's guide + the shakedown drills
├── profile/                  L  rubrics/, eval-bypasses.md, CODEOWNERS, rulesets/, scripts/
├── eval-datasets/            L+N golden-set template + how-to (20–50 real-failure tasks)
├── prompts/                  L  versioned judge-prompt convention (HIGH risk, no drive-by edits)
└── infra/                    F  minimal Bicep dev-env starter + agent-safe IaC pipeline note
```

**One reconciliation baked into the build:** the lifted `grader.yml` + grader rubric grade against
**`specs/NNNN-name.md` in the diff** (falling back to the PR description with a warning when no
spec file is present), closing the gap the audit found.

---

## 6a. Agent & skill surface — the breadth decision

The first build shipped only the two agents and two skills §6 *names*. That's a defensible floor
but under the loop's real needs, so the surface was benchmarked against the best public collections
and the team's own trusted set.

**What's out there.** The leaders are large: `wshobson/agents` (194 agents / 88 plugins,
model-tiered opus/sonnet/haiku, eval-backed — the highest-engineered), `VoltAgent/awesome-claude-code-subagents`
(154 / 10 categories), Anthropic's official marketplace (243 plugins, mostly vendor), `anthropics/skills`
(17 first-party), and `obra/superpowers` (the dominant SDLC *skill framework*). The kitchen-sink
catalogs (davila7/aitmpl, rohitg00) advertise their size as the feature — the tell, not the strength.

**Why lean is correct, from Anthropic's own guidance.** Context is a finite attention budget;
every installed skill's name+description sits in the system prompt *whether or not it fires*, so a
bloated set has a standing cost and worse selection. "Find the smallest high-signal surface."
Subagents earn their place by working in an *isolated* context and returning a distilled result —
which argues for single-responsibility agents, against general-purpose ones. The team's own
`agents.md` already lives this (4 agents; the rest retired to commands/skills; only 2 auto-spawn).

**The decision: lean-but-complete, model-tiered, deterministic-work-as-commands.** Ship one agent
per consensus role the *delivery loop* needs, tier the models, keep deterministic workflows as
commands, and push the long tail to a curated install-on-demand menu (so the close-gate — "nothing
the team doesn't understand" — stays satisfiable). Final shipped surface: **6 agents** (planner,
architect, grader, security-reviewer, build-error-resolver, debugger) + **6 skills** (spec-writer,
test-writer, api-pattern, pr-writer, eval-builder, diagnose), plus three **built-in command
dependencies** the kit relies on rather than duplicates: `/code-review` + `/simplify` (the
`review-gate` hook blocks a push until both run) and `/update-docs`. The catalog, model tiers, and
the on-demand menu live in `kit/agents/README.md`.

**Personal-toolkit skills were deliberately excluded** from a *client* kit (e.g. communication-style,
humanizer, deep-research-plus, executive-eye) — a delivery harness ships only what serves the loop
and the gates.

---

## 7. Drift flags for the standard's owner

The kit is correct; these are inconsistencies in the *standard's prose* that the harvest-loop
deputy should fix:

1. **Four vs five workflows.** ✅ *Resolved 2026-06-30* — §6's tree now lists `correctness.yml`
   (with grader marked advisory and security as gated-path/label-triggered).
2. **§10's kit tree** ✅ *Resolved 2026-06-30* — now lists five workflows plus a note pointing to
   `eval-regression.yml` / `eval-suite.yml` for §11 agentic specs.
3. **Rules loading.** If the standard intends `.claude/rules/`, it must specify `@import` from
   CLAUDE.md (Claude Code does not auto-attach by `paths:` frontmatter).
4. **`docs/agentic-spec-example.md`** is forward-referenced in §11 but unwritten — the kit's
   `eval-datasets/README.md` + `golden-set.template.yaml` give it a concrete starting point.

---

## 8. What to verify at install, and open items

- **Hook registration form.** The source `settings.json` uses `{"command":"pwsh","args":[…]}`,
  valid only on CLI **v2.1.139+**. The kit uses the single-string `"command":"pwsh -NoProfile
  -File …"` form for maximum compatibility — confirm against the client's installed CLI.
- **Prove every rail** on install (the §9 shakedown), don't assume them. `RAILS.md` lists the drills.
- **Calibrate eval thresholds** to measured variance before trusting the trip-wire.
- **Plugin packaging** is done — delivered via the `claude-code-sdlc` plugin (`/sdlc-setup`).
- **`infra/` and `deploy-dev.yml` are starters**, not turn-key — adapt to the client's Azure
  landing zone; IaC is HIGH risk every time.

---

## 9. Sources

Anthropic / official:
- Best practices for Claude Code — https://www.anthropic.com/engineering/claude-code-best-practices
- Hooks reference — https://code.claude.com/docs/en/hooks
- Configure permissions — https://code.claude.com/docs/en/permissions
- Subagents — https://code.claude.com/docs/en/sub-agents
- Agent Skills overview — https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Plugin marketplaces — https://code.claude.com/docs/en/plugin-marketplaces
- MCP — https://code.claude.com/docs/en/mcp
- GitHub Actions / claude-code-action — https://code.claude.com/docs/en/github-actions · https://github.com/anthropics/claude-code-action
- Demystifying evals for AI agents — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- A statistical approach to model evaluations — https://www.anthropic.com/research/statistical-approach-to-model-evals
- Effective context engineering for AI agents — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Equipping agents for the real world with Agent Skills — https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Building effective agents — https://www.anthropic.com/research/building-effective-agents

Agent/skill collections (benchmarked for §6a):
- wshobson/agents — https://github.com/wshobson/agents
- VoltAgent/awesome-claude-code-subagents — https://github.com/VoltAgent/awesome-claude-code-subagents
- awesome-claude-code — https://github.com/hesreallyhim/awesome-claude-code
- claude-code-templates / aitmpl — https://github.com/davila7/claude-code-templates
- Anthropic official plugins — https://github.com/anthropics/claude-plugins-official
- anthropics/skills — https://github.com/anthropics/skills
- obra/superpowers — https://github.com/obra/superpowers

Practitioner / community (treated as conventions to calibrate, not constants):
- How Claude Code stop hooks work — https://amitkoth.com/claude-code-stop-hooks/
- Claude Code permissions guide — https://www.developersdigest.tech/blog/claude-code-permissions-settings-guide
- LLM-as-a-judge — https://www.evidentlyai.com/llm-guide/llm-as-a-judge · https://www.comet.com/site/blog/llm-as-a-judge/
- Are LLMs Reliable Code Reviewers? — https://arxiv.org/html/2603.00539v1

Internal:
- `GOLD-STANDARD.md` §4–§11, §14 · `docs/the-rails.md` · `retros/` (2026-06-19, 2026-06-24) · PROGRESS.md
- `microsoft-agentic-harness` `.claude/` + `.github/` (audited, not modified)
