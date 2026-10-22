# Bundle e96eb13babc6

Checked at commit `79be36f55ae5` (2026-08-21T16:16:49+08:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `(repository root)/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 9 |
| OKF v0.2 conformance (§11, items 1–2) | not yet: 3 file(s) to change |
| Timestamps follow | no timestamp fields |
| Trust and lifecycle fields used | none |
| Trust tiers (§5.3) | unverified 6 |
| JidoSeal checker | score 22, tier none |

## What to change

### Files with no frontmatter block (1)

OKF v0.2 §11 asks every `.md` file other than `index.md` and `log.md` to start with a YAML frontmatter block holding a non-empty `type`. The smallest change is:

```yaml
---
type: Note
---
```

If these files are not meant to be part of the bundle (a README, a changelog), moving the bundle into its own folder keeps them out.

- `README.md`

### Files whose frontmatter does not parse (2)

The block between the `---` lines must be valid YAML that reads as a mapping. The parser's first message is shown for each file.

- `templates/concept-graph-template.md: frontmatter is not valid YAML: while parsing a block mapping`
- `templates/index-template.md: frontmatter is not valid YAML: while parsing a block mapping`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
