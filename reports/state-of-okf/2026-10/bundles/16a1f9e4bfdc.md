# Bundle 16a1f9e4bfdc

Checked at commit `ecf09ae3723c` (2026-09-20T12:18:36-04:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `(repository root)/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 116 |
| OKF v0.2 conformance (§11, items 1–2) | not yet: 5 file(s) to change |
| Timestamps follow | 2026-08-15 text |
| Trust and lifecycle fields used | `sources` (9), `generated` (111), `verified` (107), `status` (110), `stale_after` (110) |
| Trust tiers (§5.3) | human-reviewed 103, machine-confirmed 4, unverified 4 |
| JidoSeal checker | score 64, tier none |

## What to change

### Files with no frontmatter block (5)

OKF v0.2 §11 asks every `.md` file other than `index.md` and `log.md` to start with a YAML frontmatter block holding a non-empty `type`. The smallest change is:

```yaml
---
type: Note
---
```

If these files are not meant to be part of the bundle (a README, a changelog), moving the bundle into its own folder keeps them out.

- `AGENTS.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `README.md`
- `SECURITY.md`

### Values that follow the 2026-08-15 text (110)

These are valid under the text of 2026-08-15. To follow the current text (2026-08-21), write each as a datetime with a UTC offset, for example `2026-12-31` becomes `2026-12-31T00:00:00Z`. Both texts call themselves `okf_version: "0.2"`.

- `entities/application/act.md: stale_after = '2027-08-19'`
- `entities/application/agent-product.md: stale_after = '2027-08-19'`
- `entities/application/autonomous-agent.md: stale_after = '2027-08-19'`
- `entities/application/bill.md: stale_after = '2027-08-19'`
- `entities/application/buyer-persona.md: stale_after = '2027-08-19'`
- `entities/application/classification.md: stale_after = '2027-08-19'`
- `entities/application/cloud-infrastructure.md: stale_after = '2027-08-19'`
- `entities/application/clustering.md: stale_after = '2027-08-19'`
- `entities/application/customer-success-department.md: stale_after = '2027-08-19'`
- `entities/application/decision-maker.md: stale_after = '2027-08-29'`
- `entities/application/deep-learning.md: stale_after = '2027-08-19'`
- `entities/application/educational-institution.md: stale_after = '2027-08-19'`
- `entities/application/finance-department.md: stale_after = '2027-08-19'`
- `entities/application/global-corporation.md: stale_after = '2027-08-19'`
- `entities/application/human-resources-department.md: stale_after = '2027-08-19'`
- … and 95 more

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
