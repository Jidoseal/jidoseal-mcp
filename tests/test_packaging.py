"""
The engine version is pinned, and the pin, the published hashes, the SBOM and the installed
engine all name the same thing. If any one of them moves alone, this fails.
"""
from __future__ import annotations

import base64
import hashlib
import importlib.metadata
import json
import os
import re

from conftest import REPO


def _read(name: str) -> str:
    with open(os.path.join(REPO, name), encoding="utf-8") as fh:
        return fh.read()


def _pyproject_value(key: str) -> str:
    m = re.search(rf'^{key}\s*=\s*"([^"]+)"', _read("pyproject.toml"), re.M)
    assert m, key
    return m.group(1)


def _pinned_engine() -> str:
    deps = re.search(r"^dependencies\s*=\s*\[(.*?)\]", _read("pyproject.toml"), re.M | re.S)
    reqs = re.findall(r'"([^"]+)"', deps.group(1))
    assert len(reqs) == 1
    m = re.fullmatch(r"jidoseal==(\d+\.\d+\.\d+)", reqs[0])
    assert m, f"engine must be pinned exactly, got {reqs[0]!r}"
    return m.group(1)


def _sbom():
    return json.loads(_read("sbom.cdx.json"))


def _sbom_engine():
    return next(c for c in _sbom()["components"] if c["name"] == "jidoseal")


def test_installed_engine_is_the_pinned_one():
    import local_runner
    pinned = _pinned_engine()
    assert importlib.metadata.version("jidoseal") == pinned
    assert local_runner.VERSION == pinned


def test_hash_file_names_the_pinned_wheel():
    pinned = _pinned_engine()
    lines = [l.split() for l in _read("ENGINE-SHA256SUMS").splitlines()
             if l.strip() and not l.startswith("#")]
    names = {name: digest for digest, name in lines}
    wheel = f"jidoseal-{pinned}-py3-none-any.whl"
    assert wheel in names and re.fullmatch(r"[0-9a-f]{64}", names[wheel])
    assert _sbom_engine()["hashes"][0]["content"] == names[wheel]


def test_sbom_versions_match_pyproject():
    sbom = _sbom()
    assert sbom["metadata"]["component"]["version"] == _pyproject_value("version")
    assert _sbom_engine()["version"] == _pinned_engine()


def test_installed_engine_files_match_the_sbom_hashes():
    """Every module the installed engine consists of is byte-identical to the file listed, with
    its sha256, in sbom.cdx.json — i.e. what runs is what is published."""
    listed = {f["name"]: f["hashes"][0]["content"] for f in _sbom_engine()["components"]}
    installed = {}
    for f in importlib.metadata.files("jidoseal") or []:
        if str(f).endswith(".py") and "/" not in str(f):
            with open(str(f.locate()), "rb") as fh:
                installed[str(f)] = hashlib.sha256(fh.read()).hexdigest()
            # And the wheel's own RECORD agrees.
            record = base64.urlsafe_b64decode(f.hash.value + "==").hex()
            assert record == installed[str(f)], str(f)
    assert installed == listed


def test_server_json_version_matches_pyproject():
    server = json.loads(_read("server.json"))
    v = _pyproject_value("version")
    assert server["version"] == v
    assert all(p["version"] == v for p in server["packages"])
    assert len(server["description"]) <= 100  # MCP Registry limit
