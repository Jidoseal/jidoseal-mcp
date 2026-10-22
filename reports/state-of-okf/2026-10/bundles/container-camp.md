# container-camp (UNM-CARC)

Repository: <https://github.com/UNM-CARC/container-camp>
Checked at commit `1d5e7e61b028` (2026-09-11T07:53:57-06:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `docs/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 33 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-21 text |
| Trust and lifecycle fields used | `sources` (33), `generated` (33), `stale_after` (2) |
| Trust tiers (§5.3) | unverified 33 |
| JidoSeal checker | score 67, tier silver |

## What to change

### Documents past their `stale_after` (2)

OKF v0.2 §5.5: a concept is stale when now >= `stale_after`. Review the content, then move `stale_after` forward (and add a `verified` entry if someone confirmed it).

- `getting-started/schedule-basics.md: stale_after 2023-03-09T00:00:00Z`
- `getting-started/schedule.md: stale_after 2023-08-19T00:00:00Z`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
