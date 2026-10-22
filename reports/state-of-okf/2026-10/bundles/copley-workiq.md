# copley-workiq (chris-mcnulty)

Repository: <https://github.com/chris-mcnulty/copley-workiq>
Checked at commit `108d50acf8ce` (2026-10-16T16:35:43-07:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `examples/` (inferred: see the method) |
| `okf_version` declared | none |
| Concept files | 5 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (5), `generated` (1), `verified` (1), `status` (5), `stale_after` (5) |
| Trust tiers (§5.3) | human-reviewed 1, unverified 4 |
| JidoSeal checker | score 40, tier bronze |

## What to change

### Values that follow the 2026-08-15 text (10)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `fictional-company/processes/customer-renewal.md: stale_after = '2026-10-01'`
- `fictional-company/processes/customer-renewal.md: sources[].last_modified = '2026-07-15'`
- `sample-agent/agent-record.md: stale_after = '2026-10-24'`
- `sample-agent/agent-record.md: sources[].last_modified = '2026-07-18'`
- `sample-agent/skill-renewal-summary.md: stale_after = '2026-10-24'`
- `sample-agent/skill-renewal-summary.md: sources[].last_modified = '2026-07-10'`
- `sample-metric-attestation/net-retention-metric.md: stale_after = '2026-10-15'`
- `sample-metric-attestation/net-retention-metric.md: sources[].last_modified = '2026-07-11'`
- `sample-process/incident-handoff.md: stale_after = '2026-09-30'`
- `sample-process/incident-handoff.md: sources[].last_modified = '2026-07-12'`

### Documents past their `stale_after` (3)

OKF v0.2 §5.5: a concept is stale when now >= `stale_after`. Review the content, then move `stale_after` forward (and add a `verified` entry if someone confirmed it).

- `fictional-company/processes/customer-renewal.md: stale_after 2026-10-01T00:00:00Z`
- `sample-metric-attestation/net-retention-metric.md: stale_after 2026-10-15T00:00:00Z`
- `sample-process/incident-handoff.md: stale_after 2026-09-30T00:00:00Z`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
