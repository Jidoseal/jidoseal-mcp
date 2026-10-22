# okf-loom (ojamin)

Repository: <https://github.com/ojamin/okf-loom>
Checked at commit `b9264ee4c21d` (2026-07-10T18:31:56+01:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `docs-bundle/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.1 |
| Concept files | 30 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | no timestamp fields |
| Trust and lifecycle fields used | none |
| Trust tiers (§5.3) | unverified 30 |
| JidoSeal checker | score 33, tier bronze |

30 file(s) use the v0.1 `timestamp` key, which v0.2 supersedes with `generated: {by, at}` (§13.1); consumers may still fall back to it.

Nothing to change under the checks in this report.

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
