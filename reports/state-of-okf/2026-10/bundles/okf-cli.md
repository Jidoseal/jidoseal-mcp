# okf-cli (auto-medica-labs)

Repository: <https://github.com/auto-medica-labs/okf-cli>
Checked at commit `7a548a8db805` (2026-10-11T13:31:09+07:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `example/computations/` (inferred: see the method) |
| `okf_version` declared | none |
| Concept files | 1 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (1), `verified` (1), `status` (1), `stale_after` (1) |
| Trust tiers (§5.3) | human-reviewed 1 |
| JidoSeal checker | score 33, tier bronze |

## What to change

### Values that follow the 2026-08-15 text (2)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `revenue.md: stale_after = '2026-12-31'`
- `revenue.md: sources[].last_modified = '2026-04-02'`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
