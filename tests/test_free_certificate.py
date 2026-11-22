"""
`jidoseal_request_free_certificate` sends a request only with `confirm: true`, and then sends
exactly the documented fields to POST /api/certify-free — nothing about the files.

HTTP is mocked: `urllib.request.urlopen` is replaced, so no test here reaches jidoseal.com.
"""
from __future__ import annotations

import io
import json
import urllib.error
import urllib.request

import pytest

import offer
from conftest import call_tool

DOCUMENTED_FIELDS = [f.split()[0] for f in offer.FREE_EGRESS_FIELDS]
REPLY = {"id": "abc123", "status": "pending",
         "message": "Check your email to confirm. The link expires in 72 hours."}


class FakeHTTP:
    def __init__(self, reply=None):
        self.requests = []
        self.reply = reply if reply is not None else REPLY

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
    assert DOCUMENTED_FIELDS == ["company", "submitterName", "submitterEmail", "score",
                                 "merkleRoot", "okf11Result", "fileCount", "configSha256"]


@pytest.mark.parametrize("confirm", ["missing", False, None, "true", "yes", 1, [True], {"x": 1}])
def test_no_request_without_confirm_true(okf_root, fake_http, confirm):
    args = _args(okf_root) if confirm == "missing" else _args(okf_root, confirm=confirm)
    is_error, payload = call_tool("jidoseal_request_free_certificate", args)
    assert is_error
    assert "Nothing was sent" in payload["error"] and "confirm: true" in payload["error"]
    assert fake_http.requests == []
    # Refused before the scan too: no records were written for a request that did not start.
    assert not (okf_root / ".jidoseal").exists()


def test_confirm_true_sends_one_post_with_exactly_the_documented_keys(okf_root, fake_http):
    is_error, payload = call_tool("jidoseal_request_free_certificate", _args(okf_root, confirm=True))
    assert not is_error, payload
    assert len(fake_http.requests) == 1
    req = fake_http.requests[0]
    assert req.get_method() == "POST"
    assert req.full_url == "https://site.test/api/certify-free"
    body = json.loads(req.data.decode("utf-8"))
    assert list(body) == DOCUMENTED_FIELDS
    assert body["company"] == "Acme Ltd"
    assert body["submitterName"] == "Ada Lovelace"
    assert body["submitterEmail"] == "ada@example.com"
    assert body["okf11Result"] == "3/3"
    assert body["fileCount"] == 30
    assert isinstance(body["score"], int) and 0 <= body["score"] <= 100
    assert body["configSha256"] == "absent:no-config-file"
    assert payload["request_id"] == "abc123" and payload["status"] == "pending"
    assert payload["sent_to_site"] == body
    assert "72 hours" in payload["instruction"]


def test_the_request_carries_nothing_about_the_files(okf_root, fake_http):
    call_tool("jidoseal_request_free_certificate", _args(okf_root, confirm=True))
    req = fake_http.requests[0]
    raw = req.data.decode("utf-8")
    manifest = json.loads((okf_root / ".jidoseal" / "manifest.json").read_text("utf-8"))
    forbidden = [str(okf_root), "okf-notes-folder", "note-00", "Secret body", "# Note"]
    forbidden += [e["hash"].split(":")[-1] for e in manifest["files"].values()]
    for needle in forbidden:
        assert needle not in raw, needle
    assert {k.lower() for k in req.headers} == {"content-type", "accept", "user-agent"}


def test_the_merkle_root_sent_is_the_local_scans(okf_root, fake_http):
    call_tool("jidoseal_request_free_certificate", _args(okf_root, confirm=True))
    sent = json.loads(fake_http.requests[0].data.decode("utf-8"))
    _, scan = call_tool("jidoseal_scan", {"root": str(okf_root)})
    assert scan["corpus"]["tier"] == "okf-certified"
    assert sent["merkleRoot"] == scan["merkleRoot"] and sent["score"] == scan["score"]


def test_fewer_than_25_files_is_refused_without_a_request(tmp_path, fake_http):
    root = tmp_path / "small"
    root.mkdir()
    for i in range(24):
        (root / f"n{i}.md").write_text("---\ntype: note\n---\nx\n", encoding="utf-8")
    is_error, payload = call_tool("jidoseal_request_free_certificate", _args(root, confirm=True))
    assert is_error and "25 or more files" in payload["error"]
    assert fake_http.requests == []


def test_a_folder_failing_section_11_is_refused_without_a_request(world, fake_http):
    is_error, payload = call_tool("jidoseal_request_free_certificate",
                                  _args(world["root"], confirm=True))
    assert is_error and "not OKF Certified" in payload["error"]
    assert fake_http.requests == []


def test_invalid_email_is_refused_locally(okf_root, fake_http):
    is_error, _ = call_tool("jidoseal_request_free_certificate",
                            _args(okf_root, confirm=True, submitter_email="not-an-email"))
    assert is_error
    assert fake_http.requests == []


def test_site_errors_are_reported_not_swallowed(okf_root, monkeypatch):
    def refuse(req, timeout=None):
        raise urllib.error.HTTPError(
            req.full_url, 409, "Conflict", {},
            io.BytesIO(b'{"error": "This email address already has a free OKF Certified certificate."}'))
    monkeypatch.setattr(urllib.request, "urlopen", refuse)
    monkeypatch.setenv("JIDOSEAL_SITE_URL", "https://site.test")
    is_error, payload = call_tool("jidoseal_request_free_certificate", _args(okf_root, confirm=True))
    assert is_error and "already has a free OKF Certified certificate" in payload["error"]


def test_the_offer_for_an_okf_certified_folder_is_free_and_sends_nothing(okf_root, fake_http):
    is_error, payload = call_tool("jidoseal_certification_offer", {"root": str(okf_root)})
    assert not is_error
    assert fake_http.requests == []
    assert payload["price"]["display"] == "Free"
    assert payload["free_certificate"]["eligible"] is True
    assert payload["free_certificate"]["what_leaves_this_machine"] == offer.FREE_EGRESS_FIELDS


def test_tool_schema_requires_confirm():
    import jidoseal_mcp
    tool = next(t for t in jidoseal_mcp.TOOLS if t["name"] == "jidoseal_request_free_certificate")
    assert "confirm" in tool["inputSchema"]["required"]
    assert tool["inputSchema"]["properties"]["confirm"]["type"] == "boolean"
