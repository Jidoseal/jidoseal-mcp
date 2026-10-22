# Bundle bdbaa2f7bcc9

Checked at commit `c04ae2e156ca` (2026-09-20T20:03:55-07:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `knowledge/asdc/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 14 |
| OKF v0.2 conformance (§11, items 1–2) | not yet: 1 file(s) to change |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (13), `generated` (13), `verified` (13), `status` (13), `stale_after` (13) |
| Trust tiers (§5.3) | human-reviewed 13 |
| JidoSeal checker | score 62, tier none |

## What to change

### Files with no frontmatter block (1)

OKF v0.2 §11 asks every `.md` file other than `index.md` and `log.md` to start with a YAML frontmatter block holding a non-empty `type`. The smallest change is:

```yaml
---
type: Note
---
```

If these files are not meant to be part of the bundle (a README, a changelog), moving the bundle into its own folder keeps them out.

- `DIGEST.md`

### Values that follow the 2026-08-15 text (13)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `conventions/ceres-clear-sky-conventions.md: stale_after = '2027-03-19'`
- `datasets/ceres-ebaf-ed4-2.md: stale_after = '2027-03-14'`
- `datasets/ceres-syn1deg.md: stale_after = '2027-03-19'`
- `gotchas/ebaf-clear-sky-definitions.md: stale_after = '2027-03-14'`
- `gotchas/ebaf-climatology-baseline.md: stale_after = '2027-03-14'`
- `gotchas/ebaf-imbalance-anchored-to-ocean-heating.md: stale_after = '2027-03-14'`
- `gotchas/ebaf-surface-fluxes-are-modelled.md: stale_after = '2027-03-14'`
- `gotchas/ebaf-versus-syn1deg-versus-ssf.md: stale_after = '2027-03-14'`
- `gotchas/syn1deg-geostationary-artifacts.md: stale_after = '2027-03-19'`
- `gotchas/syn1deg-refuses-long-term-trend-use.md: stale_after = '2027-03-19'`
- `gotchas/syn1deg-surface-fluxes-are-modelled-not-measured.md: stale_after = '2027-03-19'`
- `recipes/cloud-radiative-effect.md: stale_after = '2027-03-19'`
- `recipes/energy-budget.md: stale_after = '2027-03-15'`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
