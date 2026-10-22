# okf-wiki (tom-jordan23)

Repository: <https://github.com/tom-jordan23/okf-wiki>
Checked at commit `8f6c7af2c73d` (2026-09-25T09:38:54-05:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `okf/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 41 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | has values neither text allows |
| Trust and lifecycle fields used | `sources` (35), `generated` (11), `verified` (11), `status` (41), `stale_after` (41) |
| Trust tiers (§5.3) | machine-confirmed 11, unverified 30 |
| JidoSeal checker | score 37, tier bronze |

30 file(s) use the v0.1 `timestamp` key, which v0.2 supersedes with `generated: {by, at}` (§13.1); consumers may still fall back to it.

## What to change

### Timestamp values neither v0.2 text allows (22)

`generated.at` and `verified[].at` are datetimes in both texts (`2026-06-30T14:00:00Z`); `stale_after`, `sources[].last_modified` and `usage_window` are bare dates in the 2026-08-15 text and datetimes with an offset in the 2026-08-21 text. Placeholders such as `YYYY-MM-DD` left in a template are counted here too.

- `templates/architecture.md: stale_after = 'YYYY-MM-DDT00:00:00Z'`
- `templates/architecture.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`
- `templates/concept.md: stale_after = 'YYYY-MM-DDT00:00:00Z'`
- `templates/concept.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`
- `templates/criterion.md: stale_after = 'YYYY-MM-DDT00:00:00Z'`
- `templates/criterion.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`
- `templates/decision.md: stale_after = 'YYYY-MM-DDT00:00:00Z'`
- `templates/decision.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`
- `templates/finding.md: stale_after = 'YYYY-MM-DDT00:00:00Z'`
- `templates/finding.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`
- `templates/gate.md: stale_after = 'YYYY-MM-DDT00:00:00Z'`
- `templates/gate.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`
- `templates/option.md: stale_after = 'YYYY-MM-DDT00:00:00Z'`
- `templates/option.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`
- `templates/recommendation.md: stale_after = 'YYYY-MM-DDT00:00:00Z'`
- … and 7 more

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
