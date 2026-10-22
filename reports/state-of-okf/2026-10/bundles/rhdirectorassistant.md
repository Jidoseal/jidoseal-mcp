# RHDirectorAssistant (peterharrad)

Repository: <https://github.com/peterharrad/RHDirectorAssistant>
Checked at commit `f89c05281e0c` (2026-09-15T19:35:22+01:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `okf-bundle/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 465 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | has values neither text allows |
| Trust and lifecycle fields used | `sources` (462), `generated` (463), `status` (465) |
| Trust tiers (§5.3) | unverified 465 |
| JidoSeal checker | score 66, tier bronze |

## What to change

### Timestamp values neither v0.2 text allows (1)

`generated.at` and `verified[].at` are datetimes in both texts (`2026-06-30T14:00:00Z`); `stale_after`, `sources[].last_modified` and `usage_window` are bare dates in the 2026-08-15 text and datetimes with an offset in the 2026-08-21 text. Placeholders such as `YYYY-MM-DD` left in a template are counted here too.

- `building/riverside-house.md: sources[].last_modified = '2026-09'`

### Values that follow the 2026-08-15 text (461)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `agreements/agency-agreement/appendix-01.md: sources[].last_modified = '2026-08-13'`
- `agreements/agency-agreement/appendix-02.md: sources[].last_modified = '2026-08-13'`
- `agreements/agency-agreement/appendix-03.md: sources[].last_modified = '2026-08-13'`
- `agreements/agency-agreement/appendix-04.md: sources[].last_modified = '2026-08-13'`
- `agreements/agency-agreement/appendix-05.md: sources[].last_modified = '2026-08-13'`
- `agreements/agency-agreement/appendix-06.md: sources[].last_modified = '2026-08-13'`
- `agreements/agency-agreement/appendix-07.md: sources[].last_modified = '2026-08-13'`
- `agreements/agency-agreement/appendix-08.md: sources[].last_modified = '2026-08-13'`
- `agreements/agency-agreement/appendix-09.md: sources[].last_modified = '2026-08-13'`
- `agreements/agency-agreement/clause-01-01.md: sources[].last_modified = '2026-08-13'`
- `agreements/agency-agreement/clause-01-02.md: sources[].last_modified = '2026-08-13'`
- `agreements/agency-agreement/clause-02-01.md: sources[].last_modified = '2026-08-13'`
- `agreements/agency-agreement/clause-02-02.md: sources[].last_modified = '2026-08-13'`
- `agreements/agency-agreement/clause-02-03.md: sources[].last_modified = '2026-08-13'`
- `agreements/agency-agreement/clause-03-01.md: sources[].last_modified = '2026-08-13'`
- … and 446 more

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
