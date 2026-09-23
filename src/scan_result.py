"""
scan_result.py — one local scan, rendered in the EXACT shape /app/run returns.
==============================================================================
The MCP server's `jidoseal_scan` tool has to hand a host tool the same answer a visitor gets
from the public Self-Check at `/app/run` for the same corpus — same tier, same per-file gap
list, same coverage — or the tool is quietly a different product from the website. This module
is that translation layer, and ONLY that: it runs the existing engine and re-labels its output.

WHAT IT RUNS (nothing new)
--------------------------
`local_runner.run_scan()` — the packaged CLI's own entry point — which runs
`okf_manifest.build_manifest()`, THE certified scoring logic (the same function
the certificate-issuing path calls when a paid certificate is issued). No second scan implementation
exists here: this file computes no tier, reads no frontmatter, hashes no file.

WHAT IT ASSEMBLES (the /app/run envelope)
-----------------------------------------
`AuditResult` — the shape produced by BOTH existing implementations of it: a Python
implementation and the TypeScript one the browser at /app/run actually executes. Those two are
pinned to each other by a parity test. This module is a THIRD surface onto the same contract,
and is pinned the same way: its output is diffed against both for identical input, and if any
of the three drifts, that test fails.

Two envelope fields — `score` and `merkleRoot` — exist on the TypeScript side only (they feed
the certification submission), so they are
computed here too, from the engine's own primitives (`okf_manifest.pct`,
`attestation.manifest_root`), never re-derived. A host that can see the tier must also be able
to start the purchase, and the purchase body carries exactly those two fields.

THE ONE DELIBERATE DIFFERENCE, STATED PLAINLY
---------------------------------------------
/app/run reads a folder the visitor picked in the browser; this reads a folder on disk. So:
  * `skipped` is always `[]` here. It lists bundle entries the browser rejected before
    scoring (not-`.md`, unsafe relative name); a filesystem scan globs `**/*.md` and never
    forms such an entry in the first place.
  * `include_machine=False` (the default) honours the corpus's OWN `.jidoseal/config.yaml`
    conventions, exactly as `jidoseal --root` and the certified issuance path do. For a corpus
    with no config file, nothing is excluded beyond OKF v0.2's two reserved filenames, which
    the browser skips too — i.e. identical. See the `jidoseal` CLI docs.

And one difference that is NOT ours: the Python engine and the browser port have drifted on the
per-gap ANNOTATIONS (`fix` AUTO vs NEEDS-CLIENT, and the suggested `default`/`value`/
`confidence`) for Bronze `type` and the Silver fields — the
parity test excludes exactly this difference, and it predates this server. This module
takes the Python engine's annotations verbatim, because the Python engine is the path a paid
certificate is issued from. Tier, coverage, score, merkle root, per-file tier, present fields,
which fields are missing, and frontmatter_ok all match the browser exactly.

Zero network, and that is a property of the import graph, not a claim: stdlib + `local_runner`
/ `okf_manifest` / `attestation`, all of which are already covered by the engine's static
"imports nothing network-capable" guard. This module is held to the same bar.
"""
from __future__ import annotations

import datetime
import math
import os
import uuid
from typing import Any, Dict, List

from engine_path import ensure_engine_on_path

ensure_engine_on_path()

import attestation  # noqa: E402  — merkle root over the manifest's own per-file hashes
import local_runner  # noqa: E402  — the packaged CLI's run_scan()
import okf_manifest  # noqa: E402  — build_manifest/pct: THE certified scoring logic

TIERS = ("bronze", "silver", "gold")
TIER_ORDER = {"none": 0, "bronze": 1, "silver": 2, "gold": 3}

OKF_SPEC_VERSION = "0.2"
# This surface's identity label, in the same form as the other two implementations' own
# (`okf-manifest/okf-iso-rubric-2026-08-26` and
# `tier1-scoring-ts/okf-iso-rubric-2026-08-26`). The rubric date is
# identical on purpose: the RUBRIC is the same one, only the surface differs.
ENGINE_VERSION = "jidoseal-mcp/okf-iso-rubric-2026-08-26"

# The rubric text /app/run shows the visitor, verbatim from both existing implementations.
RUBRIC = {
    "bronze": "OKF v0.2 as written (populated `type`)",
    "silver": "Bronze + ISO 9001 §7.5.2 fields (title, description, timestamp, owner)",
    "gold": "Silver + ISO 30401 (status + review_policy + reviewed_at + next_review_at on every file)",
}


def corpus_tier(entries: Dict[str, Any]) -> str:
    """Corpus tier = the LOWEST per-file tier. Same rule as the other two
    implementations — a corpus is only as certified as its weakest file."""
    if not entries:
        return "none"
    return min((e["tier"] for e in entries.values()), key=lambda t: TIER_ORDER[t])


def _js_round(x: float) -> int:
    """Round half UP, the way JavaScript's `Math.round` does — NOT Python's `round()`, which
    rounds half to even (`round(34.5) == 34`, `Math.round(34.5) === 35`). `score` is computed
    by `Math.round` in the browser scorer and travels to /api/checkout as an integer; a
    corpus whose three coverages average to exactly x.5 would otherwise be offered a different
    score here than at /app/run for the very same files."""
    return int(math.floor(x + 0.5))


def build_scan_result(root: str, include_machine: bool = False) -> Dict[str, Any]:
    """Run the real local scan of `root` and return it in /app/run's `AuditResult` shape.

    Writes the engine's usual two artifacts under `<root>/.jidoseal/` — `manifest.json` and an
    appended `progress.ndjson` — because that is what `local_runner.run_scan()` does for every
    other surface (CLI, local Web-UI) and what the certification path later binds to. NEVER
    /tmp: scan state belongs to the corpus it describes.

    FAIL LOUD: a missing root raises `FileNotFoundError` out of `run_scan` — never an empty
    manifest a caller could read as "my corpus scored zero files".
    """
    scan = local_runner.run_scan(root, exclude_machine=not include_machine)
    manifest = scan["manifest"]
    entries = manifest["files"]

    tier = corpus_tier(entries)
    coverage = {t: okf_manifest.pct(entries, t) for t in TIERS}
    files: List[Dict[str, Any]] = [
        {
            "name": rel,
            "hash": e["hash"],
            "tier": e["tier"],
            "present": e["present"],
            "missing": e["missing"],
            "frontmatter_ok": e.get("frontmatter_ok", True),
            "language": e["language"],
        }
        # build_manifest iterates `sorted(glob.glob(...))`, so `entries` is already in path
        # order — sorted() again here only to say so explicitly.
        for rel, e in sorted(entries.items())
    ]

    return {
        "audit_id": f"jsa_{uuid.uuid4().hex[:12]}",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "done",
        "okf_spec_version": OKF_SPEC_VERSION,
        "engine_version": ENGINE_VERSION,
        "rubric": dict(RUBRIC),
        "corpus": {"file_count": len(entries), "tier": tier, "coverage": coverage,
                   # In the shared envelope, unlike `config_hash` below: the browser scoring a
                   # browser-side bundle can and does compute both of these itself, so they are
                   # facts all three surfaces can state, and parity can hold them to it.
                   "language": manifest["corpus"]["language"],
                   "i18n_table": manifest["corpus"]["i18n_table"]},
        "files": files,
        # Always empty for a filesystem scan — see this module's docstring.
        "skipped": [],
        "certified_eligible": tier != "none",
        "score": _js_round((coverage["bronze"] + coverage["silver"] + coverage["gold"]) / 3),
        "merkleRoot": attestation.manifest_root(manifest),
        # Not part of AuditResult — MCP-only provenance so a host can show the caller where the
        # scan's own records landed, and so `jidoseal_start_checkout` can prove the numbers it
        # submits came from a scan that really ran on this machine.
        "scan": {
            "root": os.path.abspath(root),
            "run_id": scan["run_id"],
            "manifest_path": scan["manifest_path"],
            "progress_path": scan["progress_path"],
            "include_machine": bool(include_machine),
            # WHICH CORPUS DEFINITION this scan ran under — the
            # digest of the corpus's own .jidoseal/config.yaml, or the explicit "no config file"
            # sentinel. Read off the manifest, so it is THE SAME value the certificate records
            # when this corpus is submitted for certification, whether the submission comes from
            # here or from the website's /app/run flow (both issue through the same
            # build_manifest path). A host tool can show
            # and record it now, and check it against the certificate later.
            #
            # In the MCP-only `scan` block, NOT in the AuditResult envelope, and that is the
            # point rather than a compromise: the envelope is a contract shared with the browser
            # at /app/run, which scores a bundle the visitor picked and can never see a
            # config file. Putting it there would be a parity break with the website for a fact
            # the website's scan cannot know. The parity test relies on it.
            "config_hash": manifest["corpus"]["config_hash"],
        },
    }


def audit_result_only(result: Dict[str, Any]) -> Dict[str, Any]:
    """`result` minus the MCP-only `scan` block — i.e. exactly the `AuditResult` /app/run
    returns. Used by the parity test so the diff is against the shared contract alone."""
    return {k: v for k, v in result.items() if k != "scan"}
