# okf-pointers (SpillwaveSolutions)

Repository: <https://github.com/SpillwaveSolutions/okf-pointers>
Checked at commit `9a162e022d03` (2026-09-03T20:35:45Z), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `sample-knowledge/` (inferred: see the method) |
| `okf_version` declared | none |
| Concept files | 4 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | no timestamp fields |
| Trust and lifecycle fields used | none |
| Trust tiers (§5.3) | unverified 4 |
| JidoSeal checker | score 33, tier bronze |

4 file(s) use the v0.1 `timestamp` key, which v0.2 supersedes with `generated: {by, at}` (§13.1); consumers may still fall back to it.

Nothing to change under the checks in this report.

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
