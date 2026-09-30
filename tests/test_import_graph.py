"""
Static check: nothing on the scan path can reach the network, because nothing on it imports a
network-capable module — in this repository's code, in every module of the installed `jidoseal`
engine wheel, or in PyYAML (the engine's one dependency).

The engine is proprietary-licensed but ships as plain Python source; this test reads that
source with `ast`, so it covers imports inside functions too, not just the top of each file.
"""
from __future__ import annotations

import ast
import importlib.metadata
import os
import sys
from typing import Iterator, List, Tuple

import pytest

from conftest import SRC

FORBIDDEN = {"socket", "ssl", "http", "urllib", "urllib3", "requests", "httpx", "aiohttp",
             "ftplib", "smtplib", "poplib", "imaplib", "nntplib", "telnetlib", "xmlrpc",
             "socketserver", "asyncio", "selectors", "subprocess", "multiprocessing", "ctypes",
             "webbrowser", "checkout_client"}
FORBIDDEN_CALLS = {"__import__", "exec", "eval", "import_module", "system", "popen",
                   "execv", "execve", "execvp", "spawnv", "spawnl", "startfile"}

# Two known, bounded exceptions, each pinned by its own test below rather than waved through:
#  * okf_manifest._git_date runs `git log` (local, no network) to date a file. It is called only
#    from apply_silver — the CLI's `--apply silver` write path — which this server never calls.
#  * PyYAML's constructor calls __import__ for its UNSAFE loaders. The engine uses safe_load only.
ALLOWED = {("okf_manifest.py", "import", "subprocess"), ("constructor.py", "call", "__import__")}

SCAN_PATH_SRC = ["jidoseal_mcp", "scan_result", "offer", "engine_path", "attestation"]
ENGINE_MODULES = {"jidoseal", "local_runner", "okf_manifest", "okf_remediate", "scan_config",
                  "tier1_gate", "syntax_gate", "consent", "i18n", "frontmatter_i18n"}


def _imports(tree: ast.AST) -> Iterator[Tuple[str, ast.AST]]:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name.split(".")[0], node
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            yield node.module.split(".")[0], node


def _calls(tree: ast.AST) -> Iterator[str]:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name):
                yield f.id
            elif isinstance(f, ast.Attribute):
                yield f.attr


def _parse(path: str) -> ast.AST:
    with open(path, "rb") as fh:
        return ast.parse(fh.read(), filename=path)


def _engine_files() -> List[str]:
    files = importlib.metadata.files("jidoseal") or []
    return sorted(str(f.locate()) for f in files if str(f).endswith(".py"))


def _yaml_files() -> List[str]:
    import yaml
    d = os.path.dirname(yaml.__file__)
    return sorted(os.path.join(d, n) for n in os.listdir(d) if n.endswith(".py"))


def test_engine_wheel_contains_exactly_the_ten_scan_modules():
    names = {os.path.splitext(os.path.basename(p))[0] for p in _engine_files()}
    assert names == ENGINE_MODULES


@pytest.mark.parametrize("path", _engine_files() + _yaml_files()
                         + [os.path.join(SRC, m + ".py") for m in SCAN_PATH_SRC if m != "jidoseal_mcp"],
                         ids=os.path.basename)
def test_scan_path_module_imports_nothing_network_capable(path):
    tree = _parse(path)
    base = os.path.basename(path)
    bad = sorted({name for name, _ in _imports(tree)
                  if name in FORBIDDEN and (base, "import", name) not in ALLOWED})
    assert bad == [], f"{path} imports {bad}"
    calls = sorted(c for c in set(_calls(tree)) & FORBIDDEN_CALLS
                   if (base, "call", c) not in ALLOWED)
    assert calls == [], f"{path} calls {calls}"


def _engine_tree(name: str) -> ast.AST:
    return _parse(next(p for p in _engine_files() if os.path.basename(p) == name + ".py"))


def _functions_calling(tree: ast.AST, callee: str) -> List[str]:
    return sorted(fn.name for fn in ast.walk(tree) if isinstance(fn, ast.FunctionDef)
                  and callee in set(_calls(fn)) and fn.name != callee)


def test_engine_subprocess_is_only_git_log_on_the_apply_path():
    tree = _engine_tree("okf_manifest")
    holders = sorted(fn.name for fn in ast.walk(tree) if isinstance(fn, ast.FunctionDef)
                     and any(n == "subprocess" for n, _ in _imports(fn)))
    assert holders == ["_git_date"]
    assert _functions_calling(tree, "_git_date") == ["apply_silver"]
    # ... and nothing in this repository ever calls an engine apply_* write path.
    for name in os.listdir(SRC):
        if name.endswith(".py"):
            assert not {c for c in _calls(_parse(os.path.join(SRC, name)))
                        if c.startswith("apply_")}, name


def test_engine_parses_yaml_with_safe_load_only():
    used = set()
    for path in _engine_files():
        for node in ast.walk(_parse(path)):
            if (isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name)
                    and node.value.id == "yaml"):
                used.add(node.attr)
            if isinstance(node, ast.ImportFrom) and node.module == "yaml":
                used.update(a.name for a in node.names)
    assert "safe_load" in used
    assert used <= {"safe_load", "YAMLError"}, sorted(used)


def test_server_imports_checkout_client_only_inside_the_checkout_handler():
    tree = _parse(os.path.join(SRC, "jidoseal_mcp.py"))
    where = []
    for fn in ast.walk(tree):
        if isinstance(fn, ast.FunctionDef):
            for name, _ in _imports(fn):
                if name in FORBIDDEN:
                    where.append((fn.name, name))
    all_forbidden = [name for name, _ in _imports(tree) if name in FORBIDDEN]
    assert where == [("tool_jidoseal_start_checkout", "checkout_client")]
    assert all_forbidden == ["checkout_client"], "no module-level network import"
    assert sorted(set(_calls(tree)) & FORBIDDEN_CALLS) == []


def test_checkout_client_is_the_only_module_here_that_imports_urllib():
    users = []
    for name in sorted(os.listdir(SRC)):
        if name.endswith(".py"):
            tree = _parse(os.path.join(SRC, name))
            if any(n in FORBIDDEN - {"checkout_client"} for n, _ in _imports(tree)):
                users.append(name)
    assert users == ["checkout_client.py"]


def test_engine_is_imported_from_the_installed_wheel():
    import okf_manifest
    engine_dir = os.path.dirname(os.path.realpath(okf_manifest.__file__))
    assert os.path.realpath(os.path.dirname(_engine_files()[0])) == engine_dir
    assert engine_dir in {os.path.realpath(p) for p in sys.path if p}
