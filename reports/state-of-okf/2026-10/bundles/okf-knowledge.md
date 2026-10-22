# okf-knowledge (sniperunder123)

Repository: <https://github.com/sniperunder123/okf-knowledge>
Checked at commit `cbfb00bc42be` (2026-09-17T19:27:29+02:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `okf/resources/example-bundle/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 8 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-21 text |
| Trust and lifecycle fields used | `sources` (2), `generated` (5), `verified` (2), `status` (2), `stale_after` (2) |
| Trust tiers (§5.3) | human-reviewed 2, unverified 6 |
| JidoSeal checker | score 54, tier bronze |

3 file(s) use the v0.1 `timestamp` key, which v0.2 supersedes with `generated: {by, at}` (§13.1); consumers may still fall back to it.

Nothing to change under the checks in this report.

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
