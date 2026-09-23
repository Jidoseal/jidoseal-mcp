"""
attestation.py — Merkle-root construction over the scan-once manifest.

Reuses the per-file `sha256` hashes okf_manifest.py already computes
(`build_manifest()["files"][rel]["hash"]`) — this module does NOT
recompute file content hashes; a second hashing pass could drift from
the manifest and would defeat the "scan once" design.

Contract:
  Per-file sha256 -> sorted by path -> Merkle root.

Sorting by relpath (not by hash, not by discovery order) is what makes
the root independent of how/when files were found or passed in.

Pure stdlib. Deterministic. NO network calls anywhere in this module —
the certification service receives only the root + counts, never
content, paths, or per-file hashes.

NOTE: this module is SHIPPED, in the `jidoseal-mcp` distribution (the
MCP server computes the same Merkle root the certificate is bound to).
This file is a copy of the scan engine's attestation module. Everything
here is public.
"""
from __future__ import annotations

import hashlib
from typing import Dict, List


def leaf_hashes(manifest: dict) -> List[str]:
    """Sorted (by relpath) list of per-file hash strings from a manifest.

    Accepts either a full `build_manifest()` result (a dict with a
    "files" key) or the bare `files` sub-dict itself
    (`{relpath: {"hash": "sha256:...", ...}, ...}`).
    """
    files = manifest["files"] if "files" in manifest else manifest
    return [files[rel]["hash"] for rel in sorted(files.keys())]


def _hash_pair(left: str, right: str) -> str:
    """One Merkle internal node: sha256 hex digest of the concatenated children."""
    return hashlib.sha256((left + right).encode("utf-8")).hexdigest()


def merkle_root(hashes: List[str]) -> str:
    """Build a Merkle tree over an already-ordered list of leaf hash strings
    and return the root as a hex sha256 digest.

    An odd node at any level is duplicated (standard Bitcoin-style padding)
    rather than dropped, so no leaf is ever silently excluded from the tree.
    """
    if not hashes:
        # Empty corpus: a fixed, deterministic root distinguishable from any
        # real corpus (whose leaves are always non-empty hash strings).
        return hashlib.sha256(b"").hexdigest()
    level = list(hashes)
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        level = [_hash_pair(level[i], level[i + 1]) for i in range(0, len(level), 2)]
    return level[0]


def manifest_root(manifest: dict) -> str:
    """Sorted-by-path Merkle root computed directly from an okf_manifest.py
    manifest (or its `files` sub-dict). This is the entry point Step 2's
    attestation payload builder will call."""
    return merkle_root(leaf_hashes(manifest))


if __name__ == "__main__":
    demo = {"files": {
        "b.md": {"hash": "sha256:aaaa"},
        "a.md": {"hash": "sha256:bbbb"},
        "c.md": {"hash": "sha256:cccc"},
    }}
    print(manifest_root(demo))
