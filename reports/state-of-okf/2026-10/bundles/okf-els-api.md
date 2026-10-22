# okf-els-api (chris-page-gov)

Repository: <https://github.com/chris-page-gov/okf-els-api>
Checked at commit `811a688183b0` (2026-08-18T20:14:14+01:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `bundle/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 38 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (38), `generated` (38), `status` (38) |
| Trust tiers (§5.3) | unverified 38 |
| JidoSeal checker | score 67, tier silver |

## What to change

### Values that follow the 2026-08-15 text (22)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `knowledge/service.md: sources[].last_modified = '2026-07-20'`
- `knowledge/service.md: sources[].last_modified = '2026-07-17'`
- `knowledge/issues/boundary-internal-api.md: sources[].last_modified = '2026-07-20'`
- `knowledge/issues/boundary-internal-api.md: sources[].last_modified = '2026-07-17'`
- `knowledge/issues/drift-data-hasgeo-default.md: sources[].last_modified = '2026-07-20'`
- `knowledge/issues/drift-data-hasgeo-default.md: sources[].last_modified = '2026-07-17'`
- `knowledge/issues/drift-data-includenames.md: sources[].last_modified = '2026-07-20'`
- `knowledge/issues/drift-data-includenames.md: sources[].last_modified = '2026-07-17'`
- `knowledge/issues/drift-geo-includedates.md: sources[].last_modified = '2026-07-20'`
- `knowledge/issues/drift-geo-includedates.md: sources[].last_modified = '2026-07-17'`
- `knowledge/issues/drift-metadata-dimension-route.md: sources[].last_modified = '2026-07-20'`
- `knowledge/issues/drift-metadata-dimension-route.md: sources[].last_modified = '2026-07-17'`
- `knowledge/issues/gap-compatibility-policy.md: sources[].last_modified = '2026-07-20'`
- `knowledge/issues/gap-compatibility-policy.md: sources[].last_modified = '2026-07-17'`
- `knowledge/issues/gap-data-measure.md: sources[].last_modified = '2026-07-20'`
- … and 7 more

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
