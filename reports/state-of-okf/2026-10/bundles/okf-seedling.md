# okf-seedling (watanabe3tipapa)

Repository: <https://github.com/watanabe3tipapa/okf-seedling>
Checked at commit `d28069ce878b` (2026-10-20T22:30:20+09:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `okf/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 6 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (2), `generated` (6), `verified` (6), `status` (6), `stale_after` (6) |
| Trust tiers (§5.3) | human-reviewed 6 |
| JidoSeal checker | score 67, tier silver |

## What to change

### Values that follow the 2026-08-15 text (6)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `concepts/api-endpoint.md: stale_after = '2026-12-31'`
- `concepts/api-overview.md: stale_after = '2026-12-31'`
- `concepts/api-schema.md: stale_after = '2026-12-31'`
- `concepts/attested-computation.md: stale_after = '2026-12-31'`
- `concepts/metric.md: stale_after = '2026-12-31'`
- `concepts/playbook.md: stale_after = '2026-12-31'`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
