# okf-ts (Zenb0t)

Repository: <https://github.com/Zenb0t/okf-ts>
Checked at commit `6c88b6c301cb` (2026-08-10T21:58:39-07:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `examples/knowledge/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 4 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (2), `generated` (2), `verified` (3), `status` (4), `stale_after` (1) |
| Trust tiers (§5.3) | human-reviewed 2, machine-confirmed 1, unverified 1 |
| JidoSeal checker | score 50, tier bronze |

## What to change

### Values that follow the 2026-08-15 text (2)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `metrics/monthly-recurring-revenue.md: stale_after = '2027-08-09'`
- `metrics/monthly-recurring-revenue.md: sources[].last_modified = '2026-08-09'`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
