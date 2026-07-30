"""Tests for check_standard.py — the kit-vs-prose drift check.

A consistency check that cannot fail is worse than no check: it reports green forever and
everyone stops looking. So every test here injects a real drift and asserts the check catches
it, rather than asserting the current tree happens to be clean.

The checks read module-level paths, so each test repoints those at a synthetic repo built in
tmp_path. That keeps the tests honest about what each check actually reads.
"""

import json

import pytest

import check_standard as cs


# ── fixtures ──────────────────────────────────────────────────────────────────────────────────

RULESET_TEMPLATE = {
    "name": "main-branch-protection",
    "rules": [
        {"type": "deletion"},
        {
            "type": "required_status_checks",
            "parameters": {"required_status_checks": [{"context": "build-and-test"}]},
        },
    ],
}

GATE_COMMENT = "# <-- required status-check context (branch-protection.json)"


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A synthetic repo with the directory shape check_standard expects."""
    (tmp_path / "kit" / "workflows").mkdir(parents=True)
    (tmp_path / "kit" / "profile" / "rulesets").mkdir(parents=True)
    (tmp_path / "docs").mkdir()

    monkeypatch.setattr(cs, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(cs, "WORKFLOW_DIR", tmp_path / "kit" / "workflows")
    monkeypatch.setattr(cs, "RULESET", tmp_path / "kit" / "profile" / "rulesets" / "branch-protection.json")
    monkeypatch.setattr(cs, "STANDARD", tmp_path / "GOLD-STANDARD.md")
    return tmp_path


def write_ruleset(repo, contexts):
    ruleset = json.loads(json.dumps(RULESET_TEMPLATE))
    ruleset["rules"][1]["parameters"]["required_status_checks"] = [
        {"context": c} for c in contexts
    ]
    cs.RULESET.write_text(json.dumps(ruleset), encoding="utf-8")


def write_workflow(repo, filename, job_id, job_name, gate=False, body=""):
    comment = f"  {GATE_COMMENT}" if gate else ""
    cs.WORKFLOW_DIR.joinpath(filename).write_text(
        f"jobs:\n  {job_id}:\n    name: {job_name}{comment}\n{body}",
        encoding="utf-8",
    )


# ── check 1: rooted paths ─────────────────────────────────────────────────────────────────────


class TestRootedPaths:
    def test_a_missing_backticked_path_is_drift(self, repo):
        (repo / "GOLD-STANDARD.md").write_text("See `kit/nope.md` for detail.", encoding="utf-8")
        result = cs.check_rooted_paths()
        assert not result.ok
        assert "kit/nope.md" in result.failures[0]

    def test_an_existing_path_is_not_drift(self, repo):
        (repo / "kit" / "real.md").write_text("x", encoding="utf-8")
        (repo / "GOLD-STANDARD.md").write_text("See `kit/real.md`.", encoding="utf-8")
        assert cs.check_rooted_paths().ok

    def test_html_code_tags_are_checked_not_just_backticks(self, repo):
        """The HTML twins are hand-maintained and drift from their markdown — they must count.

        This is the surface most likely to rot, because nothing generates it.
        """
        (repo / "GOLD-STANDARD.html").write_text(
            "<p>See <code>kit/ghost.md</code>.</p>", encoding="utf-8"
        )
        result = cs.check_rooted_paths()
        assert not result.ok
        assert "kit/ghost.md" in result.failures[0]

    def test_a_dead_markdown_link_is_drift(self, repo):
        """A dead link on the published docs site is the same broken promise, seen by more people."""
        (repo / "GOLD-STANDARD.md").write_text("See [the team](docs/gone.md).", encoding="utf-8")
        result = cs.check_rooted_paths()
        assert not result.ok
        assert "docs/gone.md" in result.failures[0]

    def test_a_dead_href_is_drift(self, repo):
        (repo / "GOLD-STANDARD.html").write_text(
            '<a href="docs/gone.html">team</a>', encoding="utf-8"
        )
        assert not cs.check_rooted_paths().ok

    def test_a_live_link_resolves(self, repo):
        (repo / "docs" / "team.md").write_text("x", encoding="utf-8")
        (repo / "GOLD-STANDARD.md").write_text("See [the team](docs/team.md).", encoding="utf-8")
        assert cs.check_rooted_paths().ok

    def test_an_anchor_fragment_does_not_break_resolution(self, repo):
        """`docs/team.md#roles` points at a real file — the fragment is not part of the path."""
        (repo / "docs" / "team.md").write_text("x", encoding="utf-8")
        (repo / "GOLD-STANDARD.md").write_text("See [roles](docs/team.md#roles).", encoding="utf-8")
        assert cs.check_rooted_paths().ok

    def test_a_directory_reference_with_a_trailing_slash_resolves(self, repo):
        (repo / "kit" / "agents").mkdir()
        (repo / "GOLD-STANDARD.md").write_text("Agents live in `kit/agents/`.", encoding="utf-8")
        assert cs.check_rooted_paths().ok

    def test_allowlisted_paths_do_not_fail(self, repo, monkeypatch):
        monkeypatch.setitem(cs.ALLOWED_MISSING, "docs/later.md", "written with the first engagement")
        (repo / "GOLD-STANDARD.md").write_text("See `docs/later.md`.", encoding="utf-8")
        assert cs.check_rooted_paths().ok

    def test_planning_docs_are_not_held_to_the_current_tree(self, repo):
        """PROGRESS.md names work not yet done. Failing on that would make the check a nuisance."""
        (repo / "PROGRESS.md").write_text("Still to build: `docs/unbuilt.md`.", encoding="utf-8")
        assert cs.check_rooted_paths().ok

    def test_retros_are_not_scanned(self, repo):
        (repo / "retros").mkdir()
        (repo / "retros" / "r1.md").write_text("We deleted `kit/old.md`.", encoding="utf-8")
        assert cs.check_rooted_paths().ok

    def test_kit_files_may_reference_the_client_docs_directory(self, repo):
        """kit/** is written from the installed repo's point of view, where docs/ is theirs."""
        (repo / "kit" / "HARNESS.md").write_text("This page ships as `docs/harness.md`.", encoding="utf-8")
        assert cs.check_rooted_paths().ok

    def test_kit_files_are_still_held_to_kit_paths(self, repo):
        """The client-perspective exemption covers docs/ only — a kit/ path is unambiguous."""
        (repo / "kit" / "HARNESS.md").write_text("Templates in `kit/absent.md`.", encoding="utf-8")
        assert not cs.check_rooted_paths().ok

    def test_bare_filenames_are_ignored(self, repo):
        """Client-repo artifacts are named constantly and will never exist here."""
        (repo / "GOLD-STANDARD.md").write_text("The pod edits `epics.md` and `design-doc.md`.", encoding="utf-8")
        result = cs.check_rooted_paths()
        assert result.ok
        assert result.checked == 0

    def test_the_failure_names_the_file_and_line(self, repo):
        (repo / "GOLD-STANDARD.md").write_text("intro\n\nSee `kit/nope.md`.", encoding="utf-8")
        assert "GOLD-STANDARD.md:3" in cs.check_rooted_paths().failures[0]


# ── check 2: required contexts exist ──────────────────────────────────────────────────────────


class TestRequiredContextsExist:
    def test_a_required_check_no_job_produces_is_drift(self, repo):
        """The worst failure available: every PR waits forever on a check that never reports."""
        write_ruleset(repo, ["build-and-test", "phantom-gate"])
        write_workflow(repo, "ci.yml", "build", "build-and-test", gate=True)
        result = cs.check_required_contexts_exist()
        assert not result.ok
        assert "phantom-gate" in result.failures[0]
        assert "block forever" in result.failures[0]

    def test_contexts_backed_by_a_job_pass(self, repo):
        write_ruleset(repo, ["build-and-test"])
        write_workflow(repo, "ci.yml", "build", "build-and-test", gate=True)
        assert cs.check_required_contexts_exist().ok

    def test_a_job_in_any_workflow_file_counts(self, repo):
        write_ruleset(repo, ["build-and-test", "security-review"])
        write_workflow(repo, "ci.yml", "build", "build-and-test", gate=True)
        write_workflow(repo, "security.yml", "sec", "security-review", gate=True)
        assert cs.check_required_contexts_exist().ok

    def test_a_ruleset_requiring_nothing_fails_rather_than_passing_vacuously(self, repo):
        """Green-because-there-is-nothing-to-check is the worst possible report here.

        If branch protection stops requiring status checks, both context checks would have
        zero contexts to iterate and would pass — at the exact moment they should shout.
        """
        cs.RULESET.write_text(json.dumps({"rules": [{"type": "deletion"}]}), encoding="utf-8")
        write_workflow(repo, "ci.yml", "build", "build-and-test", gate=True)
        result = cs.check_required_contexts_exist()
        assert not result.ok
        assert "no required_status_checks rule" in result.failures[0]

    def test_the_reverse_check_also_refuses_an_empty_ruleset(self, repo):
        cs.RULESET.write_text(json.dumps({"rules": []}), encoding="utf-8")
        write_workflow(repo, "ci.yml", "build", "build-and-test", gate=True)
        assert not cs.check_gate_jobs_are_required().ok


# ── check 3: declared gates are required ──────────────────────────────────────────────────────


class TestGateJobsAreRequired:
    def test_a_gate_job_missing_from_the_ruleset_is_drift(self, repo):
        """A gate nobody requires is decoration — it reports, and a red run merges anyway."""
        write_ruleset(repo, ["build-and-test"])
        write_workflow(repo, "ci.yml", "build", "build-and-test", gate=True)
        write_workflow(repo, "extra.yml", "newgate", "new-gate", gate=True)
        result = cs.check_gate_jobs_are_required()
        assert not result.ok
        assert "new-gate" in result.failures[0]

    def test_an_unmarked_job_is_not_expected_to_be_required(self, repo):
        """deploy-dev and the eval suites are not merge gates and must not be dragged in."""
        write_ruleset(repo, ["build-and-test"])
        write_workflow(repo, "ci.yml", "build", "build-and-test", gate=True)
        write_workflow(repo, "deploy-dev.yml", "deploy", "deploy-dev", gate=False)
        assert cs.check_gate_jobs_are_required().ok

    def test_the_marker_tolerates_wording_variants(self, repo):
        """grader.yml says 'required-to-RUN status-check context' — still a declared gate.

        Matching the parenthesised file reference rather than the full phrase is deliberate: a
        check that depends on prose phrasing is the failure mode this script exists to prevent.
        """
        write_ruleset(repo, ["grader"])
        cs.WORKFLOW_DIR.joinpath("grader.yml").write_text(
            "jobs:\n  grade:\n    name: grader   "
            "# <-- required-to-RUN status-check context (branch-protection.json)\n",
            encoding="utf-8",
        )
        result = cs.check_gate_jobs_are_required()
        assert result.ok
        assert result.checked == 1, "the grader job must be recognised as a declared gate"


# ── check 4: model references ─────────────────────────────────────────────────────────────────


class TestModelReferences:
    def test_a_comment_that_disagrees_with_the_flag_is_drift(self, repo):
        """The exact drift that motivated this script."""
        cs.WORKFLOW_DIR.joinpath("grader.yml").write_text(
            "# <<MODEL>> Grader model (reference: sonnet).\njobs:\n  g:\n    name: grader\n"
            "        claude_args: |\n          --model opus\n",
            encoding="utf-8",
        )
        result = cs.check_model_references()
        assert not result.ok
        assert "sonnet" in result.failures[0] and "opus" in result.failures[0]

    def test_agreement_passes(self, repo):
        cs.WORKFLOW_DIR.joinpath("grader.yml").write_text(
            "# <<MODEL>> Grader model (reference: opus).\njobs:\n  g:\n    name: grader\n"
            "          --model opus\n",
            encoding="utf-8",
        )
        assert cs.check_model_references().ok

    def test_a_documented_model_that_is_never_invoked_is_drift(self, repo):
        cs.WORKFLOW_DIR.joinpath("grader.yml").write_text(
            "# <<MODEL>> Grader model (reference: opus).\njobs:\n  g:\n    name: grader\n",
            encoding="utf-8",
        )
        result = cs.check_model_references()
        assert not result.ok
        assert "never" in result.failures[0]

    def test_workflows_with_no_model_placeholder_are_skipped(self, repo):
        write_workflow(repo, "ci.yml", "build", "build-and-test")
        result = cs.check_model_references()
        assert result.ok
        assert result.checked == 0

    def test_all_invocations_in_one_file_must_agree(self, repo):
        """security.yml runs three reviewer passes; one drifting from the rest is still drift."""
        cs.WORKFLOW_DIR.joinpath("security.yml").write_text(
            "# <<MODEL>> Reviewer model (reference: opus).\njobs:\n  s:\n    name: security-review\n"
            "          --model opus\n          --model sonnet\n",
            encoding="utf-8",
        )
        assert not cs.check_model_references().ok


# ── check 5: the security repetition dial ─────────────────────────────────────────────────────


def _security_yml(assignment, reference):
    return (
        f"          # <<SECURITY_PASSES_HIGH>> — reference value {reference} (current behavior).\n"
        f"          PASSES_HIGH={assignment}\n"
    )


class TestSecurityDial:
    def test_all_three_sources_agreeing_passes(self, repo):
        cs.WORKFLOW_DIR.joinpath("security.yml").write_text(_security_yml(1, 1), encoding="utf-8")
        cs.STANDARD.write_text("a **dial, currently set to 1** (`SECURITY_PASSES_HIGH`)", encoding="utf-8")
        assert cs.check_security_dial().ok

    def test_the_standard_going_stale_is_drift(self, repo):
        """The standard tells the reader the dial is off — it must not be the one that rots."""
        cs.WORKFLOW_DIR.joinpath("security.yml").write_text(_security_yml(3, 3), encoding="utf-8")
        cs.STANDARD.write_text("a **dial, currently set to 1** (`SECURITY_PASSES_HIGH`)", encoding="utf-8")
        result = cs.check_security_dial()
        assert not result.ok
        assert "disagrees" in result.failures[-1]

    def test_the_code_drifting_from_its_own_comment_is_drift(self, repo):
        cs.WORKFLOW_DIR.joinpath("security.yml").write_text(_security_yml(3, 1), encoding="utf-8")
        cs.STANDARD.write_text("a **dial, currently set to 3** (`SECURITY_PASSES_HIGH`)", encoding="utf-8")
        assert not cs.check_security_dial().ok

    def test_an_unreadable_source_fails_rather_than_passing_silently(self, repo):
        """If the wording moved, the check cannot confirm agreement — it must not report green."""
        cs.WORKFLOW_DIR.joinpath("security.yml").write_text(_security_yml(1, 1), encoding="utf-8")
        cs.STANDARD.write_text("the repetition dial is currently off", encoding="utf-8")
        result = cs.check_security_dial()
        assert not result.ok
        assert "Could not read" in result.failures[0]


# ── the runner ────────────────────────────────────────────────────────────────────────────────


class TestRun:
    def test_the_real_repo_is_clean(self):
        """Guards the tree as it stands: this must pass on main, or the check is already ignored."""
        assert cs.run(quiet=True) == 0

    def test_run_returns_nonzero_when_a_check_fails(self, repo, monkeypatch):
        monkeypatch.setattr(
            cs, "CHECKS", (lambda: cs.Result("synthetic", 1, ["injected drift"]),)
        )
        assert cs.run(quiet=True) == 1

    def test_the_report_names_the_failing_check_and_the_drift(self, repo, monkeypatch, capsys):
        """A CI failure nobody can act on from the log is a failure people learn to ignore."""
        monkeypatch.setattr(
            cs, "CHECKS", (lambda: cs.Result("synthetic check", 1, ["injected drift"]),)
        )
        cs.run(quiet=False)
        captured = capsys.readouterr()
        assert "synthetic check" in captured.out, "the summary must list every check"
        assert "injected drift" in captured.err, "the detail must say what to fix"

    def test_a_clean_run_says_so(self, repo, monkeypatch, capsys):
        monkeypatch.setattr(cs, "CHECKS", (lambda: cs.Result("synthetic", 3),))
        assert cs.run(quiet=False) == 0
        assert "No drift." in capsys.readouterr().out

    def test_every_check_is_wired_into_the_runner(self):
        """A check that exists but is never called is the failure this whole script is about."""
        defined = {
            name
            for name in dir(cs)
            if name.startswith("check_") and callable(getattr(cs, name))
        }
        assert defined == {c.__name__ for c in cs.CHECKS}
