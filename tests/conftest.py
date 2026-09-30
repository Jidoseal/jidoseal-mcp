"""
Shared fixtures for the jidoseal-mcp test suite.

The suite runs against the INSTALLED `jidoseal` engine wheel (the version pinned in
pyproject.toml), exactly as a user's `pip install jidoseal-mcp` gets it.

Observation is done with a Python audit hook (PEP 578): the interpreter itself reports every
`open()`, directory listing, filesystem mutation and socket operation, including ones made
inside the engine. A hook cannot be removed once added, so ONE hook is installed here, for the
whole session, and it records only while a test holds the `Recorder` open.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from typing import Any, Dict, List, Optional, Tuple

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "src")
EXAMPLES = os.path.join(REPO, "examples", "tiers")
sys.path.insert(0, SRC)

import jidoseal_mcp  # noqa: E402


class Recorder:
    """Collects audit events while active. Use as a context manager."""

    def __init__(self) -> None:
        self.active = False
        self.events: List[Tuple[str, tuple]] = []

    def __enter__(self) -> "Recorder":
        self.events = []
        self.active = True
        return self

    def __exit__(self, *exc: Any) -> None:
        self.active = False

    def named(self, prefix: str) -> List[Tuple[str, tuple]]:
        return [(e, a) for e, a in self.events if e.startswith(prefix)]


_RECORDER = Recorder()


def _hook(event: str, args: tuple) -> None:
    if _RECORDER.active:
        _RECORDER.events.append((event, args))


sys.addaudithook(_hook)


@pytest.fixture
def recorder() -> Recorder:
    _RECORDER.active = False
    yield _RECORDER
    _RECORDER.active = False


def call_tool(name: str, arguments: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """Call a tool through the real JSON-RPC surface. Returns (is_error, payload)."""
    resp = jidoseal_mcp.handle_message({
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    })
    result = resp["result"]
    return result["isError"], json.loads(result["content"][0]["text"])


@pytest.fixture
def world(tmp_path):
    """tmp_path/root  — the folder to scan: the Gold, Silver and mixed examples.
    tmp_path/outside — a sibling folder the scan must never read or write."""
    root = tmp_path / "root"
    shutil.copytree(os.path.join(EXAMPLES, "mixed"), str(root))
    shutil.copy(os.path.join(EXAMPLES, "gold", "leave-policy.md"), str(root / "gold.md"))
    (root / "sub").mkdir()
    shutil.copy(os.path.join(EXAMPLES, "silver", "leave-policy.md"), str(root / "sub" / "silver.md"))
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "secret.md").write_text(
        "---\ntype: secret\ntitle: OUTSIDE-SECRET\n---\nOUTSIDE-SECRET body\n", encoding="utf-8")
    return {"tmp": tmp_path, "root": root, "outside": outside}


@pytest.fixture
def gold_root(tmp_path):
    """A folder that is at Gold, so the checkout tool has something to certify."""
    root = tmp_path / "private-notes-folder"
    root.mkdir()
    shutil.copy(os.path.join(EXAMPLES, "gold", "leave-policy.md"), str(root / "leave-policy.md"))
    (root / "handbook.md").write_text(
        "---\ntype: guide\ntitle: Handbook\ndescription: How we work.\n"
        "timestamp: 2026-09-01\nowner: dept:people-ops\nstatus: stable\n"
        "review_policy: yearly\nreviewed_at: 2026-09-01\nnext_review_at: 2027-09-01\n---\n"
        "# Handbook\n", encoding="utf-8")
    return root


def event_path(arg: Any) -> Optional[str]:
    """An audit event's path argument as an absolute str, or None for a file descriptor."""
    if isinstance(arg, int):
        return None
    if isinstance(arg, bytes):
        arg = os.fsdecode(arg)
    if isinstance(arg, os.PathLike):
        arg = os.fspath(arg)
    if not isinstance(arg, str):
        return None
    return os.path.abspath(arg)


def within(path: str, folder) -> bool:
    folder = os.path.realpath(str(folder))
    return os.path.commonpath([os.path.realpath(path), folder]) == folder


def python_install_dirs() -> List[str]:
    dirs = {os.path.realpath(p) for p in (sys.prefix, sys.base_prefix, sys.exec_prefix,
                                          sys.base_exec_prefix)}
    dirs.update(os.path.realpath(p) for p in sys.path if p and os.path.isdir(p))
    return sorted(dirs)


def is_python_import_read(path: str) -> bool:
    """A read the interpreter makes to import code lazily (a stdlib or site-packages module
    first used mid-scan). These are Python's own files, never the user's."""
    if not path.endswith((".py", ".pyc", ".so", ".pth")) and "__pycache__" not in path:
        return False
    return any(within(path, d) for d in python_install_dirs())
