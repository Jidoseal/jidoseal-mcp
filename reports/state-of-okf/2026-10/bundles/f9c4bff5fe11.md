# Bundle f9c4bff5fe11

Checked at commit `c7e3bd3232a2` (2026-10-14T18:16:00+10:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `(repository root)/` (inferred: see the method) |
| `okf_version` declared | none |
| Concept files | 1293 |
| OKF v0.2 conformance (§11, items 1–2) | not yet: 3 file(s) to change |
| Timestamps follow | has values neither text allows |
| Trust and lifecycle fields used | `sources` (1289), `generated` (1289), `verified` (10), `status` (1290), `stale_after` (10) |
| Trust tiers (§5.3) | machine-confirmed 10, unverified 1280 |
| JidoSeal checker | score 67, tier none |

## What to change

### Files with no frontmatter block (3)

OKF v0.2 §11 asks every `.md` file other than `index.md` and `log.md` to start with a YAML frontmatter block holding a non-empty `type`. The smallest change is:

```yaml
---
type: Note
---
```

If these files are not meant to be part of the bundle (a README, a changelog), moving the bundle into its own folder keeps them out.

- `README.md`
- `SECURITY.md`
- `examples/client-a-answer.md`

### Timestamp values neither v0.2 text allows (24)

`generated.at` and `verified[].at` are datetimes in both texts (`2026-06-30T14:00:00Z`); `stale_after`, `sources[].last_modified` and `usage_window` are bare dates in the 2026-08-15 text and datetimes with an offset in the 2026-08-21 text. Placeholders such as `YYYY-MM-DD` left in a template are counted here too.

- `okf/atlas/columns/anthropic/c1-1.md: verified[].at = '2026-10-10'`
- `okf/atlas/columns/anthropic/c1-1.md: verified[].at = '2026-10-10'`
- `okf/atlas/columns/anthropic/c1-2.md: verified[].at = '2026-10-10'`
- `okf/atlas/columns/anthropic/c1-2.md: verified[].at = '2026-10-10'`
- `okf/atlas/columns/anthropic/c1-3.md: verified[].at = '2026-10-10'`
- `okf/atlas/columns/anthropic/c2-3.md: verified[].at = '2026-10-10'`
- `okf/atlas/columns/anthropic/c2-3.md: verified[].at = '2026-10-10'`
- `okf/atlas/columns/openai/c1-3.md: verified[].at = '2026-10-10'`
- `okf/atlas/columns/openai/c1-3.md: verified[].at = '2026-10-10'`
- `okf/atlas/columns/wiz/c6-1.md: verified[].at = '2026-10-14'`
- `okf/atlas/columns/wiz/c6-1.md: verified[].at = '2026-10-14'`
- `okf/atlas/columns/wiz/c6-11.md: verified[].at = '2026-10-14'`
- `okf/atlas/columns/wiz/c6-11.md: verified[].at = '2026-10-14'`
- `okf/atlas/columns/wiz/c7-10.md: verified[].at = '2026-10-14'`
- `okf/atlas/columns/wiz/c7-10.md: verified[].at = '2026-10-14'`
- … and 9 more

### Values that follow the 2026-08-15 text (10)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `okf/atlas/columns/anthropic/c1-1.md: stale_after = '2026-11-07'`
- `okf/atlas/columns/anthropic/c1-2.md: stale_after = '2026-11-07'`
- `okf/atlas/columns/anthropic/c1-3.md: stale_after = '2026-11-07'`
- `okf/atlas/columns/anthropic/c2-3.md: stale_after = '2026-11-07'`
- `okf/atlas/columns/openai/c1-3.md: stale_after = '2026-11-07'`
- `okf/atlas/columns/wiz/c6-1.md: stale_after = '2026-11-08'`
- `okf/atlas/columns/wiz/c6-11.md: stale_after = '2026-11-08'`
- `okf/atlas/columns/wiz/c7-10.md: stale_after = '2026-11-08'`
- `okf/atlas/columns/wiz/c7-3.md: stale_after = '2026-11-08'`
- `okf/atlas/columns/wiz/c7-5.md: stale_after = '2026-11-08'`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
