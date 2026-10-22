# nkb-legal-okf-sample (drapermcp)

Repository: <https://github.com/drapermcp/nkb-legal-okf-sample>
Checked at commit `934cecdb89df` (2026-09-14T07:55:37-05:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `(repository root)/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 267 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | has values neither text allows |
| Trust and lifecycle fields used | `sources` (264), `generated` (264), `status` (264) |
| Trust tiers (§5.3) | unverified 267 |
| JidoSeal checker | score 33, tier bronze |

## What to change

### Timestamp values neither v0.2 text allows (528)

`generated.at` and `verified[].at` are datetimes in both texts (`2026-06-30T14:00:00Z`); `stale_after`, `sources[].last_modified` and `usage_window` are bare dates in the 2026-08-15 text and datetimes with an offset in the 2026-08-21 text. Placeholders such as `YYYY-MM-DD` left in a template are counted here too.

- `nodes/wyoming-criminal-section-6-1-101.md: sources[].last_modified = '2024'`
- `nodes/wyoming-criminal-section-6-1-101.md: generated.at = '2026-02-22'`
- `nodes/wyoming-criminal-section-6-1-102.md: sources[].last_modified = '2024'`
- `nodes/wyoming-criminal-section-6-1-102.md: generated.at = '2026-02-22'`
- `nodes/wyoming-criminal-section-6-1-103.md: sources[].last_modified = '2024'`
- `nodes/wyoming-criminal-section-6-1-103.md: generated.at = '2026-02-22'`
- `nodes/wyoming-criminal-section-6-1-104.md: sources[].last_modified = '2024'`
- `nodes/wyoming-criminal-section-6-1-104.md: generated.at = '2026-02-22'`
- `nodes/wyoming-criminal-section-6-1-201.md: sources[].last_modified = '2024'`
- `nodes/wyoming-criminal-section-6-1-201.md: generated.at = '2026-02-22'`
- `nodes/wyoming-criminal-section-6-1-202.md: sources[].last_modified = '2024'`
- `nodes/wyoming-criminal-section-6-1-202.md: generated.at = '2026-02-22'`
- `nodes/wyoming-criminal-section-6-1-203.md: sources[].last_modified = '2024'`
- `nodes/wyoming-criminal-section-6-1-203.md: generated.at = '2026-02-22'`
- `nodes/wyoming-criminal-section-6-1-204.md: sources[].last_modified = '2024'`
- … and 513 more

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
