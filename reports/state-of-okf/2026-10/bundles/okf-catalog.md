# okf-catalog (drathm)

Repository: <https://github.com/drathm/okf-catalog>
Checked at commit `5739aefcf962` (2026-10-08T06:08:37-04:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `test/fixtures/bundles/behaviours/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 19 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | has values neither text allows |
| Trust and lifecycle fields used | `sources` (1), `generated` (4), `verified` (6), `status` (11), `stale_after` (5) |
| Trust tiers (§5.3) | human-reviewed 5, machine-confirmed 1, unverified 13 |
| JidoSeal checker | score 39, tier bronze |

## What to change

### Timestamp values neither v0.2 text allows (2)

`generated.at` and `verified[].at` are datetimes in both texts (`2026-06-30T14:00:00Z`); `stale_after`, `sources[].last_modified` and `usage_window` are bare dates in the 2026-08-15 text and datetimes with an offset in the 2026-08-21 text. Placeholders such as `YYYY-MM-DD` left in a template are counted here too.

- `terms/eta.md: stale_after = 'soon'`
- `terms/theta.md: stale_after = '2000-06-01T18:00:00'`

### Values that follow the 2026-08-15 text (5)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `terms/alpha.md: stale_after = '2999-12-31'`
- `terms/alpha.md: sources[].last_modified = '2000-01-20'`
- `terms/alpha.md: usage_window.from = '2000-01-01'`
- `terms/alpha.md: usage_window.to = '2000-01-31'`
- `terms/zeta.md: stale_after = '2000-01-31'`

### Documents past their `stale_after` (3)

OKF v0.2 §5.5: a concept is stale when now >= `stale_after`. Review the content, then move `stale_after` forward (and add a `verified` entry if someone confirmed it).

- `terms/beta.md: stale_after 2000-06-01T18:00:00Z`
- `terms/theta.md: stale_after 2000-06-01T18:00:00Z`
- `terms/zeta.md: stale_after 2000-01-31T00:00:00Z`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
