# okf-skills (scaccogatto)

Repository: <https://github.com/scaccogatto/okf-skills>
Checked at commit `49f8fb498798` (2026-10-21T11:51:11+02:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `examples/sample-bundle/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 8 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (5), `generated` (8), `verified` (5), `status` (8), `stale_after` (2) |
| Trust tiers (§5.3) | human-reviewed 5, unverified 3 |
| JidoSeal checker | score 67, tier silver |

## What to change

### Values that follow the 2026-08-15 text (7)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `datasets/orders-db.md: sources[].last_modified = '2026-06-17'`
- `metrics/checkout-conversion.md: stale_after = '2026-12-31'`
- `metrics/checkout-conversion.md: sources[].last_modified = '2026-06-17'`
- `runbooks/payment-failures.md: stale_after = '2026-12-31'`
- `services/auth-api.md: sources[].last_modified = '2026-06-12'`
- `services/orders-api.md: sources[].last_modified = '2026-06-15'`
- `services/payments-api.md: sources[].last_modified = '2026-06-16'`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
