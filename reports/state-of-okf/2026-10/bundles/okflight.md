# okflight (kriswill)

Repository: <https://github.com/kriswill/okflight>
Checked at commit `26b0f908640a` (2026-09-05T00:44:51-07:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `test/fixtures/cards-bundle/knowledge/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 124 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-21 text |
| Trust and lifecycle fields used | `sources` (3), `generated` (22), `verified` (12), `status` (10), `stale_after` (4) |
| Trust tiers (§5.3) | human-reviewed 8, machine-confirmed 4, unverified 112 |
| JidoSeal checker | score 36, tier bronze |

## What to change

### Documents past their `stale_after` (2)

OKF v0.2 §5.5: a concept is stale when now >= `stale_after`. Review the content, then move `stale_after` forward (and add a `verified` entry if someone confirmed it).

- `computations/p99-latency.md: stale_after 2026-08-01T00:00:00Z`
- `decisions/adr-014.md: stale_after 2026-06-30T00:00:00Z`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
