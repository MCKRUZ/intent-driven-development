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

- **Brand new to the method?** Read the [loop cheat-sheet](docs/cheatsheet.html) (20 seconds),
  then the [glossary](docs/glossary.html) for any word that trips you, then
  [The Delivery Standard](GOLD-STANDARD.html) itself.
- **Prefer a story to a spec?** Follow [The Harbor Journey](docs/journey.html) — one full
  engagement, start to finish, as a continuous worked example.
- **A pod member joining an engagement?** [The Delivery Standard](GOLD-STANDARD.html) front to
  back, then [The Team](docs/team.html) for your role, then the
  [build loop](docs/build-loop.html). Keep the [glossary](docs/glossary.html) and
  [anti-pattern field guide](docs/anti-patterns.html) open.
- **A client stakeholder or sponsor?** Read [In 30 seconds](#in-30-seconds) above, then the
  [FAQ](docs/faq.html) — it answers the questions you're about to ask (data, decisions, what you'll
  see, what happens when we leave).
- **Leading or selling the engagement?** [The Delivery Standard](GOLD-STANDARD.html) section 12
  (commercial) and section 1 (the shape), plus the [FAQ](docs/faq.html) for client objections.
- **Migrating a team off Scrum?** The [FAQ](docs/faq.html) ("Do we still run sprints?") and the
  [anti-pattern field guide](docs/anti-patterns.html) (especially "cutting the safety net too
  early").

## Read it online

The standard is published at **https://mckruz.github.io/intent-driven-development/**

| Page                                                                                                       | What it covers                                                                       |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [The Delivery Standard](https://mckruz.github.io/intent-driven-development/GOLD-STANDARD.html)             | The master document — the whole method in 14 sections                                |
| [The Harbor Journey](https://mckruz.github.io/intent-driven-development/docs/journey.html)                 | The whole worked example as one continuous story — 10 stops, start to finish         |
| [The Team](https://mckruz.github.io/intent-driven-development/docs/team.html)                              | Old roles to new roles, the concrete job of each, scaling from one pod to many       |
| [Phase 0: Discovery](https://mckruz.github.io/intent-driven-development/docs/phase-0-discovery.html)       | Fixing the problem · [worked example](https://mckruz.github.io/intent-driven-development/docs/phase-0-example.html) |
| [Phase 1: Requirements](https://mckruz.github.io/intent-driven-development/docs/phase-1-requirements.html) | The signed baseline · [worked example](https://mckruz.github.io/intent-driven-development/docs/phase-1-example.html) |
| [Phase 2: Design](https://mckruz.github.io/intent-driven-development/docs/phase-2-design.html)             | Options into signed decisions · [worked example](https://mckruz.github.io/intent-driven-development/docs/phase-2-example.html) |
| [Phase 3: Foundation](https://mckruz.github.io/intent-driven-development/docs/phase-3-foundation.html)     | The factory gets built · [worked example](https://mckruz.github.io/intent-driven-development/docs/phase-3-example.html) |
| [The Build Loop](https://mckruz.github.io/intent-driven-development/docs/build-loop.html)                  | The heart of the method · [worked example](https://mckruz.github.io/intent-driven-development/docs/build-loop-example.html) |
| [The Rails](https://mckruz.github.io/intent-driven-development/docs/the-rails.html)                        | The agentic CI/CD & DevOps pipeline — the gates every change rides · [worked example](https://mckruz.github.io/intent-driven-development/docs/the-rails-example.html) |
| [Phase 7: Documentation](https://mckruz.github.io/intent-driven-development/docs/phase-7-documentation.html) | Proving a stranger can run it · [worked example](https://mckruz.github.io/intent-driven-development/docs/phase-7-example.html) |
| [Phase 8: Deployment](https://mckruz.github.io/intent-driven-development/docs/phase-8-deployment.html)     | The rehearsal, the ceremony, go-live · [worked example](https://mckruz.github.io/intent-driven-development/docs/phase-8-example.html) |
| [Phase 9: Monitoring](https://mckruz.github.io/intent-driven-development/docs/phase-9-monitoring.html)     | Alerts from real baselines, the drill, the retro · [worked example](https://mckruz.github.io/intent-driven-development/docs/phase-9-example.html) |
| [Phase C: Close & Transfer](https://mckruz.github.io/intent-driven-development/docs/phase-c-close.html)    | The close gate, the clean exit, the harvest · [worked example](https://mckruz.github.io/intent-driven-development/docs/phase-c-example.html) |

### Reference & on-ramp

Plain-language pages for getting in the door fast. No engagement context required.

| Page                                                                                                | What it covers                                                                |
| --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| [Loop cheat-sheet](https://mckruz.github.io/intent-driven-development/docs/cheatsheet.html)         | The wall card — Intent → Delegate → Discern, the checking ladder, Do/Don't    |
| [Glossary](https://mckruz.github.io/intent-driven-development/docs/glossary.html)                   | Every term of art in the standard, defined in plain words                     |
| [FAQ](https://mckruz.github.io/intent-driven-development/docs/faq.html)                             | Honest answers to what clients and new pod members actually ask               |
| [Anti-pattern field guide](https://mckruz.github.io/intent-driven-development/docs/anti-patterns.html) | The nine ways this goes wrong — symptom, cause, fix, prevent                |

## Repo layout

Every page exists twice: a markdown source (the file of record) and a paired HTML render
(the published page). `GOLD-STANDARD.md` is the master document; `docs/` holds the
deep-dives, the four plain-language reference pages (glossary, FAQ, cheat-sheet, anti-patterns),
and the Harbor Mutual examples; `PROGRESS.md` is the working notes for where the standard goes
next.
