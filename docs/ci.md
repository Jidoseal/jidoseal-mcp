# Gate a build on JidoSeal tier

`jidoseal --root <dir>` always exits 0 — it reports, it does not judge. To fail a build when any
file is below a tier, read the manifest it writes. This workflow fails when any file is below
Silver; change `WANT` to `bronze` or `gold` as needed.

```yaml
# .github/workflows/jidoseal.yml
name: knowledge-base tier
on: [pull_request]
jobs:
  jidoseal:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install jidoseal
      - run: jidoseal --root docs/          # the folder of markdown to check
      - name: fail below the wanted tier
        env: { WANT: silver }
        run: |
          python - <<'PY'
          import json, os, sys
          order = {"none": 0, "bronze": 1, "silver": 2, "gold": 3}
          want = os.environ["WANT"]
          m = json.load(open("docs/.jidoseal/manifest.json"))
          bad = sorted(f for f, e in m["files"].items() if order[e["tier"]] < order[want])
          for f in bad:
              print(f"below {want}: {f}")
          sys.exit(1 if bad else 0)
          PY
```

The scan runs entirely on the CI runner and, by JidoSeal's own account, sends nothing anywhere (see the README's "What leaves your machine" for how to check). It writes `docs/.jidoseal/manifest.json` and `progress.ndjson`.
From engine 0.1.4 the `jidoseal` CLI refuses a folder whose symlinks lead outside it, and exits with status 2, so such a folder fails the job instead of being scanned.
Add `.jidoseal/` to `.gitignore` so scan records are not committed.
