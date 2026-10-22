# okf-federation (manaty)

Repository: <https://github.com/manaty/okf-federation>
Checked at commit `7062b4da377a` (2026-08-13T14:31:10+07:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `(repository root)/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 16 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (2), `generated` (16), `verified` (1), `status` (16), `stale_after` (1) |
| Trust tiers (§5.3) | human-reviewed 1, unverified 15 |
| JidoSeal checker | score 67, tier silver |

## What to change

### Values that follow the 2026-08-15 text (1)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `examples/minimal/workspace/home/org/development-process.md: stale_after = '2027-08-13'`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
