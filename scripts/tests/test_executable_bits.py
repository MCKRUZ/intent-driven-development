"""Every tracked shell script is committed executable.

Git stores the executable bit in the tree entry mode. Not in the filesystem, and **not** in
`.gitattributes` — there is no attribute for it (`git check-attr executable <file>` answers
"unspecified" for every file, always). The mode is the only place it lives.

That matters on Windows, where the filesystem has no executable bit: `git add` records a NEW
file as `100644`, and nothing local complains. The script then dies with `Permission denied`
the first time it runs on a Linux host — `install_harness.py` in the plugin warns about exactly
this — which is the worst possible place to discover it, because it is someone else's machine.

Not hypothetical. `kit/hooks/sensitive-edit-nudge.sh` arrived this way on 2026-07-31, and so did
its synced copy in the plugin. Both were fixed by hand. This test is what makes the next one
fail here instead of there.
"""

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
EXECUTABLE = "100755"


def tracked_shell_scripts() -> list[tuple[str, str]]:
    """(mode, path) for every tracked *.sh, or skip if this is not a git checkout."""
    proc = subprocess.run(
        ["git", "ls-files", "-s", "--", "*.sh"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        pytest.skip("not a git checkout; nothing to assert about committed modes")
    rows = []
    for line in proc.stdout.splitlines():
        meta, path = line.split("\t", 1)
        rows.append((meta.split()[0], path))
    return rows


def test_shell_scripts_are_committed_executable():
    scripts = tracked_shell_scripts()

    # A vacuous pass is the failure mode this whole file exists to prevent: if the pathspec or
    # the working directory is ever wrong, an empty list would report green forever.
    assert scripts, "no tracked *.sh found — the pathspec is wrong, not a clean bill of health"

    non_executable = [path for mode, path in scripts if mode != EXECUTABLE]
    assert not non_executable, (
        "committed non-executable; these die with 'Permission denied' once installed on a "
        "Linux host. Fix each with:\n"
        + "\n".join(f"  git update-index --chmod=+x {path}" for path in non_executable)
    )
