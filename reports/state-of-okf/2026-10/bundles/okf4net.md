# okf4net (jchable)

Repository: <https://github.com/jchable/okf4net>
Checked at commit `916c02d0db0c` (2026-10-15T10:25:43+02:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `tests/fixtures/okf_v02/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 2 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-21 text |
| Trust and lifecycle fields used | `sources` (1), `generated` (2), `verified` (1), `status` (2), `stale_after` (1) |
| Trust tiers (§5.3) | human-reviewed 1, unverified 1 |
| JidoSeal checker | score 67, tier silver |

1 file(s) use the v0.1 `timestamp` key, which v0.2 supersedes with `generated: {by, at}` (§13.1); consumers may still fall back to it.

Nothing to change under the checks in this report.

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
