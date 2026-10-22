# oidm-knowledge (openimagingdata)

Repository: <https://github.com/openimagingdata/oidm-knowledge>
Checked at commit `948e2dc2ba0d` (2026-09-21T08:48:03Z), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `knowledge/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 115 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (114), `generated` (115), `status` (115), `stale_after` (18) |
| Trust tiers (§5.3) | unverified 115 |
| JidoSeal checker | score 67, tier silver |

## What to change

### Values that follow the 2026-08-15 text (35)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `applications/finding-and-location-coding.md: stale_after = '2027-09-21'`
- `applications/finding-and-location-coding.md: sources[].last_modified = '2026-03-16'`
- `applications/finding-and-location-coding.md: sources[].last_modified = '2026-02-19'`
- `applications/finding-and-location-coding.md: sources[].last_modified = '2026-06-10'`
- `applications/finding-model-forge.md: stale_after = '2027-09-21'`
- `applications/finding-model-forge.md: sources[].last_modified = '2025-08-31'`
- `applications/finding-model-forge.md: sources[].last_modified = '2025-11-27'`
- `applications/finding-models-site.md: stale_after = '2027-09-21'`
- `applications/imaging-problem-list-viewer.md: stale_after = '2027-09-21'`
- `applications/ipl-mvp-extraction.md: stale_after = '2027-09-21'`
- `applications/ipl-mvp-extraction.md: sources[].last_modified = '2025-10-20'`
- `applications/report-extraction-platform.md: stale_after = '2027-09-21'`
- `applications/report-extraction-platform.md: sources[].last_modified = '2026-07-07'`
- `applications/report-extraction-platform.md: sources[].last_modified = '2026-07-07'`
- `applications/report-extraction-platform.md: sources[].last_modified = '2026-07-20'`
- … and 20 more

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
