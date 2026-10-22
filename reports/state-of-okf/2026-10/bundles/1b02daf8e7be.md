# Bundle 1b02daf8e7be

Checked at commit `b3aa72de74d8` (2026-08-16T07:11:59-04:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `starter-kit/okf-knowledge-base/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.2 |
| Concept files | 2 |
| OKF v0.2 conformance (§11, items 1–2) | not yet: 1 file(s) to change |
| Timestamps follow | fits both texts |
| Trust and lifecycle fields used | `generated` (1) |
| Trust tiers (§5.3) | unverified 1 |
| JidoSeal checker | score 33, tier none |

## What to change

### Files with no frontmatter block (1)

OKF v0.2 §11 asks every `.md` file other than `index.md` and `log.md` to start with a YAML frontmatter block holding a non-empty `type`. The smallest change is:

```yaml
---
type: Note
---
```

If these files are not meant to be part of the bundle (a README, a changelog), moving the bundle into its own folder keeps them out.

- `AGENTS.md`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
