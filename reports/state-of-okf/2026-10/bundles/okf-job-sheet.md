# okf-job-sheet (muhaj)

Repository: <https://github.com/muhaj/okf-job-sheet>
Checked at commit `3896553c72c1` (2026-08-12T10:32:46+01:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `bundles/builder/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 13 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (13), `generated` (13), `verified` (13), `status` (13), `stale_after` (4) |
| Trust tiers (§5.3) | human-reviewed 13 |
| JidoSeal checker | score 67, tier silver |

## What to change

### Values that follow the 2026-08-15 text (17)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `business/credentials.md: sources[].last_modified = '2026-08-09'`
- `business/identity.md: sources[].last_modified = '2026-08-09'`
- `business/service-area.md: sources[].last_modified = '2026-08-09'`
- `computations/job-estimate.md: stale_after = '2027-02-28'`
- `computations/job-estimate.md: sources[].last_modified = '2026-08-09'`
- `intake/questions.md: sources[].last_modified = '2026-08-09'`
- `operations/access.md: sources[].last_modified = '2026-08-09'`
- `operations/availability.md: sources[].last_modified = '2026-08-09'`
- `operations/escalation.md: sources[].last_modified = '2026-08-09'`
- `pricing/method.md: stale_after = '2027-02-28'`
- `pricing/method.md: sources[].last_modified = '2026-08-09'`
- `pricing/rates.md: stale_after = '2027-02-28'`
- `pricing/rates.md: sources[].last_modified = '2026-08-09'`
- `pricing/terms.md: stale_after = '2027-02-28'`
- `pricing/terms.md: sources[].last_modified = '2026-08-09'`
- … and 2 more

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
