# Bundle 0f3dcfaffe5d

Checked at commit `9266f5107ef9` (2026-09-09T23:43:51+02:00), on 2026-10-22 (UTC), for the [State of OKF, October 2026](../README.md).

| | |
|---|---|
| Bundle folder | `(repository root)/` (inferred: see the method) |
| `okf_version` declared | none |
| Concept files | 46 |
| OKF v0.2 conformance (§11, items 1–2) | not yet: 23 file(s) to change |
| Timestamps follow | 2026-08-21 text |
| Trust and lifecycle fields used | `sources` (4), `generated` (1), `verified` (1), `status` (4), `stale_after` (1) |
| Trust tiers (§5.3) | human-reviewed 1, unverified 25 |
| JidoSeal checker | score 17, tier none |

## What to change

### Files with no frontmatter block (20)

OKF v0.2 §11 asks every `.md` file other than `index.md` and `log.md` to start with a YAML frontmatter block holding a non-empty `type`. The smallest change is:

```yaml
---
type: Note
---
```

If these files are not meant to be part of the bundle (a README, a changelog), moving the bundle into its own folder keeps them out.

- `00-installation-bonus.md`
- `00-installation.md`
- `CLAUDE.md`
- `README.md`
- `anmeldeformular-entwurf.md`
- `01-obsidian-und-markdown/1-obsidian-grundlagen.md`
- `01-obsidian-und-markdown/2-cheatsheet-markdown.md`
- `02-sync-mehrere-geraete/1-sync.md`
- `03-vaults-und-graph-view/1-vaults-und-graph-view.md`
- `04-ki-second-brain/1-plugin-setup-und-chat.md`
- `04-ki-second-brain/2-wissen-reinholen.md`
- `04-ki-second-brain/3-verdichten-und-wiederfinden.md`
- `04-ki-second-brain/4-dein-eigenes-wissen.md`
- `04-ki-second-brain/5-okf-format.md`
- `bonus-command-line/1-command-line.md`
- … and 5 more

### Files with frontmatter but no `type` (3)

`type` is the one key OKF v0.2 always requires (§4.1). Any short descriptive string works, for example `type: Reference`.

- `Clippings/Andrej Karpathy (@karpathy) auf X.md`
- `Clippings/Building Your Second Brain using Claude Code and Obsidian — Part 1.md`
- `Clippings/What is Google OKF (Open Knowledge Format).md`

## Check it again yourself

The `jidoseal_trust` tool of `jidoseal-mcp` (0.2.0 and later) applies the same per-file rules as this page, on your own machine: point it at the bundle folder. See [run it on your own folder](../README.md#run-it-on-your-own-folder). Something wrong here, or a different bundle folder? [Open an issue](https://github.com/Jidoseal/jidoseal-mcp/issues/new?template=state-of-okf.md).
