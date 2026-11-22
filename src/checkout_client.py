"""
checkout_client.py — the ONE module in this package that can reach the network.
===============================================================================
It does exactly two things. (1) POST the certification submission to jidoseal.com's real
`/api/checkout` route — the same request the website's "Upgrade to JidoSeal
Certified" button makes — and hand back the Stripe Checkout URL that route returns. It does
NOT take a payment: Stripe hosts the checkout, the customer pays there, and nothing is written
to the certifications table until Stripe confirms the payment server-side
(server-side, after payment). This module cannot charge anyone.
(2) POST the free OKF Certified request to `/api/certify-free`: the scan result and the folder
fingerprint, which jidoseal.com answers with 202 and a confirmation email. That route takes no
payment either.

WHY IT IS A SEPARATE FILE
-------------------------
So that "the free scan path imports nothing network-capable" is a structural fact an auditor
can check with a grep, not a promise about which branches run. `jidoseal_mcp.py`, `scan_result.py`
and `offer.py` import no socket, no urllib, no HTTP client of any kind; this file is imported
lazily, inside the `jidoseal_start_checkout` handler, and nowhere else. The same boundary
is held for the scan engine itself, and enforced by a static import check.

WHAT LEAVES THE MACHINE, EXHAUSTIVELY
-------------------------------------
Paid: the JSON body built by `build_body()` and nothing else: company, submitterName,
submitterEmail, requestedTier, score, merkleRoot, filesBelowBronze, filesBelowSilver,
filesBelowGold (counts of files below each tier), auditId (the website's own checkout
button sends the same set; `belowTier` is gone, as Bronze has one price).
Free: the JSON body built by `build_free_body()` and nothing else: company, submitterName,
submitterEmail, score, merkleRoot, okf11Result, fileCount and configSha256. No file content, no file names, no
per-file hashes, no paths. See offer.PURCHASE_EGRESS_FIELDS and offer.FREE_EGRESS_FIELDS,
which are the customer-facing statements of these same lists.
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
# Same pattern as the site's CONFIG_SHA256_RE (lib/certification-validation.ts).
_CONFIG_SHA256_RE = re.compile(
    r"^(?:absent:no-config-file|sha256:[0-9a-f]{64}(?:,sha256:[0-9a-f]{64}){0,5})$")

# The site's own floor for a free certificate (app/api/certify-free/route.ts MIN_FILE_COUNT).
FREE_MIN_FILE_COUNT = 25

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


def _count(files_below: Any, tier: str, key: str) -> int:
    """One folder-grade count for /api/checkout: how many files sit below `tier`. The site
    refuses the checkout (400) without all three, so a missing or malformed count fails HERE."""
    n = files_below.get(tier) if isinstance(files_below, dict) else None
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise CheckoutError(f"the scan result has no valid {key} count.")
    return n


def build_body(company: str, submitter_name: str, submitter_email: str,
               requested_tier: str, score: int, merkle_root: str,
               audit_id: str, files_below: Dict[str, int]) -> Dict[str, Any]:
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
        "filesBelowBronze": _count(files_below, "bronze", "filesBelowBronze"),
        "filesBelowSilver": _count(files_below, "silver", "filesBelowSilver"),
        "filesBelowGold": _count(files_below, "gold", "filesBelowGold"),
        "auditId": str(audit_id),
    }
    if not _EMAIL_RE.match(body["submitterEmail"]):
        raise CheckoutError("submitter_email is not a valid email address.")
    if body["requestedTier"] not in ("bronze", "silver", "gold"):
        raise CheckoutError("requested tier must be one of: bronze, silver, gold.")
    if not 0 <= body["score"] <= 100:
        raise CheckoutError("score must be between 0 and 100.")
    if not _MERKLE_RE.match(body["merkleRoot"]):
        raise CheckoutError("merkleRoot is not a valid hex digest.")
    return body


def build_free_body(company: str, submitter_name: str, submitter_email: str,
                    score: int, merkle_root: str, okf11_result: str, file_count: int,
                    config_sha256: Optional[str] = None) -> Dict[str, Any]:
    """The exact JSON body /api/certify-free expects: company, submitterName, submitterEmail,
    score, merkleRoot, okf11Result, fileCount and, when known, configSha256. Nothing else: no
    file name, no file content. Built as its own function so a test can assert what would leave
    the machine WITHOUT anything leaving it."""
    body: Dict[str, Any] = {
        "company": _require(company, "company", 200),
        "submitterName": _require(submitter_name, "submitter_name", 200),
        "submitterEmail": _require(submitter_email, "submitter_email", 320),
        "score": int(score),
        "merkleRoot": str(merkle_root).strip().lower(),
        "okf11Result": str(okf11_result),
        "fileCount": int(file_count),
    }
    if config_sha256:
        body["configSha256"] = str(config_sha256).strip()
    if not _EMAIL_RE.match(body["submitterEmail"]):
        raise CheckoutError("submitter_email is not a valid email address.")
    if not 0 <= body["score"] <= 100:
        raise CheckoutError("score must be between 0 and 100.")
    if not _MERKLE_RE.match(body["merkleRoot"]):
        raise CheckoutError("merkleRoot is not a valid hex digest.")
    if body["okf11Result"] != "3/3":
        raise CheckoutError("okf11Result must be 3/3: all three OKF section 11 rules must pass.")
    if body["fileCount"] < FREE_MIN_FILE_COUNT:
        raise CheckoutError(f"A free certificate needs {FREE_MIN_FILE_COUNT} or more files; "
                            f"this folder has {body['fileCount']}.")
    if "configSha256" in body and not _CONFIG_SHA256_RE.match(body["configSha256"]):
        raise CheckoutError("configSha256 is not a valid digest.")
    return body


def _post(endpoint: str, body: Dict[str, Any], timeout: float) -> Any:
    """POST `body` as JSON and return the parsed JSON reply, or raise CheckoutError with the
    site's own message. HTTP 2xx only: urlopen raises HTTPError for the rest."""
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
        return json.loads(raw), raw
    except json.JSONDecodeError:
        raise CheckoutError(f"{endpoint} did not return JSON.") from None


def submit(site_url: str, body: Dict[str, Any],
           timeout: float = DEFAULT_TIMEOUT_S) -> Dict[str, Any]:
    """POST `body` to `<site_url>/api/checkout` and return
    {"url", "site", "endpoint", "sent"} on success.

    FAIL LOUD: a non-JSON reply, a site-reported error, or the configured-stub response (what
    /api/checkout returns when the site's payment provider is not configured) all raise CheckoutError. A host tool
    must never be handed a cheerful "ok" for a checkout that does not exist.
    """
    endpoint = site_url.rstrip("/") + "/api/checkout"
    data, raw = _post(endpoint, body, timeout)
    url = data.get("url") if isinstance(data, dict) else None
    if not url:
        detail = _message_from(raw) or "no checkout URL in the response"
        raise CheckoutError(f"no Stripe Checkout session was created: {detail}")
    return {"url": url, "site": site_url.rstrip("/"), "endpoint": endpoint, "sent": body}


def submit_free(site_url: str, body: Dict[str, Any],
                timeout: float = DEFAULT_TIMEOUT_S) -> Dict[str, Any]:
    """POST `body` to `<site_url>/api/certify-free`. The site answers 202
    {id, status: "pending", message} and emails a confirmation link (valid 72 hours); errors
    are {error} with 400, 409, 429 or 502, raised here as CheckoutError with the site's text.
    Returns {"id", "status", "message", "site", "endpoint", "sent"}."""
    endpoint = site_url.rstrip("/") + "/api/certify-free"
    data, raw = _post(endpoint, body, timeout)
    cert_id = data.get("id") if isinstance(data, dict) else None
    if not cert_id or data.get("status") != "pending":
        detail = _message_from(raw) or "no pending request id in the response"
        raise CheckoutError(f"no free certificate request was created: {detail}")
    return {"id": cert_id, "status": data["status"], "message": data.get("message"),
            "site": site_url.rstrip("/"), "endpoint": endpoint, "sent": body}


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
