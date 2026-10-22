#!/usr/bin/env python3
"""Turn analyze.py's results into the published report folder.

    python3 build.py RESULTS.json OUT_DIR

Writes OUT_DIR/leaderboard.md, OUT_DIR/data.json and one page per bundle under
OUT_DIR/bundles/. The report's own prose (OUT_DIR/README.md) is written by hand from the
numbers this script prints, so every number in it can be traced to data.json.

WHO IS NAMED
  Bundles that meet OKF v0.2 conformance under the rule in analyze.py (so the whole leaderboard,
  top 20 included) are listed by name. Every other bundle is listed under an id: the first 12 hex
  digits of sha256("github.com/<owner>/<repo>" in lower case), so its author can find it, and
  it is not named in any table.
"""
import collections
import json
import os
import sys

FIELDS = ("sources", "generated", "verified", "status", "stale_after")
WHICH = {
    "both": "fits both texts",
    "2026-08-21": "2026-08-21 text",
    "2026-08-15": "2026-08-15 text",
    "mixed": "mixes the two texts",
    "neither": "has values neither text allows",
    "no-timestamps": "no timestamp fields",
}
FIX = {
    "no_frontmatter": (
        "Files with no frontmatter block",
        "OKF v0.2 §11 asks every `.md` file other than `index.md` and `log.md` to start with a "
        "YAML frontmatter block holding a non-empty `type`. The smallest change is:\n\n"
        "```yaml\n---\ntype: Note\n---\n```\n\nIf these files are not meant to be part of the "
        "bundle (a README, a changelog), moving the bundle into its own folder keeps them out."),
    "bad_frontmatter": (
        "Files whose frontmatter does not parse",
        "The block between the `---` lines must be valid YAML that reads as a mapping. The "
        "parser's first message is shown for each file."),
    "no_type": (
        "Files with frontmatter but no `type`",
        "`type` is the one key OKF v0.2 always requires (§4.1). Any short descriptive string "
        "works, for example `type: Reference`."),
    "timestamp_neither": (
        "Timestamp values neither v0.2 text allows",
        "`generated.at` and `verified[].at` are datetimes in both texts "
        "(`2026-06-30T14:00:00Z`); `stale_after`, `sources[].last_modified` and `usage_window` "
        "are bare dates in the 2026-08-15 text and datetimes with an offset in the 2026-08-21 "
        "text. Placeholders such as `YYYY-MM-DD` left in a template are counted here too."),
    "timestamp_aug15": (
        "Values that follow the 2026-08-15 text",
        "These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), "
        "write each as a datetime with a UTC offset, for example `2026-12-31` becomes "
        "`2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: \"0.2\"`."),
    "stale": (
        "Documents past their `stale_after`",
        "OKF v0.2 §5.5: a concept is stale when now >= `stale_after`. Review the content, then "
        "move `stale_after` forward (and add a `verified` entry if someone confirmed it)."),
}
ORDER = ("no_frontmatter", "bad_frontmatter", "no_type", "timestamp_neither", "timestamp_aug15",
         "stale")


def fam_count(r):
    return sum(1 for k in FIELDS if r["families"].get(k))


def score(r):
    return r.get("jidoseal", {}).get("score", -1)


def rank_key(r):
    return (-score(r), -fam_count(r), -r["concepts"], r["repo_url"].lower())


def main(results_path, out_dir):
    data = json.load(open(results_path))
    repos = data["repos"]
    bundles = [r for r in repos if r.get("concepts") is not None]
    conformant = sorted([r for r in bundles if r["conformant"]], key=rank_key)
    ranked = sorted(bundles, key=rank_key)
    named = {r["repo_url"] for r in conformant}  # includes the top 20 of the leaderboard
    for r in repos:
        r["named"] = r["repo_url"] in named
        r["page"] = (f"bundles/{r['slug']}.md" if r["named"] else f"bundles/{r['anon_id']}.md") \
            if r.get("concepts") is not None else None

    os.makedirs(os.path.join(out_dir, "bundles"), exist_ok=True)
    for r in bundles:
        with open(os.path.join(out_dir, r["page"]), "w") as fh:
            fh.write(page(r))

    with open(os.path.join(out_dir, "leaderboard.md"), "w") as fh:
        fh.write(leaderboard(conformant, data))

    public = []
    for r in repos:
        row = {k: r.get(k) for k in (
            "anon_id", "fetched", "commit", "committed", "root", "root_rule",
            "okf_version_declared", "concepts", "conformant", "nonconformant_files", "which_0_2",
            "timestamp_fits", "families", "trust_verdicts", "trust_tiers", "problem_counts",
            "jidoseal", "bundledex_conformant", "bundledex_entries", "page", "error")}
        if r["named"]:
            row.update({k: r[k] for k in ("repo_url", "slug", "name", "author")})
        if not r["fetched"]:
            row["fetch_error"] = "repository not reachable (removed, renamed or private)"
        public.append(row)
    with open(os.path.join(out_dir, "data.json"), "w") as fh:
        json.dump({"bundledex": data["bundledex"],
                   "naming": "Named: bundles that meet OKF v0.2 conformance under this "
                             "report's rule, and the top 20. Others carry only anon_id = first "
                             "12 hex digits of sha256('github.com/<owner>/<repo>', lower case).",
                   "repos": sorted(public, key=lambda x: (not x.get("slug"), x.get("slug") or x["anon_id"]))},
                  fh, indent=1, ensure_ascii=False)
    readme = os.path.join(out_dir, "README.md")
    if os.path.isfile(readme):  # refresh the top-20 table between its markers
        text = open(readme).read()
        a, b = "<!-- top20 -->\n", "<!-- /top20 -->"
        if a in text and b in text:
            rows = "".join(
                f"| {i} | [{md(r['name'])}]({r['page']}) ({md(r['author'])}) | {r['concepts']} | "
                f"{WHICH[r['which_0_2']]} | "
                f"{', '.join('`%s`' % k for k in FIELDS if r['families'].get(k)) or 'none'} |\n"
                for i, r in enumerate(conformant[:20], 1))
            text = text[:text.index(a) + len(a)] + rows + text[text.index(b):]
            with open(readme, "w") as fh:
                fh.write(text)
    stats(repos, bundles, conformant, ranked)


def leaderboard(conformant, data):
    lines = [
        "# State of OKF, October 2026: leaderboard",
        "",
        "Every bundle below meets OKF v0.2 conformance (§11, items 1 and 2) under this report's "
        "bundle-root rule, checked on 2026-10-22 (UTC) at the commit recorded in "
        "[data.json](data.json). Ordered by the JidoSeal checker's 0–100 score (the mean of its "
        "three coverage figures), then by how many of the five OKF v0.2 trust and lifecycle "
        "fields the bundle uses, then by size. The score and its Bronze/Silver/Gold tiers are "
        "defined by JidoSeal, not by OKF; [method](README.md#method).",
        "",
        "Fields: **S** `sources`, **G** `generated`, **V** `verified`, **St** `status`, "
        "**SA** `stale_after`. *Timestamps* says which text of OKF v0.2 the bundle's timestamp "
        "values follow ([why there are two](README.md#which-02)).",
        "",
        "| # | Bundle | Author | Files | Timestamps | S | G | V | St | SA | Human-reviewed files | JidoSeal score | Details |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(conformant, 1):
        f = r["families"]
        mark = lambda k: "✓" if f.get(k) else ""  # noqa: E731
        js = r.get("jidoseal", {})
        lines.append(
            f"| {i} | [{md(r['name'])}]({r['repo_url']}) | {md(r['author'])} | {r['concepts']} | "
            f"{WHICH[r['which_0_2']]} | {mark('sources')} | {mark('generated')} | "
            f"{mark('verified')} | {mark('status')} | {mark('stale_after')} | "
            f"{r['trust_tiers'].get('human-reviewed', 0)} | "
            f"{js.get('score', 'n/a')} ({js.get('tier', 'n/a')}) | [page]({r['page']}) |")
    lines += ["", f"{len(conformant)} bundles. Not listed here? See "
              "[find your bundle](README.md#find-your-bundle).", ""]
    return "\n".join(lines)


def md(s):
    return str(s).replace("|", "\\|")


def page(r):
    title = f"{r['name']} ({r['author']})" if r["named"] else f"Bundle {r['anon_id']}"
    js = r.get("jidoseal", {})
    conf = ("meets it" if r["conformant"]
            else "no concept files found under the bundle folder" if not r["concepts"]
            else f"not yet: {r['nonconformant_files']} file(s) to change")
    lines = [f"# {title}", ""]
    if r["named"]:
        lines.append(f"Repository: <{r['repo_url']}>")
    lines += [
        f"Checked at commit `{(r.get('commit') or '')[:12]}` ({r.get('committed')}), on "
        "2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).",
        "",
        "| | |",
        "|---|---|",
        f"| Bundle folder | `{r['root'] or '(repository root)'}/` "
        f"({'declared by an index.md with okf_version' if r['root_rule'] == 'declared' else 'inferred: see the method'}) |",
        f"| `okf_version` declared | {r['okf_version_declared'] or 'none'} |",
        f"| Concept files | {r['concepts']} |",
        f"| OKF v0.2 conformance (§11, items 1–2) | {conf} |",
        f"| Timestamps follow | {WHICH[r['which_0_2']]} |",
        f"| Trust and lifecycle fields used | "
        f"{', '.join('`%s` (%d)' % (k, r['families'][k]) for k in FIELDS if r['families'].get(k)) or 'none'} |",
        f"| Trust tiers (§5.3) | "
        f"{', '.join('%s %d' % (k, v) for k, v in sorted(r['trust_tiers'].items())) or 'n/a'} |",
        f"| JidoSeal checker | "
        f"{('score %s, tier %s' % (js['score'], js['tier'])) if 'score' in js else 'did not complete (' + js.get('error', 'not run') + ')'} |",
        "",
    ]
    if r["families"].get("timestamp"):
        lines += [f"{r['families']['timestamp']} file(s) use the v0.1 `timestamp` key, which v0.2 "
                  "supersedes with `generated: {by, at}` (§13.1); consumers may still fall back "
                  "to it.", ""]
    probs = r.get("problems", {})
    if probs:
        lines += ["## What to change", ""]
        for k in ORDER:
            if k in probs:
                head, how = FIX[k]
                n = r["problem_counts"][k]
                lines += [f"### {head} ({n})", "", how, ""]
                lines += [f"- `{p}`" for p in probs[k]]
                if n > len(probs[k]):
                    lines.append(f"- … and {n - len(probs[k])} more")
                lines.append("")
    elif not r["concepts"]:
        lines += ["Every `.md` file under the bundle folder is a reserved file, hidden, or "
                  "listed in `.okfignore`, so there was nothing to check. If the bundle is "
                  "elsewhere in the repository, open an issue (below).", ""]
    else:
        lines += ["Nothing to change under the checks in this report.", ""]
    lines += [
        "## Check it again yourself",
        "",
        "The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file "
        "rules as this page, on your own machine: point it at the bundle folder. See "
        "[run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong "
        "here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/"
        "jidoseal-mcp/issues/new?template=state-of-okf.md).",
        "",
    ]
    return "\n".join(lines)


def stats(repos, bundles, conformant, ranked):
    C = collections.Counter
    print("repos", len(repos), "fetched", sum(r["fetched"] for r in repos))
    print("root rule", C(r.get("root_rule") for r in repos if r["fetched"]))
    print("bundles", len(bundles), "conformant", len(conformant))
    print("which all", C(r["which_0_2"] for r in bundles))
    print("which conformant", C(r["which_0_2"] for r in conformant))
    print("declared", C(r["okf_version_declared"] for r in bundles))
    print("bdx vs ours", C((r["bundledex_conformant"], r["conformant"]) for r in bundles))
    print("tiers", C(r.get("jidoseal", {}).get("tier", "ERR") for r in bundles))
    fam = C(k for r in bundles for k, v in r["families"].items() if v)
    print("families", fam)
    print("problems", C(k for r in bundles for k in r.get("problem_counts", {})))
    print("files", sum(r["concepts"] for r in bundles))
    tt, tv = C(), C()
    for r in bundles:
        tt.update(r["trust_tiers"]); tv.update(r["trust_verdicts"])
    print("tiers files", tt, "verdicts", tv)
    print("errors", [(r["anon_id"], r.get("error"), r.get("jidoseal")) for r in repos
                     if r.get("error") or "error" in r.get("jidoseal", {})])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
