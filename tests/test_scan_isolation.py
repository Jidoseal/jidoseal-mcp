"""
The scan reads nothing outside the folder it was given.

Engine 0.1.3 discovered files with `glob("**/*.md", recursive=True)`, which follows symlinks.
jidoseal-mcp therefore refuses, before the engine runs, any folder in which such a walk could
reach outside the folder: a symlinked directory (inside or out, including a loop back up the
tree), a symlinked `.md` file whose target is outside, or a symlinked `.jidoseal/` record.
These tests hold both halves: normal scans stay inside, and the refusals happen before a
single outside byte is read. Engine 0.1.4 (the pinned version) refuses links out on its own as
well; the last tests here check that the installed `jidoseal` CLI does.
"""
from __future__ import annotations

import os

import pytest

from conftest import call_tool, event_path, is_python_import_read, within

SCAN_TOOLS = ["jidoseal_scan", "jidoseal_certification_offer"]


def _reads(recorder):
    out = []
    for _, args in recorder.named("open"):
        p = event_path(args[0])
        if p is not None:
            out.append(p)
    for _, args in recorder.named("os.listdir") + recorder.named("os.scandir"):
        p = event_path(args[0]) if args and args[0] is not None else os.path.abspath(".")
        if p is not None:
            out.append(p)
    return out


def _outside_reads(recorder, root):
    return [p for p in _reads(recorder)
            if not within(p, root) and not is_python_import_read(p)]


@pytest.mark.parametrize("tool", SCAN_TOOLS)
def test_scan_opens_and_lists_nothing_outside_the_root(world, recorder, tool):
    with recorder:
        is_error, payload = call_tool(tool, {"root": str(world["root"])})
    assert not is_error, payload
    assert _outside_reads(recorder, world["root"]) == []
    assert not any(within(p, world["outside"]) for p in _reads(recorder))


def test_scan_does_read_the_files_inside_the_root(world, recorder):
    # Guards the test above against passing vacuously (e.g. a hook that records nothing).
    with recorder:
        is_error, payload = call_tool("jidoseal_scan", {"root": str(world["root"])})
    assert not is_error
    opened = {os.path.relpath(p, str(world["root"])) for p in _reads(recorder)
              if within(p, world["root"]) and p.endswith(".md")}
    assert {"gold.md", os.path.join("sub", "silver.md"), "expenses.md"} <= opened
    assert payload["corpus"]["file_count"] == 5


@pytest.mark.parametrize("tool", SCAN_TOOLS + ["jidoseal_start_checkout"])
def test_symlinked_md_file_pointing_outside_is_refused(world, recorder, tool):
    os.symlink(str(world["outside"] / "secret.md"), str(world["root"] / "link.md"))
    args = {"root": str(world["root"])}
    if tool == "jidoseal_start_checkout":
        args.update(company="A", submitter_name="B", submitter_email="b@example.com",
                    confirm=True)
    with recorder:
        is_error, payload = call_tool(tool, args)
    assert is_error
    assert "link.md" in payload["error"] and "symlink" in payload["error"]
    assert not any(within(p, world["outside"]) for p in _reads(recorder))
    assert not (world["root"] / ".jidoseal").exists(), "refused before the engine ran"


def test_symlinked_directory_pointing_outside_is_refused(world, recorder):
    os.symlink(str(world["outside"]), str(world["root"] / "elsewhere"))
    with recorder:
        is_error, payload = call_tool("jidoseal_scan", {"root": str(world["root"])})
    assert is_error and "elsewhere" in payload["error"]
    assert not any(within(p, world["outside"]) for p in _reads(recorder))


def test_symlink_loop_is_refused_not_expanded(world, recorder):
    os.symlink("..", str(world["root"] / "sub" / "up"))
    with recorder:
        is_error, payload = call_tool("jidoseal_scan", {"root": str(world["root"])})
    assert is_error and os.path.join("sub", "up") in payload["error"]
    assert not (world["root"] / ".jidoseal").exists()


def test_symlinked_directory_inside_root_is_refused_too(world):
    # Not a read outside, but the glob would count its files twice; refused for the same reason.
    os.symlink(str(world["root"] / "sub"), str(world["root"] / "sub-again"))
    is_error, payload = call_tool("jidoseal_scan", {"root": str(world["root"])})
    assert is_error and "sub-again" in payload["error"]


def test_symlinked_md_file_inside_root_is_read_once(world, recorder):
    # Not refused: the link stays inside. Engine 0.1.4 reads each file once, so a link to a file
    # that is scanned anyway adds nothing (0.1.3 listed it twice); a link to an inside file the
    # scan would not otherwise reach is scanned under the link's own name.
    (world["root"] / ".drafts").mkdir()
    (world["root"] / ".drafts" / "draft.md").write_text("---\ntype: note\n---\n", encoding="utf-8")
    os.symlink(str(world["root"] / "gold.md"), str(world["root"] / "alias.md"))
    os.symlink(str(world["root"] / ".drafts" / "draft.md"), str(world["root"] / "draft.md"))
    with recorder:
        is_error, payload = call_tool("jidoseal_scan", {"root": str(world["root"])})
    assert not is_error, payload
    names = [f["name"] for f in payload["files"]]
    assert "gold.md" in names and "alias.md" not in names
    assert "draft.md" in names
    assert _outside_reads(recorder, world["root"]) == []


def test_symlink_in_a_hidden_directory_is_ignored_because_the_scan_never_goes_there(world, recorder):
    (world["root"] / ".git").mkdir()
    os.symlink(str(world["outside"]), str(world["root"] / ".git" / "out"))
    os.symlink(str(world["outside"] / "secret.md"), str(world["root"] / ".hidden.md"))
    with recorder:
        is_error, payload = call_tool("jidoseal_scan", {"root": str(world["root"])})
    assert not is_error, payload
    assert not any(within(p, world["outside"]) for p in _reads(recorder))


@pytest.mark.parametrize("record", [None, "manifest.json", "progress.ndjson", "config.yaml",
                                    "consent.json", "audit.jsonl", "backups"])
def test_symlinked_jidoseal_records_are_refused(world, recorder, record):
    target_dir = world["outside"] / "records"
    target_dir.mkdir()
    if record is None:
        os.symlink(str(target_dir), str(world["root"] / ".jidoseal"))
    else:
        (world["root"] / ".jidoseal").mkdir()
        (target_dir / record).write_text("", encoding="utf-8")
        os.symlink(str(target_dir / record), str(world["root"] / ".jidoseal" / record))
    with recorder:
        is_error, payload = call_tool("jidoseal_scan", {"root": str(world["root"])})
    assert is_error and ".jidoseal" in payload["error"]
    assert not any(within(p, world["outside"]) for p in _reads(recorder))
    assert [p.name for p in target_dir.iterdir()] == ([] if record is None else [record])
    if record is not None:
        assert (target_dir / record).read_text(encoding="utf-8") == ""


def test_root_given_through_a_symlink_is_scanned_inside_its_target(world, recorder):
    alias = world["tmp"] / "root-alias"
    os.symlink(str(world["root"]), str(alias))
    with recorder:
        is_error, payload = call_tool("jidoseal_scan", {"root": str(alias)})
    assert not is_error, payload
    assert _outside_reads(recorder, world["root"]) == []


def test_missing_root_is_an_error_not_an_empty_scan(tmp_path):
    is_error, payload = call_tool("jidoseal_scan", {"root": str(tmp_path / "nope")})
    assert is_error and "does not exist" in payload["error"]


# The installed engine's own command line (engine 0.1.4 and later). The server above refuses
# before the engine runs; these check that the `jidoseal` CLI, used without this server, also
# refuses a link out, writes nothing, and reads nothing outside the folder.
def _run_cli(root):
    import subprocess
    import sys
    return subprocess.run([sys.executable, "-m", "jidoseal", "--root", str(root)],
                          capture_output=True, text=True, timeout=120)


@pytest.mark.parametrize("link", ["dir", "file", "parent", "jidoseal"])
def test_the_installed_cli_refuses_a_link_out(world, link):
    root, outside = world["root"], world["outside"]
    if link == "dir":
        os.symlink(str(outside), str(root / "linked"))
    elif link == "file":
        os.symlink(str(outside / "secret.md"), str(root / "secret.md"))
    elif link == "parent":
        os.symlink("..", str(root / "up"))
    else:
        (outside / "records").mkdir()
        os.symlink(str(outside / "records"), str(root / ".jidoseal"))
    before = sorted(p.name for p in outside.rglob("*"))
    r = _run_cli(root)
    assert r.returncode == 2, (r.returncode, r.stdout, r.stderr)
    assert "Not scanned: this folder contains symlinks" in r.stderr
    assert "scanned " not in r.stdout
    assert sorted(p.name for p in outside.rglob("*")) == before
    if link != "jidoseal":
        assert not (root / ".jidoseal").exists()


def test_the_installed_cli_reads_an_inside_directory_link_once(world):
    import json
    root = world["root"]
    os.symlink(str(root / "sub"), str(root / "sub-again"))
    os.symlink("..", str(root / "sub" / "up"))
    r = _run_cli(root)
    assert r.returncode == 0, r.stderr
    manifest = json.loads((root / ".jidoseal" / "manifest.json").read_text(encoding="utf-8"))
    assert not any(f.startswith(("sub-again", os.path.join("sub", "up"))) for f in manifest["files"])
