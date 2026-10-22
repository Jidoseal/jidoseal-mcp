# Bundle feba6cbcc048

Checked at commit `08c31f1c5d7b` (2026-08-20T08:57:58+02:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `(repository root)/` (declared by an index.md with okf_version) |
| `okf_version` declared | 0.1 |
| Concept files | 99 |
| OKF v0.2 conformance (§11, items 1–2) | not yet: 12 file(s) to change |
| Timestamps follow | no timestamp fields |
| Trust and lifecycle fields used | none |
| Trust tiers (§5.3) | unverified 87 |
| JidoSeal checker | score 29, tier none |

87 file(s) use the v0.1 `timestamp` key, which v0.2 supersedes with `generated: {by, at}` (§13.1); consumers may still fall back to it.

## What to change

### Files with no frontmatter block (12)

OKF v0.2 §11 asks every `.md` file other than `index.md` and `log.md` to start with a YAML frontmatter block holding a non-empty `type`. The smallest change is:

```yaml
---
type: Note
---
```

If these files are not meant to be part of the bundle (a README, a changelog), moving the bundle into its own folder keeps them out.

- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `docs/ROADMAP.md`
- `docs/superpowers/plans/2026-07-24-index-extensions.md`
- `docs/superpowers/plans/2026-07-25-tensions-layer.md`
- `docs/superpowers/plans/2026-08-04-synthesis-arc.md`
- `docs/superpowers/plans/2026-08-13-cross-cultural-breadth.md`
- `docs/superpowers/specs/2026-06-21-eos-knowledge-bricks-design.md`
- `docs/superpowers/specs/2026-07-26-reality-observation-kernel-truth-v4.2.md`
- `docs/superpowers/specs/2026-08-02-synthesis-arc-design.md`
- `docs/superpowers/specs/2026-08-13-cross-cultural-breadth-design.md`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
