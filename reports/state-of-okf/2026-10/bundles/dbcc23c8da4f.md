# Bundle dbcc23c8da4f

Checked at commit `5543012b182a` (2026-08-15T21:59:09+09:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `docs/` (inferred: see the method) |
| `okf_version` declared | none |
| Concept files | 8 |
| OKF v0.2 conformance (§11, items 1–2) | not yet: 4 file(s) to change |
| Timestamps follow | fits both texts |
| Trust and lifecycle fields used | `sources` (4), `generated` (4), `status` (4) |
| Trust tiers (§5.3) | unverified 8 |
| JidoSeal checker | score 33, tier none |

## What to change

### Files with frontmatter but no `type` (4)

`type` is the one key OKF v0.2 always requires (§4.1). Any short descriptive string works, for example `type: Reference`.

- `README.md`
- `architecture/README.md`
- `domain/README.md`
- `infrastructure/README.md`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
