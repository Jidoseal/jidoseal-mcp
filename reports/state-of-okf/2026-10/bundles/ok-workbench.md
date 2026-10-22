# ok-workbench (edoloughlin)

Repository: <https://github.com/edoloughlin/ok-workbench>
Checked at commit `3f34507d6206` (2026-10-21T22:39:20+01:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `ok-workbench-planning/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 5 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | has values neither text allows |
| Trust and lifecycle fields used | `status` (4), `stale_after` (1) |
| Trust tiers (§5.3) | unverified 5 |
| JidoSeal checker | score 33, tier bronze |

## What to change

### Timestamp values neither v0.2 text allows (1)

`generated.at` and `verified[].at` are datetimes in both texts (`2026-06-30T14:00:00Z`); `stale_after`, `sources[].last_modified` and `usage_window` are bare dates in the 2026-08-15 text and datetimes with an offset in the 2026-08-21 text. Placeholders such as `YYYY-MM-DD` left in a template are counted here too.

- `status.md: stale_after = 'P7D'`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
