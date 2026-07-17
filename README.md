# Intent Driven Development — The Delivery Standard

How our consulting pods build software with AI agents: gated phases open and close the
engagement, and a continuous per-spec build loop — Intent → Delegate → Discern — runs
everything in between. A fictional engagement (Harbor Mutual, a regional insurer) runs
alongside the standard as a worked example, phase by phase.

## In 30 seconds

Agents write code fast now. That doesn't make software delivery faster on its own — the hard part
moves to two places: **saying clearly what you want**, and **checking that what came back is
right**. This standard is how our pods run a client engagement around those two jobs.

The work runs as one short loop, repeated for every piece of work, and it reuses the name's
initials:

- **Intent** — a human writes a short, testable description of one piece of work (a _spec_).
- **Delegate** — an agent plans and builds it, inside bounds a human set.
- **Discern** — before anyone trusts it, automated gates and a non-author human check it's good.

Gated phases open and close the engagement; the loop fills the middle. **No checking is just vibe
coding — the loop closes it.** That's what makes the speed safe to put in front of a client.

## Start here, by who you are

- **Brand new to the method?** Read the [loop cheat-sheet](https://mckruz.github.io/intent-driven-development/docs/cheatsheet.html) (20 seconds),
  then the [glossary](https://mckruz.github.io/intent-driven-development/docs/glossary.html) for any word that trips you, then
  [The Delivery Standard](https://mckruz.github.io/intent-driven-development/GOLD-STANDARD.html) itself.
- **Prefer a story to a spec?** Follow [The Harbor Journey](https://mckruz.github.io/intent-driven-development/docs/journey.html) — one full
  engagement, start to finish, as a continuous worked example.
- **A pod member joining an engagement?** [The Delivery Standard](https://mckruz.github.io/intent-driven-development/GOLD-STANDARD.html) front to
  back, then [The Team](https://mckruz.github.io/intent-driven-development/docs/team.html) for your role, then the
  [build loop](https://mckruz.github.io/intent-driven-development/docs/companion/build-loop.html). Keep the [glossary](https://mckruz.github.io/intent-driven-development/docs/glossary.html) and
  [anti-pattern field guide](https://mckruz.github.io/intent-driven-development/docs/anti-patterns.html) open.
- **A client stakeholder or sponsor?** Read [In 30 seconds](#in-30-seconds) above, then the
  [FAQ](https://mckruz.github.io/intent-driven-development/docs/faq.html) — it answers the questions you're about to ask (data, decisions, what you'll
  see, what happens when we leave).
- **Leading or selling the engagement?** [The Delivery Standard](https://mckruz.github.io/intent-driven-development/GOLD-STANDARD.html) section 12
  (commercial) and section 1 (the shape), plus the [FAQ](https://mckruz.github.io/intent-driven-development/docs/faq.html) for client objections.
- **Migrating a team off Scrum?** The [FAQ](https://mckruz.github.io/intent-driven-development/docs/faq.html) ("Do we still run sprints?") and the
  [anti-pattern field guide](https://mckruz.github.io/intent-driven-development/docs/anti-patterns.html) (especially "cutting the safety net too
  early").

## Read it online

The standard is published at **https://mckruz.github.io/intent-driven-development/**

| Page                                                                                                       | What it covers                                                                       |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [The Delivery Standard](https://mckruz.github.io/intent-driven-development/GOLD-STANDARD.html)             | The master document — the whole method in 14 sections                                |
| [The Harbor Journey](https://mckruz.github.io/intent-driven-development/docs/journey.html)                 | The whole worked example as one continuous story — 10 stops, start to finish         |
| [The Team](https://mckruz.github.io/intent-driven-development/docs/team.html)                              | Old roles to new roles, the concrete job of each, scaling from one pod to many       |
| [Phase 0: Discovery](https://mckruz.github.io/intent-driven-development/docs/companion/phase-0.html)       | Fixing the problem · [worked example](https://mckruz.github.io/intent-driven-development/docs/companion/phase-0.html#example) |
| [Phase 1: Requirements](https://mckruz.github.io/intent-driven-development/docs/companion/phase-1.html) | The signed baseline · [worked example](https://mckruz.github.io/intent-driven-development/docs/companion/phase-1.html#example) |
| [Phase 2: Design](https://mckruz.github.io/intent-driven-development/docs/companion/phase-2.html)             | Options into signed decisions · [worked example](https://mckruz.github.io/intent-driven-development/docs/companion/phase-2.html#example) |
| [Phase 3: Foundation](https://mckruz.github.io/intent-driven-development/docs/companion/phase-3.html)     | The factory gets built · [worked example](https://mckruz.github.io/intent-driven-development/docs/companion/phase-3.html#example) |
| [The Build Loop](https://mckruz.github.io/intent-driven-development/docs/companion/build-loop.html)                  | The heart of the method · [worked example](https://mckruz.github.io/intent-driven-development/docs/companion/build-loop.html#example) |
| [The Rails](https://mckruz.github.io/intent-driven-development/docs/companion/the-rails.html)                        | The agentic CI/CD & DevOps pipeline — the gates every change rides · [worked example](https://mckruz.github.io/intent-driven-development/docs/companion/the-rails.html#example) |
| [Phase 7: Documentation](https://mckruz.github.io/intent-driven-development/docs/companion/phase-7.html) | Proving a stranger can run it · [worked example](https://mckruz.github.io/intent-driven-development/docs/companion/phase-7.html#example) |
| [Phase 8: Deployment](https://mckruz.github.io/intent-driven-development/docs/companion/phase-8.html)     | The rehearsal, the ceremony, go-live · [worked example](https://mckruz.github.io/intent-driven-development/docs/companion/phase-8.html#example) |
| [Phase 9: Monitoring](https://mckruz.github.io/intent-driven-development/docs/companion/phase-9.html)     | Alerts from real baselines, the drill, the retro · [worked example](https://mckruz.github.io/intent-driven-development/docs/companion/phase-9.html#example) |
| [Phase C: Close & Transfer](https://mckruz.github.io/intent-driven-development/docs/companion/phase-c.html)    | The close gate, the clean exit, the harvest · [worked example](https://mckruz.github.io/intent-driven-development/docs/companion/phase-c.html#example) |

### Reference & on-ramp

Plain-language pages for getting in the door fast. No engagement context required.

| Page                                                                                                | What it covers                                                                |
| --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| [The artifact flow](https://mckruz.github.io/intent-driven-development/docs/companion/artifact-flow.html) | What each phase receives and produces, where each file lives, and the handoff chain end to end |
| [Loop cheat-sheet](https://mckruz.github.io/intent-driven-development/docs/cheatsheet.html)         | The wall card — Intent → Delegate → Discern, the checking ladder, Do/Don't    |
| [Glossary](https://mckruz.github.io/intent-driven-development/docs/glossary.html)                   | Every term of art in the standard, defined in plain words                     |
| [FAQ](https://mckruz.github.io/intent-driven-development/docs/faq.html)                             | Honest answers to what clients and new pod members actually ask               |
| [Anti-pattern field guide](https://mckruz.github.io/intent-driven-development/docs/anti-patterns.html) | The nine ways this goes wrong — symptom, cause, fix, prevent                |

### The harness kit

The standard ships as a working **Claude Code harness** — the engagement starter that Phase 3
installs into a client repo (GOLD-STANDARD §6 *the harness standard*, §10 *the kit*). It's the
method made executable: a governance `CLAUDE.md`, the spec template, permission settings, blocking
Stop/review hooks, six model-tiered subagents, six team-practice skills, the five CI rails, profile
rubrics/rulesets, an eval module, and infra starters. Teams install it via the **`claude-code-sdlc`
plugin** (`/sdlc-setup`); `kit/` in this repo is the canonical source.

| Page                                                                                                    | What it covers                                                                          |
| ------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [The Kit — install & map](kit/README.md)                                                                | What's in the harness, where each file installs, the adapt order, and the shakedown drills |
| [Harness research](https://mckruz.github.io/intent-driven-development/docs/harness-kit/RESEARCH.html)    | The cited rationale behind every choice, plus the STABLE / NEWER / BLEEDING-EDGE maturity tiers |
| [Call map](https://mckruz.github.io/intent-driven-development/docs/harness-kit/CALL-MAP.html)            | How the pieces wire together — hooks, agents, and the five rails, visualized             |

## Repo layout

- **`GOLD-STANDARD.md`** — the master document (14 sections); `GOLD-STANDARD.html` is its render.
- **`index.html`** — the published landing page and site navigation.
- **`docs/`** — the deep-dive markdown sources of record (`phase-*`, `build-loop`, `the-rails`, and
  their `*-example` worked examples), the four plain-language reference pages (glossary, FAQ,
  cheat-sheet, anti-patterns — each with a paired HTML render), and `journey` / `team`.
- **`docs/companion/`** — the interactive per-phase walkthroughs. These are the published HTML pages
  the site links for each phase (the idea, the mechanics, and the worked example on one page).
- **`docs/harness-kit/`** — the harness research (`RESEARCH`) and call-map (`CALL-MAP`).
- **`kit/`** — the installable Claude Code harness; the source of truth (the `claude-code-sdlc`
  plugin bundles a synced copy).
- **`retros/`** — one file per engagement: what the harvest loop changed and why.
- **`PROGRESS.md`** — working notes for where the standard goes next.

> The site is served with `.nojekyll`, so only committed `.html` files render — the phase deep-dives
> exist as markdown sources, and their published form is the companion walkthrough. Link the
> companion pages (not `docs/<page>.html`) when pointing at a phase online.
