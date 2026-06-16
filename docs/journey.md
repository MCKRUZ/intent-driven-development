# The Harbor Mutual Engagement — start to finish

_The standard tells you how the method works. This is one engagement actually running it, from the
first workshop to the day we hand back the keys. Harbor Mutual is a fictional regional insurer
rebuilding its property-claims intake; the numbers, people, and decisions below are the worked
example that runs through every deep-dive. Read it straight through as a story, or jump to any stop._

Ten stops, in the order they happened. Each links to the full episode.

| | Stop | When | The gate it had to pass |
| --- | --- | --- | --- |
| 1 | [Phase 0 · Discovery](phase-0-example.md) | wk of 2026-03-02 | Problem framed, one metric set, PO decided |
| 2 | [Phase 1 · Requirements](phase-1-example.md) | wk of 2026-03-16 | The signed baseline |
| 3 | [Phase 2 · Design](phase-2-example.md) | wk of 2026-03-23 | Architecture and every ADR signed |
| 4 | [Phase 3 · Foundation](phase-3-example.md) | two weeks following | Walking skeleton live in client dev |
| 5 | [The Build Loop](build-loop-example.md) | 2026-04-13 → 07-10 | Every spec checked per change, not in a batch |
| 6 | [The Rails](the-rails-example.md) | across the middle | Agent proposes, gate disposes |
| 7 | [Phase 7 · Documentation](phase-7-example.md) | 2026-07-13 → 07-17 | A stranger can run it from the docs |
| 8 | [Phase 8 · Deployment](phase-8-example.md) | 2026-07-20 → 07-24 | Human go/no-go to production |
| 9 | [Phase 9 · Monitoring](phase-9-example.md) | 2026-07-27 → 08-07 | Alerts from real baselines; hypercare ends |
| 10 | [Phase C · Close & Transfer](phase-c-example.md) | 2026-08-10 → 08-28 | Harbor ran a real spec without us |

---

## 1 · Phase 0 — Discovery

**Week of 2026-03-02.** Karen Voss, VP of Claims Ops, owns the problem: a property-claims intake
that takes a median 11.4 days from first notice of loss to a coverage decision. The target is five.
The pod runs the outcome workshop, Claude interrogates the brief for unmade decisions, and Luis
Ortega is named product owner at six hours a week.

**The gate:** the problem is human-authored, the one success metric is set and has a source, and the
PO decision is made.
**The moment:** the workshop forces the choice nobody had made — committed PO or proxy mode — on day
one, before a line of code.

→ [Read the full episode](phase-0-example.md)

## 2 · Phase 1 — Requirements

**Week of 2026-03-16.** Epics, stories, and NFRs get drafted by Claude and owned by humans. The big
discovery: the core system "PolicyOne" only exposes a read-only nightly **snapshot replica** — which
quietly reshapes everything downstream.

**The gate:** a signed requirements baseline, every silent decision answered.
**The moment:** the replica constraint surfaces in requirements, not in production — exactly where
you want to find it.

→ [Read the full episode](phase-1-example.md)

## 3 · Phase 2 — Design

**Week of 2026-03-23, closed Friday the 27th.** Claude presents architectures with concrete
trade-offs; a human picks; every ADR is signed. Wes Carter, Harbor's lead engineer, co-signs the
decisions he'll have to live with.

**The gate:** architecture selected, every ADR signed.
**The moment:** the client's own engineer signs the design, not just the consultants — ownership
starts here.

→ [Read the full episode](phase-2-example.md)

## 4 · Phase 3 — Foundation

**The two weeks following.** The factory gets built: the kit is installed into Harbor's repo, the
rails go in, and the thinnest end-to-end slice — four sliced specs (0001–0004) — rides the full loop
into the client's dev environment. Spec 0002 (replica verify) is the HIGH-risk spec that proves the
security rails actually hold. Tom Reilly, Harbor's platform engineer, reviews the pipeline he'll
operate after we leave.

**The gate:** one real feature running in client dev, through the whole loop.
**The moment:** the walking skeleton deploys itself — the factory is real before any volume hits it.

→ [Read the full episode](phase-3-example.md)

## 5 · The Build Loop

**2026-04-13 to 07-10, feature-complete at spec 0044.** The middle of the engagement — no phases,
just the loop, one spec at a time. The worked week is the first week of May: spec 0015 (a fast-path
work queue, MEDIUM) and spec 0016 (duplicate-claim merge, HIGH). On 0016 the grader catches an
empty-policy-number bug that **eleven green tests missed** — a live bug, caught before merge — and
Wes gives the named HIGH-risk sign-off.

**The gate:** every change checked per change — mechanical gates, a grader that didn't write it, a
non-author human.
**The moment:** eleven passing tests, one real bug, and the grader is the thing that catches it.

→ [Read the full episode](build-loop-example.md)

## 6 · The Rails

**Across the middle, Build through Phase 9.** Not a phase — the pipeline every change rides, shown
through six episodes: the grader catch, a self-healing CI fix, a flaky test quarantined (not
"fixed"), the IaC funnel stopping a public storage account, a rollback that **fails in rehearsal**
and forces a fix, and configuration drift caught on a schedule.

**The gate:** agent proposes, gate disposes — every time.
**The moment:** the rollback failing in rehearsal is the win, not the failure — that's what
rehearsal is for.

→ [Read the full episode](the-rails-example.md)

## 7 · Phase 7 — Documentation

**2026-07-13 to 07-17.** Claude drafts the README, API docs, and RUNBOOK; humans verify them by
following them cold. Ines Roy — a Harbor engineer hired three weeks earlier — cold-verifies the
README and stalls at step four on a Key Vault permission, fixed the same day. Tom cold-walks the
RUNBOOK.

**The gate:** the docs are verified by use, not by reading.
**The moment:** the test of documentation is a new hire who's never seen the system getting it
running — and where she stalls is the bug.

→ [Read the full episode](phase-7-example.md)

## 8 · Phase 8 — Deployment

**Week of 2026-07-20, go-live Thursday the 23rd at 07:00.** The rehearsal on Tuesday fails — config
keys moved ahead of the release artifact — which becomes spec 0046 (configuration versioned with the
artifact); re-rehearsed clean on Wednesday. The go/no-go has seven named roles; Dan in security
holds until the secret-rotation record is attached. First real claim lands Thursday at 08:14: a
coverage recommendation in three hours and six minutes. Twenty-seven claims, day one.

**The gate:** a human go/no-go to production. Always.
**The moment:** a rehearsal that fails on Tuesday is why Thursday's go-live is boring.

→ [Read the full episode](phase-8-example.md)

## 9 · Phase 9 — Monitoring

**2026-07-27 to 08-07, inside hypercare.** Six alerts ship, each modeled from a real baseline rather
than a guess. A drill on the 5th catches a routing typo in one alert before it ever mattered. The
retro is honest: accepted-as-is at 84%, four escaped bugs total, the security-review queue running
slow at 2.1 days — which becomes a standing twice-weekly security slot.

**The gate:** alert thresholds confirmed against real baseline data; hypercare ends clean.
**The moment:** every escaped bug gets the same question — which check should have caught it? — and
the answer becomes a new check.

→ [Read the full episode](phase-9-example.md)

## 10 · Phase C — Close & Transfer

**2026-08-10 to 08-28.** The clean exit. Harbor's own engineers run specs as Orchestrators with our
Checkers, Wes becomes Harbor's Setup Owner with Tom as his deputy, and the close gate on the 20th is
the real test: spec 0049 (decommission the legacy fallback, HIGH risk) driven end-to-end by Ines,
with the hook correctly blocking a gated-path edit, Dan signing, and Harbor's own go/no-go promoting
it. We were not driving. Our access is revoked Wednesday the 26th. Final read: a completed-cohort
median of **4.2 days**, under the five-day target.

**The gate:** the client ran one real spec end-to-end — triage, spec, delegate, grade, merge, deploy
— without us.
**The moment:** the engagement ends not when the software ships, but when Harbor doesn't need us to
ship the next thing.

→ [Read the full episode](phase-c-example.md)

---

_New to the method behind the story? The [loop cheat-sheet](cheatsheet.md) is the 20-second version,
the [glossary](glossary.md) defines the terms, and [The Delivery Standard](../GOLD-STANDARD.md) is
the whole method._
