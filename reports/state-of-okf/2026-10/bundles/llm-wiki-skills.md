# llm-wiki-skills (weiiiii0622)

Repository: <https://github.com/weiiiii0622/llm-wiki-skills>
Checked at commit `e63af11b4bdd` (2026-06-23T23:10:06+08:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `fixtures/demo-vault/wiki/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.1 |
| Concept files | 3 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | no timestamp fields |
| Trust and lifecycle fields used | `sources` (3), `status` (3) |
| Trust tiers (§5.3) | unverified 3 |
| JidoSeal checker | score 33, tier bronze |

3 file(s) use the v0.1 `timestamp` key, which v0.2 supersedes with `generated: {by, at}` (§13.1); consumers may still fall back to it.

Nothing to change under the checks in this report.

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
