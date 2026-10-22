# dev-workspace (iwe-org)

Repository: <https://github.com/iwe-org/dev-workspace>
Checked at commit `249943bcc30a` (2026-08-09T19:35:56-04:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `data/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 32 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (5), `generated` (32), `verified` (4), `status` (2), `stale_after` (4) |
| Trust tiers (§5.3) | human-reviewed 4, unverified 28 |
| JidoSeal checker | score 33, tier bronze |

## What to change

### Values that follow the 2026-08-15 text (9)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `architecture/state-model.example.md: sources[].last_modified = '2026-07-25'`
- `codebase/flow-session-lifecycle.example.md: stale_after = '2026-11-01'`
- `codebase/flow-session-lifecycle.example.md: sources[].last_modified = '2026-07-25'`
- `codebase/store.example.md: stale_after = '2026-11-01'`
- `codebase/store.example.md: sources[].last_modified = '2026-07-25'`
- `codebase/timer.example.md: stale_after = '2026-11-01'`
- `codebase/timer.example.md: sources[].last_modified = '2026-07-25'`
- `codebase/store/streak.example.md: stale_after = '2026-11-01'`
- `codebase/store/streak.example.md: sources[].last_modified = '2026-07-25'`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
