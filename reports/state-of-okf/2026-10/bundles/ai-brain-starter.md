# ai-brain-starter (david-wulf)

Repository: <https://github.com/david-wulf/ai-brain-starter>
Checked at commit `bb162c3b705a` (2026-10-20T22:36:54+02:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `okf/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 15 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | has values neither text allows |
| Trust and lifecycle fields used | `sources` (3), `generated` (15), `verified` (15), `status` (15), `stale_after` (1) |
| Trust tiers (§5.3) | unverified 15 |
| JidoSeal checker | score 67, tier silver |

## What to change

### Timestamp values neither v0.2 text allows (16)

`generated.at` and `verified[].at` are datetimes in both texts (`2026-06-30T14:00:00Z`); `stale_after`, `sources[].last_modified` and `usage_window` are bare dates in the 2026-08-15 text and datetimes with an offset in the 2026-08-21 text. Placeholders such as `YYYY-MM-DD` left in a template are counted here too.

- `okf-spec.md: generated.at = '2026-09-28'`
- `arbeit/beispiel-decision.md: stale_after = 'None'`
- `arbeit/beispiel-decision.md: generated.at = '2026-08-24'`
- `arbeit/ordner1/memory/decisions/beispiel-entscheidung.md: generated.at = '2026-10-18'`
- `arbeit/ordner1/memory/meetings/2026-10-01-beispiel-meeting.md: generated.at = '2026-10-18'`
- `arbeit/ordner1/memory/patterns/beispiel-muster.md: generated.at = '2026-10-18'`
- `arbeit/ordner1/soul/never-do.md: generated.at = '2026-10-18'`
- `arbeit/ordner1/soul/profil.md: generated.at = '2026-10-18'`
- `arbeit/ordner2/beispiel-kennzahl.md: generated.at = '2026-10-18'`
- `arbeit/ordner2/beispiel-prozess.md: generated.at = '2026-10-18'`
- `arbeit/quellen/beispiel-quelle.md: generated.at = '2026-10-18'`
- `methoden/beispiel-playbook.md: generated.at = '2026-08-20'`
- `privat/ordner1/beispiel-notiz.md: generated.at = '2026-10-18'`
- `privat/ordner1/beispiel-stammdaten.md: generated.at = '2026-10-18'`
- `privat/ordner2/beispiel-projekt.md: generated.at = '2026-10-18'`
- … and 1 more

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
