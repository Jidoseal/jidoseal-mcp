# context-vault (SeeingBlue)

Repository: <https://github.com/SeeingBlue/context-vault>
Checked at commit `18d518984ead` (2026-09-13T15:58:53-04:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `(repository root)/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 56 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | has values neither text allows |
| Trust and lifecycle fields used | `sources` (2), `generated` (55), `status` (56) |
| Trust tiers (§5.3) | unverified 56 |
| JidoSeal checker | score 66, tier bronze |

## What to change

### Timestamp values neither v0.2 text allows (9)

`generated.at` and `verified[].at` are datetimes in both texts (`2026-06-30T14:00:00Z`); `stale_after`, `sources[].last_modified` and `usage_window` are bare dates in the 2026-08-15 text and datetimes with an offset in the 2026-08-21 text. Placeholders such as `YYYY-MM-DD` left in a template are counted here too.

- `_templates/_template-contact.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`
- `_templates/_template-daily.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`
- `_templates/_template-digest.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`
- `_templates/_template-goal.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`
- `_templates/_template-meeting.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`
- `_templates/_template-note.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`
- `_templates/_template-preference.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`
- `_templates/_template-project.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`
- `_templates/_template-routine.md: generated.at = 'YYYY-MM-DDT00:00:00Z'`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
