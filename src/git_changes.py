"""
git_changes.py — what changed in a folder's Markdown since a git commit, and what trust it broke.
================================================================================================
Backs the `jidoseal_changes` tool: an agent (or the person reviewing it) asks "what did I just
edit, and which verified documents does that edit leave unconfirmed?"

THE ONE MODULE HERE THAT STARTS A PROCESS
-----------------------------------------
It runs the local `git` binary — and nothing else — to list changed files and read their
committed versions. It is imported only inside the `jidoseal_changes` handler, so the scan path
never loads it (tests/test_import_graph.py). Every call is `git` with a fixed argument list
built here, no shell, and with the settings below, which keep git on this machine and stop a
repository's own config from running a program:
  * `protocol.allow=never` — git may not use any transport, so it cannot fetch;
  * `GIT_NO_LAZY_FETCH=1` — a partial clone may not fetch a missing object on demand;
  * `core.fsmonitor=false`, `--no-ext-diff`, `--no-textconv` — a repository's config cannot
    name a program for git to run;
  * `GIT_TERMINAL_PROMPT=0`, `GIT_OPTIONAL_LOCKS=0` — no prompt, and no write to the index.
Reads only: it writes nothing, to the folder or to the repository.
"""
from __future__ import annotations

import os
import subprocess
from typing import Any, Dict, List, Optional, Tuple

import okf_trust

GIT_CONFIG = ("-c", "protocol.allow=never", "-c", "core.fsmonitor=false",
              "-c", "core.quotepath=false")
GIT_ENV = {"GIT_NO_LAZY_FETCH": "1", "GIT_TERMINAL_PROMPT": "0", "GIT_OPTIONAL_LOCKS": "0",
           "GIT_PAGER": "cat", "GIT_ASKPASS": "", "SSH_ASKPASS": ""}
MAX_FILES = 500


class ChangesError(Exception):
    pass


def _git(root: str, *args: str, check: bool = True) -> bytes:
    env = dict(os.environ, **GIT_ENV)
    try:
        out = subprocess.run(["git", *GIT_CONFIG, "-C", root, *args], env=env,
                             capture_output=True, timeout=60, check=False)
    except FileNotFoundError:
        raise ChangesError("git is not installed or not on PATH.") from None
    except subprocess.TimeoutExpired:
        raise ChangesError("git took longer than 60 seconds.") from None
    if check and out.returncode != 0:
        msg = out.stderr.decode("utf-8", "replace").strip().splitlines()
        raise ChangesError("git: " + (msg[-1] if msg else f"exit {out.returncode}"))
    return out.stdout


def _hidden(rel: str) -> bool:
    return any(part.startswith(".") for part in rel.split("/"))


def _committed(root: str, sha: str, rel: str) -> Optional[str]:
    raw = _git(root, "show", "--no-textconv", f"{sha}:./{rel}", check=False)
    return raw.decode("utf-8", "replace") if raw else None


def _current(root: str, rel: str) -> Optional[str]:
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        return None
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8", "replace")


def _same(a: Any, b: Any) -> bool:
    return repr(a) == repr(b)


def compare(before: Optional[str], after: Optional[str]) -> Dict[str, Any]:
    """What one edit did to a document's frontmatter, body and trust."""
    fb, pb, bb = okf_trust.parse_frontmatter(before) if before is not None else (None, None, None)
    fa, pa, ba = okf_trust.parse_frontmatter(after) if after is not None else (None, None, None)
    out: Dict[str, Any] = {}
    kb, ka = set(fb or {}), set(fa or {})
    if before is not None and after is not None:
        out["frontmatter"] = {
            "added": sorted(ka - kb),
            "removed": sorted(kb - ka),
            "changed": sorted(k for k in kb & ka if not _same(fb[k], fa[k])),
        }
        out["body_changed"] = (bb or "").strip() != (ba or "").strip()
    flags: List[str] = []
    if after is not None:
        out["trust_now"] = okf_trust.trust(fa, pa)
    if before is not None:
        tb = okf_trust.trust(fb, pb)
        out["trust_before"] = {"verdict": tb["verdict"], "trust_tier": tb["trust_tier"]}
    if before is not None and after is not None:
        verified_before = (fb or {}).get("verified")
        verified_after = (fa or {}).get("verified")
        content_changed = out["body_changed"] or bool(
            set(out["frontmatter"]["changed"] + out["frontmatter"]["added"]
                + out["frontmatter"]["removed"]) - {"verified", "generated"})
        if verified_before and not verified_after:
            flags.append("verified removed: the document no longer records who confirmed it")
        elif verified_before and content_changed and _same(verified_before, verified_after):
            flags.append("verification not renewed: the content changed but `verified` did not, "
                         "so the recorded confirmation predates this text")
        if content_changed and fb and isinstance(fb.get("generated"), dict) and _same(
                (fb or {}).get("generated"), (fa or {}).get("generated")):
            flags.append("generated.at not updated: OKF v0.2 §5.2 uses it to mark the last "
                         "meaningful change")
        if fb and str(fb.get("type", "")).strip() and not str((fa or {}).get("type", "")).strip():
            flags.append("type removed: OKF v0.2 requires a non-empty `type`")
        if fb and fa is None:
            flags.append("frontmatter no longer parses: " + (pa or "unknown problem"))
        if "status" in out["frontmatter"]["changed"] + out["frontmatter"]["added"] + \
                out["frontmatter"]["removed"]:
            flags.append(f"status changed: {(fb or {}).get('status', 'stable')!r} -> "
                         f"{(fa or {}).get('status', 'stable')!r}")
        if "stale_after" in out["frontmatter"]["changed"] + out["frontmatter"]["added"] + \
                out["frontmatter"]["removed"]:
            flags.append(f"stale_after changed: {(fb or {}).get('stale_after')!r} -> "
                         f"{(fa or {}).get('stale_after')!r}")
        tb_v, ta_v = out["trust_before"]["verdict"], out["trust_now"]["verdict"]
        if tb_v == "ok" and ta_v != "ok":
            flags.append(f"was trusted (ok), now {ta_v}")
    elif before is not None and fb and fb.get("verified"):
        flags.append("a verified document was deleted")
    out["flags"] = flags
    return out


def changes(root: str, since: str = "HEAD") -> Dict[str, Any]:
    """Every `*.md` under `root` that differs between commit `since` and the working tree."""
    if not isinstance(since, str) or not since.strip() or since.strip().startswith("-"):
        raise ChangesError("`since` must name a commit, branch or tag (for example HEAD or "
                           "HEAD~3), and may not start with '-'.")
    since = since.strip()
    top = _git(root, "rev-parse", "--show-toplevel", check=False).decode().strip()
    if not top:
        raise ChangesError(f"not inside a git repository: {root}")
    sha = _git(root, "rev-parse", "--verify", "--quiet", "--end-of-options",
               since + "^{commit}", check=False).decode().strip()
    if not sha:
        raise ChangesError(f"no such commit: {since!r}")

    entries: List[Tuple[str, str]] = []
    raw = _git(root, "diff", "--no-ext-diff", "--no-textconv", "--no-renames", "--relative",
               "--name-status", "-z", sha, "--", "*.md").split(b"\0")
    for i in range(0, len(raw) - 1, 2):
        entries.append((raw[i].decode()[:1], raw[i + 1].decode("utf-8", "replace")))
    for p in _git(root, "ls-files", "-z", "--others", "--exclude-standard", "--",
                  "*.md").split(b"\0"):
        if p:
            entries.append(("A", p.decode("utf-8", "replace")))
    entries = sorted({(s, p) for s, p in entries if not _hidden(p)}, key=lambda e: e[1])

    kinds = {"A": "added", "M": "modified", "D": "deleted", "T": "modified"}
    files: List[Dict[str, Any]] = []
    for status, rel in entries[:MAX_FILES]:
        before = None if status == "A" else _committed(root, sha, rel)
        after = None if status == "D" else _current(root, rel)
        files.append({"path": rel, "change": kinds.get(status, status), **compare(before, after)})

    flagged = [f for f in files if f["flags"]]
    return {
        "since": {"ref": since, "commit": sha},
        "compared": "the commit above against the files on disk now (committed or not)",
        "summary": {
            "changed": len(entries),
            "added": sum(f["change"] == "added" for f in files),
            "modified": sum(f["change"] == "modified" for f in files),
            "deleted": sum(f["change"] == "deleted" for f in files),
            "with_flags": len(flagged),
            "verification_not_renewed": sum(
                any(x.startswith("verification not renewed") for x in f["flags"]) for f in files),
            "not_ok_now": sum(f.get("trust_now", {}).get("verdict") not in (None, "ok")
                              for f in files),
        },
        "files": files,
        **({"truncated": f"only the first {MAX_FILES} of {len(entries)} files are listed"}
           if len(entries) > MAX_FILES else {}),
    }
