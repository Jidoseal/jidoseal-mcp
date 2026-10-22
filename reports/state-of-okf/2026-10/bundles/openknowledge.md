# openknowledge (openknowledge-sh)

Repository: <https://github.com/openknowledge-sh/openknowledge>
Checked at commit `99b05e27ce32` (2026-10-11T22:00:58+02:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `Wiki/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 67 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | fits both texts |
| Trust and lifecycle fields used | `sources` (2), `generated` (2), `verified` (1), `status` (2) |
| Trust tiers (§5.3) | human-reviewed 1, unverified 66 |
| JidoSeal checker | score 35, tier bronze |

65 file(s) use the v0.1 `timestamp` key, which v0.2 supersedes with `generated: {by, at}` (§13.1); consumers may still fall back to it.

Nothing to change under the checks in this report.

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
