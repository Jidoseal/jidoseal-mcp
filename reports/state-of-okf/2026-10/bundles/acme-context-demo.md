# acme-context-demo (GDG-PVD)

Repository: <https://github.com/GDG-PVD/acme-context-demo>
Checked at commit `95b9427d2dbe` (2026-08-13T12:58:24-04:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `memory/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 6 |
| OKF v0.2 conformance (§11, items 1–2) | meets it |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (6), `generated` (6), `verified` (5), `status` (6), `stale_after` (1) |
| Trust tiers (§5.3) | human-reviewed 5, unverified 1 |
| JidoSeal checker | score 67, tier silver |

## What to change

### Values that follow the 2026-08-15 text (6)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `acme/finance/renewal_terms.md: sources[].last_modified = '2026-04-09'`
- `acme/pricing/discount_authority.md: sources[].last_modified = '2026-07-02'`
- `acme/product/icp_definition.md: sources[].last_modified = '2026-06-18'`
- `acme/security/subprocessors.md: stale_after = '2026-06-30'`
- `acme/security/subprocessors.md: sources[].last_modified = '2026-01-30'`
- `acme/support/escalation_path.md: sources[].last_modified = '2026-05-11'`

### Documents past their `stale_after` (1)

OKF v0.2 §5.5: a concept is stale when now >= `stale_after`. Review the content, then move `stale_after` forward (and add a `verified` entry if someone confirmed it).

- `acme/security/subprocessors.md: stale_after 2026-06-30T00:00:00Z`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
