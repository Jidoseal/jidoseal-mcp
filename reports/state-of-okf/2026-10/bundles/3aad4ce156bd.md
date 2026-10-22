# Bundle 3aad4ce156bd

Checked at commit `7db6469075f3` (2026-10-20T21:00:28Z), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `packs/okpack-ai-research/` (inferred: see the method) |
| `okf_version` declared | none |
| Concept files | 17 |
| OKF v0.2 conformance (§11, items 1–2) | not yet: 6 file(s) to change |
| Timestamps follow | no timestamp fields |
| Trust and lifecycle fields used | `sources` (9), `status` (1) |
| Trust tiers (§5.3) | unverified 11 |
| JidoSeal checker | score 22, tier none |

## What to change

### Files with no frontmatter block (6)

OKF v0.2 §11 asks every `.md` file other than `index.md` and `log.md` to start with a YAML frontmatter block holding a non-empty `type`. The smallest change is:

```yaml
---
type: Note
---
```

If these files are not meant to be part of the bundle (a README, a changelog), moving the bundle into its own folder keeps them out.

- `CHANGELOG.md`
- `CLAUDE.md`
- `README.md`
- `conformance/README.md`
- `subdomain/INSTALL-ALONGSIDE.md`
- `subdomain/PERSONA.md`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
