"""
checkout_client.py — the ONE module in this package that can reach the network.
===============================================================================
It does exactly one thing: POST the certification submission to jidoseal.com's real
`/api/checkout` route — the same request the website's "Upgrade to JidoSeal
Certified" button makes — and hand back the Stripe Checkout URL that route returns. It does
NOT take a payment: Stripe hosts the checkout, the customer pays there, and nothing is written
to the certifications table until Stripe confirms the payment server-side
(server-side, after payment). This module cannot charge anyone.

WHY IT IS A SEPARATE FILE
-------------------------
So that "the free scan path imports nothing network-capable" is a structural fact an auditor
can check with a grep, not a promise about which branches run. `jidoseal_mcp.py`, `scan_result.py`
and `offer.py` import no socket, no urllib, no HTTP client of any kind; this file is imported
lazily, inside the `jidoseal_start_checkout` handler, and nowhere else. The same boundary
is held for the scan engine itself, and enforced by a static import check.

WHAT LEAVES THE MACHINE, EXHAUSTIVELY
-------------------------------------
The JSON body built in `submit()` below and nothing else: company, submitterName,
submitterEmail, requestedTier, score, merkleRoot, auditId, belowTier. That is the identical
field set the website's own checkout button sends. No file content, no file names, no
per-file hashes, no paths. See offer.PURCHASE_EGRESS_FIELDS, which is the customer-facing
statement of this same list.
"""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

# Shape checks mirrored from the website's own submission validation so an obviously-bad submission
# fails HERE, locally, instead of travelling to the site to be rejected. This is a pre-filter,
# never a replacement: the server validates every field again on arrival.
_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_MERKLE_RE = re.compile(r"^[0-9a-f]{32,128}$", re.IGNORECASE)

DEFAULT_TIMEOUT_S = 30


class CheckoutError(Exception):
    """The checkout request could not be turned into a real Stripe Checkout URL. Raised with
    the site's own message where there is one — never swallowed into a fake success."""


def _require(value: Any, field: str, max_len: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CheckoutError(f"{field} is required.")
    v = value.strip()
    if len(v) > max_len:
        raise CheckoutError(f"{field} must be at most {max_len} characters.")
    return v


def build_body(company: str, submitter_name: str, submitter_email: str,
               requested_tier: str, score: int, merkle_root: str,
               audit_id: str, below_tier: bool) -> Dict[str, Any]:
    """The exact JSON body /api/checkout expects — same keys, same casing, same types as
    the website's own checkout button. Built as its own function so a test can assert what would
    leave the machine WITHOUT anything leaving it."""
    body = {
        "company": _require(company, "company", 200),
        "submitterName": _require(submitter_name, "submitter_name", 200),
        "submitterEmail": _require(submitter_email, "submitter_email", 320),
        "requestedTier": str(requested_tier).strip().lower(),
        "score": int(score),
        "merkleRoot": str(merkle_root).strip().lower(),
        "auditId": str(audit_id),
        "belowTier": bool(below_tier),
    }
    if not _EMAIL_RE.match(body["submitterEmail"]):
        raise CheckoutError("submitter_email is not a valid email address.")
    if body["requestedTier"] not in ("bronze", "silver", "gold"):
        raise CheckoutError("requested tier must be one of: bronze, silver, gold.")
    if not 0 <= body["score"] <= 100:
        raise CheckoutError("score must be between 0 and 100.")
    if not _MERKLE_RE.match(body["merkleRoot"]):
        raise CheckoutError("merkleRoot is not a valid hex digest.")
    if body["belowTier"] and body["requestedTier"] != "bronze":
        raise CheckoutError("belowTier pricing only exists for the bronze tier.")
    return body


def submit(site_url: str, body: Dict[str, Any],
           timeout: float = DEFAULT_TIMEOUT_S) -> Dict[str, Any]:
    """POST `body` to `<site_url>/api/checkout` and return
    {"url", "site", "endpoint", "sent"} on success.

    FAIL LOUD: a non-JSON reply, a site-reported error, or the configured-stub response (what
    /api/checkout returns when the site's payment provider is not configured) all raise CheckoutError. A host tool
    must never be handed a cheerful "ok" for a checkout that does not exist.
    """
    endpoint = site_url.rstrip("/") + "/api/checkout"
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json",
                 "User-Agent": "jidoseal-mcp"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        detail = _message_from(raw) or f"HTTP {e.code}"
        raise CheckoutError(f"{endpoint} refused the submission: {detail}") from None
    except urllib.error.URLError as e:
        raise CheckoutError(f"could not reach {endpoint}: {e.reason}") from None

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise CheckoutError(f"{endpoint} did not return JSON.") from None

    url = data.get("url") if isinstance(data, dict) else None
    if not url:
        detail = _message_from(raw) or "no checkout URL in the response"
        raise CheckoutError(f"no Stripe Checkout session was created: {detail}")
    return {"url": url, "site": site_url.rstrip("/"), "endpoint": endpoint, "sent": body}


def _message_from(raw: str) -> Optional[str]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    for key in ("error", "note", "detail", "message"):
        if isinstance(data.get(key), str):
            return data[key]
    return None
