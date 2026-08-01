"""Tests for the fleet telemetry collector.

Same discipline as test_check_standard.py: inject real drift and assert it is caught. A
collector that has silently stopped noticing disarmed gates is worse than no collector — it
reports a clean fleet forever and everyone stops looking. These tests are what make its green
mean anything.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import collect_rails_telemetry as ct  # noqa: E402

SCHEMA = json.loads(
    (Path(__file__).resolve().parents[2] / "kit/profile/rails-telemetry.schema.json")
    .read_text(encoding="utf-8")
)


def report(**overrides) -> dict:
    """A well-formed, clean report. Tests mutate one thing so the failure is unambiguous."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    base = {
        "schema_version": 1,
        "repo": "acme/claims",
        "generated_at": now,
        "window": {"days": 7, "from": now, "to": now},
        "activity": {
            "gates": [{"context": "build-and-test", "runs": 3, "passed": 3, "failed": 0}],
            "pull_requests_merged": 4,
        },
        "overrides": {
            "labels": [{"label": "accepted-risk:correctness", "count": 0, "uses": []}],
            "ledgers": [{"path": ".github/eval-bypasses.md", "present": True,
                         "active_entries": 0, "expired_entries": 0}],
        },
        "enforcement": {
            "source": "live",
            "required_contexts": ["build-and-test"],
            "gate_jobs_present": ["build-and-test"],
            "findings": [],
        },
    }
    base.update(overrides)
    return base


def write(tmp_path: Path, name: str, data: dict | str) -> Path:
    repo = tmp_path / name
    (repo / ".github").mkdir(parents=True)
    path = repo / ".github" / "rails-telemetry.json"
    path.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")
    return repo


# --------------------------------------------------------------------------- the schema itself

def test_schema_matches_the_shape_the_workflows_emit():
    """The schema and the fixture must agree, or the schema documents a file nobody writes."""
    props = SCHEMA["properties"]
    assert set(SCHEMA["required"]) <= set(report())
    assert props["schema_version"]["const"] == ct.SCHEMA_VERSION
    for section in ("activity", "overrides", "enforcement"):
        assert set(props[section]["required"]) <= set(report()[section])


def test_every_finding_kind_the_collector_ranks_exists_in_the_schema():
    """A kind the workflows can emit but the schema does not name would be silently untyped."""
    kinds = set(SCHEMA["properties"]["enforcement"]["properties"]["findings"]
                ["items"]["properties"]["kind"]["enum"])
    assert "gate_not_required" in kinds          # the disarmed case
    assert "telemetry_incomplete" in kinds       # the collector appends this one itself
    assert set(SCHEMA["properties"]["enforcement"]["properties"]["source"]["enum"]) == {
        "live", "committed", "unavailable"}


# --------------------------------------------------------------------------- reading

def test_clean_repo_reports_clean(tmp_path):
    repo = write(tmp_path, "clean", report())
    assert ct.main([str(repo)]) == 0


def test_disarmed_gate_is_high_and_fails_the_run(tmp_path):
    """THE case this whole mechanism exists for: the gate runs, reports, and enforces nothing."""
    data = report()
    data["enforcement"]["required_contexts"] = []          # nobody requires it any more
    data["enforcement"]["findings"] = [{
        "kind": "gate_not_required", "severity": "high", "context": "build-and-test",
        "detail": "declares itself required; branch protection does not require it",
    }]
    repo = write(tmp_path, "disarmed", data)

    rep = ct.load(str(repo))
    assert rep.high_findings
    assert ct.main([str(repo)]) == 1


def test_missing_report_is_unknown_not_clean(tmp_path):
    """Silence must never be read as health — the whole point of the coverage line."""
    empty = tmp_path / "silent"
    empty.mkdir()
    rep = ct.load(str(empty))
    assert rep.error is not None
    assert ct.main([str(empty)]) == 1


def test_unknown_schema_version_is_refused_not_guessed(tmp_path):
    """A v2 file read with v1 assumptions yields numbers that look fine and mean something else."""
    repo = write(tmp_path, "future", report(schema_version=2))
    rep = ct.load(str(repo))
    assert rep.error is not None and "schema_version" in rep.error
    assert not rep.findings


def test_malformed_json_does_not_abort_the_fleet(tmp_path):
    """One broken file must not hide the other repos — usually it is the interesting one."""
    bad = write(tmp_path, "broken", "{not json")
    good = write(tmp_path, "fine", report(repo="acme/other"))
    reports = ct.collect([str(bad), str(good)])
    assert len(reports) == 2
    assert any(r.error for r in reports)
    assert any(r.repo == "acme/other" for r in reports)


def test_stale_report_is_flagged(tmp_path):
    old = (datetime.now(timezone.utc) - timedelta(days=ct.STALE_AFTER_DAYS + 5))
    repo = write(tmp_path, "stale", report(generated_at=old.strftime("%Y-%m-%dT%H:%M:%SZ")))
    rep = ct.load(str(repo))
    assert any(f["kind"] == "telemetry_incomplete" for f in rep.findings)


def test_committed_enforcement_source_is_surfaced(tmp_path):
    """Intent read from a file is not proof of what the platform enforces; say which it was."""
    data = report()
    data["enforcement"]["source"] = "committed"
    repo = write(tmp_path, "intent", data)
    assert ct.load(str(repo)).enforcement_source == "committed"


# --------------------------------------------------------------------------- fleet behaviour

def test_worst_repo_sorts_first(tmp_path):
    clean = write(tmp_path, "a-clean", report(repo="acme/a"))
    data = report(repo="acme/z")
    data["enforcement"]["findings"] = [
        {"kind": "gate_not_required", "severity": "high", "context": "grader", "detail": "x"}]
    bad = write(tmp_path, "z-bad", data)

    ordered = ct.collect([str(clean), str(bad)])
    # Unreadable first, then by severity — a fleet view is read from the top.
    assert ordered[0].repo == "acme/z"


def test_empty_root_is_distinguished_from_a_missing_argument(tmp_path, capsys):
    """A root with no reports is a FINDING, not a usage error — and must not exit 0."""
    (tmp_path / "some-repo").mkdir()
    assert ct.main(["--root", str(tmp_path)]) == 1
    assert "not clean" in capsys.readouterr().err


def test_discover_finds_repos_not_merely_reports(tmp_path):
    """A repo that never ran the workflow must still appear — absent is the finding."""
    for name in ("one", "two"):
        write(tmp_path, name, report(repo=f"acme/{name}"))
        (tmp_path / name / ".git").mkdir()
    silent = tmp_path / "never-ran"          # a real repo, no report
    (silent / ".git").mkdir(parents=True)
    (tmp_path / "not-a-repo").mkdir()        # not a repo at all — correctly ignored

    found = ct.discover(str(tmp_path))
    assert len(found) == 3
    assert any("never-ran" in f for f in found)

    reports = ct.collect(found)
    assert any(r.error and "never-ran" in str(r.source) for r in reports)


def test_silent_repo_makes_the_fleet_view_fail(tmp_path):
    """The whole promise: silence is reported as unknown and exits non-zero."""
    write(tmp_path, "good", report())
    (tmp_path / "good" / ".git").mkdir()
    (tmp_path / "silent" / ".git").mkdir(parents=True)
    assert ct.main(["--root", str(tmp_path)]) == 1


def test_overrides_are_totalled_across_labels(tmp_path):
    data = report()
    data["overrides"]["labels"] = [
        {"label": "accepted-risk:correctness", "count": 2, "uses": []},
        {"label": "gate-exception", "count": 1, "uses": []},
    ]
    repo = write(tmp_path, "overridden", data)
    assert ct.load(str(repo)).overrides == 3


def test_render_names_the_disarmed_repo(tmp_path):
    data = report(repo="acme/quiet")
    data["enforcement"]["findings"] = [
        {"kind": "gate_not_required", "severity": "high", "context": "security-review",
         "detail": "not required"}]
    repo = write(tmp_path, "quiet", data)
    out = ct.render(ct.collect([str(repo)]))
    assert "acme/quiet" in out and "gate_not_required" in out and "security-review" in out


def test_report_file_path_accepted_directly(tmp_path):
    repo = write(tmp_path, "direct", report())
    assert ct.load(str(repo / ".github" / "rails-telemetry.json")).error is None


@pytest.mark.parametrize("severity,expected_exit", [("high", 1), ("medium", 0), ("low", 0)])
def test_only_high_findings_fail_the_run(tmp_path, severity, expected_exit):
    """Medium and low are for reading, not for stopping a person's morning."""
    data = report()
    data["enforcement"]["findings"] = [
        {"kind": "required_context_never_reported", "severity": severity,
         "context": "grader", "detail": "quiet"}]
    repo = write(tmp_path, f"sev-{severity}", data)
    assert ct.main([str(repo)]) == expected_exit
