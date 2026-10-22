# lokf (nicholsn)

Repository: <https://github.com/nicholsn/lokf>
Checked at commit `80404397fcee` (2026-10-20T10:22:25-07:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `examples/acme-knowledge/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 8 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (2), `generated` (3), `verified` (4), `status` (2), `stale_after` (3) |
| Trust tiers (§5.3) | human-reviewed 2, machine-confirmed 2, unverified 4 |
| JidoSeal checker | score 42, tier bronze |

4 file(s) use the v0.1 `timestamp` key, which v0.2 supersedes with `generated: {by, at}` (§13.1); consumers may still fall back to it.

## What to change

### Values that follow the 2026-08-15 text (7)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `computations/weekly-active-users-count.md: stale_after = '2026-12-31'`
- `computations/weekly-active-users-count.md: sources[].last_modified = '2026-05-12'`
- `metrics/weekly-active-users.md: stale_after = '2026-12-31'`
- `metrics/weekly-active-users.md: sources[].last_modified = '2026-05-12'`
- `metrics/weekly-active-users.md: usage_window.from = '2026-06-01'`
- `metrics/weekly-active-users.md: usage_window.to = '2026-06-30'`
- `services/analytics-api.md: stale_after = '2026-07-01'`

### Documents past their `stale_after` (1)

OKF v0.2 §5.5: a concept is stale when now >= `stale_after`. Review the content, then move `stale_after` forward (and add a `verified` entry if someone confirmed it).

- `services/analytics-api.md: stale_after 2026-07-01T00:00:00Z`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
