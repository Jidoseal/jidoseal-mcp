# okf-bundle (BlackBox-ai-lab)

Repository: <https://github.com/BlackBox-ai-lab/okf-bundle>
Checked at commit `04cc78d96372` (2026-08-05T21:35:39-05:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `out/bundle/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 10 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (9), `generated` (10), `verified` (9), `status` (10), `stale_after` (10) |
| Trust tiers (§5.3) | human-reviewed 1, machine-confirmed 8, unverified 1 |
| JidoSeal checker | score 67, tier silver |

## What to change

### Values that follow the 2026-08-15 text (19)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `components/ci-action.md: stale_after = '2026-07-04'`
- `components/ci-action.md: sources[].last_modified = '2026-07-27'`
- `components/scaffolder.md: stale_after = '2026-11-01'`
- `components/scaffolder.md: sources[].last_modified = '2026-07-27'`
- `components/stop-hook.md: stale_after = '2026-11-01'`
- `components/stop-hook.md: sources[].last_modified = '2026-08-02'`
- `components/validator.md: stale_after = '2026-11-01'`
- `components/validator.md: sources[].last_modified = '2026-07-27'`
- `components/visualizer.md: stale_after = '2026-11-01'`
- `components/visualizer.md: sources[].last_modified = '2026-07-27'`
- `decisions/vendor-the-spec.md: stale_after = '2026-11-01'`
- `reference/okf-spec.md: stale_after = '2026-11-01'`
- `reference/okf-spec.md: sources[].last_modified = '2026-07-27'`
- `skills/okf-skill.md: stale_after = '2026-11-01'`
- `skills/okf-skill.md: sources[].last_modified = '2026-07-27'`
- … and 4 more

### Documents past their `stale_after` (1)

OKF v0.2 §5.5: a concept is stale when now >= `stale_after`. Review the content, then move `stale_after` forward (and add a `verified` entry if someone confirmed it).

- `components/ci-action.md: stale_after 2026-07-04T00:00:00Z`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
