#!/usr/bin/env python3
"""
jidoseal_mcp.py — JidoSeal's inbound MCP server (JSON-RPC 2.0 over stdio).
==========================================================================
Lets a host tool (Claude Code, Cursor, an OpenKnowledge workflow, any MCP client) run
JidoSeal's free local scan and reach the paid certification from inside its own environment,
without the customer leaving the host and without their files leaving the machine.

It exposes the website's model, unchanged:
  1. `jidoseal_scan`                  — the free Self-Check. Returns the corpus's tier
                                        (Bronze/Silver/Gold), the per-file list of missing
                                        fields, and coverage — the same answer /app/run gives
                                        for the same corpus (scan_result.py explains how that
                                        identity is held). 100% local, zero content egress.
  2. `jidoseal_certification_offer`   — what certification would cost for this corpus and why,
                                        what it includes, and exactly which facts a purchase
                                        would send. Still 100% local: it computes an offer, it
                                        does not start one.
  3. `jidoseal_start_checkout`        — creates a real Stripe Checkout session on jidoseal.com
                                        and returns its URL for the customer to open. THE ONLY
                                        tool here that touches the network, and it still takes
                                        no payment: Stripe does that, on jidoseal.com, only
                                        when the customer completes the checkout themselves.

=================================================================================================
ARM'S LENGTH — WHY THIS IS A SEPARATE PROCESS SPEAKING A PUBLIC PROTOCOL
=================================================================================================
Hosts that call this server may be GPL-3.0 (OpenKnowledge is). So the boundary
between them is a process boundary and a published wire protocol: JSON-RPC 2.0 over stdio, per
the Model Context Protocol spec. This package contains no OpenKnowledge source, vendors
none, links none, and imports none — the dependency in both directions is on the PROTOCOL, and
the only data crossing is MCP's own JSON envelopes plus JidoSeal's own scan result. No host's
internal data structures enter this process and none of ours leave it. That is the FSF's own
arm's-length test for separate works, and it is why this file speaks JSON and not Python.

Nothing here is specific to any one host. The same server serves Claude Code, Cursor and an
OpenKnowledge workflow identically — see README.md.

=================================================================================================
STDOUT IS THE WIRE
=================================================================================================
On stdio transport, stdout carries the JSON-RPC stream and NOTHING else: one stray `print()`
from any imported module corrupts the session. So `main()` takes the real stdout for framing
and rebinds `sys.stdout` to stderr before a single engine module is used (the engine's own
prints live in `__main__`/CLI paths, but "lives in a branch we don't call" is not a guarantee —
this is). Diagnostics go to stderr, where MCP hosts already collect them.

=================================================================================================
ZERO NETWORK ON THE FREE PATH — A PROPERTY OF THE IMPORT GRAPH
=================================================================================================
This module imports stdlib (json/os/sys/typing) plus `scan_result` and `offer`, and neither
they nor anything they pull in (`local_runner`, `okf_manifest`, `attestation`, and the engine
modules those use) imports socket, urllib, or any HTTP client. `checkout_client` — the one
module that does — is imported INSIDE the `jidoseal_start_checkout` handler, so it is not even
loaded during a scan. Both halves are checked by static AST inspection, and a real scan
run with sockets disabled proves the executed path opens no socket and resolves no hostname either.
"""
from __future__ import annotations

import json
import os
import sys
from typing import Any, Callable, Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import offer as offer_mod  # noqa: E402
import scan_result  # noqa: E402
from engine_path import ensure_engine_on_path  # noqa: E402

ensure_engine_on_path()

import local_runner  # noqa: E402  — EGRESS_DISCLOSURE: the ONE sentence, never paraphrased

SERVER_NAME = "jidoseal"
# Tracks the engine/CLI version (local_runner.VERSION) it scans with, with this surface's own
# suffix: the scan a host gets is the CLI's scan, so a bug report naming a version can be
# resolved against one number.
SERVER_VERSION = f"{local_runner.VERSION}+mcp.1"

# The MCP revisions this server implements. `initialize` echoes the client's own when we know
# it (the spec's negotiation rule) and otherwise offers the newest we speak.
SUPPORTED_PROTOCOL_VERSIONS = ("2025-06-18", "2025-03-26", "2024-11-05")
LATEST_PROTOCOL_VERSION = SUPPORTED_PROTOCOL_VERSIONS[0]

# Copy-truth, stated once and reused in every tool description. It says what this code path
# actually does — the scan engine imports nothing network-capable — and claims nothing else:
# not that the client is open source, and nothing about the paid path, which is a different
# code path with its own, separately stated, egress list.
EGRESS_LINE = local_runner.EGRESS_DISCLOSURE.replace("\n", " ")

TOOLS: List[Dict[str, Any]] = [
    {
        "name": "jidoseal_scan",
        "title": "JidoSeal Self-Check (free, local)",
        "description": (
            "Run JidoSeal's free Self-Check over a folder of Markdown documents on THIS "
            "machine and return its OKF/ISO certification tier — Bronze, Silver or Gold — "
            "plus, for every file, which fields are missing for the next tier, and the "
            "corpus's coverage against each tier. Same rubric, and the same tier, coverage and "
            "per-file gap list as the Self-Check at jidoseal.com/app/run for the same folder. "
            "Bronze = OKF v0.2 as written (a populated `type`); Silver = Bronze + ISO 9001 "
            "§7.5.2 fields (title, description, timestamp, owner); Gold = Silver + ISO 30401 "
            "(status, review_policy, reviewed_at, next_review_at). Each gap is marked AUTO "
            "(JidoSeal can propose the value) or NEEDS-CLIENT (only the owner can answer it), "
            "so the caller can close them for free before paying for anything. "
            "Free and unlimited. " + EGRESS_LINE + " "
            "Writes the scan's own records to <root>/.jidoseal/ (manifest.json and an "
            "appended progress.ndjson) and nowhere else."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "root": {
                    "type": "string",
                    "description": "Absolute path of the folder to scan. Every *.md file under "
                                   "it is scanned, recursively.",
                },
                "include_machine": {
                    "type": "boolean",
                    "default": False,
                    "description": "Scan every Markdown file, ignoring this corpus's own "
                                   "machine/transient excludes from .jidoseal/config.yaml. "
                                   "Leave false: the certified path scans without it.",
                },
            },
            "required": ["root"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": False, "destructiveHint": False, "openWorldHint": False},
    },
    {
        "name": "jidoseal_certification_offer",
        "title": "What JidoSeal certification would cost for this corpus",
        "description": (
            "Scan a folder locally and return the paid-certification offer for it: the tier it "
            "qualifies for, the real price for that tier and why that price applies, what the "
            "certificate includes (a signed certificate bound to a Merkle root of the corpus, "
            "a verifiable badge, a public verification page, a registry listing), and the "
            "exact list of facts a purchase would send to jidoseal.com. Charges nothing, "
            "starts nothing, and sends nothing — it is a local computation about a purchase "
            "the customer has not made. " + EGRESS_LINE
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "root": {"type": "string", "description": "Absolute path of the folder."},
                "include_machine": {"type": "boolean", "default": False},
            },
            "required": ["root"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": False, "destructiveHint": False, "openWorldHint": False},
    },
    {
        "name": "jidoseal_start_checkout",
        "title": "Start the JidoSeal certification purchase (returns a Stripe Checkout link)",
        "description": (
            "Ask jidoseal.com to create a Stripe Checkout session for certifying this corpus, "
            "and return the checkout URL for the customer to open and pay. Call it only with "
            "the customer's explicit go-ahead: it is the purchase step. It does NOT take a "
            "payment — this server never sees a card, Stripe hosts the checkout, and nothing "
            "is charged or issued unless the customer completes it themselves. "
            "This is the one JidoSeal tool that contacts the network, and it sends only: "
            "company, name and email as typed by the customer, the tier, a 0-100 score, the "
            "corpus's Merkle root, the local scan's id, and which Bronze price applies. No "
            "file contents, no file names, no per-file hashes, no paths. The tier, score and "
            "Merkle root are taken from a fresh local scan run here — never from the caller."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "root": {"type": "string", "description": "Absolute path of the folder to certify."},
                "company": {"type": "string", "description": "The customer's company name, as it should appear on the certificate."},
                "submitter_name": {"type": "string", "description": "The person submitting, as typed by them."},
                "submitter_email": {"type": "string", "description": "Where the certificate and receipt go."},
                "include_machine": {"type": "boolean", "default": False},
            },
            "required": ["root", "company", "submitter_name", "submitter_email"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": False, "destructiveHint": False, "openWorldHint": True},
    },
]


# ---------------------------------------------------------------------------------------------
# Tool handlers. Each returns a JSON-serialisable dict; raising ToolError turns into an
# `isError: true` tool result (a tool that failed), never a JSON-RPC error (a protocol that
# failed) — the distinction MCP draws so a model can see and react to the failure.
# ---------------------------------------------------------------------------------------------
class ToolError(Exception):
    pass


def _root_arg(args: Dict[str, Any]) -> str:
    root = args.get("root")
    if not isinstance(root, str) or not root.strip():
        raise ToolError("`root` is required: the absolute path of the folder to scan.")
    root = os.path.expanduser(root.strip())
    if not os.path.isdir(root):
        raise ToolError(f"scan root does not exist (or is not a directory): {root}")
    return root


def _scan(args: Dict[str, Any]) -> Dict[str, Any]:
    return scan_result.build_scan_result(_root_arg(args),
                                         include_machine=bool(args.get("include_machine", False)))


def tool_jidoseal_scan(args: Dict[str, Any]) -> Dict[str, Any]:
    result = _scan(args)
    result["egress"] = local_runner.EGRESS_DISCLOSURE
    return result


def tool_jidoseal_certification_offer(args: Dict[str, Any]) -> Dict[str, Any]:
    root = _root_arg(args)
    result = scan_result.build_scan_result(
        root, include_machine=bool(args.get("include_machine", False)))
    return offer_mod.build_offer(result, root)


def tool_jidoseal_start_checkout(args: Dict[str, Any]) -> Dict[str, Any]:
    # Imported HERE, and only here: the network-capable module must not be on the scan path's
    # import graph. See this file's header.
    import checkout_client

    root = _root_arg(args)
    result = scan_result.build_scan_result(
        root, include_machine=bool(args.get("include_machine", False)))
    tier = result["corpus"]["tier"]
    if not result["certified_eligible"]:
        raise ToolError(
            "This corpus is not at Bronze yet, so there is nothing to certify and no checkout "
            "to start. Run jidoseal_scan, close the missing fields it lists (free, on this "
            "machine), and try again."
        )

    below = offer_mod.first_scan_was_below_bronze(root) if tier == "bronze" else False
    try:
        body = checkout_client.build_body(
            company=args.get("company", ""),
            submitter_name=args.get("submitter_name", ""),
            submitter_email=args.get("submitter_email", ""),
            requested_tier=tier,
            score=result["score"],
            merkle_root=result["merkleRoot"],
            audit_id=result["audit_id"],
            below_tier=bool(below) if below is not None else True,
        )
        out = checkout_client.submit(offer_mod.site_url(), body)
    except checkout_client.CheckoutError as e:
        raise ToolError(str(e)) from None

    price = offer_mod.price_for(tier, below)
    return {
        "checkout_url": out["url"],
        "instruction": "Open this link to pay. JidoSeal never sees the card — Stripe hosts the "
                       "checkout. Nothing is charged, and no certificate is issued, unless the "
                       "customer completes it there.",
        "tier": tier,
        "price": price,
        "corpus": {
            "root": os.path.abspath(root),
            "file_count": result["corpus"]["file_count"],
            "score": result["score"],
            "merkle_root": result["merkleRoot"],
            "audit_id": result["audit_id"],
            # The corpus definition this purchase would certify under — the same digest the
            # certificate records Returned so the caller can
            # record it alongside the checkout it just started; it is NOT part of what the
            # checkout body sends, because the certificate's copy is computed server-side from
            # the corpus itself at issuance, never taken from a caller's word.
            "config_hash": result["scan"]["config_hash"],
        },
        "sent_to_site": out["sent"],
        "not_sent": offer_mod.PURCHASE_EGRESS_NOT_SENT,
        "endpoint": out["endpoint"],
    }


HANDLERS: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
    "jidoseal_scan": tool_jidoseal_scan,
    "jidoseal_certification_offer": tool_jidoseal_certification_offer,
    "jidoseal_start_checkout": tool_jidoseal_start_checkout,
}


# ---------------------------------------------------------------------------------------------
# JSON-RPC 2.0 / MCP plumbing.
# ---------------------------------------------------------------------------------------------
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603
PARSE_ERROR = -32700


def _result(msg_id: Any, result: Dict[str, Any]) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": msg_id, "result": result}


def _error(msg_id: Any, code: int, message: str) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}


def _tool_result(payload: Dict[str, Any], is_error: bool = False) -> Dict[str, Any]:
    """MCP tool result. The payload travels as pretty-printed JSON in a single text block —
    readable by a model, parseable by a program. `structuredContent` carries the same object
    for clients that prefer it; no `outputSchema` is declared, so no client is obliged to
    validate it against a shape this server would then have to keep in two places."""
    out: Dict[str, Any] = {
        "content": [{"type": "text", "text": json.dumps(payload, indent=2, sort_keys=False)}],
        "isError": is_error,
    }
    if not is_error:
        out["structuredContent"] = payload
    return out


def handle_message(msg: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """One JSON-RPC message in, at most one response out. Returns None for notifications
    (no `id`), which per the spec are never answered."""
    method = msg.get("method")
    msg_id = msg.get("id")
    is_notification = "id" not in msg
    params = msg.get("params") or {}

    if is_notification:
        return None

    if method == "initialize":
        asked = params.get("protocolVersion")
        version = asked if asked in SUPPORTED_PROTOCOL_VERSIONS else LATEST_PROTOCOL_VERSION
        return _result(msg_id, {
            "protocolVersion": version,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": SERVER_NAME, "title": "JidoSeal", "version": SERVER_VERSION},
            "instructions": (
                "JidoSeal certifies a Markdown knowledge base against OKF v0.2 + ISO 9001 "
                "§7.5.2 + ISO 30401. Start with jidoseal_scan on the folder: it runs entirely "
                "on this machine, costs nothing, and returns the tier plus the missing fields "
                "per file so they can be fixed for free. jidoseal_certification_offer then "
                "prices the optional certificate, and jidoseal_start_checkout returns a Stripe "
                "link for the customer to pay — only ever with their explicit go-ahead."
            ),
        })

    if method == "ping":
        return _result(msg_id, {})

    if method == "tools/list":
        return _result(msg_id, {"tools": TOOLS})

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        handler = HANDLERS.get(name)
        if handler is None:
            return _error(msg_id, INVALID_PARAMS, f"unknown tool: {name!r}")
        if not isinstance(args, dict):
            return _error(msg_id, INVALID_PARAMS, "`arguments` must be an object")
        try:
            return _result(msg_id, _tool_result(handler(args)))
        except ToolError as e:
            return _result(msg_id, _tool_result({"error": str(e)}, is_error=True))
        except Exception as e:  # a real defect: report it AS a tool failure, never silently
            return _result(msg_id, _tool_result(
                {"error": f"{type(e).__name__}: {e}"}, is_error=True))

    return _error(msg_id, METHOD_NOT_FOUND, f"method not found: {method!r}")


def serve(stdin, stdout) -> None:
    """Newline-delimited JSON-RPC over the given binary streams — MCP's stdio framing."""
    for raw in stdin:
        line = raw.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            _write(stdout, _error(None, PARSE_ERROR, "invalid JSON"))
            continue
        messages = msg if isinstance(msg, list) else [msg]
        for one in messages:
            if not isinstance(one, dict):
                _write(stdout, _error(None, INVALID_PARAMS, "message must be an object"))
                continue
            try:
                response = handle_message(one)
            except Exception as e:  # never let one bad message end the session
                response = _error(one.get("id"), INTERNAL_ERROR, f"{type(e).__name__}: {e}")
            if response is not None:
                _write(stdout, response)


def _write(stdout, payload: Dict[str, Any]) -> None:
    stdout.write((json.dumps(payload) + "\n").encode("utf-8"))
    stdout.flush()


def main() -> None:
    # Take the real stdout for the wire, then point sys.stdout at stderr so that nothing —
    # not this module, not the engine, not a stray debug print — can write to the JSON-RPC
    # stream by accident. See this file's header.
    wire_out = sys.stdout.buffer
    sys.stdout = sys.stderr
    print(f"{SERVER_NAME} MCP server {SERVER_VERSION} — stdio. {EGRESS_LINE}", file=sys.stderr)
    serve(sys.stdin.buffer, wire_out)


if __name__ == "__main__":
    main()
