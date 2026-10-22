# Bundle fdf6cfb8011d

Checked at commit `e34ae5845c5a` (2026-10-02T04:44:17+05:30), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `(repository root)/` (inferred: see the method) |
| `okf_version` declared | none |
| Concept files | 100 |
| OKF v0.2 conformance (§11, items 1–2) | not yet: 47 file(s) to change |
| Timestamps follow | no timestamp fields |
| Trust and lifecycle fields used | `status` (53) |
| Trust tiers (§5.3) | unverified 53 |
| JidoSeal checker | score 35, tier none |

## What to change

### Files with no frontmatter block (47)

OKF v0.2 §11 asks every `.md` file other than `index.md` and `log.md` to start with a YAML frontmatter block holding a non-empty `type`. The smallest change is:

```yaml
---
type: Note
---
```

If these files are not meant to be part of the bundle (a README, a changelog), moving the bundle into its own folder keeps them out.

- `Resources/note-templates/experiments/A1 Clinical sample collection.md`
- `Resources/note-templates/experiments/A2 Cell line authentication.md`
- `Resources/note-templates/experiments/A3 Cell culture maintenance.md`
- `Resources/note-templates/experiments/B1 DNA RNA extraction.md`
- `Resources/note-templates/experiments/B2 PCR and gel.md`
- `Resources/note-templates/experiments/B3 RT-qPCR.md`
- `Resources/note-templates/experiments/B4 Gene cloning.md`
- `Resources/note-templates/experiments/B5 Plasmid prep and transfection.md`
- `Resources/note-templates/experiments/B6 Knockdown knockout.md`
- `Resources/note-templates/experiments/B7 ChIP.md`
- `Resources/note-templates/experiments/B8 Agarose gel.md`
- `Resources/note-templates/experiments/C1 Protein extraction.md`
- `Resources/note-templates/experiments/C2 Western blot.md`
- `Resources/note-templates/experiments/C3 Immunoprecipitation.md`
- `Resources/note-templates/experiments/C4 ELISA.md`
- … and 32 more

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
