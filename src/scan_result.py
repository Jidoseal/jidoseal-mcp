"""
scan_result.py — one local scan, rendered in the EXACT shape /app/run returns.
==============================================================================
The MCP server's `jidoseal_scan` tool has to hand a host tool the same answer a visitor gets
from the public Self-Check at `/app/run` for the same corpus — same tier, same per-file gap
list, same coverage — or the tool is quietly a different product from the website. This module
is that translation layer, and ONLY that: it runs the existing engine and re-labels its output.

CRITERIA: the scan runs under OKF Folder Criteria v1.0.0 (engine 0.2.0), the live ladder: OKF
Certified (free), Bronze, Silver, Gold. `run_scan` is called with criteria "1.0.0" explicitly,
because the library default is still "0.9.2" (the pre-0.2.0 output).

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
taken from the engine's own v1.0.0 folder result (`score`) and primitives (
`attestation.manifest_root`), never re-derived. A host that can see the tier must also be able
to start the purchase, and the purchase body carries exactly those two fields.

THE ONE DELIBERATE DIFFERENCE, STATED PLAINLY
---------------------------------------------
/app/run reads a folder the visitor picked in the browser; this reads a folder on disk. So:
  * `skipped` is always `[]` here. It lists bundle entries the browser rejected before
    scoring (not-`.md`, unsafe relative name); a filesystem scan reads `**/*.md` and never
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
import os
import uuid
from typing import Any, Dict, List

from engine_path import ensure_engine_on_path

ensure_engine_on_path()

import attestation  # noqa: E402  — merkle root over the manifest's own per-file hashes
import local_runner  # noqa: E402  — the packaged CLI's run_scan()
import okf_manifest  # noqa: E402  — build_manifest/pct: THE certified scoring logic

# OKF Folder Criteria v1.0.0 (engine 0.2.0). Ordered lowest to highest; "none" is below OKF Certified.
TIERS = ("okf-certified", "bronze", "silver", "gold")
TIER_ORDER = {"none": 0, "okf-certified": 1, "bronze": 2, "silver": 3, "gold": 4}
CRITERIA_VERSION = "1.0.0"

OKF_SPEC_VERSION = "0.2"
# What this server tells a user about a scan's network use: stated as JidoSeal's own claim,
# because the engine that does the scan is proprietary. The engine's own absolute sentence
# (local_runner.EGRESS_DISCLOSURE, qualified the same way since engine 0.1.4) is not shown by
# this server, which states the claim once, here, in its own words.
SCAN_EGRESS_CLAIM = (
    "JidoSeal states that a scan makes no network connection and sends no file, file name or "
    "file content anywhere. The scan engine is proprietary, so this is JidoSeal's own claim, "
    "not an independent audit; the jidoseal-mcp README and tests show how to check it."
)
# This surface's identity label, in the same form as the other two implementations' own
# (`okf-manifest/okf-criteria-1.0.0` and `tier1-scoring-ts/okf-criteria-1.0.0`).
ENGINE_VERSION = "jidoseal-mcp/okf-criteria-1.0.0"

# The tier text /app/run shows the visitor (approved site wording, 2026-11-21).
RUBRIC = {
    "okf-certified": "OKF Certified (free): every file passes the three OKF v0.2 §11 conformance rules.",
    "bronze": "Bronze: adds a title, description, date and owner on every file.",
    "silver": "Silver: adds a status, a review policy and the dates of its last and next review on every file.",
    "gold": "Gold: adds AI-provenance fields: sources, AI involvement and licence.",
}

# The engine's per-file `missing` is keyed by the criteria v0.9.2 tiers (bronze = `type`,
# silver = title/description/timestamp/owner, gold = the four review fields). Under v1.0.0 each
# gap list blocks the tier one step up: v0.9.2 bronze -> okf-certified, silver -> bronze,
# gold -> silver. The engine writes no gap list for v1.0.0 Gold (the AI-provenance checks).
_MISSING_KEY_V092_TO_V1 = {"bronze": "okf-certified", "silver": "bronze", "gold": "silver"}


def _missing_v1(missing: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {t: [] for t in TIERS}
    for old, new in _MISSING_KEY_V092_TO_V1.items():
        out[new] = list(missing.get(old, []))
    return out


def build_scan_result(root: str, include_machine: bool = False) -> Dict[str, Any]:
    """Run the real local scan of `root` and return it in /app/run's `AuditResult` shape.

    Writes the engine's usual two artifacts under `<root>/.jidoseal/` — `manifest.json` and an
    appended `progress.ndjson` — because that is what `local_runner.run_scan()` does for every
    other surface (CLI, local Web-UI) and what the certification path later binds to. NEVER
    /tmp: scan state belongs to the corpus it describes.

    FAIL LOUD: a missing root raises `FileNotFoundError` out of `run_scan` — never an empty
    manifest a caller could read as "my corpus scored zero files".
    """
    scan = local_runner.run_scan(root, exclude_machine=not include_machine,
                                  criteria=okf_manifest.CRITERIA_V1)
    manifest = scan["manifest"]
    entries = manifest["files"]

    # The engine's own v1.0.0 folder result: grade (lowest file grade, `none` if the third OKF
    # section 11 rule fails), coverage per tier, and the 0-100 score. Nothing is recomputed here.
    corpus_v1 = manifest["corpus"]
    tier = corpus_v1["grade"]
    coverage = dict(corpus_v1["coverage"])
    okf11 = manifest["corpus"]["okf11"]
    grades = [e["grade"] for e in entries.values()]
    files: List[Dict[str, Any]] = [
        {
            "name": rel,
            "hash": e["hash"],
            "tier": e["grade"],
            "present": e["present"],
            "missing": _missing_v1(e["missing"]),
            "frontmatter_ok": e.get("frontmatter_ok", True),
            "language": e["language"],
        }
        # build_manifest returns its files in sorted path order, so `entries` is already in
        # path order — sorted() again here only to say so explicitly.
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
                   "criteria_version": corpus_v1["criteria_version"],
                   # In the shared envelope, unlike `config_hash` below: the browser scoring a
                   # browser-side bundle can and does compute both of these itself, so they are
                   # facts all three surfaces can state, and parity can hold them to it.
                   "language": manifest["corpus"]["language"],
                   "i18n_table": manifest["corpus"]["i18n_table"]},
        "files": files,
        # Always empty for a filesystem scan — see this module's docstring.
        "skipped": [],
        "certified_eligible": tier != "none",
        "score": corpus_v1["score"],
        # "3/3" when every file passes the three OKF v0.2 section 11 rules: the free OKF
        # Certified request needs exactly that string.
        "okf11Result": f"{okf11['rules_passed']}/3",
        # Files below each tier: the folder-grade counts /api/checkout requires (since 0.3.1).
        "filesBelow": {t: sum(1 for g in grades if TIER_ORDER[g] < TIER_ORDER[t]) for t in TIERS},
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
