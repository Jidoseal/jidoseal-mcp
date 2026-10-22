# okfsmith (Bilal-Junaid-Jiwani)

Repository: <https://github.com/Bilal-Junaid-Jiwani/okfsmith>
Checked at commit `3d069bba8c7b` (2026-10-21T10:25:56+05:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `examples/bundles/cs-curriculum/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 7 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (7), `generated` (5), `verified` (3), `status` (7), `stale_after` (3) |
| Trust tiers (§5.3) | human-reviewed 3, unverified 4 |
| JidoSeal checker | score 57, tier bronze |

## What to change

### Values that follow the 2026-08-15 text (3)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `courses/cs101.md: stale_after = '2027-09-26'`
- `resources/sicp.md: stale_after = '2027-09-26'`
- `topics/recursion.md: stale_after = '2027-09-26'`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
