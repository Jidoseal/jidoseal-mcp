# mneme (Scott1743)

Repository: <https://github.com/Scott1743/mneme>
Checked at commit `7538bb3f2a7a` (2026-08-01T03:07:26+08:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `sample-bundle/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 5 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | fits both texts |
| Trust and lifecycle fields used | `sources` (3), `generated` (5), `status` (5) |
| Trust tiers (§5.3) | unverified 5 |
| JidoSeal checker | score 67, tier silver |

5 file(s) use the v0.1 `timestamp` key, which v0.2 supersedes with `generated: {by, at}` (§13.1); consumers may still fall back to it.

Nothing to change under the checks in this report.

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
