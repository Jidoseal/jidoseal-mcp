"""
offer.py — the paid certification, described exactly as the website describes it.
=================================================================================
The free scan is one half of the product; this is the other half, and a host tool that can
only see the first half is showing the customer half a product. `jidoseal_certification_offer`
answers, entirely locally: what tier this corpus is at, what certification costs for that tier
and WHY that price, what the customer gets, where the purchase happens, and — precisely —
which facts would leave the machine if they went ahead.

NOTHING HERE TOUCHES THE NETWORK. This module computes an offer; it does not start a purchase.
That separation is deliberate and is a tool boundary, not a comment: `checkout_client.py` is
the one module in this package that can open a socket, and it is imported ONLY inside
`jidoseal_start_checkout`'s handler. So "the free path is 100% local" is a property of the
import graph on every other path, held by a static import check.

PRICING IS QUOTED, NOT INVENTED
-------------------------------
Every number and every qualifying clause below is the site's own published copy
(jidoseal.com's pricing section: the per-grade table and the two price cards), reproduced
verbatim so a host tool can never quote a price the customer would not actually be charged:
    Bronze  $149 — if the folder met Bronze on its first scan
            $199 — if JidoSeal's fixes got it there
    Silver  $349
    Gold    $599
    Self-Check — free (the scan and the fixes)
One flat price per grade, however many files; there is no file-count tiering. The scan and the
fixes are free; the certificate is the only thing that costs money. Which Bronze price applies
is decided by the website's own rule,
reproduced in `first_scan_was_below_bronze()` below from the corpus's OWN scan history rather
than from anything the caller asserts.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from engine_path import ensure_engine_on_path

ensure_engine_on_path()

import local_runner  # noqa: E402  — progress_path(): the corpus's own append-only scan history

# The public site. Overridable so a test (or a self-hosted instance) can point the checkout
# tool at a loopback address instead; it is NEVER read on the scan path.
DEFAULT_SITE_URL = "https://jidoseal.com"


def site_url() -> str:
    return (os.environ.get("JIDOSEAL_SITE_URL") or DEFAULT_SITE_URL).rstrip("/")


# Verbatim from jidoseal.com — tier, what the tier means, the price(s), and the condition
# attached to each price. `alt` exists only where the site itself publishes two prices.
PRICING = {
    "bronze": {
        "tier": "Bronze",
        "rubric": "OKF v0.2, as written",
        "price_usd": 149,
        "price": "$149",
        "price_note": "if the folder met Bronze on its first scan",
        "alt_price_usd": 199,
        "alt_price": "$199",
        "alt_price_note": "if JidoSeal's fixes got it there",
    },
    "silver": {
        "tier": "Silver",
        "rubric": "+ fields that evidence ISO 9001 §7.5.2",
        "price_usd": 349,
        "price": "$349",
        "price_note": "one flat price per grade, however many files",
    },
    "gold": {
        "tier": "Gold",
        "rubric": "+ fields that evidence ISO 30401",
        "price_usd": 599,
        "price": "$599",
        "price_note": "one flat price per grade, however many files",
    },
}

SELF_CHECK_PRICE = "Free"

PRICING_NOTE = (
    "One flat price per grade, however many files. You only pay once your folder has reached "
    "the grade, so the free scan tells you exactly where you stand first. Scanning and fixing "
    "stay free whether or not you buy a certificate. The certificate is the only thing that "
    "costs money."
)

# What the paid product is, verbatim from the site's JidoSeal Certified card.
CERTIFICATION_INCLUDES = [
    "A dated certificate for the grade your folder reached",
    "A public verification page anyone can check",
    "A badge that links to it, and a listing in the public registry",
    "A printable certificate",
    "Signed off by a person at JidoSeal, from the grade, score and fingerprint only",
    "Valid for one year",
]

# The complete list of what a purchase sends to jidoseal.com — aggregate facts and the contact
# details the customer types, and nothing else. Stated field by field because "zero content
# egress" is a claim about the FREE path, and the paid path deserves the same precision rather
# than a reassuring summary.
PURCHASE_EGRESS_FIELDS = [
    "company (typed by the customer)",
    "submitterName (typed by the customer)",
    "submitterEmail (typed by the customer)",
    "requestedTier — one of bronze/silver/gold",
    "score — a single integer 0-100",
    "merkleRoot — one sha256 hex digest over the corpus's per-file hashes",
    "auditId — the local scan's own random id",
    "belowTier — one boolean, which Bronze price applies",
]

PURCHASE_EGRESS_NOT_SENT = (
    "No file contents, no file names, no per-file hashes, no directory paths, and no part of "
    "the corpus itself are sent. The merkle root is a one-way digest: it binds the certificate "
    "to this exact corpus, and nothing can be read back out of it."
)


def first_scan_was_below_bronze(root: str) -> Optional[bool]:
    """Was this corpus below Bronze the FIRST time it was scanned?

    That is the question the website answers in the
    browser (a fix was applied while the corpus was not yet `certified_eligible`), and it is
    what decides the Bronze price. The browser knows it from session state; a host tool calling
    over MCP has no session — but the corpus does: `<root>/.jidoseal/progress.ndjson` is an
    append-only history, and every scan's `done` event carries its Bronze coverage. A corpus
    whose EARLIEST recorded scan already had 100% Bronze coverage was at Bronze before any fix
    (corpus tier = the lowest per-file tier, so `tier != "none"` is exactly `bronze == 100`).

    Returns True (was below Bronze), False (was already at Bronze), or None when the history
    cannot be read at all — in which case callers quote the HIGHER price rather than guess low.
    """
    path = local_runner.progress_path(root)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if ev.get("phase") == "done" and ev.get("op") == "scan":
                    cov = ev.get("coverage") or {}
                    bronze = cov.get("bronze")
                    if isinstance(bronze, (int, float)):
                        return bronze < 100
    except OSError:
        return None
    return None


def price_for(tier: str, below_tier: Optional[bool]) -> Dict[str, Any]:
    """The price the customer would actually be charged for `tier`, and why.

    `below_tier` only ever changes the Bronze price (the site restricts the
    below-tier product to Bronze); unknown (None) quotes the higher Bronze price, because a
    quote that turns out low at the checkout screen is the one error mode with a cost attached.
    """
    entry = PRICING[tier]
    if tier != "bronze":
        return {
            "amount_usd": entry["price_usd"],
            "display": entry["price"],
            "why": entry["price_note"],
            "below_tier": False,
        }
    if below_tier is False:
        return {
            "amount_usd": entry["price_usd"],
            "display": entry["price"],
            "why": "This corpus was already at Bronze on its first scan, before any fix was "
                   "applied, so certifying it is $149.",
            "below_tier": False,
        }
    unknown = below_tier is None
    return {
        "amount_usd": entry["alt_price_usd"],
        "display": entry["alt_price"],
        "why": (
            "No earlier scan of this corpus is on record, so the $199 price is quoted; if it "
            "was already at Bronze on its first scan the price is $149."
            if unknown else
            "This corpus needed corrections before it reached Bronze, so certifying it is $199."
        ),
        "below_tier": True,
        "price_unconfirmed": unknown,
    }


def gap_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    """How many field gaps stand between this corpus and each tier, and how many of those the
    customer has to answer themselves (`NEEDS-CLIENT`) rather than accept a proposed value for
    (`AUTO`). Counts only — the per-file list is already in the scan result, and this exists so
    a host can say "7 gaps left" without walking it."""
    out: Dict[str, Any] = {}
    for tier in ("bronze", "silver", "gold"):
        gaps = [g for f in result["files"] for g in f["missing"].get(tier, [])]
        out[tier] = {
            "total": len(gaps),
            "auto": sum(1 for g in gaps if g.get("fix") == "AUTO"),
            "needs_client": sum(1 for g in gaps if g.get("fix") == "NEEDS-CLIENT"),
            "files_affected": sum(1 for f in result["files"] if f["missing"].get(tier)),
        }
    out["unreadable_frontmatter"] = [
        f["name"] for f in result["files"] if not f.get("frontmatter_ok", True)
    ]
    return out


def build_offer(result: Dict[str, Any], root: str) -> Dict[str, Any]:
    """The certification offer for an already-scanned corpus. Pure local computation over
    `result` (a scan_result.build_scan_result() return) — no network, no payment, no purchase.
    """
    tier = result["corpus"]["tier"]
    eligible = result["certified_eligible"]
    below = first_scan_was_below_bronze(root) if tier == "bronze" else None
    site = site_url()

    offer: Dict[str, Any] = {
        "corpus": {
            "root": os.path.abspath(root),
            "tier": tier,
            "file_count": result["corpus"]["file_count"],
            "coverage": result["corpus"]["coverage"],
            "score": result["score"],
            "merkle_root": result["merkleRoot"],
            "audit_id": result["audit_id"],
            # Which corpus definition the scan behind this offer ran under, and the value the
            # certificate itself will record. Quoted here so the
            # caller sees it BEFORE paying: the corpus definition is part of what is being
            # certified, not a detail that surfaces only on the artifact afterwards.
            "config_hash": result["scan"]["config_hash"],
        },
        "certified_eligible": eligible,
        "gaps_remaining": gap_summary(result),
        "self_check": {
            "price": SELF_CHECK_PRICE,
            "what_it_is": "The scan you just ran. Free, unlimited, and it runs entirely on "
                          "this machine.",
            "egress": local_runner.EGRESS_DISCLOSURE,
        },
        "pricing": {
            "tiers": PRICING,
            "self_check": SELF_CHECK_PRICE,
            "note": PRICING_NOTE,
        },
        "includes": list(CERTIFICATION_INCLUDES),
        "purchase": {
            "processed_by": "Stripe, on jidoseal.com — this MCP server never handles a card, "
                            "never charges anything, and cannot complete a purchase.",
            "starts_at": f"{site}/app/run",
            "checkout_api": f"{site}/api/checkout",
            "tool": "jidoseal_start_checkout",
            "requires_from_customer": ["company", "submitter_name", "submitter_email"],
            "what_leaves_this_machine": list(PURCHASE_EGRESS_FIELDS),
            "what_does_not": PURCHASE_EGRESS_NOT_SENT,
        },
    }

    if eligible:
        offer["price"] = price_for(tier, below)
        offer["next_step"] = (
            f"This corpus qualifies for {PRICING[tier]['tier']} certification at "
            f"{offer['price']['display']}. To start the purchase, call jidoseal_start_checkout "
            "with the customer's company, name and email — it returns a Stripe Checkout link "
            "for them to open and pay. Nothing is charged until they complete that checkout, "
            "and this server never sees a card."
        )
    else:
        offer["price"] = None
        offer["next_step"] = (
            "This corpus is not yet at Bronze, so there is nothing to certify yet. The scan "
            "result lists the missing fields per file — close them (free, on this machine), "
            "re-run jidoseal_scan, and the certification offer appears. A corpus that needed "
            "corrections before it reached Bronze certifies at $199 rather than $149."
        )
    return offer
