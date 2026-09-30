"""
A scan writes only under <root>/.jidoseal/ — `manifest.json`, and `progress.ndjson`
appended to — and never modifies the user's notes.

Held two ways: a before/after snapshot of every file around the scan (content and mtime),
and the interpreter's own audit events for every open-for-write and every filesystem mutation.
"""
from __future__ import annotations

import json
import os

import pytest

from conftest import call_tool, event_path, within

WRITE_EVENTS = ("os.mkdir", "os.rename", "os.replace", "os.remove", "os.rmdir", "os.truncate",
                "os.chmod", "os.chown", "os.utime", "os.symlink", "os.link", "shutil.")


def _snapshot(folder):
    """{relpath: (mtime, bytes)} for files, {relpath: "dir"} for directories. A directory's own
    mtime is left out: creating `.jidoseal/` inside the root necessarily bumps the root's."""
    out = {}
    for dirpath, dirnames, filenames in os.walk(str(folder)):
        for name in dirnames + filenames:
            p = os.path.join(dirpath, name)
            if os.path.isdir(p) and not os.path.islink(p):
                out[os.path.relpath(p, str(folder))] = "dir"
                continue
            st = os.lstat(p)
            data = None
            if os.path.isfile(p) and not os.path.islink(p):
                with open(p, "rb") as fh:
                    data = fh.read()
            out[os.path.relpath(p, str(folder))] = (st.st_mtime_ns, data)
    return out


def _is_write_open(args):
    mode, flags = args[1], args[2]
    if isinstance(mode, str) and any(c in mode for c in "wax+"):
        return True
    if isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND
                                           | os.O_TRUNC):
        return True
    return False


def _write_targets(recorder):
    targets = []
    for event, args in recorder.events:
        if event == "open" and _is_write_open(args):
            targets.append(event_path(args[0]))
        elif event.startswith(WRITE_EVENTS):
            targets.extend(event_path(a) for a in args[:2] if isinstance(a, (str, bytes)))
    return [t for t in targets if t is not None]


@pytest.mark.parametrize("tool", ["jidoseal_scan", "jidoseal_certification_offer"])
def test_only_jidoseal_records_change(world, tool):
    before = _snapshot(world["tmp"])
    is_error, payload = call_tool(tool, {"root": str(world["root"])})
    assert not is_error, payload
    after = _snapshot(world["tmp"])

    changed = {k for k in set(before) | set(after) if before.get(k) != after.get(k)}
    expected = {os.path.join("root", ".jidoseal"),
                os.path.join("root", ".jidoseal", "manifest.json"),
                os.path.join("root", ".jidoseal", "progress.ndjson")}
    assert changed == expected


@pytest.mark.parametrize("tool", ["jidoseal_scan", "jidoseal_certification_offer"])
def test_every_write_the_interpreter_sees_is_under_root_jidoseal(world, recorder, tool):
    with recorder:
        is_error, _ = call_tool(tool, {"root": str(world["root"])})
    assert not is_error
    targets = _write_targets(recorder)
    assert targets, "the scan writes its records, so the hook must have seen writes"
    jdir = world["root"] / ".jidoseal"
    assert [t for t in targets if not within(t, jdir)] == []


def test_notes_are_byte_for_byte_unchanged(world):
    notes = {p: p.read_bytes() for p in world["root"].rglob("*.md")}
    call_tool("jidoseal_scan", {"root": str(world["root"])})
    call_tool("jidoseal_scan", {"root": str(world["root"])})
    assert {p: p.read_bytes() for p in world["root"].rglob("*.md")} == notes


def test_progress_is_appended_and_manifest_rewritten(world):
    call_tool("jidoseal_scan", {"root": str(world["root"])})
    progress = world["root"] / ".jidoseal" / "progress.ndjson"
    first = progress.read_text(encoding="utf-8").splitlines()
    call_tool("jidoseal_scan", {"root": str(world["root"])})
    second = progress.read_text(encoding="utf-8").splitlines()
    assert second[:len(first)] == first and len(second) > len(first)
    for line in second:
        json.loads(line)
    manifest = json.loads((world["root"] / ".jidoseal" / "manifest.json").read_text("utf-8"))
    assert set(manifest["files"]) == {"expenses.md", "leave-policy.md", "notes.md", "gold.md",
                                      os.path.join("sub", "silver.md")}


def test_scan_result_names_where_it_wrote(world):
    _, payload = call_tool("jidoseal_scan", {"root": str(world["root"])})
    jdir = os.path.join(str(world["root"]), ".jidoseal")
    assert payload["scan"]["manifest_path"] == os.path.join(jdir, "manifest.json")
    assert payload["scan"]["progress_path"] == os.path.join(jdir, "progress.ndjson")


def test_existing_config_is_read_not_rewritten(world):
    jdir = world["root"] / ".jidoseal"
    jdir.mkdir()
    config = jdir / "config.yaml"
    config.write_text("# corpus conventions\n", encoding="utf-8")
    before = (config.read_bytes(), os.stat(str(config)).st_mtime_ns)
    is_error, _ = call_tool("jidoseal_scan", {"root": str(world["root"])})
    assert not is_error
    assert (config.read_bytes(), os.stat(str(config)).st_mtime_ns) == before
