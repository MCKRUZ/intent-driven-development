# The Rails

Deep-dive on the CI/CD and DevOps pipeline every agent-built change rides. The rails are not a
phase. They get **built** in Phase 3 (the factory), they run under **every** change all through
Build, the same artifact gets **promoted** to production in Phase 8, and they get **watched** in
Phase 9. This page is the pipeline itself, as a standing standard: the workflows, the merge bar,
the deploy-and-promote path, the infrastructure pipeline, the agents that work inside the
pipeline — and the one principle that governs all of it.

That principle is the whole reason agent-built software can be trusted to ship at all: **the agent
proposes, a gate disposes.** An agent investigates, plans, and produces a change as a reviewable
artifact — a branch and a pull request, an infrastructure plan, a fix suggestion — but a
deterministic policy layer plus a named human decides whether that change ever takes effect. This
is not our invention. It is what every mature agentic-DevOps system in the industry converged on,
independently, by 2026: none of them lets an agent merge to a protected branch or apply
destructive infrastructure unsupervised. The rails are where that rule stops being a good
intention and becomes a fact about the world.

> **The gates at a glance.** Four workflows, plus the branch protection that makes them
> mandatory. **ci** — build/test/lint/coverage — *hard block*. **grader** — a fresh agent's
> check-by-check verdict against the spec — *required to run; advises, never blocks*. **security**
> — the security-reviewer agent, on a `risk:high` label or any guarded path — *blocks on HIGH*.
> **deploy-dev** — ships the merged artifact to dev and rolls back on a failed deploy. All four
> ride one rule: the agent proposes, a gate disposes. The detail is in section 3–section 5.

**If you're starting here:**

|                          |                                                                                                                                                                                                             |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The method**           | Claude (the AI coding agent) drafts documents and writes most code. Humans own every decision and verify every result.                                                                                      |
| **The rhythm**           | Numbered phases open and close the engagement; in between runs a continuous build loop. Each phase ends with automated checks (the **gate**) plus a named human sign-off. Gates are the billing milestones. |
| **Where the rails live** | Built in Phase 3, before any feature exists. Run under every change all through Build. Promote the proven artifact to production in Phase 8. Watched in Phase 9. The rails outlast every phase boundary.    |
| **Our pod (4-6 people)** | Pod Lead · Setup Owner · Orchestrators · Quality Engineer. ([Team deep-dive](team.md)) The Setup Owner owns the rails as a product.                                                                          |

**Words this page leans on** (every other term is explained where it first appears):

| Term                              | What it means                                                                                                                                                                                  |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The rails**                     | The enforcement, taken together: CI gates, the grader, branch protection, the deploy pipeline, and the infrastructure pipeline. Called rails because nobody has to remember them — every change runs on them. |
| **CI**                            | Continuous integration — the automated checks (build, tests, lint, test coverage) that run on every proposed change before it can merge.                                                       |
| **A workflow**                    | One automation file in the repo (a GitHub Actions YAML) that runs on a trigger — a push, a PR, a label, a merge. The rails are four of them.                                                   |
| **PR**                            | Pull request — the proposed change under review. One spec = one branch = one PR.                                                                                                               |
| **The grader**                    | A fresh AI agent that did **not** write the code. It reads the spec and the change and posts a check-by-check verdict on the PR. Required to run; its verdict advises — the human Checker decides. |
| **The Stop hook**                 | A script that fires when an agent tries to finish its turn. If tests fail or the build is broken, it refuses to let the agent stop. "Done" stops being the agent's opinion.                     |
| **Branch protection**             | Repository settings that make the gates mandatory: no change merges without CI green, the grader having run, and an approval from someone who didn't write it.                                  |
| **The deploy pipeline**           | The workflow that ships a merged change to an environment. Merge to main deploys to dev automatically; promotion up to test and prod is deliberate and gated.                                   |
| **Promotion**                     | Moving the **same proven artifact** up an environment: dev → test → production. The same pipeline, the same build, a different target — never a rebuild, never a hand-copy.                     |
| **Rollback**                      | The exact, rehearsed procedure that returns an environment to the previous version — with a written trigger, not a judgment call invented mid-incident.                                        |
| **IaC / Bicep**                   | Infrastructure as code — the cloud environment defined in version-controlled files instead of clicked together by hand. Bicep is Azure's language for it; the pattern is stack-independent.    |
| **Gated path**                    | A file or directory in the repo (migrations, auth, the pipeline itself, infrastructure) where any change is held to extra review, independent of the spec's risk tier.                          |
| **Dry-run**                       | Running a change in read-only preview to see what it *would* do without doing it: `bicep what-if`, `terraform plan`, a `--dry-run=server` apply. The infrastructure equivalent of plan mode.   |
| **Policy-as-code**                | Rules about what infrastructure is allowed — no public storage, encryption on, tags present — written as code that runs as a gate, so the check is mechanical, not a reviewer's memory.        |
| **Agent proposes, gate disposes** | The governing rule: an agent may produce any change, but only as a reviewable artifact; a deterministic check plus a named human decides whether it takes effect. The rails enforce it.          |
| **Least-privilege identity**      | Every actor — human or agent — gets its own credential scoped to exactly what its job needs and nothing more. What an agent *can* do is bounded by its permissions, not by its instructions.    |

This page answers five questions, and nothing else:

1. **What is the one rule the rails enforce, and why does everything hang off it?** (agent
   proposes, gate disposes — and its three corollaries)
2. **What are the gates, concretely?** (the four workflows, the merge bar, what blocks and what
   advises)
3. **How does a change reach production safely?** (deploy, promotion, the rehearsed rollback)
4. **How is infrastructure changed without a 2 a.m. incident?** (the agent-safe IaC pipeline:
   generate → validate → policy → dry-run → approve → scoped apply → watch drift)
5. **When agents work *inside* the pipeline, what holds them?** (bounded tools, self-validation,
   least-privilege identity, containment)

Operating the rails day to day, promoting to production, and tuning production alerts are out of
scope here — those are the Build loop, Phase 8, and Phase 9. This page is the pipeline as an
artifact: how it is built, what it enforces, and the principle it exists to make unavoidable.

> **Worked example:** [`the-rails-example.md`](the-rails-example.md) — six episodes of the rails
> doing their job at Harbor Mutual: the grader catching a bug eleven green tests missed, a
> self-healing pipeline that stops at a PR, a flaky test quarantined instead of "fixed," a Bicep
> change through the what-if funnel, the rollback that failed in rehearsal first, and drift
> proposed-not-applied — with an honest table of what in it is net-new to the kit.

---

## 1. The one principle: agent proposes, gate disposes

Strip away the vendor names and every working agentic-DevOps system in 2025–2026 is the same
shape. The agent does the investigating, planning, and producing. It stops at a **reviewable
artifact**. A deterministic policy layer plus a human decides whether the artifact takes effect.
The agent never has the last word on a protected resource.

The pattern is so consistent across the industry that it reads like a law:

- A leading vendor's **coding agent** can only push to branches it creates, cannot approve or
  merge its own work, and its checks will not even run without explicit human approval —
  autonomy bounded by the same branch protection humans live under.
- A **self-healing CI agent** that diagnoses a broken pipeline stops at a merge request with the
  fix. It does not push to the protected branch; it proposes.
- An **infrastructure health system** that detects configuration drift visualizes it and
  *proposes* a remediation plan. Applying it is a human choice, never a silent auto-apply.

Three different companies, three different problems, one rule. We did not adopt it because the
industry did; we arrived at it for the same reason they did — it is the only rule that holds when
the agent is wrong, and a probabilistic actor is sometimes wrong. This is the same sentence that
runs through the whole standard — **gates report, humans decide** — and the rails are where it is
mechanically enforced rather than merely intended.

Three corollaries fall out of the principle. Each one is a design rule for the rails, not a nicety:

- **Mechanical self-validation is mandatory.** Before an agent surfaces a change as done, it must
  re-run the build, the tests, the linters from the environment itself and prove them green — not
  assert success, prove it. This is exactly what the **Stop hook** is: the agent cannot end its
  turn on a red test or a broken build. An agent's claim that something works is an opinion; the
  environment's green is ground truth. The rails trust only the second.
- **A bounded tool surface beats raw access.** An agent given named, constrained tools
  (read a file, write a file, run the tests, run the linter) outperforms — and is far safer than —
  an agent handed the whole filesystem and a shell with "fix it." The constraint is not a
  limitation to apologize for; it is the thing that makes the agent's behavior legible and its
  blast radius small.
- **Autonomy is graded, and it widens slowly.** A new piece of agent automation starts in a
  *propose-and-approve* posture — it recommends, a human disposes — and only graduates to a
  tighter loop after its behavior has been watched and trusted on real work. The risk of agentic
  systems is almost never the model being dumb; it is granting too much autonomy too quickly. The
  rails make the cautious default the easy one.

And underneath all three: **identity is the real guardrail.** What an agent can do is bounded by
the permissions of the credential it runs under, not by the words in its prompt. When a prompt
fails — and prompts fail — the identity is what is still holding. Section 8 is where this gets
concrete.

---

## 2. Who is involved

The rails are the **Setup Owner's** product, the way Intent is the Pod Lead's and design is the
architect's. They are built in Phase 3 and tended as a product for the whole engagement: the
workflows, the branch protection, the infrastructure code, the secrets handling. The Setup Owner
is never the sole approver of their own rails — a named deputy reads every change, because the
both-eyes rule applies hardest to the code that *is* the factory.

### Our side

| Person                   | In the rails                                                                                                                                                                  |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Setup Owner**          | Owns the rails as a product: the four workflows, branch protection, the infrastructure pipeline, secrets handling, the agent identities. Drafts with Claude; reviews everything; merges none of it alone. |
| **Setup Owner's deputy** | Named on day one (the senior Orchestrator in a 4-6 pod). Reviews every rails change — workflow YAML, IaC, identity scope. The both-eyes rule applied to the foundation.       |
| **Quality Engineer**     | Wires the mechanical gates (coverage, the eval gate on agentic specs) and — the part most teams skip — **proves the rails fail safely**: that the Stop hook actually blocks, the grader actually posts, the deploy actually rolls back. |
| **Orchestrators**        | Run changes through the rails all day. When the pipeline itself needs a fix, it rides the loop like any change — a spec, a plan, a bounded agent, a non-author Checker.       |
| **Pod Lead**             | Owns the risk tiers that decide how hard each path is gated, and the gate-exception rule for the rare true emergency.                                                        |

### Client side

| Person                         | Needed for                                                                                                                       |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| **DevOps / platform engineer** | Reviews every pipeline and IaC change — **they operate the rails after we leave.** Owns branch-protection admin, runner policy, the secrets vault. |
| **Security**                   | Signs off on the pipeline, the secrets handling, the agent identities and their RBAC scope, and the data-flow brief.             |
| **Sponsor**                    | Sees the rails proven at the Phase 3 exit demo — working software in their own dev environment, through the real pipeline.       |

### Claude's role in the rails

This is where Claude writes the most consequential code in the engagement — the code that *is* the
factory — and where that code is under the tightest gating, because a defect in the rails ships in
every change that rides them afterward.

- **Drafts the workflow YAML and the Bicep.** Both HIGH risk: human review on every change, the
  deputy and the client's DevOps reading them before they merge.
- **Runs as the grader.** A fresh agent that did not write the change reads the spec and posts a
  check-by-check verdict on the PR — itself a part of the rails (section 3).
- **May propose pipeline and infrastructure fixes** — as a PR, never as an apply. A red pipeline,
  a drifted resource: Claude can analyze it and draft the fix, and the fix goes through the same
  merge bar as everything else (section 7).

What Claude never does: merge IaC or pipeline changes unattended, act as the sole approver of
rails work, apply infrastructure directly, put a secret anywhere near the repo, or hand-build a
pipeline shortcut "off the rails" to save a day. The entire value of the rails is that the first
real software went *through* them, not around them.

---

## 3. The gates: the four workflows

The rails are four workflows in the repo, plus the branch protection that makes them mandatory
(section 4). Each one has a job, and each one is clear about whether it **blocks** (a hard gate, a
machine's call) or **advises** (an input to a human's call). Confusing the two is how teams either
ship unreviewed agent code or drown every typo in ceremony.

| Workflow         | Fires on                                            | Blocks or advises                        | What it does                                                                                                                                          |
| ---------------- | --------------------------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ci**           | every PR                                            | **Blocks** (hard gate)                   | Build, tests, lint, 80% coverage on new code. The mechanical floor. A red CI is a closed door — no human can wave it through without an exception.    |
| **grader**       | every PR                                            | **Advises** (required to run, can't block) | A fresh AI agent reads the spec in the diff and posts a check-by-check verdict as a PR comment. "The grader ran" is a required check; *what* it said is the human Checker's input, not a gate. |
| **security**     | the `risk:high` label **or** any PR touching a registered gated path | **Blocks** on HIGH; **advises** otherwise | Runs the security-reviewer agent. Path-triggered: it fires on any PR that touches a guarded path (auth, migrations, the pipeline, infra) independent of the spec's tier. |
| **deploy-dev**   | merge to main                                       | n/a (it ships)                           | Deploys the merged artifact to the client's dev environment, and restores the last good version when a deploy fails — the rollback the rails rehearse. |

Two things about this table carry more weight than they look:

**The grader advises; it never blocks.** It is tempting to let a confident AI verdict gate the
merge. We do not, and the reason is in the threat model: a polished, plausible explanation is
exactly how an agent talks a human into approving harm. The grader's job is to surface the
check-by-check truth — including the hole the author was blind to — and hand it to a person who
owns the decision. Machines gate the mechanical (does it build, do the tests pass); humans own the
judgment (is this the right change, is this risk acceptable). The grader sits on the seam and
informs the human side without ever becoming it.

**The security gate is path-triggered, not just tier-triggered.** A change can be tiered MEDIUM and
still touch the auth code, the migration folder, or the pipeline YAML. Wiring a security gate means
registering its guarded path with the security workflow, so the workflow runs on *any* PR that
touches that path — in addition to firing on the `risk:high` label. The gate is the workflow plus
the path registration. This is why a "small" change to a dangerous file does not slip through on
its tier: the path catches it regardless.

---

## 4. The merge bar

Branch protection is what turns four workflows from suggestions into rails. It is repository
configuration — set by the Setup Owner or a named client admin applying our policy — and it makes
the gates mandatory at the one moment that matters: the merge.

Every PR, to merge, must clear:

- **CI green** — build, tests, lint, coverage, all passing. Hard block.
- **The grader has run** — the workflow completed and posted its verdict. The verdict can say
  anything; the *running* is required.
- **A non-author approval** — someone who did not write the change approved it. The author of a
  change is never its only approver. This is the rule that survives every collapse of pod size:
  even a two-person pod holds it.

A `risk:high` change adds two more:

- **The security workflow passed** — the security-reviewer agent's pass, blocking on HIGH.
- **A named human sign-off recorded in the PR** — a person, by name, accepting the risk. Not a
  thumbs-up; a recorded sentence with a name attached.

And the constraints on the agent itself, enforced by the platform, not by trust:

- The agent can push **only to branches it creates** (`spec/NNNN-*`), never to main.
- The agent **cannot approve or merge its own work** — the platform forbids it, the same way it
  forbids a human author from being their own approver.
- Every commit an agent makes is **co-authored**, so the provenance is in the history: who, or
  what, wrote this line is never a guess.

The merge bar has exactly one escape hatch, and it is deliberately expensive: a true emergency
merge past a gate requires the Pod Lead plus one other human, an exception label, and a Retro+
agenda item. Two exceptions in a month is not bad luck — it means the gate or the specs are wrong.
Fix that; do not normalize the bypass.

---

## 5. Deploy and promotion

A merge is not a deploy to production. The rails move a change up through environments, and the
gap between "merged" and "in production" is where the most important word in this section lives:
**promotion.**

The environment path:

- **Merge → dev, automatically.** The `deploy-dev` workflow ships every merged change to the
  client's dev environment with no human in the loop — because the merge already cleared the merge
  bar, and dev is the safe place for the rails to be exercised by real software constantly.
- **Dev → test, on demand.** Promoted deliberately, smoke-tested on arrival. The test environment
  is added at the first hardening pass, not in Phase 3 — Foundation builds the narrowest real
  thing.
- **Test → prod, by ceremony.** The first promotion to production is the Phase 8 go/no-go: evidence
  on the table, every named role asked, a human saying **go**, out loud, on the record. Every
  promotion after that rides the client's release cadence — and a human go/no-go **every** time.
  This is the single most protected stop in the standard, and no amount of agent confidence ever
  removes it.

Two rules govern every promotion:

**Promote the artifact; never rebuild it.** The same build that passed test goes to production —
promoted, not freshly compiled "real quick." A rebuilt artifact is something no environment ever
verified, running in the one environment where that matters. The pipeline moves the proven thing
up; it does not make a new thing at each step.

**A rollback that has never run is a wish.** The deploy pipeline restores the last good version
when a deploy fails — and that path is *rehearsed* before it is ever needed, in test, by the hands
that would run it at 2 a.m.: deploy → roll back → redeploy, with the trigger condition ("roll back
if X") written down in advance, not invented mid-incident. The rails are not proven by the YAML
being present; they are proven by a deploy failing and the rollback catching it. A rail that has
never failed safely has not been proven (section 9).

---

## 6. The infrastructure pipeline

Infrastructure is code, it lives in the repo, and it is **HIGH risk every time** — because it is
hard to undo and it runs in production later. An agent can draft a Bicep change in seconds; the
discipline is entirely in what stands between that draft and a changed cloud. The industry's
agent-safe IaC pipeline is a read-only-until-the-last-step funnel, and we run it as such:

```
generate IaC (agent drafts)
  → build / schema-validate          (does it even compile against the resource schema?)
  → static policy-as-code gate       (no public storage, encryption on, tags present, region allowed)
  → dry-run: bicep what-if           (read-only — what would this change, exactly?)
  → cost / budget review             (what does the diff cost; does it breach the budget gate?)
  → human approval gate              (a named human reads the what-if and the policy result)
  → scoped, least-privilege apply    (a deploy identity that can touch only this, nothing more)
  → continuous drift assessment      (real infra vs. code, on a schedule)
  → propose — not auto-apply — remediation when drift appears
```

Every step before the apply is read-only. That is the point: the agent and the pipeline can do all
the thinking, validating, and previewing they want, and *nothing changes* until a human has read
the dry-run and a least-privilege identity executes a scoped apply.

The pieces, on the .NET/Azure default (the pattern is stack-independent — see the profile-swap
appendix for what the names become elsewhere):

- **Schema validation** catches the malformed resource before it ever reaches the cloud. A
  generated template that does not validate is caught by a machine, not by an apply that
  half-succeeds.
- **Policy-as-code** is the security baseline as a gate: a rules engine (PSRule for Azure, or a
  scanner over the compiled ARM) blocks the public-by-default storage account, the unencrypted
  disk, the untagged resource group — mechanically, on every change, instead of relying on a
  reviewer remembering to look.
- **The dry-run is plan mode for infrastructure.** `bicep what-if` shows precisely what would be
  created, changed, or deleted. A human reads it before approving. An infrastructure change
  approved without reading its what-if is a change approved blind.
- **The cost gate** puts the price of the diff on the PR and can block on a budget breach.
  (Cost-estimation tooling is most mature on the Terraform profile; on the Bicep default the
  what-if pricing read carries it. Named honestly so nobody promises a tool that doesn't fit the
  stack.)
- **Drift assessment** runs on a schedule and compares the real environment to the code. When it
  finds drift, it **flags and proposes** — it does not silently re-apply the config over whatever a
  human changed by hand in a real incident. Remediation is a choice an operator makes, the same
  agent-proposes/gate-disposes rule one more time.

The infrastructure pipeline is the place the principle is least negotiable, because the blast
radius is largest. Never auto-apply a destructive change. Schema-validate before apply. Scope the
deploy identity to exactly the resources in play. A destructive `apply` an agent ran unattended is
the one mistake on this page with no clean undo.

---

## 7. Agents working inside the pipeline

This is the part the phrase "DevOps pipelines using agentic" points straight at: not only do agents
build software that rides the rails — agents work **inside** the rails, on the pipeline itself. A
red build, a flaky test, a drifted resource: an agent can investigate and fix it. The discipline
that makes this safe instead of reckless is everything in section 1, applied to the pipeline's own
machinery.

**The self-healing pipeline, done right.** When CI goes red, an agent can be pointed at the
failure: it reads the build logs, forms a hypothesis about the config or code at fault, works the
problem through a **bounded set of named tools** — read a file, write a file, run the tests, run
the linter — and iterates until the environment itself reports green. Then it emits the fix **as a
PR suggestion.** It stops at a merge request. It does not push to the protected branch; it proposes
the change and the change clears the same merge bar as everything else.

Two design choices separate a self-healing pipeline from a self-harming one:

- **Named tools, not the raw repo.** The reference implementations in the industry are emphatic on
  this: do not dump the whole repository and the whole failure log into the model and say "fix it."
  Give the agent a small, named tool surface and let it work through it. The bounded surface is
  what makes the agent's actions legible and its mistakes containable. "Here is the filesystem, go"
  is the prompt that produces the incident.
- **Self-validation before it surfaces a fix.** The agent does not get to claim the pipeline is
  fixed. It re-runs the tests and the lint from the environment and proves green, exactly as the
  Stop hook demands of any agent. A proposed fix that the agent has not validated against the
  environment is not a fix; it is a guess wearing a green checkmark.

**Flaky tests get a state machine, not a reflex.** The wrong design is "an agent fixes every red
test." A flaky test — one that fails intermittently with no code change — is not always a bug to
fix; sometimes it is a test to quarantine while a human looks. The industry-proven shape is a small
state machine — **Active → Quarantined → Disabled** — with eligibility thresholds before an agent
touches anything (a real failure rate, real wasted time, failures on the default branch, not a
single red run) and a grace period after a confirmed fix before the test rejoins the suite, so a
stale branch does not re-break CI. Triage and a state machine beat a reflex to "make it green."

**Containment wraps all of it.** An agent that touches the pipeline runs in a sandbox with
default-deny network egress and writes confined to its workspace. The environment layer — the
sandbox, the egress policy — catches what the model's own judgment misses. The worst real-world
agent incidents were not the model deciding to do harm; they were exfiltration through a *permitted*
path the model never flagged as dangerous. The containment is the backstop for exactly the failure
the model cannot see.

---

## 8. Identity, secrets, and blast radius

Every actor that touches the rails — human or agent — runs under its own credential, scoped to
exactly what its job needs. This is the guardrail that is still standing when a prompt has been
talked into something it shouldn't do. **No role grant, no resource access** — and an agent's
instructions cannot grant it a role.

- **Each agent that acts on infrastructure or the pipeline gets its own least-privilege identity.**
  A managed or federated credential — no stored secret, rotated automatically — beats a certificate,
  which beats a client secret. Scope it to the resource or resource group, never the whole
  subscription. An agent with its own narrow identity is also an agent whose every action is
  attributable to it in the audit log.
- **Secrets live in the client's vault, never in the repo.** Not in code, not in CLAUDE.md, not in
  a spec. The Anthropic API key, the Azure credentials, every token — the client's Key Vault and
  GitHub secrets from day one. A key in a commit is the one unrecoverable mistake of the
  foundation: a rotation event and an audit-log review, not an edit.
- **Secrets rotate before production.** Everything the pod ever touched gets rotated into
  production-only values the pod cannot read, signed by the client's security. The engagement
  should end with us having never known a production secret.
- **There is a kill switch.** Conditional-access policy applied at the class level means a whole
  category of agent identity can be disabled in one operation if something goes wrong. The ability
  to stop an agent class instantly is not optional infrastructure; it is part of granting the
  autonomy in the first place.

The mental model from the threat side: treat an agent as a first-class non-human identity with its
own lifecycle, owner, and time-bounded access — not as a script running under a human's
credentials. Agent sprawl (orphaned identities nobody owns, shadow automation nobody inventoried)
is its own risk; every agent identity has a named owner or it does not exist.

---

## 9. Proving and watching the rails

A pipeline that has never caught anything is not proven — it is merely present. The rails earn
trust by failing safely on purpose, and they keep it by being watched.

**Prove every rail by forcing its failure.** Before Foundation closes, each rail is made to fail
deliberately and caught:

- A failing test proves the **Stop hook** actually blocks an agent from finishing.
- A PR with a planted spec mismatch proves the **grader** actually posts the miss.
- A known-bad deploy proves the **pipeline restores** the last good version.
- A probe PR touching a guarded path proves the **security gate** fires — a throwaway change opened
  solely to confirm the gate triggers, then closed unmerged.

A rail that has only ever seen green has not been tested; it has been *assumed*. The shakedown is
not optional polish — it is the difference between a rail and a decoration.

**Watch the rails with the delivery numbers, not activity counts.** The health of the rails shows
up in the DORA four — deploy frequency, lead time, change-fail rate, time-to-recover — read as
trends, on the internal dashboard. Never velocity, story points, PR count, or lines of code: agents
inflate every one of those, and the published research is blunt about it — measured teams have
doubled PR volume while actual delivery stayed flat. The rails are healthy when changes flow and
fail rarely, not when the agents are busy.

**Log everything with provenance.** Every recommendation an agent made, every artifact that got
applied, every policy-gate outcome — logged centrally, with co-authorship on the commits, so any
change is traceable to the identity that produced it. After a poisoned tool-return steers an agent
into something it shouldn't, the log that only shows "a successful authorized call" is useless;
the provenance trail is what makes the rails auditable rather than merely automated.

---

## 10. What goes wrong with the rails

- **The pipeline that exists but was never exercised.** CI green because nothing real ever ran
  through it. The rails are proven by a change breaking and being caught, not by the YAML being
  present. Force each failure; a rail that has never failed safely has not been proven.
- **Auto-merging the agent's fix.** A self-healing pipeline that pushes its own fix to the
  protected branch has thrown away the only rule that makes it safe. The agent proposes; the merge
  bar disposes. Stopping at the PR is the whole design, not a limitation to optimize away.
- **The raw-shell agent.** Handing an agent the whole repo and a shell with "fix the build"
  instead of a bounded, named tool surface. It will touch three things nobody wanted touched, and
  the log won't tell you why. Named tools, every time.
- **The rebuilt artifact.** Production gets a fresh build instead of the promoted one that passed
  test — and now production runs something no environment verified. Promote, never rebuild.
- **The rollback that was only ever written.** Documented, reviewed, never run — then executed for
  the first time during an incident, where every surprise costs downtime. Rehearse it in test,
  before it is needed.
- **A secret in the repo.** The one unrecoverable foundation mistake. The client's vault from day
  one — never in code, never in CLAUDE.md, never in a spec.
- **The unattended destructive apply.** An agent runs an infrastructure `apply` that deletes or
  replaces, with no human reading the dry-run first. Every step before the apply is read-only for
  exactly this reason; the what-if is read by a person, always.
- **Autonomy granted too fast.** Wiring a brand-new agent automation straight to closed-loop
  because it worked twice. Autonomy widens slowly, after behavior is watched on real work. The
  primary risk of agentic ops is too much autonomy too soon.
- **The over-scoped agent identity.** An agent running with subscription-wide rights "to keep it
  simple." When its prompt is subverted, the blast radius is everything it could reach. Scope to
  the resource, give it its own identity, keep the kill switch.
- **Approval fatigue.** Gating every trivial step behind a human until the humans rubber-stamp
  without reading. Shift oversight from per-step to per-strategy — approve the plan up front,
  retain the ability to intervene — and keep the sandbox so an incautious approval is not
  catastrophic. Effective oversight is being positioned to intervene, not clicking approve a
  hundred times.
- **Ignoring drift.** The schedule flags that real infrastructure diverged from the code, and
  nobody acts, so the repo stops being the truth. Drift is a proposed remediation waiting for an
  operator, not a notification to dismiss.

---

> **Where this goes next.** This page is the **delivery rails** — the CI/CD and DevOps pipeline the
> pod builds so that agents can develop software safely. It is the primary, develop-*with*-agents
> track of the standard. There is a second track, for the engagements where the deliverable *is*
> autonomous operations: agentic AIOps, SRE-style incident agents that observe, diagnose, and
> remediate production, the two-tier (Review vs. Autonomous) trust model, and agentic remediation
> at scale. That companion deep-dive (forthcoming, with the first agentic-ops engagement) is a
> different track — but it runs on the exact same governing principle this page is built on: the
> agent proposes, a gate disposes.

Back: [Phase 3: Foundation](phase-3-foundation.md) — the phase that builds the rails and proves
them on the walking skeleton.

Next: [The Build Loop](build-loop.md) — what the rails were built for: how every change from
Foundation to feature-complete gets specified, bounded, built, and proven on them.
