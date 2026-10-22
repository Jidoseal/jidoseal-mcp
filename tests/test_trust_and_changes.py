"""
The two free trust tools: `jidoseal_trust` (stale / unverified / ok for a document) and
`jidoseal_changes` (what an edit changed, and which verified documents it left unconfirmed),
plus the "which 0.2?" rules in okf_trust.py that the State of OKF report also uses.
"""
from __future__ import annotations

import datetime
import os
import shutil
import subprocess

import pytest

import okf_trust
from conftest import call_tool

NOW = datetime.datetime(2026, 10, 21, 12, 0, tzinfo=datetime.timezone.utc)

VERIFIED = """---
type: Policy
title: Leave
stale_after: 2027-01-01T00:00:00Z
generated: { by: agent:writer, at: 2026-06-01T00:00:00Z }
verified: { by: human:ahormati, at: 2026-06-25T09:00:00Z }
---
Staff get 25 days.
"""


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


# --- "which 0.2?" -----------------------------------------------------------------------------
@pytest.mark.parametrize("key,value,fits", [
    ("stale_after", "2026-12-31", "2026-08-15"),
    ("stale_after", "2026-12-31T00:00:00Z", "2026-08-21"),
    ("stale_after", "2026-12-31T00:00:00+02:00", "2026-08-21"),
    ("stale_after", "2026-12-31T00:00:00", "neither"),
    ("sources[].last_modified", "2026-05-30", "2026-08-15"),
    ("usage_window.from", "2026-06-01T00:00:00Z", "2026-08-21"),
    ("generated.at", "2026-06-20T22:53:05Z", "both"),
    ("generated.at", "2026-06-20T22:53:05", "2026-08-15"),
    ("generated.at", "2026-06-20", "neither"),
    ("generated.at", "2026-06-30 14:00:00+00:00", "neither"),
    ("verified[].at", "yesterday", "neither"),
])
def test_timestamp_fit(key, value, fits):
    assert okf_trust.timestamp_fit(key, value) == fits


def test_unquoted_dates_stay_as_written():
    fm, problem, _ = okf_trust.parse_frontmatter(
        "---\ntype: X\nstale_after: 2026-12-31\ngenerated: {by: a, at: 2026-06-20T22:53:05Z}\n---\n")
    assert problem is None
    assert fm["stale_after"] == "2026-12-31"
    assert fm["generated"]["at"] == "2026-06-20T22:53:05Z"


@pytest.mark.parametrize("fits,answer", [
    ([], "no-timestamps"), (["both"], "both"), (["both", "2026-08-21"], "2026-08-21"),
    (["both", "2026-08-15"], "2026-08-15"), (["2026-08-15", "2026-08-21"], "mixed"),
    (["2026-08-21", "neither"], "neither"),
])
def test_which_text(fits, answer):
    assert okf_trust.which_text(fits) == answer


# --- trust ------------------------------------------------------------------------------------
def test_verified_and_fresh_is_ok():
    t = okf_trust.trust_of_text(VERIFIED, NOW)
    assert t["verdict"] == "ok" and t["trust_tier"] == "human-reviewed"
    assert t["okf_conformant"] is True and t["stale"] is False


def test_a_bare_verified_mapping_counts_as_one_entry():
    assert okf_trust.trust_of_text(VERIFIED, NOW)["latest_verified_at"] == "2026-06-25T09:00:00Z"


def test_past_stale_after_is_stale_in_both_texts():
    for stamp in ("2026-09-23", "2026-09-23T00:00:00Z"):
        t = okf_trust.trust_of_text(VERIFIED.replace("2027-01-01T00:00:00Z", stamp), NOW)
        assert t["verdict"] == "stale" and t["stale"] is True


def test_content_changed_after_verification_is_unverified():
    t = okf_trust.trust_of_text(VERIFIED.replace("2026-06-01T00:00:00Z", "2026-07-01T00:00:00Z"), NOW)
    assert t["verdict"] == "unverified" and t["changed_since_verified"] is True


def test_machine_only_verification_is_machine_confirmed():
    t = okf_trust.trust_of_text(VERIFIED.replace("human:ahormati", "process:nightly"), NOW)
    assert t["trust_tier"] == "machine-confirmed" and t["verdict"] == "ok"


@pytest.mark.parametrize("text,verdict", [
    ("no frontmatter at all\n", "unverified"),
    ("---\ntype: Note\n---\nbody\n", "unverified"),
    ("---\ntype: Note\nstatus: deprecated\nverified: {by: human:a, at: 2026-01-01T00:00:00Z}\n---\n", "stale"),
    ("---\ntype: Note\nstatus: draft\nverified: {by: human:a, at: 2026-01-01T00:00:00Z}\n---\n", "unverified"),
])
def test_verdicts(text, verdict):
    assert okf_trust.trust_of_text(text, NOW)["verdict"] == verdict


@pytest.mark.parametrize("block", ["n: !!int notanumber", "a: [unclosed", "- just\n- a list"])
def test_unreadable_frontmatter_is_reported_not_raised(block):
    t = okf_trust.trust_of_text(f"---\n{block}\n---\nbody\n", NOW)
    assert t["verdict"] == "unverified" and t["okf_conformant"] is False


def test_missing_type_is_not_conformant():
    t = okf_trust.trust_of_text("---\ntitle: No type\n---\n", NOW)
    assert t["okf_conformant"] is False


# --- jidoseal_trust through the MCP surface ---------------------------------------------------
def test_trust_tool_on_one_file(tmp_path):
    p = _write(tmp_path / "leave.md", VERIFIED)
    is_error, payload = call_tool("jidoseal_trust", {"path": str(p)})
    assert not is_error, payload
    assert payload["trust_tier"] == "human-reviewed"
    assert payload["which_0_2"] == "both" or payload["which_0_2"] == "2026-08-21"


def test_trust_tool_on_a_folder(tmp_path):
    _write(tmp_path / "leave.md", VERIFIED)
    _write(tmp_path / "sub" / "old.md", "---\ntype: Note\nstale_after: 2020-01-01\n---\n")
    _write(tmp_path / "index.md", "# Index\n")  # reserved: not a concept, not checked
    _write(tmp_path / ".hidden" / "x.md", "no frontmatter\n")
    is_error, payload = call_tool("jidoseal_trust", {"path": str(tmp_path)})
    assert not is_error, payload
    assert payload["summary"]["files"] == 2
    assert payload["summary"]["stale"] == 1 and payload["summary"]["ok"] == 1
    assert payload["summary"]["which_0_2"] == "mixed"


def test_trust_tool_writes_nothing(tmp_path, recorder):
    _write(tmp_path / "leave.md", VERIFIED)
    with recorder:
        is_error, _ = call_tool("jidoseal_trust", {"path": str(tmp_path)})
    assert not is_error
    writes = [a for e, a in recorder.named("open") if len(a) > 1 and isinstance(a[1], str)
              and any(c in a[1] for c in "wax+")]
    assert writes == [] and not (tmp_path / ".jidoseal").exists()


def test_trust_tool_refuses_a_link_out(world):
    os.symlink(str(world["outside"]), str(world["root"] / "linked"))
    is_error, payload = call_tool("jidoseal_trust", {"path": str(world["root"])})
    assert is_error and "symlink" in payload["error"]


def test_trust_tool_rejects_a_missing_path(tmp_path):
    is_error, _ = call_tool("jidoseal_trust", {"path": str(tmp_path / "nope")})
    assert is_error


# --- jidoseal_changes -------------------------------------------------------------------------
git = shutil.which("git")
needs_git = pytest.mark.skipif(git is None, reason="git not installed")


def _repo(tmp_path):
    root = tmp_path / "notes"
    root.mkdir()
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
               GIT_COMMITTER_EMAIL="t@t")
    run = lambda *a: subprocess.run(["git", *a], cwd=str(root), env=env, check=True,  # noqa: E731
                                    capture_output=True)
    run("init", "-q")
    _write(root / "leave.md", VERIFIED)
    _write(root / "gone.md", VERIFIED.replace("Leave", "Gone"))
    _write(root / "plain.md", "---\ntype: Note\n---\nx\n")
    run("add", "-A")
    run("commit", "-qm", "init")
    return root


@needs_git
def test_changes_flags_an_edit_that_leaves_verification_behind(tmp_path):
    root = _repo(tmp_path)
    _write(root / "leave.md", VERIFIED.replace("25 days", "20 days"))
    (root / "gone.md").unlink()
    _write(root / "new.md", "fresh, no frontmatter\n")
    is_error, payload = call_tool("jidoseal_changes", {"root": str(root)})
    assert not is_error, payload
    by = {f["path"]: f for f in payload["files"]}
    assert set(by) == {"leave.md", "gone.md", "new.md"}
    assert by["leave.md"]["change"] == "modified" and by["leave.md"]["body_changed"]
    assert any(x.startswith("verification not renewed") for x in by["leave.md"]["flags"])
    assert any(x.startswith("generated.at not updated") for x in by["leave.md"]["flags"])
    assert by["gone.md"]["change"] == "deleted"
    assert "a verified document was deleted" in by["gone.md"]["flags"]
    assert by["new.md"]["change"] == "added"
    assert payload["summary"]["verification_not_renewed"] == 1


@needs_git
def test_changes_with_renewed_verification_is_not_flagged(tmp_path):
    root = _repo(tmp_path)
    _write(root / "leave.md", VERIFIED.replace("25 days", "20 days")
           .replace("2026-06-01T00:00:00Z", "2026-10-01T00:00:00Z")
           .replace("2026-06-25T09:00:00Z", "2026-10-02T09:00:00Z"))
    is_error, payload = call_tool("jidoseal_changes", {"root": str(root)})
    assert not is_error
    assert payload["files"][0]["flags"] == []


@needs_git
def test_changes_rejects_option_like_refs_and_non_repos(tmp_path):
    root = _repo(tmp_path)
    assert call_tool("jidoseal_changes", {"root": str(root), "since": "--output=/tmp/x"})[0]
    assert call_tool("jidoseal_changes", {"root": str(root), "since": "no-such-ref"})[0]
    plain = tmp_path / "plain"
    plain.mkdir()
    assert call_tool("jidoseal_changes", {"root": str(plain)})[0]


@needs_git
def test_changes_runs_only_git_and_writes_nothing(tmp_path, recorder):
    root = _repo(tmp_path)
    _write(root / "leave.md", VERIFIED.replace("25 days", "20 days"))
    with recorder:
        is_error, _ = call_tool("jidoseal_changes", {"root": str(root)})
    assert not is_error
    spawned = [a for e, a in recorder.events if e == "subprocess.Popen"]
    assert spawned and all(os.path.basename(os.fsdecode(a[0])) == "git" for a in spawned)
    assert all("protocol.allow=never" in [os.fsdecode(x) for x in a[1]] for a in spawned)
    assert not (root / ".jidoseal").exists()


@needs_git
def test_trust_and_changes_make_no_socket_call(tmp_path, recorder):
    root = _repo(tmp_path)
    _write(root / "leave.md", VERIFIED.replace("25 days", "20 days"))
    with recorder:
        assert not call_tool("jidoseal_trust", {"path": str(root)})[0]
        assert not call_tool("jidoseal_changes", {"root": str(root)})[0]
    assert recorder.named("socket.") == []
