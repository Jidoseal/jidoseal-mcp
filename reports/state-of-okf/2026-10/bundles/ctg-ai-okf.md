# ctg-ai-okf (claymoretechgroup)

Repository: <https://github.com/claymoretechgroup/ctg-ai-okf>
Checked at commit `1d7de0843fc0` (2026-09-02T20:17:25-05:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `test/fixtures/families/bundle-bad/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.1 |
| Concept files | 6 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | has values neither text allows |
| Trust and lifecycle fields used | `sources` (1), `generated` (2), `verified` (1), `status` (1), `stale_after` (1) |
| Trust tiers (§5.3) | machine-confirmed 1, unverified 5 |
| JidoSeal checker | score 39, tier bronze |

1 file(s) use the v0.1 `timestamp` key, which v0.2 supersedes with `generated: {by, at}` (§13.1); consumers may still fall back to it.

## What to change

### Timestamp values neither v0.2 text allows (1)

`generated.at` and `verified[].at` are datetimes in both texts (`2026-06-30T14:00:00Z`); `stale_after`, `sources[].last_modified` and `usage_window` are bare dates in the 2026-08-15 text and datetimes with an offset in the 2026-08-21 text. Placeholders such as `YYYY-MM-DD` left in a template are counted here too.

- `ideas/half-trusted.md: generated.at = '2026-06-20 22:53'`

### Values that follow the 2026-08-15 text (1)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `ideas/half-trusted.md: stale_after = '2026-09-23'`

### Documents past their `stale_after` (1)

OKF v0.2 §5.5: a concept is stale when now >= `stale_after`. Review the content, then move `stale_after` forward (and add a `verified` entry if someone confirmed it).

- `ideas/half-trusted.md: stale_after 2026-09-23T00:00:00Z`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
