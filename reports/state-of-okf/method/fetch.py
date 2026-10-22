#!/usr/bin/env python3
"""Fetch the Markdown files of every bundle listed by BundleDex.

    python3 fetch.py bundles.json CLONE_DIR

One shallow clone per unique repository (BundleDex lists some repositories twice), with a
sparse checkout of `*.md` only, so no code or binary in a repository is ever downloaded or
run. Each clone has a 120-second limit. The outcome of every fetch is written to
CLONE_DIR/fetch.json; a repository that is gone or private is recorded, not retried.
"""
import concurrent.futures
import json
import os
import subprocess
import sys

ENV = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_LFS_SKIP_SMUDGE="1")


def key(url):
    return url.rstrip("/").lower().removeprefix("https://github.com/").replace("/", "__")


def run(args, cwd=None):
    return subprocess.run(args, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=120)


def fetch(url, dest):
    try:
        if os.path.isdir(os.path.join(dest, ".git")):  # fetched by an earlier run
            head = run(["git", "log", "-1", "--format=%H %cI"], cwd=dest).stdout.split()
            return {"ok": True, "commit": head[0], "committed": head[1]}
        r = run(["git", "clone", "--quiet", "--depth", "1", "--filter=blob:none", "--no-checkout",
                 "-c", "core.hooksPath=/dev/null", url, dest])
        if r.returncode != 0:
            return {"ok": False, "error": r.stderr.strip().splitlines()[-1:] or ["clone failed"]}
        run(["git", "sparse-checkout", "set", "--no-cone", "*.md"], cwd=dest)
        r = run(["git", "checkout", "--quiet"], cwd=dest)
        if r.returncode != 0:
            return {"ok": False, "error": r.stderr.strip().splitlines()[-1:] or ["checkout failed"]}
        head = run(["git", "log", "-1", "--format=%H %cI"], cwd=dest).stdout.split()
        return {"ok": True, "commit": head[0], "committed": head[1]}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": ["timed out after 120 s"]}


def main(bundles_path, clone_dir):
    bundles = json.load(open(bundles_path))["bundles"]
    urls = sorted({b["repo_url"].rstrip("/").lower(): b["repo_url"] for b in bundles}.values())
    os.makedirs(clone_dir, exist_ok=True)
    out = {}
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        futs = {pool.submit(fetch, u, os.path.join(clone_dir, key(u))): u for u in urls}
        for i, f in enumerate(concurrent.futures.as_completed(futs), 1):
            out[key(futs[f])] = f.result()
            if i % 50 == 0:
                print(f"{i}/{len(urls)}", file=sys.stderr, flush=True)
    with open(os.path.join(clone_dir, "fetch.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(sum(v["ok"] for v in out.values()), "of", len(out), "fetched", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
