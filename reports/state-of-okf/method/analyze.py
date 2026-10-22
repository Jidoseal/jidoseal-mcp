#!/usr/bin/env python3
"""Check every fetched bundle: where the bundle is, OKF v0.2 conformance, which v0.2 text its
timestamps follow, its trust fields, and the JidoSeal checker's result.

    python3 -I analyze.py bundles.json CLONE_DIR OUT.json

Run with the `jidoseal` engine installed (pip install jidoseal-mcp). Each repository is checked
in its own child process with a 300-second limit, so one huge or odd repository cannot stop
the run. Nothing in a repository is executed: only its `*.md` files are read.

THE BUNDLE-ROOT RULE (BundleDex gives only the repository, not the folder)
  1. If an `index.md` declares `okf_version` in its frontmatter (SPEC §12), the bundle is the
     folder of the shallowest such `index.md`.
  2. Otherwise, among folders that hold `.md` files with a non-empty `type`, the bundle is the
     folder whose subtree holds the most such files while at least half of its concept files
     have one; ties go to the shallower folder, then to the first by name.
  3. If no `.md` file in the repository has a `type`, no bundle root is identified.
Concept files are the `.md` files under the root except `index.md` and `log.md` (SPEC §3.1),
files under a folder whose name starts with "." or is `node_modules`, and paths matched by a
`.okfignore` at the root (a BundleDex convention, not part of the SPEC).
"""
import collections
import concurrent.futures
import fnmatch
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "..", "src"))
RESERVED = ("index.md", "log.md")
SKIP_DIRS = ("node_modules",)
MAX_LISTED = 15


def repo_key(url):
    return url.rstrip("/").lower().removeprefix("https://github.com/").replace("/", "__")


def anon_id(url):
    """What a bundle not listed by name is filed under: the first 12 hex digits of the sha256
    of `github.com/<owner>/<repo>` in lower case."""
    path = url.rstrip("/").lower().removeprefix("https://")
    return hashlib.sha256(path.encode()).hexdigest()[:12]


# --- one repository (runs in a child process) ---------------------------------------------------
def _md_files(top):
    out = []
    for dirpath, dirnames, filenames in os.walk(top, followlinks=False):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and d not in SKIP_DIRS)
        for f in sorted(filenames):
            p = os.path.join(dirpath, f)
            if f.endswith(".md") and not f.startswith(".") and not os.path.islink(p):
                out.append(os.path.relpath(p, top).replace(os.sep, "/"))
    return out


def _okfignore(root_abs):
    p = os.path.join(root_abs, ".okfignore")
    if not os.path.isfile(p):
        return []
    with open(p, encoding="utf-8", errors="replace") as fh:
        return [ln.strip().rstrip("/") for ln in fh if ln.strip() and not ln.startswith("#")]


def _ignored(rel, patterns):
    parts = rel.split("/")
    for pat in patterns:
        pat = pat.lstrip("/")
        if fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(parts[-1], pat):
            return True
        if any(fnmatch.fnmatch("/".join(parts[:i]), pat) for i in range(1, len(parts))):
            return True
    return False


def _under(rel, folder):
    return folder == "" or rel.startswith(folder + "/")


def analyze_one(clone):
    sys.path.insert(0, SRC)
    import okf_trust

    files = _md_files(clone)
    parsed = {}
    for rel in files:
        with open(os.path.join(clone, rel), "rb") as fh:
            text = fh.read(2_000_000).decode("utf-8", "replace")
        fm, problem, _ = okf_trust.parse_frontmatter(text)
        parsed[rel] = (fm, problem, text)

    def has_type(rel):
        fm = parsed[rel][0]
        return bool(fm) and bool(str(fm.get("type") or "").strip())

    declared = sorted((rel.count("/"), rel) for rel in files
                      if rel.split("/")[-1] == "index.md" and parsed[rel][0]
                      and "okf_version" in parsed[rel][0])
    concepts_all = [r for r in files if r.split("/")[-1] not in RESERVED]
    root, rule, okf_version = None, "none", None
    if declared:
        idx = declared[0][1]
        root = idx.rsplit("/", 1)[0] if "/" in idx else ""
        rule, okf_version = "declared", str(parsed[idx][0].get("okf_version"))
    else:
        typed = [r for r in concepts_all if has_type(r)]
        if typed:
            cands = {""}
            for r in typed:
                parts = r.split("/")[:-1]
                cands.update("/".join(parts[:i]) for i in range(1, len(parts) + 1))
            best = None
            for d in cands:
                t = sum(_under(r, d) for r in typed)
                n = sum(_under(r, d) for r in concepts_all)
                if n and t * 2 >= n:
                    k = (t, -d.count("/") - (d != ""))
                    if best is None or k > best[0] or (k == best[0] and d < best[1]):
                        best = (k, d)
            if best is None:  # no folder is half typed: take the one with the highest share
                best = (None, max(sorted(cands), key=lambda d: (
                    sum(_under(r, d) for r in typed) / max(1, sum(_under(r, d) for r in concepts_all)),
                    sum(_under(r, d) for r in typed))))
            root, rule = best[1], "inferred"

    out = {"root": root, "root_rule": rule, "okf_version_declared": okf_version,
           "md_files_in_repo": len(files)}
    if root is None:
        return out
    root_abs = os.path.join(clone, root) if root else clone
    ign = _okfignore(root_abs)
    concepts = [r for r in concepts_all if _under(r, root)
                and not _ignored(r[len(root) + 1:] if root else r, ign)]
    out["okfignore"] = bool(ign)

    problems = collections.defaultdict(list)
    fits = collections.Counter()
    fams = collections.Counter()
    trust_count = collections.Counter()
    tiers = collections.Counter()
    for r in concepts:
        fm, problem, text = parsed[r]
        shown = r[len(root) + 1:] if root else r
        if fm is None:
            problems["no_frontmatter" if problem == "no frontmatter block" else "bad_frontmatter"
                     ].append(shown if problem == "no frontmatter block" else f"{shown}: {problem}")
            continue
        if not str(fm.get("type") or "").strip():
            problems["no_type"].append(shown)
        for k in ("sources", "generated", "verified", "status", "stale_after", "timestamp"):
            if k in fm:
                fams[k] += 1
        if "# Citations" in text:
            fams["citations_heading"] += 1
        t = okf_trust.trust(fm)
        trust_count[t["verdict"]] += 1
        tiers[t["trust_tier"]] += 1
        if t["changed_since_verified"]:
            trust_count["changed_since_verified"] += 1
        for s in t["timestamps"]:
            fits[s["fits"]] += 1
            if s["fits"] == "neither":
                problems["timestamp_neither"].append(f"{shown}: {s['key']} = {s['value']!r}")
            elif s["fits"] == "2026-08-15":
                problems["timestamp_aug15"].append(f"{shown}: {s['key']} = {s['value']!r}")
        if t["stale"]:
            problems["stale"].append(f"{shown}: stale_after {t['stale_after']}")

    n_bad = len({p.split(":")[0] for k in ("no_frontmatter", "bad_frontmatter", "no_type")
                 for p in problems[k]})
    out.update({
        "concepts": len(concepts),
        "conformant": bool(concepts) and n_bad == 0,
        "nonconformant_files": n_bad,
        "which_0_2": okf_trust.which_text(
            f for f, c in fits.items() for _ in range(c)) if fits else "no-timestamps",
        "timestamp_fits": dict(fits),
        "families": dict(fams),
        "trust_verdicts": dict(trust_count),
        "trust_tiers": dict(tiers),
        "problem_counts": {k: len(v) for k, v in problems.items() if v},
        "problems": {k: v[:MAX_LISTED] for k, v in problems.items() if v},
    })
    try:
        import scan_result
        res = scan_result.build_scan_result(root_abs)
        out["jidoseal"] = {"tier": res["corpus"]["tier"], "score": res["score"],
                           "coverage": res["corpus"]["coverage"],
                           "files": res["corpus"]["file_count"]}
    except Exception as e:  # recorded, not hidden
        out["jidoseal"] = {"error": f"{type(e).__name__}: {e}"[:300]}
    return out


# --- the whole run ------------------------------------------------------------------------------
def _child(clone):
    try:
        r = subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "--one", clone],
                           capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            return {"error": (r.stderr.strip().splitlines() or ["failed"])[-1][:300]}
        return json.loads(r.stdout.strip().splitlines()[-1])
    except subprocess.TimeoutExpired:
        return {"error": "check took longer than 300 s"}


def main(bundles_path, clone_dir, out_path):
    meta = json.load(open(bundles_path))
    fetched = json.load(open(os.path.join(clone_dir, "fetch.json")))
    repos = {}
    for b in meta["bundles"]:
        repos.setdefault(b["repo_url"].rstrip("/").lower(), []).append(b)
    results = {}
    todo = {u: os.path.join(clone_dir, repo_key(u)) for u in repos if fetched.get(repo_key(u), {}).get("ok")}
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        futs = {pool.submit(_child, c): u for u, c in todo.items()}
        for i, f in enumerate(concurrent.futures.as_completed(futs), 1):
            results[futs[f]] = f.result()
            if i % 50 == 0:
                print(f"{i}/{len(todo)}", file=sys.stderr, flush=True)
    rows = []
    for u, entries in sorted(repos.items()):
        b = entries[0]
        f = fetched.get(repo_key(u), {})
        rows.append({
            "repo_url": b["repo_url"], "slug": b["slug"], "name": b["name"], "author": b["author"],
            "stars": b.get("stars"), "anon_id": anon_id(u), "bundledex_entries": len(entries),
            "bundledex_conformant": any(e.get("okf_conformant") for e in entries),
            "bundledex_okf_version": b.get("okf_version"),
            "fetched": bool(f.get("ok")), "fetch_error": None if f.get("ok") else " ".join(f.get("error", [])),
            "commit": f.get("commit"), "committed": f.get("committed"),
            **(results.get(u) or {}),
        })
    with open(out_path, "w") as fh:
        json.dump({"bundledex": meta["_meta"], "repos": rows}, fh, indent=1)


if __name__ == "__main__":
    if sys.argv[1] == "--one":
        print(json.dumps(analyze_one(sys.argv[2])))
    else:
        main(*sys.argv[1:4])
