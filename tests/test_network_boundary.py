"""
No network during a scan — not a connection, not a DNS lookup, not even a socket object.

Three independent checks:
  1. In-process, with every socket entry point replaced by one that fails the test, and the
     interpreter's `socket.*` audit events recorded.
  2. In a fresh interpreter: after a scan and an offer, no network-capable module (socket,
     ssl, urllib.request, http.client, checkout_client) has even been imported.
  3. End to end: the real `jidoseal-mcp` stdio server in a child process whose audit hook
     kills the process (exit 97) on the first socket event of any kind.
Each harness has a self-check proving it would catch a socket if one were opened.
"""
from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import textwrap

import pytest

from conftest import REPO, SRC, call_tool

# `selectors` is deliberately not listed: on Python 3.9 the stdlib's own `uuid` imports
# `platform` -> `subprocess` -> `selectors`, none of which opens anything by being imported.
# A child process is ruled out separately, by test_scan_starts_no_child_process.
NETWORK_MODULES = ("socket", "ssl", "urllib.request", "http.client", "checkout_client",
                   "asyncio")


class NetworkUsed(AssertionError):
    pass


@pytest.fixture
def no_network(monkeypatch):
    def refuse(*args, **kwargs):
        raise NetworkUsed(f"network used during a scan: {args!r}")

    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.setattr(socket.socket, "connect_ex", refuse)
    monkeypatch.setattr(socket.socket, "sendto", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)
    monkeypatch.setattr(socket, "getaddrinfo", refuse)
    monkeypatch.setattr(socket, "gethostbyname", refuse)
    monkeypatch.setattr(socket, "gethostbyname_ex", refuse)


def test_self_check_the_blocker_catches_a_connect(no_network):
    with pytest.raises(NetworkUsed):
        socket.create_connection(("127.0.0.1", 9))
    with pytest.raises(NetworkUsed):
        socket.getaddrinfo("example.com", 443)
    s = socket.socket()
    try:
        with pytest.raises(NetworkUsed):
            s.connect(("127.0.0.1", 9))
    finally:
        s.close()


def test_self_check_the_recorder_sees_socket_events(recorder):
    with recorder:
        socket.socket().close()
    assert recorder.named("socket.")


@pytest.mark.parametrize("tool", ["jidoseal_scan", "jidoseal_certification_offer"])
def test_scan_and_offer_make_no_socket_call(world, no_network, recorder, tool):
    with recorder:
        is_error, payload = call_tool(tool, {"root": str(world["root"])})
    assert not is_error, payload
    assert recorder.named("socket.") == []


def test_checkout_without_confirm_makes_no_socket_call(gold_root, no_network, recorder):
    with recorder:
        is_error, _ = call_tool("jidoseal_start_checkout", {
            "root": str(gold_root), "company": "A", "submitter_name": "B",
            "submitter_email": "b@example.com"})
    assert is_error
    assert recorder.named("socket.") == []


def _child_env(extra_path=None):
    env = dict(os.environ)
    parts = ([extra_path] if extra_path else []) + [SRC]
    env["PYTHONPATH"] = os.pathsep.join(parts + [env.get("PYTHONPATH", "")]).rstrip(os.pathsep)
    env.pop("JIDOSEAL_SITE_URL", None)
    return env


def test_a_fresh_scan_never_imports_a_network_module(world):
    script = textwrap.dedent(f"""
        import json, sys
        import jidoseal_mcp
        jidoseal_mcp.tool_jidoseal_scan({{"root": {str(world["root"])!r}}})
        jidoseal_mcp.tool_jidoseal_certification_offer({{"root": {str(world["root"])!r}}})
        print(json.dumps([m for m in {NETWORK_MODULES!r} if m in sys.modules]))
    """)
    out = subprocess.run([sys.executable, "-c", script], env=_child_env(), cwd=REPO,
                         capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, out.stderr
    assert json.loads(out.stdout.strip().splitlines()[-1]) == []


KILL_ON_SOCKET = """
import os, sys
def _hook(event, args):
    if event.startswith("socket."):
        sys.stderr.write("NETWORK EVENT: %s %r\\n" % (event, args))
        sys.stderr.flush()
        os._exit(97)
sys.addaudithook(_hook)
"""


@pytest.fixture
def kill_on_socket(tmp_path):
    d = tmp_path / "hook"
    d.mkdir()
    (d / "sitecustomize.py").write_text(KILL_ON_SOCKET, encoding="utf-8")
    return str(d)


def test_self_check_the_child_harness_kills_on_a_socket(kill_on_socket):
    out = subprocess.run([sys.executable, "-c", "import socket; socket.socket()"],
                         env=_child_env(kill_on_socket), capture_output=True, text=True,
                         timeout=60)
    assert out.returncode == 97, (out.returncode, out.stderr)


def test_stdio_server_end_to_end_opens_no_socket(world, kill_on_socket):
    root = str(world["root"])
    msgs = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize",
         "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                    "clientInfo": {"name": "pytest", "version": "0"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
         "params": {"name": "jidoseal_scan", "arguments": {"root": root}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
         "params": {"name": "jidoseal_certification_offer", "arguments": {"root": root}}},
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call",
         "params": {"name": "jidoseal_start_checkout",
                    "arguments": {"root": root, "company": "A", "submitter_name": "B",
                                  "submitter_email": "b@example.com"}}},
    ]
    stdin = "".join(json.dumps(m) + "\n" for m in msgs)
    out = subprocess.run([sys.executable, "-m", "jidoseal_mcp"], input=stdin,
                         env=_child_env(kill_on_socket), cwd=REPO, capture_output=True,
                         text=True, timeout=120)
    assert out.returncode == 0, (out.returncode, out.stderr)
    replies = {r["id"]: r for r in map(json.loads, out.stdout.splitlines())}
    assert sorted(replies) == [1, 2, 3, 4, 5]
    assert replies[3]["result"]["isError"] is False
    assert replies[4]["result"]["isError"] is False
    assert replies[5]["result"]["isError"] is True  # no confirm: refused, nothing sent


@pytest.mark.parametrize("tool", ["jidoseal_scan", "jidoseal_certification_offer"])
def test_scan_starts_no_child_process(world, recorder, tool):
    # A child process would be outside every check above, so there must be none.
    with recorder:
        is_error, _ = call_tool(tool, {"root": str(world["root"])})
    assert not is_error
    spawned = [e for e, _ in recorder.events
               if e.startswith(("subprocess.", "os.system", "os.exec", "os.posix_spawn",
                                "os.spawn", "os.fork", "os.startfile"))]
    assert spawned == []
