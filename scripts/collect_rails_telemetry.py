#!/usr/bin/env python3
"""Read every repo's committed rails-telemetry.json and report the fleet.

Overrides and gate outcomes were already recorded per repo. Nothing aggregated them, so across
a portfolio nobody could answer three questions: are the gates firing, are they being routinely
waved through, and has one been quietly switched off.

The third is the one that needs a tool. A gate has two halves — the check, and the rule that
requires it to pass. Delete the rule and the check still runs, still reports, and looks entirely
normal; a red run just merges anyway. From outside that repo, a disarmed gate and a gate that
never caught anything produce identical evidence. `check_standard.py` catches this in OUR repo;
nothing caught it in a client's, which is what the telemetry file and this script exist for.

This is OPERATOR TOOLING and is deliberately NOT part of `kit/` — it is never installed into a
client repo. It reads what the installed `rails-telemetry` workflow committed.

    python scripts/collect_rails_telemetry.py <path-or-repo> [...]   # report; exit 1 on a high finding
    python scripts/collect_rails_telemetry.py --root ../clients      # every repo under a directory
    python scripts/collect_rails_telemetry.py --root ../clients --json

Accepts a repo root (the file is found at .github/rails-telemetry.json) or the JSON file itself.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1
REPORT_REL = Path(".github") / "rails-telemetry.json"

# Ranked worst-first. `gate_not_required` leads because it is the failure the whole pipeline of
# work exists to surface: the repo looks green precisely because nothing is being enforced.
SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# A report older than this is describing a week nobody has looked at since. Not an error — repos
# go quiet legitimately — but reporting it as current would be the same lie the telemetry exists
# to prevent.
STALE_AFTER_DAYS = 21


@dataclass
class RepoReport:
    """One repo's telemetry, or the reason it could not be read."""

    source: Path
    repo: str = "?"
    findings: list[dict] = field(default_factory=list)
    overrides: int = 0
    merged: int = 0
    gates: int = 0
    enforcement_source: str = "unavailable"
    generated_at: str | None = None
    error: str | None = None

    @property
    def worst(self) -> int:
        return min((SEVERITY_ORDER.get(f.get("severity", "low"), 2) for f in self.findings),
                   default=3)

    @property
    def high_findings(self) -> list[dict]:
        return [f for f in self.findings if f.get("severity") == "high"]


def _resolve(target: str) -> Path:
    """A repo root, or the report file itself. Both are natural things to type."""
    p = Path(target)
    return p if p.is_file() else p / REPORT_REL


def load(target: str) -> RepoReport:
    """Parse one report. An unreadable report is a RESULT, never an exception.

    A collector that dies on the first malformed file tells you nothing about the other
    forty repos, and the one that failed is usually the one worth looking at.
    """
    path = _resolve(target)
    rep = RepoReport(source=path)

    if not path.is_file():
        rep.error = "no rails-telemetry.json — the workflow is not installed, has never run, or is disabled"
        return rep
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        rep.error = f"unreadable: {exc}"
        return rep
    if not isinstance(data, dict):
        rep.error = "not a JSON object"
        return rep

    version = data.get("schema_version")
    if version != SCHEMA_VERSION:
        # Refuse rather than guess. Reading a v2 file with v1 assumptions would produce numbers
        # that look fine and mean something else, which is worse than an obvious gap.
        rep.error = f"schema_version {version!r}, expected {SCHEMA_VERSION} — not read"
        return rep

    rep.repo = data.get("repo", "?")
    rep.generated_at = data.get("generated_at")
    enforcement = data.get("enforcement") or {}
    rep.enforcement_source = enforcement.get("source", "unavailable")
    rep.findings = list(enforcement.get("findings") or [])

    activity = data.get("activity") or {}
    rep.gates = len(activity.get("gates") or [])
    rep.merged = activity.get("pull_requests_merged", 0)

    overrides = data.get("overrides") or {}
    rep.overrides = sum(entry.get("count", 0) for entry in (overrides.get("labels") or []))

    if (stale := _staleness_days(rep.generated_at)) is not None and stale > STALE_AFTER_DAYS:
        rep.findings.append({
            "kind": "telemetry_incomplete",
            "severity": "medium",
            "detail": f"last report is {stale} days old — this repo's gate status is not being watched",
        })
    return rep


def _staleness_days(generated_at: str | None) -> int | None:
    if not generated_at:
        return None
    try:
        when = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
    except ValueError:
        return None
    return (datetime.now(timezone.utc) - when).days


def collect(targets: list[str]) -> list[RepoReport]:
    """Worst first — the point of a fleet view is that you read the top and stop."""
    return sorted((load(t) for t in targets),
                  key=lambda r: (0 if r.error else 1, r.worst, r.repo))


def discover(root: str) -> list[str]:
    """Every git repo directly under `root`, reporting or not.

    Deliberately keyed on `.git` rather than on the report file. Discovering by report would
    only ever find repos that are ALREADY reporting, so a repo where the workflow was never
    installed — or was installed and has never run — would be silently absent from the fleet
    view. That is precisely the failure this tool exists to prevent, reproduced one level up:
    a clean-looking report whose cleanliness comes from not having looked.

    Sorted so output is stable run to run.
    """
    return sorted(str(p.parent) for p in Path(root).glob("*/.git"))


def render(reports: list[RepoReport]) -> str:
    if not reports:
        return "No repos given. Pass repo paths, or --root <dir> to scan for them."

    lines: list[str] = ["Rails telemetry — fleet view", ""]

    unreadable = [r for r in reports if r.error]
    disarmed = [r for r in reports if not r.error and r.high_findings]

    # The headline is a claim about coverage, and it is deliberately careful: a repo we could
    # not read is UNKNOWN, not healthy. Folding those into "clean" is how a fleet report starts
    # lying by omission.
    lines.append(
        f"  {len(reports)} repo(s): {len(disarmed)} with high-severity findings, "
        f"{len(unreadable)} not reporting, "
        f"{len(reports) - len(disarmed) - len(unreadable)} clean"
    )
    lines.append("")

    for rep in reports:
        if rep.error:
            lines.append(f"  [NOT REPORTING] {rep.source.parent.parent.name or rep.source}")
            lines.append(f"      {rep.error}")
            lines.append("")
            continue

        mark = "HIGH" if rep.high_findings else ("...." if not rep.findings else "note")
        lines.append(f"  [{mark}] {rep.repo}")
        detail = (f"      gates seen {rep.gates} · merged PRs {rep.merged} · "
                  f"overrides {rep.overrides} · enforcement read from {rep.enforcement_source}")
        lines.append(detail)
        for finding in sorted(rep.findings,
                              key=lambda f: SEVERITY_ORDER.get(f.get("severity", "low"), 2)):
            ctx = finding.get("context")
            head = f"      - [{finding.get('severity')}] {finding.get('kind')}"
            lines.append(f"{head} ({ctx})" if ctx else head)
            lines.append(f"          {finding.get('detail', '')}")
        lines.append("")

    if disarmed or unreadable:
        lines.append("  A gate that is present but not required reports normally and blocks nothing.")
        lines.append("  A repo that is not reporting is UNKNOWN, not clean.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("targets", nargs="*", help="repo roots, or rails-telemetry.json paths")
    parser.add_argument("--root", help="scan this directory for repos that have a report")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    targets = list(args.targets)
    if args.root:
        found = discover(args.root)
        if not found and not targets:
            # Deliberately distinct from the no-arguments error. "Nothing there" and "you
            # forgot the flag" have different fixes, and sending someone to re-type a flag
            # they already typed is how a tool gets a reputation for being broken.
            print(f"No rails-telemetry.json found under {args.root!r}.\n"
                  f"Expected each repo at <root>/<repo>/{REPORT_REL.as_posix()}.\n"
                  f"Either the workflow is not installed in those repos, or it has not run yet — "
                  f"which is itself worth knowing: an unreported repo is unknown, not clean.",
                  file=sys.stderr)
            return 1
        targets.extend(found)
    if not targets:
        parser.error("give at least one repo path, or --root <dir>")

    reports = collect(targets)

    if args.json:
        print(json.dumps([{
            "repo": r.repo, "source": str(r.source), "error": r.error,
            "enforcement_source": r.enforcement_source,
            "overrides": r.overrides, "merged": r.merged,
            "findings": r.findings,
        } for r in reports], indent=2))
    else:
        print(render(reports))

    # Non-zero when something needs a person: a high finding, or a repo we could not read.
    # "Could not read" counts deliberately — silence is not the same as clean, and a collector
    # that exits 0 on a fleet it failed to inspect is a green light nobody earned.
    return 1 if any(r.error or r.high_findings for r in reports) else 0


if __name__ == "__main__":
    sys.exit(main())
