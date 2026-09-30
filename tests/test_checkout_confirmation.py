"""
`jidoseal_start_checkout` sends a request only with `confirm: true`, and then sends exactly the
eight documented fields — nothing about the files.

HTTP is mocked: `urllib.request.urlopen` is replaced, so no test here reaches jidoseal.com.
"""
from __future__ import annotations

import io
import json
import os
import urllib.request

import pytest

import offer
from conftest import call_tool

DOCUMENTED_FIELDS = [f.split()[0] for f in offer.PURCHASE_EGRESS_FIELDS]


class FakeHTTP:
    def __init__(self, reply=None):
        self.requests = []
        self.reply = reply if reply is not None else {"url": "https://checkout.stripe.test/c/1"}

    def __call__(self, req, timeout=None):
        self.requests.append(req)
        return io.BytesIO(json.dumps(self.reply).encode("utf-8"))


@pytest.fixture
def fake_http(monkeypatch):
    fake = FakeHTTP()
    monkeypatch.setattr(urllib.request, "urlopen", fake)
    monkeypatch.setenv("JIDOSEAL_SITE_URL", "https://site.test")
    return fake


def _args(root, **extra):
    args = {"root": str(root), "company": "Acme Ltd", "submitter_name": "Ada Lovelace",
            "submitter_email": "ada@example.com"}
    args.update(extra)
    return args


def test_the_documented_list_is_the_eight_fields():
    assert DOCUMENTED_FIELDS == ["company", "submitterName", "submitterEmail", "requestedTier",
                                 "score", "merkleRoot", "auditId", "belowTier"]


@pytest.mark.parametrize("confirm", ["missing", False, None, "true", "yes", 1, [True], {"x": 1}])
def test_no_request_without_confirm_true(gold_root, fake_http, confirm):
    args = _args(gold_root) if confirm == "missing" else _args(gold_root, confirm=confirm)
    is_error, payload = call_tool("jidoseal_start_checkout", args)
    assert is_error
    assert "Nothing was sent" in payload["error"] and "confirm: true" in payload["error"]
    assert fake_http.requests == []
    # Refused before the scan too: no records were written for a purchase that did not start.
    assert not (gold_root / ".jidoseal").exists()


def test_confirm_true_sends_one_post_with_only_the_documented_fields(gold_root, fake_http):
    is_error, payload = call_tool("jidoseal_start_checkout", _args(gold_root, confirm=True))
    assert not is_error, payload
    assert len(fake_http.requests) == 1
    req = fake_http.requests[0]
    assert req.get_method() == "POST"
    assert req.full_url == "https://site.test/api/checkout"
    body = json.loads(req.data.decode("utf-8"))
    assert list(body) == DOCUMENTED_FIELDS
    assert body["company"] == "Acme Ltd"
    assert body["submitterName"] == "Ada Lovelace"
    assert body["submitterEmail"] == "ada@example.com"
    assert body["requestedTier"] == "gold"
    assert isinstance(body["score"], int) and 0 <= body["score"] <= 100
    assert isinstance(body["belowTier"], bool)
    assert payload["checkout_url"] == "https://checkout.stripe.test/c/1"
    assert payload["sent_to_site"] == body


def test_the_request_carries_nothing_about_the_files(gold_root, fake_http):
    call_tool("jidoseal_start_checkout", _args(gold_root, confirm=True))
    req = fake_http.requests[0]
    raw = req.data.decode("utf-8")
    manifest = json.loads((gold_root / ".jidoseal" / "manifest.json").read_text("utf-8"))
    forbidden = [str(gold_root), os.path.basename(str(gold_root)), "leave-policy", "handbook",
                 "Leave policy", "How we work", "people-ops"]
    forbidden += [e["hash"].split(":")[-1] for e in manifest["files"].values()]
    for needle in forbidden:
        assert needle not in raw, needle
    # Headers too: nothing but content negotiation and a fixed user agent.
    assert {k.lower() for k in req.headers} == {"content-type", "accept", "user-agent"}
    assert req.get_header("User-agent") == "jidoseal-mcp"


def test_the_merkle_root_sent_is_the_local_scans(gold_root, fake_http):
    call_tool("jidoseal_start_checkout", _args(gold_root, confirm=True))
    sent = json.loads(fake_http.requests[0].data.decode("utf-8"))
    _, scan = call_tool("jidoseal_scan", {"root": str(gold_root)})
    assert sent["merkleRoot"] == scan["merkleRoot"]


def test_default_site_is_jidoseal_com(gold_root, fake_http, monkeypatch):
    monkeypatch.delenv("JIDOSEAL_SITE_URL")
    call_tool("jidoseal_start_checkout", _args(gold_root, confirm=True))
    assert fake_http.requests[0].full_url == "https://jidoseal.com/api/checkout"


def test_below_bronze_folder_is_refused_without_a_request(world, fake_http):
    is_error, payload = call_tool("jidoseal_start_checkout", _args(world["root"], confirm=True))
    assert is_error and "not at Bronze" in payload["error"]
    assert fake_http.requests == []


def test_invalid_email_is_refused_locally(gold_root, fake_http):
    is_error, _ = call_tool("jidoseal_start_checkout",
                            _args(gold_root, confirm=True, submitter_email="not-an-email"))
    assert is_error
    assert fake_http.requests == []


def test_site_without_a_checkout_url_is_an_error_not_a_fake_success(gold_root, monkeypatch):
    fake = FakeHTTP(reply={"note": "payments not configured"})
    monkeypatch.setattr(urllib.request, "urlopen", fake)
    monkeypatch.setenv("JIDOSEAL_SITE_URL", "https://site.test")
    is_error, payload = call_tool("jidoseal_start_checkout", _args(gold_root, confirm=True))
    assert is_error and "payments not configured" in payload["error"]


def test_the_offer_tool_sends_nothing(gold_root, fake_http):
    is_error, payload = call_tool("jidoseal_certification_offer", {"root": str(gold_root)})
    assert not is_error
    assert fake_http.requests == []
    assert payload["purchase"]["what_leaves_this_machine"] == offer.PURCHASE_EGRESS_FIELDS


def test_tool_schema_requires_confirm():
    import jidoseal_mcp
    tool = next(t for t in jidoseal_mcp.TOOLS if t["name"] == "jidoseal_start_checkout")
    assert "confirm" in tool["inputSchema"]["required"]
    assert tool["inputSchema"]["properties"]["confirm"]["type"] == "boolean"
