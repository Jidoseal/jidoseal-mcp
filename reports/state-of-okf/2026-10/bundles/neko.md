# neko (aqilputi)

Repository: <https://github.com/aqilputi/neko>
Checked at commit `918c7931c3ef` (2026-10-15T15:02:05-03:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `docs/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 9 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (2), `generated` (9), `status` (9), `stale_after` (1) |
| Trust tiers (§5.3) | unverified 9 |
| JidoSeal checker | score 67, tier silver |

9 file(s) use the v0.1 `timestamp` key, which v0.2 supersedes with `generated: {by, at}` (§13.1); consumers may still fall back to it.

## What to change

### Values that follow the 2026-08-15 text (1)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `fontes-de-dados.md: stale_after = '2027-01-15'`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
