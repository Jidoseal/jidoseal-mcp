# software-supply-chain-landscape (jrjsmrtn)

Repository: <https://github.com/jrjsmrtn/software-supply-chain-landscape>
Checked at commit `9b47530e18bf` (2026-10-08T23:55:48+02:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `knowledge/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 73 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | has values neither text allows |
| Trust and lifecycle fields used | `sources` (73), `generated` (73), `verified` (72), `status` (73), `stale_after` (73) |
| Trust tiers (§5.3) | machine-confirmed 72, unverified 1 |
| JidoSeal checker | score 67, tier silver |

## What to change

### Timestamp values neither v0.2 text allows (4)

`generated.at` and `verified[].at` are datetimes in both texts (`2026-06-30T14:00:00Z`); `stale_after`, `sources[].last_modified` and `usage_window` are bare dates in the 2026-08-15 text and datetimes with an offset in the 2026-08-21 text. Placeholders such as `YYYY-MM-DD` left in a template are counted here too.

- `disclosure/datasheets-for-datasets.md: sources[].last_modified = '2018-03'`
- `disclosure/model-cards.md: sources[].last_modified = '2019-01'`
- `distribution/tea.md: sources[].last_modified = '2025-12'`
- `intelligence/vex.md: sources[].last_modified = '2022-06'`

### Values that follow the 2026-08-15 text (103)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `landscape.md: stale_after = '2028-08-01'`
- `bom-types/cbom.md: stale_after = '2027-08-01'`
- `bom-types/hbom.md: stale_after = '2027-08-01'`
- `bom-types/mbom.md: stale_after = '2027-08-01'`
- `bom-types/ml-bom.md: stale_after = '2027-08-01'`
- `bom-types/obom.md: stale_after = '2027-08-01'`
- `bom-types/saasbom.md: stale_after = '2027-08-01'`
- `bom-types/sbom.md: stale_after = '2027-08-01'`
- `disclosure/datasheets-for-datasets.md: stale_after = '2027-08-01'`
- `disclosure/model-cards.md: stale_after = '2027-08-01'`
- `distribution/tea.md: stale_after = '2027-01-08'`
- `distribution/tea.md: sources[].last_modified = '2026-10-08'`
- `distribution/tea.md: sources[].last_modified = '2026-10-07'`
- `distribution/tea.md: sources[].last_modified = '2026-09-30'`
- `distribution/tea.md: sources[].last_modified = '2026-01-16'`
- … and 88 more

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
