# guide_okf (demouv-projects)

Repository: <https://github.com/demouv-projects/guide_okf>
Checked at commit `11b3f1265e49` (2026-08-13T08:11:02+02:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `(repository root)/` (inferred: see the method) |
| `okf_version` declared | none |
| Concept files | 44 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (39), `generated` (44), `verified` (44), `status` (44), `stale_after` (44) |
| Trust tiers (§5.3) | unverified 44 |
| JidoSeal checker | score 67, tier silver |

## What to change

### Values that follow the 2026-08-15 text (44)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `README.md: stale_after = '2026-11-12'`
- `chapters/01-introduction.md: stale_after = '2026-11-12'`
- `chapters/02-historique.md: stale_after = '2026-11-12'`
- `chapters/03-probleme.md: stale_after = '2026-11-12'`
- `chapters/04-definition.md: stale_after = '2026-11-12'`
- `chapters/05-principes.md: stale_after = '2026-11-12'`
- `chapters/06-anatomie-bundle.md: stale_after = '2026-11-12'`
- `chapters/07-anatomie-concept.md: stale_after = '2026-11-12'`
- `chapters/08-exemples.md: stale_after = '2026-11-12'`
- `chapters/09-liens-graphe.md: stale_after = '2026-11-12'`
- `chapters/10-conformite.md: stale_after = '2026-11-12'`
- `chapters/11-okf-vs-rag.md: stale_after = '2026-11-12'`
- `chapters/12-okf-vs-outils.md: stale_after = '2026-11-12'`
- `chapters/13-workflow.md: stale_after = '2026-11-12'`
- `chapters/14-premier-bundle.md: stale_after = '2026-11-12'`
- … and 29 more

### Documents past their `stale_after` (5)

OKF v0.2 §5.5: a concept is stale when now >= `stale_after`. Review the content, then move `stale_after` forward (and add a `verified` entry if someone confirmed it).

- `sources/google-cloud-okf-introduction.md: stale_after 2026-09-12T00:00:00Z`
- `sources/google-cloud-okf-v02-trust.md: stale_after 2026-09-12T00:00:00Z`
- `sources/googlecloudplatform-knowledge-catalog.md: stale_after 2026-09-12T00:00:00Z`
- `sources/okf-spec-v02.md: stale_after 2026-09-12T00:00:00Z`
- `sources/openknowledgeformat-fr.md: stale_after 2026-09-12T00:00:00Z`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
