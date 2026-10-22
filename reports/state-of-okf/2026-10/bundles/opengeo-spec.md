# opengeo-spec (cangqiaoGEO)

Repository: <https://github.com/cangqiaoGEO/opengeo-spec>
Checked at commit `2360468ce184` (2026-09-02T14:57:26+08:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `template/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 12 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | has values neither text allows |
| Trust and lifecycle fields used | `sources` (1), `generated` (12), `verified` (3), `status` (12), `stale_after` (1) |
| Trust tiers (§5.3) | human-reviewed 3, unverified 9 |
| JidoSeal checker | score 67, tier silver |

## What to change

### Timestamp values neither v0.2 text allows (11)

`generated.at` and `verified[].at` are datetimes in both texts (`2026-06-30T14:00:00Z`); `stale_after`, `sources[].last_modified` and `usage_window` are bare dates in the 2026-08-15 text and datetimes with an offset in the 2026-08-21 text. Placeholders such as `YYYY-MM-DD` left in a template are counted here too.

- `audience.md: generated.at = '<ISO时间>'`
- `boundaries.md: generated.at = '<ISO时间>'`
- `channels.md: generated.at = '<ISO时间>'`
- `faq.md: generated.at = '<ISO时间>'`
- `identity.md: generated.at = '<ISO时间>'`
- `positioning.md: generated.at = '<ISO时间>'`
- `evidence/_template.md: sources[].last_modified = '<YYYY-MM-DD>'`
- `evidence/_template.md: generated.at = '<ISO时间>'`
- `monitors/weekly.md: generated.at = '<ISO时间>'`
- `products/_template.md: stale_after = '<价格有效期，YYYY-MM-DD，必填>'`
- `products/_template.md: generated.at = '<ISO时间>'`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
