# okf-agent-graph (SpillwaveSolutions)

Repository: <https://github.com/SpillwaveSolutions/okf-agent-graph>
Checked at commit `8cfe11c5fb8e` (2026-08-27T08:13:31-05:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `sample-ager/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 16 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | no timestamp fields |
| Trust and lifecycle fields used | `verified` (6), `status` (16) |
| Trust tiers (§5.3) | unverified 16 |
| JidoSeal checker | score 33, tier bronze |

16 file(s) use the v0.1 `timestamp` key, which v0.2 supersedes with `generated: {by, at}` (§13.1); consumers may still fall back to it.

Nothing to change under the checks in this report.

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
