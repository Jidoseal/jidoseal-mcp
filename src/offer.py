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
`jidoseal_start_checkout`'s handler. So "the free path opens no socket" is a property of the
import graph on every other path, held by a static import check.

PRICING IS QUOTED, NOT INVENTED
-------------------------------
Every number below is the site's own published price list (OKF Folder Criteria v1.0.0 ladder),
reproduced so a host tool can never quote a price the customer would not actually be charged:
    OKF Certified  free (the free certificate; see `free_certificate_body` in checkout_client)
    Bronze  $349  (renewal $200)
    Silver  $599  (renewal $300)
    Gold    $999  (renewal $450)
    Self-Check — free (the scan and the fixes)
One flat price per grade, however many files; there is no file-count tiering and Bronze has one
price. The scan and the fixes are free; a paid certificate is the only thing that costs money.
"""
from __future__ import annotations

import os
from typing import Any, Dict

from engine_path import ensure_engine_on_path

ensure_engine_on_path()

import scan_result  # noqa: E402  — SCAN_EGRESS_CLAIM: the one qualified sentence about a scan

# The public site. Overridable so a test (or a self-hosted instance) can point the checkout
# tool at a loopback address instead; it is NEVER read on the scan path.
DEFAULT_SITE_URL = "https://jidoseal.com"


def site_url() -> str:
    return (os.environ.get("JIDOSEAL_SITE_URL") or DEFAULT_SITE_URL).rstrip("/")


# Verbatim from jidoseal.com — tier, what the tier means, the price, the renewal price. The
# `rubric` strings are the approved site wording and are the same text scan_result.RUBRIC shows.
PRICING = {
    "okf-certified": {
        "tier": "OKF Certified",
        "rubric": scan_result.RUBRIC["okf-certified"],
        "price_usd": 0,
        "price": "Free",
        "price_note": "free certificate; one per email address, per folder and per company domain",
    },
    "bronze": {
        "tier": "Bronze",
        "rubric": scan_result.RUBRIC["bronze"],
        "price_usd": 349,
        "price": "$349",
        "renewal_usd": 200,
        "renewal": "$200",
        "india_business_inr": "₹18,499",
        "price_note": "one flat price per grade, however many files",
    },
    "silver": {
        "tier": "Silver",
        "rubric": scan_result.RUBRIC["silver"],
        "price_usd": 599,
        "price": "$599",
        "renewal_usd": 300,
        "renewal": "$300",
        "india_business_inr": "₹31,799",
        "price_note": "one flat price per grade, however many files",
    },
    "gold": {
        "tier": "Gold",
        "rubric": scan_result.RUBRIC["gold"],
        "price_usd": 999,
        "price": "$999",
        "renewal_usd": 450,
        "renewal": "$450",
        "india_business_inr": "₹53,099",
        "price_note": "one flat price per grade, however many files",
    },
}

# The tiers a paid checkout can be started for. OKF Certified is the free certificate.
PAID_TIERS = ("bronze", "silver", "gold")

# Bundles and referral, as the site words them.
BUNDLES = [
    "Agency 5-pack: five Bronze certificates, $1,299, use them within 12 months.",
    "Certified OKF tool: includes one 50%-off Bronze code.",
    "Refer a peer: they get 20% off a Bronze certificate.",
]

SELF_CHECK_PRICE = "Free"

PRICING_NOTE = (
    "One flat price per grade, however many files. You only pay once your folder has reached "
    "the grade, so the free scan tells you exactly where you stand first. Scanning and fixing "
    "stay free whether or not you buy a certificate. A paid certificate is the only thing that "
    "costs money; OKF Certified is free."
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
# details the customer types, and nothing else. Stated field by field because "no network use"
# is a claim about the FREE path, and the paid path deserves the same precision rather than a
# reassuring summary. (test_checkout_confirmation derives the seven keys from these strings'
# first words, so keep each key first.)
PURCHASE_EGRESS_FIELDS = [
    "company (typed by the customer)",
    "submitterName (typed by the customer)",
    "submitterEmail (typed by the customer)",
    "requestedTier — one of bronze/silver/gold",
    "score — a single integer 0-100",
    "merkleRoot — one sha256 hex digest over the corpus's per-file hashes",
    "auditId — the local scan's own random id",
]

# What the FREE OKF Certified request sends to POST <site>/api/certify-free: the scan result
# (a score, the OKF section 11 count, how many files) and the folder fingerprint, plus the
# contact details the customer types. Nothing else. (test_free_certificate derives the keys
# from these strings' first words, so keep each key first.)
FREE_EGRESS_FIELDS = [
    "company (typed by the customer)",
    "submitterName (typed by the customer)",
    "submitterEmail (typed by the customer)",
    "score — a single integer 0-100",
    "merkleRoot — one sha256 hex digest over the corpus's per-file hashes",
    "okf11Result — the text 3/3: all three OKF v0.2 section 11 rules pass",
    "fileCount — how many files were scanned (25 or more)",
    "configSha256 — one digest of the folder's own .jidoseal/config.yaml, or the text absent:no-config-file",
]

FREE_MIN_FILES = 25

FREE_NEXT_STEPS = (
    "jidoseal.com emails a confirmation link to the address given; the link expires in 72 hours "
    "and the certificate is issued when the customer opens it. Nothing is charged. A free "
    "certificate needs 25 or more files, and there is one per email address, per folder and "
    "per company domain."
)

# Where those fields go next. jidoseal.com's /api/checkout copies them into the Stripe Checkout
# session it creates (web/app/api/checkout/route.ts): the email as the session's customer_email,
# all seven as session metadata. That happens when the session is created, before any payment.
PURCHASE_STRIPE_HOP = (
    "jidoseal.com copies these fields into the Stripe Checkout session it creates for the "
    "purchase: the email as the session's customer email, and all seven as session metadata. "
    "That happens when the session is created, before any payment. No card data passes "
    "through this server; Stripe hosts the payment page."
)

PURCHASE_EGRESS_NOT_SENT = (
    "No file contents, no file names, no per-file hashes, no directory paths, and no part of "
    "the corpus itself are sent. The merkle root is a one-way digest: it binds the certificate "
    "to this exact corpus, and nothing can be read back out of it."
)


def price_for(tier: str) -> Dict[str, Any]:
    """The price the customer would actually be charged for `tier`. One price per tier:
    Bronze has no below-tier price any more."""
    entry = PRICING[tier]
    out: Dict[str, Any] = {
        "amount_usd": entry["price_usd"],
        "display": entry["price"],
        "why": entry["price_note"],
    }
    if "renewal_usd" in entry:
        out["renewal_usd"] = entry["renewal_usd"]
        out["renewal"] = entry["renewal"]
        out["india_business_inr"] = entry["india_business_inr"]
    return out


def gap_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    """How many field gaps stand between this corpus and each tier, and how many of those the
    customer has to answer themselves (`NEEDS-CLIENT`) rather than accept a proposed value for
    (`AUTO`). Counts only — the per-file list is already in the scan result, and this exists so
    a host can say "7 gaps left" without walking it."""
    out: Dict[str, Any] = {}
    for tier in scan_result.TIERS:
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


def free_eligible(result: Dict[str, Any]) -> bool:
    """Can this folder ask for the free OKF Certified certificate? The same gate
    /api/certify-free applies: all three OKF section 11 rules pass, and 25 or more files."""
    return (result["okf11Result"] == "3/3"
            and result["corpus"]["tier"] != "none"
            and result["corpus"]["file_count"] >= FREE_MIN_FILES)


def build_offer(result: Dict[str, Any], root: str) -> Dict[str, Any]:
    """The certification offer for an already-scanned corpus. Pure local computation over
    `result` (a scan_result.build_scan_result() return) — no network, no payment, no purchase.
    """
    tier = result["corpus"]["tier"]
    paid = tier in PAID_TIERS
    site = site_url()

    offer: Dict[str, Any] = {
        "corpus": {
            "root": os.path.abspath(root),
            "tier": tier,
            "criteria_version": result["corpus"]["criteria_version"],
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
        "certified_eligible": result["certified_eligible"],
        "gaps_remaining": gap_summary(result),
        "self_check": {
            "price": SELF_CHECK_PRICE,
            "what_it_is": "The scan you just ran. Free, unlimited, and it runs on this "
                          "machine.",
            "egress": scan_result.SCAN_EGRESS_CLAIM,
        },
        "pricing": {
            "tiers": PRICING,
            "self_check": SELF_CHECK_PRICE,
            "bundles": list(BUNDLES),
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
            "passed_on_to_stripe": PURCHASE_STRIPE_HOP,
            "what_does_not": PURCHASE_EGRESS_NOT_SENT,
        },
        "free_certificate": {
            "tier": "OKF Certified",
            "price": "Free",
            "eligible": free_eligible(result),
            "tool": "jidoseal_request_free_certificate",
            "free_certify_api": f"{site}/api/certify-free",
            "requires_from_customer": ["company", "submitter_name", "submitter_email"],
            "what_leaves_this_machine": list(FREE_EGRESS_FIELDS),
            "what_does_not": PURCHASE_EGRESS_NOT_SENT,
            "next_steps": FREE_NEXT_STEPS,
        },
    }

    if paid:
        offer["price"] = price_for(tier)
        offer["next_step"] = (
            f"This corpus qualifies for {PRICING[tier]['tier']} certification at "
            f"{offer['price']['display']}. To start the purchase, call jidoseal_start_checkout "
            "with the customer's company, name and email — it returns a Stripe Checkout link "
            "for them to open and pay. Nothing is charged until they complete that checkout, "
            "and this server never sees a card."
        )
    elif tier == "okf-certified":
        offer["price"] = price_for(tier)
        offer["next_step"] = (
            "This corpus is OKF Certified: every file passes the three OKF v0.2 §11 "
            "conformance rules. The OKF Certified certificate is free. "
            + ("To request it, call jidoseal_request_free_certificate with the customer's "
               "company, name and email. " + FREE_NEXT_STEPS
               if offer["free_certificate"]["eligible"] else
               f"It needs {FREE_MIN_FILES} or more files, and this folder has "
               f"{result['corpus']['file_count']}. ")
            + "Bronze ($349) adds a title, description, date and owner on every file; the "
              "scan result lists the missing fields per file, and closing them is free."
        )
    else:
        offer["price"] = None
        offer["next_step"] = (
            "This corpus is not yet OKF Certified, so there is nothing to certify yet. The "
            "scan result lists the missing fields per file — close them (free, on this "
            "machine), re-run jidoseal_scan, and the certification offer appears."
        )
    return offer
