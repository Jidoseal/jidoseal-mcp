"""
okf_trust.py — OKF v0.2 trust, lifecycle and "which 0.2?" checks, read from frontmatter.
=======================================================================================
Backs the `jidoseal_trust` tool, the trust half of `jidoseal_changes`, and the State of OKF
report in reports/state-of-okf/ (whose scripts import this module, so the report and the tool
apply one rule set).

WHAT IT ANSWERS
---------------
For one concept document, per OKF v0.2 §5:
  * its trust tier (§5.3): unverified / machine-confirmed / human-reviewed, reading a bare
    `verified` mapping as a one-element list, as §5.2 requires;
  * its lifecycle (§5.4, §5.5): `status` (absent means stable) and whether `stale_after` has
    passed;
  * whether its content changed after its latest verification (`generated.at` later than the
    newest `verified[].at`; §5.2 keeps the two independent, so a consumer has to compare them);
and one verdict an agent can act on before it relies on the document: "stale", "unverified"
or "ok", with the reasons.

"WHICH 0.2?"
------------
OKF v0.2 changed on 2026-08-21 without a version bump (GoogleCloudPlatform/open-knowledge-format
pull 6, merge commit ad30107). The text of 2026-08-15 (commit 25461db) wrote `stale_after`,
`sources[].last_modified` and `usage_window.from`/`to` as bare dates (`YYYY-MM-DD`) and
`generated.at` / `verified[].at` as ISO 8601 datetimes. The text of 2026-08-21 makes every one of
them an ISO 8601 datetime with an explicit UTC offset (`2026-06-30T14:00:00Z`). Both say
`okf_version: "0.2"`. `timestamp_fit` says which text each timestamp value follows, and
`which_text` sums that up for a document or a whole bundle.

WHY A LOADER OF ITS OWN
-----------------------
PyYAML follows YAML 1.1 and turns an unquoted `2026-08-15` into a `date` before anyone can look
at it, so "was this written as a date or a datetime?" would be unanswerable. The loader below
drops PyYAML's timestamp resolver — what pull 6 did to the reference agent — so every value
stays the string the author wrote. It is otherwise `yaml.SafeLoader`.

Reads nothing and writes nothing itself: callers hand it text. Stdlib plus PyYAML (already
the engine's one dependency); no network-capable import (tests/test_import_graph.py).
"""
from __future__ import annotations

import datetime
import re
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

import yaml

SPEC_TEXTS = {
    "2026-08-15": "OKF v0.2 as of 2026-08-15 (commit 25461db): stale_after, "
                  "sources[].last_modified and usage_window are bare dates (YYYY-MM-DD)",
    "2026-08-21": "OKF v0.2 as of 2026-08-21 (pull 6, merge commit ad30107): every timestamp "
                  "is an ISO 8601 datetime with an explicit UTC offset",
}


class _StringTimestampLoader(yaml.SafeLoader):
    pass


_StringTimestampLoader.yaml_implicit_resolvers = {
    first: [(tag, rx) for tag, rx in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for first, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}

_FENCE = re.compile(r"\A﻿?---[ \t]*\r?\n(.*?)^---[ \t]*\r?$", re.S | re.M)


def parse_frontmatter(text: str) -> Tuple[Optional[Dict[str, Any]], Optional[str], str]:
    """(frontmatter, problem, body). frontmatter is None when there is no block or it does not
    parse to a mapping; `problem` then says which. Timestamps stay strings."""
    m = _FENCE.match(text)
    if not m:
        return None, "no frontmatter block", text
    body = text[m.end():]
    try:
        fm = yaml.load(m.group(1), Loader=_StringTimestampLoader)  # noqa: S506 — SafeLoader subclass
    except (yaml.YAMLError, ValueError, TypeError, OverflowError) as e:
        # ValueError and friends: an explicit tag PyYAML cannot honour, e.g. `!!int notanumber`.
        first = (str(e).splitlines() or [type(e).__name__])[0]
        return None, "frontmatter is not valid YAML: " + first, body
    if fm is None:
        fm = {}
    if not isinstance(fm, dict):
        return None, "frontmatter is not a mapping", body
    return fm, None, body


# --- timestamps --------------------------------------------------------------------------------
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DT_OFFSET = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}(:?\d{2})?)$")
_DT_NAIVE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?$")

# Keys the 2026-08-15 text wrote as dates, and keys both texts write as datetimes.
DATE_KEYS = ("stale_after", "sources[].last_modified", "usage_window.from", "usage_window.to")
DATETIME_KEYS = ("generated.at", "verified[].at")


def _as_list(v: Any) -> List[Any]:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def timestamp_values(fm: Dict[str, Any]) -> Iterator[Tuple[str, str]]:
    """Every timestamp-valued key OKF v0.2 defines, as (key, value-as-written)."""
    if "stale_after" in fm:
        yield "stale_after", fm["stale_after"]
    windows = [fm.get("usage_window")]
    for src in _as_list(fm.get("sources")):
        if isinstance(src, dict):
            if "last_modified" in src:
                yield "sources[].last_modified", src["last_modified"]
            windows.append(src.get("usage_window"))
    for w in windows:
        if isinstance(w, dict):
            for k in ("from", "to"):
                if k in w:
                    yield "usage_window." + k, w[k]
    gen = fm.get("generated")
    if isinstance(gen, dict) and "at" in gen:
        yield "generated.at", gen["at"]
    for v in _as_list(fm.get("verified")):
        if isinstance(v, dict) and "at" in v:
            yield "verified[].at", v["at"]


def timestamp_fit(key: str, value: Any) -> str:
    """Which v0.2 text a timestamp value follows: "both", "2026-08-15", "2026-08-21" or
    "neither"."""
    s = str(value).strip() if value is not None else ""
    if key in DATETIME_KEYS:
        if _DT_OFFSET.match(s):
            return "both"
        if _DT_NAIVE.match(s):
            return "2026-08-15"  # a datetime, which is all the earlier text asked for
        return "neither"
    if _DATE.match(s):
        return "2026-08-15"
    if _DT_OFFSET.match(s):
        return "2026-08-21"
    return "neither"


def which_text(fits: Iterable[str]) -> str:
    """Sum up timestamp fits: "no-timestamps", "both", "2026-08-21", "2026-08-15", "mixed"
    (some values follow one text and some the other), or "neither" (at least one value fits
    neither text)."""
    fits = set(fits)
    if not fits:
        return "no-timestamps"
    if fits == {"both"}:
        return "both"
    if fits <= {"both", "2026-08-21"}:
        return "2026-08-21"
    if fits <= {"both", "2026-08-15"}:
        return "2026-08-15"
    return "neither" if "neither" in fits else "mixed"


def parse_instant(value: Any) -> Optional[datetime.datetime]:
    """A timestamp as an aware UTC datetime, accepting both v0.2 texts. A bare date is read as
    00:00 UTC that day and a datetime without an offset as UTC; `trust` says when it did so."""
    s = str(value).strip() if value is not None else ""
    try:
        if _DATE.match(s):
            return datetime.datetime.fromisoformat(s).replace(tzinfo=datetime.timezone.utc)
        if _DT_OFFSET.match(s) or _DT_NAIVE.match(s):
            s2 = s[:-1] + "+00:00" if s.endswith("Z") else s
            if re.search(r"[+-]\d{2}$", s2):
                s2 += ":00"
            elif re.search(r"[+-]\d{4}$", s2):
                s2 = s2[:-2] + ":" + s2[-2:]
            dt = datetime.datetime.fromisoformat(s2)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=datetime.timezone.utc)
            return dt.astimezone(datetime.timezone.utc)
    except ValueError:
        return None
    return None


# --- trust ------------------------------------------------------------------------------------
def trust_tier(fm: Dict[str, Any]) -> str:
    """OKF v0.2 §5.3."""
    entries = [v for v in _as_list(fm.get("verified")) if isinstance(v, dict)]
    if not entries:
        return "unverified"
    if any(str(v.get("by", "")).strip().startswith("human:") for v in entries):
        return "human-reviewed"
    return "machine-confirmed"


def _iso(dt: Optional[datetime.datetime]) -> Optional[str]:
    return dt.isoformat().replace("+00:00", "Z") if dt else None


def trust(fm: Optional[Dict[str, Any]], problem: Optional[str] = None,
          now: Optional[datetime.datetime] = None) -> Dict[str, Any]:
    """The trust answer for one document. `fm` None means no usable frontmatter."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    if fm is None:
        return {"verdict": "unverified", "reasons": [problem or "no frontmatter"],
                "okf_conformant": False, "conformance": problem or "no frontmatter",
                "trust_tier": "unverified", "status": None, "stale": None,
                "which_0_2": "no-timestamps", "timestamps": []}
    reasons: List[str] = []
    notes: List[str] = []
    stamps = [{"key": k, "value": str(v), "fits": timestamp_fit(k, v)}
              for k, v in timestamp_values(fm)]

    status = str(fm.get("status") or "stable").strip().lower()
    stale_after = parse_instant(fm["stale_after"]) if "stale_after" in fm else None
    stale: Optional[bool] = None
    if "stale_after" in fm:
        if stale_after is None:
            notes.append(f"stale_after {fm['stale_after']!r} is not a date or datetime, so "
                         "staleness cannot be decided")
        else:
            stale = now >= stale_after
            if timestamp_fit("stale_after", fm["stale_after"]) == "2026-08-15":
                notes.append("stale_after is a bare date; read as 00:00 UTC that day")
    if stale:
        reasons.append(f"stale since {_iso(stale_after)} (stale_after)")
    if status == "deprecated":
        reasons.append("status is deprecated: kept for links and history, no longer current")

    tier = trust_tier(fm)
    gen = fm.get("generated") if isinstance(fm.get("generated"), dict) else {}
    generated_at = parse_instant(gen.get("at")) if gen.get("at") is not None else None
    verified_ats = [parse_instant(v.get("at")) for v in _as_list(fm.get("verified"))
                    if isinstance(v, dict) and v.get("at") is not None]
    latest_verified = max((d for d in verified_ats if d), default=None)
    changed_since = bool(generated_at and latest_verified and generated_at > latest_verified)

    unverified: List[str] = []
    if tier == "unverified":
        unverified.append("no `verified` entry: nobody has confirmed this content")
    elif changed_since:
        unverified.append(f"content changed at {_iso(generated_at)}, after its latest "
                          f"verification at {_iso(latest_verified)}")
    if status == "draft":
        unverified.append("status is draft: not yet reviewed")

    verdict = "stale" if reasons else ("unverified" if unverified else "ok")
    has_type = bool(str(fm.get("type") or "").strip())
    return {
        "verdict": verdict,
        "reasons": reasons + unverified,
        # OKF v0.2 §11 for one concept file: parseable frontmatter with a non-empty `type`.
        "okf_conformant": has_type,
        **({} if has_type else {"conformance": "no `type`: OKF v0.2 requires a non-empty type"}),
        "trust_tier": tier,
        "status": status,
        "stale": stale,
        "stale_after": _iso(stale_after),
        "generated_at": _iso(generated_at),
        "latest_verified_at": _iso(latest_verified),
        "changed_since_verified": changed_since,
        "which_0_2": which_text(s["fits"] for s in stamps),
        "timestamps": stamps,
        **({"notes": notes} if notes else {}),
    }


def trust_of_text(text: str, now: Optional[datetime.datetime] = None) -> Dict[str, Any]:
    fm, problem, _ = parse_frontmatter(text)
    return trust(fm, problem, now)
