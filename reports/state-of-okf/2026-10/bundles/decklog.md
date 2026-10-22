# decklog (icostadev)

Repository: <https://github.com/icostadev/decklog>
Checked at commit `f594302c7f7a` (2026-07-10T18:36:15Z), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `sample-bundle/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.1 |
| Concept files | 80 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | no timestamp fields |
| Trust and lifecycle fields used | `status` (73) |
| Trust tiers (§5.3) | unverified 80 |
| JidoSeal checker | score 33, tier bronze |

80 file(s) use the v0.1 `timestamp` key, which v0.2 supersedes with `generated: {by, at}` (§13.1); consumers may still fall back to it.

Nothing to change under the checks in this report.

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
