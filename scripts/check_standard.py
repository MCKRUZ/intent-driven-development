#!/usr/bin/env python3
"""Fail when the written standard and the kit it describes disagree.

`sync_kit.py --check` (in claude-code-sdlc) keeps the kit honest against the plugin's generated
harness. Nothing kept it honest against the prose that *describes* the kit — which is how
GOLD-STANDARD section 14 came to state a model policy the shipped workflows had already moved
past. It was found by accident. This script is the mechanism that would have found it.

Deliberately narrow. Only mechanical claims are checked: paths, status-check contexts, and two
literal reference values. Claims about judgement, roles, or intent are not automatable and are
not attempted — they belong to the setup review.

    python scripts/check_standard.py          # human-readable report; exit 1 on any drift
    python scripts/check_standard.py --quiet   # only failures
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

RULESET = REPO_ROOT / "kit" / "profile" / "rulesets" / "branch-protection.json"
WORKFLOW_DIR = REPO_ROOT / "kit" / "workflows"
STANDARD = REPO_ROOT / "GOLD-STANDARD.md"

# Planning and historical records. They legitimately name things that do not exist yet or no
# longer do; holding them to the current state of the tree would make the check a nuisance and
# nuisance checks get switched off.
UNSCANNED = {"PROGRESS.md", "PLUGIN-SYNC.md"}
UNSCANNED_DIRS = {".git", "retros", "node_modules"}

# A path may be missing ONLY with a reason recorded here. That is the point of the allowlist:
# it turns "this file does not exist" from an accident into a decision someone signed.
ALLOWED_MISSING = {
    "docs/agentic-spec-example.md": (
        "Deliberate forward reference. GOLD-STANDARD section 11 marks it 'to be added with the "
        "first agentic engagement' — the example needs a real engagement to be written from."
    ),
    "docs/harness.md": (
        "Path in the INSTALLED client repo, not this one. kit/HARNESS.md is delivered to the "
        "client as docs/harness.md; the reference is correct from the client's side."
    ),
}

# Paths rooted at a directory that exists in THIS repo, in either notation: markdown backticks
# or the <code> tags the hand-maintained HTML twins use. Covering both matters more than it
# looks — the twins are written by hand and drift from their markdown, so checking only
# backticks would leave exactly the rot-prone half of the surface unchecked.
#
# Bare filenames are deliberately NOT checked: the docs are full of client-repo artifacts
# (epics.md, design-doc.md, check_gates.py) that will never exist here, and matching them
# produced ~540 false positives against ~280 true ones.
# Four notations, all of them claims that a file is there: markdown code spans, the <code> tags
# the HTML twins use, markdown link targets, and hrefs. Links matter as much as code spans —
# a dead link on a published docs site is the same broken promise, seen by more people.
_ROOTED = r"(?:kit|docs)/[A-Za-z0-9_./-]+"
ROOTED_PATH = re.compile(
    rf"`({_ROOTED})`"
    rf"|<code>({_ROOTED})</code>"
    rf"|\]\(({_ROOTED})[^)]*\)"
    rf"|href=\"({_ROOTED})[^\"]*\""
)

# Job name lines in the kit workflows carry a marker comment when they are a merge gate. The
# marker is matched on the parenthesised file reference rather than the whole phrase, because
# the wording varies ("required status-check context", "required-to-RUN status-check context")
# and a check that depends on prose phrasing is the thing this script exists to prevent.
JOB_NAME = re.compile(r"^\s{4}name:\s*(\S+)\s*(#.*)?$", re.MULTILINE)
GATE_MARKER = "status-check context (branch-protection.json)"

MODEL_REFERENCE = re.compile(r"<<MODEL>>.*?\(reference:\s*([A-Za-z0-9.-]+)\)")
MODEL_FLAG = re.compile(r"^\s*--model\s+([A-Za-z0-9.-]+)\s*$", re.MULTILINE)

PASSES_ASSIGNMENT = re.compile(r"^\s*PASSES_HIGH=(\d+)\s*$", re.MULTILINE)
PASSES_REFERENCE = re.compile(r"<<SECURITY_PASSES_HIGH>>\s*—\s*reference value\s*(\d+)")
PASSES_PROSE = re.compile(r"dial, currently set to (\d+)\*\*")


@dataclass
class Result:
    """One check's outcome. `failures` are drifts; `checked` is what the check actually covered."""

    name: str
    checked: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def scannable_files() -> list[Path]:
    """Every prose file whose claims describe the current state of this repo."""
    out: list[Path] = []
    for pattern in ("*.md", "*.html"):
        for path in REPO_ROOT.rglob(pattern):
            if UNSCANNED_DIRS & set(path.relative_to(REPO_ROOT).parts):
                continue
            if path.name in UNSCANNED:
                continue
            out.append(path)
    return sorted(out)


def check_rooted_paths() -> Result:
    """Every backticked kit/… or docs/… path in the prose resolves to a real file or directory."""
    result = Result("rooted paths resolve")
    for path in scannable_files():
        # kit/** is written from the installed client repo's point of view, where `docs/…`
        # means THEIR docs directory. Only the kit/ prefix is unambiguous there.
        in_kit = path.is_relative_to(REPO_ROOT / "kit")
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(text.splitlines(), start=1):
            for groups in ROOTED_PATH.findall(line):
                token = next(g for g in groups if g)
                target = token.split("#")[0].rstrip("/")  # drop any anchor fragment
                if in_kit and target.startswith("docs/"):
                    continue
                result.checked += 1
                if (REPO_ROOT / target).exists() or target in ALLOWED_MISSING:
                    continue
                rel = path.relative_to(REPO_ROOT).as_posix()
                result.failures.append(
                    f"{rel}:{line_no} references `{token}`, which does not exist. "
                    f"Create it, fix the reference, or record it in ALLOWED_MISSING with a reason."
                )
    return result


def _workflow_job_names() -> dict[str, list[tuple[str, bool]]]:
    """Job `name:` values per workflow file, each flagged as a declared merge gate or not."""
    jobs: dict[str, list[tuple[str, bool]]] = {}
    for wf in sorted(WORKFLOW_DIR.glob("*.yml")):
        text = wf.read_text(encoding="utf-8", errors="replace")
        found = [
            (name, GATE_MARKER in (comment or ""))
            for name, comment in JOB_NAME.findall(text)
        ]
        if found:
            jobs[wf.name] = found
    return jobs


def _required_contexts() -> list[str]:
    """The required status-check contexts, or raise.

    Raising rather than returning [] is deliberate. An empty list would make both
    context checks pass vacuously — reporting green precisely when branch protection had
    stopped requiring anything, which is the moment they most need to speak up.
    """
    ruleset = json.loads(RULESET.read_text(encoding="utf-8"))
    for rule in ruleset.get("rules", []):
        if rule.get("type") == "required_status_checks":
            checks = rule["parameters"]["required_status_checks"]
            return [c["context"] for c in checks]
    raise LookupError(
        f"{RULESET.relative_to(REPO_ROOT).as_posix()} has no required_status_checks rule. "
        f"Either branch protection stopped requiring checks, or the ruleset shape changed."
    )


def check_required_contexts_exist() -> Result:
    """Every required status check is produced by a job that actually exists.

    A required context nothing emits is the worst failure mode available here: every PR waits
    forever on a check that will never report, and the fix is invisible from the PR page.
    """
    result = Result("required checks are produced by a real job")
    produced = {name for jobs in _workflow_job_names().values() for name, _ in jobs}
    try:
        contexts = _required_contexts()
    except LookupError as exc:
        result.failures.append(str(exc))
        return result
    for context in contexts:
        result.checked += 1
        if context not in produced:
            result.failures.append(
                f"branch-protection.json requires the status check '{context}', but no job in "
                f"kit/workflows/*.yml is named '{context}'. Every PR would block forever."
            )
    return result


def check_gate_jobs_are_required() -> Result:
    """Every job that calls itself a merge gate is actually required by the ruleset.

    The reverse of the check above, and the likelier drift: adding a gate job to ci.yml is the
    memorable half, wiring it into branch protection is the half people forget. A gate nobody
    requires is decoration — it reports, and a red run merges anyway.
    """
    result = Result("declared gate jobs are required by the ruleset")
    try:
        required = set(_required_contexts())
    except LookupError as exc:
        result.failures.append(str(exc))
        return result
    for wf_name, jobs in _workflow_job_names().items():
        for name, is_declared_gate in jobs:
            if not is_declared_gate:
                continue
            result.checked += 1
            if name not in required:
                result.failures.append(
                    f"kit/workflows/{wf_name} declares job '{name}' a required status-check "
                    f"context, but branch-protection.json does not require it. It would run "
                    f"and report, and a red run would merge anyway."
                )
    return result


def check_model_references() -> Result:
    """Each workflow's documented reference model matches the model it actually invokes.

    This is the exact drift that motivated the script: the comment said one thing, the
    `--model` flag another, and the standard quoted the comment.
    """
    result = Result("workflow model comments match the invoked model")
    for wf in sorted(WORKFLOW_DIR.glob("*.yml")):
        text = wf.read_text(encoding="utf-8", errors="replace")
        reference = MODEL_REFERENCE.search(text)
        if not reference:
            continue
        expected = reference.group(1)
        invoked = set(MODEL_FLAG.findall(text))
        result.checked += 1
        if not invoked:
            result.failures.append(
                f"kit/workflows/{wf.name} documents a reference model '{expected}' but never "
                f"passes --model. The comment describes behaviour the file does not have."
            )
        elif invoked != {expected}:
            result.failures.append(
                f"kit/workflows/{wf.name} documents reference model '{expected}' but invokes "
                f"{sorted(invoked)}. The comment and the workflow disagree."
            )
    return result


def check_security_dial() -> Result:
    """The security repetition dial reads the same in the code, its comment, and the standard.

    Three places state this number and all three are load-bearing: the standard tells the
    reader the dial is off, so the standard must not be the one that goes stale.
    """
    result = Result("security repetition dial agrees across code, comment, and standard")
    security = (WORKFLOW_DIR / "security.yml").read_text(encoding="utf-8", errors="replace")
    standard = STANDARD.read_text(encoding="utf-8", errors="replace")

    readings = {
        "kit/workflows/security.yml (PASSES_HIGH=)": PASSES_ASSIGNMENT.search(security),
        "kit/workflows/security.yml (reference comment)": PASSES_REFERENCE.search(security),
        "GOLD-STANDARD.md ('dial, currently set to N')": PASSES_PROSE.search(standard),
    }
    values: dict[str, str] = {}
    for where, match in readings.items():
        result.checked += 1
        if match is None:
            result.failures.append(
                f"Could not read the repetition dial from {where}. Either the value moved or "
                f"the wording changed — this check cannot confirm the three agree."
            )
        else:
            values[where] = match.group(1)

    if len(set(values.values())) > 1:
        detail = ", ".join(f"{w} = {v}" for w, v in values.items())
        result.failures.append(f"The repetition dial disagrees between sources: {detail}.")
    return result


CHECKS = (
    check_rooted_paths,
    check_required_contexts_exist,
    check_gate_jobs_are_required,
    check_model_references,
    check_security_dial,
)


def run(quiet: bool = False) -> int:
    results = [check() for check in CHECKS]
    failed = [r for r in results if not r.ok]

    if not quiet:
        print("Standard-vs-kit consistency\n")
        for r in results:
            mark = "ok  " if r.ok else "FAIL"
            print(f"  [{mark}] {r.name} ({r.checked} checked)")
        print()

    sys.stdout.flush()  # keep the summary above the failures in CI logs
    for r in failed:
        print(f"FAIL: {r.name}", file=sys.stderr)
        for failure in r.failures:
            print(f"  - {failure}", file=sys.stderr)
        print(file=sys.stderr)

    if failed:
        total = sum(len(r.failures) for r in failed)
        print(
            f"{total} drift(s) between the standard and the kit it describes.",
            file=sys.stderr,
        )
        return 1

    if not quiet:
        print("No drift.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--quiet", action="store_true", help="print failures only")
    args = parser.parse_args()
    return run(quiet=args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
